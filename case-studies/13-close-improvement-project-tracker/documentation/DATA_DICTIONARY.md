# Data Dictionary

## sample-data/project_plan.csv

| Field | Meaning | Example |
|---|---|---|
| task_id | Task key | T07 |
| workstream | Discovery, Design, Build, Test, Deploy | Build |
| task_name | What the task is | Build recurring JE automation |
| planned_start, planned_end | Baseline dates | 2026-08-20 |
| actual_start, actual_end | Blank until it happens | 2026-08-24 |
| planned_cost | Budget at completion for the task | 15000 |
| actual_cost | Spent to date | 11000 |
| percent_complete | Progress, 0 to 100 | 70 |
| milestone_flag | Y if the task is a milestone | N |
| owner_role | Role, never a person | Automation analyst |

## sample-data/risk_register.csv

| Field | Meaning |
|---|---|
| probability, impact | 1 to 5 each |
| response | What's being done about it |
| status | Open or Closed |

## expected-output

| File | What it holds |
|---|---|
| earned_value_by_task.csv | PV, EV, AC, SV, CV, SPI, CPI and RAG per task |
| earned_value_rollup.csv | Same by workstream plus TOTAL, with EAC and VAC |
| milestone_health.csv | State and slip days per milestone as of the status date |
| risk_scored.csv | Register with score and level, open first |
| status_report.md | The generated one-page report |
| control_summary.csv | Totals, indices and tie-out |
