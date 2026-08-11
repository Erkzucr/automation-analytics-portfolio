# Alteryx Reconciliation Demo

A small, self-contained Alteryx workflow with the sample records built right into it, so it runs without pointing at any external file. It matches two record sets, flags anything outside tolerance for review, and separates out what's unmatched on either side.

## How to run it

1. Open `Synthetic_Reconciliation_Demo.yxmd` in Alteryx Designer (built on 2023.2, should work on nearby versions).
2. Hit **Run**.
3. Check the four Browse outputs: accepted, review, source-A-only, source-B-only.

## What you should see

- Accepted: REC001, REC002, REC005
- Review: REC003
- Source A only: REC004
- Source B only: REC006

## Tools used

Text Input, Join, Formula, Filter, Browse — nothing exotic, just enough to show the matching and exception logic clearly.

All records are made up for this demo. No production data, external connections, or references to any real organization.

