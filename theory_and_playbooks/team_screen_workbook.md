# Stripe Team Screen Practice Workbook

# Overview

This workbook is inspired by the style of problems commonly seen in Stripe assessments:

- Transaction processing
- Fraud detection systems
- Rules engines
- Merchant scoring
- Multi-pass data processing
- Parsing CSV-like records
- Hash maps and aggregations
- Business logic implementation

The goal is not advanced algorithms.

The goal is to practice:

- Reading long specifications
- Asking clarifying questions
- Implementing business rules correctly
- Writing readable code
- Testing edge cases
- Debugging effectively

---

# Problem 1: Merchant Risk Score

## Description

You are given a list of merchants and a list of transactions.

Each merchant starts with a base risk score.

For every transaction whose amount is greater than 1000, add 10 points to the merchant's score.

Return all merchants and their final scores sorted lexicographically by merchant_id.

---

## Example

### Input

```python
transactions = [
    "merchant1,1200",
    "merchant1,500",
    "merchant2,2400"
]

merchants = [
    "merchant1,10",
    "merchant2,20"
]
```

### Output

```python
[
    "merchant1,20",
    "merchant2,30"
]
```

---

# Problem 2: Multi-Pass Risk Engine

## Description

Each merchant starts with a base score.

Perform the following passes over the entire transaction list:

### Pass 1

If amount > 1000

```text
score *= 2
```

### Pass 2

If amount > 1800

```text
score += 5
```

Return the final score for every merchant.

---

## Example

### Input

```python
transactions = [
    "merchant1,1500",
    "merchant1,2000"
]

merchants = [
    "merchant1,10"
]
```

### Output

```python
[
    "merchant1,45"
]
```

---

# Problem 3: Frequent Customer Detection

## Description

A merchant becomes riskier when the same customer repeatedly transacts with them.

For every customer:

- First transaction => no change
- Second transaction => no change
- Third transaction and every transaction after => +10 score

Apply the rule separately for each merchant.

---

## Example

### Input

```python
transactions = [
    "merchant1,alice",
    "merchant1,alice",
    "merchant1,alice",
    "merchant1,bob"
]

merchants = [
    "merchant1,0"
]
```

### Output

```python
[
    "merchant1,10"
]
```

---

# Problem 4: Hourly Fraud Burst

## Description

For each merchant and customer pair:

If three or more transactions occur during the same hour:

- Add 20 penalty points

The penalty is applied once per qualifying transaction starting from the third transaction.

---

## Example

### Input

```python
transactions = [
    "merchant1,alice,13",
    "merchant1,alice,13",
    "merchant1,alice,13"
]

merchants = [
    "merchant1,0"
]
```

### Output

```python
[
    "merchant1,20"
]
```

---

# Problem 5: Fraud Scoring System

## Description

Each merchant starts with a base score.

Perform three passes:

### Pass 1

If amount > 1000

```text
score += 10
```

### Pass 2

If the same customer has made 3 or more transactions

```text
score += 5
```

### Pass 3

If the same customer makes 3 or more transactions in the same hour

```text
score += 20
```

Return final scores.

---

## Example

### Input

```python
transactions = [
    "merchant1,1500,alice,10",
    "merchant1,1500,alice,10",
    "merchant1,1500,alice,10"
]

merchants = [
    "merchant1,0"
]
```

### Output

```python
[
    "merchant1,75"
]
```

---

# Problem 6: Transaction Rules Engine

## Description

Each transaction has a matching rule.

Transaction format:

```text
merchant_id,amount
```

Rule format:

```text
threshold,multiplier
```

For every transaction:

If:

```text
amount > threshold
```

Multiply the merchant score by multiplier.

Each transaction uses its own corresponding rule.

---

## Example

### Input

```python
transactions = [
    "merchant1,1500"
]

rules = [
    "1000,2"
]

merchants = [
    "merchant1,10"
]
```

### Output

```python
[
    "merchant1,20"
]
```

---

# Problem 7: Account Reputation System

## Description

Every user starts with a reputation score.

Event types:

```text
failed_login
password_reset
chargeback
```

Rules:

```text
failed_login => -5
password_reset => -2
chargeback => -20
```

Apply all events and return final reputations.

---

## Example

### Input

```python
users = [
    "alice,50",
    "bob,70"
]

events = [
    "alice,failed_login",
    "alice,failed_login",
    "alice,failed_login"
]
```

### Output

```python
[
    "alice,35",
    "bob,70"
]
```

---

# Problem 8: Merchant Scoring Engine (Stripe Style)

## Description

Implement a simplified fraud scoring engine.

Inputs:

### transactions

```text
merchant_id,amount,customer_id,hour
```

### merchants

```text
merchant_id,base_score
```

Rules:

### Pass 1

If amount > 1000

```text
score *= 2
```

### Pass 2

If a customer has made at least 3 transactions to the same merchant

```text
score += 10
```

### Pass 3

If a customer has made at least 3 transactions in the same hour to the same merchant

```text
score -= 5
```

Return merchants in lexicographical order.

---

## Example

### Input

```python
transactions = [
    "merchant1,1200,alice,10",
    "merchant1,1300,alice,10",
    "merchant1,1400,alice,10",
    "merchant2,500,bob,12"
]

merchants = [
    "merchant1,10",
    "merchant2,20"
]
```

### Output

```python
[
    "merchant1,85",
    "merchant2,20"
]
```

---

# Problem 9: Merchant Chargeback Analyzer

## Description

Each chargeback increases merchant risk.

Rules:

```text
1 chargeback => +10
2 chargebacks => +25
3+ chargebacks => +50
```

Return final merchant scores.

---

## Example

### Input

```python
merchants = [
    "merchant1,20"
]

chargebacks = [
    "merchant1",
    "merchant1",
    "merchant1"
]
```

### Output

```python
[
    "merchant1,70"
]
```

---

# Problem 10: Full Stripe Mock (45-Minute Simulation)

## Description

Implement a fraud detection engine.

Inputs:

### transactions

```text
merchant_id,amount,customer_id,hour
```

### rules

```text
threshold,multiplier,bonus,penalty
```

Each transaction has a corresponding rule.

### merchants

```text
merchant_id,base_score
```

Perform the following passes:

### Pass 1

If amount > threshold

```text
score *= multiplier
```

### Pass 2

If a customer has made at least 3 transactions to the same merchant

```text
score += bonus
```

### Pass 3

If a customer has made at least 3 transactions in the same hour to the same merchant

```text
score -= penalty
```

Return:

```python
[
    "merchant_id,final_score"
]
```

sorted lexicographically.

---

# Recommended Interview Workflow

For every problem:

1. Restate the requirements
2. Ask clarifying questions
3. Identify data structures
4. Explain the approach
5. Implement
6. Test manually
7. Check edge cases
8. Discuss complexity

Focus on:

- Correctness
- Readability
- Communication
- Debugging

These are the strongest signals for Stripe Team Screen interviews.
