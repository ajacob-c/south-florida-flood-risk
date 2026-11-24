import numpy as np
import pandas as pd

from src import config
from src.scoring import compute_risk_index, label_quadrant, minmax, weighted_mean


def test_minmax_range_and_constant():
    s = pd.Series([0, 5, 10, 100])
    out = minmax(s, clip_pct=1.0)
    assert out.min() == 0 and out.max() == 1
    assert (minmax(pd.Series([3, 3, 3])) == 0).all()


def test_minmax_clips_outliers():
    s = pd.Series(list(range(100)) + [10_000])
    out = minmax(s, clip_pct=0.99)
    assert out.max() == 1.0
    assert out.iloc[50] > 0.4  # not squashed by the outlier


def test_weighted_mean_handles_missing():
    df = pd.DataFrame({"a": [1.0, np.nan], "b": [0.0, 1.0]})
    out = weighted_mean(df, {"a": 0.5, "b": 0.5})
    assert out.iloc[0] == 0.5
    assert out.iloc[1] == 1.0  # renormalized over the one available value


def test_risk_index_and_quadrants():
    df = pd.DataFrame({
        "sfha_share": [0.0, 1.0, 1.0, 0.0],
        "low_elev_share": [0.0, 1.0, 1.0, 0.0],
        "claims_rate": [0.0, 10.0, 10.0, 0.0],
        "svi": [0.0, 1.0, 0.0, 1.0],
    })
    out = compute_risk_index(df, config.EXPOSURE_WEIGHTS, config.RISK_WEIGHTS)
    assert out["risk"].iloc[1] > out["risk"].iloc[0]
    q = label_quadrant(out)
    assert q.iloc[1] == "High exposure / High vulnerability"
    assert q.iloc[2] == "High exposure / Lower vulnerability"
    assert q.iloc[3] == "Lower exposure / High vulnerability"
    assert q.iloc[0] == "Lower exposure / Lower vulnerability"
