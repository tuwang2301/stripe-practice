from collections import defaultdict
import math

def calculate_fees(transaction_csv):
    # -- Parsing ---
    transaction_list = []
    for tran in transaction_csv:
        id, _, amount, _, _, _, _, transaction_type, payment_provider, status = tran.split(',')
        transaction_list.append(
            {
                "id": id,
                "transaction_type": transaction_type,
                "amount": int(amount),
                "payment_provider": payment_provider,
                "status": status,
                "fee": 0
            }
        )

    # Computing
    for tran in transaction_list:
        if tran["status"] == 'payment_completed':
            tran["fee"] = (tran["amount"]*21) / 1000 + 30
        elif tran["status"] == 'dispute_lost':
            tran["fee"] = 15
        elif tran["status"] == 'dispute_won':
            tran["fee"] = 15 if tran["payment_provider"] == 'card' else 0

    # Output
    return [", ".join([tran["id"],tran["transaction_type"],tran["payment_provider"],str(tran["fee"])]) for tran in transaction_list]

if __name__ == "__main__":
    transactions = [
        "du_1,py_3,1000,eur,2025-01-01,acct_2,ie,dispute,klarna,dispute_won",
        "du_2,py_3,1000,eur,2025-01-01,acct_2,ie,dispute,klarna,dispute_lost",
        "du_3,py_1,1000,eur,2025-01-01,acct_1,ie,dispute,card,dispute_won",
        "du_4,py_2,2500,eur,2025-01-01,acct_2,ie,dispute,card,dispute_lost"
    ]

    result = calculate_fees(transaction_csv=transactions)
    print(result)
