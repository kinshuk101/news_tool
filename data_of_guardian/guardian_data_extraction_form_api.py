import json
import pandas as pd
import requests
from datetime import datetime, timedelta, date
import calendar

global_df=pd.DataFrame()
# today = date.today()
# global pub_date
# pub_date=[]
# global headlines
# headlines=[]
# print(today)
# try:
#         response_API=requests.get('https://content.guardianapis.com/search?from-date={}&to-date={}&page-size=100&q=world&api-key=d82d0bd6-3738-4c4c-8132-023942ee6836'.format(today,today))
#         data = response_API.text
#         parse_json = json.loads(data)

#         date=today     
#         headline=[]
#         for result in parse_json['response']['results']:
#             headline.append(result['webTitle'])
        
#         pub_date.append(date)
#         headlines.append(headline)
# except Exception as e:
#             print('error occured',e)

# newdf=pd.DataFrame({'pub_date':pub_date,'headlines':headlines})
# print(newdf)

start_date = datetime(2023, 5, 1)  # start date in ymd format
end_date = datetime(2023, 6, 6)  # end date in ymd format

current_date = start_date
global pub_date
pub_date=[]
global headlines
headlines=[]
while current_date <= end_date:
    using_date=current_date.strftime('%Y-%m-%d')
    try:
            response_API=requests.get('https://content.guardianapis.com/search?from-date={}&to-date={}&page-size=100&q=world&api-key=d82d0bd6-3738-4c4c-8132-023942ee6836'.format(using_date,using_date))
            data = response_API.text
            parse_json = json.loads(data)

            date=using_date     
            headline=[]
            for result in parse_json['response']['results']:
                headline.append(result['webTitle'])
            
            pub_date.append(date)
            headlines.append(headline)
    except Exception as e:
              print('error occured',e)
    days_in_month = calendar.monthrange(current_date.year, current_date.month)
    if current_date.day == days_in_month:
        current_date += timedelta(days=1)
        current_date = current_date.replace(day=1)
        current_date = current_date.replace(month=current_date.month+1)
    else:
        current_date += timedelta(days=1)


newdf=pd.DataFrame({'pub_date':pub_date,'headlines':headlines})
print(newdf)
json_data=newdf.to_json(orient='records')
with open('output.json','w') as f:
      f.write(json_data)
#fetching for month february
# global_feb=pd.DataFrame()
# for x in range(0,29):
#         try:
#             response_API=requests.get('https://content.guardianapis.com/search?from-date=2023-05-08&to-date=2023-05-08&page-size=100&q=world&api-key=d82d0bd6-3738-4c4c-8132-023942ee6836')
#             data = response_API.text

#         except Exception as e:
#               print('error occured',e,x)

# response_API=requests.get('https://content.guardianapis.com/search?from-date=2023-05-08&to-date=2023-05-08&page-size=100&q=world&api-key=d82d0bd6-3738-4c4c-8132-023942ee6836')
# data = response_API.text

# parse_json = json.loads(data)

# pub_date=[]
# headlines=[]
# for result in parse_json['response']['results']:
#     pub_date.append(result['webPublicationDate'])
#     headlines.append(result['webTitle'])

# newdf=pd.DataFrame({'pub_date':pub_date,'headlines':headlines})
# print (newdf)    

# print(len(parse_json['response']['results']))
