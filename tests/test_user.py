import unittest
# If your app is instantiated directly in app.py like `app = Flask(__name__)`
from app import app as create_app


class UserTests(unittest.TestCase):
    def setUp(self):
        """Set up a test client."""
        self.app = create_app({'TESTING': True}).test_client()

    def test_successful_login(self):
        """Test successful login."""
        response = self.app.post('/login', data={'email': 'admin@example.com', 'password': 'secure'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login successful', response.data)

    def test_failed_login(self):
        """Test failed login with wrong credentials."""
        response = self.app.post('/login', data={'email': 'admin@example.com', 'password': 'wrong'})
        self.assertEqual(response.status_code, 401)
        self.assertIn(b'Login Failed', response.data)

    def test_signup(self):
        """Test user signup."""
        response = self.app.post('/signup', data={'email': 'newuser@example.com', 'password': 'newpass', 'confirm_password': 'newpass'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Account created successfully', response.data)

if __name__ == '__main__':
    unittest.main()
