# Stripe Virtual Onsite Preparation Strategy Guide

Preparing for the Stripe Software Engineer Virtual Onsite requires shifting your focus from competitive programming (LeetCode) to **practical software engineering and design**. This guide provides an actionable preparation plan based on the official guidelines.

---

## 1. Core Principles of Stripe Coding Interviews

Stripe evaluates you based on the work you would do on the job. The engineering bar is high, but it prioritizes:
1. **Correctness & Robustness**: Does the code work for all edge cases? Can you prove it is correct using manual tests or assertions?
2. **Readability & Clean Code**: Is your code simple and maintainable? Do you use clear naming and follow idiomatic practices of your chosen language (e.g. Python)?
3. **Communication**: Stripe interviewers are **collaborators**. Talk out loud, explain your design decisions, state your hypotheses when debugging, and ask clarifying questions before writing code.
4. **Tooling Familiarity**: You should be highly productive in your editor, know how to run and debug code, and use standard libraries (like `collections.defaultdict`, `collections.deque`, `collections.OrderedDict`, etc.) effortlessly.

---

## 2. Onsite Interview Formats

### A. AI Programming Exercise (60 mins)
* **What it is**: Replaces the traditional programming screening exercise. You work on a progressive, multi-part problem using HackerRank's AI Coding environment with a built-in assistant (often a basic/less-capable model).
* **Language & Setup**: You pre-select your preferred language. Searching Google for syntax is fully allowed.
* **Strategy**:
  - **Collaborate, Don't Outsource**: Treat the AI like a junior developer. Do not dump the whole prompt and ask it to write the code. Instead, explain your architectural idea and ask the AI to verify it first.
  - **Verify Before Coding**: Tell the AI: *"I plan to use a hash map for tracking and a queue for time windows. Does this approach have any edge cases?"*
  - **Incremental Growth**: Instruct the AI to write small helper functions. Verify and test Part 1 completely before asking the AI to adapt the code for Part 2.

### B. Integration (60 mins)
* **What it is**: The interviewer provides a pre-configured local environment and task description. You must call external or simulated APIs, fetch data, manipulate/process that data, and return/report results.
* **Language & Setup**: Same as above (pre-selected language, Google searching for syntax allowed).
* **Strategy**:
  - **Trace the API Flow**: Skim the API specification and mock URLs for the first 3-5 minutes.
  - **Handle Network Realities**: Always write defensive code for HTTP failures, handle pagination (cursor-based), and handle rate limits (e.g. sleep 1s on HTTP 429).
  - **Check CSV/JSON formatting**: Make sure to use standard modules (`csv`, `json`) rather than manual string formats to handle special characters cleanly.


### C. Bug Squash (60 mins - New Grad Only)
* **What it is**: Navigating a large, unfamiliar codebase (typically an open-source project) to find and fix bugs.
* **Strategy**:
  - **Formulate a hypothesis**: Don't aimlessly scan files. Make a hypothesis based on failing tests, run tests, and narrow down the codebase systematically.
  - **Tooling**: Ensure you know how to use print statements, debuggers, or grep search to locate functions quickly.
  - **Explain what the code does**: Show that you understand the architecture of the project before writing the fix.

---

## 3. Practice Problems in this Folder

We have prepared 4 advanced, stateful coding problems mimicking the Stripe onsite format:

1. **`01_account_scheduler`**: Combines stateful class design, time-interval availability tracking, and LRU eviction policy using `collections.OrderedDict`.
2. **`02_find_linked_users`**: Focuses on entity resolution, building undirected graphs, and calculating transitive closures using DFS/BFS.
3. **`03_detect_trigger_resolve`**: Telecom/telemetry telemetry alerts requiring double-ended queues (`collections.deque`) and sliding window aggregations.
4. **`04_payment_to_invoice`**: Business logic problem with priority-based matching (matching exact amounts, tie-breaking by dates/ID, and forgiveness-range matching).

---

## 4. Progressive Practice Labs

To prepare step-by-step, use our curated training tracks under `virtual_onsite/`:

### A. Programming Exercise Practice Track
* **[01_easy_payment_validations.py](file:///D:/Projects/stripe-practice/virtual_onsite/programming_practice/01_easy_payment_validations.py)**: Basic CSV transaction validation logic.
* **[02_medium_dispute_tracker.py](file:///D:/Projects/stripe-practice/virtual_onsite/programming_practice/02_medium_dispute_tracker.py)**: Stateful class to process disputes and compute merchant risks with priority logic.
* **[03_hard_event_telemetry.py](file:///D:/Projects/stripe-practice/virtual_onsite/programming_practice/03_hard_event_telemetry.py)**: Time-series sliding window state updates.

### B. Integration & API Practice Track
* **[01_easy_json_logger.py](file:///D:/Projects/stripe-practice/virtual_onsite/integration_practice/01_easy_json_logger.py)**: Basic JSON log parser outputting clean CSV files.
* **[01_b_defensive_log_converter.py](file:///D:/Projects/stripe-practice/virtual_onsite/integration_practice/01_b_defensive_log_converter.py)**: Advanced defensive parser demonstrating standard `csv` write safety and timestamp exception handling.
* **[02_medium_api_paged_fetcher.py](file:///D:/Projects/stripe-practice/virtual_onsite/integration_practice/02_medium_api_paged_fetcher.py)**: API client implementing cursor pagination and HTTP 429 rate limit retries.
* **[03_hard_webhook_signature_verifier.py](file:///D:/Projects/stripe-practice/virtual_onsite/integration_practice/03_hard_webhook_signature_verifier.py)**: Webhook parser executing header validation and cryptographic signature verification.
* **[04_medium_subscription_billing_sync.py](file:///D:/Projects/stripe-practice/virtual_onsite/integration_practice/04_medium_subscription_billing_sync.py)**: Subscription sync engine retrieving data from paged active subscriptions and updating customer statuses via POST.
* **[05_hard_multi_currency_payout_reconciler.py](file:///D:/Projects/stripe-practice/virtual_onsite/integration_practice/05_hard_multi_currency_payout_reconciler.py)**: Payout reconciler fetching transaction records via queries, evaluating totals, and triggering reconcile/flag status updates.


