"""Evidence, evaluation, and translation plates for Figures 9--11."""

from __future__ import annotations

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Arc, Circle, Ellipse, Polygon, Rectangle

from figure_v3_common import (
    BLUE, CORAL, FIGURE_WIDTH_IN, GRAY, GRID, INK,
    NAVY, OFF_WHITE, PALE_BLUE, PALE_BLUE_2, PALE_CORAL, PALE_CORAL_2,
    PALE_GRAY, PANEL, WHITE, arrow, grid_crop, heading, image_box, label_box,
    link, mask_overlay, rounded_panel, save, schema,
)


def _title(fig, text: str) -> None:
    fig.suptitle(text, x=0.5, y=0.985, fontsize=11.2, weight="bold", color=INK)


def _lesion_polygon(cx: float, cy: float, sx: float, sy: float):
    return [
        (cx - sx, cy), (cx - 0.55 * sx, cy + 0.78 * sy),
        (cx + 0.25 * sx, cy + sy), (cx + sx, cy + 0.18 * sy),
        (cx + 0.58 * sx, cy - 0.78 * sy), (cx - 0.28 * sx, cy - sy),
    ]


def build_fig09() -> None:
    """Map lesion-error phenotypes to loss emphasis and evaluation bundles."""
    title = "Lesion-level errors require distinct objectives and metric bundles"
    fig, ax = plt.subplots(figsize=(FIGURE_WIDTH_IN, 6.25))
    schema(ax)
    _title(fig, title)
    ax.text(0.5, 0.935, "Reference contour  ·  Prediction contour", ha="center",
            fontsize=8.1, color=INK)
    ax.add_patch(Rectangle((0.405, 0.934), 0.030, 0.002, facecolor=BLUE, edgecolor="none"))
    ax.add_patch(Rectangle((0.555, 0.934), 0.030, 0.002, facecolor=CORAL, edgecolor="none"))

    base = grid_crop("longitudinal_flair_asset_sheet.png", 4, 1, 0, 0)
    specifications = [
        ("(a)", "Small-lesion miss", None,
         "Focal / Tversky emphasis", "Lesion sensitivity · lesion F1"),
        ("(b)", "False-positive lesion", _lesion_polygon(0.74, 0.36, 0.045, 0.055),
         "Specificity-aware overlap", "FP lesions per scan · PPV"),
        ("(c)", "Boundary displacement", _lesion_polygon(0.39, 0.58, 0.050, 0.055),
         "Boundary / surface\nemphasis", "HD95 · surface distance"),
        ("(d)", "Volume bias", _lesion_polygon(0.35, 0.58, 0.075, 0.085),
         "Overlap + volume control", "Volume error · Dice"),
    ]
    ref = _lesion_polygon(0.35, 0.58, 0.045, 0.055)
    for i, (panel, name, pred, loss, metrics) in enumerate(specifications):
        col, row = i % 2, i // 2
        x, y, w, h = 0.025 + col * 0.49, 0.505 - row * 0.415, 0.465, 0.365
        rounded_panel(ax, x, y, w, h, face=OFF_WHITE, edge=GRID, radius=0.014)
        heading(ax, panel, name, x=x + 0.012, y=y + h - 0.018)
        ix, iy, iw, ih = x + 0.020, y + 0.055, 0.190, 0.225
        image_box(ax, base, ix, iy, iw, ih, edge=GRID)
        if i == 0:
            mask_overlay(ax, ix, iy, iw, ih, reference=ref, prediction=None)
            ax.text(ix + 0.67 * iw, iy + 0.30 * ih, "missed", fontsize=7.5,
                    color=CORAL, weight="bold", ha="center")
            link(ax, (ix + 0.63 * iw, iy + 0.34 * ih),
                 (ix + 0.37 * iw, iy + 0.55 * ih), color=CORAL, style="-")
        else:
            mask_overlay(ax, ix, iy, iw, ih, reference=ref, prediction=pred)
        tx, tw = x + 0.235, w - 0.255
        ax.text(tx, y + 0.270, "LOSS EMPHASIS", fontsize=7.2,
                color=NAVY, weight="bold")
        label_box(ax, tx, y + 0.185, tw, 0.065, loss,
                  face=PALE_BLUE_2, edge=BLUE, fontsize=7.15)
        arrow(ax, (tx + tw / 2, y + 0.180), (tx + tw / 2, y + 0.151),
              color=GRAY, scale=7)
        ax.text(tx, y + 0.128, "METRIC BUNDLE", fontsize=7.2,
                color=CORAL, weight="bold")
        label_box(ax, tx, y + 0.045, tw, 0.065, metrics,
                  face=PALE_CORAL_2, edge=CORAL, fontsize=7.05)
    ax.text(0.5, 0.030,
            "Synthetic FLAIR anatomy; contours are schematic. No loss substitutes for lesion-level error analysis.",
            ha="center", fontsize=8.0, color=INK)
    save(fig, "fig09_error_loss_mapping", title,
         ["small-lesion miss", "false positive", "boundary shift", "volume bias"],
         raster=True, schematic_curves=False, assertions=[
             "Synthetic FLAIR crops carry separate reference and prediction contours.",
             "Each error phenotype maps to a compatible loss emphasis and complementary metric bundle.",
             "No empirical values, rankings, or simulated performance curves are shown.",
         ])


