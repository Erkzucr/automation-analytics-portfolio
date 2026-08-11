# Test Cases

| ID | Scenario | Expected result |
|---|---|---|
| T01 | Draft statement verified against source | Accepted |
| T02 | Missing source segment | Input exception |
| T03 | Duplicate draft entry | Duplicate exception |
| T04 | Draft references a topic not in the transcript | Unmapped exception |
| T05 | Invalid type on a metadata field | Data-quality exception |
| T06 | Verified detail total | Agrees with summary |
| T07 | Input count | Equals accepted plus exceptions |
