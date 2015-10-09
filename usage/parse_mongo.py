import requests
from pymongo import MongoClient
import json

connection = MongoClient()
db = connection.lexisnexis
collection = db["test"]

t = collection.find().limit(500)

output = []
junk = []

# figure out /process and /code

headers = {'Content-Type': 'application/json'}

for i in t:
    data = {'text': i['article_body'],
    'id': i['doc_id'], 'date':
    '20010101'}
    data = json.dumps(data)
    r = requests.get('http://localhost:5002/hypnos/extract', data=data,
                     headers=headers)
    rj = r.json()
    try:   # clunky check for key
        rj['status'] 
        junk.append(rj)
    except:
        output.append(rj)


for o in output:
    for key, s in o[o.keys()[0]]['sents'].iteritems():
        if s['events']:
            print s['events']
