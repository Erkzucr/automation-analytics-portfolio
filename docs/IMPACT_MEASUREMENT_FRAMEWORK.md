# How impact is measured

Metrics used to decide whether an automation was worth building:

- **Hours saved per year**: baseline minutes per task × frequency × volume, divided by 60. Label baseline vs realized; they're not the same number.
- **Automation coverage**: automated records / total input records
- **Exception rate**: exceptions / total input records
- **Review efficiency**: accepted records / records reviewed
- **Control completion**: checks completed / checks required
- **Agent test pass rate**: routed as expected / test conversations (case 11)
- **Variance explained**: sum of decomposed effects / total variance, must be 100% (case 12)
- **SPI and CPI**: earned value over planned and over actual; 1.0 is on plan (case 13)

All figures in this repo are based on synthetic or public data, not production numbers.

## Demonstration depth rubric

The `demonstration_depth` column in the Power BI data is scored against this table. A case gets a 5 only if every row is true, and CI proves the last one.

| Depth | What has to exist |
|---|---|
| 1 | A write-up of the problem |
| 2 | Plus an architecture diagram |
| 3 | Plus sample data and a data dictionary |
| 4 | Plus documented test cases and a control matrix |
| 5 | Plus runnable code that produces the expected output, tests that check it, and both running in CI |

As of v1.3 all thirteen cases are at 5. Cases 01 to 09 run through `demo/case-pipeline`, case 10 through `node --test`, and 11, 12 and 13 through their own scripts. For case 10 the UI is checked by hand; what's under automated test is the logic that decides what gets saved.
