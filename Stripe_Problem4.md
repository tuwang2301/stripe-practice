Here is the question parsed and logically organized into Markdown format:

## Part 1 - Calculate the fee for various transaction types

Stripe processes millions of transactions every day across the globe of various types, payments, refunds and disputes. Each of these transactions carries fees. A transaction fee is the sum of a fixed fee and a variable fee.

You're given a list of transactions in a CSV file, you need to calculate the fee for each transaction. Write a function/method `calculate_fees(transaction_csv)` that takes transactions as a CSV string and returns the fees for each transaction. The output should be in the desired format stated below. Following are input and output formats.

---

### Fees for each Status

* **payment_completed**: 2.1% of payment_amount + 30


* **dispute_lost**: 15


* **dispute_won**: 15 for card payments, 0 for Klarna payments


* **everything else**: 0



---

### Input Format

**Transaction**

* `string id` // identifier for the transaction


* `string reference` // reference for the transaction


* `int amount` // amount in cents authorised


* `string currency` // 150 format of the currency


* `string date` // date of the transaction completion


* `string merchant_id` // transaction merchant


* `string buyer_country` // country where the buyer paid, ISO code


* `string transaction_type` // payment, refund, dispute


* `string payment_provider` // card, klarna


* `string status` // payment_completed, payment_failed, payment_pending, dispute_won, dispute_lost, refund_completed, refund_failed, refund_pending



### Output Format

**Fee**

* `String id` // transaction id


* `String transaction_type` // payment, refund, dispute


* `String payment_provider` // card, klarna


* `int fee`


---

### Examples

**Sample Input 1**

```csv
id, reference, amount, currency, date, merchant_id,buyer_country, transaction_type, payment_provider, status
py_1,1,1000, eur, 2024-12-24, acct_1, ie, payment, card, payment_completed
py_2, 2, 2500, eur, 2024-12-24,acct_2,ie, payment, card, payment_failed
py_3,3,3400, eur, 2024-12-25, acct_2, ie, payment, klarna, payment_completed

```

**Sample Output 1**

```csv
id, transaction_type, payment_provider, fee
py_1, payment, card, 51
py_2, payment, card, 0
py 3, payment, klarna, 101

```

**Sample Input 2**

```csv
id, reference, amount, currency,date, merchant_id,buyer_country, transaction_type,payment_provider, status
du_1, py_3, 1000, eur, 2025-01-01,acct_2,ie, dispute, klarna, dispute_won
du_2, py_3,1000, eur, 2025-01-01,acct_2,ie, dispute, klarna, dispute_lost
du_3, py_1, 1000, eur, 2025-01-01,acct_1,ie,dispute,card, dispute_won
du_4, py_2, 2500, eur, 2025-01-01,acct_2,ie,dispute,card, dispute_lost

```

**Sample Output 2**

```csv
id, transaction_type, payment_provider, fee
du_1, dispute, klarna, 0
du_2, dispute, klarna, 15
du_3, dispute, card, 15
du_4, dispute, card, 15

```

> **Note:** Feel free to use the Sample Input as a string constant in your code
> 
> 

---

### Starter Code



```python
def calculate_fees (transaction_csv):
#Write your code here
main

```