from collections import defaultdict

def transactionDisputeSystem(transactions_list, disputes_list, merchants_list):
    # -- Parsing ---
    transactions = {}
    for transaction in transactions_list:
        tx_id, merchant_id, customer_id, amount, timestamp_minutes = transaction.split(',')
        transactions[tx_id] = {
            "merchant_id": merchant_id,
            "customer_id": customer_id,
            "amount": int(amount),
            "timestamp_minutes": int(timestamp_minutes)
        }

    disputes = {}
    for dispute in disputes_list:
        tx_id, dispute_type = dispute.split(',')
        disputes[tx_id] = dispute_type

    merchants = {}
    for merchant in merchants_list:
        merchant_id, base_risk = merchant.split(',')
        merchants[merchant_id] = int(base_risk)

    # Pass 1: check type 'FRAUD' -> multiply risk by 3
    for tx_id, dispute_type in list(disputes.items()):
        if dispute_type == 'FRAUD':
            if tx_id in transactions:
                merchant_id = transactions[tx_id]["merchant_id"]
                if merchant_id in merchants:
                    merchants[merchant_id] *= 3

    # Pass 2: check (customer_id, merchant_id, amount) >= 2 times within 60 minute window -> DUPLICATE
    customer_merchant_amount_count = defaultdict(list)
    for tx_id, tran in transactions.items():
        key = (tran["customer_id"], tran["merchant_id"], tran["amount"])
        customer_merchant_amount_count[key].append((tx_id, tran["timestamp_minutes"]))

    for key, timestamps in customer_merchant_amount_count.items():
        if len(timestamps) < 2:
            continue

        # Sort by timestamp to evaluate sliding window
        timestamps.sort(key=lambda x: x[1])

        i = 0
        while i < len(timestamps):
            j = i + 1
            while j < len(timestamps) and (timestamps[j][1] - timestamps[i][1] <= 60):
                disputes[timestamps[j][0]] = 'DUPLICATE'
                disputes[timestamps[i][0]] = 'DUPLICATE'
                j += 1
            i += 1

    for tx_id, dispute_type in disputes.items():
        if dispute_type == 'DUPLICATE':
            if tx_id in transactions:
                merchant_id = transactions[tx_id]["merchant_id"]
                if merchant_id in merchants:
                    merchants[merchant_id] += 10

    # Pass 3: check total disputed amount
    merchant_total_disputed_amount = defaultdict(int)
    for tx_id, dispute_type in disputes.items():
        if tx_id in transactions:
            merchant_id = transactions[tx_id]["merchant_id"]
            amount = transactions[tx_id]["amount"]
            merchant_total_disputed_amount[merchant_id] += amount

    for merchant_id, merchant_total in merchant_total_disputed_amount.items():
        if merchant_total > 1000:
            if merchant_id in merchants:
                merchants[merchant_id] += 50

    # Output: sorted lexicographically by merchant_id
    return [f"{merchant_id},{risk}" for merchant_id, risk in sorted(merchants.items())]
