import os
import collections
import itertools

from typing import List

import numpy as np
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn import naive_bayes
import joblib

from . import ngrams, textutil
from .ticker import Ticker
from .article_iterator import ArticleIterator

MODEL_SAVEFILE = './trained-model.pkl'


class ArticleClassifier:
    def __init__(self, dbpath='./', workdir='./', nbatch=1000):
        """
        The article classifier class. Stores data in dbpath, performing
        training and classification processes to specially formatted files
        (which it creates).

        To use:

            # how to train
            nb = ArticleClassifier(dbpath='/path/to/db')
            fn = nb.create_input_file(metadata)
            nb.train(fn)
            nb.save()

            # how to classify
            nb = ArticleClassifier(dbpath='/path/to/db')
            nb.load()
            fn = nb.create_input_file(metadata)
            classes = nb.classify(fn)

        The format of the metadata is given below, where the filename paths
        are relative to the current machine (on the local filesystem):
            {
                "id": "1704.00222",
                "categories": ["cs.NM", "hep-th"],
                "filename": "/path/to/file.txt"
            }

        Parameters
        ----------
        dbpath : string
            The path of the save files for this classifier.

        workdir : string
            Path to a place for temporary files (if different than dbpath)

        nbatch : integer
            The number of articles to batch process at a time. This parameter
            is determined by memory restrictions.
        """
        self.savefile = os.path.join(dbpath, MODEL_SAVEFILE)

        self.nbatch = nbatch
        self.dbpath = dbpath
        self.workdir = workdir

    def create_input_file(self, metadata, ngram_kwargs=None):
        """
        Transform the metadata of a group of articles into the training file
        format with:

            1. article id label
            2. category information
            3. ngrammed & cleaned full text

        The reasoning behind this is to create the streaming input for
        out-of-core processing with scikit learn.

        Parameters
        ----------
        metadata : json object
            The metadata of a group of articles

        ngram_kwargs : dict
            Keywords for the ngram formation process. Defaults are preferred.
        """
        ngram_kwargs = ngram_kwargs or {}

        articles = [m.get('filename') for m in metadata]
        articlefile = os.path.join(self.workdir, 'articles.txt')

        article_per_line = self._concatenate_texts(articles, articlefile)
        # At this point, alltxt should be a file where each line is
        # the text from a single article.

        # BDC34: clean is already happening in _concatenate_texts()
        # cleanfile = textutil.clean_file(article_per_line)
        # Creates new file that should just be the same as alltxts
        # but UTF normalized and cleaned etc.

        phrase4file = self._form_ngrams(article_per_line, **ngram_kwargs)
        os.remove(article_per_line)

        # This will add the metadata back to the lines created by
        # concatenate_texts.
        metafile = self._create_meta_format(phrase4file, metadata)
        os.remove(phrase4file)

        return metafile

    def _concatenate_texts(self, articles: List[str], output_file):
        """
        Take a list of strings (filenames of article text files) and clean &
        concatenate them into a single text file where each line represents an
        article.

        Parameters
        ----------
        article_files : list of str
            List of filenames of individual article files

        output_file : string
            Filename into which to concatenate the files
        """
        with open(output_file, 'w') as output:
            for article in articles:
                with open(article) as fin:
                    for line in fin:
                        output.write(textutil.clean_text(line))
                        output.write(' ')
                output.write('\n')  # Only one \n per article, watch indent
        return output_file

    def _form_ngrams(self, articlefile, min_count=30,
                     schedule=(400, 300, 200, 100)):
        """
        Given a concatenated file ``article_file``, form the equivalent ngram
        file using a particular threshold schedule (and hence depth).

        Parameters
        ----------
        articlefile : str
            Filename of concatenated text for form ngrams

        min_count : int
            Number of minimum occurences for an ngram

        schedule : list of numbers
            Threshold score for formation of ngrams

        Returns
        -------
        outfile : str
            Filename of resulting concatenated article texts
        """
        outputs = ngrams.ngram(
            articlefile, min_count=min_count, depth=len(schedule),
            threshold_sched=schedule
        )

        for output in outputs[:-1]:
            os.remove(output)

        return outputs[-1]

    def _create_meta_format(self, articlefile, metadata):
        """
        Transform a joined articlefile with its metadata into a final full
        metadata file.
        """
        outfile = textutil.filename_descriptor(articlefile, 'meta')

        with open(articlefile) as fin, open(outfile, 'w') as fout:
            for i, (line, meta) in enumerate(zip(fin, metadata)):
                aid = meta.get('id', '')
                cats = meta.get('categories', [])
                fout.write(encode_doc(aid, cats, line))

        return outfile

    def _build_catmap(self, infile):
        """
        Construct a mapping of integers to category names
        """
        data_stream = ArticleIterator(infile).iter_sequential()
        cat_count = collections.Counter([
            decode_doc(d)[1] for d in data_stream
        ])
        if '' in cat_count:
            cat_count.pop('')

        self.cat2ind = {k: i for i, k in enumerate(sorted(cat_count.keys()))}
        self.ind2cat = {v: k for k, v in self.cat2ind.items()}

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

    @property
    def trained(self):
        return hasattr(self, 'classifier')

    def train(self, infile):
        """
        Train the classifier given a set of article metadata

        Parameters
        ----------
        infile : string
            Filename of combined article metadata
        """
        # Iterator over parsed Reuters SGML files.
        clock = Ticker()

        self._build_catmap(infile)
        class_ind = np.array(list(self.cat2ind.values()), dtype='int')
        clock.tick('Category map')

        self.classifier = naive_bayes.MultinomialNB(alpha=0.001)
        self.vectorizer = HashingVectorizer(
            decode_error='ignore', stop_words='english', norm=None,
            n_features=2**20, alternate_sign=False
        )

        for i, (x, y) in enumerate(self.iterfile(infile, random=True)):
            self.classifier.partial_fit(x, y, classes=class_ind)
            clock.tick('Partial train {}'.format(i))

    def test(self, infile, batchcount=None):
        """
        Test the accuracy of a model to predict categories by running the
        classifier and checking against the provided categories.

        Parameters
        ----------
        infile : string
            Filename of combined article metadata

        Returns
        -------
        accuracy : float
            Percentage of correct category inferences
        """
        if not self.trained:
            raise AttributeError("Model must be trained before use")

        clock = Ticker()

        stream = self.iterfile(infile, random=True)
        stream = itertools.islice(stream, batchcount)

        accuracies = []
        for i, (x, y) in enumerate(stream):
            accuracy = (
                (self.classifier.predict(x) - y) == 0
            ).astype('float').mean()
            accuracies.append(accuracy)
            clock.tick('Accuracy {}: {}'.format(i, accuracy))

        return np.mean(accuracies)

    def classify(self, infile):
        """
        Return the categories of a train file `infile`.

        Parameters
        ----------
        infile : string
            Filename of combined article metadata

        Returns
        -------
        categories : list of strings
            Categories associated with each line of the article file
        """
        clock = Ticker()

        if not self.trained:
            raise AttributeError("Model must be trained before use")

        predictions = []
        for i, (x, y) in enumerate(self.iterfile(infile)):
            predictions.extend(self.classifier.predict(x))
            clock.tick('Partial classify {}'.format(i))
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


