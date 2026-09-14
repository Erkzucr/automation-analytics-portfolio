"""Run the conversation test set through the routing simulation."""
from __future__ import annotations

import csv
from pathlib import Path

from agent_router import load_triggers, route

HERE = Path(__file__).resolve().parent
INPUT = HERE / "test_conversations.csv"
OUT_DIR = HERE.parent / "expected-output"


def run() -> tuple[list[dict], dict]:
    triggers = load_triggers()
    results: list[dict] = []
    with INPUT.open(encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            actual, matched = route(row["user_message"], triggers)
            results.append({
                "case_id": row["case_id"],
                "expected_topic": row["expected_topic"],
                "actual_topic": actual,
                "matched_trigger": matched or "",
                "passed": actual == row["expected_topic"],
            })
    passed = sum(1 for r in results if r["passed"])
    refusals = sum(1 for r in results if r["actual_topic"] == "T05")
    summary = {
        "test_cases": len(results),
        "passed": passed,
        "failed": len(results) - passed,
        "refusal_routed": refusals,
        "fallback_routed": sum(1 for r in results if r["actual_topic"] == "T99"),
        "pass_rate": f"{passed / len(results):.0%}" if results else "n/a",
    }
    return results, summary


def write(results: list[dict], summary: dict) -> None:
    OUT_DIR.mkdir(exist_ok=True)
    with (OUT_DIR / "routing_results.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(results[0].keys()))
        w.writeheader()
        w.writerows(results)
    with (OUT_DIR / "evaluation_summary.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["control_name", "control_value"])
        for k, v in summary.items():
            w.writerow([k, v])


if __name__ == "__main__":
    results, summary = run()
    write(results, summary)
    for r in results:
        flag = "ok " if r["passed"] else "FAIL"
        print(f"{flag} {r['case_id']} expected {r['expected_topic']} got {r['actual_topic']} ({r['matched_trigger'] or 'no trigger'})")
    print()
    for k, v in summary.items():
        print(f"{k}: {v}")
    if summary["failed"]:
        raise SystemExit(1)
