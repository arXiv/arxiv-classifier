# File: export-papers-20210804.sql
# Desc: Get metadata from the arXiv database.
#       The paper version is needed to lookup the text files that usually exist in /data/txt.
# Use:  mysql --defaults-extra-file=~/.my.db-rep.ro.cnf -BC arXiv < export-papers.sql > export-papers-sample.tsv

select m.paper_id,
       m.version,
       case when instr(paper_id, '/')=0 then substr(paper_id,1,4) 
            else substr(paper_id,instr(paper_id, '/')+1,4)
       end yymm,
       m.created,
       m.abs_categories,
       m.submitter_id,
       m.source_format,
       m.source_size,
       m.source_flags,
       ( select s.remote_host 
           from arXiv_submissions s 
          where s.document_id = m.document_id 
            and s.doc_paper_id = m.paper_id 
          limit 1 
       ) remote_host,
       d.country,
       replace(m.authors,  '\t',' ') authors,
       replace(m.title,    '\t',' ') title,
       replace(m.abstract, '\t',' ') abstract
  from arXiv_metadata m
  left join arXiv_demographics d on d.user_id = m.submitter_id
 where m.is_withdrawn = 0
   and m.is_current   = 1
   and
 order by 3,1
 limit 20
;



# The first 500k arxiv papers were not submitted using the database.
# select document_id, paper_id,abs_categories  
#   from arXiv_metadata m 
#  where m.is_withdrawn = 0 
#    and m.is_current   = 1 
#    and not exists (select 1 from arXiv_submissions s where s.document_id = m.document_id) 
#  limit 1;
# +-------------+------------+----------------+
# | document_id | paper_id   | abs_categories |
# +-------------+------------+----------------+
# |           1 | cs/0001020 | cs.CL          |
# +-------------+------------+----------------+

