import requests
import pandas as pd

BASE_URL="https://spa1.scrape.center/api/movie"
header={
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"
}
all_movies=[]
for num in range(11,21):
    url=BASE_URL+f"/{num}/"
    response=requests.get(url,headers=header)
    data=response.json()
    name=data.get("name")
    alias=data.get("alias")
    cover=data.get("cover")
    categories=data.get("categories")
    regions=data.get("regions")
    actors=[actor["name"] for actor in data.get("actors")]
    movie_info={
        "名称": name,
        "别名": alias,
        "封面": cover,
        "类别": categories,
        "地区": regions,
        "主演": actors
    }
    print(movie_info)
    all_movies.append(movie_info)

df=pd.DataFrame(all_movies)
df.to_csv("movie.csv",index=False,encoding="utf-8")
print("保存成功")



