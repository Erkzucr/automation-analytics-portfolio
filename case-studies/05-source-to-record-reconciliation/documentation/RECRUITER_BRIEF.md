# Recruiter Brief: Source-to-Record Reconciliation

**Short version:** Matching two independently generated datasets and deciding what happens to everything that doesn't match.

**Situation:** Source and record-of-truth datasets that should agree, but differ because of formatting, timing, or actual breaks.

**Task:** Reconcile the two without hiding unmatched records behind an inner join.

**Action:** Standardized both sides, ran a full outer match, calculated differences, and classified breaks by type instead of dumping everything into one generic "exception" bucket.

**Result:** A reconciliation pattern where matched, missing, and broken records are all visible, with the summary tying back to detail every time.
