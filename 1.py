import datetime as dt
import requests
import pandas as pd
import json

data = []

print("Hello Python!!")
print(f"今天日期{dt.datetime.today().strftime("%Y%m%d")}")

#原始資料連結
#https://api.cnyes.com/media/api/v1/newslist/category/headline?startAt=1751508401&endAt=1754100401&isIndexHeadline=0&isCategoryHeadline=0&limit=10

#鉅亨網爬蟲程式
url="https://api.cnyes.com/media/api/v1/newslist/category/headline"  #連結
#payload= {"page":1,"limit":30,"startAt":1752645542,"endAt":1753509542}  #參數
#參數
payload= {
	"page":1,"limit":30,
	"startAt":int((dt.datetime.today() - dt.timedelta(days=10)).timestamp()),
	"endAt":int(dt.datetime.today().timestamp())
	}  
res=requests.get(url, params = payload)  #連線鉅亨網
jd= json.loads(res.text)  #解析json轉成dict
data.append(pd.DataFrame(jd['items']['data']))

for i in range(2, jd['items']['last_page'] +1):
	print("i = " , i)
	payload["page"] = i
	res=requests.get(url, params = payload)  #連線鉅亨網
	jd= json.loads(res.text)  #解析json轉成dict
	data.append(pd.DataFrame(jd['items']['data']))


#df= pd.DataFrame(jd["items"]["data"])  #取出新聞資料
df= pd.concat(data, ignore_index = True)  #取出新聞資料
df= df[["newsId","title","summary"]]  #取出特定欄位

df["link"]=df["newsId"].apply(lambda x: "https://m.cnyes.com/new/id/" + str(x))  #建立連結

#輸出時，略過index
df.to_csv("news.csv", encoding='utf-8-sig', index=False)
df.to_excel("news.xlsx", index=False)

print(df)

