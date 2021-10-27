# File: add_fulltext.py
# Desc: Look for the full-text of the current paper-version in /data/txt/txt and write to a json data file

import csv
import filter_fulltext
import fulltext_util as u
import json
import re
from os import path

#MAX_CHAR      = 30000 # ds6
MAX_CHAR       = 40000 # ds7,8,10,11,12
#MAX_CHAR      = 50000 # ds5,9
#MAX_CHAR      = 70000

#DATASET_NAME = 'ds0'
#DATASET_NAME = 'ds2-fulltext-toy'
#DATASET_NAME = 'ds3-mixed-small'
#DATASET_NAME = 'ds4-mixed-small'
#DATASET_NAME = 'ds5-mixed-small'
#DATASET_NAME = 'ds6-mixed-tiny'
#DATASET_NAME = 'ds7-mixed-small'
#DATASET_NAME = 'ds8-mixed-large'
#DATASET_NAME = 'ds9-mixed-all'
#DATASET_NAME = 'ds10-mixed-large'
#DATASET_NAME = 'ds11-mixed-large'
DATASET_NAME = 'ds12-recent-papers'
#DATASET_TYPES = ['train', 'validate', 'test']
DATASET_TYPES = ['test']
#DATASET_TYPES = ['debug']

for dataset_type in DATASET_TYPES:
  read_file    = f'{DATASET_NAME}-{dataset_type}.tsv'
  json_file    = f'{DATASET_NAME}-{dataset_type}.json'

  wj = open(json_file, 'w', newline='\n')
  print('[', file=wj)
  with open(read_file) as rf:
    r = csv.reader(rf, csv.excel_tab)
    #next(r)

    i = 0
    for row in r:
      i += 1
      #if i > 2:
      #  break

      data = {
        'document_id'      : row[0],
        'paper_id'         : row[1],
        'version'          : row[2],
        'yymm'             : row[3],
        'primary_category' : row[4],
        'title'            : row[5],
      }
      title    = row[5]
      abstract = row[6]
      paper_id = data.get("paper_id")
      version  = data.get("version")

                                       # When the paper full text doesn't exist,
                                       #   use the abstract (1%)
                                       # When the abstract and references can not
                                       #   be found in the full text, also use
                                       #   the abstract (20%). There may be some
                                       #   diversity benefits to have a few smaller
                                       #   texts used in the model. Similar to the
                                       #   way images are sometimes skewed in vision.
      text_file = u.get_text_path(paper_id, version)
      filterer = filter_fulltext.FilterFullText(text_file, title)
      if filterer.exists and filterer.found_abstract_and_references():
        text = " ".join(filterer.parsed_text)
        data['text_type'] = 'fulltext'
      else:
        text = abstract
        data['text_type'] = 'abstract'

                                       # Probably better to have more papers,
                                       #   than the full paper. 
                                       #   See count-lines.py for stats. 
                                       #     ~80% papers have < 50k parsed charactors.
                                       # Marcin may have said long papers
                                       #   don't work well.
      text = text[:MAX_CHAR]
      data['text'] = text

      line = json.dumps(data, separators=(",",":") )
      if i > 1:
        print(',', file=wj)
      print(f'{ line }', file=wj)

  print(']', file=wj)
  wj.close()

