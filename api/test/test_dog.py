import unittest
from faker import Faker
import azure.functions as func
import json
from dog import main

fake = Faker('en_GB')

class TestDogFunction(unittest.TestCase):
    def test_add_dog_success(self):
        # Generate test data
        data = {
            'petName': fake.first_name(),
            'dateOfBirth': fake.date_of_birth(minimum_age=0, maximum_age=15).strftime("%Y-%m-%d"),
            'breed': fake.word(ext_word_list=['Golden Retriever', 'Labrador', 'Poodle']),
            'ownerName': fake.name(),
            'ownerEmail': fake.email()
        
        }
        body = json.dumps(data)

        # Create a mock HTTP request
        req = func.HttpRequest(
            method='POST',
            url='/api/dog',
            body=body.encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )

        # Call the function
        resp = main(req)

        # Check the response
        self.assertEqual(resp.status_code, 200)
        self.assertIn(data['petName'], resp.get_body().decode())

if __name__ == '__main__':
    unittest.main()
