# Recruiter Brief: Policy-Driven Calculation Governance

**Short version:** Governing a recurring calculation whose rules change over time, so you can always answer "what rule applied when."

**Situation:** Rules, assumptions, and approvals for a recurring calculation were inconsistently tracked.

**Task:** Make rule changes auditable instead of silently overwriting the previous version.

**Action:** Moved rules into a versioned table, validated that only active and approved versions apply, logged assumptions per run, and built a movement view comparing results to the prior rule version.

**Result:** A governed calculation pattern where every output can be traced back to the exact rule version that produced it.
