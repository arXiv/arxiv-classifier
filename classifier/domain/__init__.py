"""Classifier domain classes."""

from dataclasses import dataclass

from arxiv.taxonomy import Category

@dataclass
class ClassificationResult:
    category: Category
    log_likelihood: float
