# -*- coding: utf-8 -*-
import json
import re
import urllib.request 
from urllib.parse import quote
from textblob import TextBlob 
import matplotlib.pyplot as plt
import pandas as pd
from plotly.offline import plot
import plotly.express as px

from django.http.response import JsonResponse
from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.
@api_view(['GET'])
def search(request):
    #query = request.session['search']
    print(request)
    query = request.GET['query']
    print(query)
    # poi = request.GET['poi_name']
    print(request.GET.get('poi_name'))
    poi_name= request.GET.get('poi_name')
    country= request.GET.get('country')
    language= request.GET.get('language')
    core = 'CovidTweets'
    query = re.sub('\W+', ' ', query)
    query = query.strip()
    q = quote('(' + query+ ')')

    # variables to help formatting of input url

    or_seperator = "%20OR%20"
    and_seperator = "%20AND%20"
    url_prefix = "http://3.21.190.202:8983/solr/{core}/select?q=".format(core = core)
    url_suffix = "&wt=json&indent=true&rows=200"
    query_string = "-replied_to_tweet_id:%5B*%20TO%20*%5D%26"+ and_seperator +"tweet_text:" + q
    print('querystring-----  ',query_string)
    if poi_name:
        query_string=query_string+ and_seperator +'poi_name:'+poi_name
        print('updated : ==----',query_string)

    if country:
        query_string=query_string + and_seperator +'country:'+country

    if language:
        query_string=query_string+ and_seperator+'tweet_lang:'+language
    
    print(query_string)    
    inurl = url_prefix + query_string + url_suffix
    print(inurl)
    data = urllib.request.urlopen(inurl)
    print(data)
    tweets = json.load(data)['response']['docs']
    final_tweets = []
    other_tweets = []
    trendingTopics=[]
    # result= json.dumps(data)
    for tweet in tweets:
        if(len(final_tweets) > 20):
            break
        tweet['sentiment'] = analyze_sentiment(tweet['tweet_text'])

        # sentiment of the tweet
        positive_replies = 0
        negative_replies = 0
        neutral_replies = 0

        #collecting replies
        reply_query_string = "replied_to_tweet_id:" + tweet['id']

        inurl = url_prefix + reply_query_string + url_suffix
        data = urllib.request.urlopen(inurl)
        replies = json.load(data)['response']['docs']
        count = 0
        for reply in replies:
            count+=1
            if(count >20):
                break
            if(analyze_sentiment(reply['tweet_text']) == 'positive'):
                positive_replies+=1
            if(analyze_sentiment(reply['tweet_text']) == 'negative'):
                negative_replies+=1
            if(analyze_sentiment(reply['tweet_text']) == 'neutral'):
                neutral_replies+=1
        tweet['replies'] = replies

        tweet['positive_replies'] = positive_replies
        tweet['negative_replies'] = negative_replies
        tweet['neutral_replies'] = neutral_replies
        # final_tweets.append(tweet)
        if(len(replies) > 0):
            final_tweets.append(tweet)
        else:
            other_tweets.append(tweet)

    i = 0
    while(len(final_tweets) < 20 and i < len(other_tweets)):
        final_tweets.append(other_tweets[i])
        i+=1


    # return Response(final_tweets);
    # json_string = json.dumps(tweets)
    jsn_list = json.loads(json.dumps(final_tweets)) 
    # for lis in jsn_list:
    #        for key,val in lis.items():
    context={}
    # return render(request, "home.htm", context)
    return render(request, "home.htm", {'time_series_json_string': jsn_list})
           

    

    #context={"text":"test text"}
    # return JsonResponse(request,'home.htm',tweets[0],safe=False)
    #return render(request,'home.htm',context)

def clean_tweet(tweet):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

def analyze_sentiment(tweet):
    analysis = TextBlob(clean_tweet(tweet))
    
    if analysis.sentiment.polarity > 0:
        return 'positive'
    elif analysis.sentiment.polarity == 0:
        return 'neutral'
    else:
        return 'negative'
    
 
def home_page(request):
    if request.method == 'GET': 
        searched = request.GET.get('searched')
        # print(search)
        context = {}
    return render(request, 'index.htm',{})
    
    # return render(request, 'index.htm', {})
    
def overview(request):
    df1 = pd.DataFrame(dict(Topics=['COVID19', 'Unite2FightCorona', 'LargestVaccineDrive', 'DoYourJob', 'ActOnClimate',
                                       'MannKiBaat','Verdict','Tokyo2020','BidenBorderCrisis','Paralympics','HealthForAll',
                                       'COVIDCharcha','WearAMask','DeltaVariant','Singhuborder','WeCanDoThis','Cheer4India']))
    df2 = pd.DataFrame(dict(Count=[853,174,133,83,53,49,45,45,44,32,28,28,23,21,20,19,18]))
    fig = px.bar(df1, x=df1.Topics, y=df2.Count, color=df1.Topics)
    fig.update_layout(
    autosize=False,
    width=900,
    height=400,
    yaxis=dict(
         title_text="Tweet count",
    #     ticktext=["Very long label", "long label", "3", "label"],
    #     tickvals=[1, 2, 3, 4],
    #     tickmode="array",
    #     titlefont=dict(size=30),
    )
    )
    fig.update_yaxes(automargin=True)
    plt_div = plot(fig, output_type='div')
    return render(request, "overview.htm", {'plot_div':plt_div})
    
    
            
    # return render(request, 'overview.htm',{})
     
        



