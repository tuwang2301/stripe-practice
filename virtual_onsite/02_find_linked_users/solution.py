from collections import defaultdict, deque

def find_direct_links(rows, weights, threshold, target_user_id):
    target_user = None
    for r in rows:
        if r["id"] == target_user_id:
            target_user = r
            break

    if not target_user:
        return []

    direct_links = []
    for r in rows:
        if r["id"] == target_user_id:
            continue

        match_score = 0
        for field in weights:
            if r.get(field) == target_user.get(field):
                match_score += weights[field]

        if match_score >= threshold:
            direct_links.append(r["id"])

    return direct_links

def find_links_within_two_hops(rows, weights, threshold, target_user_id):
    # Build graph of direct links for all nodes
    graph = {}
    for r in rows:
        graph[r["id"]] = find_direct_links(rows, weights, threshold, r["id"])

    if target_user_id not in graph:
        return set()

    # BFS to find nodes up to distance 2
    visited = {target_user_id}
    queue = deque([(target_user_id, 0)])
    result = set()

    while queue:
        node, dist = queue.popleft()
        if dist > 0:
            result.add(node)
        if dist < 2:
            for neighbor in graph[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, dist + 1))
    return result

def find_all_linked(rows, weights, threshold, target_user_id):
    # Build graph of direct links for all nodes
    graph = {}
    for r in rows:
        graph[r["id"]] = find_direct_links(rows, weights, threshold, r["id"])

    if target_user_id not in graph:
        return []

    # BFS to find connected component
    visited = {target_user_id}
    queue = deque([target_user_id])
    result = set()

    while queue:
        node = queue.popleft()
        if node != target_user_id:
            result.add(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    return sorted(list(result))
