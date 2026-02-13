#!/usr/bin/env python3
"""
Reproduce all plots in datasets/NREL/Plots using data from Battery_cells/.

Run from repo root or from datasets/NREL:
  python reproduce_nrel_plots.py [--t] [--svd] [--multi] [--severity] [--out-dir PLOTS_DIR]

Default: regenerate all plot types into Plots/ (plot_T_result, plot_svd_result,
plot_multi_cells, plot_across_severity_level).
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# -----------------------------------------------------------------------------
# Paths (relative to script or cwd)
# -----------------------------------------------------------------------------
SCRIPT_DIR = Path(__file__).resolve().parent
NREL_DIR = SCRIPT_DIR
BATTERY_CELLS = NREL_DIR / "Battery_cells"
T_RESULT_DIR = BATTERY_CELLS / "T_result"
SVD_RESULT_DIR = BATTERY_CELLS / "SVD_result"
DEFAULT_PLOTS_BASE = NREL_DIR / "Plots"

THRESHOLD = 0.3
POINTS_AFTER_DETECTED = 200
PANELS_PER_PAGE_SEVERITY = 4  # 2x2
MULTI_PANELS_PER_ROW = 2
XLABEL = "time indices(0.1 second)"


def _base_id_from_t_result_path(path: Path) -> str:
    """e.g. 1500mAh1-20S0C.xlsx_reform_severity_level2.csv_rt_detect... -> 1500mAh1_20S0C"""
    name = path.stem
    m = re.match(r"^(.+?)\.xlsx_reform_severity_level\d+\.csv_rt_detect_result_window100$", name)
    if m:
        return m.group(1).replace("-", "_")
    return name.replace("-", "_").replace(".", "_")


def _base_id_from_svd_path(path: Path) -> str:
    """e.g. 1500mAh1-100S0C_30_100_SVD_detects -> 1500mAh1_100S0C"""
    name = path.stem
    if name.endswith("_30_100_SVD_detects"):
        base = name[: -len("_30_100_SVD_detects")]
        return base.replace("-", "_")
    return name.replace("-", "_")


def _severity_level_from_t_result_path(path: Path) -> int | None:
    m = re.search(r"severity_level(\d+)", path.name)
    return int(m.group(1)) if m else None


def _dataset_name_from_t_result_path(path: Path) -> str | None:
    """e.g. 1500mAh1-20S0C.xlsx_reform_severity_level2.csv_rt_detect... -> 1500mAh1-20S0C"""
    name = path.stem
    m = re.match(r"^(.+?)\.xlsx_reform_severity_level\d+\.csv_rt_detect_result_window100$", name)
    return m.group(1) if m else None


def _parse_soc(dataset_name: str) -> int | None:
    # e.g. 1500mAh1-40S0C -> 40; OE-LFP10Ah-80SOC-cell3 -> 80
    m = re.search(r"(\d+)S0C", dataset_name)
    if m:
        return int(m.group(1))
    m = re.search(r"(\d+)SOC", dataset_name, re.I)
    if m:
        return int(m.group(1))
    return None


def _cell_id(dataset_name: str) -> str:
    """Same physical cell across SOCs: strip SOC part."""
    # 1500mAh1-40S0C -> 1500mAh1; OE-LFP10Ah-80SOC-cell3 -> OE-LFP10Ah-cell3
    s = re.sub(r"-\d+S0C$", "", dataset_name)
    s = re.sub(r"-\d+SOC.*", "", s, flags=re.I)
    return s


def _safe_cell_id(cell_id: str) -> str:
    """For filenames: alphanumeric and underscores only."""
    return re.sub(r"[^a-zA-Z0-9]+", "_", cell_id).strip("_")


# -----------------------------------------------------------------------------
# Single-panel overlay (dual y-axis: left = signal, right = detection)
# -----------------------------------------------------------------------------
def _plot_overlay(
    df: pd.DataFrame,
    *,
    time_col: str = "time_ind",
    score_col: str = "detected_value_rt",
    signal_col: str = "signal",
    signal_label: str = "Temperature (°C)",
    score_label: str = "Detection",
    title: str = "",
    threshold: float = THRESHOLD,
    first_ind: int | None = None,
    first_signal_val: float | None = None,
    score_color: str = "red",
    signal_color: str = "darkblue",
    threshold_color: str = "darkgreen",
    figsize: tuple[float, float] = (9, 6),
    dpi: int = 300,
) -> plt.Figure:
    x = df[time_col].to_numpy(dtype=float)
    sc = pd.to_numeric(df[score_col], errors="coerce").to_numpy()
    sg = pd.to_numeric(df[signal_col], errors="coerce").to_numpy()

    fig, ax1 = plt.subplots(figsize=figsize, dpi=dpi)
    ax1.plot(x, sg, color=signal_color, linewidth=1, alpha=0.85, label=signal_label)
    ax1.set_ylabel(signal_label, color=signal_color)
    ax1.tick_params(axis="y", labelcolor=signal_color)
    ax1.set_xlabel(XLABEL)

    ax2 = ax1.twinx()
    ax2.plot(x, sc, color=score_color, linewidth=1, label=score_label)
    ax2.set_ylabel(score_label, color=score_color)
    ax2.tick_params(axis="y", labelcolor=score_color)
    ax2.set_ylim(-0.2, 1.0)

    if threshold is not None and np.isfinite(threshold):
        ax2.axhline(y=float(threshold), linestyle="--", color=threshold_color, linewidth=1)
    if first_ind is not None:
        ax1.axvline(x=first_ind, linestyle=":", color=threshold_color, linewidth=1)

    ax1.set_title(title)
    fig.legend(loc="upper right", bbox_to_anchor=(0.88, 0.88))
    plt.tight_layout()
    return fig


def _plot_detection_only(
    df: pd.DataFrame,
    *,
    time_col: str = "time_ind",
    score_col: str = "detected_value_rt",
    title: str = "",
    threshold: float = THRESHOLD,
    first_ind: int | None = None,
    figsize: tuple[float, float] = (9, 5),
    dpi: int = 300,
) -> plt.Figure:
    x = df[time_col].to_numpy(dtype=float)
    sc = pd.to_numeric(df[score_col], errors="coerce").to_numpy()

    fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
    ax.plot(x, sc, color="steelblue", linewidth=1.1)
    ax.axhline(y=threshold, linestyle="--", color="darkred", linewidth=1)
    if first_ind is not None:
        ax.axvline(x=first_ind, linestyle=":", color="darkgreen", linewidth=1)
    ax.set_xlabel(XLABEL)
    ax.set_ylabel("Real-time detection value")
    ax.set_title(title)
    ax.set_ylim(-0.2, 1.0)
    plt.tight_layout()
    return fig


def _first_exceedance_index(df: pd.DataFrame, score_col: str = "detected_value_rt", thresh: float = THRESHOLD) -> int | None:
    sc = pd.to_numeric(df[score_col], errors="coerce")
    idx = np.where(sc.to_numpy() >= thresh)[0]
    return int(idx[0]) if len(idx) else None


# -----------------------------------------------------------------------------
# T_result plots
# -----------------------------------------------------------------------------
def run_plot_t_result(out_base: Path) -> None:
    out_dir = out_base / "plot_T_result"
    out_dir.mkdir(parents=True, exist_ok=True)

    if not T_RESULT_DIR.exists():
        print("T_result dir not found, skip plot_T_result")
        return

    for path in sorted(T_RESULT_DIR.glob("*_rt_detect_result_window100.csv")):
        base_id = _base_id_from_t_result_path(path)
        df = pd.read_csv(path)
        # T_result CSV: first col may be empty or index; columns temperature, detected_value_rt
        if "time_ind" not in df.columns:
            df["time_ind"] = np.arange(1, len(df) + 1, dtype=float)
        if "signal" not in df.columns and "temperature" in df.columns:
            df["signal"] = df["temperature"]

        first_idx = _first_exceedance_index(df)
        first_signal = float(df["signal"].iloc[first_idx]) if first_idx is not None and first_idx < len(df) else None
        first_time = df["time_ind"].iloc[first_idx].item() if first_idx is not None else None
        dname = _dataset_name_from_t_result_path(path)
        soc = _parse_soc(dname) if dname else None
        display_name = (dname or base_id.replace("_", "-"))
        if first_signal is not None and first_time is not None:
            soc_str = f" {soc}% SOC |" if soc is not None else " "
            title = f"{display_name} |{soc_str} First ≥ 0.3 at T = {first_signal:.1f} °C (index {int(first_time)})"
        else:
            title = display_name

        # Overlay
        fig = _plot_overlay(
            df,
            signal_col="signal",
            signal_label="Temperature (°C)",
            title=title,
            first_ind=first_time,
            first_signal_val=first_signal,
        )
        fig.savefig(out_dir / f"{base_id}_overlay.png", dpi=300, bbox_inches="tight")
        plt.close(fig)

        # Detection only
        fig = _plot_detection_only(df, title=title, first_ind=first_time)
        fig.savefig(out_dir / f"{base_id}_detection.png", dpi=300, bbox_inches="tight")
        plt.close(fig)

    print(f"plot_T_result: wrote {len(list(out_dir.glob('*.png')))} PNGs to {out_dir}")


# -----------------------------------------------------------------------------
# SVD result plots
# -----------------------------------------------------------------------------
def run_plot_svd_result(out_base: Path) -> None:
    out_dir = out_base / "plot_svd_result"
    out_dir.mkdir(parents=True, exist_ok=True)

    if not SVD_RESULT_DIR.exists():
        print("SVD_result dir not found, skip plot_svd_result")
        return

    for path in sorted(SVD_RESULT_DIR.glob("*_30_100_SVD_detects.csv")):
        base_id = _base_id_from_svd_path(path)
        df = pd.read_csv(path)
        # SVD has time_ind, signal, detected_value_rt
        if "time_ind" not in df.columns and df.columns[0] != "time_ind":
            df["time_ind"] = np.arange(0, len(df), dtype=float)  # or from first col
        time_col = "time_ind" if "time_ind" in df.columns else df.columns[1]
        if time_col != "time_ind":
            df["time_ind"] = df[time_col]

        first_idx = _first_exceedance_index(df)
        first_time = df["time_ind"].iloc[first_idx].item() if first_idx is not None else None
        first_sig = float(df.loc[first_idx, "signal"]) if first_idx is not None and "signal" in df.columns else None

        if first_sig is not None and first_time is not None:
            title = f"{base_id.replace('_', '-')} SVD 30_100 | First ≥ 0.3 at σ₁ = {first_sig:.3f} (index {int(first_time)})"
        else:
            title = f"{base_id.replace('_', '-')} SVD 30_100"

        # Overlay (signal = first singular value)
        fig = _plot_overlay(
            df,
            signal_col="signal",
            signal_label="First singular value (σ₁)",
            title=title,
            first_ind=first_time,
            first_signal_val=first_sig,
        )
        fig.savefig(out_dir / f"{base_id}_SVD_overlay.png", dpi=300, bbox_inches="tight")
        plt.close(fig)

        fig = _plot_detection_only(df, title=title, first_ind=first_time)
        fig.savefig(out_dir / f"{base_id}_SVD_detection.png", dpi=300, bbox_inches="tight")
        plt.close(fig)

    print(f"plot_svd_result: wrote {len(list(out_dir.glob('*.png')))} PNGs to {out_dir}")


# -----------------------------------------------------------------------------
# Multi-cell / multi-SOC plots (window: start to first ≥0.3 + 200)
# -----------------------------------------------------------------------------
def _load_window_t_result(dataset_name: str, severity_level: int) -> pd.DataFrame | None:
    """Load T_result CSV and return window from 1 to first ≥0.3 + 200."""
    pattern = f"{dataset_name}.xlsx_reform_severity_level{severity_level}.csv_rt_detect_result_window100.csv"
    path = T_RESULT_DIR / pattern
    if not path.exists():
        return None
    df = pd.read_csv(path)
    df = df.rename(columns={df.columns[0]: "idx"})
    df["time_ind"] = np.arange(1, len(df) + 1, dtype=float)
    if "temperature" in df.columns:
        df["signal"] = df["temperature"]
    idx = _first_exceedance_index(df)
    if idx is None:
        return None
    end = min(len(df), idx + 1 + POINTS_AFTER_DETECTED)
    return df.iloc[:end].copy()


def run_plot_multi_cells(out_base: Path) -> None:
    out_dir = out_base / "plot_multi_cells"
    out_dir.mkdir(parents=True, exist_ok=True)

    if not T_RESULT_DIR.exists():
        print("T_result dir not found, skip plot_multi_cells")
        return

    # Build meta: file -> dataset_name, severity_level, SOC, cell
    meta_list = []
    for path in T_RESULT_DIR.glob("*_rt_detect_result_window100.csv"):
        dname = _dataset_name_from_t_result_path(path)
        sev = _severity_level_from_t_result_path(path)
        if dname is None or sev is None:
            continue
        soc = _parse_soc(dname)
        if soc is None:
            continue
        meta_list.append({"path": path, "dataset_name": dname, "severity_level": sev, "SOC": soc, "cell": _cell_id(dname)})

    meta = pd.DataFrame(meta_list)
    if meta.empty:
        print("No T_result meta, skip plot_multi_cells")
        return

    # Multi-SOC: same cell, multiple SOCs
    cell_counts = meta.groupby("cell").size()
    cells_multi = cell_counts[cell_counts >= 2].index.tolist()

    for cell_id in cells_multi:
        sub = meta[meta["cell"] == cell_id].sort_values("SOC", ascending=False)
        rows_data = []
        for _, row in sub.iterrows():
            df = _load_window_t_result(row["dataset_name"], row["severity_level"])
            if df is None:
                continue
            first_idx = _first_exceedance_index(df)
            first_time = df["time_ind"].iloc[first_idx].item() if first_idx is not None else None
            temp_at_03 = float(df["signal"].iloc[first_idx]) if first_idx is not None else None
            title_o = f"{row['dataset_name']} — {row['SOC']}% SOC\nTemp at first ≥0.3: {temp_at_03:.1f} °C" if temp_at_03 is not None else f"{row['dataset_name']} — {row['SOC']}% SOC"
            title_d = f"{row['SOC']}% SOC — Temp at ≥0.3: {temp_at_03:.1f} °C" if temp_at_03 is not None else f"{row['SOC']}% SOC"
            rows_data.append((df, title_o, title_d, first_time))

        if not rows_data:
            continue
        n_col = 2 if len(rows_data) <= 4 else 3
        n_row = int(np.ceil(len(rows_data) / n_col))
        safe = _safe_cell_id(cell_id)
        # Overlay grid
        fig_big, axes = plt.subplots(n_row, n_col, figsize=(6 * n_col, 4.5 * n_row), dpi=300)
        axes = np.atleast_2d(axes)
        for i, (df, title_o, _t_d, first_time) in enumerate(rows_data):
            r, c = i // n_col, i % n_col
            ax1 = axes[r, c]
            ax2 = ax1.twinx()
            ax1.plot(df["time_ind"], df["signal"], color="darkblue", linewidth=1, alpha=0.85)
            ax2.plot(df["time_ind"], df["detected_value_rt"], color="red", linewidth=1)
            ax2.axhline(y=THRESHOLD, linestyle="--", color="darkgreen", linewidth=1)
            if first_time is not None:
                ax1.axvline(x=first_time, linestyle=":", color="darkgreen", linewidth=1)
            ax1.set_title(title_o)
            ax2.set_ylim(-0.2, 1.0)
        for j in range(len(rows_data), axes.size):
            axes.flat[j].set_visible(False)
        plt.tight_layout()
        fig_big.savefig(out_dir / f"{safe}_multiSOC_overlay.png", dpi=300, bbox_inches="tight")
        plt.close(fig_big)

        # Detection-only grid
        fig_big, axes = plt.subplots(n_row, n_col, figsize=(5 * n_col, 3.5 * n_row), dpi=300)
        axes = np.atleast_2d(axes)
        for i, (df, _t_o, title_d, first_time) in enumerate(rows_data):
            r, c = i // n_col, i % n_col
            ax = axes[r, c]
            ax.plot(df["time_ind"], df["detected_value_rt"], color="steelblue", linewidth=1.1)
            ax.axhline(y=THRESHOLD, linestyle="--", color="darkred", linewidth=1)
            if first_time is not None:
                ax.axvline(x=first_time, linestyle=":", color="darkgreen", linewidth=1)
            ax.set_title(title_d)
            ax.set_ylim(-0.2, 1.0)
        for j in range(len(rows_data), axes.size):
            axes.flat[j].set_visible(False)
        plt.tight_layout()
        fig_big.savefig(out_dir / f"{safe}_multiSOC_detection_only.png", dpi=300, bbox_inches="tight")
        plt.close(fig_big)

    # Multi-cell: same SOC, multiple cells
    soc_counts = meta.groupby("SOC").size()
    socs_multi = soc_counts[soc_counts >= 2].index.tolist()
    for soc_val in sorted(socs_multi, reverse=True):
        sub = meta[meta["SOC"] == soc_val].sort_values("dataset_name")
        rows_data = []
        for _, row in sub.iterrows():
            df = _load_window_t_result(row["dataset_name"], row["severity_level"])
            if df is None:
                continue
            first_idx = _first_exceedance_index(df)
            first_time = df["time_ind"].iloc[first_idx].item() if first_idx is not None else None
            temp_at_03 = float(df["signal"].iloc[first_idx]) if first_idx is not None else None
            title_o = f"{row['dataset_name']}\nTemp at first ≥0.3: {temp_at_03:.1f} °C" if temp_at_03 is not None else row["dataset_name"]
            title_d = f"{row['dataset_name']} — Temp at ≥0.3: {temp_at_03:.1f} °C" if temp_at_03 is not None else row["dataset_name"]
            rows_data.append((df, title_o, title_d, first_time))

        if not rows_data:
            continue
        n_col = 2 if len(rows_data) <= 4 else 3
        n_row = int(np.ceil(len(rows_data) / n_col))
        # Overlay grid
        fig_big, axes = plt.subplots(n_row, n_col, figsize=(6 * n_col, 4.5 * n_row), dpi=300)
        axes = np.atleast_2d(axes)
        for i, (df, title_o, _t_d, first_time) in enumerate(rows_data):
            r, c = i // n_col, i % n_col
            ax1 = axes[r, c]
            ax2 = ax1.twinx()
            ax1.plot(df["time_ind"], df["signal"], color="darkblue", linewidth=1, alpha=0.85)
            ax2.plot(df["time_ind"], df["detected_value_rt"], color="red", linewidth=1)
            ax2.axhline(y=THRESHOLD, linestyle="--", color="darkgreen", linewidth=1)
            if first_time is not None:
                ax1.axvline(x=first_time, linestyle=":", color="darkgreen", linewidth=1)
            ax1.set_title(title_o)
            ax2.set_ylim(-0.2, 1.0)
        for j in range(len(rows_data), axes.size):
            axes.flat[j].set_visible(False)
        plt.tight_layout()
        fig_big.savefig(out_dir / f"SOC{soc_val}_multiCell_overlay.png", dpi=300, bbox_inches="tight")
        plt.close(fig_big)

        fig_big, axes = plt.subplots(n_row, n_col, figsize=(5 * n_col, 3.5 * n_row), dpi=300)
        axes = np.atleast_2d(axes)
        for i, (df, _t_o, title_d, first_time) in enumerate(rows_data):
            r, c = i // n_col, i % n_col
            ax = axes[r, c]
            ax.plot(df["time_ind"], df["detected_value_rt"], color="steelblue", linewidth=1.1)
            ax.axhline(y=THRESHOLD, linestyle="--", color="darkred", linewidth=1)
            if first_time is not None:
                ax.axvline(x=first_time, linestyle=":", color="darkgreen", linewidth=1)
            ax.set_title(title_d)
            ax.set_ylim(-0.2, 1.0)
        for j in range(len(rows_data), axes.size):
            axes.flat[j].set_visible(False)
        plt.tight_layout()
        fig_big.savefig(out_dir / f"SOC{soc_val}_multiCell_detection_only.png", dpi=300, bbox_inches="tight")
        plt.close(fig_big)

    print(f"plot_multi_cells: wrote to {out_dir}")


# -----------------------------------------------------------------------------
# Plot across severity level (paginated detection + overlay)
# -----------------------------------------------------------------------------
def run_plot_across_severity(out_base: Path) -> None:
    out_dir = out_base / "plot_across_severity_level"
    out_dir.mkdir(parents=True, exist_ok=True)

    if not T_RESULT_DIR.exists():
        print("T_result dir not found, skip plot_across_severity_level")
        return

    by_sev: dict[int, list[Path]] = {}
    for path in T_RESULT_DIR.glob("*_rt_detect_result_window100.csv"):
        sev = _severity_level_from_t_result_path(path)
        if sev is None:
            continue
        by_sev.setdefault(sev, []).append(path)

    for sev, paths in sorted(by_sev.items()):
        # Build dataframes with time_ind and signal
        dfs = []
        for path in sorted(paths):
            df = pd.read_csv(path)
            df = df.rename(columns={df.columns[0]: "idx"})
            df["time_ind"] = np.arange(1, len(df) + 1, dtype=float)
            if "temperature" in df.columns:
                df["signal"] = df["temperature"]
            dname = _dataset_name_from_t_result_path(path)
            soc = _parse_soc(dname) if dname else None
            first_idx = _first_exceedance_index(df)
            temp_at_03 = float(df["signal"].iloc[first_idx]) if first_idx is not None and first_idx < len(df) else None
            df["_title"] = f"{dname or path.stem} {soc or '?'}% SOC T@≥0.3: {temp_at_03:.1f}°C" if temp_at_03 is not None else (dname or path.stem)
            df["_first_ind"] = df["time_ind"].iloc[first_idx].item() if first_idx is not None else None
            dfs.append(df)

        n_per_page = PANELS_PER_PAGE_SEVERITY
        for page_start in range(0, len(dfs), n_per_page):
            page_dfs = dfs[page_start : page_start + n_per_page]
            page_num = page_start // n_per_page + 1

            # Detection page
            n_col = 2
            n_row = 2
            fig, axes = plt.subplots(n_row, n_col, figsize=(10, 8), dpi=300)
            axes = axes.flatten()
            for i, df in enumerate(page_dfs):
                ax = axes[i]
                ax.plot(df["time_ind"], df["detected_value_rt"], color="steelblue", linewidth=1)
                ax.axhline(y=THRESHOLD, linestyle="--", color="darkred", linewidth=1)
                if df["_first_ind"].iloc[0] is not None:
                    ax.axvline(x=df["_first_ind"].iloc[0], linestyle=":", color="darkgreen", linewidth=1)
                ax.set_title(df["_title"].iloc[0])
                ax.set_xlabel(XLABEL)
                ax.set_ylabel("Detection")
                ax.set_ylim(-0.2, 0.6)
            for j in range(len(page_dfs), len(axes)):
                axes[j].set_visible(False)
            plt.tight_layout()
            fig.savefig(out_dir / f"severity_level_{sev}_detection_page{page_num}.png", dpi=300, bbox_inches="tight")
            plt.close(fig)

            # Overlay page (same layout)
            fig, axes = plt.subplots(n_row, n_col, figsize=(10, 8), dpi=300)
            axes = axes.flatten()
            for i, df in enumerate(page_dfs):
                ax = axes[i]
                ax2 = ax.twinx()
                ax.plot(df["time_ind"], df["signal"], color="darkblue", linewidth=1, alpha=0.85)
                ax2.plot(df["time_ind"], df["detected_value_rt"], color="red", linewidth=1)
                ax2.axhline(y=THRESHOLD, linestyle="--", color="darkgreen", linewidth=1)
                if df["_first_ind"].iloc[0] is not None:
                    ax.axvline(x=df["_first_ind"].iloc[0], linestyle=":", color="darkgreen", linewidth=1)
                ax.set_title(df["_title"].iloc[0])
                ax.set_xlabel(XLABEL)
                ax.set_ylabel("Temperature (°C)")
                ax2.set_ylabel("Detection")
                ax2.set_ylim(-0.2, 1.0)
            for j in range(len(page_dfs), len(axes)):
                axes[j].set_visible(False)
            plt.tight_layout()
            fig.savefig(out_dir / f"severity_level_{sev}_overlay_page{page_num}.png", dpi=300, bbox_inches="tight")
            plt.close(fig)

    print(f"plot_across_severity_level: wrote to {out_dir}")


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------
def main() -> None:
    ap = argparse.ArgumentParser(description="Reproduce NREL Plots")
    ap.add_argument("--t", action="store_true", help="Only plot_T_result")
    ap.add_argument("--svd", action="store_true", help="Only plot_svd_result")
    ap.add_argument("--multi", action="store_true", help="Only plot_multi_cells")
    ap.add_argument("--severity", action="store_true", help="Only plot_across_severity_level")
    ap.add_argument("--out-dir", type=Path, default=DEFAULT_PLOTS_BASE, help="Base dir for Plots (default: NREL/Plots)")
    args = ap.parse_args()

    out_base = args.out_dir.resolve()
    if not args.t and not args.svd and not args.multi and not args.severity:
        args.t = args.svd = args.multi = args.severity = True

    if args.t:
        run_plot_t_result(out_base)
    if args.svd:
        run_plot_svd_result(out_base)
    if args.multi:
        run_plot_multi_cells(out_base)
    if args.severity:
        run_plot_across_severity(out_base)


if __name__ == "__main__":
    main()
