# Agent design notes

## Knowledge sources

Three synthetic SOPs and one FAQ file, all in `sample-data/knowledge-base/`. In Copilot Studio these are added as file knowledge sources with generative answers turned on and general knowledge turned off, so the agent only answers from what's uploaded. Each source has an owner and a version in its header. When a source changes, the test set runs again before the new version is published.

## Topics

Six topics: five with content and one fallback. Trigger phrases are in `agent-config/topics.yaml`. They are grouped by what the topic does:

| Kind | Topics | What happens |
|---|---|---|
| Answer from knowledge | T01, T02, T03 | Generative answer grounded in one SOP, citation shown |
| Collect and call flow | T04 | Adaptive card collects fields, Power Automate flow creates a request record, agent returns the request ID |
| Refuse and escalate | T05 | Scripted refusal, offer to hand off with transcript |
| Fallback | T99 | One rephrase attempt, then escalation and an "unanswered" log entry |

## Actions

One action: `create_request_record`, a Power Automate flow triggered from T04. It writes a row to a request list (a SharePoint list or a Dataverse table in a live build) with the collected fields, a timestamp and the conversation ID, and returns the request ID. It sends no approvals and touches no finance system.

## Escalation

Every escalation goes to the finance process owner with the transcript, the topic that fired and the timestamp attached. The person picking it up has the context without asking the user to repeat it.

## Deployment

Published to a Microsoft Teams channel restricted to the finance team. Authentication is the tenant's standard Teams sign-in, so the agent knows who is asking without any extra login. That's also what makes the conversation log attributable.

## Logging and review

Copilot Studio's analytics cover session volume and topic hit rates. A weekly export of unanswered and escalated conversations goes to the process owner. When there's a gap, the fix goes into the SOP, not into a new trigger phrase.

## What I'd change for a real deployment

- Add a "confidence too low" branch that escalates instead of answering when the generative answer can't cite a source.
- Version the knowledge base in the same repo as the test set so a change to an SOP forces a test run.
- Add a second flow for "log a question the SOP doesn't answer" so the gap list builds itself.

## Where this came from

This pattern comes from building Copilot Studio agents for finance users as part of day-to-day work, along with the "Building in Microsoft Copilot Studio" course on LinkedIn Learning. The case rebuilds it with invented content so the design is visible and nothing from an employer is.
