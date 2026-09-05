import pandas as pd

# 读取 CSV/Excel
# 查看数据（head、info、describe）
# 处理空值
# 数据类型转换（把百分比转成数字）
# 筛选、排序
# 导出新 Excel
# 代码异常处理（文件不存在也不崩）

# 读取数据
df=pd.read_csv("data/tiobe-index.csv",encoding="utf-8")

#将值为null的数据改为无数据
df.fillna("无数据")   #inplace=True表示将修改后的数据保存到原数据中

#清洗数据，将带%的数据转为数字
def clean_data(data):
    return float(str(data).replace("%",""))

df["评分"]=df["Ratings"].apply(clean_data)        #创建新的列,apply()方法将clean_data()方法应用到每一行数据
#筛选、排序
df_good=df[df["评分"]>1].copy().sort_values("评分",ascending=False)

df_good.to_excel("data/tiobe-index-good.xlsx",index=False,engine="openpyxl")
