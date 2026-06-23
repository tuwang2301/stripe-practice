# Question 1: Fraud Detection Scoring (Original OA)

You are given a list of transactions, a list of rules (one per transaction), and a list of merchants. Each merchant has a `base_score`. Your task is to compute a final fraud score for each merchant based on their transactions.

## Rules

Initialize each merchant's `current_score = base_score`.
Then apply the following **3 separate passes** over the full transaction list in order:

### Pass 1: Amount Threshold
For each transaction:
- If `transaction.amount > rule.min_transaction_amount` → `current_score *= rule.multiplicative_factor`

### Pass 2: Repeat Customer Additive
For each transaction, track how many times a `customer_id` has transacted with a `merchant_id` (cumulative, in list order):
- If the count for `(customer_id, merchant_id)` reaches **3 or more** (including the current transaction) → `current_score += rule.additive_factor`
*Note: The additive factor is added once per qualifying transaction (3rd, 4th, 5th, ...). At the 3rd transaction, we also retroactively add the additive factors for the 1st and 2nd transactions.*

### Pass 3: Same-Hour Frequency Penalty
For each transaction, track how many times the same `(customer_id, merchant_id, hour)` triple has appeared:
- If the count reaches **3 or more** (including current transaction), apply a penalty based on the hour:
  - **12 – 17 inclusive**: **Add** `rule.penalty` (applied retroactively to ALL txns in that group, including 1st and 2nd)
  - **9–11 or 18–21**: **Subtract** `rule.penalty` (same retroactive logic)
  - **Outside**: No action

---

## Input Format

- `transactions_list[i] = "merchant_id,amount,customer_id,hour"`
- `rules_list[i] = "min_transaction_amount,multiplicative_factor,additive_factor,penalty"`
- `merchants_list[i] = "merchant_id,base_score"`

## Output Format

Return a list of `"merchant_id,score"` strings sorted **lexicographically** by merchant_id.
