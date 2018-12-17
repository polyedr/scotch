# /tests/test_auth.py

import unittest
import json
from app import create_app, db


class AuthTestCase(unittest.TestCase):
    """Test case for the authentication blueprint"""

    def setUp(self):
        """Set up test variables"""
        self.app = create_app(config_name="testing")
        # Initialization of the test_client
        self.client = self.app.test_client
        # This is the user test json data 
        self.user_data = {
            'email': 'test@example.com',        
            'password': 'test_password'    
        }

        with self.app.app_context():
            # create all tables
            db.session.close()
            db.drop_all()
            db.create_all()

    def test_registration(self):
        """Test user registration works"""
        res = self.client().post('/auth/register', data=self.user_data)
        # Get the results returned in json format
        result = json.loads(res.data.decode())
        # Assert the request with the message and 201 status
        self.assertIn("You have registered successfully", result['message'])
        self.assertEqual(res.status_code, 201)

    def test_already_registered_user(self):
        """Test that a user cannot be registered twice"""
        res = self.client().post('/auth/register', data=self.user_data)
        result = json.loads(res.data.decode())
        # assert that the request contains a success message and a 201 status code
        self.assertIn("You have registered successfully", result['message'])
        self.assertEqual(res.status_code, 201)

    def test_already_registered_user(self):
        """Test that a user cannot be registered twice."""
        res = self.client().post('/auth/register', data=self.user_data)
        self.assertEqual(res.status_code, 201)
        second_res = self.client().post('/auth/register', data=self.user_data)
        self.assertEqual(second_res.status_code, 202) 
        result = json.loads(second_res.data.decode())
        self.assertEqual(
            result['message'], "User already exists. Please login")












