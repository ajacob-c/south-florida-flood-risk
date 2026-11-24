"""Download helpers for FEMA NFHL, OpenFEMA claims, and Census tracts."""
from __future__ import annotations

import geopandas as gpd
import pandas as pd
import requests

from . import config


def get_tracts(year: int = 2023) -> gpd.GeoDataFrame:
    """Census tracts for Miami-Dade and Broward (EPSG:4326)."""
    from pygris import tracts

    frames = [
        tracts(state=config.STATE_FIPS, county=fips, year=year, cb=True)
        for fips in config.COUNTIES.values()
    ]
    gdf = pd.concat(frames, ignore_index=True)
    return gpd.GeoDataFrame(gdf[["GEOID", "geometry"]], crs=frames[0].crs).to_crs(config.WEB_CRS)


def fetch_nfhl(bbox: tuple[float, float, float, float], page_size: int = 1000) -> gpd.GeoDataFrame:
    """Page through FEMA NFHL flood hazard zones intersecting a lon/lat bbox."""
    xmin, ymin, xmax, ymax = bbox
    params = {
        "f": "geojson",
        "where": "1=1",
        "geometry": f"{xmin},{ymin},{xmax},{ymax}",
        "geometryType": "esriGeometryEnvelope",
        "inSR": "4326",
        "spatialRel": "esriSpatialRelIntersects",
        "outFields": "FLD_ZONE,SFHA_TF,ZONE_SUBTY",
        "outSR": "4326",
        "resultRecordCount": page_size,
    }
    frames, offset = [], 0
    while True:
        r = requests.get(config.NFHL_URL, params={**params, "resultOffset": offset}, timeout=120)
        r.raise_for_status()
        payload = r.json()
        feats = payload.get("features", [])
        if not feats:
            break
        frames.append(gpd.GeoDataFrame.from_features(feats, crs="EPSG:4326"))
        offset += len(feats)
        if len(feats) < page_size and not payload.get("exceededTransferLimit"):
            break
    if not frames:
        return gpd.GeoDataFrame(columns=["FLD_ZONE", "SFHA_TF", "geometry"], crs="EPSG:4326")
    return pd.concat(frames, ignore_index=True)


def fetch_nfip_claims(top: int = 1000) -> pd.DataFrame:
    """NFIP claims for both counties, aggregated to claim counts and paid totals per tract."""
    rows = []
    for fips in config.COUNTIES.values():
        county_code = config.STATE_FIPS + fips
        skip = 0
        while True:
            params = {
                "$filter": f"countyCode eq '{county_code}'",
                "$select": "censusTract,amountPaidOnBuildingClaim,amountPaidOnContentsClaim,yearOfLoss",
                "$top": top,
                "$skip": skip,
                "$format": "json",
            }
            r = requests.get(config.OPENFEMA_CLAIMS_URL, params=params, timeout=120)
            r.raise_for_status()
            batch = r.json().get("FimaNfipClaims", [])
            if not batch:
                break
            rows.extend(batch)
            skip += len(batch)
            if len(batch) < top:
                break
    df = pd.DataFrame(rows)
    if df.empty:
        return pd.DataFrame(columns=["GEOID", "claims", "paid_total"])
    df["paid"] = (
        pd.to_numeric(df["amountPaidOnBuildingClaim"], errors="coerce").fillna(0)
        + pd.to_numeric(df["amountPaidOnContentsClaim"], errors="coerce").fillna(0)
    )
    df = df.dropna(subset=["censusTract"])
    df["GEOID"] = df["censusTract"].astype(str).str.zfill(11)
    return df.groupby("GEOID").agg(claims=("paid", "size"), paid_total=("paid", "sum")).reset_index()
