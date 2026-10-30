# GitHub preparation

## Prepared project

The proposed tracked project includes four organized full-code notebooks, scoped review comments, research documentation, input/cleanup manifests, original figures, a deterministic geometry constant baseline, integrity tests and GitHub Actions checks.

All four full recovered originals remain unchanged locally at the project root and in the recovery archive. Their root paths and archive are ignored so only the reviewed notebooks are proposed for publication. The one saved SHAP error is cleared only in its review copy. Raw/derived datasets and training logs stay local until redistribution permission is confirmed.

## Before publishing

1. Confirm authors, supervisor, affiliation, source citations and contributor consent.
2. Confirm permissions for simulation data, tables, historical figures and notebook embedded outputs. Provide an approved retrieval location and match checksums when sharing data.
3. Choose a code license with contributors' agreement and document separate data/model terms.
4. Review notebook outputs and metadata for restricted or personal information. Pattern checks are scoped and do not inspect every binary/image payload.
5. Reproduce the intended presentation protocol in a clean environment. Report historical scores as historical until reproduced; use the code review to resolve physical assumptions and validation concerns.
6. Run the audit/tests and inspect staged files before committing.

## Local commands

```bash
git init -b main
git add .
git status --short
git diff --cached --stat
python python_scripts/audit_research.py
python -m unittest discover -s python_scripts -p "test_*.py" -v
git commit -m "Document recovered reverse osmosis experiments and add reproducible checks"
```

After creating the intended GitHub repository, add its URL as origin and push main. No Git repository or remote is created and nothing is uploaded by this review step. Do not force-add local data, archives or recovered originals without explicitly deciding their sharing terms and role.
