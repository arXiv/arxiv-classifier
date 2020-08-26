"""
Houses controllers for classifier service.

Each controller function returns a 3-tuple of response data (``dict``), 
status code (``int``), and extra response headers (``dict``).
"""
from typing import Any, Dict, IO, List, Tuple
from werkzeug.exceptions import InternalServerError, ServiceUnavailable
import logging

from arxiv import status

from classifier.routes import serialize
from classifier.domain import ClassifierPrediction
from classifier.services import classifier
import json

logger = logging.getLogger(__file__)

def classify_stream(doc: IO[bytes]) -> List[ClassifierPrediction]:
    """
    Classification of a document stream.

    Parameters
    ----------
    doc
        byte stream of the document.

    Returns
    -------
    list
        List of :class:`ClassifierPrediction` objects.

    """
    doc = json.load(doc)
    if not isinstance(doc, dict):
        raise Exception('Incorrect input format')
    return classifier.classify(doc)

def health_check() -> Tuple[str, int, Dict[str, Any]]:
    """
    Exercise the connection with the classifier service.

    Returns
    -------
    dict
        Search result response data.
    int
        HTTP status code.
    dict
        Headers to add to the response.

    """
    try:
        classification = classifier.classify({'title':'this is a title',
                                              'abstract':'this is the abstract of the article'})
    except Exception as ex:
        raise InternalServerError('DOWN: classifier failed') from ex

    if not all([hasattr(catp,'probability') and hasattr(catp, 'category')
            for catp
            in classification] ):
        logger.error(f"malformed results: {classification}")
        raise InternalServerError('DOWN: malformed classifier results')

    try:
        test = serialize.as_json( classification )
    except Exception as ex:
        logger.error(ex)
        raise InternalServerError('DOWN: serialize of classifier result failed') from ex

    return 'OK', status.HTTP_200_OK, {}


