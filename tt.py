from  flask import Flask,jsonify
from pymongo import MongoClient
import pandas as pd
from collections.abc import MutableMapping
import pymongo
import babelfish
def getdb():
    connection_url= "mongodb://aiaaadmin:aiaa_2k190102_MCPL@139.162.209.89:27017/admin"
    client=MongoClient(connection_url)
    dbname=client['manuscript_notifier_test']
    print(dbname)
  #  mydb=client.list_database_names()
   # print(client.list_database_names())
    collection_name=dbname['document_logs']
    print(collection_name)

    record=collection_name.find()
    item=list(record)
   # print(item)
    df=pd.DataFrame(item)
    print(df.head())

getdb()

