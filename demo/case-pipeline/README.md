# Case pipeline

Cases 01 to 09 all describe the same skeleton in their READMEs: validate, standardize, apply the case's logic, split accepted from exceptions, summarize, tie out. This folder is that skeleton in code. The `expected-output` of each case comes from running it, and CI checks that what's committed still matches.

```
cd demo/case-pipeline
python run_case.py all            # rewrite every case's expected-output
python run_case.py 06             # one case
python run_case.py all --check    # compare a fresh run against what's committed
python -m unittest discover -s tests -v
```

## What every case gets for free

| Stage | Rule | Exception reason |
|---|---|---|
| Standardize | Trim, uppercase codes, amounts to two decimals | none; this fixes rows rather than rejecting them |
| Required fields | Any listed field empty | `MISSING_FIELD:<field>` |
| Amount | Not parseable as a number | `INVALID_AMOUNT` |
| Unique key | `record_id` appears more than once (both rows go to exceptions) | `DUPLICATE_KEY` |
| Reference | `dimension_a` not in the reference file | `UNMAPPED_REFERENCE` |
| Reference status | Reference row is not ACTIVE | `INACTIVE_REFERENCE` |
| Source status | Source already flagged the row | `SOURCE_STATUS_<code>` |
| Tie-out | accepted + exceptions = input, in count and in amount | `count_tie_out`, `total_tie_out` in the summary |

## What's specific per case

Each case has a `case.json` naming its logic block and parameters. The parameters are made up.

| Case | Logic | What it adds |
|---|---|---|
| 01 | `estimate_reasonableness` | Amount above the per-category ceiling goes to review |
| 02 | `period_allowlist` | Period not in the harmonization map can't be aligned |
| 03, 05, 08, 09 | `none` | The common stages are enough; the write-up carries the design |
| 04 | `priority` | Every accepted row gets HIGH / MEDIUM / LOW by amount so a reviewer knows where to start |
| 06 | `period_movement` | Dimension total vs prior period; absolute move above threshold goes to review |
| 07 | `policy_rate` | Rate by category from the policy table; a category with no policy goes to the register |

## Why the sample data has ugly rows in it

After the first twenty clean rows, every `input_primary.csv` has a row with a missing amount, a duplicate key, an unmapped reference, an amount with a letter O in it, a row pointing at an inactive reference, and one row that's messy but valid (lowercase codes, stray spaces). Earlier versions of this repo listed those scenarios in `TEST_CASES.md` without data that triggered them. Now the suite checks that every reason shows up in every case.

Plain csv and no third-party packages, so `pipeline.py` can be read top to bottom in one sitting.
