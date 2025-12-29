import numpy as np
import pandas as pd

from pTRPred import detect_asvotes, detect_realtime, write_rt_csv


def test_detect_asvotes_basic():
    y = np.linspace(0, 1, 120)
    votes = detect_asvotes(y, lowwl=5, highwl=20, mad_k=2.5, direction="positive")
    assert votes.shape == y.shape
    assert np.all(np.isfinite(votes))
    assert np.max(np.abs(votes)) <= 1.0 + 1e-12


def test_detect_realtime_columns_and_first_time():
    t = np.arange(200)
    y = np.concatenate([np.zeros(100), np.linspace(0, 10, 100)])
    out = detect_realtime(t, y, lowwl=5, highwl=30, mad_k=2.5, direction="positive", burn_in=60, smooth_k=10)
    assert list(out.columns) == [
        "time_ind",
        "signal",
        "detected_offline",
        "detected_value_rt",
        "flag",
        "first_detection_time",
    ]
    assert out["flag"].dtype == bool
    # first_detection_time constant per spec
    assert out["first_detection_time"].nunique(dropna=False) == 1


def test_write_rt_csv(tmp_path):
    df = pd.DataFrame({"a": [1, 2], "b": [3, 4]})
    p = tmp_path / "out.csv"
    ret = write_rt_csv(df, str(p))
    assert ret == str(p)
    assert p.exists()
