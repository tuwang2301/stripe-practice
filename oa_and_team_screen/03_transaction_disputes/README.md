# Problem 3: Transaction Dispute System

Compute a final risk score for each merchant based on their transactions and disputes.

## Inputs

- `transactions_list[i] = "tx_id,merchant_id,customer_id,amount,timestamp_minutes"`
- `disputes_list[i] = "tx_id,dispute_type"` (e.g. `FRAUD`, `ERROR`)
- `merchants_list[i] = "merchant_id,base_risk"`

## Rules

Perform the following three passes in order:

1. **Fraud Dispute**: If a transaction has dispute type `FRAUD` → `merchant_risk *= 3`.
2. **Duplicate Detection**: If the same `(customer_id, merchant_id, amount)` appears **>= 2 times** within a **60-minute window** (inclusive, `|t1 - t2| <= 60`) → mark all such transactions in that window as `DUPLICATE` → `merchant_risk += 10` per duplicate transaction.
3. **Disputed Amount Threshold**: If a merchant's total disputed amount (from all disputes including initial disputes and newly detected duplicates) is strictly greater than 1000 → `merchant_risk += 50`.

## Output Format

Return the merchant risk scores in the format `"merchant_id,risk"`, sorted lexicographically by `merchant_id`.
