"""Classifier domain classes."""

from dataclasses import dataclass, field
from typing import List

from arxiv.taxonomy import Category

@dataclass
class ClassifierPrediction:
    """Represents a classification prediction."""
    
    category: Category
    """Category for the prediction."""

    probability: float
    """Probability of the category."""


@dataclass
class Article:
    """Represents an article to classify."""

    title: str = None
    """Title of the article."""

    authors: List[str] = field(default_factory=list)
    """List of the authors."""

    abstract: str = None
    """Abstract of the article."""

    fulltext: str = None
    """Full text of the article."""

    @classmethod
    def from_dict(cls, doc: dict) -> 'Article':
        """
        Create an article object from a dictionary of fields.
        """

        return Article(
            title=doc.get('title', ''),
            abstract=doc.get('abstract', ''),
            authors=[],  # ignore for now
            fulltext=doc.get('fulltext', '')
        )

