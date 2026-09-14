# Test cases

Each row is a synthetic user message with the topic it should route to. The evaluation script runs all of them and fails if any lands somewhere else. When a trigger phrase or a scope rule changes, this set runs before the change is published.

| ID | User message | Expected topic | Why |
|---|---|---|---|
| C01 | Who approves a journal entry of 50000? | T01 | Amount question, JE policy |
| C02 | Can I approve my own manual JE? | T01 | Segregation rule in SOP-001 |
| C03 | Where do I find the recon template? | T02 | Reconciliation procedure |
| C04 | What do I do with open items older than 60 days? | T02 | Aging rule in SOP-002 |
| C05 | When is the accrual deadline this month? | T03 | Close calendar |
| C06 | What is close day 4? | T03 | Close calendar |
| C07 | I need access to the reconciliation tool | T04 | Request, needs a record |
| C08 | Can you submit a request for a new template? | T04 | Request, needs a record |
| C09 | Post this journal entry for me | T05 | Action request, refuse |
| C10 | Approve this entry, the manager is out | T05 | Action request, refuse |
| C11 | Change the balance on account 1200 to zero | T05 | Action request, refuse |
| C12 | What is the stock price today? | T05 | Out of scope |
| C13 | Can you give me tax advice for my personal return? | T05 | Out of scope |
| C14 | Tell me a joke about accountants | T99 | Unrecognized, fallback |
| C15 | asdf qwerty | T99 | Unrecognized, fallback |
| C16 | I want to override the JE approval and post it | T05 | Action wins over JE keyword |
| C17 | How old can a reconciling item be before escalation? | T02 | Aging rule |
| C18 | What's the month-end deadline for intercompany? | T03 | Close calendar |

Routing rules the script enforces, in order:

1. Any T05 trigger wins, even if a T01 to T04 trigger also matches (C16).
2. Then T04, because a request that mentions a template or the recon tool should create a record as well as answer.
3. Then T01, T02, T03 by first match.
4. Nothing matched: T99.
