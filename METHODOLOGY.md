# Methodology

The methodology is a first-class artifact. Each metric entry must document source, exact query/filter, transformation, known limitations, update cadence, validation rules, and vintage behavior.

## Global rules
- Snapshot raw data before parsing.
- Keep every metric vintage rather than overwriting revised values.
- Publish latest vintage on the site while preserving prior vintages in the data pipeline.
- Show gaps as gaps.
- Label estimates as `ESTIMATE` with method notes.
- Do not publish any number that fails validation.
- Essays may not contain numbers that do not come from the pipeline.

## Phase 0 acceptance criteria
Phase 0 is complete when the scaffold exists, CI runs, EIA API key plumbing is present, the Astro site renders placeholder pages with a dummy chart, and `make test` passes.
