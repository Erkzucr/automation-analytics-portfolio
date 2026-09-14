import csv
import filecmp
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))

from variance_analysis import CASE, decompose, kpis, read_rows, run  # noqa: E402

CFG = {"material_amount": 15000, "material_pct": 5.0}


class VarianceTests(unittest.TestCase):
    def test_decomposition_sums_to_total_variance_on_every_line(self):
        for r in read_rows(CASE / "sample-data" / "people_cost_monthly.csv"):
            d = decompose(r, CFG)
            pieces = d["headcount_effect"] + d["rate_effect"] + d["mix_effect"] + d["one_off_effect"]
            self.assertAlmostEqual(pieces, d["variance"], places=1, msg=f"{r['cost_center']} {r['country']} {r['period']}")

    def test_pure_headcount_variance_lands_in_headcount(self):
        d = decompose({"period": "P", "cost_center": "X", "country": "Y", "budget_headcount": 10, "budget_rate": 4000.0,
                       "actual_headcount": 15, "actual_rate": 4000.0, "one_off_amount": 0.0, "revenue": 1.0}, CFG)
        self.assertEqual(d["variance"], 20000.0)
        self.assertEqual(d["headcount_effect"], 20000.0)
        self.assertEqual(d["rate_effect"], 0.0)
        self.assertEqual(d["material_flag"], "YES")
        self.assertEqual(d["primary_driver"], "HEADCOUNT")

    def test_material_needs_both_amount_and_percent(self):
        small_pct = decompose({"period": "P", "cost_center": "X", "country": "Y", "budget_headcount": 200, "budget_rate": 5000.0,
                               "actual_headcount": 200, "actual_rate": 5100.0, "one_off_amount": 0.0, "revenue": 1.0}, CFG)
        self.assertEqual(small_pct["variance"], 20000.0)
        self.assertEqual(small_pct["material_flag"], "NO")  # 2% on a big base
        small_amt = decompose({"period": "P", "cost_center": "X", "country": "Y", "budget_headcount": 2, "budget_rate": 3000.0,
                               "actual_headcount": 3, "actual_rate": 3000.0, "one_off_amount": 0.0, "revenue": 1.0}, CFG)
        self.assertEqual(small_amt["material_flag"], "NO")  # 50% on a tiny base

    def test_kpis_one_row_per_period(self):
        rows = read_rows(CASE / "sample-data" / "people_cost_monthly.csv")
        k = kpis([decompose(r, CFG) for r in rows], rows)
        self.assertEqual([x["period"] for x in k], sorted({r["period"] for r in rows}))
        for x in k:
            self.assertTrue(0 < x["people_cost_pct_revenue"] < 100)

    def test_expected_output_is_reproducible(self):
        with tempfile.TemporaryDirectory() as tmp:
            s = run(Path(tmp), with_chart=False)
            self.assertEqual(s["decomposition_ties"], "PASS")
            for name in ("variance_detail.csv", "kpi_summary.csv", "material_variances.csv", "control_summary.csv"):
                self.assertTrue(filecmp.cmp(Path(tmp) / name, CASE / "expected-output" / name, shallow=False), name)


if __name__ == "__main__":
    unittest.main()
