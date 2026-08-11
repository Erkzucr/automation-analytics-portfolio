# ADR-005: Human review for AI output

## Context
AI-generated content can read as polished and confident even when it's wrong, which makes it easy to skip verification.

## Decision
Treat any AI-generated output as a draft that requires human verification before it's treated as final.

## Consequences
Adds a review step that slows down the process slightly, but it's the difference between AI as a drafting tool and AI as an unchecked source of truth.
