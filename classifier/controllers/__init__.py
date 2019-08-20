"""
Houses controllers for classifier service.

Each controller function returns a 3-tuple of response data (``dict``), 
status code (``int``), and extra response headers (``dict``).
"""
from typing import Tuple, Dict, Any
from arxiv import status
from ..services import classifier


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
    except Exception:
        return 'DOWN', status.HTTP_503_SERVICE_UNAVAILABLE, {}
    if classification['results']:
        return 'OK', status.HTTP_200_OK, {}
    return 'DOWN', status.HTTP_500_INTERNAL_SERVER_ERROR, {}
