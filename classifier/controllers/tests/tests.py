"""Tests for :mod:`controllers`."""

from unittest import TestCase, mock

from werkzeug.exceptions import InternalServerError, ServiceUnavailable

from arxiv import status
from classifier.controllers import health_check


class TestHealthCheck(TestCase):
    """Tests for :func:`.health_check`."""

    @mock.patch('classifier.controllers.classifier')
    def test_classify_is_down(self, mock_classifier):
        """Test returns 'DOWN' + status 503 when classify raises an exception."""
        mock_classifier.classify.side_effect = RuntimeError
        with self.assertRaises(ServiceUnavailable):
            response, status_code, _ = health_check()
        
    @mock.patch('classifier.controllers.classifier')
    def test_classify_returns_no_result(self, mock_classifier):
        """Test returns 'DOWN' + status 500 when classify returns no results."""
        mock_classifier.classify.return_value = dict(metadata={}, results=[])
        with self.assertRaises(InternalServerError):
            response, status_code, _ = health_check()

    @mock.patch('classifier.controllers.classifier')
    def test_classify_returns_result(self, mock_classifier):
        """Test returns 'OK' + status 200 when classify returns results."""
        mock_classifier.classify.return_value = dict(metadata={}, results=[dict(results=['cs.DL'])])
        response, status_code, _ = health_check()
        self.assertEqual(response, 'OK', "Response content should be OK")
        self.assertEqual(status_code, status.HTTP_200_OK,
                         "Should return 200 status code.")
