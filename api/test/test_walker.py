import unittest
from faker import Faker
import azure.functions as func
import json
from walker import main

fake = Faker('en_GB')

class TestWalkerFunction(unittest.TestCase):
    def test_add_walker_success(self):
        # Generate test data
        data = {
            'forename': fake.first_name(),
            'surname': fake.last_name(),
            'experienceStartDate': fake.date(pattern="%Y-%m-%d"),
            'aboutMe': fake.text(),
            'email': fake.email(),
            'city': 'Winchester',
            'postCode': fake.postcode()
        }
        body = json.dumps(data)

        # Create a mock HTTP request
        req = func.HttpRequest(
            method='POST',
            url='/api/walker',
            body=body.encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )

        # Call the function
        resp = main(req)

        # Check the response
        self.assertEqual(resp.status_code, 200)
        self.assertIn(data['forename'], resp.get_body().decode())

if __name__ == '__main__':
    unittest.main()