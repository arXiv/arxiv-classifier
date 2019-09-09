import os
import re
import string
import ftfy
import unidecode

RE_PUNCTUATION = re.compile(r'[{}]'.format(re.escape(string.punctuation)))
RE_MULTIWHITE = re.compile(r'\s+')
RE_HYPHENLINE = re.compile(r'-\s*\n\s*')
RE_CIDWORD = re.compile(r'\(cid:\d+\)')
RE_NUMBER = re.compile(r'\b[0-9]+\b')
RE_ALPHA_NUMERIC = re.compile(r'[^a-zA-Z0-9]+')


def filename_descriptor(filename, desc):
    name, ext = os.path.splitext(filename)
    return '{}-{}{}'.format(filename, desc, ext)


def normalize_unicode(txt):
    """

    Utilize several libraries to systematically remove / normalize unicode
    variations between text (into ascii) and throw away characters which
    cannot be normalized.

    Parameters
    ----------
    txt : string
        Input unicode text (utf-8) which is to be converted to ascii

    Returns
    -------
    out : string
        ASCII text reformulation of original

    """
    out = ftfy.fix_text(txt, normalization='NFKC')
    out = unidecode.unidecode(out)
    out = out.encode('ascii', 'ignore')
    out = out.decode('ascii')
    return out


def clean_text(txt):
    """
    Normalize a string by removing intra-document variations which are not
    dependent on the underlying text. Additionally, removed some unnecessary
    characters which do not assist in NLP. Specifically:
        * remove pdf2txt "cid:" identifiers
        * remove newline hyphenated words
        * remove punctuation
        * only allow alpha-numerics
        * remove pure numbers
        * collapse whitespace and remove newlines

    Parameters
    ----------
    txt : string
        Document text to clean / normalize

    Returns
    -------
    out : string
        Cleaned text, ready for segmentation into words
    """
    txt = normalize_unicode(txt)

    txt = txt.lower()
    txt = RE_CIDWORD.subn(' UNK ', txt)[0]
    txt = RE_HYPHENLINE.subn('', txt)[0]
    txt = RE_PUNCTUATION.subn(r' ', txt)[0]
    txt = RE_ALPHA_NUMERIC.subn(r' ', txt)[0]
    txt = RE_NUMBER.subn(r' ', txt)[0]

    txt = RE_MULTIWHITE.subn(' ', txt)[0]
    txt = txt.replace('\n', '')
    return txt.strip()


def clean_file(filename):
    """
    Apply `clean_text` for all lines of a file.

    Parameters
    ----------
    filename : str
        Name of input file separated into lines

    Returns
    -------
    outfile : str
        Name of output file (so we don't do this in memory)
    """
    outfile = filename_descriptor(filename, 'clean')

    with open(filename) as fin, open(outfile, 'w') as fout:
        for line in fin:
            fout.write('{}\n'.format(clean_text(line)))

    return outfile
