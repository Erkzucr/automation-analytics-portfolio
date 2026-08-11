# DAX Measures

```DAX
Total Case Studies = COUNTROWS(portfolio_cases)

Average Demonstration Depth = AVERAGE(portfolio_cases[demonstration_depth])

Advanced Case Studies =
CALCULATE(
    COUNTROWS(portfolio_cases),
    portfolio_cases[complexity] = "Advanced"
)

Total Documented Tests = SUM(portfolio_cases[documented_tests])

Executable Demos = DISTINCTCOUNT(demo_execution[technology])

Total Accepted Records = SUM(demo_execution[accepted_count])

Total Exception Records = SUM(demo_execution[exception_count])

Exception Rate =
DIVIDE(
    [Total Exception Records],
    [Total Accepted Records] + [Total Exception Records]
)
```
