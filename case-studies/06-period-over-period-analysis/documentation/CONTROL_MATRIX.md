# Control Matrix

Every control here is enforced by `demo/case-pipeline/pipeline.py` and evidenced in this case's `expected-output`. Nothing on this list is aspirational.

| ID | Objective | Procedure | Evidence |
|---|---|---|---|
| CTL-01 | Input population is complete | Count input rows before any filtering | control_summary.csv input_count |
| CTL-02 | Required fields are present | Reject rows with empty required fields | exception_records.csv MISSING_FIELD |
| CTL-03 | Keys are unique | Reject every row that shares a duplicate key, including the first occurrence | exception_records.csv DUPLICATE_KEY |
| CTL-04 | Amounts are numeric | Reject amounts that don't parse | exception_records.csv INVALID_AMOUNT |
| CTL-05 | Dimensions map to an active reference | Lookup against input_reference.csv and its status | exception_records.csv UNMAPPED_REFERENCE, INACTIVE_REFERENCE |
| CTL-06 | Source flags are respected | Rows already marked for review never reach accepted | exception_records.csv SOURCE_STATUS_REVIEW |
| CTL-07 | Nothing is lost | accepted + exceptions = input, in count and amount | control_summary.csv count_tie_out, total_tie_out |
| CTL-08 | Output is reproducible | Committed expected-output equals a fresh run | demo/case-pipeline tests, CI |
| CTL-09 | Large movements are explained | Absolute move vs prior period above threshold goes to review | exception_records.csv MOVEMENT_ABOVE_THRESHOLD, accepted_records.csv movement_amount |
