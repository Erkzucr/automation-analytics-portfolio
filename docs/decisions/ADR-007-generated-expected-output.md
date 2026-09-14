# ADR-007: Expected output is generated

## Context
Until v1.1 the `expected-output` folders of cases 01 to 09 were written by hand, and the sample data never triggered the documented test cases. Rows with a missing field or a duplicate key existed in `TEST_CASES.md` and nowhere else.

## Decision
One shared pipeline produces each case's expected output from its sample data and a small `case.json`. The sample data includes the failing rows. CI regenerates the output and fails if it differs from what's committed.

## Consequences
Changing a rule means rerunning the pipeline and committing the diff, which is where a reviewer should look anyway. The pipeline uses the csv module and no third-party packages so it can be read in one sitting. The nine cases share code; what differs between them is in `case.json` and in the write-up.
