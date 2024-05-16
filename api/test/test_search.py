import unittest
import azure.functions as func
from search import main

class TestSearchFunction(unittest.TestCase):
    def test_search_valid_location(self):
        # Create a mock HTTP request
        req = func.HttpRequest(
            method='GET',
            url='/api/search?location=Winchester',
            body=b'',
            params={'location': 'Winchester'}
        )
        
        # Call the function
        resp = main(req)
        
        # Check the output
        self.assertEqual(resp.status_code, 200)
        self.assertIn('Winchester', resp.get_body().decode())

    def test_search_no_location(self):
        # Create a mock HTTP request without a location
        req = req=func.HttpRequest(
            method='GET',
            url='/api/search',
            body=b'',
            params={}
        )
        
        # Call the function
        resp = main(req)
        
        # Check the output
        self.assertEqual(resp.status_code, 400)

if __name__ == '__main__':
    unittest.main()
