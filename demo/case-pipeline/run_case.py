"""Run one case study (or all of them) through the shared pipeline.

    python run_case.py 05          # writes case-studies/05-*/expected-output
    python run_case.py all
    python run_case.py 05 --check  # runs to a temp folder and compares with expected-output
"""
from __future__ import annotations

import filecmp
import sys
import tempfile
from pathlib import Path

from pipeline import run_case

ROOT = Path(__file__).resolve().parents[2]
CASES = ROOT / "case-studies"


def is_pipeline_case(d: Path) -> bool:
    """Cases 12 and 13 have their own case.json and their own scripts; the shared pipeline
    only owns the cases that use the input_primary / input_reference layout."""
    return (d / "case.json").exists() and (d / "sample-data" / "input_primary.csv").exists()


def find_case(prefix: str) -> Path:
    matches = sorted(CASES.glob(f"{prefix}-*"))
    if not matches:
        raise SystemExit(f"no case starting with {prefix}")
    return matches[0]


def check(case_dir: Path) -> bool:
    with tempfile.TemporaryDirectory() as tmp:
        run_case(case_dir, Path(tmp))
        ok = True
        for name in ("accepted_records.csv", "exception_records.csv", "control_summary.csv"):
            if not filecmp.cmp(Path(tmp) / name, case_dir / "expected-output" / name, shallow=False):
                print(f"  DIFF {case_dir.name}/{name}")
                ok = False
        return ok


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__)
        return 2
    target, flags = argv[0], argv[1:]
    dirs = sorted(d for d in CASES.iterdir() if is_pipeline_case(d)) if target == "all" else [find_case(target)]
    failed = 0
    for d in dirs:
        if "--check" in flags:
            ok = check(d)
            print(f"{'ok  ' if ok else 'FAIL'} {d.name}")
            failed += 0 if ok else 1
        else:
            s = run_case(d)
            print(f"{d.name}: {s['accepted_count']} accepted, {s['exception_count']} exceptions, tie-out {s['count_tie_out']}/{s['total_tie_out']}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
