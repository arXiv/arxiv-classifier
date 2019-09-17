"""
Calling the classifier service.
"""
from typing import List

from classifier.domain import ClassifierPrediction

import classifier.services.naivebayes

def classify(content: bytes) -> List[ClassifierPrediction]:
    """Performs a classification."""

    naivebayes.classify()
    