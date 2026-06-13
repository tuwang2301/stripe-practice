from collections import defaultdict
import math

def merchantLoyaltyScore(transactions_list, merchants_list):
    # Parsing
    transactions = []
    for tran in transactions_list:
        merchant_id,customer_id,amount,category = tran.split(',')
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

    # Pass 1
    for tran in transactions:
        if tran["amount"] > 500:
            merchants[tran["merchant_id"]] *= 1.5

    
    # Pass 2
    customer_merchant_count = defaultdict(int)
    for tran in transactions:
        key = (tran["customer_id"], tran["merchant_id"])

        customer_merchant_count[key] += 1

        if customer_merchant_count[key] >= 2:
            merchants[tran["merchant_id"]] += 50

    # Pass 3
    for tran in transactions:
        if tran["category"] == "electronics":
            merchants[tran["merchant_id"]] += 20
        elif tran["category"] == "food":
            merchants[tran["merchant_id"]] -= 10

    # Output
    return [f"{merchant_id},{math.floor(merchants[merchant_id])}" for merchant_id in sorted(merchants)]


if __name__ == "__main__":
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
    result = merchantLoyaltyScore(transactions_list=transactions_list, merchants_list=merchants_list)
    print(result)
