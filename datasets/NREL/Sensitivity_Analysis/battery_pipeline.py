from __future__ import annotations

import re
import argparse
from pathlib import Path
from typing import Iterable, Optional, Tuple, Dict

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# -----------------------------
# Utils
# -----------------------------
def _drop_junk_cols(df: pd.DataFrame) -> pd.DataFrame:
    """Drop typical index/junk columns created by CSV exports."""
    junk = [c for c in df.columns if c in {"X", "X.x", "X.y"} or c.startswith("Unnamed:")]
    return df.drop(columns=junk, errors="ignore")

def _infer_dataset_col(df: pd.DataFrame) -> str:
    for c in ["dataset", "dataset_name", "Dataset", "name"]:
        if c in df.columns:
            return c
    raise ValueError(f"Cannot find dataset column in detection file. Columns={list(df.columns)}")

def _infer_value_col(df: pd.DataFrame, dataset_col: str) -> str:
    """Pick the single numeric column (excluding dataset col)."""
    candidates = [c for c in df.columns if c != dataset_col]
    # prefer numeric columns
    numeric = [c for c in candidates if pd.api.types.is_numeric_dtype(df[c])]
    if len(numeric) == 1:
        return numeric[0]
    if len(numeric) > 1:
        # if multiple numeric columns exist, choose the one with highest non-null rate
        nn = {c: df[c].notna().mean() for c in numeric}
        return max(nn, key=nn.get)
    raise ValueError(f"Cannot infer a numeric value column. Columns={list(df.columns)}")


def _parse_start_max_from_filename(path: Path) -> Optional[Tuple[int, int]]:
    """
    Parse names like:
      10_60_detected_result_whole.csv
      10_60_detected_result_wholeSVD.csv
    """
    m = re.search(r"(\d+)_(\d+)_detected_result_whole(?:SVD)?\.csv$", path.name)
    if not m:
        return None
    return int(m.group(1)), int(m.group(2))

# -----------------------------
# Loading + merging
# -----------------------------
def load_base_results(
    base_csv: str,
    n_rows: Optional[int] = 118,
    dataset_key: str = "dataset_name",
) -> pd.DataFrame:
    df = pd.read_csv(base_csv)
    df = _drop_junk_cols(df)
    if n_rows is not None:
        df = df.iloc[:n_rows].copy()

    # harmonize label column name
    if "Label" in df.columns and "label" not in df.columns:
        df = df.rename(columns={"Label": "label"})

    # ensure dataset key exists
    if dataset_key not in df.columns:
        # fallback: sometimes user uses "dataset"
        if "dataset" in df.columns:
            df = df.rename(columns={"dataset": dataset_key})
        else:
            raise ValueError(f"Base file must contain '{dataset_key}' column.")
    return df

