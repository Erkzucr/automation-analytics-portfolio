# Exception Monitoring and Prioritization

Having an exception report is one thing. Having one that tells the right person what to look at first is another. This case study is about the second part.

## Business problem

A pile of unresolved items isn't useful if nobody knows who owns each one, how old it is, or which ones actually matter. I've seen review queues where "exceptions" just meant a spreadsheet tab nobody opened until quarter-end. That's the failure mode I designed against here.

## What I built

Validated records get routed through an ownership assignment step and an age-banding calculation, and the result is a prioritized view instead of a flat list. New, unassigned, and aged-out items surface differently, so review effort goes where it's actually needed.

```mermaid
flowchart TB
 A1[Synthetic source A] --> B[Schema and completeness checks]
 A2[Synthetic reference data] --> B
 B --> C{Valid input?}
 C -- No --> X1[Input exception]
 C -- Yes --> D[Standardize generic fields]
 D --> E[Apply Exception monitoring logic]
 E --> F{Review required?}
 F -- Yes --> X2[Review exception]
 F -- No --> G[Accepted detail]
 G --> H[Create summary output]
 H --> I{Control totals agree?}
 I -- No --> X3[Control exception]
 I -- Yes --> J[Publish summary and support]
 X1 --> K[Unified exception register]
 X2 --> K
 X3 --> K
 K --> J
```

## Process walkthrough

1. Load source and reference data.
2. Validate schema, required fields, and unique keys.
3. Standardize identifiers, dates, statuses, and values.
4. Assign owner groups and calculate age bands.
5. Separate accepted records from items needing review.
6. Build the prioritized monitoring view and supporting detail.
7. Reconcile the summary back to detail.

## Controls demonstrated

- Required-field and duplicate-key validation
- Reference completeness checks so ownership assignment doesn't fail silently
- Input-to-output count reconciliation
- Summary-to-detail tie-out
- A single exception register instead of one queue per failure type

The interesting part of this one is less the calculation and more the prioritization logic, deciding what surfaces first so review time doesn't get wasted on low-priority noise. All data is synthetic.
