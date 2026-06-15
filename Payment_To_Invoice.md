Design and implement a payment-to-invoice matcher. Inputs: (a) invoices, a list like ["invoice-id-1, 10000, 2022-01-01", "invoice-id-2, 30000, 2022-01-01"], where amounts are integer cents; (b) payment, a single string like "payment-id, 30000, paying for: invoice-id-1" or "payment-id, 30000" when the invoice id is absent; and (c) an optional forgiveness value (integer cents). Output: a canonical message "{payment-id} paid {paid_amount} amount for invoice {invoice-id} on date {invoice_date}" and, when forgiveness is used, append "; forgave {difference}" indicating how much was forgiven. Matching rules and priorities:

If the payment explicitly contains an invoice id, match that invoice and ignore amount-based or forgiveness-based matching.
Otherwise, match by exact amount; if multiple invoices have that amount, pick the earliest by date; if still tied, break ties by smallest invoice-id lexicographically.
Otherwise, if a forgiveness value is provided, match the invoice whose amount differs from the payment by at most forgiveness; if multiple qualify, pick the earliest by date, then invoice-id.
If nothing matches, specify no match found. Requirements: describe your data structures for invoices and payments, your parsing approach (prefer simple substring/split over regex), and why you use integer cents instead of floats. Provide pseudocode or code for match_payment(invoices, payment, forgiveness=None). Finally, enumerate a comprehensive test suite covering: explicit id present/absent, multiple exact-amount candidates, forgiveness matches (including boundary equals and just-over-the-limit), tie-breaking by date and id, and regression tests ensuring earlier behaviors remain correct after adding forgiveness.

**Solving this problem**
okay so for this problem I will create a dictionary with invoiceId as key
We will check the invoice id of the payment first
I will create a dictionary with the amount as key, and list of the invoices.
If no we switch to find the list of invoice with same amount => sorted by date => sort by id
If no we switch to use the forgiveness by sorting the keys in dictionary, using binary search to search by forgiveness
If no return None
