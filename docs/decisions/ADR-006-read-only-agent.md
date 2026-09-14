# ADR-006: The finance agent is read-only

## Context
A Copilot Studio agent can call actions that write to systems. For a finance help desk that would mean the agent could post an entry or record an approval, and an auditor would then ask which conversation approved which entry.

## Decision
No action in the agent writes to a finance system. It answers from an allowlisted knowledge base with citations, it can create a request record that a person picks up, and it refuses anything that asks it to change data or approve. Since the write capability isn't configured, there is no instruction for the model to ignore.

## Consequences
Some users will want more than the agent gives them, so the refusal wording has to point them to a person. In return the agent can be used by finance staff and reviewed by auditors without a separate control discussion. A future write action would get the same treatment as any automated control: a named owner, evidence per execution, and a test set showing it fires only when it should.