def load_detection_file(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    df = _drop_junk_cols(df)
    dataset_col = _infer_dataset_col(df)
    value_col = _infer_value_col(df, dataset_col)
    parsed = _parse_start_max_from_filename(path)
    if parsed is None:
        # fallback: keep the original value_col name
        out_col = value_col
    else:
        start_w, max_w = parsed
        out_col = f"X{start_w}_{max_w}"
    out = df[[dataset_col, value_col]].rename(columns={dataset_col: "dataset_name", value_col: out_col})
    return out

def merge_detection_results(base: pd.DataFrame, det_paths: Iterable[Path]) -> pd.DataFrame:
    out = base.copy()
    for p in det_paths:
        det = load_detection_file(p)
        out = out.merge(det, on="dataset_name", how="left")
    return out

# -----------------------------
# Classification + summaries
# -----------------------------
def add_predictions(
    df: pd.DataFrame,
    score_col: str,
    threshold: float = 0.3,
    label_col: str = "label",
) -> pd.DataFrame:
    """
    Adds:
      label_<score_col> : predicted (0/1) using threshold
      conclusion_<score_col> : TP/TN/FP/FN/UNK
    """
    if label_col not in df.columns:
        raise ValueError(f"Missing ground-truth column '{label_col}' in base df.")

    pred_col = f"label_{score_col}"
    conc_col = f"conclusion_{score_col}"

    out = df.copy()
    out[pred_col] = np.where(out[score_col] >= threshold, 1, 0)

    y = out[label_col].values
    yhat = out[pred_col].values

    conclusion = np.full(len(out), "UNK", dtype=object)
    known = (y != 2) & ~pd.isna(y)

    conclusion[known & (y == 1) & (yhat == 1)] = "TP"
    conclusion[known & (y == 0) & (yhat == 0)] = "TN"
    conclusion[known & (y == 1) & (yhat == 0)] = "FN"
    conclusion[known & (y == 0) & (yhat == 1)] = "FP"

    out[conc_col] = conclusion
    return out


def summarize_by_battery(
    df: pd.DataFrame,
    conclusion_col: str,
    battery_col: str = "battery",
) -> pd.DataFrame:
    """
    Return TP/TN/FP/FN counts per battery, plus error rate (FP+FN)/known_total.
    """
    if battery_col not in df.columns:
        raise ValueError(f"Missing battery column '{battery_col}' in df.")

    g = df.groupby(battery_col, dropna=False)[conclusion_col]
    summary = pd.DataFrame({
        "count_TP": g.apply(lambda x: (x == "TP").sum()),
        "count_TN": g.apply(lambda x: (x == "TN").sum()),
        "count_FP": g.apply(lambda x: (x == "FP").sum()),
        "count_FN": g.apply(lambda x: (x == "FN").sum()),
        "count_UNK": g.apply(lambda x: (x == "UNK").sum()),
        "total": g.size(),
    }).reset_index()

    known_total = summary["total"] - summary["count_UNK"]
    summary["error_rate_known"] = np.where(
        known_total > 0,
        (summary["count_FP"] + summary["count_FN"]) / known_total,
        np.nan,
    )
    return summary


# -----------------------------
# Plots (threshold sensitivity)
# -----------------------------
def plot_threshold_sensitivity(
    df: pd.DataFrame,
    battery: str,
    start_window: int,
    out_png: Path,
    y_threshold: float = 0.3,
    battery_col: str = "battery",
    label_col: str = "label",
    jitter: float = 0.9,
) -> None:
    """
    Reproduces your jitter plots:
      x = maximal window size (60, 75, 100, 125, 150)
      y = detected score (X{start}_{max})
      color = label (Negative/Positive/Unknown)
    """
    sub = df[df[battery_col] == battery].copy()
    if sub.empty:
        return

    # collect all columns that match X{start_window}_*
    patt = re.compile(rf"^X{start_window}_(\d+)$")
    cols = [c for c in sub.columns if patt.match(c)]
    if not cols:
        return
    long = sub.melt(
        id_vars=[label_col],
        value_vars=cols,
        var_name="setting",
        value_name="value",
    )
    long["threshold"] = long["setting"].str.extract(r"_(\d+)$").astype(int)
    # map labels
    def _map_lab(x):
        if x == 1:
            return "Positive"
        if x == 2:
            return "Unknown"
        return "Negative"

    long["label_name"] = long[label_col].map(_map_lab)

    # jitter x
    rng = np.random.default_rng(123)
    x = long["threshold"].astype(float).values
    x = x + rng.normal(0, jitter, size=len(x)) * 0.15

    # plot
    plt.figure(figsize=(6, 7.5))
    for name in ["Negative", "Positive", "Unknown"]:
        d = long[long["label_name"] == name]
        if d.empty:
            continue
        # re-create jitter only for that subset
        idx = d.index.to_numpy()
        plt.scatter(x[np.isin(long.index, idx)], d["value"].values, label=name, s=30)

    plt.axhline(y=y_threshold, linewidth=2)
    plt.xticks(sorted(long["threshold"].unique()), rotation=90)
    plt.xlabel("Maximal Window Size")
    plt.ylabel("Maximal Detected Value")
    plt.title(f"Maximal Detected Value vs. Threshold\n- Lower Window Size {start_window} ({battery})")
    plt.legend(loc="lower center", bbox_to_anchor=(0.5, -0.18), ncol=3, frameon=False)
    plt.tight_layout()

    out_png.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_png, dpi=160)
    plt.close()


