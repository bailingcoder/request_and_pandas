import random
import requests
from lxml import html
import pandas as pd
import os
from playwright.sync_api import sync_playwright
import time

url="https://movie.douban.com/top250"       #豆瓣电影url
#UA池
UA_POOL = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15"
]
def save_all_movies(all_movies):
    try:
        if not os.path.exists("data"):
            os.mkdir("data")
        df = pd.DataFrame(all_movies)  # 创建DataFrame
        df.to_csv("data/movies.csv", index=False, encoding="utf-8")
        print("保存成功")
    except Exception as e:
        print(f"保存失败：{e}")

def get_movie_info(movie_info_url):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)         #启动浏览器
            page=browser.new_page(user_agent=random.choice(UA_POOL))    #创建新的页面

            page.goto(movie_info_url,timeout=60000)         #访问页面
            time.sleep(random.uniform(2,5))         #随机等待
            #等待加载
            try:
                page.wait_for_load_state("networkidle",timeout=60000)       #等待页面加载完成
                page.wait_for_selector("#info", state="visible",timeout=60000)  # 显式等待 #info 元素出现
            except Exception as e:
                print(f"等待加载失败：{e}")

            title=page.locator("h1").inner_text()        #获取标题
            authors=[author.inner_text() for author in page.locator("#info span.attrs a[rel='v:directedBy']").all()]      #获取作者
            #获取编剧  ~：后面跟的兄弟元素
            editors_btn=page.locator("#info span:nth-child(3) span.attrs a[class='more-attrs']")
            if editors_btn.is_visible(timeout=2000):
                editors_btn.click()
                page.wait_for_timeout(500)
            editors=[editor.inner_text() for editor in page.locator("span.pl:has-text('编剧') ~ span.attrs a").all()]
            # 获取演员
            actors_btn=page.locator("#info span:nth-child(5) span.attrs a[class='more-attrs']")
            if actors_btn.is_visible(timeout=2000):
                actors_btn.click()
                page.wait_for_timeout(500)
            actors=[actor.inner_text() for actor in page.locator("span.attrs a[rel='v:starring']").all()]
            # 获取上映时间
            dates=[data.inner_text() for data in page.locator("#info span[property='v:initialReleaseDate']").all()]
            types=[type.inner_text() for type in page.locator("#info span[property='v:genre']").all()]      #获取类型
            language = page.locator("#info").text_content().split("语言:")[1].split()[0].strip()          #获取语言
            rating=page.locator("strong[property='v:average']").inner_text()        #获取评分
            # 获取简介
            expand_btn = page.locator("div.related-info a.a_show_full")
            # 如果按钮存在，就点击它
            if expand_btn.is_visible(timeout=2000):
                expand_btn.click()
                page.wait_for_timeout(500)  # 等简介展开
                intro = page.locator("#link-report-intra > span.all.hidden").inner_text().strip()       #获取简介
            else:
                page.wait_for_selector("#link-report-intra > span[property='v:summary']", state="visible",timeout=60000)  # 等待加载
                intro=page.locator("#link-report-intra > span[property='v:summary']").inner_text().strip()
            movie_info={
                "标题": title,         #标题
                "作者": authors,     # 作者
                "编剧": editors,     # 编剧
                "主演": actors,       # 主演
                "上映时间": dates,         # 上映时间
                "类型": types,         # 类型
                "语言": language,   # 语言
                "评分": rating,       # 评分
                "简介": intro          # 简介
            }
            return movie_info
    except Exception as e:
        print(f"获取信息失败：{e}")
        return None

def main():
    all_movies=[]       # 保存所有电影信息的列表
    for i in range(0,10):
        header={
            "User-Agent": random.choice(UA_POOL)
        }
        final_url=f"https://movie.douban.com/top250?start={i*25}&filter="       # 构造url
        response=requests.get(final_url,headers=header)
        html_doc=response.text
        selector=html.fromstring(html_doc)
        print(f"正在爬取第{i+1}页...")
        movie_list=selector.xpath("//div[@class='hd']")
        for movie in movie_list:
            movie_url=movie.xpath(".//a/@href")[0]
            print(f"正在爬取:{movie_url}")
            movie_info=get_movie_info(movie_url)        # 获取电影信息
            print(movie_info)
            if movie_info:
                all_movies.append(movie_info)

    #保存数据
    save_all_movies(all_movies)

if __name__ == '__main__':
    main()