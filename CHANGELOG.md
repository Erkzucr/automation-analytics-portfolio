# Changelog

## v1.3
- Two new cases. 12 is people cost variance analysis: headcount, rate, mix and one-off decomposition that ties on every line, materiality on amount and percent, KPI summary, bridge chart, seven tests. 13 is a close improvement project tracker: earned value by task, workstream and total, milestone health, scored risk register, generated status report, seven tests
- Both wired into CI; rubric and dashboard data updated to thirteen cases
- Confidentiality pass over markdown, code, data, the Alteryx workflow and the PDF. No employer names, internal identifiers, system names or credentials anywhere. One test fixture name neutralized
- Prose pass over every README, brief and decision note: shorter, concrete, no em dashes, no rhetorical openers, less first person
- Spanish README rewritten as a full version rather than a summary; Spanish recruiter guide added

## v1.2
- Shared pipeline in `demo/case-pipeline` now produces the expected output of cases 01 to 09. Each case has a `case.json` with its logic block and parameters
- Sample data for those cases extended with edge rows (missing field, duplicate key, unmapped and inactive reference, non-numeric amount, messy-but-valid row) so every documented test case is exercised
- Control matrix in every case, each row pointing at where its evidence lands; test cases rewritten to match the data
- Case 10: pure logic extracted to `src/inventoryLogic.js`, six tests covering seven scenarios with `node --test`, data model, test plan and control matrix
- Case 11: control matrix added
- Depth rubric written down in `docs/IMPACT_MEASUREMENT_FRAMEWORK.md`; all cases meet depth 5 and CI enforces the runnable part
- CI split into a Python job and a Node job
- Charts: coverage chart now shows test cases per case; demo outputs chart rebuilt horizontally
- ADR-007 on generating expected output

## v1.1
- New case 11: Copilot Studio finance agent, with topics, guardrails, synthetic knowledge base, a versioned conversation test set, and a Python simulation of the routing that runs in CI
- CI runs the agent evaluation alongside the reconciliation demo tests
- Charts rebuilt and linked from the README
- Power BI dashboard data updated to include cases 10 and 11 and the agent evaluation
- README rewritten around a case table, Spanish README updated, recruiter guide updated
- ADR-006 on the read-only agent
- Fixed the CI badge link

## v1.0
- Nine case studies covering reconciliation, exceptions, governance, and AI-assisted work
- Working Python reconciliation demo with tests
- Verified Alteryx workflow using synthetic data
- Architecture diagrams, sample datasets, and decision notes for each case
