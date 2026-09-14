# ADR-004: Control summary

## Context
Without a running record of counts and tie-out values, there's no way to confirm after the fact that a process reconciled.

## Decision
Retain input, output, and tie-out counts as part of every run's output.

## Consequences
A small amount of extra bookkeeping per run, and in return you can prove completeness later without re-running anything.
