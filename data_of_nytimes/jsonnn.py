
import json
import pandas as pd
from nltk.probability import FreqDist
import requests

global big_json
f=open('htfile.json')
big_json=json.load(f)

def making_big_data(f):
    data=json.loads(f)

    pub_date=[]
    headlines=[]
    keywords=[]

    for eachnews in data['response']['docs']:
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
    global big_json
    if(big_json=='{}'):
        big_json = newdf.to_json(orient='records')
    else:
        old_jsondf=pd.DataFrame(big_json)    
        big_df    =pd.concat([old_jsondf,newdf],ignore_index=True)
        big_json  =big_df.to_json(orient='records')
        
response_API=requests.get('https://api.nytimes.com/svc/archive/v1/2023/6.json?api-key=aWeeMXcQHVgh8o2w35JAEHnXdpVqGG3L')
data = response_API.text
making_big_data(data)

with open('processed_nytimes_data.json','w')as f:
    f.write(big_json)











    # #converting this dataframe back to json
    # json_data = newdf.to_json(orient='records')
    # #
# filtered_df = newdf.loc[(newdf['pub_date'] >= '2023-04-10') & (newdf['pub_date'] <= '2023-04-15')]
# filtered_df['keywords'].apply(collectdata)
# answer=FreqDist(answerlist)
# print(answer.most_common(50))




# #saving json file
# with open('data.json', 'w') as f:
#     json.dump(json_data, f)
# #


# #opening saved json file
# fnew=open('data.json')
# datanew=json.load(fnew)
# #

# #converting to dataframe the json file
# df = pd.read_json(datanew)
# print(df)
# #ab is df ko use krke data dalke ya fr data fetch krke use krlo or agr dal rhe ho data
# #to json m convert krke upload krdo#

