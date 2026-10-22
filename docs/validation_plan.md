# Planned separate evaluation workflow

All evaluations are **Not evaluated yet**. This is a separate workflow maintained
by the same developer, not organizationally independent model validation.

## Before fitting

Complete source/license/provenance, target, prediction horizon, label maturity,
eligible population, feature availability, and borrower policies. Freeze a split
manifest and audit joins, duplicates, exclusion counts, date coverage and missingness.
Record reasons for every exception. If usable dates do not exist, disclose that
out-of-time validation is unavailable and describe the weaker split actually used.

Declare selection criteria, tuning budget, calibration design, metric conventions,
and test-access policy before model comparison. No performance targets are established
by this scaffold. Choose any future acceptance criteria in context and justify them.

## Evidence to produce

| Question | Planned evidence |
| --- | --- |
| Are risk rankings informative? | ROC-AUC and PR-AUC with integration convention, prevalence and event counts |
| Are probabilities useful? | Brier score, log loss, calibration curves, bin counts and uncertainty; prevalence baseline |
| Does the challenger add value? | Paired baseline/challenger differences on identical observations, before/after calibration |
| Does reliability persist over time? | Out-of-time cohorts and temporal slices where possible, with maturity and coverage |
| Are conclusions robust? | Sensitivity analyses, dependence-aware intervals, failure-case log |
| Has the input population changed? | Missingness/category changes, PSI and feature-level distribution measures |

## Uncertainty and stability

Use paired comparisons for models evaluated on the same cases. IID row bootstrap
intervals can be too narrow with repeated borrowers or temporal dependence. Consider
borrower-cluster resampling, temporal block bootstrap, or an explicitly justified
combined/hierarchical scheme. Specify block length, number of replicates, event
coverage, and assumptions. Temporal folds provide additional stability evidence;
few time periods or defaults can prevent reliable interval estimation. Report such
limitations, undefined metrics, and wide intervals rather than hiding them.

## Sensitivity and failures

Vary defensible target definitions/horizons, maturity lag, cohort exclusions,
feature groups, missing-value handling, regularization, class weighting, calibration
method, seed, time windows, and borrower rules. These are research questions, not
permission to select whichever result looks best. Predetermine core analyses;
label post hoc analyses as exploratory. Repeat model comparisons on common cohorts
when changes would otherwise confound sample and model effects.

Record sparse-category behavior, unseen values, missingness shifts, very low event
counts, one-class slices, probability extremes, unstable calibration bins, and
subgroups with insufficient support. Document expected handling before implementing
it. Trace any material failure to data, target, assumptions, or fitting choices.

## Drift monitoring design

Compare a fixed, documented reference population with later cohorts. For PSI,
record training/reference-derived bin boundaries, missing/unknown bins, category
pooling, minimum counts and any zero-count smoothing. PSI sums
(p_i - q_i) * log(p_i / q_i) over common bins; zero proportions need a declared
handling policy. It is sensitive to binning, sample size, sparse categories and
smoothing; there is no universal scientific threshold separating safe and unsafe models.

Also inspect feature-level quantiles/distributions, missingness, category frequencies,
and prediction distributions. Any alerts need dataset-specific justification and
review. Drift indicates a distribution change; it does not itself establish worse
predictive performance. Assess performance/calibration only once outcomes mature,
and investigate target prevalence, population and measurement changes separately.

## Reproducibility and final assessment

Freeze preprocessing, estimator and calibrator; evaluate once on the held-out test
under the declared plan. Produce a manifest with code commit, lockfile/software,
config, seed, source and table fingerprints, SQL, split boundaries, label cutoff,
and artifact lineage. Re-run from clean inputs, compare outputs within documented
numerical tolerances, and fill the [report template](../reports/templates/model_validation_report.md).
Report adverse findings, limitations, and unresolved recommendations as carefully
as favorable comparisons. Do not commit generated reports or private artifacts.
