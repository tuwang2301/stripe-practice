# Problem 4: Transaction Fees Scorer

Calculate the fee for each transaction based on its status and payment provider.

## Fees Table

- `payment_completed`: `2.1%` of amount + `30` (rounded down to nearest integer cent)
- `dispute_lost`: `15`
- `dispute_won`: `15` for card payments, `0` for Klarna payments
- Everything else: `0`

## Input Format

A CSV structure representing transactions, either as a list of CSV strings or a single multi-line CSV string.
Fields:
`id, reference, amount, currency, date, merchant_id, buyer_country, transaction_type, payment_provider, status`

## Output Format

Return a list of strings in CSV format representing the fee for each transaction:
`id, transaction_type, payment_provider, fee`
