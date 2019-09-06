"""
Houses controllers for classifier service.

Each controller function returns a 3-tuple of response data (``dict``), 
status code (``int``), and extra response headers (``dict``).
"""
from typing import Any, Dict, IO, List, Tuple
from werkzeug.exceptions import InternalServerError, ServiceUnavailable

from arxiv import status

from classifier.domain import ClassifierPrediction
from classifier.services import classifier


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
    return []

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
        classification = classifier.classify("Sample text") # attempt a classification task
    except Exception as ex:
        raise ServiceUnavailable('DOWN') from ex

    if 'results' in classification and classification['results']:
        return 'OK', status.HTTP_200_OK, {}

    # Malformed response (i.e., missing 'results') and catch-all
    raise InternalServerError('DOWN')
