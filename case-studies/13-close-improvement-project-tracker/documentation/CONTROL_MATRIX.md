# Control Matrix

| ID | Objective | Procedure | Evidence |
|---|---|---|---|
| CTL-01 | Status is calculated, not asserted | PV, EV, AC from plan fields only | earned_value_by_task.csv, test T02 |
| CTL-02 | Rollup is complete | TOTAL BAC equals sum of task BAC | control_summary rollup_ties, test T04 |
| CTL-03 | Thresholds are explicit | RAG bands read from case.json | test T03 |
| CTL-04 | Milestones judged by dates | State from planned, actual and status date only | milestone_health.csv, test T05 |
| CTL-05 | Decision list is the top of the risk list | Score = probability × impact, open first | risk_scored.csv, test T06 |
| CTL-06 | Report cannot drift from data | status_report.md generated each run | test T07 |
| CTL-07 | Output is reproducible | Committed output equals a fresh run | test T07, CI |
