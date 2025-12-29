from __future__ import annotations

from typing import Literal, Sequence
import numpy as np
import pandas as pd


def roll_windows(
    time: Sequence,
    window: int,
    step: int = 1,
    align: Literal["end", "center", "start"] = "end",
    type: Literal["rolling", "expanding"] = "rolling",
) -> pd.DataFrame:
    """Build rolling / expanding window indices over a time vector.

    Parameters
    ----------
    time:
        Sequence of time stamps/indices. Stored in output as `t_rep` per window.
    window:
        Window length. Must be >= 1.
    step:
        Step between successive windows. Must be >= 1.
    align:
        Which time point to use as window representative:
        - "end": end index
        - "start": start index
        - "center": floor((start+end)/2)
    type:
        - "rolling": fixed window length (except when n < window)
        - "expanding": start fixed at 1, end expands from `window` onward

    Returns
    -------
    pd.DataFrame with columns:
      - window_id: 1..W
      - start, end: 1-based inclusive indices into `time`
      - t_rep: representative time value according to `align`
      - idx: list of 1-based indices within each window
    """
    if window < 1:
        raise ValueError("`window` must be >= 1")
    if step < 1:
        raise ValueError("`step` must be >= 1")

    align = align.lower()
    if align not in {"end", "center", "start"}:
        raise ValueError("`align` must be one of {'end','center','start'}")

    type = type.lower()
    if type not in {"rolling", "expanding"}:
        raise ValueError("`type` must be one of {'rolling','expanding'}")

    ts = pd.Series(time)
    n = len(ts)

    if type == "rolling":
        if n < window:
            starts = np.array([1], dtype=int)
            ends = np.array([n], dtype=int)
        else:
            starts = np.arange(1, n - window + 2, step, dtype=int)
            ends = starts + window - 1
    else:  # expanding
        if n < window:
            ends = np.array([n], dtype=int)
        else:
            ends = np.arange(window, n + 1, step, dtype=int)
            if ends.size == 0:
                ends = np.array([n], dtype=int)
        starts = np.full_like(ends, 1)

    if align == "end":
        t_rep_idx_1b = ends
    elif align == "start":
        t_rep_idx_1b = starts
    else:
        t_rep_idx_1b = np.floor((starts + ends) / 2).astype(int)

    t_rep = ts.iloc[t_rep_idx_1b - 1].to_numpy()
    idx_list = [list(range(int(s), int(e) + 1)) for s, e in zip(starts, ends)]

    return pd.DataFrame(
        {
            "window_id": np.arange(1, len(starts) + 1, dtype=int),
            "start": starts,
            "end": ends,
            "t_rep": t_rep,
            "idx": idx_list,
        }
    )
