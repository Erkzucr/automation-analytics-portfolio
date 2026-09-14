# Recruiter Brief: Copilot Studio Finance Agent

**Short version:** A read-only agent that answers finance policy questions from approved SOPs, creates request records through a flow, and refuses anything else.

**Situation:** Senior finance staff spend time answering the same policy and process questions, and the answer depends on who is asked.

**Task:** Put the answers in one place with a citation, without creating a bot that can act on financial data.

**Action:** Built in Microsoft Copilot Studio with an allowlisted knowledge base, topic routing, one Power Automate action for request records, scripted refusals for action requests, and a versioned test set that runs in CI through a Python simulation of the routing.

**Result:** No write actions exist. Every answer cites a source. Gaps go back into the SOPs. The test set caught a routing miss on its first run.
