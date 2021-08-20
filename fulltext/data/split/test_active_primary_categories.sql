# File: test_active_primary_categories.sql
# Use:
#       mysql --defaults-extra-file=~/.my.db-rep.ro.cnf -BCN arxiv <  test_active_primary_categories.sql | tr '\t' ',' > test_active_primary_categories.csv
#       cat test_active_primary_categories.csv | tr -d '\n'

select substring_index(abs_categories,' ',1) primary_category, 
       count(*)
  from arXiv_metadata
 where 1=1
   and is_withdrawn = 0
   and is_current   = 1
   and abs_categories is not null
 group by 1
 order by 2 desc
;

quit
;


select count(*)
  from arXiv_metadata
 where 1=1
   and is_withdrawn = 0
   and is_current   = 1
   and abs_categories is null
;
yes - 1891826
no  - 0


+-----------------------+----------+
| primary_category      | count(*) |
+-----------------------+----------+
| 'hep-ph',             |   116240 |
| 'astro-ph',           |    94102 |
| 'hep-th',             |    93073 |
| 'quant-ph',           |    82896 |
| 'cond-mat.mes-hall',  |    52717 |
| 'gr-qc',              |    51710 |
| 'cond-mat.mtrl-sci',  |    46511 |
| 'cs.CV',              |    45116 |
| 'cond-mat.str-el',    |    40268 |
| 'cs.LG',              |    38540 |
| 'math.AP',            |    35504 |
| 'cond-mat.stat-mech', |    35346 |
| 'astro-ph.SR',        |    34969 |
| 'astro-ph.GA',        |    33949 |
| 'math.CO',            |    33448 |
| 'astro-ph.CO',        |    33033 |
| 'math.PR',            |    30981 |
| 'nucl-th',            |    29709 |
| 'astro-ph.HE',        |    29264 |
| 'math.AG',            |    28775 |
| 'math-ph',            |    27743 |
| 'cs.IT',              |    27147 |
| 'cond-mat.supr-con',  |    27124 |
| 'math.NT',            |    24649 |
| 'math.DG',            |    23299 |
| 'cond-mat.soft',      |    22607 |
| 'physics.optics',     |    21089 |
| 'cs.CL',              |    21086 |
| 'math.OC',            |    20449 |
| 'hep-ex',             |    20000 |
| 'math.NA',            |    18855 |
| 'math.DS',            |    17466 |
| 'astro-ph.EP',        |    16225 |
| 'hep-lat',            |    16003 |
| 'math.FA',            |    15446 |
| 'astro-ph.IM',        |    13462 |
| 'cs.AI',              |    12994 |
| 'physics.flu-dyn',    |    12715 |
| 'math.GT',            |    12648 |
| 'math.CA',            |    12411 |
| 'cs.CR',              |    12310 |
| 'math.RT',            |    12058 |
| 'stat.ME',            |    11908 |
| 'stat.ML',            |    11683 |
| 'cs.NI',              |    11485 |
| 'math.ST',            |    11391 |
| 'cond-mat',           |    11326 |
| 'cs.DS',              |    11198 |
| 'cond-mat.quant-gas', |    11129 |
| 'physics.ins-det',    |    11075 |
| 'math.GR',            |    11003 |
| 'physics.atom-ph',    |    10253 |
| 'nucl-ex',            |    10156 |
| 'cond-mat.dis-nn',    |    10032 |
| 'cs.RO',              |     9689 |
| 'physics.soc-ph',     |     9483 |
| 'cs.DC',              |     8925 |
| 'math.RA',            |     8544 |
| 'physics.plasm-ph',   |     8449 |
| 'math.CV',            |     8386 |
| 'eess.SP',            |     8108 |
| 'physics.gen-ph',     |     8060 |
| 'physics.chem-ph',    |     8053 |
| 'math.QA',            |     7797 |
| 'cs.LO',              |     7761 |
| 'math.LO',            |     7414 |
| 'cs.SE',              |     7281 |
| 'cs.SI',              |     7033 |
| 'math.AT',            |     6969 |
| 'math.OA',            |     6727 |
| 'math.AC',            |     6574 |
| 'stat.AP',            |     6564 |
| 'cond-mat.other',     |     6395 |
| 'physics.app-ph',     |     6370 |
| 'cs.CY',              |     6217 |
| 'physics.comp-ph',    |     6074 |
| 'nlin.CD',            |     5944 |
| 'eess.IV',            |     5767 |
| 'q-bio.PE',           |     5738 |
| 'cs.IR',              |     5247 |
| 'cs.SY',              |     5060 |
| 'physics.bio-ph',     |     5045 |
| 'physics.acc-ph',     |     4965 |
| 'cs.GT',              |     4854 |
| 'math.MG',            |     4829 |
| 'eess.SY',            |     4794 |
| 'cs.HC',              |     4676 |
| 'nlin.SI',            |     4432 |
| 'cs.NE',              |     4318 |
| 'q-bio.NC',           |     4265 |
| 'cs.DB',              |     4203 |
| 'physics.class-ph',   |     3984 |
| 'cs.CC',              |     3927 |
| 'math.SG',            |     3886 |
| 'math.SP',            |     3853 |
| 'cs.DM',              |     3779 |
| 'nlin.PS',            |     3681 |
| 'cs.PL',              |     3478 |
| 'q-bio.QM',           |     3366 |
| 'cs.CG',              |     3173 |
| 'physics.med-ph',     |     2955 |
| 'math.CT',            |     2943 |
| 'physics.data-an',    |     2820 |
| 'math.GM',            |     2768 |
| 'stat.CO',            |     2746 |
| 'physics.geo-ph',     |     2707 |
| 'eess.AS',            |     2588 |
| 'cs.SD',              |     2555 |
| 'physics.hist-ph',    |     2525 |
| 'math.GN',            |     2505 |
| 'cs.DL',              |     2473 |
| 'physics.ao-ph',      |     2433 |
| 'physics.ed-ph',      |     2366 |
| 'cs.CE',              |     2317 |
| 'math.HO',            |     2208 |
| 'nlin.AO',            |     2186 |
| 'cs.FL',              |     2127 |
| 'q-bio.BM',           |     2119 |
| 'math.KT',            |     2078 |
| 'q-bio.MN',           |     1876 |
| 'cs.OH',              |     1845 |
| 'chao-dyn',           |     1764 |
| 'physics.space-ph',   |     1679 |
| 'cs.MA',              |     1504 |
| 'cs.AR',              |     1469 |
| 'cs.MM',              |     1445 |
| 'q-fin.ST',           |     1434 |
| 'cs.GR',              |     1381 |
| 'q-bio.GN',           |     1373 |
| 'cs.ET',              |     1307 |
| 'q-fin.GN',           |     1269 |
| 'alg-geom',           |     1201 |
| 'econ.GN',            |     1193 |
| 'q-alg',              |     1175 |
| 'econ.EM',            |     1168 |
| 'physics.pop-ph',     |     1126 |
| 'physics.atm-clus',   |     1088 |
| 'cs.NA',              |     1072 |
| 'q-fin.MF',           |     1043 |
| 'q-fin.PR',           |     1023 |
| 'cs.SC',              |      981 |
| 'q-fin.RM',           |      899 |
| 'q-bio.TO',           |      896 |
| 'cmp-lg',             |      890 |
| 'cs.PF',              |      857 |
| 'solv-int',           |      842 |
| 'cs.MS',              |      823 |
| 'q-fin.CP',           |      820 |
| 'q-fin.PM',           |      813 |
| 'q-bio.CB',           |      796 |
| 'q-fin.TR',           |      772 |
| 'q-bio.OT',           |      620 |
| 'q-bio.SC',           |      613 |
| 'econ.TH',            |      586 |
| 'dg-ga',              |      557 |
| 'stat.OT',            |      481 |
| 'patt-sol',           |      449 |
| 'nlin.CG',            |      446 |
| 'q-fin.EC',           |      378 |
| 'cs.OS',              |      359 |
| 'funct-an',           |      318 |
| 'adap-org',           |      304 |
| 'mtrl-th',            |      165 |
| 'comp-gas',           |      139 |
| 'chem-ph',            |      128 |
| 'cs.GL',              |       92 |
| 'supr-con',           |       69 |
| 'atom-ph',            |       68 |
| 'acc-phys',           |       47 |
| 'plasm-ph',           |       27 |
| 'ao-sci',             |       13 |
| 'bayes-an',           |       11 |
+-----------------------+----------+



