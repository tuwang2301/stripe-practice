# Problem 6: Chronological Fraud Rule Authorization Report

Produce a chronological report of authorization decisions based on a list of requests and incoming fraud rules.

## Inputs

- `requests`: a list of dictionaries with keys:
  - `time`: integer seconds
  - `unique_id`: string
  - `amount`: integer
  - `card_number`: string
  - `merchant`: string
- `rules`: a list of dictionaries with keys:
  - `time`: integer seconds
  - `field`: string
  - `value`: string

## Rules

- Initially, all requests are `APPROVE`.
- From each rule's time onward (i.e., for any request with `request.time >= rule.time`), any future request whose specified field equals the rule's value must be marked `REJECT`.
- Valid rule fields are: `unique_id`, `amount`, `card_number`, `merchant`.
- Rule matching uses string comparison: `rule.value == str(request[field])`.

## Output Format

Return a list of strings, each formatted as:
`"time unique_id amount DECISION"`
where `DECISION` is `REJECT` if any rule applies, otherwise `APPROVE`.
The report must be ordered by increasing time; for ties, preserve the original input order of requests.
