# File: split.py
# Desc: Get some test data, mostly select randomly from bunches of year+month.
# Use:  source ~/.bashrc  # use a python3 that supports f-strings
#       python3 split.py
# Ref:
# https://github.com/arXiv/arxiv-base/blob/develop/arxiv/taxonomy/definitions.py
#
# Dragons: It's quirky and doesn't write the last yymm. 
#   Just dup the last readfile line and increment its yymm.

import csv
import random

TAB = '\t'

                                       # Replace the first with the second category
CATEGORY_ALIASES = {
    'math.MP': 'math-ph',
    'stat.TH': 'math.ST',
    'math.IT': 'cs.IT',
    'q-fin.EC': 'econ.GN',
    'cs.SY': 'eess.SY',
    'cs.NA': 'math.NA'
}

                                       # Used subject categories, with aliases removed.
ACTIVE_CATEGORIES = ['astro-ph.CO','astro-ph.EP','astro-ph.GA','astro-ph.HE','astro-ph.IM','astro-ph.SR','cond-mat.dis-nn','cond-mat.mes-hall','cond-mat.mtrl-sci','cond-mat.other','cond-mat.quant-gas','cond-mat.soft','cond-mat.stat-mech','cond-mat.str-el','cond-mat.supr-con','cs.AI','cs.AR','cs.CC','cs.CE','cs.CG','cs.CL','cs.CR','cs.CV','cs.CY','cs.DB','cs.DC','cs.DL','cs.DM','cs.DS','cs.ET','cs.FL','cs.GL','cs.GR','cs.GT','cs.HC','cs.IR','cs.IT','cs.LG','cs.LO','cs.MA','cs.MM','cs.MS','cs.NE','cs.NI','cs.OH','cs.OS','cs.PF','cs.PL','cs.RO','cs.SC','cs.SD','cs.SE','cs.SI','econ.EM','econ.GN','econ.TH','eess.AS','eess.IV','eess.SP','eess.SY','gr-qc','hep-ex','hep-lat','hep-ph','hep-th','math-ph','math.AC','math.AG','math.AP','math.AT','math.CA','math.CO','math.CT','math.CV','math.DG','math.DS','math.FA','math.GM','math.GN','math.GR','math.GT','math.HO','math.KT','math.LO','math.MG','math.NA','math.NT','math.OA','math.OC','math.PR','math.QA','math.RA','math.RT','math.SG','math.SP','math.ST','nlin.AO','nlin.CD','nlin.CG','nlin.PS','nlin.SI','nucl-ex','nucl-th','physics.acc-ph','physics.ao-ph','physics.app-ph','physics.atm-clus','physics.atom-ph','physics.bio-ph','physics.chem-ph','physics.class-ph','physics.comp-ph','physics.data-an','physics.ed-ph','physics.flu-dyn','physics.gen-ph','physics.geo-ph','physics.hist-ph','physics.ins-det','physics.med-ph','physics.optics','physics.plasm-ph','physics.pop-ph','physics.soc-ph','physics.space-ph','q-bio.BM','q-bio.CB','q-bio.GN','q-bio.MN','q-bio.NC','q-bio.OT','q-bio.PE','q-bio.QM','q-bio.SC','q-bio.TO','q-fin.CP','q-fin.GN','q-fin.MF','q-fin.PM','q-fin.PR','q-fin.RM','q-fin.ST','q-fin.TR','quant-ph','stat.AP','stat.CO','stat.ME','stat.ML','stat.OT']

TOY_CATEGORIES = [
  'math.PR',     # Probability
  'astro-ph.GA', # Astrophysics of Galaxies
  'hep-ph',      # High Energy Physics - Phenomenology
  'cs.HC',       # Human-Computer Interaction
]

                                       # How much sample data would be created?
                                       # 12 Months * 30 years = 360 months
                                       # 360 months * 150 subject categories = 54000
                                       # actual: train=3, validate=1, test=2
                                       #   wc -l ds3*.tsv
                                       #   63280 ds3-fulltext-small-test-20210804.tsv
                                       #   83473 ds3-fulltext-small-train-20210804.tsv
                                       #   35045 ds3-fulltext-small-validate-20210804.tsv
                                       #   63280 ds3-mixed-small-test.tsv
                                       #  108909 ds3-mixed-small-train.tsv
                                       #   35045 ds3-mixed-small-validate.tsv

