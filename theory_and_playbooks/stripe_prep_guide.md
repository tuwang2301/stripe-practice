# Stripe Internship — OA & Screening Prep

## Interview Format

- **Team Screen**: 60 min total — 45 min coding + 15 min buffer
- **Language**: Your choice (Python recommended)
- **Resources allowed**: Docs, Stack Overflow — **NO AI tools**
- **Style**: Practical simulation problems, NOT pure DSA

---

## Question 1 — Fraud Detection Scoring (Original OA)

### Problem Statement

You are given a list of transactions, a list of rules (one per transaction), and a list of merchants. Each merchant has a `base_score`. Your task is to compute a final fraud score for each merchant based on their transactions.

**Initialize** each merchant's `current_score = base_score`.

Then apply the following **3 separate passes** over the full transaction list (order matters):

---

### Pass 1 — Amount Threshold

For each transaction:

- If `transaction.amount > rule.min_transaction_amount` → `current_score *= rule.multiplicative_factor`

---

### Pass 2 — Repeat Customer Additive

For each transaction, track how many times a `customer_id` has transacted with a `merchant_id` (cumulative, in list order):

- If the count for `(customer_id, merchant_id)` reaches **3 or more** (including the current transaction) → `current_score += rule.additive_factor`

> The additive factor is added once per qualifying transaction (3rd, 4th, 5th, ...).

---

### Pass 3 — Same-Hour Frequency Penalty

For each transaction, track how many times the same `(customer_id, merchant_id, hour)` triple has appeared:

- If the count reaches **3 or more** (including current transaction), apply a penalty based on the hour:

| Hour Range        | Action                                                                                          |
| ----------------- | ----------------------------------------------------------------------------------------------- |
| 12 – 17 inclusive | **Add** `rule.penalty` (applied retroactively to ALL txns in that group, including 1st and 2nd) |
| 9–11 or 18–21     | **Subtract** `rule.penalty` (same retroactive logic)                                            |
| Outside above     | No action                                                                                       |

