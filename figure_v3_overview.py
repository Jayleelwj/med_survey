"""Image-anchored overview plates for Figs. 1--3 of the IEEE survey.

ImageGen assets provide only synthetic MRI and spatial-feature subjects.  All
scientific labels, grouping rules, contours, operators, and connectors are
deterministic Matplotlib vectors.  The module deliberately avoids the repeated
rounded-box grammar of the earlier figures: spatial anatomy, tensor glyphs,
patient-by-visit structure, and evidence strata carry the visual argument.
"""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes
from matplotlib.patches import Circle, Polygon, Rectangle

import figure_v3_common as c


def _plate_title(fig: plt.Figure, text: str) -> None:
    fig.suptitle(text, x=0.5, y=0.987, fontsize=11.2, fontweight="bold",
                 color=c.INK)


def _narrow_heading(ax: Axes, label: str, title: str) -> None:
    """Two-line heading sized for a narrow GridSpec column."""
    ax.text(0.015, 0.982, label, transform=ax.transAxes, va="top", ha="left",
            fontsize=9.7, fontweight="bold", color=c.NAVY)
    ax.text(0.16, 0.982, title, transform=ax.transAxes, va="top", ha="left",
            fontsize=8.8, fontweight="bold", color=c.INK, linespacing=1.05)


def _crop(sheet: str, cols: int, rows: int, col: int, row: int,
          *, pad_x: float = 0.025, pad_y: float = 0.045) -> np.ndarray:
    return c.grid_crop(sheet, cols, rows, col, row,
                       pad_x=pad_x, pad_y=pad_y)


def _rule(ax: Axes, x0: float, x1: float, y: float, *, color: str = c.GRID,
          lw: float = 0.7, style: str = "-") -> None:
    ax.plot([x0, x1], [y, y], color=color, lw=lw, linestyle=style,
            solid_capstyle="round", zorder=2)


def _leader(ax: Axes, start: tuple[float, float], end: tuple[float, float],
            *, color: str = c.GRAY, style: str = "-") -> None:
    """Non-directional callout line; never used to imply data flow."""
    c.link(ax, start, end, color=color, lw=0.72, style=style)


def _image_fit(ax: Axes, image: np.ndarray, x: float, y: float,
               w: float, h: float, *, edge: str = c.GRID,
               lw: float = 0.7, zorder: int = 3) -> None:
    """Place an image without changing its native aspect ratio."""
    inset = ax.inset_axes([x, y, w, h], zorder=zorder)
    inset.imshow(image, interpolation="lanczos", aspect="equal")
    inset.set_xticks([])
    inset.set_yticks([])
    inset.set_facecolor(c.WHITE)
    for spine in inset.spines.values():
        spine.set_visible(True)
        spine.set_color(edge)
        spine.set_linewidth(lw)


def _stack_glyph(ax: Axes, x: float, y: float, *, color: str = c.BLUE,
                 fill: str = c.PALE_BLUE, scale: float = 1.0) -> None:
    w, h, d = 0.047 * scale, 0.042 * scale, 0.006 * scale
    for k in reversed(range(3)):
        ax.add_patch(Rectangle((x + k * d, y + k * d), w, h,
                               facecolor=fill, edgecolor=color, lw=0.65,
                               zorder=3 + 2 - k))


def _slice_glyph(ax: Axes, x: float, y: float, *, kind: str,
                 scale: float = 1.0) -> None:
    """Compact vector input-representation glyphs."""
    w, h = 0.052 * scale, 0.062 * scale
    if kind == "2-D":
        ax.add_patch(Rectangle((x, y), w, h, facecolor=c.PALE_BLUE,
                               edgecolor=c.BLUE, lw=0.75, zorder=3))
        ax.add_patch(Circle((x + 0.55 * w, y + 0.54 * h), 0.10 * h,
                            facecolor=c.PALE_CORAL, edgecolor=c.CORAL,
                            lw=0.65, zorder=4))
    elif kind == "2.5-D":
        for k in reversed(range(3)):
            off = 0.007 * k * scale
            ax.add_patch(Rectangle((x + off, y + off), w, h,
                                   facecolor=c.PALE_BLUE_2 if k != 1 else c.PALE_BLUE,
                                   edgecolor=c.BLUE, lw=0.65, zorder=3 + 2 - k))
    elif kind == "3-D":
        c.voxel_cube(ax, x, y, 0.058 * scale, face=c.PALE_BLUE,
                     edge=c.BLUE, n=3)
    elif kind == "Multisequence":
        fills = (c.PALE_GRAY, c.PALE_BLUE, c.PALE_CORAL)
        edges = (c.GRAY, c.BLUE, c.CORAL)
        for k, (fill, edge) in enumerate(zip(fills, edges)):
            ax.add_patch(Rectangle((x + 0.012 * k * scale,
                                    y + 0.006 * k * scale), w, h,
                                   facecolor=fill, edgecolor=edge, lw=0.65,
                                   zorder=3 + k))
    elif kind == "Longitudinal":
        for k, edge in enumerate((c.BLUE, c.CORAL)):
            ax.add_patch(Rectangle((x + 0.040 * k * scale, y), w, h,
                                   facecolor=c.PALE_BLUE_2 if k == 0 else c.PALE_CORAL_2,
                                   edgecolor=edge, lw=0.7, zorder=3))
        ax.text(x + 0.036 * scale, y + 0.5 * h, "\u0394", ha="center", va="center",
                fontsize=7.7, color=c.NAVY, zorder=5)


