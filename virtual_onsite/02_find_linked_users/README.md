# Problem 2: Find Linked Users (Entity Resolution & Graphs)

Build a system to find linked users based on similarity weights of user records.

## Inputs

- `rows`: a list of user records:
  ```python
  {
      "id": 1,
      "name": "Alice",
      "email": "alice@gmail.com",
      "company": "Stripe"
  }
  ```
- `weights`: a dictionary mapping field to weight, e.g.:
  ```python
  {
      "name": 0.2,
      "email": 0.5,
      "company": 0.3
  }
  ```
- `threshold`: a float between 0 and 1.
- `target_user_id`: the ID of the user to start searching from.

## Similarity Score Definition

For two records A and B:
- For each field in `{name, email, company}`:
  - If `A[field] == B[field]`, add `weights[field]` to the similarity score.
  - Otherwise, add `0`.
- Two records are **directly linked** if their similarity score is `>= threshold`.

## Requirements

### Part 1: Direct Matches
`find_direct_links(rows, weights, threshold, target_user_id) -> List[int]`
- Returns a list of record IDs directly linked to the target user (excluding the target user itself).

### Part 2: Reachable within 2 Hops
`find_links_within_two_hops(rows, weights, threshold, target_user_id) -> Set[int]`
- Returns all record IDs reachable from the target user by a path of length at most 2 edges (excluding the target user itself).

### Part 3: Full Connected Component
`find_all_linked(rows, weights, threshold, target_user_id) -> List[int]`
- Returns all record IDs in the same connected component as the target user (excluding the target user itself), sorted lexicographically.
