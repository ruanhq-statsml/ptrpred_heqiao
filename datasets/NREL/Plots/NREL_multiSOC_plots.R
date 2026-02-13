# NREL multi-SOC plots: same cell, different SOCs in one figure (2x2 or 2x3)
# Focus on the window where detected_value_rt first exceeds threshold 0.3
# Output: HeqiaoDraft_withPlots/NREL_cursor/

args <- commandArgs(trailingOnly = FALSE)
script_arg <- args[grepl("^--file=", args)]
if (length(script_arg) > 0) {
  script_dir <- dirname(normalizePath(sub("^--file=", "", script_arg)))
  base_dir <- dirname(script_dir)
  setwd(base_dir)
} else if (file.exists("HeqiaoDraft_withPlots/dataset_correspondence.xlsx")) {
  setwd("HeqiaoDraft_withPlots")
} else if (!file.exists("dataset_correspondence.xlsx")) {
  stop("Run from repo root or from HeqiaoDraft_withPlots so dataset_correspondence.xlsx and rt_detect files are found.")
}
if (!dir.exists("NREL_cursor")) dir.create("NREL_cursor")

library(ggplot2)
library(dplyr)
library(gridExtra)

plot_detection_overlay <- function(
  df,
  title = "Real-time Detection vs Signal",
  time_col = "time_ind",
  score_col = "detected_value_rt",
  signal_col = "signal",
  first_det_col = NULL,
  score_label = "Real-Time Detected Value",
  signal_label = "Temperature",
  x_label = "time indices(0.1 second)",
  threshold = NULL,
  scale_factor = NULL,
  score_color = "blue",
  signal_color = "black",
  score_color_h = "red",
  save_path = NULL,
  width = 9,
  height = 7.5,
  dpi = 300,
  right_clip = c(-0.2, 1),
  right_adaptive = TRUE,
  right_pad = 0.03,
  auto_legend = TRUE,
  base_size = 12
) {
  if (!time_col %in% names(df)) stop("time_col not found.")
  if (!score_col %in% names(df)) stop("score_col not found.")
  if (!signal_col %in% names(df)) stop("signal_col not found.")

  sc <- df[[score_col]]
  sg <- df[[signal_col]]
  tm <- df[[time_col]]

  rng_sg <- range(sg, na.rm = TRUE)
  sg_min <- rng_sg[1]; sg_max <- rng_sg[2]; sg_span <- sg_max - sg_min
  if (!is.finite(sg_span) || sg_span == 0) { sg_min <- 0; sg_max <- 1; sg_span <- 1 }
  if (!is.null(scale_factor) && is.finite(scale_factor) && scale_factor > 0) {
    sg_max <- sg_min + scale_factor; sg_span <- scale_factor
  }

  rng_sc <- range(sc, na.rm = TRUE)
  dmin <- rng_sc[1]; dmax <- rng_sc[2]
  if (!is.finite(dmin) || !is.finite(dmax) || dmin == dmax) { dmin <- -0.2; dmax <- 1 }
  if (!is.null(right_clip) && length(right_clip) == 2 && right_clip[1] < right_clip[2]) {
    if (right_adaptive) { dmin <- max(dmin, right_clip[1]); dmax <- min(dmax, right_clip[2]) }
    else { dmin <- right_clip[1]; dmax <- right_clip[2] }
  }
  dspan <- dmax - dmin
  if (!is.finite(dspan) || dspan == 0) dspan <- 1
  pad <- right_pad * dspan
  dmin <- dmin - pad; dmax <- dmax + pad; dspan <- dmax - dmin

  df$det_on_signal__ <- (sc - dmin) / dspan * sg_span + sg_min
  inv_to_detect <- function(y) (y - sg_min) / sg_span * dspan + dmin

  if (auto_legend) {
    mid_x <- mean(range(tm, na.rm = TRUE))
    mid_y <- mean(range(sg, na.rm = TRUE))
    q_tr <- sum(tm >= mid_x & sg >= mid_y, na.rm = TRUE)
    q_tl <- sum(tm < mid_x & sg >= mid_y, na.rm = TRUE)
    q_br <- sum(tm >= mid_x & sg < mid_y, na.rm = TRUE)
    q_bl <- sum(tm < mid_x & sg < mid_y, na.rm = TRUE)
    best_q <- names(which.min(c(tr = q_tr, tl = q_tl, br = q_br, bl = q_bl)))
    leg_pos <- switch(best_q, tr = c(0.97, 0.97), tl = c(0.03, 0.97), br = c(0.97, 0.03), bl = c(0.03, 0.03))
    leg_just <- switch(best_q, tr = c(1, 1), tl = c(0, 1), br = c(1, 0), bl = c(0, 0))
  } else { leg_pos <- "top"; leg_just <- NULL }

  p <- ggplot(df, aes(x = .data[[time_col]])) +
    geom_line(aes(y = .data[[signal_col]], color = "Temperature"), linewidth = 1, alpha = 0.85, na.rm = TRUE) +
    geom_line(aes(y = det_on_signal__, color = "Detection"), linewidth = 1, na.rm = TRUE) +
    scale_y_continuous(
      name = signal_label,
      limits = c(sg_min, sg_max),
      sec.axis = sec_axis(trans = ~ inv_to_detect(.), name = score_label, breaks = pretty(c(dmin, dmax), n = 5))
    ) +
    scale_color_manual(values = c(Detection = score_color, Temperature = signal_color)) +
    labs(x = x_label, title = title) +
    theme_minimal(base_size = base_size) +
    theme(
      panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
      plot.title = element_text(size = base_size + 2, face = "bold"),
      axis.title.y = element_text(color = signal_color), axis.title.y.right = element_text(color = score_color),
      legend.position = leg_pos, legend.justification = leg_just,
      legend.background = element_blank(), legend.key = element_blank(), legend.title = element_blank()
    )

  if (!is.null(threshold) && is.finite(threshold)) {
    thr_on_signal <- (threshold - dmin) / dspan * sg_span + sg_min
    p <- p + geom_hline(yintercept = thr_on_signal, linetype = "dashed", color = score_color_h, linewidth = 1)
  }
  if (!is.null(first_det_col) && first_det_col %in% names(df)) {
    uvals <- unique(df[[first_det_col]]); uvals <- uvals[is.finite(uvals)]
    if (length(uvals) > 0)
      p <- p + geom_vline(xintercept = uvals[1], linetype = "dotted", color = "steelblue", linewidth = 1)
  }
  if (!is.null(save_path)) ggsave(filename = save_path, plot = p, width = width, height = height, dpi = dpi)
  p
}

