# Automation & Analytics Portfolio

[![Python demo tests](https://github.com/Erkzucr/automation-analytics-portfolio/actions/workflows/python-tests.yml/badge.svg)](https://github.com/REPLACE_WITH_GITHUB_USERNAME/automation-analytics-portfolio/actions/workflows/python-tests.yml)

Hi, I'm Erick — I put this repo together to show how I actually approach automation and reconciliation work, without leaning on anything from a real employer.

Cases 01-09 are built from synthetic data — no production files, no internal process names, nothing traceable to an employer. Case 10 is different: it's a real app I built and shipped for a school, with the sensitive parts (Firebase config, real data) deliberately left out of the repo.

**[Start here if you're reviewing this for a role](RECRUITER_START_HERE.md)** · [Resumen en español](README_ES.md) · [One-page PDF](assets/Erick_Zuniga_Automation_Analytics_Portfolio_OnePager.pdf)

## What's in here

Nine case studies, each modeling a type of problem I've dealt with in real reconciliation and controls work — mismatched sources, exception handling, period-over-period checks, control evidence, and a couple that lean into how I use AI responsibly in that kind of workflow. Every case has an architecture diagram, sample data, and a short write-up of the problem and how I'd solve it.

There are also two working demos you can actually run:

```bash
cd demo/python-reconciliation-demo
python run_demo.py
python -m unittest discover -s tests -v
```

And an Alteryx workflow at `demo/alteryx-reconciliation-demo/Synthetic_Reconciliation_Demo.yxmd` — open it and run it, it only touches the synthetic data bundled alongside it.

There's also a [3-page Power BI dashboard](demo/power-bi-portfolio-dashboard/README.md) built on this portfolio's own metadata, with rendered screenshots and everything needed to rebuild it yourself.

## Case studies

- [Periodic Estimate Analysis](case-studies/01-periodic-estimate-analysis/README.md)
- [Multi-Source Data Harmonization](case-studies/02-multi-source-harmonization/README.md)
- [Balanced Output Preparation](case-studies/03-balanced-output-preparation/README.md)
- [Exception Monitoring and Prioritization](case-studies/04-exception-monitoring/README.md)
- [Source-to-Record Reconciliation](case-studies/05-source-to-record-reconciliation/README.md)
- [Period-Over-Period Analysis](case-studies/06-period-over-period-analysis/README.md)
- [Policy-Driven Calculation Governance](case-studies/07-policy-driven-calculation-governance/README.md)
- [Control Evidence and Assurance Lifecycle](case-studies/08-control-evidence-lifecycle/README.md)
- [AI-Assisted Knowledge Capture](case-studies/09-ai-assisted-knowledge-capture/README.md)
- [School Inventory Web App](case-studies/10-school-inventory-webapp/README.md) — a real React/Firebase app I built and shipped, not a synthetic exercise

## How I think about this work

Standardize first, automate second, build in controls from the start, and keep improving once it's live. That order matters more than the tooling — I've used Alteryx, Power Query, VBA, and Python for different pieces of it, but the sequence is the same regardless of what's driving the automation.

## A note on data

Everything — the CSVs, the numbers, the "companies" — is made up for this repo. Nothing here comes from a production system or an employer's internal process.
