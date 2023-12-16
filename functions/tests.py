import unittest
from unittest.mock import MagicMock, patch
from main import viewcount_http

class TestViews(unittest.TestCase):

    @patch('main.firestore')  # Check if this path is accurate
    def test_visit_count_increment(self, mock_firestore):
        mock_document = MagicMock()
        mock_visits_ref = MagicMock()
        mock_visits_ref.document.return_value = mock_document
        mock_firestore.client.return_value.collection.return_value = mock_visits_ref

        # Mocking the request object
        mock_request = MagicMock()
        mock_request.method = 'GET'
        mock_request.remote_addr = '127.0.0.1'

        # Set initial visit count
        mock_document.get.return_value.to_dict.return_value = {'views': 5}

        # Call the function with the mock request
        response_text, status_code, _ = viewcount_http(mock_request)

        # Check if the visit count was incremented
        mock_document.set.assert_called_once_with({'views': 6})

        # Check if the response contains the correct visit count
        self.assertEqual(response_text, '6')
        self.assertEqual(status_code, 200)

    @patch('main.firestore')  # Check if this path is accurate
    def test_document_creation(self, mock_firestore):
        mock_document = MagicMock()
        mock_visits_ref = MagicMock()
        mock_visits_ref.document.return_value = mock_document
        mock_firestore.client.return_value.collection.return_value = mock_visits_ref

        # Mocking the request object
        mock_request = MagicMock()
        mock_request.method = 'GET'
        mock_request.remote_addr = '127.0.0.1'

        # Set initial visit count
        mock_document.get.return_value.to_dict.return_value = {'views': 10}

        # Call the function with the mock request
        viewcount_http(mock_request)

        # Check if a new document is created with the correct fields
        mock_visits_ref.document.assert_called_once()
        mock_document.set.assert_called_once()

if __name__ == '__main__':
    unittest.main()
