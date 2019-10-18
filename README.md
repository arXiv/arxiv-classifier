# arxiv-classifier

# How to Train
```
nb = ArticleClassifier(dbpath='/path/to/db')
fn = nb.create_input_file(metadata)
nb.train(fn)
nb.save()
   
```
# How to Classify
```
nb = ArticleClassifier(dbpath='/path/to/db')
nb.load()
fn = nb.create_input_file(metadata)
classes = nb.classify(fn)
```

In these examples, metadata should be a List of Dict where the Dict are in the format given below. The file name paths are relative to the current machine (on the local file system):

```
{
  "id": "1704.00222",
  "categories": ["cs.NM", "hep-th"],
  "filename": "/path/to/file.txt"
}
```

# Trained Models

Trained model for use by arXiv staff can be found at s3://arxiv-classifier-models 
