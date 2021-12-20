# File: convert_json_to_predictions_over_time.py
# Desc: After testing a model, read the prediction results,
#         and shape it to read into Tableau as a line/bar graph over time.
#       Normalize announce date to first day of month.
#       Keep subject category.
#       Compare announced category to highest rated prediction.
#       https://tableau.cornell.edu/#/views/arXivClassifierM15/Sheet1

'''
Why we don't use it below a threshold:
  # MIN_CONFIDENCE = 0
  cat m15-ds9-predictions-over-time.tsv | awk '{print $4}' | sort | uniq -c
  61167 correct
  60297 incorrect

  # MIN_CONFIDENCE = .7
  cat m15-ds9-predictions-over-time.tsv | awk '{print $4}' | sort | uniq -c
  42970 correct
  19274 incorrect
'''

import csv
import json
import sys
from datetime import datetime

READFILE = "m15-ds9-classified-inline_0.json"
WRITEFILE = "m15-ds9-predictions-over-time.tsv"
CONFUSIONFILE = "m15-ds9-predictions-confusion-matrix.tsv"
MIN_CONFIDENCE = .7

# union of predicted and announced subject categories
categories = set()

# confusion_matrix, 
#   for each announced category, count the top predictions.
#   ie: {"ai":{"ai":1,"ml":0}} 
cm = {} 

d1 = datetime.now()
i = 1
with open(WRITEFILE, "w", newline="\n") as csvfile:
    wf = csv.writer(csvfile, csv.unix_dialect, quoting=csv.QUOTE_MINIMAL, delimiter='\t')
    header = f'paper_id,announced_category,predicted_category,correct,announced_date,archive'
    wf.writerow(header.split(","))

    with open(READFILE) as rf:
        line = rf.readline()
        while line:
            # { "paper_id": "cond-mat/0001074", 
            #   "version": "1", 
            #   "primary_category": "cond-mat.stat-mech", 
            #   "text_type": "abstract", 
            #   "probabilities": [["cond-mat.quant-gas", 0.6066799163818359], ... ]
            # }
            j = json.loads(line)
            paper_id = j["paper_id"]
            primary_category = j["primary_category"]
            predicted_category = j["probabilities"][0][0]
            prediction_confidence = j["probabilities"][0][1]
            correct_prediction = 'correct' if predicted_category == primary_category else 'incorrect'

            tmp = paper_id.find("/")
            yymm = paper_id[0:4] if tmp == -1 else paper_id[tmp + 1 : tmp + 5]
            y = "19" + yymm[0:2] if yymm[0] == "9" else "20" + yymm[0:2]
            m = yymm[2:4]
            announced_date = f'{y}-{m}-01'

            tmp = primary_category.find(".")
            archive = primary_category if tmp == -1 else primary_category[0:tmp]

            arr = []
            arr.append(paper_id)
            arr.append(primary_category)
            arr.append(predicted_category)
            arr.append(correct_prediction)
            arr.append(announced_date)
            arr.append(archive)

            if prediction_confidence >= MIN_CONFIDENCE:
              wf.writerow(arr)

            # Store all subject categories
            categories.add(primary_category)
            categories.add(predicted_category)

            # Confusion matrix
            predictions = cm.get(primary_category)
            if not predictions:
              predictions = {}
              cm[primary_category] = predictions
            count = predictions.get(predicted_category)
            count = 1 if not count else count + 1
            predictions[predicted_category] = count

            line = rf.readline()
            i = i + 1
            #if i >= 10:
            #    break

with open(CONFUSIONFILE, "w", newline="\n") as csvfile:
    wf = csv.writer(csvfile, csv.unix_dialect, quoting=csv.QUOTE_MINIMAL, delimiter='\t')
    sorted_categories = sorted(categories)
    wf.writerow([''] + sorted_categories)
    for ac in sorted_categories:
      arr = []
      arr.append(ac)
      for pc in sorted_categories:
        num = 0
        hash1 = cm.get(ac)
        if hash1:
          x = hash1.get(pc)
          if x:
            num = x 
        arr.append(str(num))
      wf.writerow(arr)

d2 = datetime.now()
delta = d2 - d1
seconds = delta.total_seconds()
print(f"Ending duration for {i} papers is { seconds } seconds at { datetime.now() } ")
sys.stdout.flush()
sys.stderr.flush()