def _panel_header(ax, x, y, w, label, title):
    ax.text(x, y, label, fontsize=10.0, weight="bold", color=NAVY, va="top")
    ax.text(x + 0.047, y, title, fontsize=7.4, weight="bold", color=INK, va="top")
    ax.add_patch(Rectangle((x, y - 0.031), w, 0.0015, facecolor=GRID, edgecolor="none"))


def _brain_glyph(ax, x: float, y: float, s: float, color: str = BLUE) -> None:
    ax.add_patch(Ellipse((x, y), 0.72 * s, s, facecolor=WHITE,
                         edgecolor=color, lw=0.75, zorder=4))
    ax.add_patch(Arc((x - 0.09 * s, y), 0.18 * s, 0.35 * s,
                     theta1=250, theta2=105, color=color, lw=0.65, zorder=5))
    ax.add_patch(Arc((x + 0.09 * s, y), 0.18 * s, 0.35 * s,
                     theta1=75, theta2=290, color=color, lw=0.65, zorder=5))
    ax.add_patch(Circle((x + 0.18 * s, y + 0.12 * s), 0.045 * s,
                        facecolor=CORAL, edgecolor="none", zorder=6))


def _person_glyph(ax, x: float, y: float, s: float, color: str = NAVY) -> None:
    ax.add_patch(Circle((x, y + 0.25 * s), 0.12 * s, facecolor=WHITE,
                        edgecolor=color, lw=0.8, zorder=4))
    ax.add_patch(Polygon([(x - 0.20 * s, y - 0.25 * s),
                          (x + 0.20 * s, y - 0.25 * s),
                          (x + 0.13 * s, y + 0.10 * s),
                          (x - 0.13 * s, y + 0.10 * s)],
                         closed=True, facecolor=WHITE, edgecolor=color,
                         lw=0.8, zorder=4))


def _lock_glyph(ax, x: float, y: float, s: float, color: str = NAVY) -> None:
    ax.add_patch(Arc((x, y + 0.16 * s), 0.48 * s, 0.52 * s,
                     theta1=0, theta2=180, color=color, lw=1.0, zorder=4))
    ax.add_patch(Rectangle((x - 0.30 * s, y - 0.28 * s), 0.60 * s, 0.43 * s,
                           facecolor=PALE_GRAY, edgecolor=color, lw=0.8, zorder=4))
    ax.add_patch(Circle((x, y - 0.07 * s), 0.045 * s,
                        facecolor=color, edgecolor="none", zorder=5))


def _monitor_glyph(ax, x: float, y: float, s: float, color: str = NAVY) -> None:
    ax.add_patch(Rectangle((x - 0.42 * s, y - 0.22 * s), 0.84 * s, 0.55 * s,
                           facecolor=WHITE, edgecolor=color, lw=0.8, zorder=4))
    ax.add_patch(Ellipse((x, y + 0.03 * s), 0.48 * s, 0.32 * s,
                         facecolor=PALE_BLUE, edgecolor=BLUE, lw=0.65, zorder=5))
    ax.plot([x - 0.18 * s, x + 0.18 * s], [y - 0.34 * s] * 2,
            color=color, lw=0.8, zorder=4)
    ax.plot([x, x], [y - 0.22 * s, y - 0.34 * s], color=color, lw=0.8, zorder=4)


