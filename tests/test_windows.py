import pytest
import numpy as np 
import pandas as pd
from pTRPred import roll_windows


def test_roll_windows_rolling_end():
    t = np.arange(10)
    out = roll_windows(t, window=4, step=2, align="end", type="rolling")
    # starts: 1,3,5,7 ; ends: 4,6,8,10
    assert out.shape[0] == 4
    assert out["start"].tolist() == [1, 3, 5, 7]
    assert out["end"].tolist() == [4, 6, 8, 10]
    assert out["t_rep"].tolist() == [t[3], t[5], t[7], t[9]]
    assert out["idx"].iloc[0] == [1, 2, 3, 4]


def test_roll_windows_expanding_center():
    t = np.arange(9)
    out = roll_windows(t, window=3, step=3, align="center", type="expanding")
    # ends: 3,6,9 ; starts all 1
    assert out["start"].tolist() == [1, 1, 1]
    assert out["end"].tolist() == [3, 6, 9]
    # centers: floor((1+3)/2)=2 -> t[1]; (1+6)/2=3 -> t[2]; (1+9)/2=5 -> t[4]
    assert out["t_rep"].tolist() == [t[1], t[2], t[4]]


def test_roll_windows_errors():
    with pytest.raises(ValueError):
        roll_windows([1, 2, 3], window=0)
    with pytest.raises(ValueError):
        roll_windows([1, 2, 3], window=2, step=0)
    with pytest.raises(ValueError):
        roll_windows([1, 2, 3], window=2, align="bad")  # type: ignore
    with pytest.raises(ValueError):
        roll_windows([1, 2, 3], window=2, type="bad")  # type: ignore
