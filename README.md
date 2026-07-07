# Arizona Abundance Index

A reproducible data pipeline and static publication site for tracking whether Arizona is building housing, energy, chips, data centers, and permit capacity.

## Quick start

```bash
make install
make test
make build
```

## Configuration

Copy `.env.example` to `.env` and set `EIA_API_KEY` before working with EIA API-backed sources. Phase 0 does not fetch live data.