# ---- Discover rt_detect files and parse cell + SOC ----
rt_files <- list.files(
  path = ".",
  pattern = "\\.xlsx_reform_severity_level[0-9]+\\.csv_rt_detect_result_window100\\.csv$",
  full.names = FALSE
)
if (length(rt_files) == 0) stop("No rt_detect_result_window100.csv files found in current directory.")

# Parse: dataset_name, severity_level, cell, SOC
meta <- data.frame(
  file = rt_files,
  dataset_name = sub("\\.xlsx_reform.*", "", rt_files),
  stringsAsFactors = FALSE
)
meta$severity_level <- as.integer(sub(".*severity_level([0-9]+).*", "\\1", meta$file))

# SOC: support both S0C (e.g. 1500mAh1-100S0C) and SOC (e.g. OE-LFP10Ah-80SOC-cell13)
meta$SOC <- NA_integer_
idx_s0c <- grep("S0C", meta$dataset_name)
idx_soc <- grep("SOC", meta$dataset_name, ignore.case = TRUE)
if (length(idx_s0c)) meta$SOC[idx_s0c] <- as.integer(sub(".*-(\\d+)S0C$", "\\1", meta$dataset_name[idx_s0c]))
if (length(idx_soc)) meta$SOC[idx_soc] <- as.integer(sub(".*-(\\d+)SOC.*", "\\1", meta$dataset_name[idx_soc]))

# Cell: same physical cell across SOCs
meta$cell <- meta$dataset_name
if (length(idx_s0c)) meta$cell[idx_s0c] <- sub("-\\d+S0C$", "", meta$dataset_name[idx_s0c])
if (length(idx_soc)) meta$cell[idx_soc] <- sub("-\\d+SOC", "", meta$dataset_name[idx_soc])

# Only keep rows with valid SOC
meta <- meta[!is.na(meta$SOC), ]

