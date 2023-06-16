from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render
import pandas as pd
import numpy as np
import nltk
from nltk.corpus import stopwords
stop = set(stopwords.words('english'))
from nltk.probability import FreqDist
from django.templatetags.static import static

import csv
import os


def homePage(request):
    data={}
    try:
        startd = request.POST.get('start_date')
        endd=request.POST.get('end_date')
        answerlist=[]
        def collectdata(obj):
            for i in obj:
                answerlist.append(i)

        def removecommaspace(obj):
            obbj=obj.replace(", ",",")

        def removespace(obj):
            obbj=obj.replace(" ","")
            return obbj

        def removecomma(obj):
            obbj=obj.replace(","," ")
            return obbj

        def stem(obj):
            L=[]
            for i in obj.split():
                L.append(i)
            return L

        def apply_comma(obj):
            if type(obj) == str:
                new_obj = obj + ","
                return new_obj
            else:
                return obj
        # file = open('static/twomonthdatafeb_april.csv','w')
        newdf = pd.read_csv('static/twomonthdatafeb_april.csv')
        
        newdf=newdf[['pub_date','keywords','headlines']]

        newdf['keywords']=newdf['keywords'].apply(removespace)
        newdf['keywords']=newdf['keywords'].apply(removecomma)

        filtered_df = newdf.loc[(newdf['pub_date'] >= startd) & (newdf['pub_date'] <= endd)]
        #when date is taken and applied on df

        filtered_df['keywords']=filtered_df['keywords'].apply(stem)
        filtered_df['keywords'].apply(collectdata)
        answer=FreqDist(answerlist)
        for element in answer.most_common(70):
            data[element[0][1:-1]]=element[1]
        # print((data))
    except Exception as e:
        print("Error occurred ", e)
        pass
    return render(request,"index.html",{'data':data})








def userform(request):
    finalans={}
    try:
        if request.method=='GET':
            startd=request.GET['startd']
            endd=request.GET['endd']
            finalans={
                'startd':startd,
                'endd':endd
            }
            # url = "/about-us/token={}".format(finalans)
            # return HttpResponseRedirect(url)
    except:
        pass
    return render(request,"userform.html",finalans)