def _method_glyph(ax: Axes, x: float, y: float, *, kind: str) -> None:
    """Domain-specific method marks with no implied performance ranking."""
    if kind == "CNN / U-Net":
        widths = (0.048, 0.038, 0.028)
        for k, width in enumerate(widths):
            ax.add_patch(Rectangle((x + 0.018 * k, y + 0.008 * k), width,
                                   0.055 - 0.010 * k, facecolor=c.PALE_BLUE,
                                   edgecolor=c.BLUE, lw=0.65, zorder=3))
        ax.plot([x + 0.060, x + 0.085, x + 0.110],
                [y + 0.035, y + 0.018, y + 0.035], color=c.CORAL, lw=0.85,
                zorder=4)
    elif kind == "Transformer / hybrid":
        for row in range(2):
            for col in range(4):
                ax.add_patch(Rectangle((x + 0.020 * col, y + 0.029 * row),
                                       0.015, 0.021, facecolor=c.PALE_BLUE,
                                       edgecolor=c.BLUE, lw=0.5, zorder=3))
        for col in range(4):
            ax.plot([x + 0.0075, x + 0.0675],
                    [y + 0.0105 + 0.006 * col, y + 0.0395 - 0.006 * col],
                    color=c.GRAY, lw=0.45, alpha=0.85, zorder=2)
    elif kind == "Generative / unfolding":
        ax.add_patch(Circle((x + 0.025, y + 0.030), 0.022,
                            facecolor=c.PALE_GRAY, edgecolor=c.GRAY, lw=0.7))
        ax.add_patch(Circle((x + 0.085, y + 0.030), 0.022,
                            facecolor=c.PALE_CORAL, edgecolor=c.CORAL, lw=0.7))
        ax.plot([x + 0.047, x + 0.063], [y + 0.030, y + 0.030],
                color=c.NAVY, lw=0.9)
        ax.text(x + 0.055, y + 0.045, "z / DC", ha="center", va="bottom",
                fontsize=7.2, color=c.NAVY)
    elif kind == "SSL / federated":
        centers = ((x + 0.018, y + 0.046), (x + 0.018, y + 0.010),
                   (x + 0.082, y + 0.046), (x + 0.082, y + 0.010))
        for center in centers:
            ax.add_patch(Circle(center, 0.010, facecolor=c.PALE_BLUE,
                                edgecolor=c.BLUE, lw=0.65, zorder=4))
            ax.plot([center[0], x + 0.050], [center[1], y + 0.028],
                    color=c.GRAY, lw=0.55, linestyle="--", zorder=2)
        ax.add_patch(Circle((x + 0.050, y + 0.028), 0.014,
                            facecolor=c.PALE_CORAL, edgecolor=c.CORAL,
                            lw=0.7, zorder=4))


def _evidence_icon(ax: Axes, x: float, y: float, level: int) -> None:
    """Small evidence glyphs; the vertical coordinate carries maturity."""
    if level == 0:  # internal split
        ax.add_patch(Rectangle((x - 0.018, y - 0.015), 0.036, 0.030,
                               facecolor=c.PALE_GRAY, edgecolor=c.GRAY, lw=0.65))
        ax.plot([x - 0.004, x - 0.004], [y - 0.015, y + 0.015],
                color=c.CORAL, lw=0.7)
    elif level == 1:  # centers
        for dx in (-0.020, 0, 0.020):
            ax.add_patch(Circle((x + dx, y), 0.008,
                                facecolor=c.PALE_BLUE, edgecolor=c.BLUE,
                                lw=0.65))
        ax.plot([x - 0.020, x + 0.020], [y, y], color=c.GRAY, lw=0.55)
    elif level == 2:  # prospective human-AI loop
        ax.add_patch(Circle((x - 0.012, y + 0.007), 0.008,
                            facecolor=c.PALE_BLUE, edgecolor=c.BLUE, lw=0.65))
        ax.add_patch(Rectangle((x - 0.020, y - 0.015), 0.016, 0.016,
                               facecolor=c.PALE_BLUE, edgecolor=c.BLUE, lw=0.55))
        ax.add_patch(Rectangle((x + 0.005, y - 0.013), 0.025, 0.025,
                               facecolor=c.PALE_GRAY, edgecolor=c.GRAY, lw=0.65))
        ax.plot([x - 0.003, x + 0.005], [y, y], color=c.NAVY, lw=0.7)
    else:  # patient net benefit
        ax.add_patch(Circle((x, y + 0.009), 0.009,
                            facecolor=c.PALE_CORAL, edgecolor=c.CORAL, lw=0.65))
        ax.add_patch(Polygon([(x - 0.017, y - 0.015), (x + 0.017, y - 0.015),
                             (x + 0.010, y + 0.001), (x - 0.010, y + 0.001)],
                            closed=True, facecolor=c.PALE_CORAL,
                            edgecolor=c.CORAL, lw=0.65))


