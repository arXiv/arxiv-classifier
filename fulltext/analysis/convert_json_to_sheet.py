# File: convert_json_to_sheet.py
# Desc: export prediction results to drop into this google sheet:
#       https://docs.google.com/spreadsheets/d/1g9yvTZI7MdxI2_yxTrw-vIyWuUrF93r7MKINt4UTeds/edit#gid=1665087432


import csv
import json
import numpy  as np
import pandas as pd
import re
import requests
import sys
import time
from datetime import timedelta,datetime
from pathlib     import Path

readfile  = 'partial.json'
writefile = 'partial.csv'

d1 = datetime.now()
i = 0
with open(writefile, 'w', newline='\n') as csvfile:
  wf = csv.writer(csvfile, csv.unix_dialect, quoting=csv.QUOTE_MINIMAL)
  wf.writerow( f',doc_paper_id,top_pg,top_pg_logit,top_pg_logit,announced,top_pwc,top_pwc_score,pg_success,pwc_success,user_matches_announced'.split(',') )

  with open(readfile) as rf:
    sj = rf.readline()
    while sj:
      j = json.loads(sj)
      paper_id = j["paper_id"]

      arr = []
      arr.append(i)
      arr.append(paper_id)
      arr.append(j["version"])
      arr.append(j["text_type"])
      arr.append(None)
      arr.append(j["primary_category"])

      p = j["probabilities"]
      arr.append(p[0][0])
      arr.append(p[0][1])

      arr.append('FALSE')
      matches = 'FALSE'
      if p[0][0] == j["primary_category"]:
        matches = 'TRUE'
      arr.append( matches )
      arr.append('FALSE')

      wf.writerow(arr)

      sj = rf.readline()
      i = i + 1
      #if i >= 10:
      #  break


d2 = datetime.now()
delta = d2 - d1
seconds = delta.total_seconds()
print(f'Ending duration is { seconds } seconds at { datetime.now() } ')
sys.stdout.flush()
sys.stderr.flush()

