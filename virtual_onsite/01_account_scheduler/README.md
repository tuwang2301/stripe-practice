# Problem 1: Account Scheduler (Stateful Class & LRU Cache)

Design a class `AccountScheduler` that manages the time-based availability of a fixed set of account IDs.

## Class Interface

### 1. Initialization
`AccountScheduler(accounts, locked_until)`
- `accounts`: a list of integers representing all account IDs in the system.
- `locked_until`: a dictionary mapping `account_id` → integer timestamp.
- If an account is not in `locked_until`, its default availability start time is `0`.

### 2. Availability Queries
`is_available(account_id, t) -> bool`
- Returns whether `account_id` is available at time `t`.
- An account is unavailable (locked) if `t < locked_until[account_id]`.
- It is available if `t >= locked_until[account_id]`.

### 3. Explicit Acquire
`acquire(account_id, t, duration) -> bool`
- Attempts to acquire/lock a specific account for a duration starting at time `t`.
- If the account is not available at time `t` (i.e. `t < locked_until[account_id]`), return `False`.
- Otherwise, update its locked time to:
  `locked_until[account_id] = max(locked_until[account_id], t) + duration`
  and return `True`.
- The successfully acquired account becomes the **most recently used** (MRU) account.

### 4. Auto-Acquire with LRU Policy
`auto_acquire(t, duration) -> Optional[account_id]`
- Finds all accounts that are available at time `t`.
- Selects the **least recently used** (LRU) available account.
- "Last used" is the last time the account was successfully acquired (either via `acquire` or `auto_acquire`).
- Accounts that have never been acquired are treated as having the oldest possible last-used time (and thus are preferred).
- Locks the selected account and returns its ID. If no accounts are available, returns `None`.

Assume all calls are sequential and timestamps are non-decreasing.