CATEGORIES   = ACTIVE_CATEGORIES
READ_FILE    = 'papers-20210804.tsv'
YYMM_FILTER  = None

dataset = 12
if dataset == 2:
  CATEGORIES                = TOY_CATEGORIES
  DATASET_NAME              = 'ds2-fulltext-toy'
  TEST_PAPERS_PER_MONTH     = 4
  TRAIN_PAPERS_PER_MONTH    = 25
  VALIDATE_PAPERS_PER_MONTH = 4
                                       # 2 digit year, so: 2010-jan, 2020-jan 
                                       # 2002 wont actually be used, 
                                       #   it just triggers loop output.
  YYMM_FILTER               = ['1001', '1501', '2001', '2002'] 


elif dataset == 3:
  DATASET_NAME              = 'ds3-mixed-small'
  TEST_PAPERS_PER_MONTH     = 2
  TRAIN_PAPERS_PER_MONTH    = 4
  VALIDATE_PAPERS_PER_MONTH = 1

                                       # ds4 and ds5 is approximately where:
                                       #   split.py recoded as a single loop
                                       #   category aliases were dropped
                                       #   large full text files are truncated
                                       #   header and reference text are removed 
elif dataset == 4:
  DATASET_NAME              = 'ds4-mixed-small'
  TEST_PAPERS_PER_MONTH     = 3
  TRAIN_PAPERS_PER_MONTH    = 3
  VALIDATE_PAPERS_PER_MONTH = 1

elif dataset == 5:
  DATASET_NAME              = 'ds5-mixed-small'
  TEST_PAPERS_PER_MONTH     = 3
  TRAIN_PAPERS_PER_MONTH    = 2
  VALIDATE_PAPERS_PER_MONTH = 1

elif dataset == 6:
  DATASET_NAME              = 'ds6-mixed-tiny'
  TEST_PAPERS_PER_MONTH     = 1
  TRAIN_PAPERS_PER_MONTH    = 1
  VALIDATE_PAPERS_PER_MONTH = 1

elif dataset == 7:
  DATASET_NAME              = 'ds7-mixed-small'
  TEST_PAPERS_PER_MONTH     = 5
  TRAIN_PAPERS_PER_MONTH    = 5
  VALIDATE_PAPERS_PER_MONTH = 1

elif dataset == 8:
  DATASET_NAME              = 'ds8-mixed-large'
  TEST_PAPERS_PER_MONTH     = 5
  TRAIN_PAPERS_PER_MONTH    = 100
  VALIDATE_PAPERS_PER_MONTH = 5

elif dataset == 9:
  DATASET_NAME              = 'ds9-mixed-all'
  TEST_PAPERS_PER_MONTH     = 5
  TRAIN_PAPERS_PER_MONTH    = 1000
                                       # 20% validation is suggested for small datasets
                                       #   this is larger so maybe ok, 
                                       #     also some category-month counts are small
  VALIDATE_PAPERS_PER_MONTH = 10

elif dataset == 10:
  DATASET_NAME              = 'ds10-mixed-large'
  TEST_PAPERS_PER_MONTH     = 5
  TRAIN_PAPERS_PER_MONTH    = 50
  VALIDATE_PAPERS_PER_MONTH = 5

elif dataset == 11:
  DATASET_NAME              = 'ds11-mixed-large'
  TEST_PAPERS_PER_MONTH     = 5
  TRAIN_PAPERS_PER_MONTH    = 25
  VALIDATE_PAPERS_PER_MONTH = 5

elif dataset == 12:
  DATASET_NAME              = 'ds12-recent-papers'
  TEST_PAPERS_PER_MONTH     = 2000
  TRAIN_PAPERS_PER_MONTH    = 0
  VALIDATE_PAPERS_PER_MONTH = 0
  READ_FILE                 = 'papers-1937098-1964332.tsv'



                                       # awk '{print $1}' papers-20210804.tsv  | sort -u | wc -l
                                       # 1914188
read_file     = f'{ READ_FILE }'                 # must be sorted by yymm
train_file    = f'{ DATASET_NAME }-train.tsv'    # for fastai to build the model
validate_file = f'{ DATASET_NAME }-validate.tsv' # for fastai to refine the model
test_file     = f'{ DATASET_NAME }-test.tsv'     # for arxiv to test the finished model

