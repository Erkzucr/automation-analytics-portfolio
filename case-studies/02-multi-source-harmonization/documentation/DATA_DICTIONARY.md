# Data Dictionary

| Field | Meaning | Example |
|---|---|---|
| record_id | Unique key, generated per synthetic source | REC00001 |
| period_key | Period the record maps to after standardization | P01 |
| dimension_a | First grouping attribute, harmonized across sources | DA001 |
| dimension_b | Second grouping attribute | DB001 |
| category_code | Category assigned once mapped to the canonical schema | CAT01 |
| value_amount | Synthetic value used to demonstrate aggregation | 1250.00 |
| status_code | Status after validation and mapping | VALID |

## Output-only fields

| Field | Meaning | Example |
|---|---|---|
| exception_reason | Why a row landed in exception_records.csv | DUPLICATE_KEY |
