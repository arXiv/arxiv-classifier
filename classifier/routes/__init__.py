"""arxiv classifier routes."""
from typing import Union

from flask import Blueprint, request, Response

from arxiv.base import logging
from classifier.controllers import health_check

logger = logging.getLogger(__name__)

blueprint = Blueprint('classifier', __name__, url_prefix='/')

@blueprint.route('classify', methods=['POST'])
def service_status() -> Union[str, Response]:
    """Health check endpoint for classifier."""
    doc = request.args.get('doc')
    # TODO: serialize response into JSON
    return classify(doc) # type: ignore

@blueprint.route('status', methods=['GET', 'HEAD'])
def service_status() -> Union[str, Response]:
    """Health check endpoint for classifier."""
    return health_check() # type: ignore