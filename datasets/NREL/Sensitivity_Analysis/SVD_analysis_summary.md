# SVD-Based Procedure: Results Summary

This document summarizes the results for the **SVD-based procedure** using detection outputs from files ending in `wholeSVD.csv` (e.g. `10_60_detected_result_wholeSVD.csv`, …). The same analyses as the non-SVD pipeline are replicated for SVD.

------------------------------------------------------------------------

## 1. Data and Setup

-   **Input**: `battery_class_results.csv` (ground truth) merged with 15 SVD result CSVs:
    -   Window 10: `10_60`, `10_75`, `10_100`, `10_125`, `10_150`
    -   Window 30: `30_60`, `30_75`, `30_100`, `30_125`, `30_150`
    -   Window 40: `40_60`, `40_75`, `40_100`, `40_125`, `40_150`
-   **Threshold**: 0.3 (same as non-SVD).
-   **Battery categorization**: Same as main analysis (Commercial LFP/NMC/LCO, Soteria, Soteria (Control), Lab/Custom, Lab/Generic).

------------------------------------------------------------------------

## 2. Output Files

| File | Description |
|----|----|
| `battery_cell_SVD_whole_stats.csv` | Merged SVD stats per dataset (all window/threshold columns). |
| `threshold_sensitivity_accuracy_summary_SVD.csv` | **Overall** accuracy per SVD algorithm (TP, TN, FP, FN, accuracy). |
| `threshold_sensitivity_accuracy_by_category_SVD.csv` | **By battery category** accuracy per SVD algorithm. |
| `thresholding_sensitivity_windowlower_{10,30,40}_{category}_SVD.png` | Threshold sensitivity plots by battery category for SVD. |

------------------------------------------------------------------------

## 3. SVD Accuracy Summary (Overall)

Accuracy = (TP + TN) / (TP + TN + FP + FN), n = 109 (excluding Label = 2).

| Algorithm (window_threshold) | TP  | TN  | FP  | FN  | Accuracy   |
|------------------------------|-----|-----|-----|-----|------------|
| conclusion_10_125            | 53  | 11  | 16  | 29  | **0.5872** |
| conclusion_10_60             | 74  | 4   | 23  | 8   | **0.7156** |
| conclusion_10_75             | 74  | 5   | 22  | 8   | **0.7248** |
| conclusion_10_150            | 46  | 15  | 12  | 36  | **0.5596** |
| conclusion_40_60             | 77  | 1   | 26  | 5   | **0.7156** |
| conclusion_40_75             | 75  | 0   | 27  | 7   | **0.6881** |
| conclusion_40_100            | 71  | 5   | 22  | 11  | **0.6972** |
| conclusion_40_125            | 69  | 6   | 21  | 13  | **0.6881** |
| conclusion_40_150            | 58  | 10  | 17  | 24  | **0.6239** |
| conclusion_30_75             | 75  | 1   | 26  | 7   | **0.6972** |
| conclusion_30_100            | 70  | 6   | 21  | 12  | **0.6972** |
| conclusion_30_125            | 65  | 8   | 19  | 17  | **0.6697** |
| conclusion_30_150            | 52  | 9   | 18  | 30  | **0.5596** |

**Best SVD config**: `conclusion_10_75` (accuracy **0.7248**).\
**Worst SVD config**: `conclusion_10_150` and `conclusion_30_150` (accuracy **0.5596**).

------------------------------------------------------------------------

## 4. SVD vs Non-SVD (Main Pipeline)

-   **Same best config**: 10_75 (0.7248) for both.
-   **SVD improves** at some configs (e.g. 40_150: 0.4587 → 0.6239; 10_125: 0.6055 → 0.5872 is slightly lower for SVD).
-   **SVD-specific** accuracy-by-category breakdown is in `threshold_sensitivity_accuracy_by_category_SVD.csv`.

------------------------------------------------------------------------

## 5. Plots (SVD)

-   **By battery category**: For each (window = 10, 30, 40) and each category (Commercial LCO/LFP/NMC, Lab/Custom, Lab/Generic, Soteria, Soteria (Control)), a plot is saved as\
    `thresholding_sensitivity_windowlower_{win}_{category}_SVD.png`\
    (e.g. `thresholding_sensitivity_windowlower_10_Commercial__LFP__SVD.png`).
-   **Chemistry-based SVD plots** (SO, NMC, LCO, Rec, LFP for windows 10/30/40) are still produced from `battery_cell_SVD_whole_stats.csv` as in the original script.

------------------------------------------------------------------------

## 6. How to Reproduce

From the `Sensitivity_Analysis` folder run:

``` bash
Rscript threshold_sensitivity.R
```

The SVD block runs only if `10_60_detected_result_wholeSVD.csv` exists. It then:

1.  Loads and merges all 15 `*wholeSVD.csv` files with `battery_class_results.csv`.
2.  Assigns conclusions (TP/TN/FP/FN) with threshold 0.3 and `safe_conclusion()`.
3.  Writes SVD accuracy summary and by-category CSVs.
4.  Builds and saves SVD threshold-sensitivity plots by battery category.
5.  Produces the original chemistry-based SVD plots.
