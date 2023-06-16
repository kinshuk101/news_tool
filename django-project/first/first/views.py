from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render
import pandas as pd
import nltk
from nltk.probability import FreqDist
from django.templatetags.static import static
import json


def homePage(request):
    data={}
    startd = request.POST.get('start_date')
    endd=request.POST.get('end_date')
    newspaper=request.POST.get('newspaper')
    try:
        answerlist=[]
        def collectdata(obj):
            for i in obj:
                if len(i)<5:
                    continue
                answerlist.append(i)

        f=open('static/{}'.format(newspaper))
        json_data=json.load(f)
        newdf=pd.DataFrame(json_data)

        filtered_df = newdf.loc[(newdf['pub_date'] >= startd) & (newdf['pub_date'] <= endd)]
        #when date is taken and applied on df

        filtered_df['keywords'].apply(collectdata)
        answer=FreqDist(answerlist)
        for element in answer.most_common(70):
            data[element[0]]=element[1]
        data['startd']=startd
        data['endd']=endd
        data['newspaper']=newspaper
    except Exception as e:
        print("Error occurred ", e)
        pass
    return render(request,"index.html",{'data':data})













