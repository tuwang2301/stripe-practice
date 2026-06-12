# STRIPE ULTIMATE WEAPON
## Team Screen + Virtual Onsite Preparation Playbook

# What Stripe Actually Tests

Stripe-style interviews are usually not about:

- Dynamic Programming
- Segment Trees
- Competitive Programming tricks

Instead they heavily test:

- Parsing
- Business logic implementation
- Rules engines
- Multi-pass processing
- Aggregation
- State management
- Edge cases
- Communication
- Debugging
- Readable code

Think:

"Build a mini Stripe system"

instead of:

"Solve a LeetCode Hard problem"

---

# SECTION 1 - MUST KNOW PATTERNS

## Pattern 1 - Parsing

Input:

merchant1,1200,customer1,10

Convert to:

merchant_id
amount
customer_id
hour

---

## Pattern 2 - Aggregation

Track:

merchant -> score

customer -> transaction_count

merchant/customer -> frequency

---

## Pattern 3 - Multi-Pass Processing

Pass 1:
High amount

Pass 2:
Repeat customer

Pass 3:
Hourly burst

Pass 4:
Generate report

This is extremely Stripe-like.

---

## Pattern 4 - Parallel Datasets

transactions[i]

matches

rules[i]

This appeared in your OA.

---

## Pattern 5 - Rules Engine

Instead of hardcoding:

if amount > 1000

you consume rules dynamically.

---

# SECTION 2 - CLARIFYING QUESTIONS

Before coding ask:

1. Can IDs repeat?
2. Can merchants appear without transactions?
3. Is input guaranteed valid?
4. Can amounts be negative?
5. Should output be sorted?
6. Are transaction timestamps ordered?
7. What should happen on ties?

These questions create strong interviewer signals.

---

# SECTION 3 - EASY MOCKS

## EASY 1 - Merchant Revenue

Input:

merchant,amount

Aggregate revenue.

Output sorted.

---

## EASY 2 - Customer Counter

Count transactions per customer.

---

## EASY 3 - Invalid Payments

Reject:

amount <= 0

---

## EASY 4 - CSV Parser

Convert CSV strings into records.

---

## EASY 5 - Duplicate IDs

Find duplicate transaction IDs.

---

# SECTION 4 - MEDIUM MOCKS

## MEDIUM 1 - Merchant Risk Score

Each merchant has:

merchant_id,base_score

Rule:

amount > 1000

score += 10

Example:

merchant1,10

1200

500

Output:

merchant1,20

---

## MEDIUM 2 - Merchant Reputation

Rules:

successful_payment => +2

refund => -5

chargeback => -20

Compute final score.

---

## MEDIUM 3 - Login Monitoring

Track:

user_id,event_type

3 failed logins

=> lock account

---

## MEDIUM 4 - Velocity Detection

Same customer

5 transactions within same hour

=> suspicious

---

## MEDIUM 5 - Multi-Pass Risk Engine

Pass 1

High amount

Pass 2

Repeated customer

Pass 3

Generate scores

---

# SECTION 5 - ADVANCED TEAM SCREEN MOCKS

## TEAM SCREEN 1 - Fraud Engine

Transactions:

merchant,amount,customer,hour

Rules:

threshold,multiplier

Merchants:

merchant,base_score

Pass 1:

amount > threshold

score *= multiplier

Pass 2:

3+ customer transactions

score += 10

Pass 3:

3+ same-hour transactions

score -= 5

Return sorted results.

Target:
35-45 minutes

---

## TEAM SCREEN 2 - Dynamic Rules System

Rules:

HIGH_AMOUNT,+10

REPEAT_CUSTOMER,+5

BURST_ACTIVITY,-7

Apply rules from config.

Do not hardcode.

---

## TEAM SCREEN 3 - Merchant Ranking

Compute:

risk_score

Sort by:

highest score

then merchant_id

---

## TEAM SCREEN 4 - Payment Monitoring Platform

Build:

Merchant state

Customer state

Hourly state

Generate risk report.

---

## TEAM SCREEN 5 - Rule Simulator

Each transaction has:

corresponding rule

similar to your Stripe OA.

Requires:

parallel arrays

multiple passes

state tracking

---

# SECTION 6 - VIRTUAL ONSITE MOCKS

## ONSITE 1 - Fraud Detection Service

Implement:

evaluate_transactions()

Input:

transactions
rules
merchants

Output:

merchant scores

Discuss:

data structures

complexity

testing

---

## ONSITE 2 - Chargeback Analytics

Generate:

merchant chargeback report

customer chargeback report

top risky merchants

---

## ONSITE 3 - Payment Intelligence Engine

Transactions

Refunds

Disputes

Produce final risk rankings.

---

## ONSITE 4 - Alerting System

Generate alerts when:

high amount

burst activity

repeat customers

Return alert objects.

---

## ONSITE 5 - Stripe Mini Simulation

The biggest mock.

Inputs:

transactions
rules
merchants
customers

Pass 1:

amount scoring

Pass 2:

frequency scoring

Pass 3:

hour scoring

Pass 4:

merchant ranking

Pass 5:

report generation

Expected time:

60 minutes

---

# SECTION 7 - PYTHON CHEAT SHEET

Must know:

dict

set

list

Counter

defaultdict

sorted

sort

split

join

enumerate

zip

---

Examples

from collections import defaultdict

counts = defaultdict(int)

counts["alice"] += 1

---

from collections import Counter

Counter(["a","a","b"])

---

sorted(data, key=lambda x: x[1])

---

# SECTION 8 - INTERVIEW SCRIPT

First 2 minutes:

"Let me make sure I understand the requirements."

Ask questions.

Then:

"I'll use a dictionary to track merchant scores."

Then:

"I'll walk through an example."

Then code.

Then:

"Let me test a few edge cases."

This script alone is worth a lot of interviewer signal.

---

# FINAL BATTLE PLAN

Daily:

2 HashMap problems

2 Stripe-style mocks

1 full mock interview

Focus:

Readability > Cleverness

Correctness > Optimization

Communication > Silence

Testing > Guessing

This is the closest preparation strategy to the Stripe OA screenshots you shared.
