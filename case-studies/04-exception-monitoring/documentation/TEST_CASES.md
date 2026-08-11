# Test Cases

| ID | Scenario | Expected result |
|---|---|---|
| T01 | Complete, unique record | Accepted |
| T02 | Missing required field | Input exception |
| T03 | Duplicate key | Duplicate exception |
| T04 | Owner group not in reference table | Unmapped exception |
| T05 | Invalid type on an age or date field | Data-quality exception |
| T06 | Prioritized detail total | Agrees with summary |
| T07 | Input count | Equals accepted plus exceptions |
