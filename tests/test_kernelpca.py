"""Unit tests for roll_kernel_pca and build_signal_kernel_pca."""

import pytest

pytest.importorskip("sklearn")

import numpy as np
import pandas as pd

from pTRPred import roll_kernel_pca, build_signal_kernel_pca


def test_roll_kernel_pca_basic():
    """roll_kernel_pca returns correct structure and D list length."""
    n = 40
    rng = np.random.default_rng(42)
    df = pd.DataFrame(
        {
            "time": np.arange(n),
            "x1": rng.normal(size=n),
            "x2": rng.normal(size=n),
            "x3": rng.normal(size=n),
        }
    )
    fit = roll_kernel_pca(
        df,
        time="time",
        x_cols=["x1", "x2", "x3"],
        window=10,
        step=5,
        n_components=1,
        kernel="rbf",
    )
    assert "windows" in fit
    assert "D" in fit
    assert "scores" in fit
    assert "colnames" in fit
    assert "preproc" in fit
    assert fit["kernel"] == "rbf"
    assert fit["windows"].shape[0] == len(fit["D"])
    assert fit["colnames"] == ["x1", "x2", "x3"]
    # At least some windows should have non-None eigenvalues
    non_none = [d for d in fit["D"] if d is not None]
    assert len(non_none) >= 1
    for d in non_none:
        assert len(d) == 1
        assert np.isfinite(d[0]) and d[0] >= 0


def test_roll_kernel_pca_linear_kernel():
    """roll_kernel_pca with linear kernel runs and returns valid D."""
    n = 25
    rng = np.random.default_rng(1)
    df = pd.DataFrame(
        {"time": np.arange(n), "a": rng.normal(size=n), "b": rng.normal(size=n)}
    )
    fit = roll_kernel_pca(
        df,
        time="time",
        x_cols="a|b",
        window=8,
        step=4,
        n_components=1,
        kernel="linear",
    )
    assert fit["kernel"] == "linear"
    assert len(fit["D"]) == fit["windows"].shape[0]
    non_none = [d for d in fit["D"] if d is not None]
    assert len(non_none) >= 1


def test_roll_kernel_pca_na_omit_rows():
    """roll_kernel_pca with na_action=omit_rows handles NaNs."""
    n = 30
    rng = np.random.default_rng(5)
    df = pd.DataFrame(
        {
            "time": np.arange(n),
            "x1": rng.normal(size=n),
            "x2": rng.normal(size=n),
        }
    )
    df.loc[5, "x1"] = np.nan
    df.loc[12, "x2"] = np.nan
    fit = roll_kernel_pca(
        df,
        time="time",
        x_cols=["x1", "x2"],
        window=10,
        step=5,
        na_action="omit_rows",
    )
    assert len(fit["D"]) == fit["windows"].shape[0]
    non_none = [d for d in fit["D"] if d is not None]
    assert len(non_none) >= 1


def test_roll_kernel_pca_expanding():
    """roll_kernel_pca with type=expanding runs."""
    n = 20
    rng = np.random.default_rng(7)
    df = pd.DataFrame(
        {"time": np.arange(n), "u": rng.normal(size=n), "v": rng.normal(size=n)}
    )
    fit = roll_kernel_pca(
        df,
        time="time",
        x_cols=["u", "v"],
        window=6,
        step=3,
        type="expanding",
        kernel="rbf",
    )
    assert fit["windows"].shape[0] >= 1
    assert len(fit["D"]) == fit["windows"].shape[0]


def test_roll_kernel_pca_missing_time_raises():
    """roll_kernel_pca raises when time column is missing."""
    df = pd.DataFrame({"t": [1, 2, 3], "x": [1.0, 2.0, 3.0]})
    with pytest.raises(ValueError, match="`time` must be a column"):
        roll_kernel_pca(df, time="time", x_cols="x", window=2)


def test_roll_kernel_pca_invalid_na_action_raises():
    """roll_kernel_pca raises for invalid na_action."""
    df = pd.DataFrame({"time": [1, 2, 3], "x": [1.0, 2.0, 3.0]})
    with pytest.raises(ValueError, match="na_action"):
        roll_kernel_pca(
            df,
            time="time",
            x_cols="x",
            window=2,
            na_action="invalid",
        )


def test_build_signal_kernel_pca_output_shape():
    """build_signal_kernel_pca returns DataFrame with time_ind and signal."""
    n = 35
    rng = np.random.default_rng(10)
    df = pd.DataFrame(
        {
            "time": np.arange(n),
            "x1": rng.normal(size=n),
            "x2": rng.normal(size=n),
        }
    )
    out = build_signal_kernel_pca(
        df,
        time="time",
        x_cols=["x1", "x2"],
        window=10,
        step=5,
        kernel="rbf",
    )
    assert isinstance(out, pd.DataFrame)
    assert list(out.columns) == ["time_ind", "signal"]
    # Number of rows = number of windows from roll_windows
    n_windows = max(1, (n - 10) // 5 + 1) if n >= 10 else 1
    assert len(out) == n_windows
    assert out["time_ind"].notna().all()
    # signal can have NaNs for failed windows
    assert out["signal"].dtype == float


def test_build_signal_kernel_pca_linear():
    """build_signal_kernel_pca with linear kernel produces finite signal where expected."""
    n = 30
    rng = np.random.default_rng(3)
    df = pd.DataFrame(
        {
            "time": np.arange(n),
            "a": rng.normal(size=n),
            "b": rng.normal(size=n),
        }
    )
    out = build_signal_kernel_pca(
        df,
        time="time",
        x_cols=["a", "b"],
        window=8,
        step=4,
        kernel="linear",
    )
    assert out.shape[1] == 2
    assert (out["signal"].notna() | np.isnan(out["signal"])).all()
    # At least one finite value
    assert np.any(np.isfinite(out["signal"]))
