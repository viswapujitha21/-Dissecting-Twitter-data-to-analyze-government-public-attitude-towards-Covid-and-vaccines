# -*- coding: utf-8 -*-
import json
import re
import urllib.request 
from urllib.parse import quote


from django.http.response import JsonResponse
from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.
@api_view(['GET'])
def search(request):
    query = request.GET['query']
    core = 'CovidTweets'
    query = re.sub('\W+', ' ', query)
    query = query.strip()
    q_en = quote('(' + query+ ')')

    # variables to help formatting of input url
    or_seperator = "%20OR%20"
    url_prefix = "http://localhost:8983/solr/{core}/select?q=".format(core = core)
    url_suffix = "&wt=json&indent=true&rows=20"
    query_string = "text_txt_en:" + q_en + or_seperator + "text_en:" + q_en 


    inurl = url_prefix + query_string + url_suffix
    data = urllib.request.urlopen(inurl)
    docs = json.load(data)['response']['docs']
    return Response(docs);