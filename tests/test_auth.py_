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
        """Test if user cannot be registered twice."""
        res = self.client().post('/auth/register', data=self.user_data)
        self.assertEqual(res.status_code, 201)
        second_res = self.client().post('/auth/register', data=self.user_data)
        self.assertEqual(second_res.status_code, 202)
        result = json.loads(second_res.data.decode())
        self.assertEqual(result['message'], "User already exists. Please login")

    def test_user_login(self):
        """Test if registered user can login"""
        res = self.client().post('/auth/register', data=self.user_data)
        self.assertEqual(res.status_code, 201)
        login_res = self.client().post('/auth/login', data=self.user_data) # <APIResponse 58 bytes [500 INTERNAL SERVER ERROR]>

        # get the results in json format
        #result = json.loads(login_res.data.decode())
        result = json.loads(login_res.data)
        # Test that the response contains success message
        print("login_res=", login_res)             
        print("login_res.data=", login_res.data)        
        print("result=", result)        
        print("result['message']=", result['message'])
        #print()
        self.assertEqual(result['message'], 'You logged in successfully.')
        # Assert that the status code is equal to 200
        self.assertEqual(login_res.status_code, 200)
        self.assertTrue(result['access_token'])

    def test_non_registered_user_login(self):
        """Test non registered users cannot login"""
        # define a dictionary to represent an unregistered user
        not_a_user = {
            'email': 'not_a_user@example.com',
            'password': 'nopassword'
        }
        # send a POST request to /auth/login with the data above
        res = self.client().post('/auth/login', data=not_a_user)
        # get the result in json
        result = json.loads(res.data.decode())
        print("result=", result)
        # assert that this response must contain an error message
        # and an error status code 401(Unauthorized)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(
            result['message'], "Invalid email or password, Please try again")
