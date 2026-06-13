from collections import defaultdict
import math

def transactionDisputeSystem(transactions_list, disputes_list, merchants_list):
    # -- Parsing ---
    transactions = defaultdict()
    for transaction in transactions_list:
        tx_id,merchant_id,customer_id,amount,timestamp_minutes = transaction.split(',')
        transactions[tx_id] = {
            "merchant_id": merchant_id,
            "customer_id": customer_id,
            "amount": int(amount),
            "timestamp_minutes": int(timestamp_minutes)
        }

    disputes = defaultdict()
    for dispute in disputes_list:
        tx_id, dispute_type = dispute.split(',')
        disputes[tx_id] = dispute_type

    merchants = defaultdict(int)
    for merchant in merchants_list:
        merchant_id, base_risk = merchant.split(',')
        merchants[merchant_id] = int(base_risk)

    # Pass 1: check type 'FRAUD' -> multiply risk by 3
    for key, value in disputes.items():
        if value == 'FRAUD':
            merchant_id = transactions[key]["merchant_id"]
            merchants[merchant_id] *= 3

    # Pass 2: check (customer_id, merchant_id, amount) >= 2 times within 60 minute window -> DUPLICATE
    customer_merchant_amount_count = defaultdict(list)

    for tx_id, tran in transactions.items():
        key = (tran["customer_id"], tran["merchant_id"], tran["amount"])
        customer_merchant_amount_count[key].append((tx_id, tran["timestamp_minutes"]))

    for timestamps in customer_merchant_amount_count.values():
        if len(timestamps) < 2: continue

        timestamps.sort(key=lambda x : x[1])

        i, j = 0, 1
        while i < j < len(timestamps):
            (tx_id1, timestamp1) = timestamps[i]
            (tx_id2, timestamp2) = timestamps[j]

            if timestamp2 - timestamp1 <= 60:
                disputes[tx_id1] = disputes[tx_id2] = 'DUPLICATE'
                j += 1
            else:
                i += 1

    for tx_id, dispute in disputes.items():
        if dispute == 'DUPLICATE':
            merchant_id = transactions[tx_id]["merchant_id"]
            merchants[merchant_id] += 10

    # Pass 3: check total disputed amount (amount of transaction exist in disputes_list)
    merchant_total_disputed_amount = defaultdict(int)
    for tx_id, dispute in disputes.items():
        merchant_id = transactions[tx_id]["merchant_id"]
        amount = transactions[tx_id]["amount"]
        merchant_total_disputed_amount[merchant_id] += amount

    for merchant_id, merchant_total in merchant_total_disputed_amount.items():
        if merchant_total > 1000:
            merchants[merchant_id] += 50

    # Output
    return [f"{merchant_id},{base_risk}" for merchant_id, base_risk in merchants.items()]

if __name__ == "__main__":
    transactions_list = [
        "tx1,M1,C1,50,100",
        "tx2,M1,C1,50,145",   # same (C1,M1,50), |145-100|=45 → DUPLICATE
        "tx3,M1,C1,50,210",   # same (C1,M1,50), |210-145|=65 > 60 → NOT dup of tx2, |210-100|=110 > 60 → NOT dup of tx1
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
    result = transactionDisputeSystem(transactions_list=transactions_list, disputes_list=disputes_list, merchants_list=merchants_list)
    print(result)