# ---- Build list of cells that have multiple SOCs ----
cell_counts <- meta %>% group_by(cell) %>% summarise(n = n(), .groups = "drop")
cells_multi <- cell_counts$cell[cell_counts$n >= 2]
# Prefer cells with 4–6 SOCs for 2x2 or 2x3
cells_multi <- cells_multi[order(-cell_counts$n[match(cells_multi, cell_counts$cell)])]

# Window around first exceedance of 0.3
THRESHOLD <- 0.3
# Time range: from start (index 1) to detected index + 200
POINTS_AFTER_DETECTED <- 200

load_window <- function(dataset_name, severity_level) {
  fname <- paste0(dataset_name, ".xlsx_reform_severity_level", severity_level, ".csv_rt_detect_result_window100.csv")
  if (!file.exists(fname)) return(NULL)
  df <- read.csv(fname)
  if (!"detected_value_rt" %in% names(df) || !"temperature" %in% names(df)) return(NULL)
  idx <- which(df$detected_value_rt >= THRESHOLD)
  if (length(idx) == 0) return(NULL)
  indice <- min(idx)
  start_indice <- 1L
  end_indice <- min(nrow(df), indice + POINTS_AFTER_DETECTED)
  det_raw <- df[start_indice:end_indice, ]
  det_raw$time_ind <- seq_len(nrow(det_raw))
  det_raw$signal <- det_raw$temperature
  list(df = det_raw, temp_at_03 = df$temperature[indice], indice_global = indice)
}

# ---- Version 1: Overlay panels (Temperature + Detection, threshold 0.3) in 2x2 or 2x3 ----
for (cell_id in cells_multi) {
  sub_meta <- meta[meta$cell == cell_id, ] %>% arrange(desc(SOC))
  if (nrow(sub_meta) < 2) next

  plots_list <- list()
  for (j in seq_len(nrow(sub_meta))) {
    row <- sub_meta[j, ]
    res <- load_window(row$dataset_name, row$severity_level)
    if (is.null(res)) next
    title_j <- sprintf("%s — %d%% SOC\nTemp at first ≥0.3: %.1f °C", row$dataset_name, row$SOC, res$temp_at_03)
    pj <- plot_detection_overlay(
      res$df,
      title = title_j,
      score_label = "Detection",
      signal_label = "Temperature (°C)",
      x_label = "time indices(0.1 second)",
      threshold = THRESHOLD,
      score_color = "red",
      signal_color = "darkblue",
      score_color_h = "darkgreen",
      base_size = 10,
      auto_legend = TRUE
    )
    plots_list[[length(plots_list) + 1]] <- pj
  }
  if (length(plots_list) == 0) next

  n_plots <- length(plots_list)
  n_col <- if (n_plots <= 4) 2 else 3
  n_row <- ceiling(n_plots / n_col)
  out_file <- file.path("NREL_cursor", paste0(gsub("[^a-zA-Z0-9]", "_", cell_id), "_multiSOC_overlay.png"))
  p_combined <- do.call(gridExtra::arrangeGrob, c(plots_list, list(ncol = n_col, nrow = n_row)))
  png(out_file, width = 6 * n_col, height = 4.5 * n_row, units = "in", res = 300)
  grid::grid.draw(p_combined)
  dev.off()
  message("Saved: ", out_file)
}

