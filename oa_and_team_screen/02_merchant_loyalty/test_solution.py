import unittest
from solution import merchantLoyaltyScore

class TestMerchantLoyaltyScore(unittest.TestCase):
    def test_sample_case(self):
        transactions_list = [
            "m1,c1,500,food",
            "m1,c1,499,food",
            "m3,c2,501,electronics",
            "m2,c1,500,food",
            "m3,c1,500,food",
            "m2,c2,500,electronics",
        ]
        merchants_list = [
            "m1,13",
            "m2,2.5",
            "m3,10.5"
        ]
        # Trace:
        # m1 base=13:
        # Pass 1: no amount > 500
        # Pass 2: c1 buy from m1 twice (tx0 and tx1) -> +50. score = 13 + 50 = 63.
        # Pass 3: tx0 category food (-10), tx1 category food (-10) -> score = 63 - 20 = 43.
        # m2 base=2.5:
        # Pass 1: no amount > 500
        # Pass 2: c1 count 1, c2 count 1 -> no bonus
        # Pass 3: tx3 food (-10), tx5 electronics (+20) -> score = 2.5 - 10 + 20 = 12.5. floor is 12.
        # m3 base=10.5:
        # Pass 1: tx2 (501) > 500 -> 10.5 * 1.5 = 15.75
        # Pass 2: c2 count 1, c1 count 1 -> no bonus
        # Pass 3: tx2 electronics (+20), tx4 food (-10) -> score = 15.75 + 20 - 10 = 25.75. floor is 25.
        expected = [
            "m1,43",
            "m2,12",
            "m3,25"
        ]
        self.assertEqual(merchantLoyaltyScore(transactions_list, merchants_list), expected)

if __name__ == '__main__':
    unittest.main()
