import unittest
from unittest.mock import MagicMock, patch
from main import viewcount_http

class TestViews(unittest.TestCase):

    def setUp(self):
        # Set up a mock request object
        self.mock_request = MagicMock()
        self.mock_request.method = 'GET'
        self.mock_request.remote_addr = '127.0.0.1'  # Sample IP address for testing

    @patch('main.firestore')
    def test_visit_count_increment(self, mock_firestore):
        # Mock Firestore client and document reference
        mock_db = MagicMock()
        mock_firestore.client.return_value = mock_db
        mock_visits_ref = mock_db.collection.return_value.document.return_value

        # Set initial visit count
        mock_visits_ref.get.return_value.to_dict.return_value = {'views': 5}

        # Call the function with the mock request
        response_text, status_code, headers = viewcount_http(self.mock_request)

        # Check if the visit count was incremented
        mock_visits_ref.set.assert_called_once_with({'views': 6})

        # Check if the response contains the correct visit count
        self.assertEqual(response_text, '6')
        self.assertEqual(status_code, 200)

    @patch('main.firestore')
    def test_document_creation(self, mock_firestore):
        # Mock Firestore client and document reference
        mock_db = MagicMock()
        mock_firestore.client.return_value = mock_db
        mock_visits_ref = mock_db.collection.return_value.document.return_value

        # Set initial visit count
        mock_visits_ref.get.return_value.to_dict.return_value = {'views': 10}

        # Call the function with the mock request
        viewcount_http(self.mock_request)

        # Check if a new document is created with the correct fields
        mock_visits_ref.document.assert_called_once_with('11')
        mock_visits_ref.document.return_value.set.assert_called_once_with({
            'visitID': 11,
            'ip': '127.0.0.1',
            # Add more fields to test here if necessary
        })

if __name__ == '__main__':
    unittest.main()
