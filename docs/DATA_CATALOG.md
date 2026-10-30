# Data catalogue

Observed file structure and schemas only. Source provenance and derivation are not inferred from filenames. Full column inventories are in [table_schemas.json](table_schemas.json).

| Table | Sheet | Data rows | Columns |
| --- | --- | ---: | ---: |
| `Extracted_HDF5_Data.xlsx` | Sheet1 | 21,420 | 14 |
| `Metadata.xlsx` | Sheet1 | 1,268 | 7 |
| `Perfect_RO_Plant_Dataset.xlsx` | RO_Simulation_Dataset | 1,268 | 24 |
| `Perfect_RO_Plant_Dataset2.xlsx` | RO_Simulation_Dataset | 1,268 | 24 |
| `Raw_CFD_Data.xlsx` | Sheet1 | 400 | 14 |
| `Summary_CFD_Dataset.xlsx` | Sheet1 | 1,268 | 24 |
| `Summary_CFD_Dataset_FeatureEngineered.xlsx` | Sheet1 | 1,268 | 50 |
| `desalination.csv` | CSV | 20,000 | 9 |
| `Raw_CFD_Data2.csv` | CSV | 400 | 15 |

## Simulation coverage

| Configuration | Resolution directory | HDF5 | XMF |
| --- | --- | ---: | ---: |
| configuration1_interspacer0.75mm | HR_spacer_images | 199 | 199 |
| configuration1_interspacer0.75mm | LR_spacer_images | 199 | 199 |
| configuration2_interspacer1mm | HR_spacer_images | 150 | 150 |
| configuration2_interspacer1mm | LR_spacer_images | 150 | 150 |
| configuration3_interspacer1.5mm | HR_spacer_images | 100 | 100 |
| configuration3_interspacer1.5mm | LR_spacer_images | 100 | 100 |
| configuration4_interspacer2mm | HR_spacer_images | 75 | 75 |
| configuration4_interspacer2mm | LR_spacer_images | 75 | 75 |
| configuration5_interspacer2.5mm | HR_spacer_images | 60 | 60 |
| configuration5_interspacer2.5mm | LR_spacer_images | 60 | 60 |
| configuration6_interspacer3mm | HR_spacer_images | 50 | 50 |
| configuration6_interspacer3mm | LR_spacer_images | 50 | 50 |

## Interpretation and lineage

`desalination.csv` contains plant-style feed/permeate flow and TDS, salinity, temperature, recovery, flux and pressure-drop columns. Its relationship to the CFD collection is not recorded. The temperature column contains an existing replacement character. No encoding repair was applied.

The metadata workbook lists simulation companions. The extracted-data workbook describes per-dataset statistics and shapes. CFD summary tables contain field aggregates; the engineered version adds derived columns implemented in process2 cell 42. The two Perfect workbooks label mesh attributes and input/output quantities, but their names do not establish correctness or provenance.

Original source URLs, acquisition dates, solver/version, boundary conditions, units, independent-run identifiers and sharing licenses remain to be supplied. See the file manifest for exact local data versions.


## Recovered implementation lineage

Recovered preprocessing cells 8–11 implement HDF5 dataset statistics. Process2 cells 3–12 implement companion metadata and field summaries; cell 42 implements engineered features. Gem cell 2 writes the second RO workbook using its boundary-plane assumptions. Exact table regeneration has not been performed. The first and second RO workbooks remain distinct versions.
