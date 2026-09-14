# Data Dictionary

## sample-data/people_cost_monthly.csv

| Field | Meaning | Example |
|---|---|---|
| period | Month, YYYY-MM | 2026-03 |
| cost_center | Synthetic cost center code | CC300 |
| country | Synthetic country code | PL1 |
| budget_headcount | Planned FTE | 24 |
| budget_rate | Planned loaded monthly cost per FTE (salary + employer costs + benefits) | 4812.50 |
| actual_headcount | Actual FTE | 26 |
| actual_rate | Actual loaded monthly cost per FTE | 4903.10 |
| one_off_amount | Non-recurring cost in the month (severance, retention, true-up) | 24000.00 |
| revenue | Synthetic revenue attributed to the cost center, for the % KPI | 310000.00 |

## expected-output/variance_detail.csv

| Field | Meaning |
|---|---|
| budget_cost, actual_cost | headcount × rate, plus one-offs on the actual side |
| variance, variance_pct | actual minus budget, and as % of budget |
| headcount_effect | (actual HC minus budget HC) × budget rate |
| rate_effect | (actual rate minus budget rate) × budget HC |
| mix_effect | (ΔHC) × (Δrate), the cross term |
| one_off_effect | one_off_amount |
| material_flag | YES if both thresholds in case.json are met |
| primary_driver | Largest absolute effect, only on material lines |

## expected-output/kpi_summary.csv

One row per period. See the KPI table in the README.
