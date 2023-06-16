import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
from datetime import datetime, timedelta,date
import calendar
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
stop_words = set(stopwords.words('english'))

newstoday=[]
pub_date=[]
headline=[]
today=date.today().strftime("%Y-%m-%d")
api_date=date.today()
api_date=api_date-timedelta(days=1)
api_date=api_date.strftime("%Y%m%d")

api="http://archive.org/wayback/available?url=reuters.com&timestamp={}050000".format(api_date)
print(api)
response=requests.get(api)
data=response.text
parse_json = json.loads(data)
weburl = parse_json['archived_snapshots']['closest']['url']
r=requests.get(weburl)
soup=BeautifulSoup(r.text,"lxml")
news=soup.find_all('a',class_="text__text__1FZLe text__dark-grey__3Ml43 text__medium__1kbOh text__heading_5_and_half__3YluN heading__base__2T28j heading_5_half media-story-card__heading__eqhp9")
for eachnews in news:
    newstoday.append(eachnews.text)

pub_date.append(today)    
headline.append(newstoday)

newdf=pd.DataFrame({'pub_date':pub_date,'headlines':headline})

def removelast(obj):
    for i in range(len(obj)):
        obj[i]=obj[i].replace(", article with image","")
        obj[i]=obj[i].replace(", article with gallery","")
        obj[i]=obj[i].replace(", article with video","")
        obj[i]=obj[i].replace("Morning bid: ","")
        obj[i]=obj[i].replace("Morning Bid: ","")
        obj[i]=obj[i].replace(",","")
    return obj

def process(obj):
    token_kumar=[]
    for i in range(len(obj)):
        token_kumar+=(word_tokenize(obj[i]))
    filtered_token=[token.lower() for token in token_kumar if token.lower() not in stop_words]
    return filtered_token    

newdf['headlines']=newdf['headlines'].apply(removelast)

newdf['keywords']=newdf['headlines'].apply(process)



f=open('processed_reuters_data.json')
json_data=json.load(f)
olddf=pd.DataFrame(json_data) 

bigdf=pd.concat([olddf,newdf],ignore_index=True)
json_data=bigdf.to_json(orient="records")
# with open('processed_reuters_data.json','w') as f:
#       f.write(json_data)
print(bigdf)
      