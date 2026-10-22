# Proposed data contract — pending dataset selection

These are proposed requirements, not assertions about an existing dataset. Every
source-specific field name, type, constraint, and exception must be agreed and
versioned before ingestion. No horizon or dataset has been chosen.

| Concept | Proposed requirement | Decision status |
| --- | --- | --- |
| Borrower identifier | Stable pseudonymous string; map repeated records to a borrower; never use as a model feature | Pending source selection |
| Record identifier and grain | Unique non-null string per prediction record; define loan/account vs borrower grain and duplicate rules | Pending |
| Observation/prediction time | Timezone-aware timestamp or documented date precision; reflects decision information set | Pending |
| Outcome | Explicit binary default-event definition and event timestamp; distinguish unknown from negative | Pending |
| Horizon | Positive, justified duration after prediction; interval boundary and eligible population documented | Pending; no chosen duration |
| Label maturity | Outcome observation cutoff and reporting lag; require full follow-up for negatives | Pending |
| Features | Name, description, type, units, availability/publication lag, revision policy and transformation lineage | Pending |
| Missingness | Null conventions, invalid sentinels, reasons and rates by cohort; no silent filling of outcome labels | Pending |
| Data types | Explicit strings, numeric precision/ranges, booleans, category dictionaries and timestamps | Pending |
| Validation rules | Key uniqueness, referential integrity, join cardinality, allowed categories/ranges, chronology and label completeness | Pending |
| Provenance | Source URL/owner, retrieval date, version, checksums, extraction query and processing lineage | Pending |
| License | Usage, redistribution, attribution and retention terms verified before acquisition/use | Pending |
| Sensitive attributes | Identify direct/proxy attributes, legal/ethical constraints and access policy; no automatic inclusion as predictors | Pending |

## Selection and exception policy

Prefer a lawful, documented source permitting educational analysis with enough
outcome information to define an observable target. Assess selection bias, coverage,
representativeness and the meaning of a record. Do not infer borrower identity from
private attributes or claim anonymization from hashing alone.

If stable borrower IDs are absent, document residual dependence/leakage risks. If
usable dates or availability timestamps are absent, disclose the limitation; do not
claim out-of-time evaluation. Missing maturity information may make the source
unsuitable for the proposed task. Selection may require revising the scope rather
than inventing unavailable fields.

Sensitive attributes, if lawfully available, may support carefully scoped subgroup
audits under a documented policy. Decide separately whether they can be used for
modeling; exclusion does not eliminate proxy effects or prove fairness. Never
publish individual records or sensitive subgroup extracts.

Future data checks must distinguish hard failures from reviewed exceptions, record
exclusion counts, and halt on unresolved target/maturity violations. The current
configuration command checks YAML structure only and implements none of these
record-level rules.
