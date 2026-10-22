# Architecture

Status: only packaging, CLI, and configuration validation exist. All research stages
below are planned. See the [README diagram](../README.md#planned-architecture).

## Working foundation

`credit_risk.cli` parses commands and maps configuration failures to a nonzero exit.
`credit_risk.config` reads UTF-8 YAML with a safe loader, rejects duplicate keys,
and validates strict Pydantic models. It does not ingest records, connect to DuckDB,
fit preprocessing, train models, or generate results. Imports have no such side effects.

`configs/base.yaml` intentionally leaves source and target decisions unresolved.
Nulls are required explicit placeholders. `pending`, `temporal`, and `grouped` are
permitted split values; temporal/grouped choices require the corresponding column
name. This schema cannot verify that columns exist or that a proposed split is valid.
The fixed project stage is `foundation`; evolve the schema deliberately when experiments exist.
A seed is recorded for future work; it does not guarantee deterministic results.

## Planned boundaries and artifact flow

| Future component | Responsibility | Outputs consumed downstream |
| --- | --- | --- |
| `data` and versioned SQL | Provenance, ingestion, schema, join and maturity checks | Cohort tables and validation findings |
| `features` | Availability-aware transformations fitted only on training data | Feature schema and fitted preprocessing |
| `models` | Fit baseline/challenger on approved training partitions | Model artifacts, configs and frozen predictions |
| `validation` | Evaluate frozen predictions under a predeclared protocol | Metrics, intervals, sensitivity and drift tables |
| `reporting` | Render traceable, sanitized evidence | Reproducible research report |

These packages will be created when implemented. DuckDB will store local analytical
intermediates; SQL will make cohort construction and joins inspectable. Files belong
under ignored `data/`; there is no remote service, feature store, or plugin layer.

Training and evaluation will use separate entry points and artifacts. Evaluation
will record cohort IDs/fingerprints, labels, model/config hashes and split boundaries;
it must not tune against final test outputs. Shared metric/data utilities are sensible,
but the evaluation workflow should check assumptions and failures separately from
training code. One developer maintains both; this is not organizational independence.

A future run manifest must include source/license, data and SQL fingerprints,
Git commit, config, lockfile/environment, seed, split boundaries, label cutoff,
platform and relevant library versions. Fingerprints aid traceability, not anonymization.
No future commands are promised by the present CLI.
