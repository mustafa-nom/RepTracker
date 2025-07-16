import unittest
from unittest.mock import patch
from unittest import mock
from app import app
from services import congress_api

class TestActivityRoute(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    @patch('routes.activity.fetch_rep_activity')
    @patch('routes.activity.fetch_reps')
    def test_activity_route_returns_senator_bills(self, mock_fetch_reps, mock_fetch_rep_activity):
        # Mock of fetch_reps
        mock_fetch_reps.return_value = {
            "fields": {
                "congressional_districts": [
                    {
                        "current_legislators": [
                            {
                                "type": "senator",
                                "bio": {"first_name": "Jane", "last_name": "Doe"},
                                "references": {"bioguide_id": "S123"}
                            }
                        ]
                    }
                ]
            }
        }
        # Mock of fetch_rep_activity
        mock_fetch_rep_activity.return_value = {
            "sponsoredLegislation": [
                {"title": "Test Bill"}
            ]
        }
        response = self.client.get('/activity?zip=12345')
        self.assertIn(b"Jane Doe", response.data)
        self.assertIn(b"Test Bill", response.data)
        
    @patch('services.congress_api.requests.get')
    def test_fetch_rep_activity_success(self, mock_get):
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"sponsoredLegislation": ["A", "B"]}
        mock_get.return_value = mock_response

        result = congress_api.fetch_rep_activity('S123')
        self.assertIn("sponsoredLegislation", result)
        self.assertEqual(result["sponsoredLegislation"], ["A", "B"])

if __name__ == "__main__":
    unittest.main()