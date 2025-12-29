# pTRPred
This provides methods for detecting early warning signal for the battery thermal runaway. 
Combined with robust multi-scale slope-based detection to identify emerging changes in time series.
Includes visualization tools for overlaying detection scores with original signals. 

A small utility library that provides:

- Rolling/expanding window index construction (`roll_windows`)
- Rolling SVD (eigendecomposition) of per-window covariance (`roll_svd`)
- ARIMAX fitting and batch residual extraction (`fit_arimax_vec`, `arimax_residuals_df`)
- Pipelines that combine ARIMAX residualization + rolling SVD (`arimax_then_roll_svd`)
- Signal builders and multi-scale slope-vote change detectors (`detect_asvotes`, `detect_realtime`)
- Simple plotting utilities (`plot_detection_overlay`)

## Install (editable, for development)

```bash
python -m pip install -U pip
python -m pip install -e ".[dev,arima,fast]"
```

If you do not need ARIMAX functionality, omit `arima`. If you do not need sparse/fast eigensolvers, omit `fast`.

## Run tests

```bash
pytest
```
