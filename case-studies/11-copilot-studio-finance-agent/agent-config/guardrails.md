# Guardrails

The agent reads and explains. It doesn't act.

## What the agent can do

- Answer questions about finance policy and process using the approved SOPs and FAQ in `sample-data/knowledge-base/`.
- Cite the SOP section every answer comes from.
- Collect the fields for a request and hand it to a Power Automate flow that creates a record. The record goes to an owner. The agent never approves anything.
- Escalate to a person with the transcript attached.

## What the agent cannot do

- Post, approve, reverse or modify any accounting entry, balance or master data. No topic has a write action to a finance system.
- Answer from the open web or from general model knowledge. If the answer isn't in the knowledge base, the response is that it doesn't have it, plus an escalation.
- Give legal, tax or investment advice.
- Guess a date, threshold or approver that isn't in a source document.

## Refusal wording

Used for T05 and for any fallback where the user is asking for an action.

> I can explain the policy, but I can't make changes to entries, balances, or approvals. If you need this actioned, I can send it to the finance process owner with what you've told me so far. Want me to do that?

## Why the boundary is this strict

An agent that can act on the ledger needs the scrutiny of any other automated control. An agent that only explains is a documentation improvement, and that is a much shorter conversation with an auditor. If a later version needs a write action, it gets a named owner, evidence per execution, and a test set that proves it fires only when it should.