def build_fig10() -> None:
    """Technical evaluation logic without empirical or schematic curves."""
    title = "Evaluation logic from leakage control to governed clinical use"
    fig, ax = plt.subplots(figsize=(FIGURE_WIDTH_IN, 6.30))
    schema(ax)
    _title(fig, title)

    panels = [
        (0.025, 0.555, 0.455, 0.355, "(a)", "Leakage-resistant design"),
        (0.520, 0.555, 0.455, 0.355, "(b)", "Segmentation operators"),
        (0.025, 0.105, 0.300, 0.395, "(c)", "Diagnostic / prognostic claims"),
        (0.350, 0.105, 0.300, 0.395, "(d)", "Aggregation / uncertainty"),
        (0.675, 0.105, 0.300, 0.395, "(e)", "Clinical evidence / governance"),
    ]
    for x, y, w, h, lab, name in panels:
        rounded_panel(ax, x, y, w, h, face=OFF_WHITE, edge=GRID, radius=0.015)
        _panel_header(ax, x + 0.014, y + h - 0.016, w - 0.028, lab, name)

    # (a) Patient grouping and one-way locked external testing.
    x, y, w, h, *_ = panels[0]
    ax.text(x + 0.040, y + 0.282, "Development patients",
            fontsize=6.3, color=NAVY, weight="bold")
    for row in range(3):
        yy = y + 0.235 - row * 0.052
        _person_glyph(ax, x + 0.050, yy, 0.035, NAVY)
        for visit in range(3):
            _brain_glyph(ax, x + 0.100 + visit * 0.050, yy, 0.034, BLUE)
        ax.plot([x + 0.079, x + 0.227], [yy - 0.026] * 2, color=BLUE, lw=0.65)
    ax.plot([x + 0.265, x + 0.265], [y + 0.105, y + 0.280],
            color=GRAY, lw=0.9, ls="--")
    _lock_glyph(ax, x + 0.265, y + 0.082, 0.060, NAVY)
    ax.text(x + 0.265, y + 0.030, "model + threshold lock", ha="center",
            fontsize=6.6, color=NAVY, weight="bold")
    ax.text(x + 0.310, y + 0.282, "Held-out site/time",
            fontsize=6.1, color=CORAL, weight="bold")
    _person_glyph(ax, x + 0.325, y + 0.215, 0.040, CORAL)
    _brain_glyph(ax, x + 0.375, y + 0.215, 0.045, CORAL)
    _brain_glyph(ax, x + 0.415, y + 0.215, 0.045, CORAL)
    ax.text(x + 0.370, y + 0.135, "one-shot external test\n+ protocol stress",
            ha="center", fontsize=6.7, color=INK)
    arrow(ax, (x + 0.292, y + 0.095), (x + 0.345, y + 0.135),
          color=NAVY, connection="arc3,rad=-0.18")

    # (b) Metric operators expose different segmentation failures.
    x, y, w, h, *_ = panels[1]
    cx = [x + 0.060, x + 0.165, x + 0.270, x + 0.375]
    for xx, symbol, label in zip(cx, ("∩", "•", "∂", "V"),
                                 ("Overlap\nDice", "Lesions\nSensitivity · FP", "Boundary\nHD95", "Burden\nVolume bias")):
        ax.add_patch(Circle((xx, y + 0.225), 0.034, facecolor=PALE_BLUE,
                            edgecolor=BLUE, lw=0.8))
        ax.text(xx, y + 0.225, symbol, ha="center", va="center",
                fontsize=10.0, weight="bold", color=NAVY)
        ax.text(xx, y + 0.145, label, ha="center", va="center", fontsize=7.2)
    label_box(ax, x + 0.070, y + 0.047, w - 0.140, 0.058,
              "Report a task-specific bundle—not a single score",
              face=PALE_CORAL_2, edge=CORAL, fontsize=7.7, weight="bold")

    # (c) Claims require distinct discrimination, calibration, and utility operators.
    x, y, w, h, *_ = panels[2]
    ax.text(x + 0.025, y + 0.310, "score + observed outcome + intended case spectrum",
            fontsize=6.2, color=INK)
    claim_nodes = [
        (x + 0.060, "D", "Discrimination", "Se/Sp · AUC"),
        (x + 0.150, "C", "Calibration", "intercept · Brier"),
        (x + 0.240, "U", "Utility", "net benefit"),
    ]
    for xx, symbol, name, metric in claim_nodes:
        ax.add_patch(Circle((xx, y + 0.245), 0.026, facecolor=PALE_BLUE,
                            edgecolor=BLUE, lw=0.8))
        ax.text(xx, y + 0.245, symbol, ha="center", va="center",
                fontsize=8.0, weight="bold", color=NAVY)
        ax.text(xx, y + 0.202, name, ha="center", va="center",
                fontsize=5.55, weight="bold")
        ax.text(xx, y + 0.178, metric, ha="center", va="center",
                fontsize=4.55)
    ax.text(x + 0.025, y + 0.125, "prognostic horizon and censoring", fontsize=6.4,
            color=NAVY, weight="bold")
    ax.plot([x + 0.040, x + 0.260], [y + 0.090] * 2, color=GRAY, lw=0.9)
    ax.add_patch(Circle((x + 0.055, y + 0.090), 0.0045, facecolor=CORAL, edgecolor=CORAL))
    ax.add_patch(Polygon([(x + 0.155, y + 0.097), (x + 0.162, y + 0.090),
                          (x + 0.155, y + 0.083), (x + 0.148, y + 0.090)],
                         closed=True, facecolor=WHITE, edgecolor=CORAL, lw=0.8))
    ax.plot([x + 0.250, x + 0.250], [y + 0.078, y + 0.102], color=CORAL, lw=0.9)
    for xx, text in [(x + 0.055, "index"), (x + 0.155, "horizon τ"),
                     (x + 0.250, "event / censor")]:
        ax.text(xx, y + 0.055, text, ha="center", fontsize=5.7)
    ax.text(x + w / 2, y + 0.020, "Discrimination ≠ calibration ≠ utility",
            ha="center", fontsize=6.3, color=CORAL, weight="bold")

    # (d) Respect the nested statistical unit and report uncertainty/failures.
    x, y, w, h, *_ = panels[3]
    center = (x + 0.090, y + 0.225)
    for radius, edge, text, ty in [
        (0.075, GRAY, "site", y + 0.325), (0.057, BLUE, "patient", y + 0.293),
        (0.039, NAVY, "exam", y + 0.261), (0.020, CORAL, "lesion", y + 0.229),
    ]:
        ax.add_patch(Circle(center, radius, facecolor="none", edgecolor=edge, lw=0.9))
        ax.text(x + 0.170, ty, text, fontsize=6.1, color=edge, weight="bold")
    shield = [(x + 0.220, y + 0.255), (x + 0.280, y + 0.255),
              (x + 0.272, y + 0.205), (x + 0.250, y + 0.175),
              (x + 0.228, y + 0.205)]
    ax.add_patch(Polygon(shield, closed=True, facecolor=PALE_CORAL_2,
                         edgecolor=CORAL, lw=0.9))
    ax.text(x + 0.250, y + 0.218, "CI", ha="center", va="center",
            fontsize=7.0, weight="bold", color=CORAL)
    ax.text(x + 0.250, y + 0.130, "strata · failures\nquality gate · abstention",
            ha="center", fontsize=5.9)
    ax.text(x + 0.150, y + 0.085, "resample and estimate at patient / site level",
            ha="center", fontsize=5.85, color=INK)
    ax.text(x + w / 2, y + 0.025, "Confidence ≠ correctness under shift",
            ha="center", fontsize=6.3, color=NAVY, weight="bold")

    # (e) Evidence ladder and bounded action.
    x, y, w, h, *_ = panels[4]
    stages = [
        ("L1", "Internal"), ("L2", "Same-site"), ("L3", "External"),
        ("L4", "Prospective"), ("L5", "Net benefit"),
    ]
    for j, (level, name) in enumerate(stages):
        yy = y + 0.290 - j * 0.049
        ax.add_patch(Circle((x + 0.055, yy), 0.018, facecolor=PALE_BLUE if j < 3 else PALE_CORAL,
                            edgecolor=BLUE if j < 3 else CORAL, lw=0.75))
        ax.text(x + 0.055, yy, level, ha="center", va="center", fontsize=6.8, weight="bold")
        ax.text(x + 0.086, yy, name, va="center", fontsize=6.1)
        if j < 4:
            arrow(ax, (x + 0.055, yy - 0.020), (x + 0.055, yy - 0.033), color=GRAY, scale=6)
    _person_glyph(ax, x + 0.205, y + 0.270, 0.060, NAVY)
    _monitor_glyph(ax, x + 0.248, y + 0.270, 0.070, NAVY)
    ax.text(x + 0.226, y + 0.218, "editable output\n+ human review",
            ha="center", fontsize=5.6)
    _lock_glyph(ax, x + 0.205, y + 0.145, 0.060, CORAL)
    ax.add_patch(Arc((x + 0.248, y + 0.145), 0.056, 0.056,
                     theta1=35, theta2=320, color=CORAL, lw=1.0))
    ax.text(x + 0.226, y + 0.075, "monitor · rollback\nrevalidate",
            ha="center", fontsize=5.5)
    ax.text(0.5, 0.035, "Metric adequacy  ≠  evidence strength  ≠  clinical utility",
            ha="center", fontsize=8.7, color=NAVY, weight="bold")
    save(fig, "fig10_evaluation_frameworks", title,
         ["leakage-resistant design", "segmentation operators",
          "diagnostic and prognostic claims", "aggregation and uncertainty",
          "clinical evaluation and governance"],
         raster=False, schematic_curves=False, assertions=[
             "The plate contains no axes, plot marks, curves, bars, or empirical values.",
             "Patient-level splitting precedes locked external and protocol-stress evaluation.",
             "Metric bundles are separated from evidence level and bounded clinical action.",
             "The evidence ladder runs from internal testing to patient net benefit.",
         ])


