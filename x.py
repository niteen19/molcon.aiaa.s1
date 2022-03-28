import json

from bson import ObjectId
from flask import Flask,jsonify
from pymongo import MongoClient

#app= Flask(__name__)
#@app.route("/ipvalidation")
#def authentication():
connection_url = "mongodb://cciAdmin:cciAdmin2k200707@192.168.6.104:27019/admin"
client = MongoClient(connection_url)
dbname = client['ClientAuthentication']
print(dbname)
collection_name = dbname['Clientauthentication']
print(collection_name)
cursor1=(collection_name.find({'_id':ObjectId("622b5de519fc61695cf501d1")}))

cursor=collection_name.find()
list_cursor=list(cursor1)

jsndata= json.dumps(list_cursor)
print(jsndata)

jsnObject= json.loads(jsndata)
print(jsnObject)
print(len(jsnObject))
#print(jsnObject['authorized-addresses'])



#def authentication()

#if __name__=="__main__":
 #   app.run(debug=True)


