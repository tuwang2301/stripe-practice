"""
STRIPE PRACTICE PROBLEM 03: Cursor-Based API Pagination Integrator (HARD)
======================================================================

PROBLEM DESCRIPTION:
Stripe's Integration round simulates working with third-party or Stripe APIs.
For this problem, you need to integrate with a mock Customer API.

Your task is to implement a function:
`fetch_and_filter_customers(api_url, api_token, created_after_timestamp, report_file_path)`

API Specifications:
1. HTTP GET requests to `api_url` require the Header:
   `{"Authorization": "Bearer <api_token>"}`
2. The endpoint supports pagination query parameters:
   - `limit`: The number of items to return per page (max 100).
   - `starting_after`: A cursor ID representing the last item from the previous page.
3. Response JSON structure:
   ```json
   {
       "data": [
           {"id": "cus_1", "email": "a@gmail.com", "created": 1000},
           {"id": "cus_2", "email": "b@gmail.com", "created": 1200}
       ],
       "has_more": true
   }
   ```
4. Rate Limiting:
   The mock API server may return a `429 Too Many Requests` status code. 
   When this happens, your code must sleep for `1 second` and retry the request.
5. Authorization:
   If the API token is incorrect, the server returns a `401 Unauthorized`.

Tasks to perform in the function:
1. Make HTTP GET requests to retrieve ALL customers from the paginated API.
2. Filter the customers to only include those created strictly after `created_after_timestamp`.
3. Write the filtered customers to `report_file_path` in CSV format:
   `customer_id,email,created_timestamp`
4. Return the count of filtered customers.

MOCK ENVIRONMENT:
To make this run locally without internet access, we have provided a mocked `requests.get`
below that simulates pagination, rate-limiting, and authentication.
Your solution should use `requests.get` as if it were the real library.
"""

import time
import requests
import json

# ===================================================================
# MOCK SERVER (Do not modify this class, it simulates the Stripe API)
# ===================================================================
class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code
    
    def json(self):
        return self.json_data
        
    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.exceptions.HTTPError(f"HTTP Error: {self.status_code}")

_request_count = 0
def mock_get(url, headers=None, params=None, timeout=None):
    global _request_count
    _request_count += 1
    
    # Check Token
    auth_header = headers.get("Authorization") if headers else None
    if auth_header != "Bearer stripe_onsite_token":
        return MockResponse({"error": "Unauthorized"}, 401)
        
    # Simulate Rate Limit on every 3rd request
    if _request_count % 3 == 0:
        return MockResponse({"error": "Rate limit exceeded"}, 429)
        
    # Mock Customer Database
    customers_db = [
        {"id": "cus_1", "email": "alice@gmail.com", "created": 100},
        {"id": "cus_2", "email": "bob@gmail.com", "created": 150},
        {"id": "cus_3", "email": "charlie@gmail.com", "created": 200},
        {"id": "cus_4", "email": "david@gmail.com", "created": 250},
        {"id": "cus_5", "email": "emma@gmail.com", "created": 300}
    ]
    
    limit = params.get("limit", 2) if params else 2
    starting_after = params.get("starting_after") if params else None
    
    start_idx = 0
    if starting_after:
        for idx, cus in enumerate(customers_db):
            if cus["id"] == starting_after:
                start_idx = idx + 1
                break
                
    end_idx = start_idx + limit
    page_data = customers_db[start_idx:end_idx]
    has_more = end_idx < len(customers_db)
    
    return MockResponse({"data": page_data, "has_more": has_more}, 200)

# Override requests.get with our mock for local testing
requests.get = mock_get


# ===================================================================
# STARTER CODE
# ===================================================================
def fetch_and_filter_customers(api_url, api_token, created_after_timestamp, report_file_path):
    # WRITE YOUR CODE HERE
    # Remember to:
    # 1. Loop through all pages using cursor-based pagination ('starting_after')
    # 2. Check for HTTP status code 429, sleep 1 second, and retry.
    # 3. Handle errors and raise_for_status().
    # 4. Filter by created > created_after_timestamp.
    # 5. Write to report_file_path in CSV format.
    # 6. Return the count of filtered customers.
    pass


# ===================================================================
# TEST SUITE (Run this file to verify your solution)
# ===================================================================
if __name__ == "__main__":
    url = "https://api.stripe.mock/v1/customers"
    token = "stripe_onsite_token"
    created_after = 180 # Should match: cus_3(200), cus_4(250), cus_5(300)
    report_file = "filtered_customers.csv"
    
    result = fetch_and_filter_customers(url, token, created_after, report_file)
    print("Filtered Customer Count:", result)
    
    if result == 3:
        # Check file content
        try:
            with open(report_file, 'r') as f:
                content = f.read().strip().split('\n')
                print("Generated File Contents:")
                for line in content:
                    print("  ", line)
                
                expected_lines = [
                    "cus_3,charlie@gmail.com,200",
                    "cus_4,david@gmail.com,250",
                    "cus_5,emma@gmail.com,300"
                ]
                
                # Check line by line
                if content == expected_lines:
                    print("SUCCESS: Practice Problem 03 Passed!")
                else:
                    print("FAIL: File content does not match expected lines.")
        except Exception as e:
            print("FAIL: Could not read generated report file:", e)
    else:
        print("FAIL: Expected count 3 but got", result)
