import datetime

def parse_invoice(invoice_str):
    parts = [p.strip() for p in invoice_str.split(',')]
    inv_id = parts[0]
    amount = int(parts[1])
    date_str = parts[2]
    # Parse date to date object for easy comparison
    date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
    return {
        "id": inv_id,
        "amount": amount,
        "date_str": date_str,
        "date_obj": date_obj
    }

def parse_payment(payment_str):
    parts = [p.strip() for p in payment_str.split(',')]
    pay_id = parts[0]
    amount = int(parts[1])
    target_invoice_id = None
    
    # Check if there is a paying for section
    for part in parts[2:]:
        if part.startswith("paying for:"):
            target_invoice_id = part.replace("paying for:", "").strip()
            break
            
    return {
        "id": pay_id,
        "amount": amount,
        "target_invoice_id": target_invoice_id
    }

def match_payment(invoices, payment, forgiveness=None):
    # Parse all invoices
    parsed_invoices = [parse_invoice(inv) for inv in invoices]
    # Parse payment
    pay = parse_payment(payment)

    # 1. Explicit match
    if pay["target_invoice_id"]:
        for inv in parsed_invoices:
            if inv["id"] == pay["target_invoice_id"]:
                return f"{pay['id']} paid {pay['amount']} amount for invoice {inv['id']} on date {inv['date_str']}"
        # If explicit invoice ID is provided but not found, we do NOT fall back.
        # "match that invoice and ignore amount-based or forgiveness-based matching"
        return "no match found"

    # 2. Exact amount match
    exact_matches = [inv for inv in parsed_invoices if inv["amount"] == pay["amount"]]
    if exact_matches:
        # Tie-breaking: earliest by date, then lexicographically by id
        exact_matches.sort(key=lambda x: (x["date_obj"], x["id"]))
        best_inv = exact_matches[0]
        return f"{pay['id']} paid {pay['amount']} amount for invoice {best_inv['id']} on date {best_inv['date_str']}"

    # 3. Forgiveness match
    if forgiveness is not None:
        forgiveness_matches = []
        for inv in parsed_invoices:
            diff = abs(inv["amount"] - pay["amount"])
            if diff <= forgiveness:
                forgiveness_matches.append((inv, diff))

        if forgiveness_matches:
            # Tie-breaking: earliest by date, then lexicographically by id
            forgiveness_matches.sort(key=lambda x: (x[0]["date_obj"], x[0]["id"]))
            best_inv, diff = forgiveness_matches[0]
            if diff > 0:
                return f"{pay['id']} paid {pay['amount']} amount for invoice {best_inv['id']} on date {best_inv['date_str']}; forgave {diff}"
            else:
                return f"{pay['id']} paid {pay['amount']} amount for invoice {best_inv['id']} on date {best_inv['date_str']}"

    return "no match found"
