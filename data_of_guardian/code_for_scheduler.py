import json
import pandas as pd
import requests
from datetime import datetime, timedelta, date
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))

today = date(2023,6,7).strftime("%Y-%m-%d")

global pub_date
pub_date=[]
global headlines
headlines=[]
try:
        response_API=requests.get('https://content.guardianapis.com/search?from-date={}&to-date={}&page-size=100&q=world&api-key=d82d0bd6-3738-4c4c-8132-023942ee6836'.format(today,today))
        data = response_API.text
        parse_json = json.loads(data)

        date=today     
        headline=[]
        for result in parse_json['response']['results']:
            headline.append(result['webTitle'])
        
        pub_date.append(date)
        headlines.append(headline)
except Exception as e:
            print('error occured',e)

newdf=pd.DataFrame({'pub_date':pub_date,'headlines':headlines})


def convert_to_keywords(obj):
        tokens=[]
        for my_string in obj:
                # Split string into list of words
                words = my_string.split()
                # Remove stopwords from list of words
                words = [word.replace(',','') for word in words]
                words = [word.replace('|','') for word in words] 
                words = [word.replace('–','') for word in words]
                words = [word.lower() for word in words if word.lower() not in stop_words and word!='']

                # Add remaining words to list of tokens
                tokens.extend(words)
        return tokens

# print((convert_to_keywords(newdf['headlines'][0])))
newdf['keywords']=newdf['headlines'].apply(convert_to_keywords)
print(newdf['pub_date'])

f=open('processed_guardian_data.json')
json_data=json.load(f)
old_df=pd.DataFrame(json_data)

big_df=pd.concat([old_df,newdf],ignore_index=True)
json_file=big_df.to_json(orient='records')
with open('processed_guardian_data.json','w') as f:
       f.write(json_file)