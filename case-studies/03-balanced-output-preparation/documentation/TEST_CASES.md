# Test Cases

| ID | Scenario | Expected result |
|---|---|---|
| T01 | Clean, unique record | Accepted |
| T02 | Missing required field | Input exception |
| T03 | Duplicate key | Duplicate exception |
| T04 | Record maps to no reporting dimension | Unmapped exception |
| T05 | Value fails type check | Data-quality exception |
| T06 | Aggregated detail total | Agrees with summary |
| T07 | Input count | Equals accepted plus exceptions |
