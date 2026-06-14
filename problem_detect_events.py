from collections import *
import math

def solution(logs, window_size, threshold):
    # Monitor (merchant_id, status_code)
    merchant_status = defaultdict(list)
    for l in logs:
        (timestamp, merchant_id, status_code, count) = l
        merchant_status[(merchant_id, status_code)].append((timestamp, count))

    result = []
    for key, value in merchant_status.items():
        (merchant_id, status_code) = key
        rolling_sum = 0
        triggered = False
        window = deque()

        for timestamp, count in value:
            cutoff = timestamp - window_size + 1

            while window and window[0][0] < cutoff:
                rolling_sum -= window.popleft()[1]

            window.append((timestamp, count))
            rolling_sum += count

            if not triggered and rolling_sum >= threshold:
                result.append((timestamp, merchant_id, status_code, 'TRIGGER'))
                triggered = True
            elif triggered and rolling_sum < threshold:
                result.append((timestamp, merchant_id, status_code, 'RESOLVE'))
                triggered = False        
                
    return result 
    pass    
    


if __name__ == "__main__":
    # logs = [(1, 'A', 404, 2), (1, 'A', 404, 1), (2, 'B', 500, 3), (3, 'A', 404, 1), (4, 'B', 500, 1)]
    logs = [(1, 'm1', 500, 2), (2, 'm1', 500, 2), (5, 'm1', 500, 1), (6, 'm1', 500, 1)]
    window_size = 3
    threshold = 4

    result = solution(logs=logs, window_size=window_size, threshold=threshold)
    print(result)
