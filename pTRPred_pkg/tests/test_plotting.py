import matplotlib
matplotlib.use("Agg")  # headless
import numpy as np
import pandas as pd

from pTRPred import plot_detection_overlay


def test_plot_detection_overlay_smoke(tmp_path):
    n = 50
    df = pd.DataFrame(
        {
            "time_ind": np.arange(n),
            "signal": np.random.default_rng(0).normal(size=n),
            "detected_value_rt": np.linspace(0, 2, n),
            "first_detection_time": [10] * n,
        }
    )
    outpath = tmp_path / "fig.png"
    fig, ax1, ax2 = plot_detection_overlay(df, threshold=1.3, save_path=str(outpath))
    assert fig is not None and ax1 is not None and ax2 is not None
    assert outpath.exists()
