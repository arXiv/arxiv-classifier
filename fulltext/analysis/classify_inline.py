# File: classify_inline.py
# Desc: load the model and run preditions

# gcloud compute ssh classify-inline-32x128 --zone us-west1-b --project arxiv-bgm37-2
# gcloud compute scp ds12-recent-papers-test.json.gz classify-inline-32x128:/mnt/data/ --zone us-west1-b
# gcloud compute scp classify_inline.py classify-inline-32x128:/mnt/data/ --zone us-west1-b

import json
import numpy  as np
import pandas as pd
import re
import requests
import stream_json
import sys
import time
import torch
from fastai.text import *
from pathlib     import Path
from datetime import timedelta
from datetime import datetime
import time


def classify(index, mod):

  #modelfile     = 'm12-ds11-mixed-large.pkl'
  modelfile     = 'm15-ds9-mixed-all-export8.pkl'

  #readfile      = 'ds12-recent-papers-test.json'
  readfile      = 'ds9-mixed-all-test.json'

  #writefile_base = 'm15-ds12-classified-inline'
  writefile_base = 'm15-ds9-classified-inline'

  learn = load_learner(path=Path('models'), file=Path(modelfile))  

  i = 0
  with open(f'{writefile_base}_{index}.json', 'w') as wf:
    with open(readfile) as rf:
      sj = stream_json.StreamJson(rf)
      #print(f'1.')
      for item in sj:
        #print(f'2.{item}')
        if i % mod == index:
          j = json.loads(item)
          paper_id = j["paper_id"]

          p1 = [ float(q) for q in learn.predict([ j["text"] ])[2] ]
          p2 = list(zip(learn.data.classes, p1))
          p3 = sorted(p2, key=lambda p: p[1], reverse=True)
          data = {
            "paper_id"         : paper_id,
            "version"          : j["version"],
            "primary_category" : j["primary_category"],
            "text_type"        : j["text_type"],
            "probabilities"    : p3,
          }

          s_data = json.dumps(data)
          print(s_data, file=wf)
          wf.flush()

        i = i + 1
        sys.stdout.flush()
        sys.stderr.flush()

        #if i >= 200:
        #  break

if __name__ == '__main__':
  if len(sys.argv) == 3:
    i            = int(sys.argv[1])
    thread_count = int(sys.argv[2])
  else:
    i            = 0
    thread_count = 1

  print(f'Starting { i }/{ thread_count }, at { datetime.now() } ')
  d1 = datetime.now()

  classify(i,thread_count)

  d2 = datetime.now()
  delta = d2 - d1
  seconds = delta.total_seconds()
  print(f'Ending duration is { seconds } seconds, for { i }/{ thread_count } at { datetime.now() } ')

  sys.stdout.flush()
  sys.stderr.flush()

