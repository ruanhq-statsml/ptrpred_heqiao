from __future__ import annotations

from typing import Any, Dict, Optional, Sequence

import numpy as np
import pandas as pd
import warnings

from .preprocessing import extract_X
from .rollsvd import roll_svd


def fit_arimax_vec(
    y,
    xreg: Optional[np.ndarray] = None,
    seasonal: bool = True,
    stepwise: bool = True,
    approximation: bool = False,
    **kwargs: Any,
) -> Dict[str, Any]:
    """Fit a single ARIMAX model (auto-selected order) and return aligned residuals/fitted."""
    try:
        import pmdarima as pm  # type: ignore
    except Exception as e:
        raise ImportError(
            "Package 'pmdarima' is required for ARIMAX functionality. "
            "Install it with: pip install rollsvd-tools[arima]"
        ) from e

    y_arr = np.asarray(y, dtype=float).reshape(-1)
    n = int(y_arr.shape[0])

    if xreg is not None:
        X = np.asarray(xreg, dtype=float)
        if X.ndim == 1:
            X = X.reshape(-1, 1)
        if X.shape[0] != n:
            raise ValueError("`xreg` must have the same number of rows as `y`.")
        ok = np.isfinite(y_arr) & np.isfinite(X).all(axis=1)
        X_used = X[ok, :]
    else:
        ok = np.isfinite(y_arr)
        X_used = None

    if not np.any(ok):
        raise ValueError("No complete cases available for ARIMAX fit.")

    y_used = y_arr[ok]

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        model = pm.auto_arima(
            y=y_used,
            X=X_used,
            seasonal=seasonal,
            stepwise=stepwise,
            approximation=approximation,
            error_action="warn",
            suppress_warnings=True,
            **kwargs,
        )

    try:
        fitted_used = model.predict_in_sample(X=X_used)
    except TypeError:
        fitted_used = model.predict_in_sample(exogenous=X_used)

    try:
        resid_used = model.resid()
    except Exception:
        resid_used = y_used - np.asarray(fitted_used, dtype=float)

    return {
        "model": model,
        "residuals": np.asarray(resid_used, dtype=float).reshape(-1),
        "fitted": np.asarray(fitted_used, dtype=float).reshape(-1),
        "mask": ok,
    }


def arimax_residuals_df(
    data: pd.DataFrame,
    time: str,
    y_cols: Sequence[str] | str,
    xreg_cols: Sequence[str] | str,
    seasonal: bool = True,
    stepwise: bool = True,
    approximation: bool = False,
    **kwargs: Any,
) -> Dict[str, Any]:
    """Batch ARIMAX residuals for multiple series with a common regressor set."""
    if time not in data.columns:
        raise ValueError("`time` must be a column in `data`.")

    Ymat = extract_X(data, y_cols)
    Xreg = extract_X(data, xreg_cols)
    tvec = data[time].to_numpy()

    ok = np.isfinite(Ymat.to_numpy()).all(axis=1) & np.isfinite(Xreg.to_numpy()).all(axis=1)
    if not np.any(ok):
        raise ValueError("No complete cases across y_cols and xreg_cols for ARIMAX.")

    Y_ok = Ymat.loc[ok, :].reset_index(drop=True)
    X_ok = Xreg.loc[ok, :].reset_index(drop=True)
    t_ok = tvec[ok]

    n_ok, p_y = Y_ok.shape
    Resids = np.full((n_ok, p_y), np.nan, dtype=float)
    models: Dict[str, Any] = {}

    for j, col in enumerate(Y_ok.columns):
        fitj = fit_arimax_vec(
            y=Y_ok[col].to_numpy(),
            xreg=X_ok.to_numpy(),
            seasonal=seasonal,
            stepwise=stepwise,
            approximation=approximation,
            **kwargs,
        )
        inner_ok = fitj["mask"]
        Resids[inner_ok, j] = fitj["residuals"]
        models[col] = fitj["model"]

    residuals_df = pd.DataFrame({"time": t_ok})
    for j, col in enumerate(Y_ok.columns):
        residuals_df[col] = Resids[:, j]

    return {"residuals_df": residuals_df, "models": models, "mask": ok}


def arimax_then_roll_svd(
    data: pd.DataFrame,
    time: str,
    y_cols: Sequence[str] | str,
    xreg_cols: Sequence[str] | str,
    window: int,
    step: int = 1,
    align: str = "end",
    type: str = "rolling",
    center: bool = True,
    scale_: bool = False,
    k: Optional[int] = None,
    fast: bool = True,
    na_action: str = "omit_rows",
    cov_on_pairwise: bool = True,
    seasonal: bool = True,
    stepwise: bool = True,
    approximation: bool = False,
    values_only: bool = True,
    seed: Optional[int] = None,
    **kwargs: Any,
) -> Dict[str, Any]:
    """Pipeline: ARIMAX residuals → rolling SVD on residual covariance."""
    fit = arimax_residuals_df(
        data=data,
        time=time,
        y_cols=y_cols,
        xreg_cols=xreg_cols,
        seasonal=seasonal,
        stepwise=stepwise,
        approximation=approximation,
        **kwargs,
    )

    residuals_df = fit["residuals_df"]
    res_cols = [c for c in residuals_df.columns if c != "time"]

    svd_fit = roll_svd(
        data=residuals_df,
        time="time",
        x_cols=res_cols,
        window=window,
        step=step,
        align=align,  # type: ignore[arg-type]
        type=type,    # type: ignore[arg-type]
        center=center,
        scale_=scale_,
        k=k,
        fast=fast,
        na_action=na_action,  # type: ignore[arg-type]
        cov_on_pairwise=cov_on_pairwise,
        values_only=values_only,
        seed=seed,
    )

    return {"residuals_df": residuals_df, "rollsvd": svd_fit, "models": fit["models"], "mask": fit["mask"]}
