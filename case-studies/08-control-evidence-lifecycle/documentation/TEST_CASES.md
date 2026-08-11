# Test Cases

| ID | Scenario | Expected result |
|---|---|---|
| T01 | Control executed with complete evidence | Accepted |
| T02 | Missing required evidence field | Input exception |
| T03 | Duplicate execution record | Duplicate exception |
| T04 | Control not found in catalog | Unmapped exception |
| T05 | Invalid type on an evidence field | Data-quality exception |
| T06 | Certified detail total | Agrees with summary |
| T07 | Input count | Equals accepted plus exceptions |
