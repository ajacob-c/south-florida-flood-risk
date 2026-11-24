# Next steps

Status as of 2026-11-23. Update this file as items are finished.

## Where things stand

The code and repo structure are in place, but **nothing has been run yet**: the notebooks have no outputs, `data/raw/` and `outputs/` are empty, and nothing has been published.

Done (code written, not yet run):

- Repo layout, `.gitignore`, `environment.yml`, `.env.example`, LICENSE, `data/README.md`
- `src/data_access.py`: census tracts (pygris), FEMA NFHL flood zones (REST query), OpenFEMA NFIP claims
- `src/scoring.py`: min-max scaling, weighted mean, risk index, high/low exposure x vulnerability labels; tests in `tests/test_scoring.py`
- `notebooks/01_data_prep.ipynb`: share of each tract in a FEMA high-risk zone (SFHA), claims per 1,000 housing units, SVI join
- `notebooks/02_exposure_analysis.ipynb`: 30 m USGS DEM, share of each tract at or below +1/+2/+3 ft
- `notebooks/03_risk_index_and_map.ipynb`: risk index, static and folium maps, weight sensitivity check, ArcGIS publish cell

## To do, in order

1. **Environment.** Install Miniforge, run `conda env create -f environment.yml`, `conda activate sfl-flood`, `pytest`. Run `git init` and make a first commit.
2. **First end-to-end run.** Download the two manual inputs (see `data/README.md`): the Florida tract-level SVI CSV → `data/raw/svi_florida.csv`, and ACS table B25001 housing units → `data/raw/housing_units.csv`. Run notebooks 01 → 03 and fix what breaks. Fill in the download log in `data/README.md`.
3. **Fix the method.**
   - Measure the sea-level-rise cutoffs from the local average high tide line (MHHW), not from NAVD88 zero, so "+1 ft" matches what NOAA's Sea Level Rise Viewer means.
   - Switch the DEM from 30 m to 10 m (or 1 m lidar) and mask out canals and lakes.
   - Split NFIP claims out of the exposure score into its own **history score**, as the original spec has three scores: exposure, history, vulnerability.
   - Move the elevation code from notebook 02 into a helper in `src/`.
4. **FEMA-versus-elevation comparison (the headline finding).** Find areas that are low-lying but outside FEMA high-risk zones, and the reverse. Summarize by tract and map it.
5. **Buildings.** Add building footprints (Microsoft or county open data) and compute % of buildings below the elevation cutoff.
6. **Publish and write up.** Hosted feature layer plus an ArcGIS Online web map, a map screenshot in `outputs/`, and key findings in `README.md`.
7. **Stretch goals.** Pump station coverage layer first (it fits with step 4), then a sea level rise scenario slider, storm high-water-mark validation, and a GitHub Pages viewer.

## Things to check when running

- **Tract boundaries.** 2023 tracts, SVI and ACS use 2020 tract boundaries. OpenFEMA `censusTract` on older claims may use 2010 boundaries. After the claims join in notebook 01, count unmatched claims.
- **FEMA download.** `fetch_nfhl` queries a bounding box that is mostly Everglades and ocean, 1,000 polygons per request. It may be slow or time out; consider querying per county or caching per tile.
- **Large files.** Keep DEM tiles and other raw data out of git and out of OneDrive.
