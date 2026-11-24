"""Scaling and risk-index functions (pure pandas, no GIS dependencies)."""
from __future__ import annotations

import numpy as np
import pandas as pd


def minmax(s: pd.Series, clip_pct: float = 0.99) -> pd.Series:
    """Scale to 0-1. Values above the `clip_pct` quantile are capped first so a few
    extreme tracts don't squash everyone else toward zero."""
    s = pd.to_numeric(s, errors="coerce")
    if s.notna().sum() == 0:
        return s
    hi = s.quantile(clip_pct)
    lo = s.min()
    s = s.clip(upper=hi)
    if hi == lo:
        return pd.Series(0.0, index=s.index).where(s.notna())
    return (s - lo) / (hi - lo)


def weighted_mean(df: pd.DataFrame, weights: dict[str, float]) -> pd.Series:
    """Weighted mean across columns, renormalizing weights over non-missing values."""
    cols = list(weights)
    w = pd.Series(weights, dtype=float)
    vals = df[cols]
    mask = vals.notna()
    num = (vals.fillna(0) * w).sum(axis=1)
    den = (mask * w).sum(axis=1)
    return (num / den).where(den > 0)


def compute_risk_index(
    df: pd.DataFrame,
    exposure_weights: dict[str, float],
    risk_weights: dict[str, float],
    vulnerability_col: str = "svi",
) -> pd.DataFrame:
    """Add scaled components, `exposure`, `vulnerability`, and `risk` columns (0-1)."""
    out = df.copy()
    for col in exposure_weights:
        out[f"{col}_scaled"] = minmax(out[col])
    scaled = {f"{c}_scaled": w for c, w in exposure_weights.items()}
    out["exposure"] = weighted_mean(out, scaled)
    out["vulnerability"] = pd.to_numeric(out[vulnerability_col], errors="coerce").clip(0, 1)
    out["risk"] = (
        risk_weights["exposure"] * out["exposure"]
        + risk_weights["vulnerability"] * out["vulnerability"]
    )
    return out


def label_quadrant(df: pd.DataFrame, threshold: float = 0.5) -> pd.Series:
    """Label tracts by exposure x vulnerability."""
    hi_e = df["exposure"] >= threshold
    hi_v = df["vulnerability"] >= threshold
    labels = np.select(
        [hi_e & hi_v, hi_e & ~hi_v, ~hi_e & hi_v],
        ["High exposure / High vulnerability", "High exposure / Lower vulnerability",
         "Lower exposure / High vulnerability"],
        default="Lower exposure / Lower vulnerability",
    )
    return pd.Series(labels, index=df.index).where(df["exposure"].notna() & df["vulnerability"].notna())
