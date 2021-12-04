# -*- coding: utf-8 -*-
import json
import re
import urllib.request 
from urllib.parse import quote
from textblob import TextBlob 

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
        query_string=query_string+'and%20poi_name%3A'+poi_name
        print('updated : ==----',query_string)
    
    inurl = url_prefix + query_string + url_suffix
    print(inurl)
    data = urllib.request.urlopen(inurl)
    print(data)
    tweets = json.load(data)['response']['docs']
    final_tweets = []
    # result= json.dumps(data)
    for tweet in tweets:
        if(len(final_tweets) >20):
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
        for reply in replies:
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


    # return Response(final_tweets);
    # json_string = json.dumps(tweets)
    jsn_list = json.loads(json.dumps(tweets)) 
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
    



