import random
import re
import io
import os


def random_indices(iterable):
    """
    Generate a list of indices from an iterable (hence consuming it). From
    that, shuffle the indices to obtain a random order.

    Parameters
    ----------
    iterable : iterable
        Any object with __iter__ and next

    Returns
    -------
    order : list of ints
        Permuted list of indices
    """
    lst = list(iterable)
    random_order = list(range(len(lst)))
    random.shuffle(random_order)
    return random_order


class ArticleIterator:
    def __init__(self, filename, chunksize=10000):
        """
        An object for iterating through a large, concatenated text file
        (randomly) without loading the entire thing in memory. However, it will
        still require 8*n_articles bytes to do the selection since it is not
        possible to shuffle an iterator. (An alternative is to shuffle in
        chunks as TF does with Dataset)

        Parameters
        ----------
        filename : str
            Filename of concatenated texts (one per line) which to
            iterate through

        chunksize : int
            Size of read buffer in bytes
        """
        self.filename = filename
        self.chunksize = chunksize

    def _chunks(self):
        """
        Read out the file in chunks given by class properties (self.chunksize),
        yielding the file location (integer of byte index) and content as a
        tuple. This function is a generator.

        Returns
        -------
        chunks : generator
            Tuples of (byte_index, text)
        """
        with open(self.filename, 'rb') as fn:
            while True:
                loc = fn.tell()
                out = fn.read(self.chunksize)
                if not out:
                    break
                yield loc, out

    def segments(self):
        """
        Get all pairs of byte indices defining the location of each line in the
        file yielding the segments as tuples of (start, end) indices.

        Returns
        -------
        segments : generator
            Tuples of (start, end) byte indices of each line (defined by '\\n')
        """
        last = 0
        for loc, chunk in self._chunks():
            matches = re.finditer(b'\n', chunk)
            for m in matches:
                yield (last, loc + m.start())
                last = loc + m.start()

    def iter_random(self, order=None):
        """
        Iterate through the file by line, shuffled randomly

        Parameters
        ----------
        order : None or list of integers
            If not None, but be a list of indices corresponding to
            line numbers, the order in which to output them.

        Returns
        -------
        lines : generator
            Iterable of strings, each line of the file
        """
        segments = list(self.segments())

        if order is None:
            order = random_indices(segments)

        with open(self.filename, 'rb') as f:
            for index in order:
                seg = segments[index]
                f.seek(seg[0], os.SEEK_SET)
                yield f.read(seg[1] - seg[0]).strip().decode('utf-8')

    def iter_sequential(self):
        """
        Iterate through the file sequentially by line

        Returns
        -------
        lines : generator
            Iterable of strings, each line of the file
        """
        with open(self.filename, 'rb') as f:
            for seg in self.segments():
                yield f.read(seg[1] - seg[0]).strip().decode('utf-8')

    def shuffled_file(self, filename=None, order=None):
        """
        Transform the original file by shuffling the lines and saving
        to a new one.

        Parameters
        ----------
        filename : string
            Output filename

        order : None or list of ints
            If a particular order of lines is required, use that one.
            See iter_random for more information
        """
        with open(filename, 'w') as f:
            for line in self.iter_random(order=order):
                f.write('{}\n'.format(line.decode('utf-8')))
