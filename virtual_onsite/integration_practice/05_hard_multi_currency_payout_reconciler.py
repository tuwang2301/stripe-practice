"""
STRIPE INTEGRATION PRACTICE 05: Multi-currency Payout Reconciler (HARD)
========================================================================

PROBLEM DESCRIPTION:
Stripe reconciles payouts (transfers of funds to a merchant's bank account) against individual charge transactions.

Your task is to write a reconciler function to:
1. Fetch all pending payouts from GET `/v1/payouts`.
2. For each payout:
   - Query GET `/v1/transactions?payout_id={payout_id}` to fetch its associated transaction records.
   - Sum the `amount` of all associated transactions.
   - If the sum of transaction amounts matches the payout `amount`:
     - Send a POST request to `/v1/payouts/{payout_id}/reconcile` (empty body) to mark it as reconciled.
     - Increment the `"reconciled"` count.
   - If the sum does NOT match the payout `amount` (or there are no transactions):
     - Send a POST request to `/v1/payouts/{payout_id}/flag` with the JSON payload `{"reason": "amount_mismatch"}`.
     - Increment the `"flagged"` count.
3. Return a dictionary with the summary of actions taken:
   ```json
   {"reconciled": X, "flagged": Y}
   ```

If any HTTP request encounters a rate limit (HTTP 429), sleep for 1 second and retry.
If any request encounters a catastrophic failure (other 4xx/5xx HTTP codes), print/log the error, skip that payout, and continue.

Your function signature:
`reconcile_payouts(api_url, api_token)`

API Endpoints:
1. GET `/v1/payouts`
   - Response:
     ```json
     {
       "data": [
         {"id": "po_101", "amount": 10000, "currency": "usd", "status": "pending"},
         {"id": "po_102", "amount": 25000, "currency": "eur", "status": "pending"}
       ]
     }
     ```
2. GET `/v1/transactions?payout_id={payout_id}`
   - Response:
     ```json
     {
       "data": [
         {"id": "txn_1", "amount": 4000},
         {"id": "txn_2", "amount": 6000}
       ]
     }
     ```
3. POST `/v1/payouts/{payout_id}/reconcile`
   - Response:
     ```json
     {"id": "po_101", "status": "reconciled"}
     ```
4. POST `/v1/payouts/{payout_id}/flag`
   - Headers: `Content-Type: application/json`
   - JSON Payload: `{"reason": "amount_mismatch"}`
   - Response:
     ```json
     {"id": "po_102", "status": "flagged", "reason": "amount_mismatch"}
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
_payouts_db = {
    "po_1": {"id": "po_1", "amount": 12000, "currency": "usd", "status": "pending"},
    "po_2": {"id": "po_2", "amount": 5000,  "currency": "eur", "status": "pending"},
    "po_3": {"id": "po_3", "amount": 8500,  "currency": "usd", "status": "pending"}
}
_transactions_db = {
    "po_1": [{"id": "txn_a", "amount": 8000}, {"id": "txn_b", "amount": 4000}], # matches (8000+4000 = 12000)
    "po_2": [{"id": "txn_c", "amount": 3000}],                                 # mismatch (3000 != 5000)
    "po_3": [{"id": "txn_d", "amount": 5000}, {"id": "txn_e", "amount": 3500}]  # matches (5000+3500 = 8500)
}

def mock_request(method, url, headers=None, params=None, json=None, timeout=None):
    global _req_count
    _req_count += 1
    
    # Check Token
    auth = headers.get("Authorization") if headers else None
    if auth != "Bearer stripe_payout_reconciliation_token":
        return MockResponse({"error": "Unauthorized"}, 401)
        
    # Simulate Rate Limit on every 6th request
    if _req_count % 6 == 0:
        return MockResponse({"error": "Rate limit exceeded"}, 429)
        
    # GET /v1/payouts
    if method == "GET" and url.endswith("/v1/payouts"):
        return MockResponse({"data": list(_payouts_db.values())}, 200)
        
    # GET /v1/transactions?payout_id={payout_id}
    if method == "GET" and "/v1/transactions" in url:
        payout_id = params.get("payout_id") if params else None
        if payout_id in _transactions_db:
            return MockResponse({"data": _transactions_db[payout_id]}, 200)
        return MockResponse({"data": []}, 200)
        
    # POST /v1/payouts/{payout_id}/reconcile
    if method == "POST" and url.endswith("/reconcile"):
        payout_id = url.split("/v1/payouts/")[-1].split("/reconcile")[0]
        if payout_id in _payouts_db:
            _payouts_db[payout_id]["status"] = "reconciled"
            return MockResponse(_payouts_db[payout_id], 200)
        return MockResponse({"error": "Payout not found"}, 404)
        
    # POST /v1/payouts/{payout_id}/flag
    if method == "POST" and url.endswith("/flag"):
        payout_id = url.split("/v1/payouts/")[-1].split("/flag")[0]
        if payout_id in _payouts_db:
            reason = json.get("reason") if json else None
            _payouts_db[payout_id]["status"] = "flagged"
            _payouts_db[payout_id]["reason"] = reason
            return MockResponse(_payouts_db[payout_id], 200)
        return MockResponse({"error": "Payout not found"}, 404)
        
    return MockResponse({"error": "Not Found"}, 404)

requests.get = lambda url, **kwargs: mock_request("GET", url, **kwargs)
requests.post = lambda url, **kwargs: mock_request("POST", url, **kwargs)


# ===================================================================
# STARTER CODE
# ===================================================================
def reconcile_payouts(api_url, api_token):
    # WRITE YOUR CODE HERE
    pass


# ===================================================================
# TEST SUITE (Run this file to verify your solution)
# ===================================================================
if __name__ == "__main__":
    url = "https://api.stripe.mock"
    token = "stripe_payout_reconciliation_token"
    
    # Run reconciler
    try:
        summary = reconcile_payouts(url, token)
        print("Your output -> Summary:", summary)
        
        # Verify: po_1 and po_3 should be reconciled, po_2 should be flagged
        if isinstance(summary, dict) and summary.get("reconciled") == 2 and summary.get("flagged") == 1:
            if _payouts_db["po_1"]["status"] == "reconciled" and \
               _payouts_db["po_3"]["status"] == "reconciled" and \
               _payouts_db["po_2"]["status"] == "flagged" and \
               _payouts_db["po_2"].get("reason") == "amount_mismatch":
                print("SUCCESS: Integration Problem 05 Passed!")
            else:
                print("FAIL: Statuses in DB do not match expected outcomes.")
        else:
            print("FAIL: Expected summary {'reconciled': 2, 'flagged': 1}")
    except Exception as e:
        print("FAIL: Raised an error during execution:", e)
        import traceback
        traceback.print_exc()
