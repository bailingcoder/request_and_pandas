from lxml import html
import pandas as pd
import requests
import os

url="https://www.tiobe.com/tiobe-index"
header={
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"
}
# 发送请求，获取响应数据
response=requests.get(url,headers=header)
document=html.fromstring(response.text)

# 获取表头
heal_list=document.xpath("//table[@id='top20']/thead/tr/th/text()")
heal_list.pop(2)
list_tbody=[]

#获取前20名表格中的数据
table_top20=document.xpath("//table[@id='top20']/tbody/tr")
for tr in table_top20:
    table_td=[td for td in tr.xpath("./td/text()")]
    list_tbody.append(table_td)

#获取21-50名表格中的数据
other_tables=document.xpath("//*[@id='otherPL']/tbody/tr")
for tr in other_tables:
    other_td=[td for td in tr.xpath("./td/text()")]
    other_td.insert(1,"")
    other_td.insert(4,"")
    list_tbody.append(other_td)

#保存数据
df=pd.DataFrame(list_tbody,columns=heal_list)
if not os.path.exists("data"):
    os.mkdir("data")
with open("data/tiobe-index.csv", "w", encoding="utf-8", newline="") as f:
    df.to_csv(f, index=False,encoding="utf-8")
    print("保存成功")