# Roadmap and acceptance criteria

Only milestone 1 is complete. All empirical work remains planned.

| Milestone | Status | Acceptance criteria |
| --- | --- | --- |
| 1. Repository foundation | Complete | Install/import works; CLI help and strict config validation work; valid/invalid cases tested; lint, format and pytest pass; lockfile and CI workflow exist; documentation and initial public repository published |
| 2. Dataset selection and data contract | Planned | Source/license/provenance recorded; grain, target, horizon, maturity and availability defined; date and borrower limitations disclosed; contract approved for this research |
| 3. Data pipeline and leakage checks | Planned | Repeatable local ingestion/SQL; schema, join, duplication, availability and maturity checks; reproducible split manifest; train-only preprocessing and tests |
| 4. Logistic regression baseline | Planned | Reproducible baseline and prevalence comparator; documented tuning, features, folds and training artifacts; development-set evidence without test tuning |
| 5. Challenger and calibration | Planned | Comparable LightGBM experiment; validation-only/cross-fitted calibration; recorded complexity/tuning budget; frozen selection rationale |
| 6. Validation and sensitivity analysis | Planned | Separate evaluation workflow; held-out comparison, dependence-aware uncertainty, temporal analysis where supported, sensitivity, drift and failure documentation |
| 7. Final research report and optional dashboard | Planned | Reproducible reviewed report traces every empirical claim to evidence; limitations disclosed; optional dashboard only if it clarifies results |
| 8. Optional deployment | Optional; outside initial scope | Separate scope and authorization, demonstrated research value, privacy/security and operating requirements reviewed before implementation |

Next step: compare candidate datasets and complete the proposed contract, beginning
with an observable default target and defensible prediction timestamp/horizon.
Deployment is neither required for research completion nor implemented by this repository.
