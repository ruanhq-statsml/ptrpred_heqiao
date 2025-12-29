import numpy as np
import pandas as pd

from pTRPred import roll_svd, as_tibble_rollsvd


def test_roll_svd_values_only_shapes_and_order():
    n = 30
    rng = np.random.default_rng(0)
    df = pd.DataFrame(
        {
            "time": np.arange(n),
            "x1": rng.normal(size=n),
            "x2": rng.normal(size=n),
            "x3": rng.normal(size=n),
        }
    )
    fit = roll_svd(df, time="time", x_cols=["x1", "x2", "x3"], window=10, step=5, k=2, values_only=True)
    assert fit["windows"].shape[0] == len(fit["D"])
    for d in fit["D"]:
        if d is None:
            continue
        assert len(d) == 2
        # descending order
        assert d[0] >= d[1]


def test_roll_svd_full_outputs_and_tibble():
    n = 25
    rng = np.random.default_rng(1)
    df = pd.DataFrame(
        {
            "time": np.arange(n),
            "x1": rng.normal(size=n),
            "x2": rng.normal(size=n),
        }
    )
    fit = roll_svd(df, time="time", x_cols="x1|x2", window=8, step=4, k=1, values_only=False, fast=False)
    assert fit["V"] is not None
    assert fit["U_scores"] is not None
    # at least one window should succeed
    assert any(v is not None for v in fit["V"])
    tbl = as_tibble_rollsvd(fit, what="singular_values")
    assert tbl is not None
    assert set(tbl.columns) == {"window_id", "factor", "d"}
