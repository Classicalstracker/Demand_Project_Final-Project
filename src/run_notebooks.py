from pathlib import Path
import time
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
import pandas as pd
import traceback
# -----------------------------
# PROJECT PATHS
# -----------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent
NOTEBOOK_DIR = PROJECT_ROOT / "notebooks"
OUTPUT_PATH = PROJECT_ROOT / "reports" / "tables" / "regression_tracker.csv"
# -----------------------------
# NOTEBOOK EXECUTION ORDER
# -----------------------------
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
    (11, "11_Final_Insights.ipynb"),
]
# -----------------------------
# RUN SINGLE NOTEBOOK
# -----------------------------
def run_notebook(nb_path):
    start = time.time()

    try:
        with open(nb_path, "r", encoding="utf-8") as f:
            nb = nbformat.read(f, as_version=4)

        ep = ExecutePreprocessor(
            timeout=1800,  # 30 minutes
            allow_errors=False
        )

        # IMPORTANT: Run from project root
        ep.preprocess(nb, {"metadata": {"path": str(PROJECT_ROOT)}})

        elapsed = round(time.time() - start, 2)
        return "PASS", "", elapsed

    except Exception:
        elapsed = round(time.time() - start, 2)
        error_msg = traceback.format_exc()
        return "FAIL", error_msg, elapsed
# -----------------------------
# MAIN EXECUTION
# -----------------------------
def main():
    tracker = []

    print("\n## PHASE NOTEBOOK REGRESSION TRACKER\n")
    print(f"{'Phase':<5} | {'Notebook':<30} | {'Status':<6} | {'Time(sec)':<10}")
    print("-" * 65)

    for phase, nb_name in NOTEBOOKS:
        nb_path = NOTEBOOK_DIR / nb_name

        if not nb_path.exists():
            print(f"{phase:<5} | {nb_name:<30} | FAIL   | 0.0")
            tracker.append((phase, nb_name, "FAIL", 0.0, "File not found"))
            continue

        status, err, elapsed = run_notebook(nb_path)

        print(f"{phase:<5} | {nb_name:<30} | {status:<6} | {elapsed:<10}")

        tracker.append((phase, nb_name, status, elapsed, err))

    # -----------------------------
    # SUMMARY
    # -----------------------------
    df = pd.DataFrame(tracker, columns=["Phase", "Notebook", "Status", "Time", "Error"])

    total_pass = (df["Status"] == "PASS").sum()
    total_fail = (df["Status"] == "FAIL").sum()

    print("\nSummary:\n")
    print(f"Total PASS: {total_pass}")
    print(f"Total FAIL: {total_fail}")

    if total_fail > 0:
        print("\nFailures:")
        for _, row in df[df["Status"] == "FAIL"].iterrows():
            print(f"Phase {row['Phase']} | {row['Notebook']}")
            print(row["Error"][:500])  # show first 500 chars only

    # -----------------------------
    # SAVE TRACKER
    # -----------------------------
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False)

    print(f"\nSaved tracker:\n{OUTPUT_PATH}")


if __name__ == "__main__":
    main()