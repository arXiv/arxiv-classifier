from typing import IO, List, Tuple

import os
import re
import time
import random
import collections
import itertools
import numpy as np

from sklearn.feature_extraction.text import HashingVectorizer
from sklearn import naive_bayes
from sklearn.externals import joblib

from arxiv.base import logging
import arxiv.taxonomy
from . import ngrams, textutil

logger = logging.getLogger(__name__)
logger.propagate = False


class UntrainedModelException(RuntimeError):
    pass

class ArticleClassifier:
    def __init__(self, filename: str):
        self.savefile = filename

        if os.path.exists(filename):
            self.load()

    @property
    def trained(self):
        return hasattr(self, 'classifier')


    def iterfile(self, infile, random=False):
        if random:
            data_stream = ArticleIterator(infile).iter_random()
        else:
            data_stream = ArticleIterator(infile).iter_sequential()

        batcher = iter_minibatches(data_stream, self.nbatch)
        for i, (tvec, cvec) in enumerate(batcher):
            xvec = self.vectorizer.transform(tvec)
            yvec = [self.cat2ind.get(c, 0) for c in cvec]
            yvec = np.array(yvec, dtype='int')
            yield xvec, yvec
    
    def _iterstream(self, stream, random=False):
        if random:
            # TODO: Implement random stream processing
            raise NotImplementedError("Stream randomization not yet randomized.")

        text = textutil.clean_text(stream)
        vec = self.vectorizer.transform(text)
        classes = [self.cat2ind.get(c, 0) for c in arxiv.taxonomy.CATEGORIES]
        return vec, classes


    def classify(self, stream: IO) -> List[str]:
        """
        Return the categories of a train file `infile`.

        Parameters
        ----------
        stream : IO
            Streaming IO of article content

        Returns
        -------
        categories : list of strings
            Categories associated with each line of the article file
        """
        if not self.trained:
            raise UntrainedModelException("Model must be trained before use")

        predictions = []
        for i, (x, y) in enumerate(self.iterstream(stream)):
            predictions.extend(self.classifier.predict(x))
            logger.debug('Partial classify {}'.format(i))
        return [self.ind2cat[i] for i in predictions]

    def save(self):
        """
        Save the trained classifier to disk so that it be loaded again in the
        future (using scikit-learn's custom pickle dump)
        """
        if self.trained:
            joblib.dump([
                    self.classifier, self.vectorizer,
                    self.cat2ind, self.ind2cat
                ], self.savefile
            )

    def load(self):
        """
        Load the trained classifier from the database directory
        """
        parts = joblib.load(self.savefile)
        self.classifier = parts[0]
        self.vectorizer = parts[1]
        self.cat2ind = parts[2]
        self.ind2cat = parts[3]

def decode_doc(doc: str) -> Tuple[str, List[str], str]:
    """
    Given a training line, extract the articles metadata.

    Parameters
    ----------
    doc : string
        Training line

    Returns
    -------
    art : string
        Article id

    cat : list of string
        List of categories

    text : string
        Full text of article
    """
    art, cat, text = doc.split('|')
    art = art.strip()
    cat = next(iter([c.strip() for c in cat.split()]), '')
    text = text.strip()
    return art, cat, text


def get_minibatch(doc_iter, size):
    t, c = [], []

    for doc in itertools.islice(doc_iter, size):
        art, cat, text = decode_doc(doc)

        if cat:
            t.append(text)
            c.append(cat)

    return t, c

def iter_minibatches(doc_iter, nbatch):
    """Generator of minibatches."""
    t, y = get_minibatch(doc_iter, nbatch)
    while len(t):
        yield t, y
        t, y = get_minibatch(doc_iter, nbatch)
