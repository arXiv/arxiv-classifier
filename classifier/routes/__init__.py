"""arXiv classifier routes."""
from typing import IO

import io

from flask import Blueprint, current_app, jsonify, make_response, request, Response
from werkzeug.exceptions import HTTPException, BadRequest, RequestEntityTooLarge

import logging

from classifier.controllers import classify_stream, health_check
from . import serialize

logger = logging.getLogger(__name__)

blueprint = Blueprint('classifier', __name__, url_prefix='/')


@blueprint.app_errorhandler(HTTPException)
def handle_error(error) -> Response:
    """JSON error handler."""
    status_code = error.code
    response = {'message': error.description}

    return make_response(jsonify(response), status_code)

@blueprint.route('classify', methods=['POST'])
def classify() -> Response:
    """Classifier routing."""
    stream: IO[bytes]
    if request.headers.get('Content-type') is not None:
        # Parse stream length
        length = int(request.headers.get('Content-length', 0))
        if length == 0:
            raise BadRequest('Body empty or content-length not set')

        # Check that stream is within app size limits
        max_length = int(current_app.config['MAX_PAYLOAD_SIZE_BYTES'])
        if length > max_length:
            raise RequestEntityTooLarge(f'Body exceeds size of {max_length}')

        # Cast to BytesIO
        stream = io.BytesIO(request.data)
    else:
        # DANGER! request.stream will ONLY be available if (a) the content-type
        # header is not passed and (b) we have not accessed the body via any
        # other means, e.g. ``.data``, ``.json``, etc.
        stream = request.stream

    # Classify the stream and cast data to JSON
    results = classify_stream(stream)
    response = serialize.as_json(results)

    return response

@blueprint.route('status', methods=['GET', 'HEAD'])
def service_status() -> Response:
    """Health check endpoint for classifier."""
    data, code, headers = health_check()
    test = serialize.as_json(data)
    return make_response(data, code, headers)
