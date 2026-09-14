# Data Dictionary

| Field | Meaning | Example |
|---|---|---|
| record_id | Unique key | REC00001 |
| period_key | Period the exception was raised in | P01 |
| dimension_a | Owner group, or the attribute used to derive it | DA001 |
| dimension_b | Secondary grouping attribute | DB001 |
| category_code | Exception category | CAT01 |
| value_amount | Synthetic value associated with the item | 1250.00 |
| status_code | Review status | VALID |

## Output-only fields

| Field | Meaning | Example |
|---|---|---|
| exception_reason | Why a row landed in exception_records.csv | DUPLICATE_KEY |
| priority | Review priority band on accepted rows | HIGH |
