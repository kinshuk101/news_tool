import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
stop_words = set(stopwords.words('english'))

f=open("output.json")
json_data=json.load(f)
newdf=pd.DataFrame(json_data)

answerlist=[]
def collectdata(obj):
    for i in obj:
        answerlist.append(i)

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
json_data=newdf.to_json(orient='records')
with open("processed_reuters_data.json",'w')as f:
    f.write(json_data)

print(newdf)
# filtered_df = newdf.loc[(newdf['pub_date'] >= "2023-02-01") & (newdf['pub_date'] <= "2023-02-01")]
# filtered_df['keywords'].apply(collectdata)
# answer=FreqDist(answerlist)
# print(answer.most_common(70))

