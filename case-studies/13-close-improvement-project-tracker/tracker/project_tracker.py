"""Project tracker for a synthetic month-end close improvement project.

Takes a plan (tasks with planned and actual dates, costs, percent complete) and a
risk register, and produces what a sponsor actually reads:

- earned value per workstream and for the project (PV, EV, AC, SPI, CPI, variances)
- milestone health as of the status date
- risk scores and the open items that need a decision
- a one-page status report in markdown, generated, not typed

Standard library only.
"""
from __future__ import annotations

import csv
import json
from collections import defaultdict
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
CASE = HERE.parent
CONFIG = json.loads((CASE / "case.json").read_text(encoding="utf-8"))["parameters"]


def read_csv(path: Path) -> list[dict]:
    with path.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


def d(s: str) -> date | None:
    return date.fromisoformat(s) if s else None


# ------------------------------------------------------------------ earned value
def planned_fraction(task: dict, status: date) -> float:
    """How much of the task should be done by the status date, by calendar time."""
    start, end = d(task["planned_start"]), d(task["planned_end"])
    if status < start:
        return 0.0
    if status >= end:
        return 1.0
    total = (end - start).days or 1
    return (status - start).days / total


def task_metrics(task: dict, status: date, cfg: dict | None = None) -> dict:
    cfg = cfg or CONFIG
    bac = float(task["planned_cost"])
    pv = bac * planned_fraction(task, status)
    ev = bac * float(task["percent_complete"]) / 100
    ac = float(task["actual_cost"])
    sv, cv = ev - pv, ev - ac
    spi = ev / pv if pv else (1.0 if ev == 0 else 0.0)
    cpi = ev / ac if ac else (1.0 if ev == 0 else 0.0)
    return {
        "task_id": task["task_id"], "workstream": task["workstream"], "task_name": task["task_name"],
        "milestone_flag": task["milestone_flag"], "owner_role": task["owner_role"],
        "bac": round(bac, 2), "pv": round(pv, 2), "ev": round(ev, 2), "ac": round(ac, 2),
        "sv": round(sv, 2), "cv": round(cv, 2), "spi": round(spi, 2), "cpi": round(cpi, 2),
        "schedule_status": rag(spi, cfg), "cost_status": rag(cpi, cfg),
    }


def rag(index: float, cfg: dict) -> str:
    if index >= cfg["spi_cpi_warning"]:
        return "GREEN"
    if index >= cfg["spi_cpi_critical"]:
        return "AMBER"
    return "RED"


def rollup(metrics: list[dict], cfg: dict | None = None) -> list[dict]:
    cfg = cfg or CONFIG
    groups = defaultdict(lambda: defaultdict(float))
    for m in metrics:
        for k in ("bac", "pv", "ev", "ac"):
            groups[m["workstream"]][k] += m[k]
            groups["TOTAL"][k] += m[k]
    order = []
    for m in metrics:
        if m["workstream"] not in order:
            order.append(m["workstream"])
    out = []
    for ws in order + ["TOTAL"]:
        g = groups[ws]
        spi = g["ev"] / g["pv"] if g["pv"] else 1.0
        cpi = g["ev"] / g["ac"] if g["ac"] else 1.0
        eac = g["bac"] / cpi if cpi else g["bac"]
        out.append({
            "workstream": ws, "bac": round(g["bac"], 2), "pv": round(g["pv"], 2), "ev": round(g["ev"], 2), "ac": round(g["ac"], 2),
            "sv": round(g["ev"] - g["pv"], 2), "cv": round(g["ev"] - g["ac"], 2),
            "spi": round(spi, 2), "cpi": round(cpi, 2),
            "eac": round(eac, 2), "vac": round(g["bac"] - eac, 2),
            "schedule_status": rag(spi, cfg), "cost_status": rag(cpi, cfg),
            "percent_complete": round(g["ev"] / g["bac"] * 100, 1) if g["bac"] else 0.0,
        })
    return out


# --------------------------------------------------------------------- milestones
def milestone_health(tasks: list[dict], status: date) -> list[dict]:
    out = []
    for t in tasks:
        if t["milestone_flag"] != "Y":
            continue
        planned, actual = d(t["planned_end"]), d(t["actual_end"])
        if actual:
            state = "ACHIEVED" if actual <= planned else "ACHIEVED_LATE"
            slip = (actual - planned).days
        elif status > planned:
            state = "MISSED"
            slip = (status - planned).days
        else:
            state = "ON_TRACK"
            slip = 0
        out.append({"task_id": t["task_id"], "milestone": t["task_name"], "planned_date": t["planned_end"],
                    "actual_date": t["actual_end"], "state": state, "slip_days": slip, "owner_role": t["owner_role"]})
    return out


