# File: to_jsonl.py
# Desc: convert paper data in json to json lines
#
# Note: this wasn't too useful. Google's vertex-ai worked on small datasets, 
#       but then only returned an internal-error message when training on 700k papers,
#       which is near it's 1M limit.
#
# https://cloud.google.com/vertex-ai/docs/datasets/prepare-text#jsonl
#   {
#     "classificationAnnotation": {
#       "displayName": "label"
#     },
#     "textContent": "inline_text",
#     "dataItemResourceLabels": {
#       "aiplatform.googleapis.com/ml_use": "training|test|validation"
#     }
#   }

import json
import jsonlines
import sys
import stream_json

if len(sys.argv) != 4:
  print("Usage: python to_jsonl.py readfile writefile usage")
  print("   eg: python to_jsonl.py ds9-mixed-all-validate.json ds9-mixed-all-validate.jsonl validation")

else:
  readfile  = sys.argv[1]
  writefile = sys.argv[2]
  usage     = sys.argv[3]

  with jsonlines.open(writefile, mode='w') as wf:
    with open(readfile) as rf:
      sj = stream_json.StreamJson(rf)
      for item in sj:
        j  = json.loads(item)
        pc = j["primary_category"]
        if type(j["text"]) == str:
          ft = j["text"]
        else:
          ft = ','.join( j["text"] )

        data = { 
          "classificationAnnotation": { "displayName": pc }, 
          "textContent": ft, 
          "dataItemResourceLabels": { "aiplatform.googleapis.com/ml_use": usage }
        }
        wf.write(data)

