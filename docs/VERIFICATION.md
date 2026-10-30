# Verification record

Reviewed on 2026-10-30 with Python 3.12. Full recovered code is now the basis of this record.

- Four complete recovered originals, containing 94 code-cell positions, match their recorded recovery SHA-256 hashes at the project root.
- Organized copies retain all 94 positions and cell identities. One saved-error cell, gem cell 25, is cleared only in the review copy. Other changes to original sources are explicit comments, verified by exact string preservation after each known comment prefix.
- Full copies, including the error cell and all saved outputs, remain in the local recovery archive. Earlier incomplete saved files are also retained.
- All 2,558 originally saved files match their original hashes at their recorded current locations.
- All 1,268 HDF5 signatures and all 1,268 XMF companion/reference files pass the scoped integrity audit.
- Eight synthetic tests pass: four XMF reference checks and four geometry baseline partition/metric/information-boundary checks.
- The independent geometry constant baseline executed on the existing second RO workbook, with 1,168 training rows and 100 test rows. It did not recalculate or alter workbook data.
- All four organized notebook schemas are validated separately using nbformat.
- Historical model training, extraction exports, SHAP and figure generation were not rerun. Existing model outputs are historical records, not new reproduced scores.
- No global packages were changed, no Git repository was created and no files were uploaded.

The local full-preservation command is `python python_scripts/audit_research.py --verify-originals`. A data-free clone uses the ordinary audit and synthetic tests. See `CLEANUP_LOG.md`, `CODE_REVIEW.md` and `reports/verification/research_audit.json` for scope and evidence.