# ---- Version 2: Detection-only panels (clearer focus on threshold crossing) ----
# Single y-axis: detected_value_rt; horizontal line at 0.3; vertical line at first exceedance.
for (cell_id in cells_multi) {
  sub_meta <- meta[meta$cell == cell_id, ] %>% arrange(desc(SOC))
  if (nrow(sub_meta) < 2) next

  plots_list <- list()
  for (j in seq_len(nrow(sub_meta))) {
    row <- sub_meta[j, ]
    res <- load_window(row$dataset_name, row$severity_level)
    if (is.null(res)) next
    df <- res$df
    # First time index in this window where detection >= 0.3 (relative to window)
    idx_local <- which(df$detected_value_rt >= THRESHOLD)
    first_t <- if (length(idx_local) > 0) df$time_ind[min(idx_local)] else NA_real_

    pj <- ggplot(df, aes(x = time_ind, y = detected_value_rt)) +
      geom_line(color = "steelblue", linewidth = 1.1, na.rm = TRUE) +
      geom_hline(yintercept = THRESHOLD, linetype = "dashed", color = "darkred", linewidth = 1)
    if (!is.na(first_t)) pj <- pj + geom_vline(xintercept = first_t, linetype = "dotted", color = "darkgreen", linewidth = 1)
    pj <- pj + labs(
      title = sprintf("%d%% SOC — Temp at ≥0.3: %.1f °C", row$SOC, res$temp_at_03),
      x = "time indices(0.1 second)", y = "Real-time detection value"
    ) + theme_minimal(base_size = 10) + theme(panel.grid.minor = element_blank())
    plots_list[[length(plots_list) + 1]] <- pj
  }
  if (length(plots_list) == 0) next

  n_plots <- length(plots_list)
  n_col <- if (n_plots <= 4) 2 else 3
  n_row <- ceiling(n_plots / n_col)
  out_file <- file.path("NREL_cursor", paste0(gsub("[^a-zA-Z0-9]", "_", cell_id), "_multiSOC_detection_only.png"))
  p_combined <- do.call(gridExtra::arrangeGrob, c(plots_list, list(ncol = n_col, nrow = n_row)))
  png(out_file, width = 5 * n_col, height = 3.5 * n_row, units = "in", res = 300)
  grid::grid.draw(p_combined)
  dev.off()
  message("Saved: ", out_file)
}

# ---- Version 3: One faceted plot (all SOCs in one ggplot, detection only) ----
# Single figure with facet_wrap(~ SOC_label) for direct comparison.
for (cell_id in cells_multi) {
  sub_meta <- meta[meta$cell == cell_id, ] %>% arrange(desc(SOC))
  if (nrow(sub_meta) < 2) next

  big_list <- list()
  for (j in seq_len(nrow(sub_meta))) {
    row <- sub_meta[j, ]
    res <- load_window(row$dataset_name, row$severity_level)
    if (is.null(res)) next
    res$df$SOC_label <- paste0(row$SOC, "% SOC")
    res$df$temp_at_03 <- res$temp_at_03
    big_list[[length(big_list) + 1]] <- res$df
  }
  if (length(big_list) == 0) next
  big <- bind_rows(big_list)
  if (nrow(big) == 0) next

  p_facet <- ggplot(big, aes(x = time_ind, y = detected_value_rt)) +
    geom_line(color = "steelblue", linewidth = 0.9, na.rm = TRUE) +
    geom_hline(yintercept = THRESHOLD, linetype = "dashed", color = "darkred", linewidth = 0.9) +
    facet_wrap(~ SOC_label, scales = "free_x", ncol = 2) +
    labs(
      title = paste0("Same cell: ", cell_id, " — Detection value around first exceedance of 0.3"),
      x = "time indices(0.1 second)", y = "Real-time detection value"
    ) +
    theme_minimal(base_size = 11) +
    theme(panel.grid.minor = element_blank(), strip.text = element_text(face = "bold"))
  out_file <- file.path("NREL_cursor", paste0(gsub("[^a-zA-Z0-9]", "_", cell_id), "_multiSOC_facet.png"))
  ggsave(out_file, plot = p_facet, width = 10, height = 2.5 * ceiling(length(unique(big$SOC_label)) / 2), dpi = 300)
  message("Saved: ", out_file)
}

# ========== SAME SOC, DIFFERENT CELLS (multi-cell at fixed SOC) ==========
soc_counts <- meta %>% group_by(SOC) %>% summarise(n = n(), .groups = "drop")
socs_multi <- soc_counts$SOC[soc_counts$n >= 2]
socs_multi <- sort(socs_multi, decreasing = TRUE)