def _review_glyph(ax, x: float, y: float, s: float, color: str = NAVY) -> None:
    _monitor_glyph(ax, x, y, s, color)
    ax.plot([x + 0.20 * s, x + 0.45 * s], [y - 0.02 * s, y + 0.24 * s],
            color=CORAL, lw=1.1, zorder=7)


def _contours_glyph(ax, x: float, y: float, s: float) -> None:
    for dx, dy, color, ls in [(-0.05, 0.02, BLUE, "-"), (0.03, -0.02, CORAL, "--"),
                              (0.00, 0.04, GRAY, ":")]:
        ax.add_patch(Ellipse((x + dx * s, y + dy * s), 0.72 * s, 0.48 * s,
                             angle=12, facecolor="none", edgecolor=color,
                             lw=0.9, ls=ls, zorder=5))


def _modality_glyph(ax, x: float, y: float, s: float) -> None:
    for j in range(4):
        xx = x - 0.43 * s + j * 0.28 * s
        face = PALE_GRAY if j == 2 else PALE_BLUE
        edge = GRAY if j == 2 else BLUE
        ax.add_patch(Rectangle((xx, y - 0.32 * s), 0.20 * s, 0.64 * s,
                               facecolor=face, edgecolor=edge, lw=0.7))
    ax.plot([x + 0.05 * s, x + 0.22 * s], [y - 0.20 * s, y + 0.20 * s],
            color=CORAL, lw=1.1)
    ax.plot([x + 0.05 * s, x + 0.22 * s], [y + 0.20 * s, y - 0.20 * s],
            color=CORAL, lw=1.1)


