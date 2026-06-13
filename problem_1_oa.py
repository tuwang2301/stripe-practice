from collections import defaultdict

def fraudDetectionScoring(transactions_list, rules_list, merchants_list):
    # Parsing input
    merchants = defaultdict(int)
    for merchant in merchants_list:
        merchant_id, base_score = merchant.split(',')
        merchants[merchant_id] = int(base_score)

    transactions = []
    for transaction, rule in zip(transactions_list, rules_list):
        merchant_id,amount,customer_id,hour = transaction.split(',')
        min_transaction_amount,multiplicative_factor,additive_factor,penalty = rule.split(',')

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

    # Pass1: Check amount -> multiply score
    for transaction in transactions:
        if transaction["amount"] > transaction["min_amount"]:
            merchants[transaction["merchant_id"]] *= transaction["multi"]
    
    # Pass2: Check count (customer_id, merchant_id) >= 3 => add score
    customer_merchant_count = defaultdict(int)
    for transaction in transactions:
        key = (transaction["customer_id"],transaction["merchant_id"],)
        customer_merchant_count[key] += 1

    for transaction in transactions:
        key = (transaction["customer_id"],transaction["merchant_id"],)
        if customer_merchant_count[key] >= 3:
            merchants[transaction["merchant_id"]] += transaction["additive"]

    # Pass3: Check count (customer_id, merchant_id, hour) >= 3 => Do something
    customer_merchant_hour_count = defaultdict(int)
    for transaction in transactions:
        key = (transaction["customer_id"],transaction["merchant_id"],transaction["hour"])
        customer_merchant_hour_count[key] += 1

    for transaction in transactions:
        key = (transaction["customer_id"],transaction["merchant_id"],transaction["hour"])
        if customer_merchant_hour_count[key] >= 3:
            if 12 <= transaction["hour"] <= 17:
                merchants[transaction["s_id"]] += transaction["penalty"]
            elif 9 <= transaction["hour"] <= 11 or 18 <= transaction["hour"] <= 21:
                merchants[transaction["merchant_id"]] -= transaction["penalty"]

    return [f'{k},{merchants[k]}' for k in sorted(merchants)]


if __name__ == "__main__":
    transactions_list = [
        "merchant1,1200,customer1,10",
        "merchant1,500,customer1,10",
        "merchant2,2400,customer1,15",
        "merchant1,800,customer1,16",
        "merchant1,1000,customer2,17",
        "merchant1,1400,customer1,10",
    ]
    rules_list = [
        "1000,2,8,15",
        "1400,5,3,19",
        "2300,3,17,3",
        "1800,2,9,6",
        "1000,4,8,2",
        "1200,3,11,7"
    ]
    merchants_list = [
        "merchant1,10",
        "merchant2,20",
    ]

    result = fraudDetectionScoring(transactions_list=transactions_list, rules_list=rules_list, merchants_list=merchants_list)
    print(result)
