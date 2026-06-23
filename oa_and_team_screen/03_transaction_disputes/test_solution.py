import unittest
from solution import transactionDisputeSystem

class TestTransactionDisputeSystem(unittest.TestCase):
    def test_sample_case(self):
        transactions_list = [
            "tx1,M1,C1,50,100",
            "tx2,M1,C1,50,145",   # same (C1,M1,50), |145-100|=45 -> DUPLICATE
            "tx3,M1,C1,50,210",   # same (C1,M1,50), |210-145|=65 > 60 -> NOT dup of tx2, |210-100|=110 -> NOT dup of tx1
            "tx4,M2,C2,200,300",  # FRAUD
            "tx5,M2,C2,900,400",  # ERROR, contributes to disputed amount
        ]
        disputes_list = [
            "tx1,FRAUD",
            "tx4,FRAUD",
            "tx5,ERROR",
        ]
        merchants_list = [
            "M1,10",
            "M2,5",
        ]
        # Trace:
        # M1 base_risk = 10:
        # Pass 1: tx1 is FRAUD -> risk *= 3 -> 30.
        # Pass 2: tx1 and tx2 are DUPLICATE -> risk += 20 -> 50. (tx3 is not duplicate).
        # Disputes: tx1 is DUPLICATE (originally FRAUD but overwritten), tx2 is DUPLICATE.
        # Total disputed amount for M1: tx1.amount + tx2.amount = 50 + 50 = 100. (Not > 1000, so no Pass 3 penalty).
        # Score M1 = 50.
        #
        # M2 base_risk = 5:
        # Pass 1: tx4 is FRAUD -> risk *= 3 -> 15.
        # Pass 2: no duplicates.
        # Pass 3: disputed amount for M2: tx4 (200) + tx5 (900) = 1100.
        # Since 1100 > 1000 -> risk += 50 -> 65.
        # Score M2 = 65.
        expected = [
            "M1,50",
            "M2,65"
        ]
        self.assertEqual(transactionDisputeSystem(transactions_list, disputes_list, merchants_list), expected)

if __name__ == '__main__':
    unittest.main()
