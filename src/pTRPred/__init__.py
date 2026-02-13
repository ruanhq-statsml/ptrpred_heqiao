"""pTRPred public API."""

from .windows import roll_windows
from .preprocessing import extract_X, na_handle
from .rollsvd import roll_svd, as_tibble_rollsvd
from .kernelpca import roll_kernel_pca
from .arimax import fit_arimax_vec, arimax_residuals_df, arimax_then_roll_svd
from .signals import (
    build_signal_raw,
    build_signal_svd,
    build_signal_kernel_pca,
    build_signal_arimax_resid,
    build_signal_arimax_svd,
)
from .detection import detect_asvotes, detect_realtime, write_rt_csv
from .plotting import plot_detection_overlay

__all__ = [
    "roll_windows",
    "extract_X",
    "na_handle",
    "roll_svd",
    "as_tibble_rollsvd",
    "roll_kernel_pca",
    "fit_arimax_vec",
    "arimax_residuals_df",
    "arimax_then_roll_svd",
    "build_signal_raw",
    "build_signal_svd",
    "build_signal_kernel_pca",
    "build_signal_arimax_resid",
    "build_signal_arimax_svd",
    "detect_asvotes",
    "detect_realtime",
    "write_rt_csv",
    "plot_detection_overlay",
    "OnlineRealtimeDetector",
    "OnlineASVotesSliding",
    "detect_realtime_incremental",
    "detect_asvotes"    
]

__version__ = "0.1.0"
