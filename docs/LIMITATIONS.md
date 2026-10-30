# Limitations and research work remaining

- Full extraction, feature-engineering and training code has been recovered in four notebooks. The organized copies preserve executable statements except the single explicitly erroring SHAP cell. A complete clean-kernel reproduction remains pending.
- Data provenance, source citations, licenses, solver version, units, boundary conditions and contributor roles are not established by filenames.
- Alternative extractors disagree on which array axis represents the inlet. Verify orientation and membrane-wall definitions before interpreting pressure drop or concentration polarization physically.
- Case_UID is not globally unique. There are 199 distinct values in the 1,268-row second RO workbook; directory and resolution context are necessary. Independent-run identity and temporal/HR-LR relationships still need verification.
- Random-row splits and geometry holdout describe different tasks. Repeated or related observations can inflate confidence; group-level robustness and uncertainty have not been demonstrated.
- Table-wide normalization and target-derived aggregates need review for prediction-time availability and training-fold fitting. The named Reynolds/Peclet/gradient features are proxies unless their units and definitions are justified.
- Median guide lines in trade-off plots do not identify a Pareto frontier. Existing figure titles are retained as source history and should be interpreted with this limitation.
- The saved neural experiment does not set a TensorFlow seed. The full environment was not locked, and no historical model has been rerun in this review.
- The SHAP diagnostic in gem cell 25 has a saved TypeError. It is cleared only in the organized copy; complete source and outputs remain in recovered originals.
- Root compatibility datasets can be overwritten by notebook export cells. Use a disposable execution copy and retain the unchanged authoritative tables.
- The plant-style CSV's relationship to the CFD collection is undocumented. Its temperature header contains a pre-existing Unicode replacement character.
- Signature/reference checks and newly executed constant baselines are not CFD physical validation, model reproduction or evidence of optimal spacer design.
- Public release still requires accurate attribution and sharing permissions. No institutional relationship, plant deployment or license is inferred automatically.
