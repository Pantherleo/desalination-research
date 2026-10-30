# Research overview

## Implemented workflow

The recovered code includes preprocessing of a 20,000-row plant-style CSV, inspection of HDF5 datasets, construction of XMF/HDF5 metadata, field-summary exports, feature engineering, and surrogate-model experiments. The CFD collection has 1,268 paired HDF5/XMF records across six spacer configurations and HR/LR directories.

`preprocessing.ipynb` produces distributions, boxplots, correlations and per-dataset statistics. `processing.ipynb` contains an early raw-field exploration. `process2.ipynb` constructs metadata and per-case field summaries, explores sample arrays and creates engineered features. `gem.ipynb` contains two alternative boundary-feature extractors followed by single- and multi-output regression experiments.

Observed model families are XGBoost, Random Forest, LightGBM, CatBoost and a dense neural network. Targets include concentration-polarization modulus, mean channel velocity, velocity efficiency and an early pressure-drop target. This is a set of related notebook experiments, not one uniformly validated benchmark.

## Target definitions in code

- The later boundary extractor defines pressure drop as inlet-mean pressure minus outlet-mean pressure.
- `Output_CP_Modulus_Factor` is the mean concentration on the first/last planes of axis 0 divided by inlet mean concentration plus an epsilon. Axis and membrane-wall choices are assumptions in the code that require physical verification.
- `Target_Velocity_Efficiency` is mean channel speed divided by maximum channel speed. It is a defined ratio; it does not alone establish hydraulic efficiency or optimal spacer performance.
- `Output_Channel_Velocity_Mean` is a global mean velocity magnitude. Source units must be verified.

The two boundary extractors use different inlet-axis conventions. Preserve their distinction when tracing historical tables. Workbook names containing Perfect do not establish correctness.

## Validation protocols

Several experiments use an 80/20 random row split with seed 42. Cells 19, 20 and 30 of `gem` instead select the 3 mm geometry using the spacer-label string. The inspected workbook has 1,168 rows from configurations 1–5 and 100 rows from configuration 6. These protocols answer different questions and must not be pooled into one performance ranking.

Case_UID repeats across configurations and resolutions: there are 199 distinct Case_UID values among 1,268 rows. The combination of Case_UID, geometry label and mesh dimensions distinguishes the inspected rows, but does not prove independent simulations. Related timesteps and HR/LR records require grouping before robust validation.

The newly added constant baseline uses the exact configuration-6 label and fits constants only on training targets. Its results are independently generated from the existing workbook, without fitting the notebook models.

## Evidence still required

Confirm provenance, units, coordinate orientation, inlet/outlet and wall locations, solver settings and mesh convergence. Establish independent run identifiers and keep related samples together. Use training-only transforms and tune within training folds. Report grouped and temporal robustness, uncertainty and physical failure cases. Recovering code establishes the implementation, not the validity of every assumption or historical score.

See `CODE_REVIEW.md` and `HISTORICAL_RESULTS.md` for code-specific findings and retained results.
