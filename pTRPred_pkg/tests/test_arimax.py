import numpy as np
import pandas as pd
import pytest

from pTRPred.arimax import fit_arimax_vec, arimax_residuals_df


def test_fit_arimax_vec_smoke():
    pm = pytest.importorskip("pmdarima")
    rng = np.random.default_rng(0)
    n = 80
    x = rng.normal(size=(n, 2))
    y = 0.5 * x[:, 0] + rng.normal(scale=0.5, size=n)
    # include a few NaNs
    y[5] = np.nan
    x[10, 1] = np.nan
    fit = fit_arimax_vec(y, xreg=x, seasonal=False, stepwise=True)
    assert "mask" in fit and fit["mask"].shape[0] == n
    assert fit["residuals"].shape[0] == int(np.sum(fit["mask"]))


def test_arimax_residuals_df_smoke():
    pm = pytest.importorskip("pmdarima")
    rng = np.random.default_rng(1)
    n = 60
    df = pd.DataFrame(
        {
            "time": np.arange(n),
            "y1": rng.normal(size=n),
            "y2": rng.normal(size=n),
            "x1": rng.normal(size=n),
            "x2": rng.normal(size=n),
        }
    )
    out = arimax_residuals_df(df, time="time", y_cols=["y1", "y2"], xreg_cols=["x1", "x2"], seasonal=False)
    res = out["residuals_df"]
    assert "time" in res.columns
    assert set(res.columns) == {"time", "y1", "y2"}
