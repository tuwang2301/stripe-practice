"""
STRIPE INTEGRATION PRACTICE 04: Subscription Billing Sync (MEDIUM)
==================================================================

PROBLEM DESCRIPTION:
Stripe Billing manages customer subscriptions. Occasionally, subscription charges fail
because a customer's payment method has expired or been removed.

Your task is to write a sync function to:
1. Fetch all active subscriptions from a paginated GET `/v1/subscriptions` endpoint.
2. For each active subscription, look up the customer's payment method status from GET `/v1/customers/{customer_id}`.
3. If the customer does NOT have an active payment method (`has_active_payment_method == False`), update the subscription's status to `"past_due"` by making a POST request to `/v1/subscriptions/{subscription_id}` with the JSON payload `{"status": "past_due"}`.
4. Return a tuple: `(total_active_processed, total_past_due_updated)`.

If any HTTP request encounters a rate limit (HTTP 429), sleep for 1 second and retry.
If any request encounters a catastrophic failure (other 4xx/5xx HTTP codes), print/log the error, skip that record, and continue processing the rest.

Your function signature:
`sync_subscription_billing(api_url, api_token)`

API Endpoints:
1. GET `/v1/subscriptions`
   - Query params: `limit` (default 2), `starting_after` (cursor ID).
   - Response:
     ```json
     {
       "data": [
         {"id": "sub_101", "customer_id": "cust_888", "status": "active"},
         {"id": "sub_102", "customer_id": "cust_999", "status": "active"}
       ],
       "has_more": false
     }
     ```
2. GET `/v1/customers/{customer_id}`
   - Response:
     ```json
     {
       "id": "cust_888",
       "email": "alex@example.com",
       "has_active_payment_method": true
     }
     ```
3. POST `/v1/subscriptions/{subscription_id}`
   - Headers: `Content-Type: application/json`
   - JSON Payload: `{"status": "past_due"}`
   - Response:
     ```json
     {
       "id": "sub_102",
       "customer_id": "cust_999",
       "status": "past_due"
     }
     ```
"""

import time
import requests

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
_sub_db = {
    "sub_1": {"id": "sub_1", "customer_id": "cust_1", "status": "active"},
    "sub_2": {"id": "sub_2", "customer_id": "cust_2", "status": "active"},
    "sub_3": {"id": "sub_3", "customer_id": "cust_3", "status": "active"},
    "sub_4": {"id": "sub_4", "customer_id": "cust_4", "status": "active"}
}
_cust_db = {
    "cust_1": {"id": "cust_1", "has_active_payment_method": True},
    "cust_2": {"id": "cust_2", "has_active_payment_method": False}, # needs update
    "cust_3": {"id": "cust_3", "has_active_payment_method": True},
    "cust_4": {"id": "cust_4", "has_active_payment_method": False}  # needs update
}

def mock_request(method, url, headers=None, params=None, json=None, timeout=None):
    global _req_count
    _req_count += 1
    
    # Check Token
    auth = headers.get("Authorization") if headers else None
    if auth != "Bearer stripe_billing_sync_token":
        return MockResponse({"error": "Unauthorized"}, 401)
        
    # Simulate Rate Limit on every 5th request
    if _req_count % 5 == 0:
        return MockResponse({"error": "Rate limit exceeded"}, 429)
        
    # GET /v1/subscriptions
    if method == "GET" and url.endswith("/v1/subscriptions"):
        limit = params.get("limit", 2) if params else 2
        starting_after = params.get("starting_after") if params else None
        
        db_list = list(_sub_db.values())
        start_idx = 0
        if starting_after:
            for idx, item in enumerate(db_list):
                if item["id"] == starting_after:
                    start_idx = idx + 1
                    break
                    
        end_idx = start_idx + limit
        page_data = db_list[start_idx:end_idx]
        has_more = end_idx < len(db_list)
        return MockResponse({"data": page_data, "has_more": has_more}, 200)
        
    # GET /v1/customers/{customer_id}
    if method == "GET" and "/v1/customers/" in url:
        customer_id = url.split("/v1/customers/")[-1]
        if customer_id in _cust_db:
            return MockResponse(_cust_db[customer_id], 200)
        return MockResponse({"error": "Customer not found"}, 404)
        
    # POST /v1/subscriptions/{subscription_id}
    if method == "POST" and "/v1/subscriptions/" in url:
        sub_id = url.split("/v1/subscriptions/")[-1]
        if sub_id not in _sub_db:
            return MockResponse({"error": "Subscription not found"}, 404)
            
        status = json.get("status") if json else None
        if status == "past_due":
            _sub_db[sub_id]["status"] = "past_due"
            return MockResponse(_sub_db[sub_id], 200)
        return MockResponse({"error": "Invalid payload"}, 400)
        
    return MockResponse({"error": "Not Found"}, 404)

requests.get = lambda url, **kwargs: mock_request("GET", url, **kwargs)
requests.post = lambda url, **kwargs: mock_request("POST", url, **kwargs)


# ===================================================================
# STARTER CODE
# ===================================================================
def sync_subscription_billing(api_url, api_token):
    # WRITE YOUR CODE HERE
    pass


# ===================================================================
# TEST SUITE (Run this file to verify your solution)
# ===================================================================
if __name__ == "__main__":
    url = "https://api.stripe.mock"
    token = "stripe_billing_sync_token"
    
    # Run sync function
    try:
        processed, updated = sync_subscription_billing(url, token)
        print(f"Your output -> Processed: {processed}, Updated: {updated}")
        
        # Verify sub_2 and sub_4 are updated to past_due, while sub_1 and sub_3 remain active
        if processed == 4 and updated == 2:
            if _sub_db["sub_2"]["status"] == "past_due" and _sub_db["sub_4"]["status"] == "past_due" and \
               _sub_db["sub_1"]["status"] == "active" and _sub_db["sub_3"]["status"] == "active":
                print("SUCCESS: Integration Problem 04 Passed!")
            else:
                print("FAIL: Subscription statuses in DB do not match expected outcomes.")
        else:
            print(f"FAIL: Expected (4, 2) but got ({processed}, {updated})")
    except Exception as e:
        print("FAIL: Raised an error during execution:", e)
        import traceback
        traceback.print_exc()
