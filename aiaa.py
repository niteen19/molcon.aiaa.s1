
import json

import xml.etree.ElementTree as ET

from bson.json_util import dumps
from json import loads




from flask import Flask, jsonify, request, make_response
from pymongo import MongoClient, response

import pymongo
app= Flask(__name__)
@app.route("/aiaa-s1m/export/<string:a>",methods=['GET'])
def getdb(a):

    #connection_url= "mongodb://aiaaadmin:aiaa_2k190102_MCPL@139.162.209.89:27017/admin"
    connection_url = "mongodb://aiaaadmin:aiaa_2k190102_MCPL@192.168.207.141:27017/admin"

    client=MongoClient(connection_url)
    dbname=client['manuscript_notifier_test']


    args = request.args
    forceArg = args.get("force", default=False, type=bool)



    collection_name=dbname['document_logs']

    cursor=collection_name.find({'docId': a})

    jsndata=dumps(cursor)
    args = request.args
    forceArg = args.get("force", default=False, type=bool)

    if forceArg == False:
        pass
        #print ("zero")
    elif forceArg == True:
        pass
        #print("one")
    if len(jsndata)<=2:

        return  json.dumps({'status':'500', 'message':'docid not found'}), 500
    else:
        jsonObj = json.loads(jsndata)

        status = ['blocked', 'done']
        x = jsonObj[0]['status']
        if jsonObj and x not in status and forceArg==False:
            rootXmlTag = ET.Element("classification")
            subjectGroupXmlTag = ET.SubElement(rootXmlTag, "subj-group")
            subjectGroupXmlTag.set('subj-group-type', "allpubtopics")

            allTopics = jsonObj[0]['classification']['topics']
            for i in allTopics:
                print(type(i))
                subjectXmlTag = ET.SubElement(subjectGroupXmlTag, 'subject')
                subjectXmlTag.text = i['name']

                subjectXmlTag.set('code', i['cid'])

                keywordGroupXmlTag = ET.SubElement(rootXmlTag, "kwd-group")
                keywordGroupXmlTag.set('kwd-group-type', "MC_Keywords_1.0")
                kwdGroups = jsonObj[0]['classification']['textForms']
                for i in kwdGroups:
                    print(i)
                    kwdTag = ET.SubElement(keywordGroupXmlTag, "kwd");
                    kwdTag.text = i

                tree = ET.ElementTree(rootXmlTag)


                tree.write("/home/AIAA/AIAAOutgoing/S1M-Exports/{}.xml".format(a))
                collection_name.update({'docId': "6.2002-840"}, {'$set': {'status': 'done'}})
                return json.dumps({'status':'200', 'message':"status is updated to done "}),200

        elif x == 'blocked':
            return json.dumps({'status':'500', 'message':'status is blocked, can not proceed'}),500
        #elif x == 'done':
         #   return json.dumps({'status':'500', 'message':'status is already done'}),500
        elif x=='done' and forceArg == True:
            rootXmlTag = ET.Element("classification")
            subjectGroupXmlTag = ET.SubElement(rootXmlTag, "subj-group")
            subjectGroupXmlTag.set('subj-group-type', "allpubtopics")

            allTopics = jsonObj[0]['classification']['topics']
            for i in allTopics:
                #print(type(i))
                subjectXmlTag = ET.SubElement(subjectGroupXmlTag, 'subject')
                subjectXmlTag.text = i['name']

                subjectXmlTag.set('code', i['cid'])

                keywordGroupXmlTag = ET.SubElement(rootXmlTag, "kwd-group")
                keywordGroupXmlTag.set('kwd-group-type', "MC_Keywords_1.0")
                kwdGroups = jsonObj[0]['classification']['textForms']
                for i in kwdGroups:
                   # print(i)
                    kwdTag = ET.SubElement(keywordGroupXmlTag, "kwd");
                    kwdTag.text = i

                tree = ET.ElementTree(rootXmlTag)



                tree.write("/home/AIAA/AIAAOutgoing/S1M-Exports/{}.xml".format(a))


            #collection_name.update({'docId': "6.2002-840"}, {'$set': {'status': 'done'}})
            return json.dumps({'status':'500', 'message':"status is updated to done and file generated again "}), 200
        elif x == 'done':
            return json.dumps({'status':'500', 'message':'status is already done'}),500




        else:
            return json.dumps("exception occured")


if __name__=="__main__":
    app.run(debug=True,host = "0.0.0.0", port = 8888)
    #app.run(debug=True)