# Test Cases

| ID | Scenario | Expected result |
|---|---|---|
| T01 | Record present on both sides, values agree | Accepted, matched |
| T02 | Required field missing on either side | Input exception |
| T03 | Duplicate key on either side | Duplicate exception |
| T04 | Record on one side, missing on the other | Unmatched exception |
| T05 | Type mismatch between sides | Data-quality exception |
| T06 | Matched detail total | Agrees with summary |
| T07 | Combined input count | Equals accepted plus exceptions |
