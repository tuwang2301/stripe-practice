from collections import *
import math

def find_direct_links(rows, weights, threshold, target_user_id):
    target_user = {}
    for r in rows:
        if r["id"] == target_user_id:
            target_user = r

    direct_links = []
    for r in rows:
        if r["id"] == target_user["id"]: continue

        match_score = 0
        for field in weights:
            if r[field] == target_user[field]:
                match_score += weights[field]

        if match_score >= threshold:
            direct_links.append(r["id"])

    return direct_links

def find_direct_links_extra(rows, weights, threshold, target_user_id):
    undirected_graph = defaultdict(list)

    for r in rows:
        undirected_graph[r["id"]] = find_direct_links(rows,weights,threshold,r["id"])

    result = set()
    def dfs(id, count, visited):
        if id in visited or count >= 2:
            return
        
        visited.add(id)
        direct_links = undirected_graph[id]
        for dl in direct_links:
            result.add(dl)
            dfs(dl, count + 1, visited)
        
    dfs(target_user_id, 0, set())

    if target_user_id in result:
        result.remove(target_user_id)   
    return result


if __name__ == "__main__":
    rows = [
    { "id": 1, "name": "Alice", "email": "alice@gmail.com", "company": "Stripe" },
    { "id": 2, "name": "Alice", "email": "alice@gmail.com", "company": "Google" },  # linked to 1 (name+email=0.7)
    { "id": 3, "name": "Bob",   "email": "alice@gmail.com", "company": "Google" },  # linked to 2 (email+company=0.8), NOT to 1 (email only=0.5?)
    { "id": 4, "name": "Carol", "email": "carol@gmail.com", "company": "Meta" },    # isolated
    { "id": 5, "name": "Bob",   "email": "bob@gmail.com",   "company": "Google" },  # linked to 3 (name+company=0.5), 3-hop from 1
    ]

    weights = { "name": 0.2, "email": 0.5, "company": 0.3 }
    threshold = 0.7

    result = find_direct_links_extra(rows, weights, threshold, 2)
    print(result)