# ------------------------------------------------------------------------- risks
def score_risks(risks: list[dict], cfg: dict | None = None) -> list[dict]:
    cfg = cfg or CONFIG
    out = []
    for r in risks:
        score = int(r["probability"]) * int(r["impact"])
        level = "HIGH" if score >= cfg["risk_high_score"] else "MEDIUM" if score >= cfg["risk_medium_score"] else "LOW"
        out.append({**r, "score": score, "level": level})
    out.sort(key=lambda r: (r["status"] != "Open", -r["score"], r["risk_id"]))
    return out


# ------------------------------------------------------------------------ report
def status_report(roll: list[dict], milestones: list[dict], risks: list[dict], status: date) -> str:
    total = roll[-1]
    open_high = [r for r in risks if r["status"] == "Open" and r["level"] == "HIGH"]
    late = [m for m in milestones if m["state"] in ("MISSED", "ACHIEVED_LATE")]
    lines = [
        f"# Close improvement project, status as of {status.isoformat()}",
        "",
        f"Overall: {total['percent_complete']}% earned, schedule {total['schedule_status']} (SPI {total['spi']}), cost {total['cost_status']} (CPI {total['cpi']}).",
        f"Estimate at completion {total['eac']:,.0f} against a budget of {total['bac']:,.0f} (variance at completion {total['vac']:,.0f}).",
        "",
        "## By workstream",
        "",
        "| Workstream | % complete | SPI | CPI | Schedule | Cost |",
        "|---|---|---|---|---|---|",
    ]
    lines += [f"| {r['workstream']} | {r['percent_complete']} | {r['spi']} | {r['cpi']} | {r['schedule_status']} | {r['cost_status']} |" for r in roll[:-1]]
    lines += ["", "## Milestones", "", "| Milestone | Planned | State | Slip (days) |", "|---|---|---|---|"]
    lines += [f"| {m['milestone']} | {m['planned_date']} | {m['state']} | {m['slip_days']} |" for m in milestones]
    lines += ["", "## Decisions needed", ""]
    if open_high:
        lines += [f"- {r['risk_id']} ({r['workstream']}, score {r['score']}): {r['description']}. Response: {r['response']}. Owner: {r['owner_role']}." for r in open_high]
    else:
        lines.append("- No open high risks.")
    if late:
        lines.append(f"- {len(late)} milestone(s) late or missed; see table above.")
    lines += ["", "Everything in this report is synthetic and generated by tracker/project_tracker.py.", ""]
    return "\n".join(lines)


# --------------------------------------------------------------------------- run
def run(out_dir: Path | None = None) -> dict:
    out_dir = out_dir or CASE / "expected-output"
    status = d(CONFIG["status_date"])
    tasks = read_csv(CASE / "sample-data" / "project_plan.csv")
    risks = read_csv(CASE / "sample-data" / "risk_register.csv")

    metrics = [task_metrics(t, status) for t in tasks]
    roll = rollup(metrics)
    ms = milestone_health(tasks, status)
    scored = score_risks(risks)

    write_csv(out_dir / "earned_value_by_task.csv", metrics)
    write_csv(out_dir / "earned_value_rollup.csv", roll)
    write_csv(out_dir / "milestone_health.csv", ms)
    write_csv(out_dir / "risk_scored.csv", scored)
    (out_dir / "status_report.md").write_text(status_report(roll, ms, scored, status), encoding="utf-8")

    total = roll[-1]
    summary = {
        "status_date": status.isoformat(), "tasks": len(tasks), "milestones": len(ms),
        "bac": total["bac"], "pv": total["pv"], "ev": total["ev"], "ac": total["ac"],
        "spi": total["spi"], "cpi": total["cpi"], "eac": total["eac"],
        "rollup_ties": "PASS" if abs(sum(m["bac"] for m in metrics) - total["bac"]) < 0.01 else "FAIL",
        "open_high_risks": sum(1 for r in scored if r["status"] == "Open" and r["level"] == "HIGH"),
        "milestones_late_or_missed": sum(1 for m in ms if m["state"] in ("MISSED", "ACHIEVED_LATE")),
    }
    with (out_dir / "control_summary.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["control_name", "control_value"])
        for k, v in summary.items():
            w.writerow([k, v])
    return summary


if __name__ == "__main__":
    for k, v in run().items():
        print(f"{k}: {v}")
