"""Shared pipeline for case studies 01 to 09.

Every case README describes the same skeleton: validate, standardize, apply the
case's logic, split accepted from exceptions, summarize, tie out. This module is
that skeleton in code. Each case supplies a small case.json with its key fields,
its reference rules, and which logic block applies. The expected-output folder
of every case is produced by this code, so if the logic changes, the tests say so.

No pandas on purpose. The point is to be readable by a reviewer, not fast.
"""
from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path

REQUIRED_DEFAULT = ["record_id", "period_key", "dimension_a", "dimension_b", "category_code", "value_amount", "status_code"]


# ----------------------------------------------------------------------------- io
def read_csv(path: Path) -> list[dict]:
    with path.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in fieldnames})


def load_config(case_dir: Path) -> dict:
    cfg = json.loads((case_dir / "case.json").read_text(encoding="utf-8"))
    cfg.setdefault("required_fields", REQUIRED_DEFAULT)
    cfg.setdefault("key_field", "record_id")
    cfg.setdefault("reference_key", "dimension_a")
    cfg.setdefault("logic", "none")
    cfg.setdefault("parameters", {})
    return cfg


# ------------------------------------------------------------------- standardize
def standardize(row: dict) -> dict:
    out = {}
    for k, v in row.items():
        v = (v or "").strip()
        if k in ("record_id", "period_key", "dimension_a", "dimension_b", "category_code", "status_code"):
            v = v.upper()
        out[k] = v
    return out


# --------------------------------------------------------------------- validate
def validate(rows: list[dict], reference: list[dict], cfg: dict) -> tuple[list[dict], list[dict]]:
    """Return (clean_rows, exceptions). Exceptions carry an exception_reason."""
    key = cfg["key_field"]
    ref_key = cfg["reference_key"]
    ref_status = {r[ref_key].strip().upper(): r.get("reference_status", "").strip().upper() for r in reference}
    seen = defaultdict(int)
    for r in rows:
        seen[r.get(key, "")] += 1

    clean, exceptions = [], []
    for r in rows:
        reason = None
        missing = [f for f in cfg["required_fields"] if not r.get(f)]
        if missing:
            reason = f"MISSING_FIELD:{','.join(missing)}"
        else:
            try:
                r["value_amount"] = f"{float(r['value_amount']):.2f}"
            except ValueError:
                reason = "INVALID_AMOUNT"
        if reason is None and seen[r[key]] > 1:
            reason = "DUPLICATE_KEY"
        if reason is None:
            if r[ref_key] not in ref_status:
                reason = "UNMAPPED_REFERENCE"
            elif ref_status[r[ref_key]] != "ACTIVE":
                reason = "INACTIVE_REFERENCE"
        if reason:
            exceptions.append({**r, "exception_reason": reason})
        else:
            clean.append(r)
    return clean, exceptions


# ------------------------------------------------------------------- case logic
def logic_none(rows, cfg):
    return rows, []


def logic_estimate_reasonableness(rows, cfg):
    """01: an estimate above the per-category ceiling goes to review."""
    ceilings = cfg["parameters"]["category_ceiling"]
    ok, ex = [], []
    for r in rows:
        ceiling = ceilings.get(r["category_code"])
        if ceiling is not None and float(r["value_amount"]) > ceiling:
            ex.append({**r, "exception_reason": "ABOVE_CATEGORY_CEILING"})
        else:
            ok.append(r)
    return ok, ex


def logic_period_allowlist(rows, cfg):
    """02: a period not in the harmonization map can't be aligned."""
    allowed = set(cfg["parameters"]["allowed_periods"])
    ok, ex = [], []
    for r in rows:
        if r["period_key"] in allowed:
            ok.append(r)
        else:
            ex.append({**r, "exception_reason": "UNKNOWN_PERIOD"})
    return ok, ex


def logic_priority(rows, cfg):
    """04: everything passes, but each row gets a review priority by amount."""
    bands = cfg["parameters"]["priority_bands"]  # list of [threshold, label], descending
    for r in rows:
        amt = float(r["value_amount"])
        r["priority"] = next((label for threshold, label in bands if amt >= threshold), "LOW")
    return rows, []


