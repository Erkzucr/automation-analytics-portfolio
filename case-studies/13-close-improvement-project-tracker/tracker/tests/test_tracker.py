import filecmp
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))

from project_tracker import CASE, milestone_health, planned_fraction, rag, rollup, run, score_risks, task_metrics  # noqa: E402

CFG = {"spi_cpi_warning": 0.95, "spi_cpi_critical": 0.85, "risk_high_score": 12, "risk_medium_score": 6}


def task(**kw):
    base = {"task_id": "T", "workstream": "W", "task_name": "n", "planned_start": "2026-01-01", "planned_end": "2026-01-11",
            "actual_start": "", "actual_end": "", "planned_cost": "1000", "actual_cost": "0", "percent_complete": "0",
            "milestone_flag": "N", "owner_role": "r"}
    base.update(kw)
    return base


class TrackerTests(unittest.TestCase):
    def test_planned_fraction_is_linear_in_time(self):
        t = task()
        self.assertEqual(planned_fraction(t, date(2025, 12, 31)), 0.0)
        self.assertAlmostEqual(planned_fraction(t, date(2026, 1, 6)), 0.5)
        self.assertEqual(planned_fraction(t, date(2026, 2, 1)), 1.0)

    def test_earned_value_math(self):
        m = task_metrics(task(actual_cost="600", percent_complete="50"), date(2026, 1, 6), CFG)
        self.assertEqual((m["pv"], m["ev"], m["ac"]), (500.0, 500.0, 600.0))
        self.assertEqual(m["spi"], 1.0)
        self.assertAlmostEqual(m["cpi"], 0.83, places=2)
        self.assertEqual(m["schedule_status"], "GREEN")
        self.assertEqual(m["cost_status"], "RED")

    def test_rag_thresholds(self):
        self.assertEqual(rag(0.95, CFG), "GREEN")
        self.assertEqual(rag(0.90, CFG), "AMBER")
        self.assertEqual(rag(0.84, CFG), "RED")

    def test_rollup_total_equals_sum_of_workstreams(self):
        ms = [task_metrics(task(task_id="A", workstream="X", percent_complete="100", actual_cost="1000"), date(2026, 2, 1), CFG),
              task_metrics(task(task_id="B", workstream="Y", percent_complete="0"), date(2026, 2, 1), CFG)]
        r = rollup(ms, CFG)
        self.assertEqual(r[-1]["workstream"], "TOTAL")
        self.assertEqual(r[-1]["bac"], r[0]["bac"] + r[1]["bac"])
        self.assertEqual(r[-1]["ev"], 1000.0)

    def test_milestone_states(self):
        status = date(2026, 3, 1)
        t_ok = task(milestone_flag="Y", planned_end="2026-03-10")
        t_missed = task(milestone_flag="Y", planned_end="2026-02-20")
        t_late = task(milestone_flag="Y", planned_end="2026-02-20", actual_end="2026-02-25")
        t_hit = task(milestone_flag="Y", planned_end="2026-02-20", actual_end="2026-02-19")
        states = [m["state"] for m in milestone_health([t_ok, t_missed, t_late, t_hit], status)]
        self.assertEqual(states, ["ON_TRACK", "MISSED", "ACHIEVED_LATE", "ACHIEVED"])
        self.assertEqual(milestone_health([t_missed], status)[0]["slip_days"], 9)

    def test_risk_scoring_and_order(self):
        risks = [{"risk_id": "R1", "workstream": "w", "description": "d", "probability": "2", "impact": "2", "response": "", "owner_role": "", "status": "Open"},
                 {"risk_id": "R2", "workstream": "w", "description": "d", "probability": "4", "impact": "4", "response": "", "owner_role": "", "status": "Open"},
                 {"risk_id": "R3", "workstream": "w", "description": "d", "probability": "5", "impact": "5", "response": "", "owner_role": "", "status": "Closed"}]
        s = score_risks(risks, CFG)
        self.assertEqual([r["risk_id"] for r in s], ["R2", "R1", "R3"])  # open first, then score
        self.assertEqual([r["level"] for r in s], ["HIGH", "LOW", "HIGH"])

    def test_expected_output_is_reproducible(self):
        with tempfile.TemporaryDirectory() as tmp:
            s = run(Path(tmp))
            self.assertEqual(s["rollup_ties"], "PASS")
            for name in ("earned_value_by_task.csv", "earned_value_rollup.csv", "milestone_health.csv", "risk_scored.csv", "status_report.md", "control_summary.csv"):
                self.assertTrue(filecmp.cmp(Path(tmp) / name, CASE / "expected-output" / name, shallow=False), name)


if __name__ == "__main__":
    unittest.main()
