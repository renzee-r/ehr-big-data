import pymongo
import json
import os
import requests

client = pymongo.MongoClient("mongodb+srv://admin-1:JK6qJJz4lVUmDp2J@w251-ehr-project-weita.mongodb.net/ehr?retryWrites=true")
db = client.ehr
collection = db.ocrdata

for json_file in os.listdir('/tmp/json'):
    if not json_file.endswith('.json'):
        continue

    print('Processing file: ' + json_file)
    with open(json_file) as jf:
        json_string = json.load(jf)

        # Elasticsearch
        url = 'http://169.53.145.101:9200/ehr/image'
        payload = json_string
        headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
        r = requests.post(url, data=payload, headers=headers)
        print(r.text)

        # MongoDB
        mongo_row_id = collection.insert_one(json_string).inserted_id
        print(mongo_row_id)


            

