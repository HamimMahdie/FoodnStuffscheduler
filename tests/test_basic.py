import unittest
# If your app is instantiated directly in app.py like `app = Flask(__name__)`
from app import app as create_app


class BasicTests(unittest.TestCase):
    def setUp(self):
        """Set up a test client."""
        self.app = create_app({'TESTING': True}).test_client()

    def test_home_page(self):
        """Test the home page for correct HTTP response."""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Hello, world!', response.data)

if __name__ == '__main__':
    unittest.main()
