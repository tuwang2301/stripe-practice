Design a class AccountScheduler that manages the time-based availability of a fixed set of account IDs.

Initialization
You are given:

accounts : a list of integers representing all account IDs in the system.
locked_until : a dictionary mapping account_id → integer timestamp, e.g.:
locked_until = {
1: 10,
2: 5,
3: 0,
4: 20
}
Interpretation of locked_until[account_id]:

The account is unavailable (locked) for all times t such that t < locked_until[account_id] .
The account is available for all times t such that t >= locked_until[account_id] .
If an account does not appear in locked_until , treat it as if locked_until[account_id] = 0 (initially available at t >= 0 ).
All time values are integers. You may assume all method calls are processed sequentially; you do not need to handle concurrency.

Example state and queries:

accounts = [1, 2, 3, 4]
locked_until = {
1: 10,
2: 5,
3: 0,
4: 20
}

is_available(1, 8) -> False # 8 < 10
is_available(2, 8) -> True # 8 >= 5
is_available(3, 1) -> True # 1 >= 0
is_available(4, 21) -> True # 21 >= 20
Part 1 — Availability queries
Implement the class constructor and a method:

is_available(account_id, t) -> bool
that returns whether account_id is available at time t according to the locked_until rules above.

You may store and update internal state in any way you like, but is_available must be correct for any sequence of calls.

Part 2 — Explicit acquire operation
Extend AccountScheduler with a method to acquire/lock a specific account for some duration starting at a given time. Add:

acquire(account_id, t, duration)
Semantics:

t is the current time of the operation.
duration is a positive integer.
When acquire(account_id, t, duration) is called, you should update internal state so that the account becomes unavailable for the time interval [t, t + duration) . In terms of the locked_until model, this means:
locked_until[account_id] = max(locked_until[account_id], t) + duration
(i.e., if the account was already locked until some time in the future, the new lock extends from the later of the current lock and t ).
You may choose whether acquire returns void or a boolean indicating success/failure; if you support failure, it should fail (e.g., return False ) when the account is not available at time t .
Assume all acquire and is_available calls are supplied with non-decreasing timestamps (t never goes backwards).

Part 3 — Auto-select account using LRU policy
Now extend the API to support acquiring any available account automatically, using an LRU (least recently used) policy.

Add an overloaded method:

auto_acquire(t, duration) -> Optional[account_id]
Semantics:

Consider all accounts that are available at time t (i.e., is_available(account_id, t) is True ).
Among those, choose the account that was least recently used , where "used" is defined as:
The last time the account was successfully acquired (either via acquire(account_id, t, duration) or auto_acquire(t, duration) ).
Accounts that have never been acquired are treated as having the oldest possible last-used time (i.e., they should be preferred over accounts that have been used more recently).
If at least one account is available:
Select the least-recently-used available account.
Lock it for [t, t + duration) as in Part 2.
Return its account_id .
If no accounts are available at time t , return None (or a sentinel value indicating failure).
Your task:

Design the internal data structures and implement the three methods:
is_available(account_id, t)
acquire(account_id, t, duration)
auto_acquire(t, duration)
Ensure that all methods are efficient for large numbers of accounts and large numbers of operations.
Assume all calls are sequential and timestamps are non-decreasing.
