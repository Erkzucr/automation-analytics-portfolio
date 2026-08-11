# Test Cases

| ID | Scenario | Expected result |
|---|---|---|
| T01 | Active, approved rule applies cleanly | Accepted |
| T02 | Missing required field | Input exception |
| T03 | Duplicate key | Duplicate exception |
| T04 | Rule version not found or inactive | Unmapped exception |
| T05 | Invalid type on a rule parameter | Data-quality exception |
| T06 | Accepted detail total | Agrees with summary |
| T07 | Input count | Equals accepted plus exceptions |
