import json
import pandas as pd
from nltk.corpus import stopwords
from nltk.probability import FreqDist
stop_words = set(stopwords.words('english'))
f=open('output.json')
json_data=json.load(f)

#usually we use pd.read_json(json_data) to read data of json and convert it to df
# but sometimes we can directly make df if json had dictionaryinside like below.
newdf=pd.DataFrame(json_data) 

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

json_file=newdf.to_json('output.json',orient='records')       
print(newdf)
# with open('processed_guardian_data.json','w') as f:
#        f.write(json_file)


       


