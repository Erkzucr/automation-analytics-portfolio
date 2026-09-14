# Test Cases

Each scenario has a row in `sample-data/input_primary.csv` that triggers it, and `demo/case-pipeline/tests/test_pipeline.py` checks the outcome in CI.

| ID | Scenario | Expected result |
|---|---|---|
| T01 | Clean row, unique key, active reference, VALID status | Accepted |
| T02 | Required field missing (REC00021) | Exception MISSING_FIELD |
| T03 | Duplicate key (REC00003 twice) | Both rows exception DUPLICATE_KEY |
| T04 | Dimension not in reference (REC00022) | Exception UNMAPPED_REFERENCE |
| T05 | Amount not numeric (REC00023) | Exception INVALID_AMOUNT |
| T06 | Reference exists but is INACTIVE (REC00024) | Exception INACTIVE_REFERENCE |
| T07 | Messy but valid row: lowercase codes, spaces (REC00025) | Standardized and accepted |
| T08 | Source status REVIEW | Exception SOURCE_STATUS_REVIEW |
| T09 | Count tie-out | accepted + exceptions = input |
| T10 | Amount tie-out | accepted total + exception total = input total |
| T11 | Amount above category ceiling (REC00026) | Exception ABOVE_CATEGORY_CEILING |
