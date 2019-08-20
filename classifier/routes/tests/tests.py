"""Tests for :mod:`controllers`."""

from unittest import TestCase, mock

from classifier.routes import service_status

class TestHealthCheck(TestCase):
    """Tests for :func:`.health_check`."""

    @mock.patch('classifier.routes.health_check')
    def test_serv_returns_result(self, mock_health_check):
        """Test returns 'OK' + status 200 when classify returns results."""
        mock_health_check.return_value = dict(metadata={}, results=[dict(results=['cs.DL'])])
