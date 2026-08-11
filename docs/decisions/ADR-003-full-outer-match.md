# ADR-003: Full outer match

## Context
An inner join is the easy way to match two datasets, but it silently drops anything that doesn't have a counterpart on both sides.

## Decision
Use a full outer match and preserve both matched and unmatched populations.

## Consequences
The match logic is more work to write and slower to run, but it means unmatched records stay visible instead of vanishing, which is the entire point of a reconciliation.
