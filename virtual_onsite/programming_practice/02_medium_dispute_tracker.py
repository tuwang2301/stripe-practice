"""
STRIPE PROGRAMMING PRACTICE 02: Stateful Dispute Tracker (MEDIUM)
================================================================

PROBLEM DESCRIPTION:
You are designing a dispute monitoring service for Stripe.
Implement the class `DisputeTracker` that processes transactions and disputes and updates merchant risk scores.

Interface:
1. `__init__(self, merchants_list)`
   - `merchants_list`: a list of strings formatted as `"merchant_id,base_risk"`.

2. `process_transaction(self, tx_id, merchant_id, customer_id, amount)`
   - Records a transaction in the tracker.

3. `process_dispute(self, tx_id, dispute_type)`
   - Processes a dispute for the transaction matching `tx_id`.
   - The `dispute_type` can be `"FRAUD"` or `"ERROR"`.
   - Apply the following rules (in order):
     - **Rule 1 (Fraud Multiplier)**: If the dispute type is `"FRAUD"`, double (`* 2`) the merchant's current risk score.
     - **Rule 2 (Frequent Customer Penalty)**: If the customer of the disputed transaction has made **3 or more** transactions to the same merchant, increase the merchant's risk score by **+10** for each transaction that customer made to the merchant (e.g. if the customer made 4 transactions, add 40 to the risk).

4. `get_merchant_risk(self, merchant_id) -> int`
   - Returns the current risk score of the merchant. If the merchant is not found, return 0.
"""

from collections import defaultdict

class DisputeTracker:
    def __init__(self, merchants_list):
        # WRITE YOUR INITIALIZATION HERE
        pass

    def process_transaction(self, tx_id, merchant_id, customer_id, amount):
        # WRITE YOUR CODE HERE
        pass

    def process_dispute(self, tx_id, dispute_type):
        # WRITE YOUR CODE HERE
        pass

    def get_merchant_risk(self, merchant_id):
        # WRITE YOUR CODE HERE
        pass


# ===================================================================
# TEST SUITE (Run this file to verify your solution)
# ===================================================================
if __name__ == "__main__":
    merchants = ["M1,10", "M2,20"]
    tracker = DisputeTracker(merchants)
    
    # Customer C1 makes 3 transactions to M1
    tracker.process_transaction("tx1", "M1", "C1", 100)
    tracker.process_transaction("tx2", "M1", "C1", 150)
    tracker.process_transaction("tx3", "M1", "C1", 200)
    
    # Customer C2 makes 2 transactions to M1
    tracker.process_transaction("tx4", "M1", "C2", 50)
    tracker.process_transaction("tx5", "M1", "C2", 80)
    
    # Dispute C1's transaction (tx1) as ERROR (Rule 1 does not apply, Rule 2 applies because C1 has 3 transactions)
    # Risk increase: 3 transactions * 10 = +30. M1 risk = 10 + 30 = 40.
    tracker.process_dispute("tx1", "ERROR")
    print("M1 risk after tx1 dispute (expected 40):", tracker.get_merchant_risk("M1"))
    
    # Dispute C2's transaction (tx4) as FRAUD (Rule 1 applies: risk * 2 = 80. Rule 2 does not apply because C2 has only 2 transactions)
    # M1 risk = 40 * 2 = 80.
    tracker.process_dispute("tx4", "FRAUD")
    print("M1 risk after tx4 dispute (expected 80):", tracker.get_merchant_risk("M1"))
    
    # Validate final risk scores
    if tracker.get_merchant_risk("M1") == 80 and tracker.get_merchant_risk("M2") == 20:
        print("SUCCESS: Programming Problem 02 Passed!")
    else:
        print("FAIL: Verification failed.")
