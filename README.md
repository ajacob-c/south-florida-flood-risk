# South Florida Flood Risk: Miami-Dade & Broward

**Which neighborhoods are most exposed to flooding, and which of those are also the least able to recover?**

This project combines flood-zone maps, ground elevation, sea-level-rise scenarios, historical flood-insurance claims, and social vulnerability into a single tract-level risk index for Miami-Dade and Broward counties, then publishes the result as an interactive ArcGIS web map.

> Add a screenshot or GIF of your final map here: `![map](outputs/risk_map.png)`

## Method at a glance

| Component | Source | Measure (per census tract) |
|---|---|---|
| Regulatory exposure | FEMA National Flood Hazard Layer | % of tract area in Special Flood Hazard Areas (SFHA) |
| Physical exposure | USGS 3DEP DEM | % of tract area at or below +1, +2, +3 ft (NAVD88) |
| Historical impact | OpenFEMA NFIP claims | Claims per 1,000 housing units |
| Vulnerability | CDC/ATSDR Social Vulnerability Index | Overall SVI percentile |

Each component is scaled 0-1 and combined with adjustable weights (see `src/config.py`):

```
exposure = mean(SFHA share, low-elevation share, claims rate)
risk     = weighted blend of exposure and vulnerability
```

Tracts are then labelled by quadrant (high/low exposure x high/low vulnerability). The "high / high" tracts are the priority list.

### Known limitations (read before citing results)

- The elevation screen is a **"bathtub" model**: it flags every cell at or below a threshold and ignores hydrologic connectivity, drainage, pumps, and tides. It overstates inundation in places that are low but disconnected from the water, and it is not a substitute for NOAA's or the counties' hydrodynamic modeling.
- NFIP claims reflect where people **carry flood insurance and filed claims**, which is not the same as where flooding occurs.
- Tract-level results hide variation within tracts.
- This is a learning/portfolio project, not an official risk assessment.

## Repository layout

```
├── notebooks/
│   ├── 01_data_prep.ipynb          # download + build tract-level base table
│   ├── 02_exposure_analysis.ipynb  # DEM + bathtub inundation by tract
│   └── 03_risk_index_and_map.ipynb # score, map, (optionally) publish to ArcGIS
├── src/
│   ├── config.py                   # counties, CRS, weights, endpoints
│   ├── data_access.py              # FEMA / OpenFEMA / Census helpers
│   └── scoring.py                  # normalization + risk index
├── tests/test_scoring.py
├── data/README.md                  # sources, licenses, manual download steps
├── environment.yml
└── .env.example
```

## Getting started

```bash
git clone <your-repo-url>
cd south-florida-flood-risk
conda env create -f environment.yml
conda activate sfl-flood
cp .env.example .env     # only needed if you want to publish to ArcGIS Online
jupyter lab
```

Run the notebooks in order. Raw downloads are cached in `data/raw/` (git-ignored); small processed outputs land in `data/processed/` and `outputs/`.

### ArcGIS account (optional)

Everything except the final publish step runs with open-source tools and no account. To publish the result as a hosted feature layer, use a free [ArcGIS Location Platform](https://location.arcgis.com/sign-up) or ArcGIS Public account and put your credentials in `.env` (never commit it).

## Tests

```bash
pytest
```

## Data sources and licenses

See [`data/README.md`](data/README.md). Cite the original sources if you reuse results.

## License

Code: MIT (see `LICENSE`). Data retains the licenses of its original publishers.
