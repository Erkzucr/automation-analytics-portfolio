# ADR-002: Separate exceptions

## Context
Mixing accepted and exception records in one output makes it easy for review-worthy items to get lost among the records that are fine.

## Decision
Produce two distinct outputs: accepted records and exceptions.

## Consequences
Reviewers can focus on the exception output without wading through everything else, at the cost of maintaining two outputs instead of one. Worth it for the reviewability it buys.
