import json
import os
import urllib.request
from pprint import pprint

from flask import request
from pymongo import MongoClient
import xml.etree.ElementTree as ET
import json as JS
from bson.json_util import dumps
import dicttoxml
from json import loads
import os.path

from x import writeXml

connection_url= "mongodb://aiaaadmin:aiaa_2k190102_MCPL@139.162.209.89:27017/admin"
client=MongoClient(connection_url)
dbname=client['manuscript_notifier_test']
    #print(dbname)
mydb=client.list_database_names()
print(client.list_database_names())
collection_name=dbname['document_logs']
#print(collection_name)
cursor= collection_name.find({'docId':'6.2002-888'})
print(cursor)
#mylist=list(cursor)
jsndata=dumps(collection_name.find({'docId':'6.2002-840'}))
print(jsndata)
print(len(jsndata))
args = request.args
forceArg = args.get("force", default=False, type=bool)
if   (len(jsndata)) <= 2 :
    print('docid not found')
else:
    jsonObj=json.loads(jsndata)
    status=['blocked','done']
    j= jsonObj[0]['status']
    y=(jsonObj[0]['outputXmlPath'])
    print(os.path.expanduser(y))




    if  jsonObj and j not in status:
        writeXml()
        collection_name.update({'docId': "6.2002-840"}, {'$set': {'status': 'done'}})
    elif j =='blocked':
        print('status is blocked, can not proceed')
    elif j =='done':
        print("status is done,please use force param")



    else:
        print("exception occured")







