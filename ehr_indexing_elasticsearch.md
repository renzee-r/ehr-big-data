# Indexing EHR database in Elasticsearch

For inserting database into elasticsearch by python API, go <a href=https://elasticsearch-py.readthedocs.io/en/master/>here</a>. 

## Install Elasticsearch in Python
```
# pip install elasticsearch
```

## Python API script

```
# vi ehr_insert.py
```
Copy and paste the following script

```
#!/usr/bin/python

import os
import sys
import csv
from elasticsearch import Elasticsearch

# Creating es object class
es = Elasticsearch()

index='ehr'
doc_type='ehr_basic'

# to get the name of the file we're inserting into elasticsearch
fname = sys.argv[1]

with open(fname) as f:
    csvreader = csv.reader(f, delimiter='\t', quotechar='"')

    # extract headers
    # for python2, it's csvreader.next()
    # for python3, it's next(csvreader)
    # Since there's no headers in csv, won't be using the headers
    # headers = csvreader.next() 
 
    count = 0
    for fields in csvreader:
        body = {}
        for i in range(len(fields)):
            body["Medical Condition"] = fields
	      result = es.index(index=index, doc_type=doc_type, id=count, body=body)
        count += 1

	# to check regulary if the database is properly inserted
        if (count % 1000 == 0):
            print("{} records inserted".format(count))
	
    print("{} records inserted".format(count))
 ```
 
## Inserting EHR into Elasticsearch !

Before you launch the python script, make sure you already launched the elasticsearch which will be listening at port `9200`. 

```
# chmod 755 ehr_insert.py
# python ehr_insert.py ehr_samples.csv
1000 records inserted
2000 records inserted
...
...
4998 records inserted
```

## Query 
Sample query on `heart` medical condition. 

```
# curl -X GET 'http://158.85.213.187:9200/_search?q=heart' | jq -C '.'
```
Output
```
{
  "took": 4,
  "timed_out": false,
  "_shards": {
    "total": 5,
    "successful": 5,
    "failed": 0
  },
  "hits": {
    "total": 1211,
    "max_score": 0.51143664,
    "hits": [
      {
        "_index": "ehr",
        "_type": "ehr_basic",
        "_id": "4764",
        "_score": 0.51143664,
        "_source": {
          "Medical Condition": [
            "4765,\" Holter monitor report.   Predominant rhythm is sinus.  Triplet maximum rate of 178 beats per minute noted.\",4,\" Cardiovascular / Pulmonary\",\" Holter Monitor Report - 1 \",\"INDICATIONS: , Predominant rhythm is sinus.  Heart rate varied between 56-128 beats per minute, average heart rate of 75 beats per minute.  Minimum heart rate of 50 beats per minute.,640 ventricular ectopic isolated beats noted.  Rare isolated APCs and supraventricular couplets.,One supraventricular triplet reported.,Triplet maximum rate of 178 beats per minute noted.\",\"cardiovascular / pulmonary, holter monitor, heart rate, supraventricular, triplet, heart, beats\""
          ]
        }
      },

    ...
    ...
```

```
# curl -X GET 'http://158.85.213.187:9200/_search?q=heart' | jq -C '.hits.total'

1211
```