def logic_period_movement(rows, cfg):
    """06: compare each dimension's total against the prior period. Moves above the
    absolute threshold (materiality style, not a percentage) send that dimension-period to review."""
    threshold = cfg["parameters"]["movement_threshold_amount"]
    totals = defaultdict(float)
    for r in rows:
        totals[(r["dimension_a"], r["period_key"])] += float(r["value_amount"])
    periods = sorted({p for _, p in totals})
    prior = {p: periods[i - 1] for i, p in enumerate(periods) if i > 0}
    ok, ex = [], []
    for r in rows:
        p = r["period_key"]
        if p in prior:
            base = totals.get((r["dimension_a"], prior[p]), 0.0)
            move = totals[(r["dimension_a"], p)] - base
            r["movement_amount"] = f"{move:.2f}"
            if abs(move) > threshold:
                ex.append({**r, "exception_reason": "MOVEMENT_ABOVE_THRESHOLD"})
                continue
        else:
            r["movement_amount"] = ""
        ok.append(r)
    return ok, ex


def logic_policy_rate(rows, cfg):
    """07: apply the policy rate per category. A category with no policy is an exception."""
    rates = cfg["parameters"]["policy_rate_by_category"]
    ok, ex = [], []
    for r in rows:
        rate = rates.get(r["category_code"])
        if rate is None:
            ex.append({**r, "exception_reason": "NO_POLICY_FOR_CATEGORY"})
        else:
            r["policy_rate"] = f"{rate:.4f}"
            r["computed_amount"] = f"{float(r['value_amount']) * rate:.2f}"
            ok.append(r)
    return ok, ex


LOGIC = {
    "none": logic_none,
    "estimate_reasonableness": logic_estimate_reasonableness,
    "period_allowlist": logic_period_allowlist,
    "priority": logic_priority,
    "period_movement": logic_period_movement,
    "policy_rate": logic_policy_rate,
}


# ------------------------------------------------------------------------- run
def run_case(case_dir: Path, out_dir: Path | None = None) -> dict:
    cfg = load_config(case_dir)
    out_dir = out_dir or case_dir / "expected-output"
    primary = [standardize(r) for r in read_csv(case_dir / "sample-data" / "input_primary.csv")]
    reference = read_csv(case_dir / "sample-data" / "input_reference.csv")

    clean, exceptions = validate(primary, reference, cfg)

    # status routing: anything the source already flagged goes to review
    routed = []
    for r in clean:
        if r["status_code"] != "VALID":
            exceptions.append({**r, "exception_reason": f"SOURCE_STATUS_{r['status_code']}"})
        else:
            routed.append(r)

    accepted, logic_ex = LOGIC[cfg["logic"]](routed, cfg)
    exceptions.extend(logic_ex)

    accepted.sort(key=lambda r: r["record_id"])
    exceptions.sort(key=lambda r: r["record_id"])

    input_total = sum(float(r["value_amount"]) for r in primary if _is_number(r.get("value_amount")))
    accepted_total = sum(float(r["value_amount"]) for r in accepted)
    exception_total = sum(float(r["value_amount"]) for r in exceptions if _is_number(r.get("value_amount")))
    summary = {
        "input_count": len(primary),
        "accepted_count": len(accepted),
        "exception_count": len(exceptions),
        "input_total": f"{input_total:.2f}",
        "accepted_total": f"{accepted_total:.2f}",
        "exception_total": f"{exception_total:.2f}",
        "count_tie_out": "PASS" if len(accepted) + len(exceptions) == len(primary) else "FAIL",
        "total_tie_out": "PASS" if abs(input_total - accepted_total - exception_total) < 0.005 else "FAIL",
    }
    by_reason = defaultdict(int)
    for e in exceptions:
        by_reason[e["exception_reason"].split(":")[0]] += 1
    for reason, n in sorted(by_reason.items()):
        summary[f"exceptions_{reason.lower()}"] = n

    extra_cols = [c for c in ("priority", "movement_amount", "policy_rate", "computed_amount") if any(c in r for r in accepted)]
    acc_fields = REQUIRED_DEFAULT + extra_cols
    write_csv(out_dir / "accepted_records.csv", accepted, acc_fields)
    write_csv(out_dir / "exception_records.csv", exceptions, REQUIRED_DEFAULT + ["exception_reason"])
    with (out_dir / "control_summary.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["control_name", "control_value"])
        for k, v in summary.items():
            w.writerow([k, v])
    return summary


def _is_number(v) -> bool:
    try:
        float(v)
        return True
    except (TypeError, ValueError):
        return False
