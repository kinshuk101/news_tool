import json
import pandas as pd
import requests

from datetime import datetime, timedelta, date
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))


today_year=date.today().strftime("%Y")
today_month=date.today().month
pub_date=[]
headlines=[]
keywords=[]
try:

    response_API=requests.get('https://api.nytimes.com/svc/archive/v1/2023/6.json?api-key=aWeeMXcQHVgh8o2w35JAEHnXdpVqGG3L')
    data = response_API.text
    parse_json = json.loads(data)

    for eachnews in parse_json['response']['docs']:
        pub_date.append(eachnews['pub_date'])
        headlines.append(eachnews['headline']['main'])
        newlist=[]
        for keywordofnews in eachnews['keywords']:
            newlist.append(keywordofnews['value'])
        keywords.append(newlist)

    def date_setup(obj):
        str=obj[0:10]
        return str 

    def Convert(obj):
        li = list(obj.split(","))  ##comma aate hi string bnado
        return li

    def string_in_keywords(obj):
        new_list=[]
        for string in obj:
            inside_brackets = False
            current_word = ""
            for c in string:
                if c == "(":
                    inside_brackets = True
                elif c == ")":
                    inside_brackets = False
                elif c == "," and not inside_brackets:
                    new_list.append(current_word.strip())
                    current_word = ""
                else:
                    current_word += c
            new_list.append(current_word.strip()) 
        return new_list

    newdf=pd.DataFrame({'pub_date':pub_date,'headlines':headlines,'keywords':keywords})

    newdf['pub_date']=newdf['pub_date'].apply(date_setup)

    newdf['keywords']=newdf['keywords'].apply(string_in_keywords)

    newdf['headlines']=newdf['headlines'].apply(Convert)

    newdf = newdf.groupby('pub_date', as_index=False).agg({
        'headlines': lambda x: [item for sublist in x for item in sublist],
        'keywords': lambda x: [item for sublist in x for item in sublist]
    })

    f=open('htfile.json')
    big_json=json.load(f)

    current_date = date.today()
    current_day=date.today().day
    # Calculate the previous month's last day by subtracting days from current date
    previous_month_last_day = current_date - timedelta(days=current_day)
    print((previous_month_last_day))

    old_jsondf=pd.DataFrame(big_json)    

    old_jsondf=old_jsondf[old_jsondf['pub_date']<=previous_month_last_day.strftime("%Y-%m-%d")]

    big_df    =pd.concat([old_jsondf,newdf],ignore_index=True)
    big_json  =big_df.to_json(orient='records')

    with open('processed_nytimes_data.json','w')as f:
        f.write(big_json)
except Exception as e:
    print (e)




