Chronological Fraud Rule Authorization Report
Easy
Stripe
Software Engineer
Hash Table
You are given two lists: (1) Authorization Requests, each as a dictionary with keys time (int seconds), unique_id (string), amount (int), card_number (string), merchant (string); and (2) Fraud Rules, each as a dictionary with keys time (int seconds), field (string), value (string). From each rule's time onward (i.e., for any request with request.time >= rule.time), any future request whose specified field equals the rule's value must be marked fraudulent. Produce a chronological report of all requests as lines formatted: "time unique_id amount DECISION", where DECISION is REJECT if any rule applies, otherwise APPROVE. The report must be ordered by increasing time; for ties, preserve the original input order of requests. Valid rule fields are: unique_id, amount, card_number, merchant. For matching, compare rule.value to str(request[field]).

Examples
Example 1
Input
requests = [{"time": 5, "unique_id": "A1", "amount": 120, "card_number": "4111", "merchant": "X"}, {"time": 1, "unique_id": "A0", "amount": 300, "card_number": "5555", "merchant": "Y"}, {"time": 5, "unique_id": "A2", "amount": 120, "card_number": "4111", "merchant": "Z"}] rules = []
Output
["1 A0 300 APPROVE", "5 A1 120 APPROVE", "5 A2 120 APPROVE"]
Notes
No rules exist, so all requests are APPROVE. Output is ordered by time, preserving input order for the two requests at time=5.
Example 2
Input
requests = [{"time": 5, "unique_id": "A1", "amount": 120, "card_number": "4111", "merchant": "X"}, {"time": 1, "unique_id": "A0", "amount": 300, "card_number": "5555", "merchant": "Y"}, {"time": 5, "unique_id": "A2", "amount": 120, "card_number": "4111", "merchant": "Z"}] rules = [{"time": 3, "field": "card_number", "value": "4111"}, {"time": 5, "field": "merchant", "value": "Y"}, {"time": 5, "field": "amount", "value": "120"}]
Output
["1 A0 300 APPROVE", "5 A1 120 REJECT", "5 A2 120 REJECT"]
Notes
The rule on card_number=4111 at time=3 makes both time=5 requests REJECT. The merchant=Y rule at time=5 does not affect the earlier time=1 request.
Constraints
0 <= len(requests) <= 200000
0 <= len(rules) <= 200000
0 <= time <= 10^9
0 <= amount <= 10^9 (integer)
field ∈ {"unique_id", "amount", "card_number", "merchant"}
A rule with time t applies to any request with timestamp >= t
Report must be sorted by time ascending; if times are equal, preserve request input order
Rule matching uses string equality: rule.value == str(request[field])