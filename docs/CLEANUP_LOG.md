# Notebook preservation and cleanup

The full recovered originals contain 94 code-cell positions across four notebooks: preprocessing 12, processing 10, process2 42 and gem 30. Original root files and exact snapshots in `archive/recovered_originals/` remain unchanged. The independent recovery copies are also retained outside the project.

Only `gem.ipynb` cell 25 has an explicit saved error. Its error is a SHAP TypeError: object array data cannot be cast safely to float64. The organized copy clears that cell's source, outputs and execution count while keeping its position and cell identity. Its metadata points to this record. No entire notebook is deleted.

Review comments were added to selected cells to explain run order, assumptions and validation limits. Every other original source string is retained verbatim after the documented comment prefix. Other saved outputs are preserved. Unusual numerical results were not treated as errors without evidence.

`notebook_review_manifest.json` records each original and reviewed cell-source checksum, action and path. `recovery_manifest.json` records the full recovered original hashes. `file_manifest.csv` separately records the 2,558 files saved on disk before code recovery. Earlier empty/import-only saved versions remain in `archive/saved_versions_before_recovery/`.

The earlier documentation based only on incomplete saved files was superseded after recovering the full editor backups. A local archived copy of that earlier documentation is retained for traceability and excluded from GitHub. Active documentation now describes the recovered implementations.