def build_fig01() -> None:
    """Survey map: imaging substrate, orthogonal design space, evidence depth."""
    title = "Evidence-centered survey map for artificial intelligence in MS MRI"
    fig = plt.figure(figsize=(c.FIGURE_WIDTH_IN, 4.75))
    _plate_title(fig, title)
    gs = fig.add_gridspec(1, 3, width_ratios=(1.05, 1.35, 0.92),
                          left=0.035, right=0.975, top=0.925, bottom=0.075,
                          wspace=0.15)

    # (a) Spatially anchored targets.
    ax = fig.add_subplot(gs[0, 0])
    c.schema(ax)
    _narrow_heading(ax, "(a)", "MS-oriented imaging\nsubstrate")
    flair = _crop("ms_mri_asset_sheet.png", 4, 2, 2, 0,
                  pad_x=0.035, pad_y=0.035)
    susceptibility = _crop("ms_mri_asset_sheet.png", 4, 2, 0, 1,
                           pad_x=0.035, pad_y=0.04)
    cord = _crop("ms_mri_asset_sheet.png", 4, 2, 3, 1,
                 pad_x=0.035, pad_y=0.04)
    c.image_box(ax, flair, 0.03, 0.36, 0.62, 0.49, edge=c.GRID, lw=0.75)
    # Local callouts identify analysis targets without claiming a measured case.
    ax.add_patch(Circle((0.45, 0.68), 0.032, facecolor="none",
                        edgecolor=c.CORAL, lw=0.95, zorder=7))
    _leader(ax, (0.48, 0.69), (0.70, 0.76), color=c.CORAL)
    ax.text(0.72, 0.76, "White-matter\nlesion burden", ha="left", va="center",
            fontsize=7.8, color=c.INK, linespacing=1.05)
    ax.add_patch(Circle((0.22, 0.55), 0.026, facecolor="none",
                        edgecolor=c.BLUE, lw=0.9, zorder=7))
    _leader(ax, (0.20, 0.53), (0.69, 0.47), color=c.BLUE)
    ax.text(0.71, 0.47, "Spatial\nquantification", ha="left", va="center",
            fontsize=7.8, linespacing=1.05)
    c.image_box(ax, susceptibility, 0.03, 0.08, 0.26, 0.20,
                edge=c.GRID, lw=0.7)
    c.image_box(ax, cord, 0.36, 0.08, 0.18, 0.20, edge=c.GRID, lw=0.7)
    ax.text(0.16, 0.045, "Susceptibility\ncues", ha="center", va="top",
            fontsize=7.1, linespacing=0.95)
    ax.text(0.45, 0.045, "Cervical\ncord", ha="center", va="top",
            fontsize=7.1, linespacing=0.95)

    # (b) Orthogonal, combinable design dimensions around one feature subject.
    ax = fig.add_subplot(gs[0, 1])
    c.schema(ax)
    _narrow_heading(ax, "(b)", "Combinable AI\ndesign dimensions")
    ax.text(0.05, 0.84, "Data provenance", ha="left", va="center",
            fontsize=8.1, fontweight="bold", color=c.NAVY)
    provenance = ((0.06, "benchmark"), (0.28, "controlled\ncohort"),
                  (0.53, "routine PACS"), (0.77, "follow-up"))
    for x, label in provenance:
        _stack_glyph(ax, x, 0.74, scale=0.9)
        ax.text(x + 0.028, 0.70, label, ha="center", va="top", fontsize=7.2,
                linespacing=1.0)
    _rule(ax, 0.04, 0.96, 0.635, color=c.GRID)

    ax.text(0.05, 0.59, "Input representation", ha="left", va="center",
            fontsize=8.0, fontweight="bold", color=c.NAVY)
    representations = ((0.06, "2-D / 2.5-D", "2.5-D"),
                       (0.29, "3-D volume", "3-D"),
                       (0.52, "multisequence", "Multisequence"),
                       (0.77, "longitudinal", "Longitudinal"))
    for x, label, glyph_kind in representations:
        _slice_glyph(ax, x, 0.47, kind=glyph_kind, scale=0.82)
        ax.text(x + 0.034, 0.435, label, ha="center", va="top", fontsize=7.0)
    _rule(ax, 0.04, 0.96, 0.39, color=c.GRID)

    ax.text(0.05, 0.35, "Learning mechanisms around a spatial feature subject",
            ha="left", va="center", fontsize=7.8, fontweight="bold",
            color=c.NAVY)
    feature = _crop("feature_space_asset_sheet.png", 3, 2, 2, 0,
                    pad_x=0.07, pad_y=0.06)
    c.image_box(ax, feature, 0.44, 0.105, 0.14, 0.20, edge=c.NAVY, lw=0.75)
    method_layout = ((0.04, 0.215, "CNN / U-Net", "CNN / U-Net"),
                     (0.04, 0.095, "Transformer / hybrid", "Transformer /\nhybrid"),
                     (0.65, 0.215, "Generative / unfolding", "Generative /\nunfolding"),
                     (0.65, 0.095, "SSL / federated", "SSL / federated"))
    for x, y, kind, display in method_layout:
        _method_glyph(ax, x, y, kind=kind)
        ax.text(x + 0.12, y + 0.028, display, ha="left", va="center",
                fontsize=6.6, linespacing=0.98)
    ax.text(0.50, 0.035,
            "Dimensions combine by task;\nno performance ranking.",
            ha="center", va="bottom", fontsize=6.5, color=c.GRAY,
            linespacing=0.95, clip_on=True)

    # (c) Evidence depth is intentionally independent of model family.
    ax = fig.add_subplot(gs[0, 2])
    c.schema(ax)
    _narrow_heading(ax, "(c)", "Evidence maturity\nprofile")
    levels = (
        (0.76, "Internal test", "technical fit"),
        (0.57, "Held-out centers", "transportability"),
        (0.38, "Prospective workflow", "human\u2013AI use"),
        (0.19, "Patient net benefit", "clinical value"),
    )
    ax.plot([0.22, 0.22], [0.15, 0.80], color=c.GRID, lw=2.2,
            solid_capstyle="round", zorder=1)
    ax.annotate("", xy=(0.22, 0.12), xytext=(0.22, 0.82),
                arrowprops=dict(arrowstyle="-|>", color=c.NAVY, lw=0.9,
                                mutation_scale=8), zorder=2)
    for idx, (y, label, qualifier) in enumerate(levels):
        face = c.PALE_BLUE if idx < 2 else c.PALE_CORAL
        edge = c.BLUE if idx < 2 else c.CORAL
        ax.add_patch(Circle((0.22, y), 0.035, facecolor=face,
                            edgecolor=edge, lw=0.9, zorder=4))
        _evidence_icon(ax, 0.22, y, idx)
        ax.text(0.34, y + 0.012, label, ha="left", va="center",
                fontsize=7.8, fontweight="bold")
        ax.text(0.34, y - 0.024, qualifier, ha="left", va="center",
                fontsize=7.3, color=c.GRAY)
    ax.text(0.08, 0.46, "increasing\nmaturity", rotation=90, ha="center",
            va="center", fontsize=7.4, color=c.NAVY, linespacing=1.0)
    _rule(ax, 0.14, 0.94, 0.08, color=c.GRID)
    ax.text(0.54, 0.025,
            "Claims must name\nthe validation level.",
            ha="center", va="bottom", fontsize=6.8, color=c.CORAL,
            linespacing=0.95, clip_on=True)

    c.save(
        fig, "fig01_survey_map", title,
        ["MS imaging substrate", "orthogonal AI design dimensions",
         "evidence maturity"],
        assertions=[
            "Synthetic MRI anchors MS lesions, susceptibility-sensitive imaging, and cervical-cord analysis without patient data.",
            "Data provenance, representation, and learning mechanism are orthogonal design dimensions; no row pairing or performance rank is implied.",
            "Evidence maturity proceeds from internal testing to patient net benefit and is independent of architecture family.",
            "All labels, callouts, connectors, and evidence glyphs are vector objects.",
        ],
        raster=True,
    )


