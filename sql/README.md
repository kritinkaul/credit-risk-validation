# Local analytical SQL (planned)

DuckDB will query local datasets and produce reproducible cohort/feature tables.
There are no database creation or ingestion commands today. The `analytics` extra
reserves DuckDB separately from the foundation installation.

Add numbered, reviewed SQL files when the data contract exists. Use explicit columns,
record grain and join-cardinality checks, and enforce feature availability at the
prediction timestamp. Keep database files under ignored `data/local/`. Version SQL
and schema definitions; record source and query fingerprints with each future run.
