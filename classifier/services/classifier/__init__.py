"""
Calling the classifier service.
"""
from typing import List

from classifier.domain import ClassifierPrediction, Article

import classifier.services.classifier.naivebayes

from flask import g, current_app
from classifier.classifiers import CategoryClassifier
from classifier.classifiers.ulmfit import ULMFiTClassifier
from werkzeug.exceptions import InternalServerError

import functools

def create_classifier() -> CategoryClassifier:
    """
    Creates a new arXiv category classifier based on configuration of the current app.

    Returns
    -------
    classifier
    """
    classifier_type = current_app.config.get('CLASSIFIER_TYPE', 'ulmfit')
    if classifier_type == 'ulmfit':
        model_path = current_app.config['CLASSIFIER_PATH']
        return ULMFiTClassifier(model_path)
    else:
        raise InternalServerError(f'Unknown classifier type: {classifier_type}')


def get_classifier() -> CategoryClassifier:
    """
    Gets classifier from the current app's context, creates it if necessary.

    Returns
    -------
    classifier
    """
    if 'classifier' not in g:
        g.classifier = create_classifier()
    return g.classifier


def classify(doc: dict) -> List[ClassifierPrediction]:
    """Performs a classification.

    Returns
    -------
    list
        List of :class:`ClassifierPrediction` objects.
    """

    article = Article.from_dict(doc)
    return classify_article(article)


@functools.lru_cache()
def classify_article(article: Article) -> List[ClassifierPrediction]:
    return get_classifier().classify(article)
