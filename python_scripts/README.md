# Python tools

| Tool | Purpose |
| --- | --- |
| `audit_research.py` | Notebook source review hashes, saved-error/source/output checks, optional full preservation verification |
| `audit_project.py` | Underlying standard-library notebook, script, HDF5 signature and XMF reference audit |
| `baseline_geometry.py` | Read-only workbook loading and training-only mean/median geometry holdout reference |
| `test_integrity_tools.py` | Four synthetic XMF reference/path tests |
| `test_geometry_baseline.py` | Four synthetic split, information-boundary and metric tests |

All tools use only Python's standard library. They do not modify research data or replace recovered model implementations. Full HDF5 numerical validation and trained-model reproduction are outside their scope.
