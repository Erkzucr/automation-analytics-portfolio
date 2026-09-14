import csv
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))

from pipeline import run_case, validate, standardize  # noqa: E402
from run_case import CASES, check, is_pipeline_case  # noqa: E402

CASE_DIRS = sorted(d for d in CASES.iterdir() if is_pipeline_case(d))
EDGE_REASONS = {"MISSING_FIELD", "DUPLICATE_KEY", "UNMAPPED_REFERENCE", "INVALID_AMOUNT", "INACTIVE_REFERENCE", "SOURCE_STATUS_REVIEW"}


class PipelineTests(unittest.TestCase):
    def test_nine_cases_are_configured(self):
        self.assertEqual(len(CASE_DIRS), 9)

    def test_expected_output_is_reproducible(self):
        """The committed expected-output of every case is exactly what the pipeline produces."""
        for d in CASE_DIRS:
            with self.subTest(case=d.name):
                self.assertTrue(check(d), f"{d.name} expected-output is stale; run run_case.py {d.name[:2]}")

    def test_tie_outs_pass_and_every_edge_case_is_exercised(self):
        for d in CASE_DIRS:
            with self.subTest(case=d.name), tempfile.TemporaryDirectory() as tmp:
                summary = run_case(d, Path(tmp))
                self.assertEqual(summary["count_tie_out"], "PASS")
                self.assertEqual(summary["total_tie_out"], "PASS")
                reasons = {r["exception_reason"].split(":")[0] for r in csv.DictReader((Path(tmp) / "exception_records.csv").open())}
                self.assertTrue(EDGE_REASONS <= reasons, f"{d.name} missing {EDGE_REASONS - reasons}")

    def test_standardize_lets_messy_but_valid_rows_through(self):
        row = standardize({"record_id": "rec00025", "period_key": "p01 ", "dimension_a": " da003", "dimension_b": "DB005",
                           "category_code": "cat01", "value_amount": " 980.5 ", "status_code": "valid"})
        clean, ex = validate([row], [{"dimension_a": "DA003", "reference_status": "ACTIVE"}], {"required_fields": list(row), "key_field": "record_id", "reference_key": "dimension_a"})
        self.assertEqual(len(clean), 1)
        self.assertEqual(clean[0]["value_amount"], "980.50")
        self.assertEqual(clean[0]["status_code"], "VALID")

    def test_case_specific_logic_fires(self):
        expectations = {"01": "ABOVE_CATEGORY_CEILING", "02": "UNKNOWN_PERIOD", "06": "MOVEMENT_ABOVE_THRESHOLD", "07": "NO_POLICY_FOR_CATEGORY"}
        for d in CASE_DIRS:
            want = expectations.get(d.name[:2])
            if not want:
                continue
            with self.subTest(case=d.name), tempfile.TemporaryDirectory() as tmp:
                run_case(d, Path(tmp))
                reasons = {r["exception_reason"] for r in csv.DictReader((Path(tmp) / "exception_records.csv").open())}
                self.assertIn(want, reasons)


if __name__ == "__main__":
    unittest.main()
