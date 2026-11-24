# Project notes for Claude

**Question:** which neighborhoods (census tracts) in Miami-Dade and Broward face the highest flood exposure, and which of those are also the least able to recover?

- `SPEC.md`: the full original brief (data sources, analysis steps, stretch goals). Read it when you need details on what "done" means.
- `NEXT_STEPS.md`: current status and the to-do list. Read it at the start of a session and update it when an item is finished.

## Rules

- Scores per tract: exposure, history (NFIP claims per 1,000 housing units), vulnerability (SVI percentile), combined into a risk index.
- Use EPSG:2236 (Florida East State Plane, ftUS) for all area and distance math.
- Do the heavy DEM and overlay work with rasterio and GeoPandas. Use ArcGIS Online only for publishing the final layers and map.
- Never commit raw data, DEM tiles, `.env`, `*.gdb` or `*.aprx`. Document download steps in `data/README.md` instead.
- Conda environment: `sfl-flood` (`environment.yml`). Run tests with `pytest`.
