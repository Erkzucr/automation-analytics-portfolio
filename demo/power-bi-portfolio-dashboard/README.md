# Power BI Dashboard Build Kit

Not a finished .pbix (didn't want to ship a binary you can't diff), but everything needed to build one: the input data and the spec for measures and layout.

- `portfolio_cases.csv` / `demo_execution.csv` — the underlying data
- `DAX_MEASURES.md` — measures to create
- `DASHBOARD_SPEC.md` — page layout, visuals, filters

## To build it

1. Import both CSVs into Power BI Desktop.
2. Add the measures from `DAX_MEASURES.md`.
3. Lay out the three pages per `DASHBOARD_SPEC.md`.

All figures are synthetic, made up to describe this portfolio itself.
