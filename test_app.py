from app import app
import unittest


class BasicTestCase(unittest.TestCase):

    def test_index(self):
        """Test index route.""" 
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
