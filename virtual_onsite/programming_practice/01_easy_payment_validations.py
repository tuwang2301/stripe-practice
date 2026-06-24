"""
STRIPE PROGRAMMING PRACTICE 01: CSV Payment Validator (EASY)
============================================================

PROBLEM DESCRIPTION:
Stripe processes transaction logs submitted by merchants. Before processing, we must validate each record.
You are given a list of raw transaction logs as strings, and a set of registered merchant IDs.

Each transaction string is formatted as:
"transaction_id,merchant_id,amount,currency"

Your task is to:
1. Parse each transaction record.
2. Validate each record based on these rules:
   - The transaction amount must be strictly greater than 0. If not, mark as "INVALID_AMOUNT".
   - The merchant_id must be in the set of registered merchants. If not, mark as "UNREGISTERED_MERCHANT".
   - The currency must be one of the supported currencies: {"USD", "EUR", "GBP"}. If not, mark as "UNSUPPORTED_CURRENCY".
3. If a record has multiple errors, prioritize the reason in this order: 
   UNREGISTERED_MERCHANT > INVALID_AMOUNT > UNSUPPORTED_CURRENCY.
4. Output a list of formatted strings representing invalid transactions only:
   "transaction_id,ERROR_REASON"
   sorted lexicographically by transaction_id.

INPUT FORMAT:
- `transactions`: list of strings
- `registered_merchants`: set of strings

EXAMPLE:
transactions = [
    "tx_1,acct_1,100,USD",
    "tx_2,acct_99,500,EUR",
    "tx_3,acct_1,-10,GBP",
    "tx_4,acct_2,200,JPY"
]
registered_merchants = {"acct_1", "acct_2"}

Output:
[
    "tx_2,UNREGISTERED_MERCHANT",
    "tx_3,INVALID_AMOUNT",
    "tx_4,UNSUPPORTED_CURRENCY"
]
"""

def validate_transactions(transactions, registered_merchants):
    # Parse each transaction record to a dictionary with named fields
    parsed_transactions = []
    for record in transactions:
        transaction_id, merchant_id, amount_str, currency = record.split(",")
        parsed_transactions.append({
            "transaction_id": transaction_id,
            "merchant_id": merchant_id,
            "amount": float(amount_str),
            "currency": currency,
        })

    supported_currencies = {"USD", "EUR", "GBP"}
    invalid_results = []

    for txn in parsed_transactions:
        transaction_id = txn["transaction_id"]
        merchant_id = txn["merchant_id"]
        amount = txn["amount"]
        currency = txn["currency"]

        if merchant_id not in registered_merchants:
            invalid_results.append(f"{transaction_id},UNREGISTERED_MERCHANT")
            continue
        if amount <= 0:
            invalid_results.append(f"{transaction_id},INVALID_AMOUNT")
            continue
        if currency not in supported_currencies:
            invalid_results.append(f"{transaction_id},UNSUPPORTED_CURRENCY")

    return sorted(invalid_results)



# ===================================================================
# TEST SUITE (Run this file to verify your solution)
# ===================================================================
if __name__ == "__main__":
    transactions = [
        "tx_1,acct_1,100,USD",
        "tx_2,acct_99,500,EUR", # unregistered
        "tx_3,acct_1,-10,GBP",  # invalid amount
        "tx_4,acct_2,200,JPY",  # unsupported currency
        "tx_5,acct_99,-50,JPY"  # unregistered and invalid amount and unsupported -> unregistered wins
    ]
    registered_merchants = {"acct_1", "acct_2"}
    
    expected = [
        "tx_2,UNREGISTERED_MERCHANT",
        "tx_3,INVALID_AMOUNT",
        "tx_4,UNSUPPORTED_CURRENCY",
        "tx_5,UNREGISTERED_MERCHANT"
    ]
    
    result = validate_transactions(transactions, registered_merchants)
    print("Your output:", result)
    if result == expected:
        print("SUCCESS: Programming Problem 01 Passed!")
    else:
        print("FAIL: Expected", expected, "but got", result)
