# test_app.py
import unittest
import sys
import os
from unittest.mock import patch, MagicMock

# Add app to path
sys.path.insert(0, os.path.abspath('.'))

with patch('psycopg2.connect'):
    from app import app

class TestKioskApp(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

    @patch('app.get_db_connection')
    def test_home_page(self, mock_get_db_connection):
        # Mock the database connection and cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db_connection.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = [1]
        
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Hello from Kiosk!', response.data)

    @patch('app.get_db_connection')
    def test_health_endpoint(self, mock_get_db_connection):
        # Mock the database connection
        mock_conn = MagicMock()
        mock_get_db_connection.return_value = mock_conn
        
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'status', response.data)

if __name__ == '__main__':
    unittest.main()