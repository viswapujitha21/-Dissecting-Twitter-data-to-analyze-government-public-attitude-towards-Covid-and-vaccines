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
import plotly.graph_objects as go

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
    url_suffix = "&wt=json&indent=true&rows=20"
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
    n_positive=0 
    n_negative=0
    n_neutral=0
    n_positive_replies = 0
    n_negative_replies = 0
    n_neutral_replies = 0
    n_India_cnt=0
    n_Russia_cnt=0
    n_USA_cnt=0

    for tweet in tweets:
        if(len(final_tweets) > 20):
            break
        tweet['sentiment'] = analyze_sentiment(tweet['tweet_text'])
        if tweet['sentiment'] == 'positive' :
            n_positive+=1
        elif tweet['sentiment'] == 'negative' :
            n_negative+=1    
        else :
            n_neutral+=1

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

        n_positive_replies +=positive_replies
        n_negative_replies +=negative_replies
        n_neutral_replies +=neutral_replies

        # final_tweets.append(tweet)
        if(len(replies) > 0):
            final_tweets.append(tweet)
        else:
            other_tweets.append(tweet)

    i = 0
    while(len(final_tweets) < 20 and i < len(other_tweets)):
        final_tweets.append(other_tweets[i])
        i+=1

    #General tweet graph
    df1 = pd.DataFrame(dict(Sentiment=['positive','negative','neutral']))
    df2 = pd.DataFrame(dict(Count=[n_positive,n_negative,n_neutral]))
    fig = px.bar(df1, x=df1.Sentiment, y=df2.Count, color=df1.Sentiment)
    fig.update_layout(
    autosize=False,
    width=850,
    height=500,
    yaxis=dict(
         title_text="Tweet Count",
    #     ticktext=["Very long label", "long label", "3", "label"],
    #     tickvals=[1, 2, 3, 4],
    #     tickmode="array",
    #     titlefont=dict(size=30),
    )
    )
    fig.update_yaxes(automargin=True)
    plt_div = plot(fig, output_type='div')

    

    #Replies Graph
    df3 = pd.DataFrame(dict(Replies=['positive','negative','neutral']))
    df4 = pd.DataFrame(dict(Count=[n_positive_replies,n_negative_replies,n_neutral_replies]))
    fig1 = px.bar(df3, x=df3.Replies, y=df4.Count, color=df3.Replies)
    fig1.update_layout(
    autosize=False,
    width=850,
    height=500,
    yaxis=dict(
         title_text="Reply Count",
    #     ticktext=["Very long label", "long label", "3", "label"],
    #     tickvals=[1, 2, 3, 4],
    #     tickmode="array",
    #     titlefont=dict(size=30),
    )
    )
    fig1.update_yaxes(automargin=True)
    fig1.update_xaxes(title_text="Reply Responses")
    plt_div1 = plot(fig1, output_type='div')

    # return Response(final_tweets);
    # json_string = json.dumps(tweets)
    jsn_list = json.loads(json.dumps(final_tweets)) 
    # for lis in jsn_list:
    #        for key,val in lis.items():
    context={}
    # return render(request, "home.htm", context)
    return render(request, "home.htm", {'time_series_json_string': jsn_list,'plot_div':plt_div,'plot_div_replies':plt_div1})
           

    

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
    title = 'Trending topics',
    autosize=False,
    width=1560,
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
        #Country Graph
    labels = ['India','Mexico','USA']
    values = [14236,11059,10533]
    ndata = 100
    fig2 = {
        'data': [{'labels': labels,
            'values': values,
            'type': 'pie',
            'textposition':"inside",
            'textinfo':"percent",
            'textfont':{'size':12},
            'showlegend':True}],
        'layout': {'title': '',
            'showlegend':True,
            'height':600,
            'width':600,
            'autosize':False,
            'margin':{'t':70,'l':95,'r':10,'b':20},
            'separators':'.,',
            }
    }
    # fig2.update_traces(textposition='inside', textinfo='percent')
    plt_div2 = plot(fig2, output_type='div')

    #Language Graph
    lang_labels = ['en','und','es','fr','tr','pt','ca','sv','tl','cy','da','et','or','hi','gu','ta','mr','bn',
    'pa','ne','ml','iw','te','kn','de','in','it','nl','ro','is','ru','sl','lt','ja','hu','zh','vi','ht','fa','ar','my','no','pl','eu','lv','cs','fi','ur']
    lang_values = [14328,3639,10236,39,9,136,30,8,141,7,6,81,25,6044,110,47,53,121,64,48,27,3,12,8,18,352,26,8,6,1,1,6,15,5,7,16,10,72,2,2,1,4,7,9,14,11,11,2]
    ndata = 100
    fig3 = {
        'data': [{'labels': lang_labels,
            'values': lang_values,
            'type': 'pie',
            'textposition':"inside",
            'textinfo':"percent",
            'textfont':{'size':12},
            'showlegend':True}],
        'layout': {'title': '',
            'showlegend':True,
            'height':600,
            'width':600,
            'autosize':False,
            'margin':{'t':70,'l':95,'r':10,'b':20},
            'separators':'.,'}
    }
    plt_div3 = plot(fig3, output_type='div')

    # POI's Covid and non-covid tweets

    poi=['CDCgov', 'JoeBiden', 'KamalaHarris','BarackObama','tedcruz','MoHFW_INDIA','narendramodi','RahulGandhi',
    'AmitShah','ArvindKejriwal','SSalud_mx','lopezobrador','m_ebrard','PRI_Nacional','PRDMexico']

    fig4 = go.Figure(data=[
        go.Bar(name='Covid Tweet Count', x=poi, y=[747, 249, 357, 248, 171, 106, 246, 286, 87, 297, 279, 86, 93, 28, 91]),
        go.Bar(name='Non-Covid Tweet Count', x=poi, y=[321, 801, 699, 876, 940, 434, 872, 887, 926, 772, 824, 1040, 914, 1033, 1025])
    ])
    # Change the bar mode
    fig4.update_layout(barmode='group',title = 'Covid and Non-Covid Tweet distribution of POI')
    plt_div4 = plot(fig4, output_type='div')
    #fig4.show()
    
    
    #Covid and Vaccine Tweet Graph
    overall_labels = ['Covid Tweet Count','Vaccine Tweet Count']
    overall_values = [6659,6067]
    ngdata = 100
    fig5 = {
        'data': [{'labels': overall_labels,
            'values': overall_values,
            'type': 'pie',
            'textposition':"inside",
            'textinfo':"percent",
            'textfont':{'size':12},
            'showlegend':True}],
        'layout': {'title': '',
            'showlegend':True,
            'height':600,
            'width':600,
            'autosize':False,
            'margin':{'t':70,'l':95,'r':10,'b':20},
            'separators':'.,'}
    }
    plt_div5 = plot(fig5, output_type='div')
    
    
    
    return render(request, "overview.htm", {'plot_div':plt_div,'plot_div_country':plt_div2,'plot_div_lang':plt_div3,'plt_div_overall':plt_div5,'plot_div_tweets':plt_div4})
    
    
            
    # return render(request, 'overview.htm',{})
     
        



