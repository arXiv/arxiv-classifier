"""Tests for :mod:`routes`."""

import json
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
        self.assertEqual(response.data, b'OK')


class TestClassify(APITest):
    @mock.patch('classifier.routes.classify_stream')
    def test_classify_returns_result(self, mock_classify_stream):
        """Test returns results + status 200 when classify is successful."""
        mock_classify_stream.return_value = {'cs.DL': 0.375}
        expected_data = b'{"cs.DL":0.375}\n'

        response = self.client.post('/classify', data=b"mockcontent")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_classify_empty_fails(self):
        """Test returns invalid length when content is empty."""
        response = self.client.post('/classify', data=b"", headers={'Content-Type': "text/plain"})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, b'{"message":"Body empty or content-length not set"}\n')