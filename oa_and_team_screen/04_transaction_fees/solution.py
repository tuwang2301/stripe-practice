import math

def calculate_fees(transaction_csv):
    # Parse inputs robustly (handles list of strings or single multi-line string, with or without header)
    if isinstance(transaction_csv, str):
        lines = [line.strip() for line in transaction_csv.split('\n') if line.strip()]
    else:
        lines = [line.strip() for line in transaction_csv if line.strip()]

    # Skip header if present
    if lines and (lines[0].startswith('id') or 'transaction_type' in lines[0]):
        lines = lines[1:]

    transaction_list = []
    for line in lines:
        parts = [p.strip() for p in line.split(',')]
        if len(parts) < 10:
            continue
        
        tx_id = parts[0]
        amount = int(parts[2])
        transaction_type = parts[7]
        payment_provider = parts[8]
        status = parts[9]

        transaction_list.append(
            {
                "id": tx_id,
                "transaction_type": transaction_type,
                "amount": amount,
                "payment_provider": payment_provider,
                "status": status,
                "fee": 0
            }
        )

    # Compute fees
    for tran in transaction_list:
        status = tran["status"]
        provider = tran["payment_provider"]
        amount = tran["amount"]

        if status == 'payment_completed':
            # 2.1% of payment_amount + 30
            tran["fee"] = math.floor(amount * 0.021 + 30)
        elif status == 'dispute_lost':
            tran["fee"] = 15
        elif status == 'dispute_won':
            tran["fee"] = 15 if provider == 'card' else 0
        else:
            tran["fee"] = 0

    # Output format
    output = []
    for tran in transaction_list:
        output.append(f"{tran['id']},{tran['transaction_type']},{tran['payment_provider']},{tran['fee']}")
    return output
