from collections import defaultdict, deque

def solution(logs, window_size, threshold):
    # Group logs by (merchant_id, status_code) but keep their original index
    merchant_status = defaultdict(list)
    for idx, log in enumerate(logs):
        (timestamp, merchant_id, status_code, count) = log
        merchant_status[(merchant_id, status_code)].append((timestamp, count, idx))

    events = []
    for (merchant_id, status_code), logs_list in merchant_status.items():
        rolling_sum = 0
        triggered = False
        window = deque()

        for timestamp, count, idx in logs_list:
            cutoff = timestamp - window_size + 1

            # Remove elements outside the window
            while window and window[0][0] < cutoff:
                rolling_sum -= window.popleft()[1]

            # Add current log to the window
            window.append((timestamp, count))
            rolling_sum += count

            # Evaluate events
            if not triggered and rolling_sum >= threshold:
                events.append((timestamp, merchant_id, status_code, 'TRIGGER', idx))
                triggered = True
            elif triggered and rolling_sum < threshold:
                events.append((timestamp, merchant_id, status_code, 'RESOLVE', idx))
                triggered = False

    # Sort events by timestamp, and then by the original input index of the log that caused them
    events.sort(key=lambda x: (x[0], x[4]))
    
    # Remove the index from the output tuples
    return [(t, m, s, e) for t, m, s, e, idx in events]
