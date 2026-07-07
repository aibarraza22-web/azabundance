# Methodology

The methodology is a first-class artifact. Every published metric must document its source, exact retrieval/filter, transformation, validation rule, limitation, update cadence, and vintage behavior.

## Global rules

- Snapshot raw data before parsing.
- Keep every metric vintage rather than overwriting revised values.
- Publish the latest vintage on the site while preserving prior vintages in the data pipeline.
- Show gaps as gaps.
- Label estimates as `ESTIMATE` with method notes.
- Do not publish any number that fails validation.
- Essays may not contain numbers that do not come from the pipeline.

## Component index policy

The site currently publishes component metrics only. A composite Arizona Abundance Index is not calculated until at least eight quarters of validated history exist for each included component.

Published component files:

- `data/published/housing_permits_monthly.csv`
- `data/published/housing_permits_quarterly.csv`
- `data/published/datacenter_load.csv`
- `data/published/index_components.csv`
- `data/published/figure_manifest.csv`

## Housing units permitted

- **Metric:** `housing_units_permitted`.
- **Source:** U.S. Census Bureau Building Permits Survey values as republished by FRED series `AZBPPRIV`, `PHOE004BPPRIV`, and `TUCS004BPPRIV`.
- **Current coverage:** Arizona statewide, Phoenix-Mesa-Chandler MSA, and Tucson MSA for January-May 2026.
- **Transformation:** monthly units are copied into tidy rows, then summed by calendar quarter and geography for the component index. Because Q2 2026 currently contains April-May only, it is a quarter-to-date value until June is available.
- **Vintage:** current snapshot retrieved on 2026-07-07 from pages updated by FRED on 2026-06-24.
- **Validation:** tidy output must be non-empty; all values must be non-negative; every row must carry a `source_url` and `source_file`.
- **Limitations:** FRED is used as the access layer for Phase 1 speed, but the underlying source is Census BPS. Place-level top-10 cities are not yet implemented.
- **Update cadence:** monthly after BPS/FRED updates are available.

## Data center load growth

- **Metric:** `datacenter_load_mw`.
- **Source:** hand-curated CSV seeded from ACC April 2026 public materials, with a primary-document URL required for every row.
- **Current coverage:** Arizona operating and planned data center load for 2026-Q2.
- **Transformation:** curated MW values are normalized into tidy rows with `status` values of `operating` or `planned`.
- **Vintage:** current snapshot retrieved on 2026-07-07.
- **Validation:** output must be non-empty; values must be non-negative; every row must include a `source_url`.
- **Limitations:** current values are seed values and remain flagged in method notes for verification against the ACC docket before public launch.
- **Update cadence:** quarterly manual review.

## Phase 1 next steps

- Implement EIA-860M fetch/parse/validate from the latest monthly XLS files.
- Expand BPS to the Census files/API for top-10 cities and complete historical backfill.
