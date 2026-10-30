# Historical notebook results

These values are transcribed from saved outputs in the recovered `gem.ipynb`. They were not regenerated in this review. No superiority claim is made, and scores with different targets or splits are not directly comparable.

## Random-row CP model comparison: cell 24

| Model | MAE | RMSE | R2 |
| --- | ---: | ---: | ---: |
| Random Forest | 0.001149 | 0.003086 | 0.998940 |
| XGBoost | 0.001702 | 0.003091 | 0.998937 |
| LightGBM | 0.001945 | 0.003326 | 0.998769 |
| CatBoost | 0.003765 | 0.005150 | 0.997048 |

Target: `Output_CP_Modulus_Factor`. Protocol in source: 80/20 random row split, seed 42. Related samples may cross that split. These are notebook-held-out scores, distinct from the training-only CatBoost log.

## Geometry holdout: cells 19 and 30

| Source | Model | Target | Saved R2 | Saved MAE |
| --- | --- | --- | ---: | ---: |
| Cell 19 | XGBoost | CP modulus | 0.9959 | 0.0051 |
| Cell 30 | Random Forest | CP modulus | 0.9964 | 0.0056 |
| Cell 30 | Random Forest | Mean channel velocity | 1.0000 | 0.0000 |
| Cell 30 | LightGBM | CP modulus | 0.9951 | 0.0054 |
| Cell 30 | LightGBM | Mean channel velocity | 0.9999 | 0.0001 |

Source partition: configurations 1–5 for training and the 3 mm label for test, with 1,168 and 100 rows respectively. Printed values are rounded and do not establish exact zero error. They have not been matched to new model predictions or independent CFD validation.

Cells 26–29 contain additional random-row multi-output and neural experiments. Their second target is a velocity-efficiency ratio, which differs from cell 30's mean-channel-velocity target. Do not merge them into a common ranking.

## New reference

`reports/baseline_reference/metrics.json` records newly executed training-only mean/median baselines for the exact 3 mm geometry holdout. It includes an input checksum. It is a constant-reference experiment, not a reproduction of any trained model above. Do not infer a validated model improvement by subtracting historical scores from this reference.
