import unittest
from solution import calculate_fees

class TestTransactionFees(unittest.TestCase):
    def test_sample_case_1(self):
        transactions = [
            "id, reference, amount, currency, date, merchant_id,buyer_country, transaction_type, payment_provider, status",
            "py_1,1,1000, eur, 2024-12-24, acct_1, ie, payment, card, payment_completed",
            "py_2, 2, 2500, eur, 2024-12-24,acct_2,ie, payment, card, payment_failed",
            "py_3,3,3400, eur, 2024-12-25, acct_2, ie, payment, klarna, payment_completed"
        ]
        expected = [
            "py_1,payment,card,51",
            "py_2,payment,card,0",
            "py_3,payment,klarna,101"
        ]
        self.assertEqual(calculate_fees(transactions), expected)

    def test_sample_case_2(self):
        transactions = [
            "du_1, py_3, 1000, eur, 2025-01-01,acct_2,ie, dispute, klarna, dispute_won",
            "du_2, py_3,1000, eur, 2025-01-01,acct_2,ie, dispute, klarna, dispute_lost",
            "du_3, py_1, 1000, eur, 2025-01-01,acct_1,ie,dispute,card, dispute_won",
            "du_4, py_2, 2500, eur, 2025-01-01,acct_2,ie,dispute,card, dispute_lost"
        ]
        expected = [
            "du_1,dispute,klarna,0",
            "du_2,dispute,klarna,15",
            "du_3,dispute,card,15",
            "du_4,dispute,card,15"
        ]
        self.assertEqual(calculate_fees(transactions), expected)

if __name__ == '__main__':
    unittest.main()
