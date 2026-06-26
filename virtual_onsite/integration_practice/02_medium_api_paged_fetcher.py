"""
STRIPE INTEGRATION PRACTICE 02: API Paged Fetcher with Rate Limiting (MEDIUM)
=============================================================================

PROBLEM DESCRIPTION:
Stripe's APIs support paginated list views.
Your task is to write a client function to fetch all charges from a paginated API endpoint, 
filter them by date range, and handle API rate limits (HTTP 429).

Your function should look like this:
`fetch_charges_in_range(api_url, api_token, start_date_str, end_date_str)`

API Details:
1. Headers required: `{"Authorization": "Bearer <api_token>"}`.
2. Supports query parameters `limit` (max per page) and `starting_after` (cursor ID of last item).
3. JSON Response format:
   ```json
   {
       "data": [
           {"id": "ch_1", "amount": 500, "created_date": "2022-06-01"},
           {"id": "ch_2", "amount": 800, "created_date": "2022-06-02"}
       ],
       "has_more": true
   }
   ```
4. Rate Limiting:
   If the API returns a status code of `429`, your code must sleep for `1 second` and retry the request.

Tasks:
1. Page through all results using the cursor-based `starting_after` parameter.
2. Handle HTTP 429 rate limit errors (retry after sleeping 1 second).
3. Filter charges where `created_date` falls in the inclusive range `[start_date_str, end_date_str]`.
4. Return a list of dictionaries representing the filtered charges.
"""

import time
import requests
from datetime import datetime

# ===================================================================
# MOCK SERVER (Do not modify this section)
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

_req_count = 0
def mock_get(url, headers=None, params=None, timeout=None):
    global _req_count
    _req_count += 1
    
    # Check Token
    auth = headers.get("Authorization") if headers else None
    if auth != "Bearer stripe_integration_token":
        return MockResponse({"error": "Unauthorized"}, 401)
        
    # Simulate Rate Limit on every 3rd request
    if _req_count % 3 == 0:
        return MockResponse({"error": "Rate limit exceeded"}, 429)
        
    # Mock database
    db = [
        {"id": "ch_1", "amount": 1000, "created_date": "2022-06-01"},
        {"id": "ch_2", "amount": 2000, "created_date": "2022-06-05"},
        {"id": "ch_3", "amount": 1500, "created_date": "2022-06-10"},
        {"id": "ch_4", "amount": 3000, "created_date": "2022-06-15"},
        {"id": "ch_5", "amount": 500,  "created_date": "2022-06-20"}
    ]
    
    limit = params.get("limit", 2) if params else 2
    starting_after = params.get("starting_after") if params else None
    
    start_idx = 0
    if starting_after:
        for idx, item in enumerate(db):
            if item["id"] == starting_after:
                start_idx = idx + 1
                break
                
    end_idx = start_idx + limit
    page_data = db[start_idx:end_idx]
    has_more = end_idx < len(db)
    
    return MockResponse({"data": page_data, "has_more": has_more}, 200)

requests.get = mock_get


# ===================================================================
# STARTER CODE
# ===================================================================
def fetch_charges_in_range(api_url, api_token, start_date_str, end_date_str):
    try:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
    except ValueError as e:
        raise ValueError(f"Invalid date boundary format: {e}")
        
    headers = {"Authorization": f"Bearer {api_token}"}
    res = requests.get(url=api_url, headers=headers)
    data = res.json()
    
    result = []
    charges = data.get("data", []) if isinstance(data, dict) else []
    for charge in charges:
        created_date_str = charge.get("created_date")
        if not created_date_str:
            continue
        try:
            created_date = datetime.strptime(created_date_str, '%Y-%m-%d')
        except ValueError:
            continue
        if start_date <= created_date <= end_date:
            result.append(charge)
            
    return result





# ===================================================================
# TEST SUITE (Run this file to verify your solution)
# ===================================================================
if __name__ == "__main__":
    url = "https://api.stripe.mock/v1/charges"
    token = "stripe_integration_token"
    start_date = "2022-06-05"
    end_date = "2022-06-15"
    
    # Should match: ch_2(2022-06-05), ch_3(2022-06-10), ch_4(2022-06-15)
    expected_ids = ["ch_2", "ch_3", "ch_4"]
    
    result = fetch_charges_in_range(url, token, start_date, end_date)
    print("Your output:", result)
    
    if result:
        res_ids = [item["id"] for item in result]
        if res_ids == expected_ids:
            print("SUCCESS: Integration Problem 02 Passed!")
        else:
            print("FAIL: Result IDs do not match. Expected", expected_ids, "but got", res_ids)
    else:
        print("FAIL: No result returned.")
