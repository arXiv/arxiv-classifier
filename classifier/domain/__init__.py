"""Classifier domain classes."""

from dataclasses import dataclass

from arxiv.taxonomy import Category

@dataclass
class ClassifierPrediction:
    """Represents a classification prediction."""
    
    category: Category
    """Category for the prediction."""

    probability: float
    """Probability of the category."""
