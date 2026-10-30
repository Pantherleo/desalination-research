# Notebook catalogue

These are organized review copies of the four recovered notebooks. Every original cell position is preserved, so cell numbers below refer to the original 1-based positions.

| Notebook | Cells | Workflow |
| --- | ---: | --- |
| [preprocessing](01_preprocessing/preprocessing.ipynb) | 12 | Plant CSV plots and HDF5 dataset-level statistics |
| [processing](02_extraction/processing.ipynb) | 10 | Early raw-field extraction exploration and raw Excel export |
| [process2](02_extraction/process2.ipynb) | 42 | Companion metadata, XMF mappings, field summaries, sample grids and engineered features |
| [gem](03_modeling/gem.ipynb) | 30 | Alternative boundary extractors, model comparisons, multi-output targets, neural network, SHAP and geometry holdout |

`gem` cells 1–2 contain alternative extraction assumptions. Cells 3–17 develop a single-target model and plots. Cells 18–24 explore target correlations, geometry holdout and model comparison. Cell 25 is cleared only in this review copy because it has a saved SHAP TypeError. Cells 26–30 contain multi-output and neural experiments and a geometry-holdout comparison.

The full recovered notebooks at the project root and in `archive/recovered_originals/` are unchanged. Comments in review copies identify assumptions and interpretation issues without altering the executable statements of retained cells. The earlier zero-byte saved versions are archived separately and are not the active research notebooks.

Run from the project root as explained in the reproduction guide. Opening an organized notebook in Jupyter may select its own directory as the working directory; explicitly set the project root in a new setup cell before running the historical cells.
