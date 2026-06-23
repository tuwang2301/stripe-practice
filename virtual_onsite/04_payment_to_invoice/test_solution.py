import unittest
from solution import match_payment

class TestPaymentToInvoice(unittest.TestCase):
    def setUp(self):
        self.invoices = [
            "invoice-id-1, 10000, 2022-01-01",
            "invoice-id-2, 30000, 2022-01-02",
            "invoice-id-3, 30000, 2022-01-01", # Same amount as id-2 but earlier date
            "invoice-id-4, 30500, 2022-01-03"
        ]

    def test_explicit_match(self):
        payment = "payment-id-1, 30000, paying for: invoice-id-1"
        expected = "payment-id-1 paid 30000 amount for invoice invoice-id-1 on date 2022-01-01"
        self.assertEqual(match_payment(self.invoices, payment), expected)

    def test_explicit_match_not_found(self):
        payment = "payment-id-1, 30000, paying for: invoice-id-999"
        expected = "no match found"
        self.assertEqual(match_payment(self.invoices, payment), expected)

    def test_exact_amount_match_with_tiebreak(self):
        payment = "payment-id-2, 30000"
        # Matches invoice-id-3 because it has earlier date (2022-01-01) than invoice-id-2 (2022-01-02)
        expected = "payment-id-2 paid 30000 amount for invoice invoice-id-3 on date 2022-01-01"
        self.assertEqual(match_payment(self.invoices, payment), expected)

    def test_forgiveness_match(self):
        payment = "payment-id-3, 30100"
        # invoice-id-2: 30000 (diff 100)
        # invoice-id-3: 30000 (diff 100)
        # invoice-id-4: 30500 (diff 400)
        # With forgiveness = 200, matches invoice-id-2 or invoice-id-3.
        # invoice-id-3 is earlier.
        expected = "payment-id-3 paid 30100 amount for invoice invoice-id-3 on date 2022-01-01; forgave 100"
        self.assertEqual(match_payment(self.invoices, payment, forgiveness=200), expected)

    def test_forgiveness_match_boundary(self):
        payment = "payment-id-3, 30100"
        # With forgiveness = 50, diff of 100 is too large. No match.
        expected = "no match found"
        self.assertEqual(match_payment(self.invoices, payment, forgiveness=50), expected)

if __name__ == '__main__':
    unittest.main()
