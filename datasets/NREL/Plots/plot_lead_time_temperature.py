#!/usr/bin/env python3
"""Plot lead time histogram for NREL dataset."""

import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# ---- Data paths ----
parser = argparse.ArgumentParser(description="Plot lead time histogram")
parser.add_argument("csv", nargs="?", help="Path to CSV with 'second_buy' column")
args = parser.parse_args()

script_dir = Path(__file__).resolve().parent
base_dir = script_dir.parent

if args.csv:
    candidates = [Path(args.csv)]
else:
    candidates = [
        base_dir / "dataset_description2.csv",
        base_dir / "dataset_description_with_time3.csv",
        base_dir / "Sensitivity_Analysis" / "battery_class_results.csv",
        base_dir / "Sensitivity_Analysis" / "battery_cell_SVD_whole_stats.csv",
        script_dir / "dataset_description2.csv",
        Path("dataset_description2.csv"),
        Path("dataset_description_with_time3.csv"),
    ]

df = None
for p in candidates:
    if p.exists():
        df = pd.read_csv(p)
        break

if df is None or "second_buy" not in df.columns:
    raise FileNotFoundError(
        "dataset_description2.csv (or dataset_description_with_time3.csv) with column 'second_buy' not found. "
        "Run from project root or ensure the file exists."
    )

# Filter: 0 <= lead_time <= 100 (exclude > 100)
lead_time = pd.to_numeric(df["second_buy"], errors="coerce").dropna()
lead_time = lead_time[(lead_time >= 0) & (lead_time <= 100)]

n_cells = len(lead_time)
mean_s = lead_time.mean()
median_s = lead_time.median()

# ---- Plot ----
fig, ax = plt.subplots(figsize=(10, 6), facecolor="white")
ax.set_facecolor("white")

# Histogram: bins every 10 seconds (0–100)
bins = np.arange(0, 101, 10)
n, _, patches = ax.hist(
    lead_time,
    bins=bins,
    color="steelblue",
    edgecolor="white",
    linewidth=0.5,
    alpha=1.0,
)

# Mean line (dashed red)
ax.axvline(mean_s, color="red", linestyle="--", linewidth=2, label=f"Mean = {mean_s:.1f}s")

# Labels and title (slightly smaller font sizes)
ax.set_xlabel("Seconds before T = 50°C (lead time)", fontsize=10)
ax.set_ylabel("Number of cells", fontsize=10)
ax.set_title("Distribution of Lead-Time for NREL Dataset", fontsize=11)
ax.set_xlim(0, 100)
ax.legend(loc="upper right", fontsize=9)
ax.tick_params(axis="both", labelsize=9)

plt.tight_layout()

out_path = base_dir / "lead_time_Temperature.png"
fig.savefig(out_path, dpi=150, bbox_inches="tight", facecolor="white")
plt.close()
print(f"Saved: {out_path}")
