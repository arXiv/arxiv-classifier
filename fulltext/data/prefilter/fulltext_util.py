# File: fulltext_util.py
# Desc: Calculate where the full text file should be for a paper_id + version.
# Use:  python3 fulltext_util.py 2006.13338 1

def get_text_path(paper_id, version):
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

  return text_file


if __name__ == '__main__':
  import sys
  if len(sys.argv) >= 2:
    paper_id = sys.argv[1]
  else:
    paper_id = '1711.07682'
  if len(sys.argv) >= 3:
    version = sys.argv[2]
  else:
    version = 1

  print(get_text_path(paper_id, version) )

