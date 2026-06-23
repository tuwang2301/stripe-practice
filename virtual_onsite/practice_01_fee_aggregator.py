"""
STRIPE PRACTICE PROBLEM 01: CSV Fee Calculator and Aggregator (EASY)
===================================================================

PROBLEM DESCRIPTION:
Stripe processes millions of transactions every day. Each transaction has a fee based on its status and type. 
You are given a list of transactions in CSV format. Each line represents a transaction:
`id, amount, currency, transaction_type, payment_provider, status, merchant_id`

Your task is to:
1. Parse the CSV transaction records.
2. For each transaction, calculate the fee based on the following rules:
   - Status 'payment_completed': fee is 2% of the amount + 30 cents (floored to nearest integer cent).
   - Status 'dispute_lost': fee is a flat 15 cents.
   - Status 'dispute_won': fee is 15 cents for 'card' payments, and 0 for 'klarna' payments.
   - For all other statuses, the fee is 0.
3. Aggregate the total fees collected for each merchant.
4. Return a list of strings formatted as "merchant_id,total_fees" sorted lexicographically by merchant_id.

INPUT FORMAT:
A list of CSV lines (with a header in the first line).
Example:
[
    "id,amount,currency,transaction_type,payment_provider,status,merchant_id",
    "py_1,1000,usd,payment,card,payment_completed,acct_1",
    "py_2,2500,usd,payment,card,payment_failed,acct_2",
    "py_3,3400,usd,payment,klarna,payment_completed,acct_2"
]

OUTPUT FORMAT:
A list of strings sorted lexicographically by merchant_id:
[
    "acct_1,50",
    "acct_2,98"
]
(Trace: acct_1 fee = 1000 * 0.02 + 30 = 50. acct_2 fee = 0 (failed) + (3400 * 0.02 + 30) = 98).
"""

import math

def calculate_merchant_fees(transactions_csv_list):
    # WRITE YOUR CODE HERE
    pass


# ===================================================================
# TEST SUITE (Run this file to verify your solution)
# ===================================================================
if __name__ == "__main__":
    test_input = [
        "id,amount,currency,transaction_type,payment_provider,status,merchant_id",
        "py_1,1000,usd,payment,card,payment_completed,acct_1",
        "py_2,2500,usd,payment,card,payment_failed,acct_2",
        "py_3,3400,usd,payment,klarna,payment_completed,acct_2",
        "du_1,1000,usd,dispute,klarna,dispute_won,acct_2",
        "du_2,1000,usd,dispute,card,dispute_won,acct_1"
    ]
    
    # Expected results:
    # acct_1: py_1 fee = 50. du_2 fee = 15 (card dispute won). Total = 65.
    # acct_2: py_3 fee = 98. du_1 fee = 0 (klarna dispute won). Total = 98.
    expected = [
        "acct_1,65",
        "acct_2,98"
    ]
    
    result = calculate_merchant_fees(test_input)
    print("Your output:", result)
    if result == expected:
        print("SUCCESS: Practice Problem 01 Passed!")
    else:
        print("FAIL: Expected", expected, "but got", result)
