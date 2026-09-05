import csv
import requests
from lxml import html
import os

base_url="https://www.tiobe.com"
url="https://www.tiobe.com/tiobe-index"

response=requests.get(url)          #发送请求，获取响应数据
document=html.fromstring(response.text)         #解析数据，将其转换为一个文档对象

list_head=document.xpath("//table[@id='top20']/thead/tr/th/text()")         #获取表头

list_tbody=[]
list_tr=document.xpath("//table[@id='top20']/tbody/tr")
for tr in list_tr:
    list_td=[]
    #获取排名变化趋势图片
    change_img=tr.xpath("./td[3]/img/@src")
    change_img_url=change_img[0] if change_img else ""      #获取图片的URL如果存在，则返回图片的URL，否则返回空字符串

    #获取编程语言图片
    lang_img=tr.xpath("./td[4]/img/@src")
    lang_img_url=lang_img[0] if lang_img else ""

    #拼接完整URL（因为src是相对路径）
    if not change_img_url.startswith("http"):
        change_img_url=base_url+change_img_url
    if not lang_img_url.startswith("http"):
        lang_img_url=base_url+lang_img_url

    list_td=[td for td in tr.xpath("./td/text()")]
    list_td.insert(2, change_img_url)
    list_td.insert(3, lang_img_url)
    list_tbody.append(list_td)

#保存图片到本地
if not os.path.exists("data/images"):
    os.makedirs("data/images")
    for list_td in list_tbody:
        for url_img in list_td[2 :4]:
            if url_img:
                img_name=url_img.split("/")[-1]         #获取图片名称
                img_path=f"data/images/{img_name}"      #拼接图片保存路径
                if not os.path.exists(img_path):
                    img_response=requests.get(url_img)      #发送请求，获取图片数据
                    img=img_response.content        #获取图片数据
                    with open(img_path, "wb") as f:
                        f.write(img)
if not os.path.exists("data"):
    os.mkdir("data")
with open("data/tiobe-index.csv", "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(list_head)
    writer.writerows(list_tbody)


    # import csv
    # import requests
    # from lxml import html
    # import os
    #
    # url = "https://www.tiobe.com/tiobe-index"
    # response = requests.get(url)
    # document = html.fromstring(response.text)
    #
    # # 获取表头
    # list_head = document.xpath("//table[@id='top20']/thead/tr/th/text()")
    #
    # # 获取数据行（包含图片信息）
    # list_tbody = []
    # list_tr = document.xpath("//table[@id='top20']/tbody/tr")
    # for tr in list_tr:
    #     list_td = []
    #
    #     # 获取排名变化趋势图片
    #     change_img = tr.xpath("./td[1]/img/@src")
    #     change_img_url = change_img[0] if change_img else ""
    # //*[@id="top20"]/tbody/tr[1]/td[4]/img
    #//*[@id="top20"]/tbody/tr[1]/td[3]/img
    #     # 获取编程语言图片
    #     lang_img = tr.xpath("./td[3]/img/@src")
    #     lang_img_url = lang_img[0] if lang_img else ""
    #
    #     # 拼接完整URL（因为src是相对路径）
    #     if change_img_url and not change_img_url.startswith("http"):
    #         change_img_url = url.rstrip("/") + "/" + change_img_url.lstrip("/")
    #     if lang_img_url and not lang_img_url.startswith("http"):
    #         lang_img_url = url.rstrip("/") + "/" + lang_img_url.lstrip("/")
    #
    #     # 获取其他文本数据
    #     for td in tr.xpath("./td"):
    #         text = td.xpath("string()").strip()  # 获取td下的所有文本（排除img）
    #         if text:
    #             list_td.append(text)
    #
    #     list_tbody.append(list_td + [change_img_url, lang_img_url])
    #
    # # 保存图片到本地
    # if not os.path.exists("data/images"):
    #     os.makedirs("data/images")
    #
    # for i, urls in enumerate([(row[-2], row[-1]) for row in list_tbody]):
    #     for url_img in urls:
    #         if url_img:
    #             img_name = url_img.split("/")[-1]
    #             img_path = f"data/images/{img_name}"
    #             if not os.path.exists(img_path):
    #                 img_response = requests.get(url_img)
    #                 with open(img_path, "wb") as img_f:
    #                     img_f.write(img_response.content)
    #             print(f"已保存: {img_name}")
    #
    # # 保存CSV数据
    # if not os.path.exists("data"):
    #     os.mkdir("data")
    #
    # with open("data/tiobe-index.csv", "w", encoding="utf-8", newline="") as f:
    #     writer = csv.writer(f)
    #     writer.writerow(list_head + ["变化趋势图", "语言图标"])
    #     writer.writerows(list_tbody)
