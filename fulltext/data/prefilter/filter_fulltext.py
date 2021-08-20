# File: filter_fulltext.py
# Desc: Read the text for a paper. 
#       Remove before 'abstract' and after 'references'
#       Maybe some additional parsing, like remove page numbers.
# Text files are here:
#       /data/txt/txt/arxiv/1801/1801.06146v5.txt
#       /data/txt/txt/arxiv/1001/1001.2971v1.txt
# Test on nexus:
#       cd /data/logs_archive/bgm37-fulltext/
#       /opt_arxiv/python3.6/bin/python3  filter_fulltext.py  the_txt_file
#       /opt_arxiv/python3.6/bin/python3  filter_fulltext.py  the_paper_id  the_version

from os import path
import re

RE_CID        = re.compile(r'\(cid:\d+\)')
RE_MULTIWHITE = re.compile(r'\s+')

class FilterFullText:
  def __init__(self, text_file_path, title):
    self.text_file_path = text_file_path
    self.title          = title
    self.exists         = path.exists(self.text_file_path)
    self.text           = None
    self.parsed_text    = None
    self.abstract_at    = None
    self.references_at  = None

    self.length   = 0
    self.pct_abs  = 0
    self.pct_text = 0
    self.pct_ref  = 0

    if self.exists:
      with open(text_file_path, errors='ignore') as f:
        self.text = f.readlines()

      self.parsed_text = []
      found_abstract   = False
      found_references = False

                                       # Exclude text before the abstract   header
                                       # Exclude text after  the references header
                                       # Use first abstract and last references.
                                       # Table of contents- avoid early ending
      abstract_list = []
      references_list = []
      i = 0
      for tmp_line in self.text:
        i = i + 1
        line = tmp_line.strip()

        if self.line_is_abstract(line):
          abstract_list.append(i)
        if self.line_is_references(line):
          references_list.append(i)

      if len(abstract_list) > 0:
        self.abstract_at   = abstract_list[0]
      if len(references_list) > 0:
        self.references_at = references_list[-1]


                                       # Stats on line counts: 
                                       #   abstract vs body vs references
    if self.text:
      self.length = len(self.text)
      if self.abstract_at:
        self.pct_abs = round(self.abstract_at/self.length*100, 2)
      if self.references_at:
        self.pct_ref = round( (self.length-self.references_at)/self.length*100, 2)

      tmp = self.length
      if self.references_at:
        tmp = self.references_at
      if self.abstract_at:
        tmp -= self.abstract_at
      self.pct_text = round( tmp/self.length*100, 2)

      self.parsed_text = []
      if self.abstract_at:             # Add the title back in, when cut along with abstract
        self.parsed_text.append(self.title)
      accumulate = None
      i = 0
                                       # Include only the body of the paper
      begin = 0
      end   = self.length
      if self.abstract_at:
        begin = self.abstract_at
      if self.references_at:
        end = self.references_at-1
      for tmp_line in self.text[begin:end]:
        i = i + 1
        line = tmp_line.strip()
        #print(f'LINES, i:{ i }, pt:{ len(self.parsed_text) }, t:{ len(self.text) } ')

                                       # De-hypenate words split across two lines.
        if line.endswith('-'):
          if accumulate:
            accumulate = accumulate + line[0:-1]
          else:
            accumulate = line[0:-1]
        else:
          if accumulate:
            line = f'{accumulate}{line}'
            accumulate = None

          if len(line):                # Skip blank lines.
            line = self.filter_line(line)
            self.parsed_text.append(line)


  def found_abstract_and_references(self):
    return self.abstract_at != None and self.references_at != None

  def line_is_abstract(self, line):
    s = line.lower()
    return s.startswith('abstract') or s.endswith('abstract') or s.endswith('introduction')

  def line_is_references(self, line):
    s = line.lower()
    return s.endswith('references') or s.endswith('bibliography') or s.endswith('acknowledgments')

  def filter_line(self, s):
    s = RE_CID.subn('', s)[0]
    s = RE_MULTIWHITE.subn(' ', s)[0]
    return s

  def __str__(self):
    #print(f'1. { pct }')

    return f'{ self.text_file_path } | exists={ self.exists } | abstract_at={ self.abstract_at } ({self.pct_abs}) | body:({self.pct_text}) || references_at={ self.references_at } ({self.pct_ref}) | lines={ self.length }'


if __name__ == '__main__':

  import fulltext_util as u
  import sys

  if len(sys.argv) == 2:
    text_file = sys.argv[1]
  elif len(sys.argv) == 3:
    text_file = u.get_text_path(sys.argv[1], sys.argv[2])
  else:
    text_file = '0001062v1.txt'

                                       # To test, edit this file
  f = FilterFullText(text_file, 'Test Title')
  print()
  print(f'============================ START TEXT ==========')
  print()
  for line in f.text:
    print( line )
  print()
  print(f'============================ START PARSED TEXT ==========')
  print()
  LF='\\n'
  if f.parsed_text:
    print(f'f2:{ " ".join(f.parsed_text) }')
  #for line in f.get_parsed_text():
  #  print( line )
  print()
  print(f'============================ END PARSED TEXT ==========')
  print()
  print(f'f:{ f }')
  print()

