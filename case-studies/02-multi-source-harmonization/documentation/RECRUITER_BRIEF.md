# Recruiter Brief: Multi-Source Data Harmonization

**The short version:** Combining data from multiple systems that don't agree on naming or format, in a way where you can still trace every number back to its origin.

**Situation:** Records that represent the same thing arrive from different sources with different field names, formats, and status conventions.

**Task:** Get everything into one canonical shape without losing the ability to explain where any given value came from.

**Action:** Built a mapping layer that standardizes each source before comparison, validates period alignment, deduplicates on the canonical key, and preserves source lineage on every record.

**Result:** A working pattern for harmonizing multi-source data with full traceability, demonstrated on synthetic inputs.
