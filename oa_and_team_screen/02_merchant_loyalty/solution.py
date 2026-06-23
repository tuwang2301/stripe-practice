from collections import defaultdict
import math

def merchantLoyaltyScore(transactions_list, merchants_list):
    # Parsing
    transactions = []
    for tran in transactions_list:
        merchant_id, customer_id, amount, category = tran.split(',')
        transactions.append(
            {
                "merchant_id": merchant_id,
                "customer_id": customer_id,
                "amount": int(amount),
                "category": category
            }
        )

    merchants = defaultdict(float)
    for merch in merchants_list:
        merchant_id, base_points = merch.split(',')
        merchants[merchant_id] = float(base_points)

    # Pass 1: Amount multiplier
    for tran in transactions:
        mid = tran["merchant_id"]
        if mid not in merchants:
            continue
        if tran["amount"] > 500:
            merchants[mid] *= 1.5

    # Pass 2: Repeat customer bonus
    customer_merchant_count = defaultdict(int)
    for tran in transactions:
        key = (tran["customer_id"], tran["merchant_id"])
        customer_merchant_count[key] += 1
        mid = tran["merchant_id"]
        if mid not in merchants:
            continue
        if customer_merchant_count[key] >= 2:
            merchants[mid] += 50

    # Pass 3: Category adjustments
    for tran in transactions:
        mid = tran["merchant_id"]
        if mid not in merchants:
            continue
        if tran["category"] == "electronics":
            merchants[mid] += 20
        elif tran["category"] == "food":
            merchants[mid] -= 10

    # Output
    return [f"{merchant_id},{math.floor(merchants[merchant_id])}" for merchant_id in sorted(merchants)]
