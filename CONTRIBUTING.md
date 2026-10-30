# Contributing

Preserve recovered originals and distinguish code review, historical outputs and newly reproduced evidence. New changes to scientific code should describe the target, physical assumptions, inputs, validation protocol and before/after behavior.

Use `docs/EXPERIMENT_TEMPLATE.md` for each experiment. Record data hashes, independent group IDs, units, split membership, seeds, exact environment and artifact lineage. Fit transformations only on training data and keep related samples in the same split.

Place all Python files in `python_scripts/`. Update the catalogue and review manifest for intentional changes to reviewed notebook sources. Root recovered notebooks and archive snapshots remain local, unchanged provenance records.

Before proposing a change, run `python python_scripts/audit_research.py` and `python -m unittest discover -s python_scripts -p "test_*.py" -v`. For notebook behavior changes, also restart the kernel and reproduce the relevant protocol. Describe exactly what ran rather than treating saved output as fresh evidence.
