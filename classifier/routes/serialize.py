"""Serializers for classifer responses."""

from typing import Dict

from flask import jsonify, Response

ROUNDTO = 5

def _round_prop(catp: Dict)-> Dict:
    if hasattr(catp, 'probability'):
        catp.probability = round(catp.probability, ROUNDTO)
    return catp

def as_json(data: Dict) -> Response:
    """Converts a classifier results dictionary to JSON."""
    rounded = [_round_prop(catp) for catp in data]
    # To be comparable with earlier classifier, we Want a format that looks like:
    # x = { "classifier": [{"category":"nucl-ex","probability":".435"},
    #                      {"category":"physics.atom-ph","probability":"0.07"}],
    #       "service":"fbabs"
    #      }
    return jsonify({"classifier": data,
                    "service": "fb-abs"})
