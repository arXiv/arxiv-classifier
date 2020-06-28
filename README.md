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


# ULMFiT classifier

## Training

See [experiments directory](experiments/) for training and evaluation notebooks.

## Models

The ULMFiT and SentencePiece model files can be downloaded [here](https://github.com/arXiv/arxiv-classifier/releases/download/ulmfit-models-v1.0/models.tar.xz). Make sure `CLASSIFIER_PATH` configuration parameter
points to `models/abstracts-classifier.pkl` and that `CLASSIFIER_TYPE` equals `ulmfit`.  

## Testing

To test the service locally you can run it with
```shell
FLASK_APP=classifier.test_app flask run --port 9999
```

and make a request:
```shell
curl -s -H "Content-Type: application/json" -X POST http://localhost:9999/classify \
    --data '{"title":"P = NP", "abstract": "We prove that P = NP for N = 1 or P = 0."}'

[{"category":"cs.CC","probability":0.8264293074607849},{"category":"cs.DS","probability":0.1285623162984848},...]
```

Both the input and output format are not yet compatible with the Naive Bayes classifier.
