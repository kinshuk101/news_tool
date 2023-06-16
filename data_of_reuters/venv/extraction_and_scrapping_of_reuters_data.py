import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
from datetime import datetime, timedelta
import calendar

start_date=datetime(2023,6,7)
end_date=datetime(2023,6,7)

using_date=start_date.strftime("%Y%m%d")

date=[]
headline=[]

bigdf=pd.DataFrame()

while(start_date<=end_date):
    newstoday=[]
    using_date=start_date.strftime("%Y%m%d")
    api="http://archive.org/wayback/available?url=reuters.com&timestamp={}060000".format(using_date)
    response=requests.get(api)
    data=response.text
    parse_json = json.loads(data)
    weburl = parse_json['archived_snapshots']['closest']['url']#the url needed to scrap
    r=requests.get(weburl)
    soup=BeautifulSoup(r.text,"lxml")
    news=soup.find_all('a',class_="text__text__1FZLe text__dark-grey__3Ml43 text__medium__1kbOh text__heading_5_and_half__3YluN heading__base__2T28j heading_5_half media-story-card__heading__eqhp9")
    for eachnews in news:
        newstoday.append(eachnews.text)

    date.append(start_date.strftime("%Y-%m-%d"))    
    headline.append(newstoday)
    start_date+=timedelta(days=1)    
    

print((headline))
print(date)    

f=open('output.json')
json_data=json.load(f)
olddf=pd.DataFrame(json_data) 
newdf=pd.DataFrame({'pub_date':date,'headlines':headline})
bigdf=pd.concat([olddf,newdf],ignore_index=True)
json_data=bigdf.to_json(orient="records")
with open('output.json','w') as f:
      f.write(json_data)

print(bigdf)


# jjson=newdf.to_json(orient="records")

