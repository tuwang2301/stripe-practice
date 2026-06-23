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

### A. Programming Exercise (60 mins)
* **What it is**: A progressive, multi-part coding problem where requirements evolve step-by-step.
* **AI-Enabled Variant**: You will use HackerRank's AI Coding Environment with an in-IDE assistant.
* **Strategy**:
  - **Plan before prompting**: Don't jump in cold. Design the data structures first, then direct the AI to implement them.
  - **Critical Oversight**: Actively push back on over-engineered AI solutions. Scrutinize the code for logic flaws.
  - **Incremental Testing**: Run your code after each small change. Ensure Part 1 is 100% correct before moving to Part 2.

### B. Integration (60 mins)
* **What it is**: Writing code inside a larger, pre-existing system and integrating with external libraries.
* **Strategy**:
  - **Read the spec and docs**: Spend the first 5 minutes carefully reading the provided documentation.
  - **Protect the system**: Ensure that your integrations do not break existing functionality. Run regression tests.
  - **Familiarity with HTTP/JSON**: Be prepared to parse JSON, make requests, or interact with basic API responses if needed.

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
