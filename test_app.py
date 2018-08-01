""" Tests for Application """
import unittest
import os
from app import app


class BasicTestCase(unittest.TestCase):

    def test_index(self):
        """Test flask setup - Initial test""" 
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 404)
    
    def test_database(self):
        """Test database exists - Initial test"""
        tester = os.path.exists("flaskr.db")
        self.assertTrue(tester)


if __name__ == '__main__':
    unittest.main()
