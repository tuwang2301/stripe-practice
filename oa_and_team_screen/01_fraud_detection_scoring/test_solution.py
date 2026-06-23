import unittest
from solution import fraudDetectionScoring

class TestFraudDetectionScoring(unittest.TestCase):
    def test_sample_case(self):
        transactions_list = [
            "merchant1,1200,customer1,10",
            "merchant1,500,customer1,10",
            "merchant2,2400,customer1,15",
            "merchant1,800,customer1,16",
            "merchant1,1000,customer2,17",
            "merchant1,1400,customer1,10",
        ]
        rules_list = [
            "1000,2,8,15",
            "1400,5,3,19",
            "2300,3,17,3",
            "1800,2,9,6",
            "1000,4,8,2",
            "1200,3,11,7"
        ]
        merchants_list = [
            "merchant1,10",
            "merchant2,20",
        ]
        expected = [
            "merchant1,50",
            "merchant2,60"
        ]
        self.assertEqual(fraudDetectionScoring(transactions_list, rules_list, merchants_list), expected)

    def test_no_transactions(self):
        transactions_list = []
        rules_list = []
        merchants_list = [
            "merchant1,10",
            "merchant2,20",
        ]
        expected = [
            "merchant1,10",
            "merchant2,20"
        ]
        self.assertEqual(fraudDetectionScoring(transactions_list, rules_list, merchants_list), expected)

    def test_amount_exactly_threshold(self):
        transactions_list = ["merchant1,1000,customer1,10"]
        rules_list = ["1000,2,8,15"]
        merchants_list = ["merchant1,10"]
        # 1000 is not strictly greater than 1000, so score remains 10
        expected = ["merchant1,10"]
        self.assertEqual(fraudDetectionScoring(transactions_list, rules_list, merchants_list), expected)

if __name__ == '__main__':
    unittest.main()