def _sequence_callout(ax: Axes, x: float, y: float, text: str,
                      *, color: str) -> None:
    ax.plot([x, x], [y + 0.015, y + 0.042], color=color, lw=0.75, zorder=6)
    ax.add_patch(Circle((x, y + 0.046), 0.007, facecolor=c.WHITE,
                        edgecolor=color, lw=0.75, zorder=7))
    ax.text(x, y, text, ha="center", va="top", fontsize=7.25,
            linespacing=1.0)


def build_fig02() -> None:
    """Registered contrasts, explicit input representations, and domain context."""
    title = "MRI contrasts and data representations used by AI for MS"
    fig = plt.figure(figsize=(c.FIGURE_WIDTH_IN, 5.85))
    _plate_title(fig, title)
    ax = fig.add_axes([0.035, 0.055, 0.94, 0.88])
    c.schema(ax)

    # (a) Four matched brain contrasts plus specialized acquisitions.
    c.heading(ax, "(a)", "Registered brain contrasts and specialized MS views")
    brain_labels = ("T1-weighted", "T2-weighted", "FLAIR", "Post-contrast T1")
    brain_targets = ("anatomy /\natrophy", "water-sensitive\nsignal",
                     "WM lesion\nconspicuity", "enhancing\nactivity")
    xs = (0.02, 0.175, 0.33, 0.485)
    y_img, w_img, h_img = 0.665, 0.135, 0.225
    for col, (x, label, target) in enumerate(zip(xs, brain_labels, brain_targets)):
        image = _crop("ms_mri_asset_sheet.png", 4, 2, col, 0,
                      pad_x=0.035, pad_y=0.04)
        c.image_box(ax, image, x, y_img, w_img, h_img, edge=c.GRID, lw=0.7)
        ax.text(x + w_img / 2, 0.635, label, ha="center", va="top",
                fontsize=7.45, fontweight="bold")
        _sequence_callout(ax, x + w_img / 2, 0.575, target,
                          color=c.BLUE if col < 3 else c.CORAL)
    _rule(ax, 0.02, 0.62, 0.915, color=c.BLUE, lw=1.0)
    ax.text(0.32, 0.925, "Same synthetic brain case; registered contrasts",
            ha="center", va="bottom", fontsize=7.5, color=c.NAVY)

    specialized = (
        (0.665, 0, 1, "Susceptibility", "susceptibility-\nrelated cues"),
        (0.825, 3, 1, "Cervical cord", "cord lesion\nassessment"),
    )
    for x, col, row, label, target in specialized:
        image = _crop("ms_mri_asset_sheet.png", 4, 2, col, row,
                      pad_x=0.035, pad_y=0.04)
        c.image_box(ax, image, x, y_img, 0.135, h_img, edge=c.GRID, lw=0.7)
        ax.text(x + 0.0675, 0.635, label, ha="center", va="top",
                fontsize=7.45, fontweight="bold")
        _sequence_callout(ax, x + 0.0675, 0.575, target, color=c.CORAL)
    _rule(ax, 0.665, 0.96, 0.915, color=c.CORAL, lw=1.0)
    ax.text(0.812, 0.925, "Specialized acquisitions", ha="center", va="bottom",
            fontsize=7.5, color=c.CORAL)

    # (b) Representation panel uses actual MRI/feature assets rather than empty tiles.
    ax.text(0.015, 0.505, "(b)", ha="left", va="top", fontsize=10.4,
            fontweight="bold", color=c.NAVY)
    ax.text(0.09, 0.505, "Network input representations", ha="left", va="top",
            fontsize=10.0, fontweight="bold")
    representation_x = (0.03, 0.275, 0.52, 0.765)
    flair = _crop("ms_mri_asset_sheet.png", 4, 2, 2, 0,
                  pad_x=0.045, pad_y=0.05)

    # 2-D: one slice.
    c.image_box(ax, flair, representation_x[0], 0.275, 0.15, 0.155,
                edge=c.BLUE, lw=0.75)
    ax.text(representation_x[0] + 0.075, 0.245, "2-D", ha="center",
            fontsize=7.8, fontweight="bold")
    ax.text(representation_x[0] + 0.075, 0.216, "single slice", ha="center",
            fontsize=7.2, color=c.GRAY)

    # 2.5-D: adjacent slices represented by a visibly offset MRI slab.
    for k in reversed(range(3)):
        xx = representation_x[1] + 0.015 * k
        yy = 0.275 + 0.008 * k
        c.image_box(ax, flair, xx, yy, 0.135, 0.145,
                    edge=c.BLUE, lw=0.55, zorder=2 + 2 - k)
    ax.text(representation_x[1] + 0.082, 0.245, "2.5-D", ha="center",
            fontsize=7.8, fontweight="bold")
    ax.text(representation_x[1] + 0.082, 0.216, "adjacent-slice channels",
            ha="center", fontsize=7.2, color=c.GRAY)

    # 3-D: ImageGen volume/voxel subject with a vector depth bracket.
    volume = _crop("feature_space_asset_sheet.png", 3, 2, 1, 0,
                   pad_x=0.035, pad_y=0.055)
    c.image_box(ax, volume, representation_x[2], 0.275, 0.18, 0.155,
                edge=c.BLUE, lw=0.75)
    ax.plot([representation_x[2] + 0.185] * 2, [0.285, 0.418],
            color=c.BLUE, lw=0.7)
    ax.plot([representation_x[2] + 0.178, representation_x[2] + 0.192],
            [0.285, 0.285], color=c.BLUE, lw=0.7)
    ax.plot([representation_x[2] + 0.178, representation_x[2] + 0.192],
            [0.418, 0.418], color=c.BLUE, lw=0.7)
    ax.text(representation_x[2] + 0.09, 0.245, "3-D", ha="center",
            fontsize=7.8, fontweight="bold")
    ax.text(representation_x[2] + 0.09, 0.216, "volumetric context",
            ha="center", fontsize=7.2, color=c.GRAY)

    # Multisequence: registered contrast channels, not a generic stack.
    channel_w = 0.062
    for k, col in enumerate((0, 1, 2)):
        image = _crop("ms_mri_asset_sheet.png", 4, 2, col, 0,
                      pad_x=0.05, pad_y=0.06)
        c.image_box(ax, image, representation_x[3] + k * 0.052,
                    0.285 + k * 0.006, channel_w, 0.135,
                    edge=(c.GRAY, c.BLUE, c.CORAL)[k], lw=0.6,
                    zorder=2 + k)
    ax.text(representation_x[3] + 0.083, 0.245, "Multisequence",
            ha="center", fontsize=7.8, fontweight="bold")
    ax.text(representation_x[3] + 0.083, 0.216, "registered contrast channels",
            ha="center", fontsize=7.2, color=c.GRAY)
    _rule(ax, 0.03, 0.95, 0.195, color=c.GRID, lw=0.65)

    # (c) Optional module bank and scanner-domain variation.
    ax.text(0.015, 0.170, "(c)", ha="left", va="top", fontsize=10.4,
            fontweight="bold", color=c.NAVY)
    ax.text(0.09, 0.170, "Prespecified preprocessing choices and domain variables",
            ha="left", va="top", fontsize=10.0, fontweight="bold")
    center = (0.28, 0.058)
    ax.add_patch(Circle(center, 0.032, facecolor=c.PALE_BLUE,
                        edgecolor=c.BLUE, lw=0.8, zorder=4))
    ax.text(*center, "AI\ninput", ha="center", va="center", fontsize=7.3,
            fontweight="bold", linespacing=0.95, zorder=5)
    ax.text(0.28, 0.122, "Task-dependent module bank (no universal order)",
            ha="center", va="center", fontsize=6.85, color=c.NAVY)
    modules = ((0.07, 0.078, "Registration", 0.098),
               (0.17, 0.036, "Resampling", 0.014),
               (0.39, 0.036, "Bias-field corr.", 0.014),
               (0.49, 0.078, "Intensity norm.", 0.098))
    for x, y, label, label_y in modules:
        ax.add_patch(Circle((x, y), 0.010, facecolor=c.WHITE,
                            edgecolor=c.GRAY, lw=0.75, zorder=4))
        _leader(ax, (x, y), center, style="--")
        ax.text(x, label_y, label, ha="center",
                va="bottom" if label_y > y else "top", fontsize=6.85)

    domain_x = (0.60, 0.72, 0.84)
    domain_labels = ("vendor / field", "protocol", "reconstruction")
    for x, col, label in zip(domain_x, (0, 1, 4), domain_labels):
        image = _crop("domain_variability_asset_sheet.png", 3, 2,
                      col % 3, col // 3, pad_x=0.04, pad_y=0.05)
        c.image_box(ax, image, x, 0.025, 0.095, 0.075,
                    edge=c.GRID, lw=0.6)
        ax.text(x + 0.0475, 0.014, label, ha="center", va="top",
                fontsize=7.0, color=c.GRAY)
    ax.text(0.77, 0.122, "Same synthetic anatomy across image domains",
            ha="center", va="center", fontsize=6.85, color=c.CORAL)

    c.save(
        fig, "fig02_mri_inputs", title,
        ["registered MRI contrasts", "2-D/2.5-D/3-D/multisequence inputs",
         "preprocessing choices and domain variables"],
        assertions=[
            "T1-weighted MRI is labeled for anatomy/atrophy rather than as a lesion-specific sequence.",
            "Susceptibility imaging is described only as supplying susceptibility-related cues.",
            "The first four brain contrasts depict one synthetic registered case; specialized susceptibility and cord acquisitions are grouped separately.",
            "Preprocessing modules are optional prespecified choices and are not drawn as a universal rigid order.",
            "MRI, volume, and domain subjects are raster assets; all labels, brackets, callouts, and grouping marks are vectors.",
        ],
        raster=True,
    )


def _visit_thumb(ax: Axes, image: np.ndarray, x: float, y: float, *,
                 edge: str, alpha: float = 1.0) -> None:
    _image_fit(ax, image, x, y, 0.075, 0.075, edge=edge, lw=0.72,
               zorder=3)


def _contour(ax: Axes, x: float, y: float, w: float, h: float,
             points: tuple[tuple[float, float], ...], *, color: str,
             style: str = "-", lw: float = 0.95, fill: str = "none",
             alpha: float = 1.0, zorder: int = 7) -> None:
    poly = [(x + px * w, y + py * h) for px, py in points]
    ax.add_patch(Polygon(poly, closed=True, facecolor=fill, edgecolor=color,
                         lw=lw, linestyle=style, alpha=alpha, zorder=zorder))


def build_fig03() -> None:
    """Leakage-aware patient splits and multireader reference construction."""
    title = "Patient-level splitting and multireader reference construction"
    fig = plt.figure(figsize=(c.FIGURE_WIDTH_IN, 5.65))
    _plate_title(fig, title)
    gs = fig.add_gridspec(2, 2, height_ratios=(1.15, 0.95),
                          width_ratios=(1.0, 1.0), left=0.04, right=0.975,
                          top=0.925, bottom=0.065, hspace=0.17, wspace=0.13)

    longitudinal = []
    for col in range(4):
        visit = _crop("longitudinal_flair_asset_sheet.png", 4, 1, col, 0,
                      pad_x=0.035, pad_y=0.08)
        # The asset cells are portrait canvases.  A centered square crop keeps
        # the axial anatomy undistorted in compact patient-by-visit matrices.
        side = min(visit.shape[:2])
        y_start = (visit.shape[0] - side) // 2
        x_start = (visit.shape[1] - side) // 2
        longitudinal.append(
            visit[y_start:y_start + side, x_start:x_start + side]
        )

    # (a) Patient-by-visit matrix: partitions occupy whole rows.
    ax = fig.add_subplot(gs[0, :])
    c.schema(ax)
    c.heading(ax, "(a)", "Patient-level partitioning across longitudinal visits")
    x0, y0 = 0.08, 0.13
    col_x = (0.25, 0.40, 0.55)
    col_labels = ("Baseline", "Follow-up", "Registered follow-up")
    for x, label in zip(col_x, col_labels):
        ax.text(x + 0.0375, 0.82, label, ha="center", va="bottom",
                fontsize=7.5, fontweight="bold")
    rows = (
        (0.66, "Patient A", "TRAIN", c.PALE_BLUE_2, c.BLUE),
        (0.52, "Patient B", "TRAIN", c.PALE_BLUE_2, c.BLUE),
        (0.38, "Patient C", "VALIDATION", c.PALE_GRAY, c.GRAY),
        (0.24, "Patient D", "TEST", c.PALE_CORAL_2, c.CORAL),
    )
    for row_index, (y, patient, partition, face, edge) in enumerate(rows):
        ax.add_patch(Rectangle((x0, y - 0.012), 0.58, 0.102,
                               facecolor=face, edgecolor="none", zorder=0))
        ax.add_patch(Rectangle((x0, y - 0.012), 0.008, 0.102,
                               facecolor=edge, edgecolor="none", zorder=1))
        ax.text(0.105, y + 0.055, patient, ha="left", va="center",
                fontsize=7.2, fontweight="bold")
        ax.text(0.105, y + 0.022, partition, ha="left", va="center",
                fontsize=6.9, color=edge, fontweight="bold")
        for visit_index, x in enumerate(col_x):
            # The same three synthetic visits recur only to illustrate the
            # grouping rule; the plate explicitly disclaims cohort size.
            _visit_thumb(ax, longitudinal[visit_index], x, y,
                         edge=edge, alpha=0.98 - 0.04 * row_index)
        ax.plot([0.215, 0.68], [y - 0.020, y - 0.020], color=c.WHITE,
                lw=1.0, zorder=2)

    # A real longitudinal strip anchors the abstract split matrix.
    ax.plot([0.72, 0.72], [0.19, 0.83], color=c.GRID, lw=0.8)
    ax.text(0.75, 0.82, "One synthetic patient", ha="left", va="bottom",
            fontsize=7.7, fontweight="bold", color=c.NAVY)
    exemplar_y = (0.64, 0.46, 0.28)
    exemplar_labels = ("baseline", "follow-up", "registered")
    for y, image, label in zip(exemplar_y, longitudinal[:3], exemplar_labels):
        _image_fit(ax, image, 0.75, y, 0.12, 0.12, edge=c.BLUE, lw=0.7)
        ax.text(0.89, y + 0.06, label, ha="left", va="center", fontsize=7.4)
    ax.plot([0.735, 0.735], [0.29, 0.75], color=c.BLUE, lw=1.0)
    ax.plot([0.728, 0.742], [0.29, 0.29], color=c.BLUE, lw=1.0)
    ax.plot([0.728, 0.742], [0.75, 0.75], color=c.BLUE, lw=1.0)
    ax.text(0.82, 0.16, "all visits remain in one partition", ha="center",
            va="center", fontsize=7.4, color=c.NAVY)
    ax.text(0.08, 0.065,
            "Illustrative identifiers only\u2014rows do not represent cohort size.",
            ha="left", va="center", fontsize=7.25, color=c.GRAY)

    # (b) Leakage is shown as identity overlap, not as a performance result.
    ax = fig.add_subplot(gs[1, 0])
    c.schema(ax)
    c.heading(ax, "(b)", "Visit-level leakage and the patient-level remedy")
    _image_fit(ax, longitudinal[0], 0.05, 0.46, 0.24, 0.27,
               edge=c.BLUE, lw=0.8)
    _image_fit(ax, longitudinal[1], 0.39, 0.46, 0.24, 0.27,
               edge=c.CORAL, lw=0.8)
    ax.text(0.17, 0.42, "Train visit", ha="center", fontsize=7.5,
            fontweight="bold", color=c.BLUE)
    ax.text(0.51, 0.42, "Test visit", ha="center", fontsize=7.5,
            fontweight="bold", color=c.CORAL)
    # A labeled bracket denotes shared identity; it is deliberately not an arrow.
    ax.plot([0.17, 0.17, 0.51, 0.51], [0.77, 0.82, 0.82, 0.77],
            color=c.CORAL, lw=0.95)
    ax.text(0.34, 0.845, "same patient identity", ha="center", va="bottom",
            fontsize=7.5, color=c.CORAL, fontweight="bold")
    ax.text(0.69, 0.60, "\u00d7", ha="center", va="center", fontsize=18,
            fontweight="bold", color=c.CORAL)
    ax.text(0.76, 0.48, "Wrong:\nvisit-level split", ha="center", va="top",
            fontsize=7.5, color=c.CORAL, linespacing=1.05)
    _rule(ax, 0.05, 0.95, 0.30, color=c.GRID)
    ax.add_patch(Rectangle((0.08, 0.11), 0.10, 0.075,
                           facecolor=c.PALE_BLUE, edgecolor=c.BLUE, lw=0.7))
    ax.add_patch(Rectangle((0.20, 0.11), 0.10, 0.075,
                           facecolor=c.PALE_BLUE, edgecolor=c.BLUE, lw=0.7))
    ax.plot([0.075, 0.075, 0.305, 0.305], [0.20, 0.23, 0.23, 0.20],
            color=c.NAVY, lw=0.8)
    ax.text(0.19, 0.255, "same partition", ha="center", va="bottom",
            fontsize=7.2, color=c.NAVY)
    ax.text(0.40, 0.15, "Correct: split once by patient identifier,\nthen retain every visit together.",
            ha="left", va="center", fontsize=7.5, linespacing=1.15)
    ax.text(0.95, 0.035, "Schematic grouping\u2014no performance data.",
            ha="right", va="bottom", fontsize=7.15, color=c.GRAY)

    # (c) Multireader contours and adjudicated reference on one lesion crop.
    ax = fig.add_subplot(gs[1, 1])
    c.schema(ax)
    c.heading(ax, "(c)", "Multireader reference and adjudication")
    flair = _crop("ms_mri_asset_sheet.png", 4, 2, 2, 0,
                  pad_x=0.035, pad_y=0.04)
    # Square lesion crop from the raw synthetic FLAIR panel.  Unlike the
    # feature-space asset, it contains no rasterized contours; every reader
    # outline below is therefore a deterministic vector overlay.
    side = int(0.55 * flair.shape[1])
    y_start = int(0.155 * flair.shape[0])
    lesion = flair[y_start:y_start + side, :side]
    c.image_box(ax, lesion, 0.04, 0.34, 0.39, 0.43, edge=c.GRID, lw=0.75)
    c.image_box(ax, lesion, 0.57, 0.34, 0.39, 0.43, edge=c.GRID, lw=0.75)

    reader_1 = ((0.37, 0.13), (0.48, 0.10), (0.58, 0.15), (0.63, 0.26),
                (0.60, 0.39), (0.51, 0.45), (0.40, 0.41), (0.34, 0.27))
    reader_2 = ((0.34, 0.11), (0.48, 0.07), (0.61, 0.13), (0.67, 0.27),
                (0.63, 0.43), (0.51, 0.49), (0.37, 0.44), (0.30, 0.26))
    reader_3 = ((0.39, 0.15), (0.48, 0.12), (0.56, 0.17), (0.60, 0.27),
                (0.57, 0.37), (0.50, 0.42), (0.41, 0.38), (0.36, 0.27))
    _contour(ax, 0.04, 0.34, 0.39, 0.43, reader_1, color=c.BLUE,
             style="-", lw=0.9)
    _contour(ax, 0.04, 0.34, 0.39, 0.43, reader_2, color=c.CORAL,
             style="--", lw=0.9)
    _contour(ax, 0.04, 0.34, 0.39, 0.43, reader_3, color=c.GRAY,
             style=":", lw=1.0)
    consensus = ((0.36, 0.13), (0.48, 0.09), (0.59, 0.15), (0.64, 0.27),
                 (0.61, 0.41), (0.50, 0.46), (0.39, 0.42), (0.33, 0.27))
    _contour(ax, 0.57, 0.34, 0.39, 0.43, consensus, color=c.NAVY,
             lw=1.25, fill=c.PALE_BLUE, alpha=0.70)
    ax.add_patch(Circle((0.88, 0.72), 0.010, facecolor=c.PALE_CORAL,
                        edgecolor=c.CORAL, lw=0.7, zorder=8))
    ax.text(0.85, 0.72, "adjudicated", ha="right", va="center",
            fontsize=7.0, color=c.CORAL)
    ax.text(0.235, 0.30, "Reader contours", ha="center", va="top",
            fontsize=7.6, fontweight="bold")
    ax.text(0.765, 0.30, "Consensus / adjudicated reference", ha="center",
            va="top", fontsize=7.6, fontweight="bold")
    legend_y = 0.18
    for x, color, style, text in (
        (0.06, c.BLUE, "-", "Reader 1"),
        (0.27, c.CORAL, "--", "Reader 2"),
        (0.48, c.GRAY, ":", "Reader 3"),
        (0.69, c.NAVY, "-", "Reference"),
    ):
        ax.plot([x, x + 0.07], [legend_y, legend_y], color=color,
                lw=1.0 if text != "Reference" else 1.3, linestyle=style)
        ax.text(x + 0.085, legend_y, text, ha="left", va="center", fontsize=7.1)
    ax.text(0.50, 0.065,
            "Contours are schematic vector overlays; disagreement remains reportable.",
            ha="center", va="center", fontsize=7.25, color=c.GRAY)

    c.save(
        fig, "fig03_data_realism", title,
        ["patient-by-visit partition", "visit-level leakage",
         "multireader consensus and adjudication"],
        assertions=[
            "All visits from an illustrative patient remain in a single train, validation, or test partition.",
            "The leakage panel identifies shared patient identity across train and test visits and reports no performance values.",
            "Reader contours, consensus fill, adjudication marker, labels, brackets, and partition encodings are vector objects.",
            "Illustrative patient rows and synthetic images do not encode cohort size, prevalence, or empirical agreement.",
        ],
        raster=True,
    )


if __name__ == "__main__":
    build_fig01()
    build_fig02()
    build_fig03()
