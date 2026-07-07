# Sources

Source URLs and schemas must be verified live before parsers are written. Record retrieval date, URL, files inspected, expected schema, and any surprises here.

| Source | Status | Retrieval date | Notes |
|---|---|---:|---|
| Census Building Permits Survey (BPS) via FRED | Implemented for AZ, Phoenix MSA, Tucson MSA | 2026-07-07 | FRED pages report U.S. Census Bureau source, monthly not-seasonally-adjusted units, and Jun. 24, 2026 updates. Current raw snapshot covers Jan-May 2026 for `AZBPPRIV`, `PHOE004BPPRIV`, and `TUCS004BPPRIV`. |
| EIA-860M | Inspected, not yet parsed | 2026-07-07 | EIA page lists release date Jun. 25, 2026, next release Jul. 23, 2026, and monthly XLS files through May 2026. Phase 1 parser still needed. |
| EIA-923 | Not yet inspected | — | Phase 2 target. |
| EIA-930 | Not yet inspected | — | Phase 2 target; EIA API key expected via environment. |
| BLS QCEW | Inspected, not yet parsed | 2026-07-07 | BLS open data page documents CSV access; Phase 2 parser still needed. |
| Data center load curation | Implemented as hand-curated seed | 2026-07-07 | Raw CSV requires `source_url` per row and labels current values as seed values to verify against ACC April 2026 materials before launch. |
| Permit-cycle extracts | Awaiting data | — | Schema stub only until public-record extracts arrive. |
