# Quality-control regression runner for notebook phases
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
from pathlib import Path
import time
import csv

NOTEBOOKS = [
    (1, '01_Business_Understanding.ipynb'),
    (2, '02_Data_Understanding.ipynb'),
    (3, '03_Preprocessing.ipynb'),
    (4, '04_EDA.ipynb'),
    (5, '05_Merge_Analysis.ipynb'),
    (6, '06_Demand_Classification.ipynb'),
    (7, '07_Feature_Engineering.ipynb'),
    (8, '08_Model_Training.ipynb'),
]

NOTEBOOK_DIR = Path('notebooks')
CSV_PATH = Path('reports/tables/regression_tracker.csv')
PROJECT_ROOT = Path(__file__).resolve().parent.parent

def run_notebook(notebook_path, timeout=1800):
    """Run a notebook and return (status, error_message, elapsed_time)."""
    start = time.time()
    try:
        with open(notebook_path, 'r', encoding='utf-8') as f:
            nb = nbformat.read(f, as_version=4)
        ep = ExecutePreprocessor(timeout=timeout, kernel_name='python3')
        ep.preprocess(nb, {'metadata': {'path': str(PROJECT_ROOT)}})
        elapsed = round(time.time() - start, 1)
        return 'PASS', '', elapsed
    except Exception as e:
        elapsed = round(time.time() - start, 1)
        msg = str(e).split('\n')[0][:120]
        return 'FAIL', msg, elapsed

def print_tracker(tracker):
    print('\n## PHASE NOTEBOOK REGRESSION TRACKER\n')
    print(f"{'Phase':<5} | {'Notebook':<32} | {'Status':<5} | {'Time(sec)':<8}")
    for row in tracker:
        phase, nb, status, t, err = row
        print(f"{phase:<5} | {nb:<32} | {status:<5} | {t:<8}")
    passed = sum(1 for r in tracker if r[2] == 'PASS')
    failed = sum(1 for r in tracker if r[2] == 'FAIL')
    overall = 'PASS' if failed == 0 else 'FAIL'
    print(f"\nOverall Status: {overall}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    if failed:
        print("\nFailures:")
        for row in tracker:
            if row[2] == 'FAIL':
                print(f"Phase {row[0]}: {row[1]} - {row[4]}")

def save_csv(tracker, csv_path):
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Phase', 'Notebook', 'Status', 'Time(sec)', 'Error'])
        for row in tracker:
            writer.writerow(row)

def main():
    tracker = []
    for phase, nb_name in NOTEBOOKS:
        nb_path = NOTEBOOK_DIR / nb_name
        status, err, elapsed = run_notebook(nb_path)
        tracker.append((phase, nb_name, status, elapsed, err))
    print_tracker(tracker)
    save_csv(tracker, CSV_PATH)

if __name__ == "__main__":
    main()
# #!/usr/bin/env python
# """Regression test runner for notebooks in batch mode."""

# import os
# import sys
# import subprocess
# import json
# from pathlib import Path

# # Fix Unicode encoding for Windows console
# if sys.platform == 'win32':
#     import io
#     sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# # Configuration
# NOTEBOOK_DIR = Path("d:/Final Project/notebooks")
# NOTEBOOKS = [
#     "01_Business_Understanding.ipynb",
#     "02_Data_Understanding.ipynb",
#     "03_Preprocessing.ipynb",
#     "04_EDA.ipynb",
#     "05_Merge_Analysis.ipynb",
#     "06_Demand_Classification.ipynb"
# ]

# def run_notebook(notebook_path):
#     """Execute a notebook and return success/failure status."""
#     try:
#         print(f"\n{'='*60}")
#         print(f"Running: {notebook_path.name}")
#         print(f"{'='*60}")
        
#         cmd = [
#             sys.executable, "-m", "jupyter", "nbconvert",
#             "--to", "notebook",
#             "--execute",
#             f"--ExecutePreprocessor.timeout=600",
#             str(notebook_path),
#             "--output", str(notebook_path)
#         ]
        
#         result = subprocess.run(cmd, capture_output=True, text=True, cwd="d:/Final Project")
        
#         # Check for execution errors
#         if result.returncode != 0:
#             print(f"[FAILED]")
#             print(f"STDERR: {result.stderr}")
#             return False, result.stderr
        
#         # Read the notebook and check for errors
#         with open(notebook_path, 'r', encoding='utf-8') as f:
#             nb_content = json.load(f)
        
#         errors = []
#         for cell in nb_content.get('cells', []):
#             if cell.get('cell_type') == 'code':
#                 outputs = cell.get('outputs', [])
#                 for output in outputs:
#                     if output.get('output_type') == 'error':
#                         error_name = output.get('ename', 'Unknown')
#                         error_value = output.get('evalue', '')
#                         if error_name in ['NameError', 'FileNotFoundError', 'ImportError', 'ModuleNotFoundError']:
#                             errors.append(f"{error_name}: {error_value}")
        
#         if errors:
#             print(f"[FAILED] - Errors found:")
#             for error in errors:
#                 print(f"   - {error}")
#             return False, ", ".join(errors)
        
#         print(f"[PASSED]")
#         return True, "No errors"
        
#     except Exception as e:
#         print(f"[FAILED] - Exception: {str(e)}")
#         return False, str(e)

# def main():
#     """Run regression tests for all notebooks."""
#     os.chdir("d:/Final Project")
    
#     results = {}
    
#     print("\n" + "="*80)
#     print("REGRESSION TEST - Sequential Notebook Execution")
#     print("="*80)
    
#     for notebook in NOTEBOOKS:
#         nb_path = NOTEBOOK_DIR / notebook
#         if nb_path.exists():
#             success, message = run_notebook(nb_path)
#             results[notebook] = (success, message)
#         else:
#             print(f"WARNING: NOT FOUND: {notebook}")
#             results[notebook] = (False, "File not found")
    
#     # Print summary
#     print("\n" + "="*80)
#     print("REGRESSION TEST SUMMARY")
#     print("="*80)
#     print(f"\n{'Notebook':<40} {'Status':<10} {'Issues/Fixes':<50}")
#     print("-" * 100)
    
#     passed = 0
#     failed = 0
    
#     for notebook, (success, message) in results.items():
#         status = "PASS" if success else "FAIL"
#         if success:
#             passed += 1
#         else:
#             failed += 1
#         # Truncate long messages
#         display_msg = message[:47] + "..." if len(message) > 50 else message
#         print(f"{notebook:<40} {status:<10} {display_msg:<50}")
    
#     print("-" * 100)
#     print(f"Total: {passed} PASSED, {failed} FAILED\n")
    
#     return 0 if failed == 0 else 1

# if __name__ == "__main__":
#     sys.exit(main())