for (soc_val in socs_multi) {
  sub_meta <- meta[meta$SOC == soc_val, ] %>% arrange(dataset_name)
  if (nrow(sub_meta) < 2) next

  # ---- Multi-cell overlay (same SOC) ----
  plots_list <- list()
  for (j in seq_len(nrow(sub_meta))) {
    row <- sub_meta[j, ]
    res <- load_window(row$dataset_name, row$severity_level)
    if (is.null(res)) next
    title_j <- sprintf("%s\nTemp at first ≥0.3: %.1f °C", row$dataset_name, res$temp_at_03)
    pj <- plot_detection_overlay(
      res$df,
      title = title_j,
      score_label = "Detection",
      signal_label = "Temperature (°C)",
      x_label = "time indices(0.1 second)",
      threshold = THRESHOLD,
      score_color = "red",
      signal_color = "darkblue",
      score_color_h = "darkgreen",
      base_size = 10,
      auto_legend = TRUE
    )
    plots_list[[length(plots_list) + 1]] <- pj
  }
  if (length(plots_list) == 0) next
  n_plots <- length(plots_list)
  n_col <- if (n_plots <= 4) 2 else 3
  n_row <- ceiling(n_plots / n_col)
  out_file <- file.path("NREL_cursor", paste0("SOC", soc_val, "_multiCell_overlay.png"))
  p_combined <- do.call(gridExtra::arrangeGrob, c(plots_list, list(ncol = n_col, nrow = n_row)))
  png(out_file, width = 6 * n_col, height = 4.5 * n_row, units = "in", res = 300)
  grid::grid.draw(p_combined)
  dev.off()
  message("Saved: ", out_file)

  # ---- Multi-cell detection-only (same SOC) ----
  plots_list <- list()
  for (j in seq_len(nrow(sub_meta))) {
    row <- sub_meta[j, ]
    res <- load_window(row$dataset_name, row$severity_level)
    if (is.null(res)) next
    df <- res$df
    idx_local <- which(df$detected_value_rt >= THRESHOLD)
    first_t <- if (length(idx_local) > 0) df$time_ind[min(idx_local)] else NA_real_
    pj <- ggplot(df, aes(x = time_ind, y = detected_value_rt)) +
      geom_line(color = "steelblue", linewidth = 1.1, na.rm = TRUE) +
      geom_hline(yintercept = THRESHOLD, linetype = "dashed", color = "darkred", linewidth = 1)
    if (!is.na(first_t)) pj <- pj + geom_vline(xintercept = first_t, linetype = "dotted", color = "darkgreen", linewidth = 1)
    pj <- pj + labs(
      title = sprintf("%s — Temp at ≥0.3: %.1f °C", row$dataset_name, res$temp_at_03),
      x = "time indices(0.1 second)", y = "Real-time detection value"
    ) + theme_minimal(base_size = 10) + theme(panel.grid.minor = element_blank())
    plots_list[[length(plots_list) + 1]] <- pj
  }
  if (length(plots_list) == 0) next
  n_plots <- length(plots_list)
  n_col <- if (n_plots <= 4) 2 else 3
  n_row <- ceiling(n_plots / n_col)
  out_file <- file.path("NREL_cursor", paste0("SOC", soc_val, "_multiCell_detection_only.png"))
  p_combined <- do.call(gridExtra::arrangeGrob, c(plots_list, list(ncol = n_col, nrow = n_row)))
  png(out_file, width = 5 * n_col, height = 3.5 * n_row, units = "in", res = 300)
  grid::grid.draw(p_combined)
  dev.off()
  message("Saved: ", out_file)

  # ---- Multi-cell facet (same SOC) ----
  big_list <- list()
  for (j in seq_len(nrow(sub_meta))) {
    row <- sub_meta[j, ]
    res <- load_window(row$dataset_name, row$severity_level)
    if (is.null(res)) next
    res$df$cell_label <- row$dataset_name
    big_list[[length(big_list) + 1]] <- res$df
  }
  if (length(big_list) == 0) next
  big <- bind_rows(big_list)
  if (nrow(big) == 0) next
  p_facet <- ggplot(big, aes(x = time_ind, y = detected_value_rt)) +
    geom_line(color = "steelblue", linewidth = 0.9, na.rm = TRUE) +
    geom_hline(yintercept = THRESHOLD, linetype = "dashed", color = "darkred", linewidth = 0.9) +
    facet_wrap(~ cell_label, scales = "free_x", ncol = 2) +
    labs(
      title = paste0("Same SOC (", soc_val, "%) — different cells. Detection value, start to detected+200."),
      x = "time indices(0.1 second)", y = "Real-time detection value"
    ) +
    theme_minimal(base_size = 11) +
    theme(panel.grid.minor = element_blank(), strip.text = element_text(face = "bold"))
  out_file <- file.path("NREL_cursor", paste0("SOC", soc_val, "_multiCell_facet.png"))
  ggsave(out_file, plot = p_facet, width = 10, height = 2.5 * ceiling(length(unique(big$cell_label)) / 2), dpi = 300)
  message("Saved: ", out_file)
}
#Try the LSTM/Transformer based method and see whether it can predict the thermal runaway earlier?
