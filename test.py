import pickle
import pandas as pd

collection = []
for index, item in enumerate(range(15)):
    tweetsdf = pickle.load(open("./data/poi_{}.pkl".format(index+1), "rb"))
    collection.append(tweetsdf.to_dict('records'))
    print('poi {} tweets were added to the collection'.format(index+1))