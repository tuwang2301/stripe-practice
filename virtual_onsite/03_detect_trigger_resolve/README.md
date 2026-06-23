# Problem 3: Detect Trigger & Resolve Events (Sliding Window & Telemetry)

Implement a real-time event monitor to detect threshold triggers and resolutions from transaction status logs.

## Inputs

- `logs`: a list of 4-tuples `(timestamp, merchant_id, status_code, count)` sorted by non-decreasing timestamp.
- `window_size`: sliding window size (inclusive range `[t - window_size + 1, t]`).
- `threshold`: integer threshold count.

## Rules

For each independent `(merchant_id, status_code)` pair:
1. Track the **rolling error count** (sum of `count` values in the sliding window).
2. Emit a `TRIGGER` event when the rolling count changes from strictly less than threshold to **greater than or equal to threshold**.
3. Emit a `RESOLVE` event when the rolling count changes from greater than or equal to threshold to **strictly less than threshold**.
4. Do not emit consecutive duplicate events of the same type for the same pair.
5. **No synthetic events**: Events are evaluated only when processing an input log.
6. If multiple logs share the same timestamp, process them in input order.

## Output Format

Return all emitted events in chronological order as 4-tuples:
`(timestamp, merchant_id, status_code, event_type)`
*Ties in timestamp must preserve the original input order.*
