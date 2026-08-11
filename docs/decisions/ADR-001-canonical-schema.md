# ADR-001: Canonical schema

## Context
Data comes in from multiple sources, each with its own naming and formatting conventions. Comparing them directly means comparing noise, not substance.

## Decision
Map every source to one common schema before any downstream logic runs.

## Consequences
Adds an explicit mapping step and a control responsibility (someone has to maintain the mapping as sources change), but it's what makes the rest of the pipeline traceable and reviewable.
