You are given a list of user records. Each record has the following fields:

id (integer, unique)
name (string)
email (string)
company (string)
You are also given a map weights from field name to a non-negative floating-point weight, for example:

name: 0.2
email: 0.5
company:0.3
Define the similarity score between two records A and B as:

For each field among {name, email, company} :
If A.field == B.field (string equality), add weights[field] to the score.
Otherwise add 0 .
The total similarity score is the sum over all fields.
Two records are said to be directly linked if their similarity score is greater than or equal to a given threshold (where 0 <= threshold <= 1). Treat the relation as undirected: if record i is directly linked to record j, then j is directly linked to i.

You are given:

rows : a list of user records as described above.
weights : the map from field name to weight.
threshold : a floating-point number.
target_user_id : the id of a record in rows .
Assume:

id values are unique.
rows fits in memory (you do not need to design a distributed system).
Example:

rows = [
{ id: 1, name: "Alice", email: "alice@gmail.com", company: "Stripe" },
{ id: 2, name: "Alicia", email: "alice@gmail.com", company: "Stripe" },
{ id: 3, name: "Alice", email: "alice@yahoo.com", company: "Google" },
{ id: 4, name: "Bob", email: "bob@gmail.com", company: "Stripe" }
]

weights = {
name: 0.2,
email: 0.5,
company: 0.3
}

threshold = 0.5
Under the definition above:

Records 1 and 2 have the same email and company , so their similarity is 0.5 + 0.3 = 0.8 >= 0.5 → directly linked.
Records 1 and 3 only share the same name , similarity is 0.2 < 0.5 → not directly linked.
Records 2 and 3 share no identical fields under this example (depending on the exact strings) → assume not directly linked.
Part 1 — Direct matches for a target user
Implement a function that, given rows, weights, threshold, and target_user_id, returns all record IDs whose records are directly linked to the target user's record (based solely on the similarity score definition).

You can choose any reasonable function signature, such as:

find_direct_links(rows, weights, threshold, target_user_id) -> List[int]
The result should not include target_user_id itself.

Part 2 — Include exactly one layer of indirect matches
Now extend the requirement.

Construct an undirected graph where:

Each node is a record (identified by its id ).
There is an edge between two nodes if the corresponding records are directly linked (similarity ≥ threshold).
For a given target_user_id, you must now return all record IDs that are:

Directly linked to the target or
Directly linked to some record that is directly linked to the target (i.e., reachable from the target by a path of length at most 2 edges ).
Example scenario:

1 and 2 are directly linked.
2 and 3 are directly linked.
1 and 3 are not directly linked.
In this case, for target_user_id = 1, your output should include {2, 3}: record 2 is a direct match; record 3 is a one-hop indirect match through 2.

Design and implement this extended query.

Part 3 — All transitively linked users (full component)
Further extend the requirement so that, for a given target_user_id, you return all record IDs in the same connected component as the target in the graph defined above.

In other words, return every record that is reachable from the target by any number of edges (0 or more), based on the direct-link relation.

Implement a function such as:

find_all_linked(rows, weights, threshold, target_user_id) -> List[int]
that returns the IDs of all records (excluding or including the target itself — specify your choice) that belong to the same connected component as the target.