def _matrix_item(ax, x: float, y: float, color: str, label: str, glyph: str) -> None:
    if glyph == "site":
        for dx, c in [(-0.030, BLUE), (0.000, BLUE), (0.030, CORAL)]:
            ax.add_patch(Rectangle((x + dx - 0.014, y - 0.018), 0.028, 0.036,
                                   facecolor=WHITE, edgecolor=c, lw=0.75))
    elif glyph == "protocol":
        _brain_glyph(ax, x, y, 0.050, color)
        ax.add_patch(Arc((x, y), 0.070, 0.070, theta1=30, theta2=325,
                         color=CORAL, lw=0.8))
    elif glyph == "modalities":
        _modality_glyph(ax, x, y, 0.075)
    elif glyph == "target":
        _brain_glyph(ax, x, y, 0.055, color)
        ax.add_patch(Circle((x + 0.010, y + 0.006), 0.010,
                            facecolor="none", edgecolor=CORAL, lw=1.0))
    elif glyph == "contours":
        _contours_glyph(ax, x, y, 0.060)
    elif glyph == "subgroup":
        for dx, c in [(-0.030, BLUE), (0.000, CORAL), (0.030, NAVY)]:
            _person_glyph(ax, x + dx, y, 0.040, c)
    elif glyph == "abstain":
        ax.add_patch(Circle((x, y), 0.026, facecolor=PALE_BLUE,
                            edgecolor=BLUE, lw=0.8))
        ax.text(x, y, "?", ha="center", va="center", fontsize=8.0,
                color=NAVY, weight="bold")
        ax.text(x + 0.034, y, "||", va="center", fontsize=7.0,
                color=CORAL, weight="bold")
    elif glyph == "review":
        _review_glyph(ax, x, y, 0.075, color)
    elif glyph == "lock":
        _lock_glyph(ax, x, y, 0.065, color)
    elif glyph == "human_ai":
        _person_glyph(ax, x - 0.022, y, 0.055, color)
        _monitor_glyph(ax, x + 0.030, y, 0.065, color)
    elif glyph == "benefit":
        ax.add_patch(Circle((x - 0.018, y), 0.017, facecolor=PALE_BLUE,
                            edgecolor=BLUE, lw=0.8))
        ax.add_patch(Circle((x + 0.018, y), 0.017, facecolor=PALE_CORAL,
                            edgecolor=CORAL, lw=0.8))
        ax.text(x, y, "≠", ha="center", va="center", fontsize=7.0, color=INK)
    elif glyph == "monitor":
        _monitor_glyph(ax, x, y, 0.065, color)
        ax.add_patch(Arc((x, y), 0.085, 0.085, theta1=25, theta2=315,
                         color=CORAL, lw=0.9))
    ax.text(x, y - 0.058, label, ha="center", va="top", fontsize=6.65,
            color=INK, linespacing=1.05)


