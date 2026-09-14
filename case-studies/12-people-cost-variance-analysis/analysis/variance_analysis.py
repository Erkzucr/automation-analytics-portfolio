"""People cost variance analysis on synthetic data.

Reads budget vs actual headcount and loaded rate by cost center, country and month,
and does the three things a reviewer actually asks for:

1. Decompose the variance into headcount, rate, mix (the cross term) and one-offs,
   so "people cost is 12% over" turns into "we hired 4 people early and rates moved 2%".
2. Flag what's material by an absolute threshold and a percentage, both, because a
   small cost center can be 40% over and not matter and a big one can be 3% over and matter a lot.
3. Produce the KPIs that go on the monthly page: people cost as % of revenue,
   loaded cost per FTE, budget accuracy.

Standard library only. If matplotlib is installed it also draws a variance bridge.
"""
from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
CASE = HERE.parent
CONFIG = json.loads((CASE / "case.json").read_text(encoding="utf-8"))["parameters"]


def read_rows(path: Path) -> list[dict]:
    with path.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        for k in ("budget_headcount", "actual_headcount"):
            r[k] = int(r[k])
        for k in ("budget_rate", "actual_rate", "one_off_amount", "revenue"):
            r[k] = float(r[k])
    return rows


def decompose(r: dict, config: dict | None = None) -> dict:
    """budget = bh*br ; actual = ah*ar + one_off.
    headcount effect = (ah-bh)*br ; rate effect = (ar-br)*bh ; mix = (ah-bh)*(ar-br).
    The four pieces sum exactly to actual minus budget, which is what the test checks."""
    cfg = config or CONFIG
    bh, br, ah, ar, oo = r["budget_headcount"], r["budget_rate"], r["actual_headcount"], r["actual_rate"], r["one_off_amount"]
    budget = bh * br
    actual = ah * ar + oo
    hc = (ah - bh) * br
    rate = (ar - br) * bh
    mix = (ah - bh) * (ar - br)
    total = actual - budget
    pct = total / budget * 100 if budget else 0.0
    material = abs(total) >= cfg["material_amount"] and abs(pct) >= cfg["material_pct"]
    driver = max((("HEADCOUNT", hc), ("RATE", rate), ("ONE_OFF", oo), ("MIX", mix)), key=lambda kv: abs(kv[1]))[0]
    return {
        "period": r["period"], "cost_center": r["cost_center"], "country": r["country"],
        "budget_cost": round(budget, 2), "actual_cost": round(actual, 2),
        "variance": round(total, 2), "variance_pct": round(pct, 1),
        "headcount_effect": round(hc, 2), "rate_effect": round(rate, 2),
        "mix_effect": round(mix, 2), "one_off_effect": round(oo, 2),
        "material_flag": "YES" if material else "NO",
        "primary_driver": driver if material else "",
    }


def kpis(lines: list[dict], rows: list[dict]) -> list[dict]:
    by_period = defaultdict(lambda: {"budget": 0.0, "actual": 0.0, "revenue": 0.0, "fte": 0, "material": 0})
    for line, r in zip(lines, rows):
        p = by_period[line["period"]]
        p["budget"] += line["budget_cost"]
        p["actual"] += line["actual_cost"]
        p["revenue"] += r["revenue"]
        p["fte"] += r["actual_headcount"]
        p["material"] += line["material_flag"] == "YES"
    out = []
    for period in sorted(by_period):
        p = by_period[period]
        out.append({
            "period": period,
            "people_cost": round(p["actual"], 2),
            "budget": round(p["budget"], 2),
            "variance_pct": round((p["actual"] - p["budget"]) / p["budget"] * 100, 1),
            "people_cost_pct_revenue": round(p["actual"] / p["revenue"] * 100, 1),
            "loaded_cost_per_fte": round(p["actual"] / p["fte"], 2) if p["fte"] else 0,
            "budget_accuracy_pct": round(100 - abs(p["actual"] - p["budget"]) / p["budget"] * 100, 1),
            "material_lines": p["material"],
        })
    return out


def write(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


def bridge_chart(lines: list[dict], path: Path) -> bool:
    try:
        import matplotlib
        import matplotlib.ticker
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        return False
    tot = {k: sum(l[k] for l in lines) for k in ("headcount_effect", "rate_effect", "mix_effect", "one_off_effect")}
    budget = sum(l["budget_cost"] for l in lines)
    actual = sum(l["actual_cost"] for l in lines)
    labels = ["Budget", "Headcount", "Rate", "Mix", "One-offs", "Actual"]
    vals = [budget, tot["headcount_effect"], tot["rate_effect"], tot["mix_effect"], tot["one_off_effect"], actual]
    fig, ax = plt.subplots(figsize=(9, 4.5), dpi=140)
    run_total = 0.0
    for i, (lab, v) in enumerate(zip(labels, vals)):
        if i in (0, 5):
            ax.bar(lab, v, color="#163A5F")
            run_total = v
            top = v
        else:
            bottom = run_total if v >= 0 else run_total + v
            ax.bar(lab, abs(v), bottom=bottom, color="#C65911" if v > 0 else "#2E7D32")
            run_total += v
            top = max(bottom + abs(v), run_total)
        ax.text(i, top + budget * 0.01, f"{v / 1000:,.0f}k", ha="center", fontsize=9)
    ax.set_title("People cost variance bridge, six months, synthetic data", loc="left", fontweight="bold")
    ax.set_ylabel("Amount (millions)")
    ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"{v / 1e6:.1f}M"))
    ax.spines[["top", "right"]].set_visible(False)
    ax.tick_params(length=0)
    ax.set_ylim(min(budget, actual) * 0.9, max(budget, actual) * 1.06)
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)
    return True


def run(out_dir: Path | None = None, with_chart: bool = True) -> dict:
    out_dir = out_dir or CASE / "expected-output"
    rows = read_rows(CASE / "sample-data" / "people_cost_monthly.csv")
    lines = [decompose(r) for r in rows]
    write(out_dir / "variance_detail.csv", lines)
    write(out_dir / "kpi_summary.csv", kpis(lines, rows))
    material = sorted((l for l in lines if l["material_flag"] == "YES"), key=lambda l: -abs(l["variance"]))
    write(out_dir / "material_variances.csv", material)
    budget = round(sum(l["budget_cost"] for l in lines), 2)
    actual = round(sum(l["actual_cost"] for l in lines), 2)
    pieces = round(sum(l["headcount_effect"] + l["rate_effect"] + l["mix_effect"] + l["one_off_effect"] for l in lines), 2)
    summary = {
        "lines": len(lines),
        "budget_total": budget,
        "actual_total": actual,
        "variance_total": round(actual - budget, 2),
        "decomposition_ties": "PASS" if abs(pieces - (actual - budget)) < 0.05 else "FAIL",
        "material_lines": len(material),
    }
    with (out_dir / "control_summary.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["control_name", "control_value"])
        for k, v in summary.items():
            w.writerow([k, v])
    if with_chart:
        bridge_chart(lines, out_dir / "variance_bridge.png")
    return summary


if __name__ == "__main__":
    for k, v in run().items():
        print(f"{k}: {v}")
