from playwright.sync_api import sync_playwright
from lxml import html
import requests
import pandas as pd

BASE_URL="https://movie.douban.com/review/best"
header={
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"
}
def save_all_movies(all_movies):
    try:
        df=pd.DataFrame(all_movies)
        df.to_csv("电影信息.csv", index=False, encoding="utf-8")
        print("保存成功")
    except Exception as e:
        print(f"保存失败：{e}")

def get_movie_info(movie_url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(movie_url, timeout=60000)
        print(f"正在爬取:{movie_url}")
        page.wait_for_load_state("networkidle",timeout=60000)
        page.wait_for_selector("#info", state="visible", timeout=60000)
        title=page.locator("h1").inner_text()
        
        # 等待短评区域加载完成
        page.wait_for_selector("#hot-comments span.short", state="visible", timeout=30000)
        
        # 影评
        try:
            review = [review.inner_text() for review in page.locator("#hot-comments span.short").all()]
        except Exception as e:
            print(f"获取影评失败：{e}")
            review = []
            
        movie_info={
            "标题": title,
            "影评": review
        }
        browser.close()
        print(movie_info)
        return movie_info
def main():
    all_movies = []
    try:
        for page_num in range(0, 3):
            url = BASE_URL + f"?start={page_num * 20}"
            print(f"正在处理第{page_num + 1}页数据...")
            response = requests.get(url,headers=header)
            document = html.fromstring(response.text)
            movie_list = document.xpath("//*[@id='content']/div/div[1]/div/div")
            print(f"爬取到{len(movie_list)}部电影数据...")
            for movie in movie_list:
                movie_url = movie.xpath(".//a/@href")[0]
                if movie_url:
                    movie_info = get_movie_info(movie_url)
                    all_movies.append(movie_info)
    except Exception as e:
        print(f"处理数据失败：{e}")

    save_all_movies(all_movies)


