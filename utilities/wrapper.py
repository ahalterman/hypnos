import requests
from pymongo import MongoClient
import json
import logging
import logging
import argparse

connection = MongoClient()

parser = argparse.ArgumentParser()
parser.add_argument("--db", help="Mongo DB")
parser.add_argument("--collection", help="Mongo collection")
parser.add_argument("--date", help="Date to run, YYYY-MM-DD") # make a general query?
parser.add_argument("--log_file", help="File for logging")

args = parser.parse_args()
args.db
if args.db:
    db = args.db
else:
    db = connection.lexisnexis
if args.log_file:
    LOG_FILE = args.log_file
else:
    LOG_FILE = "hypnos_wrapper.log"
COLLECTION = args.collection
DATE = args.date

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

handler = logging.FileHandler(LOG_FILE)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
print "Writing logs to {0}".format(LOG_FILE)

collection = db[COLLECTION]

print "There are {0} records matching that search".format(collection.count())

headers = {'Content-Type': 'application/json'}

results = collection.find().limit(10)

for res in results:
    data_id = '123'
    data = {'text' : res['article_body'],
            'id' : data_id, 
            'date' : '200010101'} 
    data = json.dumps(data)
    r = requests.get('http://localhost:5002/hypnos/extract', data=data,
                             headers=headers)
    r = r.json()
    print r[data_id]['sents']
    collection.update({"_id": res['_id']}, {"$set": 
                                            {'parsed_sents': r[data_id]['sents'],
                                             'hypnos': 1,
                                             }})
