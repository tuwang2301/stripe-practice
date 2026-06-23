# Problem 2: Merchant Loyalty Score

Compute a final loyalty score for each merchant based on their transactions list.

## Inputs

- `transactions_list[i] = "merchant_id,customer_id,amount,category"`
- `merchants_list[i] = "merchant_id,base_points"`

## Rules

Perform the following three passes in order:

1. **Amount Multiplier**: If `amount > 500` → `base_points *= 1.5`
2. **Repeat Customer Bonus**: If the same `customer_id` has bought from the same `merchant_id` **>= 2 times** → `+50` per occurrence from the 2nd onward (processed in chronological order).
3. **Category Adjustments**: If `category == "electronics"` → `+20`; if `category == "food"` → `-10`.

## Output Format

Return the merchant scores in the format `"merchant_id,points"` where points is rounded down (`floor`), sorted lexicographically by `merchant_id`.
