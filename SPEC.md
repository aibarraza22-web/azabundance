# METAPROMPT — Project 2: The Arizona Abundance Index (data pipeline + publication site)

> Paste this entire document as the first message in a fresh session inside an empty git repo.
> Then say: "Save as SPEC.md, generate .md per Section 9, and begin Phase 0."

---

## 1. Mission and context

You are building the **Arizona Abundance Index**: a quarterly, methodology-transparent scoreboard of whether Arizona is actually building — energy, housing, chips — plus the publication site that hosts it and the builder's essays. Solo developer, small grant budget. The audience is journalists, legislators and their staff, and the national abundance/progress-studies ecosystem. Credibility is the entire product: every number must be reproducible from public data by a stranger running one command.

This is a **data journalism engineering** project, not a dashboard-widget project. The pipeline is the moat; the site is the distribution.

## 2. Non-negotiable principles

- **Reproducibility**: `make build` regenerates every published number from raw source files. Raw pulls are snapshotted and committed (or stored with checksums) so historical index values never silently change.
- **No fabricated or interpolated data presented as observed.** Gaps are shown as gaps. Estimates are labeled ESTIMATE with method notes.
- **Vintage discipline**: government data revises. Store every metric as (metric, period, value, vintage_date, source_file). The site shows latest vintage; the methodology page explains revisions; never overwrite.
- **Methodology page is a first-class artifact**: every metric documents source, exact query/filter, transformation, known limitations, and update cadence.
- **Neutral scoreboard, opinionated essays** — the Index page editorializes nothing; the essays (separate section) can argue. Never mix.

## 3. The metrics (v1 = the six marked CORE; others are v2 backlog)

| Metric | Source | Access | Notes |
|---|---|---|---|
| **CORE 1. Housing units permitted** (AZ + Phoenix/Tucson metros + top-10 cities, monthly) | U.S. Census **Building Permits Survey (BPS)** | Published monthly files + Census API; place-level and CBSA-level | The workhorse. Backfill to 2000 for trend context. |
| **CORE 2. Generation capacity added / in pipeline** (MW by fuel, AZ) | **EIA-860M** (monthly generator inventory: operating, planned, retired) | Monthly XLSX download, stable schema | Split operating vs. planned; track slippage of planned in-service dates across vintages — that slippage series is original and citable. |
| **CORE 3. Statewide generation + demand** (TWh, peak) | **EIA-923** (annual/monthly gen), **EIA-930** (hourly demand by BA: AZPS, SRP, TEPC, WALC) | Bulk CSV/API (EIA v2 API, free key) | Context layer for essays; also feeds Project 3 if built. |
| **CORE 4. Semiconductor & construction employment** (AZ, quarterly) | **BLS QCEW** (NAICS 3344 semiconductor mfg; NAICS 23 construction; Maricopa + statewide) | Open CSV/API | The chips-boom trace. Add CES monthly for timeliness. |
| **CORE 5. Data center load growth** (MW operating/planned, AZ) | ACC filings/news releases, utility investor decks (Pinnacle West), 10-year transmission plans | Manual quarterly curation into a small hand-maintained CSV with per-row source URLs | The one hand-curated metric; every row cites a primary document. Seed values (verify before publishing): ~2 GW operating / >10.6 GW planned per ACC April 2026. |
| **CORE 6. Median days to issue a building permit** (Phoenix + others as data arrives) | City permit-system extracts via public records requests (in flight separately) | CSV extracts, irregular | Ship the Index without it if needed; add when first extract lands. Design the schema for it now. |
| v2 backlog | Interconnection queue depth (LBNL annual + utility OASIS), housing completions vs. permits, apartment rents (context), transformer lead times, water (AF banked), transit/lane-miles | — | Document in BACKLOG.md, don't build. |

For every source: verify the current URL/schema live before coding against it; record in SOURCES.md with retrieval date. Do not trust this spec's descriptions — sources change.

## 4. Architecture

