# Test Cases

Scenarios I used to check the validation and control logic actually catches what it's supposed to.

| ID | Scenario | Expected result |
|---|---|---|
| T01 | Complete, unique record | Accepted |
| T02 | Missing required field | Input exception |
| T03 | Duplicate key | Duplicate exception |
| T04 | Missing reference row | Unmapped exception |
| T05 | Invalid data type | Data-quality exception |
| T06 | Accepted detail total | Agrees with summary |
| T07 | Input record count | Equals accepted plus exceptions |
