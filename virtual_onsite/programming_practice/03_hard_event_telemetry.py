"""
STRIPE PROGRAMMING PRACTICE 03: Telemetry Alert System (HARD)
============================================================

PROBLEM DESCRIPTION:
Stripe's infrastructure team monitors API telemetry logs.
We want to raise alarms if a merchant encounters too many server errors (HTTP 5xx status codes) within a sliding window.

You are given:
- `logs`: A list of tuples `(timestamp, merchant_id, status_code, count)`.
- `window_size`: The duration of the sliding window in seconds.
- `threshold`: The threshold count of server errors to trigger an alarm.

Your task is to:
1. Process logs in chronological order.
2. For each merchant, track their **server error count** (the sum of `count` for records with `status_code >= 500` whose timestamps fall in the inclusive range `[t - window_size + 1, t]`).
3. Emit a `TRIGGER` alarm for a merchant when their server error count changes from strictly less than `threshold` to **greater than or equal to threshold**.
4. Emit a `RESOLVE` alarm when their server error count changes from greater than or equal to `threshold` to **strictly less than threshold**.
5. Alarms are evaluated and emitted **only** when processing an input log. Do not emit consecutive duplicate alarms of the same type for the same merchant.
6. Return all emitted alarms in chronological order as 4-tuples:
   `(timestamp, merchant_id, 'TRIGGER'/'RESOLVE')`
   If multiple alarms are emitted at the same timestamp, preserve the original input order of the logs that triggered them.

EXAMPLE:
logs = [
    (1, "M1", 500, 2), # error count = 2
    (2, "M1", 500, 2), # error count = 4 (TRIGGER!)
    (5, "M1", 500, 1), # t=1 and t=2 expire (since 5-3+1 = 3). error count = 1 (RESOLVE!)
    (6, "M1", 200, 1)  # HTTP 200 (not an error, ignored)
]
window_size = 3
threshold = 4

Output:
[
    (2, "M1", "TRIGGER"),
    (5, "M1", "RESOLVE")
]
"""

from collections import defaultdict, deque

def detect_telemetry_alarms(logs, window_size, threshold):
    # WRITE YOUR CODE HERE
    pass


# ===================================================================
# TEST SUITE (Run this file to verify your solution)
# ===================================================================
if __name__ == "__main__":
    logs = [
        (1, "M1", 500, 2),
        (1, "M2", 503, 3), # M2 has 3 errors at t=1
        (2, "M1", 500, 2), # M1 has 2+2=4 errors -> TRIGGER at t=2
        (2, "M2", 200, 1), # ignored
        (3, "M2", 500, 1), # M2 has 3+1=4 errors -> TRIGGER at t=3
        (5, "M1", 503, 1), # M1: t=1 and t=2 expire. error count = 1 -> RESOLVE at t=5
        (5, "M2", 500, 1)  # M2: t=1 expires. error count = 1+1=2 -> RESOLVE at t=5
    ]
    window_size = 3
    threshold = 4
    
    # Expected results:
    # t=1: M2 count=3. M1 count=2. (no alarms)
    # t=2: M1 count=4 >= 4 -> TRIGGER.
    # t=3: M2 count=4 >= 4 -> TRIGGER.
    # t=5 (M1 log processed): M1 count = 1 < 4 -> RESOLVE.
    # t=5 (M2 log processed): M2 count = 2 < 4 -> RESOLVE.
    expected = [
        (2, "M1", "TRIGGER"),
        (3, "M2", "TRIGGER"),
        (5, "M1", "RESOLVE"),
        (5, "M2", "RESOLVE")
    ]
    
    result = detect_telemetry_alarms(logs, window_size, threshold)
    print("Your output:", result)
    if result == expected:
        print("SUCCESS: Programming Problem 03 Passed!")
    else:
        print("FAIL: Expected", expected, "but got", result)