- **Pipeline**: Python 3.12, pandas/polars; one module per source in `/pipeline/sources/`, each exposing `fetch()` (download + snapshot raw), `parse()` (raw → tidy), `validate()` (schema + sanity checks via pandera: row counts, value ranges, period continuity). Orchestrate with a plain Makefile or a simple runner — no Airflow, no cloud warehouse. Output: versioned parquet + a single `index.duckdb`.
- **Index computation** in `/pipeline/index.py`: each CORE metric normalized to a per-quarter series; publish both raw series and, once ≥8 quarters of history exist, an indexed composite (base=100). Until then, publish the components only — do not invent a composite with insufficient history.
- **Site**: **Astro** static site (fast, cheap, content-first). Sections: `/index` (the scoreboard: one hero chart per metric via Observable Plot or ECharts, each with a "download CSV" + "methodology" link), `/methodology`, `/data` (all CSVs + a small JSON API as static files), `/essays` (markdown blog), `/about`. Design: clean, serious, credible — closer to a Fed data page than a startup landing page. Dark-on-light, one accent color, real typographic hierarchy. No stock imagery.
- **Repo layout**:
```
/pipeline/sources/{bps,eia860m,eia923,eia930,qcew,datacenters,permits}.py
/pipeline/index.py  /pipeline/validate/
/data/raw/  /data/tidy/  /data/published/
/site/               # Astro project
/notebooks/          # exploration only; nothing published from here
SPEC.md CLAUDE.md SOURCES.md BACKLOG.md METHODOLOGY.md
```
- **Automation**: GitHub Actions monthly cron → fetch, validate, rebuild, deploy (Cloudflare Pages/Netlify); on validation failure, open an issue instead of publishing.

## 5. Phases

**Phase 0 — Scaffold (day 1–2).** Repo, CI, Astro skeleton with placeholder pages, EIA API key wired, Makefile. *Accept: site deploys with dummy chart; `make test` green.*

**Phase 1 — Two easiest sources end-to-end (week 1).** BPS + EIA-860M, raw→tidy→validated→charted on the site with real Arizona data and methodology entries. Get the full vertical slice working before breadth. *Accept: two live charts, reproducible from `make build`, methodology entries written.*

**Phase 2 — Remaining CORE sources (week 2–4).** EIA-923/930 aggregates, QCEW, the hand-curated data center CSV (with a validation rule: no row without source_url). *Accept: 5 of 6 CORE metrics live; SOURCES.md complete.*

**Phase 3 — Index page + launch polish (week 4–6).** The scoreboard page with quarter-over-quarter deltas and small sparkline history; per-metric CSV downloads; the methodology page as a genuinely readable document; OG images per chart for social sharing (this drives distribution — invest here). *Accept: a stranger can understand every number's origin within two clicks.*

**Phase 4 — Essay infrastructure + first publication (week 6–8).** Markdown pipeline with inline-chart shortcodes that pull from the published data (essays cite the same pipeline — no hand-made numbers in essays), RSS, newsletter signup (Buttondown or similar). Builder writes launch essay; you assist with charts and fact-checking against the DB, not with the arguments. *Accept: launch essay published with 3+ pipeline-backed charts.*

**Phase 5 — The slippage report (week 8–10, the original-research feature).** Using archived EIA-860M vintages (monthly files back years — download the archive), compute how planned in-service dates for Arizona generation projects slipped vintage-over-vintage, by fuel type. Publish as both a data page and the second essay. This is the piece national energy media will cite. *Accept: a per-project slippage table with methodology, plus summary stats (median slip by fuel/year).*

## 6. Validation rules to hard-code
Cross-check BPS state total ≈ sum of places (known coverage gaps — document tolerance); EIA-860M AZ operating MW must move smoothly month-over-month (>5% jumps → investigate before publishing); QCEW employment vs. CES delta flagged >3%; every published figure traceable to a tidy-table row via a `figure_id` manifest.

## 7. Things NOT to build (scope discipline)
No user accounts, no comments, no CMS, no realtime anything, no scraping of paywalled/ToS-hostile sources, no forecasting in v1 (the slippage report is retrospective), no composite index before 8 quarters of history.

## 8. Definition of done for the grant demo
A live site where the six CORE metrics render with current data, every chart has a working CSV + methodology link, `git clone && make build` reproduces the numbers, and two essays are published — one launch overview, one slippage report. That artifact plus the repo is the Emergent Ventures deliverable.

## 9. .md contents to generate
Condense Sections 2, 4, and current-phase acceptance criteria. Include: "Fetch and inspect real source files before writing parsers. Never publish a number that fails validation. Snapshot raw data before parsing. Essays may not contain numbers that don't come from the pipeline. When a source schema surprises you, update SOURCES.md in the same commit."
