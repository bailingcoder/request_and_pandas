from lxml import html
import pandas as pd
import requests
import os
from requests.auth import HTTPBasicAuth

base_url="https://ssr1.scrape.center/detail/"
headers={
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"
}
auth=HTTPBasicAuth("admin", "admin")

all_movies=[]
for i in range(1,51):
    url=base_url+str(i)
    response=requests.get(url,auth=auth ,headers=headers)
    document=html.fromstring(response.text)
    title=document.xpath("//*[@id='detail']/div[1]/div/div/div[1]/div/div[2]/a/h2/text()")     #获取标题
    types=document.xpath("//*[@id='detail']/div[1]/div/div/div[1]/div/div[2]/div[1]/button/span/text()")    #获取类型
    times=document.xpath("//*[@id='detail']/div[1]/div/div/div[1]/div/div[2]/div[2]/span[3]/text()")  #获取上映时间
    inro=document.xpath("//*[@id='detail']/div[1]/div/div/div[1]/div/div[2]/div[4]/p/text()")[0].strip()  #获取简介
    authors=document.xpath("//*[@id='detail']/div[2]/div/div/div/div/div/p/text()")         #获取作者
    actors=document.xpath("//*[@id='detail']/div[3]/div/div/div/div/div/p[1]/text()")       #获取主演
    movie_info={
        "标题":title,
        "类型":types,
        "上映时间":times,
        "简介":inro,
        "作者":authors,
        "主演":actors
    }
    all_movies.append(movie_info)
if not os.path.exists("data"):
    os.mkdir("data")
try:
    df = pd.DataFrame(all_movies)
    df.to_csv("data/movie.csv", index=False, encoding="utf-8")
    print("保存成功")
except Exception as e:
    print(f"保存失败：{e}")