def build_fig11() -> None:
    """Use domain-variable MRI and validation lanes to define priorities."""
    title = "Domain variability should drive validation priorities and deployment safeguards"
    fig, ax = plt.subplots(figsize=(FIGURE_WIDTH_IN, 5.90))
    schema(ax)
    _title(fig, title)
    ax.text(0.025, 0.925, "Observed acquisition variation", fontsize=9.0,
            color=NAVY, weight="bold")
    labels = ["reference-like", "low resolution", "intensity shift",
              "noise", "motion", "alternate protocol"]
    for j, label in enumerate(labels):
        tile = grid_crop("domain_variability_asset_sheet.png", 3, 2, j % 3, j // 3)
        x = 0.025 + j * 0.159
        image_box(ax, tile, x, 0.675, 0.135, 0.195, edge=GRID)
        ax.text(x + 0.0675, 0.648, label, ha="center", fontsize=7.3)
    ax.text(0.5, 0.600,
            "Preserve patient-level independence · lock the model · prespecify failure criteria",
            ha="center", fontsize=8.1, color=INK, weight="bold")
    arrow(ax, (0.5, 0.635), (0.5, 0.585), color=NAVY)

    rows = [
        (0.485, BLUE, PALE_BLUE_2, "ROBUSTNESS", [
            ("site-held-out\ntest", "site"), ("protocol\nstress", "protocol"),
            ("supported missing\nmodalities", "modalities"), ("failure\nlocalization", "target")]),
        (0.325, NAVY, PALE_GRAY, "TRUST", [
            ("multirater\nuncertainty", "contours"), ("subgroup\naudit", "subgroup"),
            ("uncertainty +\nabstention", "abstain"), ("transparent\nerror review", "review")]),
        (0.165, CORAL, PALE_CORAL_2, "TRANSLATION", [
            ("locked external\nvalidation", "lock"), ("human–AI\nworkflow", "human_ai"),
            ("decision change +\nnet benefit", "benefit"), ("monitor · rollback\nrevalidate", "monitor")]),
    ]
    for yy, color, face, name, items in rows:
        rounded_panel(ax, 0.120, yy - 0.055, 0.825, 0.110,
                      face=face, edge=color, radius=0.012, lw=0.65)
        ax.text(0.030, yy, name, va="center", fontsize=8.0,
                color=color, weight="bold")
        for xx, (label, glyph) in zip((0.245, 0.445, 0.645, 0.845), items):
            _matrix_item(ax, xx, yy + 0.013, color, label, glyph)
    arrow(ax, (0.970, 0.500), (0.970, 0.135), color=CORAL, lw=1.0)
    ax.text(0.985, 0.318, "increasing clinical consequence", rotation=90,
            ha="center", va="center", fontsize=6.4, color=CORAL)
    ax.text(0.5, 0.018,
            "Research priority: transportability and monitored clinical benefit—not another internal leaderboard gain.",
            ha="center", fontsize=7.7, color=INK, weight="bold")
    save(fig, "fig11_validation_roadmap", title,
         ["domain variability", "robustness lane", "trust lane", "translation lane"],
         raster=True, schematic_curves=False, assertions=[
             "Synthetic MRI tiles illustrate acquisition domains rather than patient outcomes.",
             "Three validation lanes separate robustness, trust, and clinical translation priorities.",
             "The central arrow links observed variability to prespecified validation; the right arrow denotes increasing clinical consequence.",
             "No performance values or regulatory claims are shown.",
         ])


if __name__ == "__main__":
    build_fig09()
    build_fig10()
    build_fig11()
