# Control Matrix

| ID | Objective | Procedure | Evidence |
|---|---|---|---|
| CTL-01 | Agent only answers from approved sources | Knowledge allowlisted, web and general knowledge disabled | `agent-config/topics.yaml` knowledge_sources, web_browsing |
| CTL-02 | Every answer is traceable | Citation to SOP section required in T01 to T03 | `agent-config/topics.yaml` response_rule |
| CTL-03 | Agent cannot act on financial data | No write action exists; only `create_request_record` | `documentation/AGENT_DESIGN.md`, ADR-006 |
| CTL-04 | Action requests are refused, not improvised | T05 wins routing priority over every knowledge topic | `evaluation/agent_router.py` PRIORITY, test C16 |
| CTL-05 | Unknown questions don't get guessed | Fallback T99 asks to rephrase then escalates and logs | `evaluation/test_conversations.csv` C14, C15 |
| CTL-06 | Routing changes are tested before publish | 18-case conversation set runs in CI | `evaluation/tests/test_router.py`, `expected-output/` |
| CTL-07 | Gaps go back to the SOPs | Weekly review of unanswered and escalated conversations | `agent-config/topics.yaml` logging, AGENT_DESIGN.md |
