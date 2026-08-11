# Test Cases

| ID | Scenario | Expected result |
|---|---|---|
| T01 | Record present, unique, all sources agree | Accepted |
| T02 | Required field missing from a source | Input exception |
| T03 | Duplicate key across sources | Duplicate exception |
| T04 | Source references a period not in the reference table | Unmapped exception |
| T05 | Field type mismatch between sources | Data-quality exception |
| T06 | Harmonized detail total | Agrees with summary |
| T07 | Combined input count | Equals accepted plus exceptions |