# -----------------------------
# End-to-end runner
# -----------------------------
def run_pipeline(
    base_csv: str,
    det_dir: str,
    det_glob: str = "*_detected_result_whole*.csv",
    threshold: float = 0.3,
    n_rows: Optional[int] = 118,
    out_merged_csv: Optional[str] = "battery_cell_stats_merged.csv",
    out_summary_dir: Optional[str] = "summaries",
    out_plots_dir: Optional[str] = "plots",
) -> None:
    base = load_base_results(base_csv, n_rows=n_rows)

    det_paths = sorted(Path(det_dir).glob(det_glob))
    if not det_paths:
        raise FileNotFoundError(f"No detection files found: dir={det_dir}, glob={det_glob}")

    merged = merge_detection_results(base, det_paths)

    # Save merged table (like your battery_cell_SVD_whole_stats.csv)
    if out_merged_csv:
        merged.to_csv(out_merged_csv, index=False)

    # For each detection score column X{start}_{max}, create predictions + summary
    score_cols = [c for c in merged.columns if re.match(r"^X\d+_\d+$", str(c))]
    Path(out_summary_dir).mkdir(parents=True, exist_ok=True)

    for c in score_cols:
        merged_pred = add_predictions(merged, score_col=c, threshold=threshold)
        s = summarize_by_battery(merged_pred, conclusion_col=f"conclusion_{c}")
        s.to_csv(Path(out_summary_dir) / f"summary_{c}.csv", index=False)

    # Make plots for each battery and each start window
    if out_plots_dir:
        starts = sorted({int(c.split("_")[0].replace("X", "")) for c in score_cols})
        batteries = sorted(merged["battery"].dropna().unique())

        for b in batteries:
            for sw in starts:
                out_png = Path(out_plots_dir) / f"thresholding_sensitivity_windowlower_{sw}_{b}.png"
                plot_threshold_sensitivity(
                    merged, battery=b, start_window=sw, out_png=out_png, y_threshold=threshold
                )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--base_csv", type=str, default="battery_class_results.csv")
    parser.add_argument("--det_dir", type=str, default=".")
    parser.add_argument("--det_glob", type=str, default="*_detected_result_whole*.csv")
    parser.add_argument("--threshold", type=float, default=0.3)
    parser.add_argument("--n_rows", type=int, default=118)
    parser.add_argument("--out_merged_csv", type=str, default="battery_cell_stats_merged.csv")
    parser.add_argument("--out_summary_dir", type=str, default="summaries")
    parser.add_argument("--out_plots_dir", type=str, default="plots")
    args = parser.parse_args()

    run_pipeline(
        base_csv=args.base_csv,
        det_dir=args.det_dir,
        det_glob=args.det_glob,
        threshold=args.threshold,
        n_rows=args.n_rows,
        out_merged_csv=args.out_merged_csv,
        out_summary_dir=args.out_summary_dir,
        out_plots_dir=args.out_plots_dir,
    )


if __name__ == "__main__":
    main()


#On SVD:
#python battery_pipeline.py \
#  --base_csv battery_class_results.csv \
#  --det_dir . \
#  --det_glob "*_detected_result_wholeSVD.csv" \
#  --threshold 0.3

#On None-SVD
#python battery_pipeline.py \
#  --base_csv battery_class_results.csv \
#  --det_dir . \
#  --det_glob "*_detected_result_whole.csv" \
#  --threshold 0.3



