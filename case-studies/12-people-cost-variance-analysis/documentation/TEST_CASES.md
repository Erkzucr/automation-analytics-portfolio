# Test Cases

Automated in `analysis/tests/test_variance.py`, run in CI.

| ID | Scenario | Expected result |
|---|---|---|
| T01 | Every line in the sample file | headcount + rate + mix + one-off = variance |
| T02 | Only headcount moved | Whole variance in headcount_effect, rate_effect zero, driver HEADCOUNT |
| T03 | 2% over on a large base (20k) | Not material: fails the percent threshold |
| T04 | 50% over on a tiny base (3k) | Not material: fails the amount threshold |
| T05 | KPI summary | One row per period, people cost % revenue between 0 and 100 |
| T06 | Full run | Output equals the committed expected-output byte for byte |
| T07 | Total tie-out | Sum of effects equals total variance, control_summary says PASS |
