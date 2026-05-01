"""Quality-control regression runner for notebook phases 1-10."""

import csv
import asyncio
import gc
import sys
import time
from pathlib import Path

import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
from traitlets import TraitError


PROJECT_ROOT = Path(__file__).resolve().parent.parent
NOTEBOOK_DIR = PROJECT_ROOT / "notebooks"
CSV_PATH = PROJECT_ROOT / "reports" / "tables" / "regression_tracker.csv"

NOTEBOOKS = [
    (1, "01_Business_Understanding.ipynb"),
    (2, "02_Data_Understanding.ipynb"),
    (3, "03_Preprocessing.ipynb"),
    (4, "04_EDA.ipynb"),
    (5, "05_Merge_Analysis.ipynb"),
    (6, "06_Demand_Classification.ipynb"),
    (7, "07_Feature_Engineering.ipynb"),
    (8, "08_Model_Training.ipynb"),
    (9, "09_Cross_Validation.ipynb"),
    (10, "10_Forecasting.ipynb"),
]

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


def create_execute_preprocessor(timeout: int = 1800) -> ExecutePreprocessor:
    """Create ExecutePreprocessor, preferring kernel_name=None when supported."""
    try:
        return ExecutePreprocessor(timeout=timeout, kernel_name=None)
    except TraitError:
        return ExecutePreprocessor(timeout=timeout)


def run_notebook(notebook_path: Path, timeout: int = 1800):
    """Run a notebook and return (status, error_message, elapsed_time)."""
    start = time.time()

    try:
        with notebook_path.open("r", encoding="utf-8") as f:
            nb = nbformat.read(f, as_version=4)

        ep = create_execute_preprocessor(timeout=timeout)
        ep.preprocess(nb, {"metadata": {"path": str(PROJECT_ROOT)}})

        with notebook_path.open("w", encoding="utf-8") as f:
            nbformat.write(nb, f)

        elapsed = round(time.time() - start, 1)
        return "PASS", "", elapsed
    except Exception as exc:
        elapsed = round(time.time() - start, 1)
        error = str(exc).splitlines()[0][:300]
        return "FAIL", error, elapsed
    finally:
        gc.collect()


def save_tracker(tracker, csv_path: Path) -> None:
    csv_path.parent.mkdir(parents=True, exist_ok=True)

    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Phase", "Notebook", "Status", "Time(sec)", "Error"])
        writer.writerows(tracker)


def print_tracker(tracker) -> None:
    print("\n## PHASE NOTEBOOK REGRESSION TRACKER\n")
    print(f"{'Phase':<5} | {'Notebook':<32} | {'Status':<6} | {'Time(sec)':<9}")
    print("-" * 62)
    for phase, notebook, status, elapsed, _error in tracker:
        print(f"{phase:<5} | {notebook:<32} | {status:<6} | {elapsed:<9}")

    passed = sum(1 for row in tracker if row[2] == "PASS")
    failed = sum(1 for row in tracker if row[2] == "FAIL")

    print(f"\nTotal PASS: {passed}")
    print(f"Total FAIL: {failed}")

    if failed:
        print("\nFailures:")
        for phase, notebook, status, _elapsed, error in tracker:
            if status == "FAIL":
                print(f"Phase {phase} | {notebook} | {error}")


def main() -> int:
    tracker = []

    for phase, notebook_name in NOTEBOOKS:
        notebook_path = NOTEBOOK_DIR / notebook_name
        if not notebook_path.exists():
            tracker.append((phase, notebook_name, "FAIL", 0.0, "Notebook not found"))
            continue

        status, error, elapsed = run_notebook(notebook_path, timeout=1800)
        tracker.append((phase, notebook_name, status, elapsed, error))

    save_tracker(tracker, CSV_PATH)
    print_tracker(tracker)

    return 0 if all(row[2] == "PASS" for row in tracker) else 1


if __name__ == "__main__":
    raise SystemExit(main())
