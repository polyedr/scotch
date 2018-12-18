# test_bucketlist.py

import unittest
import os
import json
from app import create_app, db


class BucketlistTestCase(unittest.TestCase):
    """This class represents the bucketlist test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.bucketlist = {"name": "Go to London for vacations"}

        # Binds the app to the current context
        with self.app.app_context():
            # Create all tables
            db.session.close()
            db.drop_all()
            db.create_all()

    def register_user(self, email="user@test.com", password="test1234password"):
        """This helper method helps log in a test user."""
        user_data = {
            'email': email,
            'password': password
        }    
        return self.client().post('/auth/register', data=user_data)

    def login_user(self, email="user@test.com", password="test1234password"):
        """This helper method helps log ni a test user"""
        user_data = {
            'email': email,
            'password': password
        }
        return self.client().post('/auth/login', data=user_data)

    def test_bucketlist_creation(self):
        """Test API can create a bucketlist (POST request)"""
        # register a test user, then log them in
        self.register_user()
        result = self.login_user()
        # obtain the access token        
        access_token = json.loads(result.data.decode())['access_token']
        
        # ensure the request has an authorization header set with the access token in it
        res = self.client().post('/bucketlists/', headers=dict(Authorization="Bearer " + access_token), data=self.bucketlist)
        self.assertEqual(res.status_code, 201)
        #print(json.loads(res.data)['name'])
        #print(str(res.data))
        self.assertIn('Go to London', str(res.data))
        # self.assertIn('Go to London', str((json.loads(res.data)['name'])))

    def test_api_can_get_all_bucketlists(self):
        """Test API can get a bucketlist (GET request)."""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']
        
        # Create a bucketlist by making a POST request
        res = self.client().post(
            '/bucketlists/', 
            headers=dict(Authorization="Bearer " + access_token),
            data=self.bucketlist)
        self.assertEqual(res.status_code, 201)
        res = self.client().get(
            '/bucketlists/', 
            headers=dict(Authorization="Bearer " + access_token)
            )
        self.assertEqual(res.status_code, 200)
        self.assertIn('Go to London', str(res.data))

    def test_api_can_get_bucketlist_by_id(self):
        """Test API can get a single bucketlist by using it's id."""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']
        
        rv = self.client().post(
            '/bucketlists/', 
            headers=dict(Authorization="Bearer " + access_token),
            data=self.bucketlist)
        # assert that the bucketlist is created 
        self.assertEqual(rv.status_code, 201)
        # get the response data in json format
        results = json.loads(rv.data.decode())
        

        result = self.client().get('/bucketlists/{}'.format(results['id']), headers=dict(Authorization="Bearer " + access_token))
        # print(result)
        self.assertEqual(result.status_code, 200)
        self.assertIn('Go to London', str(result.data))

    def test_bucketlist_can_be_edited(self):
        """Test API can edit an existing bucketlist. (PUT request)"""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']
        
        # first, we create a bucketlist by making a POST request
        rv = self.client().post(
            '/bucketlists/', 
            headers=dict(Authorization="Bearer " + access_token),
            data={'name': 'Eat, pray and love'})        
        self.assertEqual(rv.status_code, 201)
        string = "Don't just eat, but also pray and love"
        
        # get the json with the bucketlist
        results = json.loads(rv.data.decode())
        
        # then, we edit the created bucketlist by making a PUT request
        rv = self.client().put(
            '/bucketlists/{}'.format(results['id']), 
            headers=dict(Authorization="Bearer " + access_token),
            data={'name': string})        
        self.assertEqual(rv.status_code, 200)
        
        # finally, we get the edited bucketlist to see if it is actually edited.        
        results = self.client().get(
            '/bucketlists/{}'.format(results['id']),
            headers=dict(Authorization="Bearer " + access_token))
        #results.data.replace("'", "")
        #print(str((json.loads(results.data)['name'])).replace("'", ""))
        self.assertIn("Dont just eat", str((json.loads(results.data)['name'])).replace("'", ""))

    def test_bucketlist_deletion(self):
        """Test API can delete an existing bucketlist. (DELETE request)"""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']
        
        rv = self.client().post(
            '/bucketlists/',
            headers=dict(Authorization="Bearer " + access_token),
            data={'name': 'Eat, pray and love'})
        self.assertEqual(rv.status_code, 201)
        # get the bucketlist in json        
        results = json.loads(rv.data.decode())
        
        # delete the bucketlist we just created        
        res = self.client().delete(
            '/bucketlists/{}'.format(results['id']),
            headers=dict(Authorization="Bearer " + access_token),)
        self.assertEqual(res.status_code, 200)
        # Test to see if it exists, should return a 404
        result = self.client().get(
            '/bucketlists/1',
            headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(result.status_code, 404)

    def tearDown(self):
        """teardown all initialized variables"""
        with self.app.app_context():
            # Drop all tables
            db.session.remove()
            db.drop_all()


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
