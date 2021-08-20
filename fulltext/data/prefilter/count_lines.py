# File: count_lines.py
# Desc: How many lines and characters are in filtered full text?
#       How many characters would give us the bulk of the full text?
#       - I think 40k parsed charactors, from stats on 5k papers

import csv
import filter_fulltext
import json
import re
import time
from os import path

def add_stat(stats, key):
  stat = stats.get(key)
  if stat == None:
    stat = 0
  stat = stat + 1
  stats[key] = stat

read_file = 'ds3-fulltext-small-train-20210804.tsv'
with open(read_file) as rf:
  r = csv.reader(rf, csv.excel_tab)
  next(r)

  not_found   = 0
  no_abs_ref  = 0
  no_abs      = 0
  no_ref      = 0
  stats_char  = {}
  stats_lines = {}
  sum_char    = 0
  sum_lines   = 0
  i = 0
  for row in r:
    i += 1
    #if i % 100 == 0:
    #  time.sleep(0.5)
    if i > 5000:
      break

    paper_id = row[0]
    version  = row[1]

    subdir = None
    j = paper_id.find('/')
    if j == -1:
      yymm          = paper_id[:4]       # e.g. paper_id: 2006.13338
      path_category = 'arxiv'
      paper_num     = paper_id
    else:
      yymm          = paper_id[j+1:j+5]  # e.g. paper_id: astro-ph/0404130
      path_category = paper_id[:j]
      paper_num     = paper_id[j+1:]
    text_file = f'/data/txt/txt/{ path_category }/{ yymm }/{ paper_num }v{ version }.txt'

    filterer = filter_fulltext.FilterFullText(text_file, None)
    if not filterer.file_exists():
      #print(f'Not found: { text_file }')
      not_found += 1

    elif not filterer.found_abstract_and_references():
      no_abs_ref += 1
      tmp = ''
      if not filterer.found_abstract():
        no_abs += 1
        tmp = 'abs'
      else:
        tmp = '   '
      if not filterer.found_references():
        no_ref += 1
        tmp += '-ref'
      else:
        tmp += '-   '
      print(f'{i:<{8}}. Missing: { tmp }   { text_file }')

    else:
      #print(f'Found: { text_file }')
      pt = filterer.get_parsed_text()
      cl = len( pt )
      cc = sum( [ len(l) for l in pt if l ] )
      sum_lines += cl
      sum_char  += cc
      roundcl = round(cl/1000)
      roundcc = round(cc/10000)
      add_stat(stats_lines, roundcl)
      add_stat(stats_char,  roundcc)

  print('Lines/1k')
  for k in sorted(stats_lines.keys()):
    print(f'{k:<{8}}: { stats_lines[k] }')

  print('Charactors/10k')
  for k in sorted(stats_char.keys()):
    print(f'{k:<{8}}: { stats_char[k] }')

  count_papers = sum(stats_char.values())

  print(f'Papers not found: {not_found:<{8}}, percent: {round(not_found/i*100, 1):<{8}}')
  print(f'No abs          : {no_abs:<{8}}, percent: {round(no_abs/i*100, 1):<{8}}')
  print(f'No ref          : {no_ref:<{8}}, percent: {round(no_ref/i*100, 1):<{8}}')
  print(f'No abs/ref      : {no_abs_ref:<{8}}, percent: {round(no_abs_ref/i*100, 1):<{8}}')
  print(f'char            : {sum_char:<{8}}, avg    : {round(sum_char/count_papers):<{8}}')
  print(f'lines           : {sum_lines:<{8}}, avg    : {round(sum_lines/count_papers):<{8}}')

'''

[...]
4900    . Missing: abs-ref   /data/txt/txt/cond-mat/0212/0212506v1.txt
4902    . Missing: abs-ref   /data/txt/txt/cond-mat/0212/0212428v1.txt
4904    . Missing: abs-ref   /data/txt/txt/cond-mat/0212/0212448v2.txt
4905    . Missing:    -ref   /data/txt/txt/cond-mat/0212/0212128v1.txt
4906    . Missing:    -ref   /data/txt/txt/cond-mat/0212/0212129v1.txt
4907    . Missing: abs-ref   /data/txt/txt/cond-mat/0212/0212137v1.txt
4909    . Missing:    -ref   /data/txt/txt/cond-mat/0212/0212418v1.txt
4918    . Missing: abs-      /data/txt/txt/cs/0212/0212019v1.txt
4926    . Missing:    -ref   /data/txt/txt/hep-lat/0212/0212034v1.txt
4938    . Missing: abs-ref   /data/txt/txt/math/0212/0212257v5.txt
4949    . Missing: abs-      /data/txt/txt/math/0212/0212082v1.txt
4970    . Missing: abs-      /data/txt/txt/math/0212/0212137v1.txt
4973    . Missing: abs-      /data/txt/txt/math/0212/0212108v1.txt
4994    . Missing:    -ref   /data/txt/txt/math/0212/0212399v1.txt
Lines/1k
0       : 1338
1       : 1821
2       : 420
3       : 105
4       : 36
5       : 12
6       : 8
7       : 5
8       : 1
9       : 2
10      : 1
11      : 1
12      : 1
13      : 1
16      : 1
Charactors/10k
0       : 183
1       : 692
2       : 904
3       : 662
4       : 461
5       : 279
6       : 191
7       : 130
8       : 56
9       : 53
10      : 39
11      : 26
12      : 21
13      : 11
14      : 9
15      : 7
16      : 3
17      : 4
18      : 1
19      : 2
20      : 3
21      : 2
22      : 1
23      : 1
24      : 2
25      : 2
27      : 2
28      : 1
29      : 1
31      : 1
34      : 1
36      : 1
39      : 1
Papers not found: 65      , percent: 1.3
No abs          : 794     , percent: 15.9
No ref          : 921     , percent: 18.4
No abs/ref      : 1182    , percent: 23.6
char            : 126983346, avg    : 33835
lines           : 3463168 , avg    : 923
'''