mysql> select substring_index(abs_categories,' ',1) primary_category,
    ->        count(*)
    ->   from arXiv_metadata
    ->  where 1=1
    ->    and is_withdrawn = 0
    ->    and is_current   = 1
    ->    and abs_categories is not null
    ->    and paper_id like '2105%'
    ->  group by 1
    ->  order by 2 desc
    -> ;
+--------------------+----------+
| primary_category   | count(*) |
+--------------------+----------+
| cs.LG              |      976 |
| cs.CV              |      969 |
| quant-ph           |      621 |
| cs.CL              |      575 |
| hep-ph             |      429 |
| cond-mat.mtrl-sci  |      343 |
| gr-qc              |      340 |
| hep-th             |      321 |
| cond-mat.mes-hall  |      306 |
| math.AP            |      303 |
| astro-ph.GA        |      294 |
| math.NA            |      281 |
| cs.IT              |      275 |
| math.OC            |      269 |
| math.CO            |      268 |
| cs.CR              |      243 |
| cs.RO              |      239 |


mysql> select substring_index(abs_categories,' ',1) primary_category,
    ->        count(*)
    ->   from arXiv_metadata
    ->  where 1=1
    ->    and is_withdrawn = 0
    ->    and is_current   = 1
    ->    and abs_categories is not null
    ->    and paper_id like '1106%'
    ->  group by 1
    ->  order by 2 desc
    -> ;
+--------------------+----------+
| primary_category   | count(*) |
+--------------------+----------+
| hep-ph             |      404 |
| hep-th             |      338 |
| astro-ph.CO        |      338 |
| quant-ph           |      287 |
| cond-mat.mes-hall  |      242 |
| astro-ph.SR        |      219 |
| cond-mat.mtrl-sci  |      183 |
| gr-qc              |      177 |
| cond-mat.str-el    |      163 |
| astro-ph.HE        |      149 |
| math.CO            |      143 |
| math-ph            |      137 |
| cond-mat.stat-mech |      133 |
| math.PR            |      128 |
| cond-mat.supr-con  |      127 |
| cs.AI              |      124 |
| math.AG            |      115 |
| astro-ph.GA        |      103 |
| math.NT            |       97 |
| math.AP            |       95 |
| cs.IT              |       92 |
| nucl-th            |       92 |
| hep-ex             |       89 |
| math.DG            |       88 |
| astro-ph.EP        |       83 |



