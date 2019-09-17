"""Tests for :mod:`services.classifier.bayes`."""

from unittest import TestCase, mock

import classifier.services.classifier.bayes as bayes

class PretrainedTest(TestCase):
    def setUp(self):
        """We have an app."""
        self.modelfile = '/home/jaimie/workspace/arxiv/arxiv-classifier/trained-model.pkl'

