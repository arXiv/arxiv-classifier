"""Tests for :mod:`routes`."""

from unittest import TestCase, mock

from flask import Flask

from arxiv import status

import classifier.routes

class APITest(TestCase):
    def setUp(self):
        """We have an app."""
        self.app = Flask('test')
        self.app.config['MAX_PAYLOAD_SIZE_BYTES'] = 10 * 1_028
        self.app.register_blueprint(classifier.routes.blueprint)
        self.client = self.app.test_client()


class TestHealthCheck(APITest):
    """Tests for :func:`.health_check`."""

    @mock.patch('classifier.routes.health_check')
    def test_service_status_returns_result(self, mock_health_check):
        """Test returns 'OK' + status 200 when classify returns results."""
        mock_response = ('OK', status.HTTP_200_OK, {})
        mock_health_check.return_value = mock_response

        response = self.client.get('/status')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, 'OK')


class TestClassify(APITest):
    @mock.patch('classifier.routes.request')
    def test_classify_returns_result(self, mock_request):
        """Test returns 'OK' + status 200 when classify returns results."""
        mock_request.args = {'doc': 'this is a test'}

        self.assertEqual(classifier.routes.classify(), '{"result": "this is a test"}')