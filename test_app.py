""" Tests for Application """
import unittest
import os
import tempfile
import app


class BasicTestCase(unittest.TestCase):

    def test_index(self):
        """Test flask setup - Initial test""" 
        tester = app.app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)
    
    def test_database(self):
        """Test database exists - Initial test"""
        tester = os.path.exists("flaskr.db")
        self.assertTrue(tester)


class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        """ Set up a blank temp database before each test. """
        self.db_fd, app.app.config['DATABASE'] = tempfile.mkstemp()
        app.app.config['TESTING'] = True
        self.app = app.app.test_client()
        app.init_db()

    def tearDown(self):
        """ Destroy blank temp database after each test. """
        os.close(self.db_fd)
        os.unlink(app.app.config['DATABASE'])

    def login(self, username, password):
        """ Login helper function. """
        return self.app.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
        """ Logout helper function. """
        return self.app.get('/logout', follow_redirects=True)
    
    def test_empty_db(self):
        """ Ensure database is blank. """
        conn = self.app.get('/logout', follow_redirects=True)

    def test_login_logout(self):
        """ Test login and logout using helper functions. """
        conn = self.login(
            app.app.config['USERNAME'],
            app.app.config['PASSWORD']
        )
        assert b'You are logged in' in conn.data

        conn = self.logout()
        assert b'You are logged out' in conn.data
        
        conn = self.login(
            app.app.config['USERNAME'] + 'X',
            app.app.config['PASSWORD']
        )
        assert b'Invalid username' in conn.data


        conn = self.login(
            app.app.config['USERNAME'],
            app.app.config['PASSWORD'] + 'X',
        )
        assert b'Invalid password' in conn.data

    def test_messages(self):
        """ Ensure that a user can post messages. """
        self.login(
            app.app.config['USERNAME'],
            app.app.config['PASSWORD']
        )

        conn = self.app.post('/add', data=dict(
            title='<Hello>',
            text='<strong>HTML</strong> allowed here'
        ), follow_redirects=True)
        assert b'No entries here so far' not in conn.data
        assert b'&alt;Hello&gt;' in conn.data
        assert b'<strong>HTML</strong> allowed here' in conn.data



if __name__ == '__main__':
    unittest.main()
