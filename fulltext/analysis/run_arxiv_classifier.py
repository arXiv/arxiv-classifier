# File: test_arxiv_classifier.py
# Desc: Curl equivalent, for testing a model in arxiv-classifier.
'''
curl -s -X POST -H "Content-Type: application/json" --data '
{"title":"P = NP", "abstract": "We prove that P = NP for N = 1 or P = 0."
}' http://localhost:9999/classify 
'''

import json
import requests

data = {
  #"title":"P = NP",
  "abstract": "We prove that P = NP for N = 1 or P = 0.",
  #"abstract": ""
}
json_data = json.dumps(data)

#classify_url = 'http://localhost:9808/classify'
classify_url = 'http://10.128.0.17:9808/classify'  # external ip of internal kubernetes load balancer
r = requests.post(classify_url, data=json_data)
print(r.encoding, r.json())