def encode_doc(art, cat, text):
    """
    Given an article's id, categories, and fulltext, produce the training line
    of the combined file.

    Parameters
    ----------
    art : string
        Article id

    cat : list
        Categories as a list of strings

    text : string
        Full text of the article

    Returns
    -------
    train_line : string
        The formatted training line
    """
    return '{} | {} | {}'.format(art, ' '.join(cat), text)


def decode_doc(doc):
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

    # BDC34: Looks like just doing the primary category
    cat = next(iter([c.strip() for c in cat.split()]), '')

    text = text.strip()
    return art, cat, text


# def get_minibatch(doc_iter, size):
#     t, c = [], []

#     for doc in itertools.islice(doc_iter, size):
#         art, cat, text = decode_doc(doc)

#         if cat:
#             t.append(text)
#             c.append(cat)

#     return t, c


# def iter_minibatches(doc_iter, nbatch):
#     """Generator of minibatches."""
#     t, y = get_minibatch(doc_iter, nbatch)
#     while len(t):
#         yield t, y
#         t, y = get_minibatch(doc_iter, nbatch)

# BDC34 not sure how minibatch would work during classify since cat
# will always be None. Above is definitely based on minibatch functions
# from scikit sklearn out-of-core example.
#
# This version just doesn't do the batching.
def iter_minibatches(doc_iter, nbatch):
    for doc in doc_iter:
        id, cats, text = decode_doc(doc)
        yield [text], [cats]
