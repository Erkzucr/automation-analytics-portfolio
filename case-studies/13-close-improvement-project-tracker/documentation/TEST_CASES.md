# Test Cases

Automated in `tracker/tests/test_tracker.py`, run in CI.

| ID | Scenario | Expected result |
|---|---|---|
| T01 | Status date before, midway, after a task's window | Planned fraction 0, 0.5, 1 |
| T02 | Task half done, spent 600 of 1000 at the halfway date | PV 500, EV 500, AC 600, SPI 1.0, CPI 0.83 |
| T03 | Index at 0.95, 0.90, 0.84 | GREEN, AMBER, RED |
| T04 | Two workstreams | TOTAL row equals their sum |
| T05 | Milestones: future, past without actual, late actual, early actual | ON_TRACK, MISSED, ACHIEVED_LATE, ACHIEVED with correct slip |
| T06 | Three risks, one closed with the highest score | Open first, then by score; levels HIGH, LOW, HIGH |
| T07 | Full run | Output equals the committed expected-output byte for byte, rollup ties |
