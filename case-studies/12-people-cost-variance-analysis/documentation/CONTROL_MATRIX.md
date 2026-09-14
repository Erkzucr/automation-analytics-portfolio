# Control Matrix

| ID | Objective | Procedure | Evidence |
|---|---|---|---|
| CTL-01 | Variance explanation is complete | Four effects must sum to the line variance | test T01, control_summary decomposition_ties |
| CTL-02 | Materiality can't be gamed by base size | Amount AND percent thresholds from case.json | tests T03, T04 |
| CTL-03 | One-offs are visible | Carried as their own effect, never inside rate | variance_detail.csv one_off_effect |
| CTL-04 | KPIs agree with detail | Both computed from the same decomposed lines | kpi_summary.csv vs variance_detail.csv |
| CTL-05 | Review list is prioritized | Material lines sorted by absolute variance with a named driver | material_variances.csv |
| CTL-06 | Output is reproducible | Committed output equals a fresh run | test T06, CI |
