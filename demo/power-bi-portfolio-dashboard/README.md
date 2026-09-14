# Power BI Dashboard

A 3-page dashboard built on this portfolio's own metadata: how many case studies there are, how deep each one goes, and what came out of the runnable demos. Same rule as everywhere else in the repo, synthetic data only.

The `.pbix` isn't included. A binary can't be diffed and it requires Power BI Desktop just to look at it. This folder has the data, the DAX measures and the layout spec to rebuild it, plus screenshots to judge the output without opening anything.

**Executive Overview.** Case counts, demo counts, test counts, and a quick read on the complexity mix.

![Executive Overview](screenshots/page1_executive_overview.png)

**Case Study Explorer.** Every case in a matrix, with conditional formatting on demonstration depth.

![Case Study Explorer](screenshots/page2_case_study_explorer.png)

**Executable Demo Results.** Accepted and exception counts from the runnable demos, by technology.

![Executable Demo Results](screenshots/page3_executable_demo_results.png)

## To rebuild it

1. Import `portfolio_cases.csv` and `demo_execution.csv` into Power BI Desktop.
2. Add the measures from `DAX_MEASURES.md`.
3. Lay out the three pages per `DASHBOARD_SPEC.md`.

The screenshots came from this spec and data, so what you build should land close.

The CSVs cover all thirteen cases and the seven runnable pieces. The screenshots were rendered from the nine-case version and are pending a refresh.
