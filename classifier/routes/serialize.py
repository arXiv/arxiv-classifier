"""Serializers for classifer responses."""

from typing import Dict

from flask import jsonify, Response

def as_json(data: Dict) -> Response:
    """Converts a classifier results dictionary to JSON."""
    # TODO: Return to this after deciding on classification representation.
    return jsonify(data)