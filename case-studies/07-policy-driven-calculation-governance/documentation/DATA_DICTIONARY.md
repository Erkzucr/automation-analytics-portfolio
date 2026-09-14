# Data Dictionary

| Field | Meaning | Example |
|---|---|---|
| record_id | Unique key | REC00001 |
| period_key | Period the rule version applied to | P01 |
| dimension_a | Grouping attribute for rule application | DA001 |
| dimension_b | Secondary grouping attribute | DB001 |
| category_code | Category the rule targets | CAT01 |
| value_amount | Synthetic calculated value | 1250.00 |
| status_code | Status after rule application | VALID |

## Output-only fields

| Field | Meaning | Example |
|---|---|---|
| exception_reason | Why a row landed in exception_records.csv | DUPLICATE_KEY |
| policy_rate | Rate applied from the policy table | 0.1000 |
| computed_amount | value_amount × policy_rate | 125.00 |
