import requests
from bs4 import BeautifulSoup
from dateutil.parser import parse
import pandas as pd
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))

# Making a GET request
r = requests.get('https://www.washingtonpost.com/world/')
 
soup = BeautifulSoup(r.content, 'html.parser')

headline=soup.find_all('h3', class_='font-md font-bold font--headline lh-sm gray-darkest hover-blue mb-0 antialiased mb-xxs')

date=soup.find_all('span', class_='font-xxxs font-light font--meta-text lh-sm gray-dark dot-xxs-gray-dark')

headlines=[]
pub_date=[]

for lines in date:
    singledate=parse(lines.text) ##converting given date to stripped date and yyyymmdd format
    singledate=singledate.strftime('%Y-%m-%d')
    pub_date.append(singledate)

for lines in headline:
    headlines.append(lines.text)

newdf=pd.DataFrame({'pub_data':pub_date,'headlines':headlines})

def remove_stopwords(text):
    words = text.split()
    words = [word.replace(',', '') for word in words]
    filtered_words = [word.lower() for word in words if word.lower() not in stop_words]
    return filtered_words

newdf['keywords']=newdf['headlines'].apply(remove_stopwords)

json_data=newdf.to_json(orient='records')

with open('output.json','w')as f:
    f.write(json_data)






