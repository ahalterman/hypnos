import requests
import json

headers = {'Content-Type': 'application/json'}

data = {'text': "At least 37 people are dead after Islamist radical group Boko Haram assaulted a town in northeastern Nigeria. US warplanes bombed ISIS targets throughout Iraq. President Barack Obama flew to Germany to meet with German Chanceller Angela Merkel.", 'id': 'abc123', 'date': '20010101'}

data = json.dumps(data)
r = requests.get('http://localhost:5002/hypnos/extract', data=data,
                 headers=headers)
print r.json()
