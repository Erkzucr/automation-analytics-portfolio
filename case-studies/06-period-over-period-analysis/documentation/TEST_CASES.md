# Test Cases

| ID | Scenario | Expected result |
|---|---|---|
| T01 | Movement within threshold | Accepted |
| T02 | Missing required field | Input exception |
| T03 | Duplicate key | Duplicate exception |
| T04 | No prior-period value to join | Unmapped exception |
| T05 | Invalid type on a value field | Data-quality exception |
| T06 | Accepted detail total | Agrees with summary |
| T07 | Input count | Equals accepted plus exceptions |
