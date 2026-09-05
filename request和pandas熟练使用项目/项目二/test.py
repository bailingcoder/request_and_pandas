import requests
import re

# 第2页链接：start=25
url = "https://movie.douban.com/top250?start=25"
headers = {
    "User-Agent": "Mozilla/5.0"
}

resp = requests.get(url, headers=headers)
html = resp.text

titles = re.findall(r'<span class="title">(.*?)</span>', html)
print("豆瓣 Top250 第2页电影名：")
for t in titles:
    if '/' not in t:
        print(t)