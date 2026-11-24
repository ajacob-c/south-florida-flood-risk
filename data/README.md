# Data sources

Raw data is **not** committed (see `.gitignore`). Notebooks download what they can; two items need a manual download. Record the date you downloaded each dataset below.

| Dataset | Publisher | How it's obtained | Notes |
|---|---|---|---|
| Census tracts (2023 TIGER/Line) | US Census Bureau | Automatic via `pygris` | Florida, filtered to FIPS 12086 (Miami-Dade) and 12011 (Broward) |
| Housing units by tract | US Census Bureau (ACS 5-year, table B25001) | Manual or Census API | Used to normalize claims. Save as `data/raw/housing_units.csv` with columns `GEOID`, `housing_units` |
| Flood hazard zones | FEMA National Flood Hazard Layer (NFHL) | Automatic, ArcGIS REST query | Layer 28 "Flood Hazard Zones". Verify the layer id if the service changes |
| Flood insurance claims | FEMA OpenFEMA (NFIP Redacted Claims v2) | Automatic, OpenFEMA API | Filtered by county. Redacted: no addresses |
| Elevation (DEM) | USGS 3D Elevation Program | Automatic via `py3dep` (30 m) | Vertical datum NAVD88, meters |
| Social Vulnerability Index | CDC/ATSDR | **Manual**: download the Florida tract-level CSV from the CDC/ATSDR SVI site | Save as `data/raw/svi_florida.csv`. Needs columns `FIPS` and `RPL_THEMES` (overall percentile) |

## Manual steps

1. **SVI:** download the latest tract-level, state-specific (Florida) CSV from the CDC/ATSDR SVI data page. Save to `data/raw/svi_florida.csv`.
2. **Housing units:** pull ACS table B25001 for tracts in Miami-Dade and Broward (data.census.gov or the Census API). Save to `data/raw/housing_units.csv`.

## Download log

| Dataset | Date downloaded | Version / vintage |
|---|---|---|
| | | |

## Licenses

All sources above are US-government open data. Check each publisher's terms and cite them if you reuse results.
