# Reproduction guide

## Verified commands

The repository audit, geometry constant baseline and synthetic tests need Python's standard library only:

```bash
python python_scripts/audit_research.py
python -m unittest discover -s python_scripts -p "test_*.py" -v
python python_scripts/baseline_geometry.py
python python_scripts/audit_research.py --verify-originals
```

The baseline needs `data/tables/Perfect_RO_Plant_Dataset2.xlsx`. It uses cached workbook values and does not recalculate or alter the spreadsheet. It selects the exact `configuration6_interspacer3mm` label as test, fits mean and median constants on all other labels and reports MAE, RMSE and R2 for CP modulus and mean channel velocity. The default output is `reports/runs/geometry_baseline/`; reference aggregate results are in `reports/baseline_reference/metrics.json`. Predictions include source observations and remain local.

`--verify-originals` requires the complete local collection, including recovered root notebooks and archived original saved versions. It verifies every original-file hash and all four recovered notebook hashes. The ordinary audit works on a data-free clone, reporting unavailable research data explicitly. Notebook-review source hashes additionally check that executable code was not silently edited.

## Research environment

Create a clean virtual environment and activate it:

```bash
python -m venv .venv
```

PowerShell: `.\.venv\Scripts\Activate.ps1`. macOS/Linux: `source .venv/bin/activate`. Then:

```bash
python -m pip install -r requirements-research.txt
python -m jupyterlab
```

Requirements reflect recovered imports and export engines. They are not a validated lockfile. Record successful versions and platform before a full run. The neural experiment requires TensorFlow, the SHAP diagnostics require SHAP, and Excel exports in `gem` use XlsxWriter. No global packages were changed during this review.

## Working directory and protected execution

Historical cells use relative filenames such as `RO_data` and `Perfect_RO_Plant_Dataset2.xlsx`. The original table names have been restored at the project root as compatibility copies. Authoritative unchanged data copies remain in `data/tables/`.

Jupyter may use the notebook's own directory as its kernel working directory. Before running historical cells, use a new setup cell to select the project root. For example:

```python
from pathlib import Path
import os
ROOT = next(p for p in [Path.cwd(), *Path.cwd().parents]
            if (p / 'docs' / 'notebook_review_manifest.json').is_file())
os.chdir(ROOT)
```

This setup cell is optional execution guidance, not an alteration to the preserved source. Prefer a disposable project copy for full reproduction: export cells can overwrite root compatibility tables and create figures/logs in the working directory. Keep the authoritative data and recovery archive untouched.

## Suggested run order and interpretation

Read preprocessing, then early extraction, process2 summaries/features, and finally gem's explicitly selected extraction/model variant. The first two gem cells contain different boundary conventions. Do not run both blindly and assume they implement identical physical definitions. Many cells share state; notebook execution order and reused variable names matter.

The organized gem cell 25 is empty because its original saved SHAP call failed. A corrected SHAP implementation would be a separate authorized code change. The original is available locally for debugging.

Random-row experiments and geometry holdout are separate protocols. Reproduce a chosen protocol with recorded input hash, independent group IDs, features, targets, split membership, seeds, versions and outputs. Source inspection and retained outputs do not substitute for a clean-kernel run. No historical model was retrained in this review.

The standard-library HDF5 audit checks file signatures and XMF references, not internal dataset values, boundary-condition correctness or CFD convergence. See `CODE_REVIEW.md` for physical assumptions requiring verification.
