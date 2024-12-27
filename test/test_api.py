import unittest
import json
from app import app

class TestApi(unittest.TestCase):
    def test_ner_endpoint_given_json_body_returns_200(self):
        """Test if the /ner endpoint returns a 200 status code for valid input."""
        with app.test_client() as client:
            response = client.post('/ner', json={"sentence": "BTS is a Kpop boy band"})
            self.assertEqual(response.status_code, 200)

    def test_ner_endpoint_given_json_body_with_known_entities_returns_entity_result_in_response(self):
        """Test if the /ner endpoint correctly identifies known entities."""
        with app.test_client() as client:
            response = client.post('/ner', json={"sentence": "Kamala Harris"})
            data = json.loads(response.get_data(as_text=True))
            self.assertEqual(data['entities'][0]['ent'], 'Kamala Harris')
            self.assertEqual(data['entities'][0]['label'], 'Person')

if __name__ == "__main__":
    unittest.main()
