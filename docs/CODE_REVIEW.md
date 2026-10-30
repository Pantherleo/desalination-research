# Review of recovered implementations

Findings below come from inspection of the recovered source and tables. Original calculations are preserved. Comments identify review needs; no scientific implementation was silently corrected.

| Location | Observation | Implication for research use |
| --- | --- | --- |
| `gem`, cells 1 and 2 | First extractor takes inlet on axis 0; the second takes it on axis 2 | Verify XMF array ordering, flow direction and wall geometry before selecting the appropriate extractor |
| `gem`, cell 2 | CP numerator uses boundary planes, denominator uses inlet concentration plus epsilon | Record the exact formula and physical meaning; assess sensitivity when the denominator is small |
| `gem`, cell 2 | Case_UID uses the filename stem, repeated across directories | Include geometry, resolution and independent-run metadata in identifiers and joins |
| `processing`, cells 7–9 | A loop loads fields, while later cells use the surviving arrays outside that loop | The raw export is exploratory last-case data, not evidence of full-collection row extraction |
| `process2`, cells 6–7 | Duplicate metadata export | Both implementations are retained; avoid interpreting the duplicate as separate evidence |
| `process2`, cell 42 | Several normalizations use whole-table min/max; density/viscosity CV use table-level statistics | Refit transformations on training folds for predictive work; review columns that are constant per table |
| `process2`, cell 42 | Pressure_Gradient divides a pressure range by Grid_X | Treat it as the defined feature, not a verified physical pressure gradient without a physical length conversion |
| `process2` cell 42; `gem` cells 26–29 | Reynolds/Peclet-labelled proxies use particular grid/spacing values | Confirm units and characteristic-length choices before interpreting them as physical nondimensional numbers |
| `gem`, cells 9, 24, 26–29 | Random row splits | Related resolution/time samples may cross splits; evaluate independent-group splits separately |
| `gem`, cells 19/30 | Geometry holdout selects labels containing 3mm | The inspected label partition is 1,168/100; a new dataset should validate exact label membership |
| `gem`, cells 23/26 | Scatter plots and median guides are labelled Pareto | They visualize trade-offs; no nondominated-frontier computation is present |
| `gem`, cell 25 | Saved SHAP TypeError involving object-to-float casting | Only this cell is cleared in the organized copy; the full original remains recoverable |
| `gem`, cell 29 | Training-only scaler fit and early stopping; no TensorFlow seed set | Scaling avoids fitting on test features, but exact neural-run reproducibility is not established |
| Multiple export cells | Relative filenames can overwrite existing files | Use a dedicated execution copy and preserve authoritative tables before rerunning |

Saved scores are historical outputs with their own protocol. High or rounded-perfect scores do not resolve these concerns. No notebook was executed during this source review, and no numerical results were deleted merely for appearing surprising.
