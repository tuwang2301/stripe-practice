# Stripe Intern Virtual Onsite Experience & Advice

This document summarizes key insights, tips, and preparation strategies extracted from community discussions and engineering blogs regarding the **Stripe Software Engineer Intern Virtual Onsite**. 

As an Intern candidate, your onsite will consist of **2 rounds** (60 minutes each):
1. **Programming Exercise**
2. **Integration Round**

---

## 1. Programming Exercise Round

### What to Expect
* **Not LeetCode**: This round does not test competitive programming tricks, dynamic programming, or complex tree traversals. 
* **Real-Life Scenario**: You are given a practical business scenario (similar to Stripe's Online Assessment) with input/output examples and functional requirements.
* **Progressive Multi-Part**: The problem will have 3–4 progressive parts. The interviewer will reveal Part 2 only after you complete Part 1.
* **Common Patterns**: Lots of string manipulation, parsing CSV-like records, dictionary/hash map aggregations, and state management.

### Key Advice
* **Correctness > Optimality**: Stripe interviewers care that your code works, handles edge cases, and produces the correct output. An $O(N^2)$ solution that is clean and correct is infinitely better than an $O(N)$ solution that has bugs.
* **Be Fast**: Because the problem is progressive, speed of implementation is crucial. Spend less time overthinking the "perfect" architecture and more time putting your ideas into working code.
* **Test Incrementally**: Run your code after each change. Do not move to Part 2 until you have verified Part 1 with the test cases.
* **Communicate Design Decisions**: Even though it's not a system design interview, explain why you choose certain data structures (e.g., using a map for $O(1)$ lookups).

---

## 2. Integration Round

### What to Expect
* **Simulated On-the-Job Work**: You are given a spec and documentation for an existing system or a third-party API. You must call the API, parse the results, manipulate the data, and perform basic file I/O.
* **Focus Areas**: Tích hợp (integration), reading API contracts, error handling, and managing constraints.
* **Core Concepts Tested**:
  * **Cursor-based Pagination**: Stripe's APIs typically return lists using cursor-based pagination. You will need to handle `limit`, `starting_after`, and `has_more` to traverse pages.
  * **Robust Error Handling**: Handling network timeouts, malformed payloads, and API failures.
  * **Rate Limiting (HTTP 429)**: Gracefully handling rate limits using sleep, exponential backoff, or simple retry logic.

### Key Advice
* **Familiarity with Basic Libraries**: You do **not** need to memorize documentation (you can use Google/Stack Overflow), but you must know how to quickly use standard libraries in Python:
  * **HTTP Requests**: `requests.get()`, `requests.post()`, check status codes, handle rate limits/retries.
  * **JSON/CSV Parsing**: `json.loads()`, `json.dumps()`, and splitting/stripping CSV lines.
  * **File I/O**: `open()`, reading/writing lines.
* **Read the Docs Carefully**: The integration spec contains all the rules of the API. Take 3-5 minutes at the beginning to skim the documentation before writing code.
* **Avoid Over-Engineering**: Keep your code simple. Avoid complex design patterns (like factories or abstract managers) unless they are absolutely necessary.
* **Testing is Critical**: You are integrating new code into an existing setup. Make sure you don't break the system's contract. Assert inputs/outputs early.

---

## 3. Recommended Python Cheat Sheet for the Onsite

### Handling API Cursor-Based Pagination
Stripe list APIs usually return results in page sizes (controlled by `limit`). To get the next page, you take the ID of the last object in the returned array and pass it as the `starting_after` parameter.

```python
import requests
import time

def fetch_all_paginated_data(url):
    results = []
    headers = {"Authorization": "Bearer test_key"}
    next_page_token = None
    
    while True:
        params = {"limit": 100}  # Fetch max per page (often 100 in Stripe)
        if next_page_token:
            params["starting_after"] = next_page_token
            
        try:
            response = requests.get(url, headers=headers, params=params, timeout=5)
            
            # Handle Rate Limiting (HTTP 429)
            if response.status_code == 429:
                print("Rate limited, retrying in 1 second...")
                time.sleep(1)
                continue
                
            response.raise_for_status()
            payload = response.json()
            
            data_list = payload.get("data", [])
            results.extend(data_list)
            
            # Check if there is more data
            if payload.get("has_more") and data_list:
                # Use the ID of the last item in the list as the cursor for the next page
                next_page_token = data_list[-1]["id"]
            else:
                break
        except requests.exceptions.RequestException as e:
            print(f"API Connection Error: {e}")
            break
            
    return results
```

### Safe JSON Parsing & Exception Handling
```python
import json

def safe_parse_json(json_string):
    try:
        return json.loads(json_string)
    except (json.JSONDecodeError, TypeError) as e:
        print(f"Failed to parse JSON: {e}")
        return {}
```

---

## 4. References & Additional Reading

For more details, check out these community experiences and official guidelines:
1. **Reddit Discussions**:
   - [Reddit Thread: Stripe New Grad VO Experience](https://www.reddit.com/r/csMajors/comments/1pl548f/stripe_new_grad_vo_virtual_onsite_experience/) (Source of original tips)
   - [Reddit Thread: Stripe Summer Intern 2026 VO](https://www.reddit.com/r/csMajors/comments/1qczswk/stripe_summer_intern_2026usa/)
   - [Reddit Thread: Stripe Tech Screen Rejection Reasons](https://www.reddit.com/r/csMajors/comments/1oimoz4/stripe_first_round_intern_interview/)
2. **Official Stripe Documentation**:
   - [Stripe API Reference: Pagination Guidelines](https://stripe.com/docs/api/pagination) (Details on cursor pagination using `starting_after`)
   - [Stripe API Reference: Rate Limits](https://stripe.com/docs/rate-limits) (Handling HTTP 429 and retry headers)
3. **Interview Prep Guides**:
   - [Exponent: Stripe Software Engineer Interview Course & Blog](https://www.tryexponent.com/blog/stripe-software-engineer-interview-guide) (Deep dive into the Integration & Bug Squash rounds)
   - [NorahQ Blog: Preparing for Stripe's Unique Onsite Loops](https://www.norahq.com/blog/stripe-swe-interview-preparation)
