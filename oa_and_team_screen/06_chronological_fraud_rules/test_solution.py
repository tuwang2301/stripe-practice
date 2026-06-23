import unittest
from solution import process_authorizations

class TestChronologicalFraudRules(unittest.TestCase):
    def test_sample_case_1(self):
        requests = [
            {"time": 5, "unique_id": "A1", "amount": 120, "card_number": "4111", "merchant": "X"},
            {"time": 1, "unique_id": "A0", "amount": 300, "card_number": "5555", "merchant": "Y"},
            {"time": 5, "unique_id": "A2", "amount": 120, "card_number": "4111", "merchant": "Z"}
        ]
        rules = []
        expected = [
            "1 A0 300 APPROVE",
            "5 A1 120 APPROVE",
            "5 A2 120 APPROVE"
        ]
        self.assertEqual(process_authorizations(requests, rules), expected)

    def test_sample_case_2(self):
        requests = [
            {"time": 5, "unique_id": "A1", "amount": 120, "card_number": "4111", "merchant": "X"},
            {"time": 1, "unique_id": "A0", "amount": 300, "card_number": "5555", "merchant": "Y"},
            {"time": 5, "unique_id": "A2", "amount": 120, "card_number": "4111", "merchant": "Z"}
        ]
        rules = [
            {"time": 3, "field": "card_number", "value": "4111"},
            {"time": 5, "field": "merchant", "value": "Y"},
            {"time": 5, "field": "amount", "value": "120"}
        ]
        expected = [
            "1 A0 300 APPROVE",
            "5 A1 120 REJECT",
            "5 A2 120 REJECT"
        ]
        self.assertEqual(process_authorizations(requests, rules), expected)

if __name__ == '__main__':
    unittest.main()
