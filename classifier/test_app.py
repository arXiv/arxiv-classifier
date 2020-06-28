"""
An application for end-to-end testing purposes.
"""
from flask import Flask
from classifier.routes import blueprint
from classifier.services.classifier import get_classifier


def create_app(config=None):
    app = Flask(__name__)
    app.config['MAX_PAYLOAD_SIZE_BYTES'] = 2**20
    app.config['CLASSIFIER_TYPE'] = 'ulmfit'
    app.config['CLASSIFIER_PATH'] = 'models/abstracts-classifier.pkl'
    app.register_blueprint(blueprint)

    # init classifier to avoid delay on the first request
    with app.app_context():
        get_classifier()

    return app
