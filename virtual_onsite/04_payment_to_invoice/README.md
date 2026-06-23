# Problem 4: Payment to Invoice Matcher

Design and implement a system to match payments to invoices.

## Inputs

- `invoices`: a list of strings formatted as `"invoice-id, amount, date"`, where amount is in integer cents and date is `YYYY-MM-DD`.
  Example: `["invoice-id-1, 10000, 2022-01-01", "invoice-id-2, 30000, 2022-01-01"]`
- `payment`: a single string. It can be:
  - Explicit: `"payment-id, amount, paying for: invoice-id"`
  - Implicit: `"payment-id, amount"`
- `forgiveness`: optional integer cents representing a tolerance range.

## Matching Rules & Priority

1. **Explicit Match**: If the payment contains `"paying for: {invoice-id}"`, match that invoice. Ignore amount-based or forgiveness-based matching.
2. **Exact Amount Match**: Match the invoice with the exact same amount.
   - If multiple invoices have that exact amount, pick the earliest by date.
   - If still tied, break ties by smallest `invoice-id` lexicographically.
3. **Forgiveness Match**: If no exact match and `forgiveness` is provided, find all invoices whose amount differs from the payment by at most `forgiveness` (i.e. `|invoice_amount - payment_amount| <= forgiveness`).
   - If multiple qualify, pick the earliest by date.
   - If still tied, break ties by smallest `invoice-id` lexicographically.
4. **No Match**: If no invoices qualify, return `"no match found"`.

## Output Format

- If matched without forgiveness:
  `"{payment-id} paid {payment_amount} amount for invoice {invoice-id} on date {invoice_date}"`
- If matched using forgiveness:
  `"{payment-id} paid {payment_amount} amount for invoice {invoice-id} on date {invoice_date}; forgave {difference}"`
  where `difference = abs(invoice_amount - payment_amount)`.
- If no match found:
  `"no match found"`
