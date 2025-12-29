from __future__ import annotations

from typing import Optional, Tuple

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def plot_detection_overlay(
    df: pd.DataFrame,
    title: str = "Real-time Detection vs Signal",
    time_col: str = "time_ind",
    score_col: str = "detected_value_rt",
    signal_col: str = "signal",
    first_det_col: str = "first_detection_time",
    score_label: str = "Real-Time Detected Value",
    signal_label: str = "Signal",
    x_label: str = "Index",
    threshold: Optional[float] = None,
    scale_factor: Optional[float] = None,
    score_color: str = "red",
    signal_color: str = "black",
    save_path: Optional[str] = None,
    width: float = 9,
    height: float = 7.5,
    dpi: int = 300,
) -> Tuple[plt.Figure, plt.Axes, plt.Axes]:
    """Overlay real-time detection score and signal with threshold & first-crossing."""
    df_local = df.copy()

    x = df_local[time_col].to_numpy()
    sc = pd.to_numeric(df_local[score_col], errors="coerce").to_numpy()
    sg = pd.to_numeric(df_local[signal_col], errors="coerce").to_numpy()

    if scale_factor is None:
        rng_sc = (np.nanmin(sc), np.nanmax(sc))
        rng_sg = (np.nanmin(sg), np.nanmax(sg))
        span_sc = rng_sc[1] - rng_sc[0]
        span_sg = rng_sg[1] - rng_sg[0]
        if not np.isfinite(span_sc) or span_sc == 0 or not np.isfinite(span_sg) or span_sg == 0:
            alpha = 1.0
        else:
            alpha = float(span_sc / span_sg)
    else:
        alpha = float(scale_factor) if np.isfinite(scale_factor) and scale_factor != 0 else 1.0

    scaled_signal = sg * alpha

    first_det_time = None
    if first_det_col in df_local.columns:
        vals = df_local[first_det_col].unique()
        cleaned = [v for v in vals if not pd.isna(v)]
        if cleaned:
            first_det_time = cleaned[0]

    fig, ax1 = plt.subplots(figsize=(width, height), dpi=dpi)

    ax1.plot(x, sc, color=score_color, linewidth=1.2, label=score_label)
    ax1.set_ylabel(score_label, color=score_color)
    ax1.tick_params(axis="y", labelcolor=score_color)

    ax1.plot(x, scaled_signal, color=signal_color, linewidth=1.0, alpha=0.85, label=signal_label)

    if threshold is not None and np.isfinite(threshold):
        ax1.axhline(y=float(threshold), linestyle="--", color=score_color, linewidth=0.9)

    if first_det_time is not None:
        ax1.axvline(x=first_det_time, linestyle=":", color="steelblue", linewidth=1.0)

    ax1.set_xlabel(x_label)
    ax1.set_title(title)

    ax2 = ax1.twinx()
    ax2.set_ylabel(signal_label, color=signal_color)
    ax2.tick_params(axis="y", labelcolor=signal_color)

    left_ticks = ax1.get_yticks()
    ax2.set_yticks(left_ticks)
    ax2.set_yticklabels([f"{(yt / alpha):.3g}" for yt in left_ticks])

    lines = ax1.get_lines()
    ax1.legend(lines[:2], [score_label, signal_label], loc="upper right")

    plt.tight_layout()

    if save_path is not None:
        fig.savefig(save_path, dpi=dpi, bbox_inches="tight")

    return fig, ax1, ax2
