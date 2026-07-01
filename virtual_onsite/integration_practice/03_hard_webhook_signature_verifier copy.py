"""
STRIPE INTEGRATION PRACTICE 03: Webhook Signature Verifier (HARD)
================================================================

PROBLEM DESCRIPTION:
Stripe signs webhook events sent to your server.
To verify that the event was actually sent by Stripe, you must check the signature in the header.

You are given:
- `webhook_payload`: The raw string payload received from the webhook request.
- `signature_header`: The value of the `Stripe-Signature` header, formatted as:
  `t=1656000000,v1=6d73f4e...` where `t` is the timestamp and `v1` is the HMAC signature.
- `secret`: The shared webhook signing secret.
- `current_time_epoch`: The current timestamp (integer seconds) to verify expiration.
- `max_drift_seconds`: The maximum time difference in seconds allowed between `t` and `current_time_epoch` (default: 300 seconds).

Tasks to perform:
1. Parse the `signature_header` to extract the timestamp `t` (as an integer) and the signature `v1`.
2. Check if the timestamp is expired: if `current_time_epoch - t > max_drift_seconds`, return `False` (Replay Attack prevention).
3. Compute the expected signature:
   - Prepare the signature payload: `t_string + "." + webhook_payload` (e.g. `"1656000000.{"id":"evt_1"}"`).
   - Calculate the HMAC-SHA256 signature of this payload using the `secret` key.
   - You must encode both the key and the payload to bytes using UTF-8 before passing them to the HMAC function.
4. Compare the computed signature to `v1`.
   - Security Tip: Use `hmac.compare_digest` instead of `==` to prevent timing attacks.
5. Return `True` if the signature is valid and not expired, otherwise return `False`.
"""

import hmac
import hashlib

def verify_webhook_signature(webhook_payload, signature_header, secret, current_time_epoch, max_drift_seconds=300):
    if not signature_header or not isinstance(signature_header, str):
        return False
        
    t_string = None
    v1 = None
    
    # Parsing the signature header dynamically
    parts = signature_header.split(',')
    for part in parts:
        if '=' not in part:
            continue
        key, val = part.split('=', 1)
        key = key.strip()
        val = val.strip()
        if key == 't':
            t_string = val
        elif key == 'v1':
            v1 = val
            
    if t_string is None or v1 is None:
        return False

    
    # Check timestamp
    if current_time_epoch - int(t_string) > max_drift_seconds:
        return False
    
    # Prepare signature payload
    signature_payload = t_string + '.' + webhook_payload

    # Calculate signature
    signature = hmac.new(secret.encode('utf-8'), signature_payload.encode('utf-8'), hashlib.sha256).hexdigest()

    #Return Output
    return hmac.compare_digest(signature, v1)


# ===================================================================
# TEST SUITE (Run this file to verify your solution)
# ===================================================================
if __name__ == "__main__":
    secret = "whsec_test_secret"
    payload = '{"id":"evt_100","type":"charge.succeeded"}'
    timestamp = 1656000000
    
    # Compute valid signature for testing:
    # signed_payload = "1656000000.{"id":"evt_100","type":"charge.succeeded"}"
    signed_payload = f"{timestamp}.{payload}"
    valid_sig = hmac.new(
        secret.encode('utf-8'),
        signed_payload.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    
    header = f"t={timestamp},v1={valid_sig}"
    
    # Test case 1: Valid signature within drift window (t=1656000000, current=1656000100 -> drift = 100)
    print("Test 1 (Expected True):", verify_webhook_signature(payload, header, secret, 1656000100))
    
    # Test case 2: Expired signature (t=1656000000, current=1656000400 -> drift = 400 > 300)
    print("Test 2 (Expected False - Expired):", verify_webhook_signature(payload, header, secret, 1656000400))
    
    # Test case 3: Invalid signature (wrong payload)
    print("Test 3 (Expected False - Wrong Payload):", verify_webhook_signature('{"id":"evt_999"}', header, secret, 1656000100))
    
    # Verification
    if (verify_webhook_signature(payload, header, secret, 1656000100) == True and
        verify_webhook_signature(payload, header, secret, 1656000400) == False and
        verify_webhook_signature('{"id":"evt_999"}', header, secret, 1656000100) == False):
        print("SUCCESS: Integration Problem 03 Passed!")
    else:
        print("FAIL: Verification failed.")