> When the 3rd transaction triggers the rule, go back and apply the penalty for the 1st and 2nd transactions as well (each with their own rule's penalty value).

---

### Input Format

```
transactions_list[i] = "merchant_id,amount,customer_id,hour"
rules_list[i]        = "min_transaction_amount,multiplicative_factor,additive_factor,penalty"
merchants_list[i]    = "merchant_id,base_score"
```

**Constraints:**

- `1 ≤ n (transactions) ≤ 1000`
- `1 ≤ m (merchants) ≤ 1000`
- `1 ≤ base_score ≤ 50`
- `0 ≤ hour ≤ 23`
- No integer overflow

---

### Output Format

Return a list of `"merchant_id,score"` strings sorted **lexicographically** by merchant_id.

---

### Example

```python
n = 6
transactions_list = [
    "merchant1,1200,customer1,10",
    "merchant1,500,customer1,10",
    "merchant2,2400,customer1,15",
    "merchant1,800,customer1,16",
    "merchant1,1000,customer2,17",
    "merchant1,1400,customer1,10",
]
rules_list = [
    "1000,2,8,15",
    "1400,5,3,19",
    "2300,3,17,3",
    "1800,2,9,6",
    "1000,4,8,2",
    "1200,3,11,7"
]
m = 2
merchants_list = [
    "merchant1,10",
    "merchant2,20",
]

# Expected output
[
    "merchant1,50",
    "merchant2,60"
]
```

**Trace for merchant1 (base=10):**

```
Pass 1 (amount check):
  tx0: 1200 > 1000 → 10 * 2 = 20
  tx1: 500 > 1400? No
  tx3: 800 > 1800? No
  tx4: 1000 > 1000? No (not strictly greater)
  tx5: 1400 > 1200 → 20 * 3 = 60

Pass 2 (repeat customer):
  Track (customer_id, merchant_id) count:
  tx0: customer1+merchant1 → count=1
  tx1: customer1+merchant1 → count=2
  tx3: customer1+merchant1 → count=3 → 60 + 9 = 69   [add rule tx3's additive=9]
  tx5: customer1+merchant1 → count=4 → 69 + 11 = 80  [add rule tx5's additive=11]
  (tx4: customer2+merchant1 → count=1, no trigger)

  Wait — re-check with actual additive values:
  tx0 rule: add=8, tx1 rule: add=3, tx3 rule: add=9, tx5 rule: add=11
  At count=3 (tx3): 60 + 8 + 3 + 9 = 80?

  Actually per spec: add additive_factor cumulatively starting from 3rd tx:
  tx3 (count=3): score += tx0.add + tx1.add + tx3.add = 8+3+9 = 20 → 60+20=80
  tx5 (count=4): score += tx5.add = 11 → 80+11=91

Pass 3 (same-hour penalty):
  Track (customer1, merchant1, hour=10):
  tx0: count=1, tx1: count=2, tx5: count=3 → triggers!
  Hour 10 is in range 9–11 → SUBTRACT penalty for all 3:
  tx0.penalty=15, tx1.penalty=19, tx5.penalty=7
  91 - 15 - 19 - 7 = 50 ✓

Final: merchant1 = 50
```

**Trace for merchant2 (base=20):**

```
Pass 1: tx2: 2400 > 2300 → 20 * 3 = 60
Pass 2: customer1+merchant2 count=1 → no trigger
Pass 3: no same-hour triple
Final: merchant2 = 60 ✓
```

---

## Practice Problems

### Problem 2 — Merchant Loyalty Score (Warm-up)

**Input:**

```
transactions_list[i] = "merchant_id,customer_id,amount,category"
merchants_list[i]    = "merchant_id,base_points"
```

**Passes:**

1. If `amount > 500` → `base_points *= 1.5`
2. If same `customer_id` has bought from same `merchant_id` **≥ 2 times** → `+50` per occurrence from 2nd onward
3. If `category == "electronics"` → `+20`; if `category == "food"` → `-10`

**Output:** `"merchant_id,points"` (floor), sorted lexicographically

---

### Problem 3 — Transaction Dispute System (Medium)

**Input:**

```
transactions_list[i] = "tx_id,merchant_id,customer_id,amount,timestamp_minutes"
disputes_list[i]     = "tx_id,dispute_type"   # FRAUD | DUPLICATE | ERROR
merchants_list[i]    = "merchant_id,base_risk"
```

**Passes:**

1. If transaction has dispute type `FRAUD` → `merchant_risk *= 3`
2. If same `(customer_id, merchant_id, amount)` appears ≥ 2 times within 60-minute window → mark as `DUPLICATE` → `merchant_risk += 10` per duplicate tx
3. If merchant's total disputed amount > 1000 → `merchant_risk += 50`

**Focus:** time-window lookup, multi-condition grouping

---

### Problem 4 — Rate Limiter Scorer (HTTP-flavored)

**Input:**

```
requests_list[i]  = "user_id,endpoint,timestamp_seconds,status_code"
endpoints_list[i] = "endpoint,rate_limit_per_minute,penalty_score,base_score"
```

**Passes:**

1. If `user_id` sends > `rate_limit_per_minute` requests to `endpoint` in any 60s window → `base_score *= 2`
2. If same `user_id` gets ≥ 3 `429` responses from same `endpoint` → `+penalty_score` per occurrence from 3rd onward
3. If endpoint's `4xx/5xx` rate > 50% → `base_score += 100`

**Focus:** sliding window with deque, HTTP status categorization

---

## Python Solution Template

```python
from collections import defaultdict

def solve(transactions_list, rules_list, merchants_list):
    # --- Parse ---
    merchants = {}
    for m in merchants_list:
        mid, base = m.split(",")
        merchants[mid] = int(base)

    txns = []
    for t, r in zip(transactions_list, rules_list):
        mid, amt, cid, hour = t.split(",")
        min_amt, mult, add, pen = r.split(",")
        txns.append({
            "merchant_id": mid,
            "amount": int(amt),
            "customer_id": cid,
            "hour": int(hour),
            "min_amount": int(min_amt),
            "mult": int(mult),
            "add": int(add),
            "penalty": int(pen),
        })

    scores = dict(merchants)

    # --- Pass 1: Amount threshold ---
    for tx in txns:
        mid = tx["merchant_id"]
        if mid not in scores:
            continue
        if tx["amount"] > tx["min_amount"]:
            scores[mid] *= tx["mult"]

    # --- Pass 2: Repeat customer additive ---
    customer_count = defaultdict(int)  # (cid, mid) → count
    customer_txns = defaultdict(list)  # (cid, mid) → list of tx indices

    for i, tx in enumerate(txns):
        key = (tx["customer_id"], tx["merchant_id"])
        customer_count[key] += 1
        customer_txns[key].append(i)
        mid = tx["merchant_id"]
        if mid not in scores:
            continue
        if customer_count[key] >= 3:
            scores[mid] += tx["add"]
        elif customer_count[key] == 3:
            # Add for all prior txns too
            for j in customer_txns[key]:
                scores[mid] += txns[j]["add"]

    # --- Pass 3: Same-hour frequency penalty ---
    hour_count = defaultdict(int)   # (cid, mid, hour) → count
    hour_txns = defaultdict(list)   # (cid, mid, hour) → list of tx indices

    for i, tx in enumerate(txns):
        key = (tx["customer_id"], tx["merchant_id"], tx["hour"])
        hour_count[key] += 1
        hour_txns[key].append(i)
        mid = tx["merchant_id"]
        if mid not in scores:
            continue
        if hour_count[key] == 3:
            hour = tx["hour"]
            if 12 <= hour <= 17:
                for j in hour_txns[key]:
                    scores[mid] += txns[j]["penalty"]
            elif (9 <= hour <= 11) or (18 <= hour <= 21):
                for j in hour_txns[key]:
                    scores[mid] -= txns[j]["penalty"]
        elif hour_count[key] > 3:
            hour = tx["hour"]
            if 12 <= hour <= 17:
                scores[mid] += tx["penalty"]
            elif (9 <= hour <= 11) or (18 <= hour <= 21):
                scores[mid] -= tx["penalty"]

    # --- Output ---
    return [f"{mid},{scores[mid]}" for mid in sorted(scores)]
```

---

## Interview Checklist

### Before coding

- [ ] Re-read the problem — identify how many **separate passes** are required
- [ ] Ask clarifying questions: what if merchant has no transactions? can amount equal min_amount?
- [ ] Confirm output format and sort order

### While coding

- [ ] Parse all inputs first into structured dicts/lists
- [ ] Implement each pass as a **separate loop** — never combine passes
- [ ] Use `defaultdict` for frequency tracking
- [ ] Name variables clearly: `customer_tx_count` not `ctc`

### After coding

- [ ] Run the provided example and verify output manually
- [ ] Test edge cases:
  - Merchant with zero transactions
  - Customer with exactly 2 transactions (boundary)
  - Hour = 0, hour = 23 (outside penalty ranges)
  - Amount exactly equal to `min_transaction_amount` (not strictly greater)
  - Same customer, multiple merchants
