import os
from typing import final
import pysolr
import requests
import json
import pickle

IP = "localhost"
path = "C:/Software/solr-8.10.1/bin/solr"

# to start the solr
# cd "C:\Software\solr-8.10.1\bin"
# solr start
core = 'CovidTweets'

def delete_core(core):
    print("core", core)
    try:
        print(os.system('{path} delete -c {core}'.format(path=path, core=core)))
    except:
        pass


def create_core(core):
    print(os.system(
        '{path} create -c {core} -n data_driven_schema_configs'.format(
            path=path,core=core)))


class Indexer:
    def __init__(self,core_name):
        self.core_name = core_name
        self.solr_url = f'http://{IP}:8983/solr/'
        self.connection = pysolr.Solr(self.solr_url + self.core_name, always_commit=True, timeout=500000)

    def do_initial_setup(self):
        delete_core(self.core_name)
        create_core(self.core_name)

    def create_documents(self, docs):
        print(self.connection.add(docs))

    def add_fields(self):
        data = {
            "add-field":[
                {
                    "name" : "poi_name",
                    "type" : "string",
                    "multiValued" : False
                },
                {
                    "name" : "poi_id",
                    "type" : "plong",
                    "multiValued" : False
                },
                {
                    "name" : "verified",
                    "type" : "boolean",
                    "multiValued" : False
                },
                {
                    "name" : "country",
                    "type" : "string",
                    "multiValued" : False
                },
                {
                    "name" : "replied_to_tweet_id",
                    "type" : "plong",
                    "multiValued" : False
                },
                {
                    "name" : "replied_to_user_id",
                    "type" : "plong",
                    "multiValued" : False
                },
                {
                    "name" : "reply_text",
                    "type" : "text_general",
                    "multiValued" : False
                },
                {
                    "name" : "tweet_text",
                    "type" : "text_general",
                    "multiValued" : False
                },
                {
                    "name" : "tweet_lang",
                    "type" : "string",
                    "multiValued" : False
                },
                {
                    "name" : "text_en",
                    "type" : "text_en",          
                    "multiValued" : False
                },
                {
                    "name" : "text_hi",
                    "type" : "text_hi",          
                    "multiValued" : False
                },
                {
                    "name" : "text_es",
                    "type" : "text_es",          
                    "multiValued" : False
                },
                {
                    "name" : "hashtags",
                    "type" : "string",
                    "multiValued" : True
                },
                {
                    "name" : "mentions",
                    "type" : "string",
                    "multiValued" : True
                },
                {
                    "name" : "tweet_urls",
                    "type" : "string",
                    "multiValued" : True
                },
                {
                    "name" : "tweet_emoticons",
                    "type" : "string",
                    "multiValued" : True
                },
                {
                    "name" : "tweet_date",
                    "type" : "pdate",
                    "multiValued" : False
                },
                {
                    "name" : "geolocation",
                    "type" : "string",
                    "multiValued" : True
                },
            ]
        }
        print(requests.post(self.solr_url + core + "/schema", json=data).json())

    
if __name__ == "__main__":
    collection = []
    for index, item in enumerate(range(15)):
        tweetsdf = pickle.load(open("./data/poi_{}.pkl".format(index+1), "rb"))
        collection += tweetsdf.to_dict('records')
        print('poi {} tweets were added to the collection'.format(index+1))

        repliesdf = pickle.load(open("./data/poi_{}_replies.pkl".format(index+1), "rb"))
        collection += repliesdf.to_dict('records')
        print('poi {} replies were added to the collection'.format(index+1))

    i = Indexer(core)
    i.do_initial_setup()
    i.add_fields()
    i.create_documents(collection)
    

