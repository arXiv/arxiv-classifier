# File: count_papers.py
# Desc: How many papers have extracted text

import csv
import fulltext_util as u
import time
from os import path

def add_stat(stats, key):
  stat = stats.get(key)
  if stat == None:
    stat = 0
  stat = stat + 1
  stats[key] = stat

read_file = 'papers-20210804.tsv'
with open(read_file) as rf:
  r = csv.reader(rf, csv.excel_tab)
  next(r)

  not_found   = 0
  found       = 0
  i = 0
  for row in r:
    i += 1
    if i % 5000 == 0:
      #time.sleep(0.2)
      print(f'Papers, not found:{not_found:<{8}}, found:{found:<{8}}, percent: {round(not_found/i, 2):<{8}}')
    #if i > 5500:
    #  break

    paper_id = row[0]
    version  = row[1]

    text_file = u.get_text_path(paper_id, version)

    if path.exists(text_file):
      #print(f'found: { text_file }')
      found += 1
    else:
      #print(f'not found: { text_file }')
      not_found += 1

