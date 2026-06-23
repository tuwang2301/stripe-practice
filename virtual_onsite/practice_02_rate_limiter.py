"""
STRIPE PRACTICE PROBLEM 02: Rate Limiter with Sliding Window (MEDIUM)
===================================================================

PROBLEM DESCRIPTION:
In real-world web services, we must rate-limit clients to prevent API abuse.
Your task is to design a class `RateLimiter` that checks whether a request from a client should be allowed.

Interface:
1. `__init__(self, limit, window_size)`
   - `limit`: The maximum number of requests allowed for a client in the sliding window.
   - `window_size`: The duration of the sliding window in seconds.
   
2. `allow_request(self, client_id, timestamp) -> bool`
   - Evaluates a request at `timestamp` (integer seconds).
   - If the client has sent strictly less than `limit` requests in the sliding window `[timestamp - window_size + 1, timestamp]` (inclusive):
     - Record this request at the current timestamp.
     - Return `True`.
   - Otherwise, do NOT record the request, block it, and return `False`.

ASSUMPTIONS:
- Timestamps are non-decreasing (t never goes backwards) for any sequence of calls.
- You must clean up expired timestamps from memory (using a double-ended queue `collections.deque`) to prevent infinite memory usage.
"""

from collections import defaultdict, deque

class RateLimiter:
    def __init__(self, limit, window_size):
        # WRITE YOUR INITIALIZATION HERE
        pass

    def allow_request(self, client_id, timestamp):
        # WRITE YOUR LOGIC HERE
        pass


# ===================================================================
# TEST SUITE (Run this file to verify your solution)
# ===================================================================
if __name__ == "__main__":
    # Test case: Max 3 requests in a 10-second window
    limiter = RateLimiter(limit=3, window_size=10)
    
    # Client 1 requests:
    print("t=1, Client 1:", limiter.allow_request("c1", 1))   # True (1 request: [1])
    print("t=2, Client 1:", limiter.allow_request("c1", 2))   # True (2 requests: [1, 2])
    print("t=5, Client 1:", limiter.allow_request("c1", 5))   # True (3 requests: [1, 2, 5])
    print("t=8, Client 1:", limiter.allow_request("c1", 8))   # False (Blocked! Limit reached. Window [0, 8] has [1, 2, 5] = 3)
    
    # Client 2 requests (Independent):
    print("t=8, Client 2:", limiter.allow_request("c2", 8))   # True (1 request for c2: [8])
    
    # Client 1 requests at t=11 (1 expires since 11 - 10 + 1 = 2, so t=1 is outside [2, 11]):
    # Window [2, 11] contains [2, 5]. Total = 2 requests. Less than 3, so allowed.
    print("t=11, Client 1:", limiter.allow_request("c1", 11)) # True (Staged: [2, 5, 11])
    print("t=12, Client 1:", limiter.allow_request("c1", 12)) # False (Blocked! Window [3, 12] has [5, 11, 12] = 3)
