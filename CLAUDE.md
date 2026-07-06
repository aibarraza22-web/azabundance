# Project Working Rules

## Non-negotiable principles
- `make build` must regenerate every published number from raw source files.
- Raw pulls must be snapshotted before parsing so historical values never silently change.
- Store metrics with `metric`, `period`, `value`, `vintage_date`, and `source_file`.
- Never publish a number that fails validation.
- No fabricated or interpolated data may be presented as observed; estimates must be labeled `ESTIMATE` with method notes.
- The Index is a neutral scoreboard; essays are where arguments belong.
- Essays may not contain numbers that don't come from the pipeline.

## Architecture guardrails
- Python 3.12 pipeline modules live in `pipeline/sources/` and expose `fetch()`, `parse()`, and `validate()`.
- Source modules snapshot raw data in `data/raw/`, write tidy outputs to `data/tidy/`, and published outputs to `data/published/`.
- `pipeline/index.py` computes quarterly component series and may not publish a composite index until at least 8 quarters exist.
- The publication site lives in `site/` and is an Astro static site.
- Fetch and inspect real source files before writing parsers.
- When a source schema surprises you, update `SOURCES.md` in the same commit.

## Phase 0 acceptance criteria
- Repo scaffold exists for the Python pipeline, raw/tidy/published data, notebooks, and Astro site.
- Makefile provides `make build`, `make test`, and site commands.
- EIA API key plumbing exists without committing secrets.
- CI runs tests and a production site build.
- The Astro site renders placeholder pages and a dummy chart.
