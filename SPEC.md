# Project spec: "Who is most exposed to flooding in Miami-Dade and Broward?"

The original project brief. Current status and to-dos live in `NEXT_STEPS.md`.

## The question

Which neighborhoods face the highest flood exposure, and which of those are also the least able to recover?

## Data (all free)

- **FEMA National Flood Hazard Layer:** official flood zones (AE, VE, X and so on).
- **USGS 3DEP elevation (DEM):** ground elevation. South Florida is so flat that a foot or two matters a lot.
- **NOAA Sea Level Rise Viewer:** inundation layers for 1 to 6 ft scenarios.
- **OpenFEMA NFIP claims and policies:** historical flood insurance claims by ZIP code or census tract. This shows where floods actually caused damage, not just where models say they could.
- **CDC/ATSDR Social Vulnerability Index (SVI):** income, age, vehicle access and housing, by census tract.
- **Miami-Dade and Broward open data portals:** parcels, building footprints, drainage and pump stations, and the county flood-related layers.

## Analysis steps

1. Clip everything to the two counties and project to a common CRS (Florida East State Plane, EPSG:2236, or UTM 17N).
2. **Exposure score** per tract: percent of area in high-risk FEMA zones, percent of buildings below a set elevation, and area inundated at +1, +2 and +3 ft of sea level rise.
3. **History score:** NFIP claims per 1,000 housing units.
4. **Vulnerability score:** the SVI percentile.
5. Combine them into a risk index and map the top tracts (high exposure and high vulnerability).
6. **Check the result:** compare where the FEMA zones and your elevation-based zones disagree. Those mismatches are often the most interesting finding.
7. Publish the result as a hosted feature layer or web map, and write up the method in a notebook.

## Repo layout

```
south-florida-flood-risk/
├── README.md          # map screenshot, question, key findings, method
├── environment.yml    # arcgis, geopandas, rasterio, jupyter
├── .gitignore         # *.gdb, *.aprx, .env, data/raw/
├── data/README.md     # sources, download dates, licenses
├── notebooks/
│   ├── 01_data_prep.ipynb
│   ├── 02_exposure_analysis.ipynb
│   └── 03_risk_index_and_map.ipynb
├── src/               # scoring and helper functions
└── outputs/           # small GeoJSON + final map images
```

## Notes for a free account

- Use rasterio and GeoPandas for the heavy DEM and overlay work. They cost no credits and keep the repo runnable by anyone.
- Use ArcGIS Online for publishing the final layers and the interactive map.
- Don't commit the raw DEM tiles or other large files. Document the download steps instead.

## Stretch goals

- Compare 2 to 3 sea-level-rise scenarios and animate or slider-toggle them.
- Add a "pump station coverage" layer to show where drainage infrastructure is thin.
- Overlay a recent storm's high-water marks or rainfall (NOAA, USGS) to validate the model.
- Host a simple Maps SDK for JavaScript viewer on GitHub Pages.
