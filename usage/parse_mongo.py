import requests
from pymongo import MongoClient
import json
import argparse
parser = argparse.ArgumentParser()

parser.add_argument("--db", help="Mongo database to read from")
parser.add_argument("--collection", help="Mongo collection to read from")
parser.add_argument("--limit", help="Max number of stories to parse")

args = parser.parse_args()

connection = MongoClient()
#DB = args.db
db = connection.lexisnexis
collection = db[args.collection]

t = collection.find({"hypnos" : { "$ne" : 0}}).limit(int(args.limit))

output = []
junk = []

# figure out /process and /code

print "Processing {0} stories...".format(args.limit)
print "This function only returns the extracted events"

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
        collection.update({"doc_id" : i["doc_id"]}, {"$set" : {"rj" : rj, "tmp"
            : 1}})
        output.append(rj)

for o in output:
    for key, s in o[o.keys()[0]]['sents'].iteritems():
        if s['events']:
            print s['events']
