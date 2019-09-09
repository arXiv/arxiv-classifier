import os

from gensim import models

import logging
logging.basicConfig(
    format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO
)


def _apply_phraser(infile, outfile, phraser):
    """
    Simply apply the phraser to all documents in a file.

    Parameters
    ----------
    infile : string
        Input file of documents, one per line

    outfile : string
        Output file of phrased documents, one per line

    phraser : `gensim.models.Phraser`
    """
    with open(infile) as si, open(outfile, 'w') as so:
        for line in si:
            words = line.split()
            output = ' '.join(phraser[words])
            so.write('{}\n'.format(output))


def _form_ngrams(infile, outfile, min_count=20, threshold=10.0):
    """
    Takes input and output filenames to generate the next ngram level

    Parameters
    ----------
    infile : string
        File name of text file of documents

    outfile : string
        Filename of output file

    min_count : integer
        Mininum occupancy to remain in the vocabulary

    threshold : float
        See `ngram`
    """
    sentences = models.word2vec.LineSentence(infile)
    phrases = models.phrases.Phrases(
        sentences, min_count=min_count, threshold=threshold
    )
    phraser = models.phrases.Phraser(phrases)
    _apply_phraser(infile, outfile, phraser)


def ngram(infile, min_count=30, depth=5, threshold_sched=10.0):
    """
    Given a text file where one line represents one document, form the same
    document with ngrams, where the maximum length of the concatenated text
    is 2**depth words.

    Parameters
    ----------
    infile : string
        Filename of combined documents

    min_count : integer
        Ignore all words and bigrams with total collected count less than this

    depth : integer
        Number of iterations to run ngram formation

    threshold_sched : float, list of floats
        Score threshold for creating phrases, score defined by:
            (count(worda followed by wordb) - min_count) /
                (count(worda) * count(wordb)) > threshold / N
        Our default schedule is [400, 300, 200, 100]

    Returns
    -------
    filenames : list of strings
        The names of each intermediate (and final) phrased document files
    """
    if isinstance(threshold_sched, list) and len(threshold_sched) != depth:
        raise ValueError("`threshold_sched` length does not match `depth`")

    root, ext = os.path.splitext(infile)

    fnames = ['{}-{}gram{}'.format(root, i+2, ext) for i in range(depth-1)]
    sequence = [infile] + fnames

    if not isinstance(threshold_sched, (list, tuple)):
        threshold_sched = [threshold_sched]*depth

    for i in range(len(sequence)-1):
        iname, oname = sequence[i], sequence[i+1]
        _form_ngrams(
            iname, oname, min_count=min_count,
            threshold=threshold_sched[i]
        )
    return fnames
