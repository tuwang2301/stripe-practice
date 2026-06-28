"""
STRIPE INTEGRATION PRACTICE 02B: Paginated Invoice Aggregator (PRACTICE)
========================================================================

PROBLEM DESCRIPTION:
Stripe's billing system generates paginated lists of invoices.
Your task is to write a client function to fetch all invoices from a paginated API endpoint,
filter them based on target criteria, and calculate the total sum of their amounts in cents.

Your function should look like this:
`aggregate_invoices(api_url, api_token, target_currency, start_epoch, end_epoch)`

API Details:
1. Headers required: `{"Authorization": "Bearer <api_token>"}`.
2. Supports query parameters `limit` (max per page) and `starting_after` (cursor ID of last item).
3. JSON Response format:
   ```json
   {
       "data": [
           {"id": "in_1", "amount_cents": 5000, "currency": "usd", "status": "paid", "created_epoch": 1656000000},
           {"id": "in_2", "amount_cents": 3000, "currency": "eur", "status": "open", "created_epoch": 1656000100}
       ],
       "has_more": true
   }
   ```
4. Rate Limiting:
   If the API returns a status code of `429`, your code must sleep for `1 second` and retry the request.

Tasks:
1. Page through all invoices using the cursor-based `starting_after` parameter.
2. Handle HTTP 429 rate limit errors defensively (retry after sleeping 1 second).
3. Filter invoices where:
   - `currency` matches `target_currency` (case-insensitive).
   - `status` is exactly `"paid"`.
   - `created_epoch` falls in the inclusive range `[start_epoch, end_epoch]`.
4. Calculate the sum of `amount_cents` for the filtered invoices.
5. Return a tuple: `(invoice_count, total_amount_cents)` representing the count of matching invoices and their total sum.
   If any API request fails catastrophically (non-429 error), log it and return `(0, 0)`.
"""

import time
import requests
import json

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
    if auth != "Bearer stripe_billing_token":
        return MockResponse({"error": "Unauthorized"}, 401)
        
    # Simulate Rate Limit on every 4th request
    if _req_count % 4 == 0:
        return MockResponse({"error": "Rate limit exceeded"}, 429)
        
    # Mock database
    db = [
        {"id": "in_1", "amount_cents": 10000, "currency": "usd", "status": "paid", "created_epoch": 1656000000},
        {"id": "in_2", "amount_cents": 5000,  "currency": "eur", "status": "paid", "created_epoch": 1656000100},
        {"id": "in_3", "amount_cents": 15000, "currency": "usd", "status": "open", "created_epoch": 1656000200}, # unpaid
        {"id": "in_4", "amount_cents": 25000, "currency": "USD", "status": "paid", "created_epoch": 1656000300},
        {"id": "in_5", "amount_cents": 8000,  "currency": "usd", "status": "paid", "created_epoch": 1656000900}  # out of time range
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
def aggregate_invoices(api_url, api_token, target_currency, start_epoch, end_epoch):
    target_currency = target_currency.lower()
    headers = {"Authorization": f"Bearer {api_token}"}
    res = requests.get(api_url, headers=headers)
    data = res.json()
    count = 0
    total_amount = 0
    invoices = data.get("data", [])
    for inv in invoices:
        currency = inv.get("currency", "").lower()
        status = inv.get("status")
        created_epoch = inv.get("created_epoch", 0)
        amount_cents = inv.get("amount_cents", 0)
        
        if (currency == target_currency and 
            status == "paid" and 
            start_epoch <= created_epoch <= end_epoch):
            count += 1
            total_amount += amount_cents
    return (count, total_amount)


# ===================================================================
# TEST SUITE (Run this file to verify your solution)
# ===================================================================
if __name__ == "__main__":
    url = "https://api.stripe.mock/v1/invoices"
    token = "stripe_billing_token"
    currency = "usd"
    start_time = 1656000000
    end_time = 1656000500
    
    # Expected matches: 
    # - in_1 (usd, paid, t=1656000000) -> 10000 cents
    # - in_4 (USD, paid, t=1656000300) -> 25000 cents
    # Total count = 2, Total sum = 35000 cents
    
    count, total_cents = aggregate_invoices(url, token, currency, start_time, end_time)
    print(f"Your output -> Count: {count}, Total Cents: {total_cents}")
    
    if count == 2 and total_cents == 35000:
        print("SUCCESS: Integration Problem 02B Passed!")
    else:
        print(f"FAIL: Expected (2, 35000) but got ({count}, {total_cents})")
