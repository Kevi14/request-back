from app import app, db
from app.models.request import HttpRequest
import unittest
import json
import logging 

# Configure the logger for the app
app.logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s')
handler.setFormatter(formatter)
app.logger.addHandler(handler)

class TestFlaskApp(unittest.TestCase):

    def setUp(self):
        app.logger.info("Setting up test environment...")

        # Set up a test client
        self.app = app.test_client()

        # Establish an application context
        self.app_context = app.app_context()
        self.app_context.push()
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        try:
            db.create_all()
        except Exception as e:
            app.logger.error("Error creating database: %s", str(e))
            raise e

    def tearDown(self):
        app.logger.info("Tearing down test environment...")
        
        # Clean up the test database
        db.session.remove()
        db.drop_all()
        
        # Pop the application context
        self.app_context.pop()

    def test_valid_http_get_request(self):
        response = self.app.get('/api/HTTP/GET/?url=https://example.com')
        data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 200)
        self.assertIn('response', data['data'])
        self.assertIn('request', data['data'])

    def test_invalid_http_method_request(self):
        response = self.app.get('/api/HTTP/INVALID_METHOD/?url=https://example.com')
        data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['status'], 400)
        self.assertIn('Unsupported HTTP method', data['errors']['message'])

    def test_missing_url(self):
        response = self.app.get('/api/HTTP/GET/')
        data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['status'], 400)
        self.assertIn('URL is missing', data['errors']['message'])

    def test_database_entry_created(self):
        self.app.get('/api/HTTP/GET/?url=https://example.com')

        # Check if the request is saved in the database
        saved_request = HttpRequest.query.first()
        self.assertIsNotNone(saved_request)
        self.assertEqual(saved_request.method, 'GET')

if __name__ == '__main__':
    unittest.main()
