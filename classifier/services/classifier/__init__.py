"""
Calling the classifier service.
"""
from typing import List

from classifier.domain import ClassifierPrediction

import classifier.services.classifier.naivebayes

def classify(content: bytes) -> List[ClassifierPrediction]:
    """Performs a classification."""
    
