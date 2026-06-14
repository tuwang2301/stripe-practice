Detect Trigger and Resolve Events
Medium
Stripe
Software Engineer
You are given transaction logs sorted by non-decreasing timestamp. Each log is a 4-tuple: (timestamp, merchant_id, status_code, count). Monitor each (merchant_id, status_code) pair independently.

For a log processed at time t, its rolling error count is the sum of count values from records with the same (merchant_id, status_code) whose timestamps fall in the inclusive range [t - window_size + 1, t].

While processing the logs in chronological order:

Emit a TRIGGER event when a pair's rolling count changes from strictly less than threshold to greater than or equal to threshold.
Emit a RESOLVE event when a pair's rolling count changes from greater than or equal to threshold to strictly less than threshold.
Do not emit duplicate consecutive events of the same type for the same pair.
Important: events are evaluated only when processing an input log. Do not create synthetic events at times when no log exists for that pair. If multiple logs share the same timestamp, process them in input order.

Return all emitted events in chronological order as 4-tuples: (timestamp, merchant_id, status_code, event_type).

Examples
Example 1
Input
([(1, 'm1', 500, 2), (2, 'm1', 500, 2), (5, 'm1', 500, 1), (6, 'm1', 500, 1)], 3, 4)
Output
[(2, 'm1', 500, 'TRIGGER'), (5, 'm1', 500, 'RESOLVE')]
Notes
At time 2, the rolling count for ('m1', 500) becomes 4, crossing the threshold and triggering an alert. At time 5, the earlier counts have expired from the 3-second window, so the rolling count drops to 1 and emits RESOLVE.
Example 2
Input
([(1, 'A', 404, 2), (1, 'A', 404, 1), (2, 'B', 500, 3), (3, 'A', 404, 1), (4, 'B', 500, 1)], 3, 3)
Output
[(1, 'A', 404, 'TRIGGER'), (2, 'B', 500, 'TRIGGER')]
Notes
The second log at timestamp 1 brings ('A', 404) to a rolling count of 3, so it triggers. Pair ('B', 500) reaches 3 at time 2 and also triggers. Later logs keep both pairs above threshold, so no duplicate TRIGGER events are emitted.
Constraints
0 <= len(logs) <= 200000
0 <= timestamp <= 10^9, and logs are sorted by non-decreasing timestamp
1 <= window_size <= 10^9
1 <= threshold <= 10^12
1 <= count <= 10^9
merchant_id and status_code can be used as dictionary keys