wtf = open(train_file, 'w', newline='\n')
wt = csv.writer(wtf, csv.unix_dialect, quoting=csv.QUOTE_MINIMAL, delimiter='\t')
wvf = open(validate_file, 'w', newline='\n')
wv = csv.writer(wvf, csv.unix_dialect, quoting=csv.QUOTE_MINIMAL, delimiter='\t')
wxf = open(test_file, 'w', newline='\n')
wx = csv.writer(wxf, csv.unix_dialect, quoting=csv.QUOTE_MINIMAL, delimiter='\t')

yymm_papers = {}
with open(read_file) as rf:
  r = csv.reader(rf, csv.excel_tab)
  next(r)

  previous_yymm = None
  primary_category = None
  i = 0
  for row in r:
    i += 1
    #if i > 23700:
    #  break

    if len(row) != 15:
      print(f'BUG: 15 rows != {len(row)} rows')
      continue

    else: 
      document_id    = row[0]
      paper_id       = row[1]
      version        = row[2]
      yymm           = row[3]
      abs_categories = row[5]
      title          = row[13]
      abstract       = row[14]

      if YYMM_FILTER and yymm not in YYMM_FILTER:
        continue

      primary_category = None
      if abs_categories:
        for k,v in CATEGORY_ALIASES.items():
          abs_categories.replace(k,v)
        primary_category = abs_categories.split()[0]

                                       # Ignore deprecated subject-categories.
      if primary_category not in CATEGORIES:
        print(f'Ignore cat: { primary_category }.')
        continue

                                       # Read the next row of the sorted tsv.
                                       # If we've reached a new year-month,
                                       # then print the number of random papers
                                       #   from each category requested.
      if yymm != previous_yymm:
        print(f'Read papers from yymm: { previous_yymm }. Saving, then will read from yymm: {yymm}.')

        for k in yymm_papers.keys():
          papers_by_category = yymm_papers.get(k)
          if papers_by_category:
                                       # NEW CODE:

            size = len(papers_by_category)
            print(f'cat: {k}. len(papers_by_category): { len(papers_by_category) }. yymm: {yymm}.')

            left = [
                   TRAIN_PAPERS_PER_MONTH,
                   VALIDATE_PAPERS_PER_MONTH,
                   TEST_PAPERS_PER_MONTH,
            ]
            ITRAIN    = 0
            IVALIDATE = 1
            ITEST     = 2

            starting_index = random.randint(0,size-1)
            whos_up = ITRAIN
            if left[whos_up] <= 0:
              whos_up = (whos_up+1) % 3
            if left[whos_up] <= 0:
              whos_up = (whos_up+1) % 3

            write_here = None
            i = 0
            while i < size and sum(left) > 0:
              #print(f'  Category:{k}: size:{size}, i:{i}, left:{left}, whos_up:(whos_up)')
              chosen_paper = papers_by_category[starting_index]

              if whos_up == ITRAIN:
                write_here = wt
                left[ITRAIN] -= 1
              elif whos_up == IVALIDATE:
                write_here = wv
                left[IVALIDATE] -= 1
              elif whos_up == ITEST:
                write_here = wx
                left[ITEST] -= 1
              write_here.writerow(chosen_paper)
              #print(f'  Category:{ k }: size:{size}, this_many:{this_many}, so_far:{so_far}, this_paper:{this_paper}')

                                       # Which dataset type needs papers?
              whos_up = (whos_up+1) % 3
              if left[whos_up] <= 0:
                whos_up = (whos_up+1) % 3
              if left[whos_up] <= 0:
                whos_up = (whos_up+1) % 3

              i += 1                   # How many items have we looked at?
                                       # Where are we in the the list?
              starting_index = (starting_index+1)%size      


        #print(f'yymm: { yymm }. sum: { sum([ len(x) for x in yymm_papers.values() ]) }.')
        yymm_papers.clear()

                                       # Store paper by: yymm and subcategory
      papers_by_category = yymm_papers.get(primary_category)
      if not papers_by_category:
        papers_by_category = []
        yymm_papers[primary_category] = papers_by_category
      paper_to_add = [document_id, paper_id, version, yymm, primary_category, title, abstract]
      papers_by_category.append(paper_to_add)

                                       # To track when the year-month changes
                                       #   in the sorted input file
      previous_yymm = yymm

wtf.close()
wvf.close()
wxf.close()

