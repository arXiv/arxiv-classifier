# File: classify_runner.py
# Desc: use multiple processes to call classifier cluster.

import concurrent.futures
import json
import requests
import stream_json
import time

def classify(writefile_base, readfile, index, mod):
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
 
          data1 = {
            "title":    j["title"],
            "abstract": j["text"],
          }
          s_data1 = json.dumps(data1)
          #classify_url = 'http://localhost:9808/classify'
          classify_url = 'http://10.128.0.17:9808/classify'  # external ip of internal kubernetes load balancer

          data2       = None
          status_code = 0
          attempts    = 0
          while status_code != 200 and attempts < 3:
            r = requests.post(classify_url, data=s_data1)
            status_code = r.status_code
            if status_code == 200:
              data2 = r.json()
            else:
              print(f'I am:{ index+1 } of:{ mod } at line:{ i }, sleeping on err:{ status_code }')
              time.sleep(2 * (attempts+2))
            attempts = attempts + 1

          if not data2: 
            print(f'== ERROR == I am:{ index+1 } of:{ mod } at line:{ i }, err on paper_id:{ paper_id }')
          else:
            data2["paper_id"] = paper_id
            s_data2 = json.dumps(data2)

            print(s_data2, file=wf)
            wf.flush()
            print(s_data2)

          if i >= 70:
            break
          if i % 1 == 0:
            print(f'I am:{index+1} of:{mod} at line:{ i }, paper_id:{ paper_id }')

        i = i+1

def main():
  with concurrent.futures.ProcessPoolExecutor() as executor:
    #rf  = '../data/ds11-mixed-large-test.json'
    rf  = 'ds11-mixed-large-test.json'
    wfb = 'ds11-classified'
    print('readfile:',rf, 'writefile:',wfb)
    thread_count = 15
    for i in range(thread_count):
      print('i:',i,'threadcount:',thread_count)
      future = executor.submit(classify,wfb,rf,i,thread_count)
      print(future)

if __name__ == '__main__':
  main()


