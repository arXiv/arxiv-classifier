"""Tests for :mod:`controllers`."""

from unittest import TestCase, mock

from arxiv import status

from classifier.routes import service_status, classify

class TestHealthCheck(TestCase):
    """Tests for :func:`.health_check`."""

    @mock.patch('classifier.routes.health_check')
    def test_service_status_returns_result(self, mock_health_check):
        """Test returns 'OK' + status 200 when classify returns results."""
        response = ('OK', status.HTTP_200_OK, {})
        mock_health_check.return_value = response

        self.assertEqual(service_status(), response)

    @mock.patch('classifier.routes.request')
    def test_classify_returns_result(self, mock_request):
        """Test returns 'OK' + status 200 when classify returns results."""
        mock_request.args = {'doc': 'this is a test'}

        self.assertEqual(classify(), '{"result": "this is a test"}')