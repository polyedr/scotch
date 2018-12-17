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
            db.create_all()

    def test_bucketlist_creation(self):
        """Test API can create a bucketlist (POST request)"""
        res = self.client().post('/bucketlists/', data=self.bucketlist)
        self.assertEqual(res.status_code, 201)
        #print(json.loads(res.data)['name'])
        #print(str(res.data))
        self.assertIn('Go to London', str(res.data))
        # self.assertIn('Go to London', str((json.loads(res.data)['name'])))

    def test_api_can_get_all_bucketlists(self):
        """Test API can get a bucketlist (GET request)."""
        res = self.client().post('/bucketlists/', data=self.bucketlist)
        self.assertEqual(res.status_code, 201)
        res = self.client().get('/bucketlists/')
        self.assertEqual(res.status_code, 200)
        self.assertIn('Go to London', str(res.data))

    def test_api_can_get_bucketlist_by_id(self):
        """Test API can get a single bucketlist by using it's id."""
        rv = self.client().post('/bucketlists/', data=self.bucketlist)
        self.assertEqual(rv.status_code, 201)
        result_in_json = json.loads(rv.data.decode('utf-8').replace("'", "\""))
        print("result_in_json['id'] =", result_in_json['id'])
        # result = self.client().get('/bucketlists/1')
        result = self.client().get('/bucketlists/{}'.format(result_in_json['id']))
        # print(result)
        self.assertEqual(result.status_code, 200)
        self.assertIn('Go to London', str(result.data))

    def test_bucketlist_can_be_edited(self):
        """Test API can edit an existing bucketlist. (PUT request)"""
        rv = self.client().post(
            '/bucketlists/',
            data={'name': 'Eat, pray and love'})        
        self.assertEqual(rv.status_code, 201)
        string = "Don't just eat, but also pray and love"
        
        #print(string.replace("'", ""))
        rv = self.client().put(
            '/bucketlists/1',
            data={
                "name": string.replace("'", "")
            })
        self.assertEqual(rv.status_code, 200)
        results = self.client().get('/bucketlists/1')
        #results.data.replace("'", "")
        print(str((json.loads(results.data)['name'])).replace("'", ""))
        self.assertIn("Dont just eat", str((json.loads(results.data)['name'])).replace("'", ""))

    def test_bucketlist_deletion(self):
        """Test API can delete an existing bucketlist. (DELETE request)"""
        rv = self.client().post(
            '/bucketlists/',
            data={'name': 'Eat, pray and love'})
        self.assertEqual(rv.status_code, 201)
        res = self.client().delete('/bucketlists/1')
        self.assertEqual(res.status_code, 200)
        # Test to see if it exists, should return a 404
        result = self.client().get('/bucketlists/1')
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
