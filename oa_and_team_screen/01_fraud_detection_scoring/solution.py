from collections import defaultdict

def fraudDetectionScoring(transactions_list, rules_list, merchants_list):
    # Parsing input
    merchants = defaultdict(int)
    for merchant in merchants_list:
        merchant_id, base_score = merchant.split(',')
        merchants[merchant_id] = int(base_score)

    transactions = []
    for transaction, rule in zip(transactions_list, rules_list):
        merchant_id, amount, customer_id, hour = transaction.split(',')
        min_transaction_amount, multiplicative_factor, additive_factor, penalty = rule.split(',')

        transactions.append(
            {
                "merchant_id": merchant_id,
                "amount": int(amount),
                "customer_id": customer_id,
                "hour": int(hour),
                "min_amount": int(min_transaction_amount),
                "multi": int(multiplicative_factor),
                "additive": int(additive_factor),
                "penalty": int(penalty),
            }
        )

    # Pass 1: Check amount -> multiply score
    for transaction in transactions:
        mid = transaction["merchant_id"]
        if mid not in merchants:
            continue
        if transaction["amount"] > transaction["min_amount"]:
            merchants[mid] *= transaction["multi"]
    
    # Pass 2: Check count (customer_id, merchant_id) >= 3 => add score
    customer_merchant_count = defaultdict(int)
    for transaction in transactions:
        key = (transaction["customer_id"], transaction["merchant_id"])
        customer_merchant_count[key] += 1

    for transaction in transactions:
        key = (transaction["customer_id"], transaction["merchant_id"])
        mid = transaction["merchant_id"]
        if mid not in merchants:
            continue
        if customer_merchant_count[key] >= 3:
            merchants[mid] += transaction["additive"]

    # Pass 3: Check count (customer_id, merchant_id, hour) >= 3 => apply penalty
    customer_merchant_hour_count = defaultdict(int)
    for transaction in transactions:
        key = (transaction["customer_id"], transaction["merchant_id"], transaction["hour"])
        customer_merchant_hour_count[key] += 1

    for transaction in transactions:
        key = (transaction["customer_id"], transaction["merchant_id"], transaction["hour"])
        mid = transaction["merchant_id"]
        if mid not in merchants:
            continue
        if customer_merchant_hour_count[key] >= 3:
            hour = transaction["hour"]
            if 12 <= hour <= 17:
                merchants[mid] += transaction["penalty"]
            elif 9 <= hour <= 11 or 18 <= hour <= 21:
                merchants[mid] -= transaction["penalty"]

    return [f'{k},{merchants[k]}' for k in sorted(merchants)]
