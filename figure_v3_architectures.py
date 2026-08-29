"""ImageGen-anchored, vector-topology architecture plates for Figs. 4--8.

Only synthetic MRI and spatial-feature subjects are raster.  Scientific labels,
operators, arrows, masks, and network topology are deterministic vectors.
"""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes
from matplotlib.patches import Circle, Polygon, Rectangle

import figure_v3_common as C


def _mri(col: int = 2, row: int = 0) -> np.ndarray:
    return C.grid_crop("ms_mri_asset_sheet.png", 4, 2, col, row)


def _feature(col: int, row: int) -> np.ndarray:
    return C.grid_crop("feature_space_asset_sheet.png", 3, 2, col, row)


def _longitudinal(col: int) -> np.ndarray:
    return C.grid_crop("longitudinal_flair_asset_sheet.png", 4, 1, col, 0,
                       pad_x=0.018, pad_y=0.025)


def _image_anchor(ax: Axes, image: np.ndarray, x: float, y: float,
                  w: float, h: float, label: str) -> None:
    C.image_box(ax, image, x, y, w, h, edge=C.GRID, lw=0.75)
    ax.text(x + w / 2, y - 0.026, label, ha="center", va="top",
            fontsize=7.5, color=C.INK)


def _output_overlay(ax: Axes, x: float, y: float, w: float, h: float,
                    label: str, *, volume: bool = False) -> None:
    if volume:
        C.voxel_cube(ax, x, y + 0.015, min(w, h) * 0.78,
                     face=C.PALE_CORAL, edge=C.CORAL, n=4)
        ax.add_patch(Circle((x + w * 0.48, y + h * 0.50), min(w, h) * 0.10,
                            facecolor=C.CORAL, edgecolor=C.CORAL, alpha=0.72,
                            zorder=7))
    else:
        C.image_box(ax, _mri(2, 0), x, y, w, h, edge=C.CORAL, lw=0.8)
        C.mask_overlay(
            ax, x, y, w, h,
            reference=[(0.24, 0.42), (0.34, 0.30), (0.49, 0.34),
                       (0.54, 0.52), (0.41, 0.63), (0.27, 0.57)],
            prediction=[(0.25, 0.43), (0.35, 0.32), (0.48, 0.35),
                        (0.52, 0.51), (0.40, 0.60), (0.28, 0.56)],
        )
    ax.text(x + w / 2, y - 0.026, label, ha="center", va="top",
            fontsize=7.5, color=C.CORAL)


def _edge_operator(ax: Axes, start: tuple[float, float],
                   center: tuple[float, float], end: tuple[float, float],
                   symbol: str, *, color: str) -> None:
    C.arrow(ax, start, (center[0] - 0.026, center[1]), color=color, lw=0.85)
    C.op(ax, center[0], center[1], symbol, r=0.024, fontsize=7.4,
         face=C.WHITE, edge=C.GRAY)
    C.arrow(ax, (center[0] + 0.026, center[1]), end, color=color, lw=0.85)


def _slab(ax: Axes, x: float, y: float, w: float, h: float, text: str,
          *, decoder: bool = False, volume: bool = False) -> None:
    C.feature_slab(
        ax, x, y, w, h,
        face=C.PALE_CORAL if decoder else C.PALE_BLUE,
        edge=C.CORAL if decoder else C.BLUE,
        depth=3 if volume else 2,
        label=text,
    )


def _draw_unet(ax: Axes, label: str, title: str, *, dimension: str,
               residual: bool = False) -> None:
    C.schema(ax)
    C.heading(ax, label, title)
    volume = dimension == "3-D"
    if volume:
        _image_anchor(ax, _feature(1, 0), 0.012, 0.49, 0.105, 0.31,
                      "3-D MRI volume")
    else:
        _image_anchor(ax, _mri(2, 0), 0.014, 0.51, 0.100, 0.29,
                      "2-D multisequence MRI")

    enc = [
        (0.145, 0.65, 0.078, 0.125),
        (0.275, 0.50, 0.068, 0.110),
        (0.395, 0.36, 0.059, 0.095),
    ]
    block_name = "Residual\nblock" if residual else f"{dimension} Conv"
    for x, y, w, h in enc:
        _slab(ax, x, y, w, h, block_name, volume=volume)
    C.arrow(ax, (0.114, 0.655), (enc[0][0], enc[0][1] + enc[0][3] / 2),
            color=C.BLUE)

    for i in range(2):
        sx, sy, sw, sh = enc[i]
        ex, ey, _, eh = enc[i + 1]
        mid = ((sx + sw + ex) / 2, (sy + sh / 2 + ey + eh / 2) / 2)
        _edge_operator(ax, (sx + sw, sy + sh / 2), mid,
                       (ex, ey + eh / 2), "↓2", color=C.BLUE)

    bottleneck = (0.470, 0.205, 0.064, 0.090)
    _slab(ax, *bottleneck, "Residual\nbase" if residual else f"{dimension}\nbase",
          volume=volume)
    sx, sy, sw, sh = enc[-1]
    _edge_operator(ax, (sx + sw, sy + sh / 2), (0.472, 0.335),
                   (bottleneck[0], bottleneck[1] + bottleneck[3] / 2),
                   "↓2", color=C.BLUE)

    concat = [(0.555, 0.405), (0.660, 0.555), (0.755, 0.700)]
    dec = [
        (0.590, 0.355, 0.061, 0.100),
        (0.695, 0.500, 0.064, 0.110),
        (0.790, 0.640, 0.066, 0.120),
    ]
    for x, y, w, h in dec:
        _slab(ax, x, y, w, h, block_name, decoder=True, volume=volume)
    for cx, cy in concat:
        C.op(ax, cx, cy, "C", r=0.024, edge=C.NAVY)

    _edge_operator(ax, (bottleneck[0] + bottleneck[2], bottleneck[1] + 0.045),
                   (0.545, 0.325), (concat[0][0], concat[0][1] - 0.026),
                   "↑2", color=C.CORAL)
    for i in range(1, 3):
        px, py, pw, ph = dec[i - 1]
        cx, cy = concat[i]
        _edge_operator(ax, (px + pw, py + ph / 2),
                       ((px + pw + cx) / 2, (py + ph / 2 + cy) / 2),
                       (cx, cy - 0.026), "↑2", color=C.CORAL)
    for (cx, cy), (dx, dy, _, dh) in zip(concat, dec):
        C.arrow(ax, (cx + 0.026, cy), (dx, dy + dh / 2), color=C.CORAL)

    for i, (ex, ey, ew, eh) in enumerate(enc):
        cx, cy = concat[2 - i]
        C.arrow(ax, (ex + ew / 2, ey + eh), (cx, cy + 0.026),
                color=C.NAVY, lw=0.82,
                connection=f"arc3,rad={-0.12 - 0.025 * i}")

    C.label_box(ax, 0.870, 0.665, 0.045, 0.070,
                "1×1\nConv", face=C.PALE_GRAY, edge=C.GRAY, fontsize=7.0)
    C.arrow(ax, (dec[-1][0] + dec[-1][2], 0.700), (0.870, 0.700),
            color=C.CORAL)
    _output_overlay(ax, 0.925, 0.625, 0.055, 0.155,
                    "3-D mask" if volume else "voxelwise mask", volume=volume)
    C.arrow(ax, (0.915, 0.700), (0.925, 0.700), color=C.CORAL)

    ax.text(0.515, 0.930,
            "↓2 = explicit downsample   ·   ↑2 = explicit upsample   ·   C = channel Concat",
            ha="center", va="center", fontsize=7.5, color=C.INK)
    if residual:
        C.rounded_panel(ax, 0.105, 0.002, 0.355, 0.178,
                        face=C.OFF_WHITE, edge=C.GRID, radius=0.012)
        ax.text(0.445, 0.157, "short residual Add", ha="right", va="top",
                fontsize=7.0, weight="bold", color=C.NAVY)
        ax.text(0.138, 0.070, "x", ha="center", va="center", fontsize=7.6,
                weight="bold")
        C.label_box(ax, 0.185, 0.045, 0.105, 0.050, "Fθ(x)",
                    face=C.PALE_BLUE, edge=C.BLUE, fontsize=7.4)
        C.label_box(ax, 0.185, 0.102, 0.105, 0.030,
                    "identity / projection*", face=C.WHITE,
                    edge=C.GRAY, fontsize=6.9)
        C.op(ax, 0.340, 0.070, "+", r=0.019, edge=C.CORAL)
        C.arrow(ax, (0.151, 0.070), (0.185, 0.070), color=C.BLUE)
        C.arrow(ax, (0.290, 0.070), (0.320, 0.070), color=C.BLUE)
        C.arrow(ax, (0.151, 0.079), (0.185, 0.117), color=C.GRAY,
                connection="arc3,rad=-0.20")
        C.arrow(ax, (0.290, 0.117), (0.340, 0.090), color=C.GRAY,
                connection="arc3,rad=-0.15")
        C.arrow(ax, (0.359, 0.070), (0.405, 0.070), color=C.CORAL)
        ax.text(0.415, 0.070, "y", ha="left", va="center", fontsize=7.6,
                weight="bold")
        ax.text(0.282, 0.012, "*1×1 projection only when shape/channels differ",
                ha="center", va="bottom", fontsize=6.9, color=C.GRAY)
        C.link(ax, (0.452, 0.175), (enc[1][0] + 0.025, enc[1][1]),
               color=C.GRAY, style="--", connection="arc3,rad=-0.18")


def build_fig04() -> None:
    title = "U-Net families: dimensionality, skip fusion, and residual learning"
    fig, axes = plt.subplots(3, 1, figsize=(C.FIGURE_WIDTH_IN, 7.85))
    fig.subplots_adjust(left=0.025, right=0.985, top=0.940, bottom=0.035,
                        hspace=0.075)
    fig.suptitle(title, y=0.987, fontsize=11.2, weight="bold", color=C.INK)
    _draw_unet(axes[0], "(a)", "U-Net", dimension="2-D")
    _draw_unet(axes[1], "(b)", "3D U-Net", dimension="3-D")
    _draw_unet(axes[2], "(c)", "Residual U-Net", dimension="2-D", residual=True)
    C.save(
        fig, "fig04_unet_3d_residual", title,
        ["U-Net", "3D U-Net", "Residual U-Net"],
        assertions=[
            "Every encoder transition has an explicit downsample and every decoder transition an explicit upsample.",
            "Each long-skip C node receives a matching-resolution encoder feature and an upsampled decoder feature before decoder convolution.",
            "The 3D panel labels volumetric input, 3-D operations, and a 3-D mask.",
            "The residual magnifier separates short element-wise Add from long channel Concat and conditionally uses projection only for shape mismatch.",
        ],
    )


def _dense_panel(ax: Axes) -> None:
    C.schema(ax)
    C.heading(ax, "(a)", "Dense U-Net: dense-block magnifier and decoder fusion")
    _image_anchor(ax, _feature(0, 1), 0.012, 0.39, 0.125, 0.40,
                  "multiscale feature anchor")
    _slab(ax, 0.165, 0.585, 0.045, 0.105, r"$x_0$")
    C.arrow(ax, (0.137, 0.600), (0.165, 0.635), color=C.BLUE)

    x_starts = [0.390, 0.600, 0.810]
    c_centers = [0.285, 0.495, 0.705]
    h_starts = [0.315, 0.525, 0.735]
    source_centers = [(0.1875, 0.6375)]
    for layer, (cx, hx, xx) in enumerate(zip(c_centers, h_starts, x_starts), 1):
        C.op(ax, cx, 0.637, "C", r=0.022, edge=C.NAVY)
        C.label_box(ax, hx, 0.605, 0.060, 0.064, f"H{layer}",
                    face=C.PALE_GRAY, edge=C.GRAY, fontsize=7.6, weight="bold")
        _slab(ax, xx, 0.585, 0.045, 0.105, rf"$x_{layer}$")
        C.arrow(ax, (cx + 0.022, 0.637), (hx, 0.637), color=C.NAVY)
        C.arrow(ax, (hx + 0.060, 0.637), (xx, 0.637), color=C.BLUE)
        for j, src in enumerate(source_centers):
            C.arrow(ax, (src[0], 0.692), (cx, 0.659), color=C.NAVY,
                    lw=0.72, connection=f"arc3,rad={-0.14 - 0.055 * j}")
        source_centers.append((xx + 0.0225, 0.6375))
    ax.text(0.555, 0.805,
            r"$x_l=H_l(\mathrm{Concat}[x_0,\ldots,x_{l-1}])$; dense links concatenate, never add",
            ha="center", va="center", fontsize=7.8, color=C.NAVY)

    ax.text(0.310, 0.310, "representative U-shaped decoder fusion",
            ha="center", fontsize=7.5, weight="bold", color=C.INK)
    _slab(ax, 0.175, 0.205, 0.090, 0.085, "dense encoder\nskip")
    _slab(ax, 0.175, 0.075, 0.090, 0.085, "upsampled\ndecoder", decoder=True)
    C.op(ax, 0.355, 0.185, "C", r=0.024, edge=C.NAVY)
    C.arrow(ax, (0.265, 0.247), (0.335, 0.200), color=C.BLUE)
    C.arrow(ax, (0.265, 0.117), (0.335, 0.170), color=C.CORAL)
    C.label_box(ax, 0.405, 0.130, 0.145, 0.110, "Dense decoder\nblock",
                face=C.PALE_CORAL, edge=C.CORAL, fontsize=7.6)
    C.arrow(ax, (0.379, 0.185), (0.405, 0.185), color=C.CORAL)
    _output_overlay(ax, 0.590, 0.105, 0.080, 0.155, "prediction")
    C.arrow(ax, (0.550, 0.185), (0.590, 0.185), color=C.CORAL)
    C.rounded_panel(ax, 0.715, 0.075, 0.250, 0.225,
                    face=C.OFF_WHITE, edge=C.GRID)
    ax.text(0.840, 0.270, "Operator audit", ha="center", va="center",
            fontsize=7.7, weight="bold", color=C.NAVY)
    ax.text(0.840, 0.165,
            "Dense: all preceding " + r"$x_j$" + " → C → " + r"$H_l$" + "\n"
            "U-shaped: encoder skip + decoder → C\n"
            "No element-wise Add",
            ha="center", va="center", fontsize=7.0, linespacing=1.25)


def _attention_panel(ax: Axes) -> None:
    C.schema(ax)
    C.heading(ax, "(b)", "Attention U-Net: additive attention-gated skip")
    _image_anchor(ax, _feature(2, 0), 0.012, 0.35, 0.140, 0.47,
                  "spatial-attention anchor")

    _slab(ax, 0.190, 0.690, 0.085, 0.100, "encoder feature\n" + r"$x^l$")
    _slab(ax, 0.190, 0.400, 0.085, 0.100, "decoder\ngate g", decoder=True)
    C.label_box(ax, 0.335, 0.700, 0.100, 0.080, "Wₓ: 1×1\nprojection",
                face=C.PALE_BLUE_2, edge=C.BLUE, fontsize=7.4)
    C.label_box(ax, 0.335, 0.410, 0.100, 0.080, "Wg: 1×1\nprojection",
                face=C.PALE_CORAL_2, edge=C.CORAL, fontsize=7.4)
    C.arrow(ax, (0.275, 0.740), (0.335, 0.740), color=C.BLUE)
    C.arrow(ax, (0.275, 0.450), (0.335, 0.450), color=C.CORAL)
    C.op(ax, 0.515, 0.590, "+", r=0.024, edge=C.GRAY)
    C.arrow(ax, (0.435, 0.740), (0.493, 0.605), color=C.BLUE,
            connection="arc3,rad=0.08")
    C.arrow(ax, (0.435, 0.450), (0.493, 0.575), color=C.CORAL,
            connection="arc3,rad=-0.08")
    C.label_box(ax, 0.560, 0.535, 0.145, 0.110,
                "ReLU → ψ: 1×1\n→ sigmoid",
                face=C.PALE_GRAY, edge=C.GRAY, fontsize=7.5)
    C.arrow(ax, (0.539, 0.590), (0.560, 0.590), color=C.GRAY)
    C.label_box(ax, 0.735, 0.555, 0.055, 0.070, r"$\alpha$",
                face=C.WHITE, edge=C.NAVY, fontsize=8.2, weight="bold")
    C.arrow(ax, (0.705, 0.590), (0.735, 0.590), color=C.NAVY)
    C.op(ax, 0.825, 0.710, r"$\odot$", r=0.025, edge=C.NAVY)
    C.arrow(ax, (0.790, 0.590), (0.817, 0.686), color=C.NAVY,
            connection="arc3,rad=-0.10")
    C.arrow(ax, (0.232, 0.790), (0.825, 0.735), color=C.BLUE,
            connection="arc3,rad=-0.14")
    _slab(ax, 0.870, 0.660, 0.075, 0.100,
          "gated skip\n" + r"$\alpha\odot x^l$")
    C.arrow(ax, (0.850, 0.710), (0.870, 0.710), color=C.BLUE)

    _slab(ax, 0.555, 0.235, 0.105, 0.095, "upsampled\ndecoder d", decoder=True)
    C.op(ax, 0.790, 0.310, "C", r=0.025, edge=C.NAVY)
    C.arrow(ax, (0.660, 0.282), (0.767, 0.299), color=C.CORAL)
    C.arrow(ax, (0.907, 0.660), (0.798, 0.333), color=C.BLUE,
            connection="arc3,rad=0.10")
    C.label_box(ax, 0.835, 0.250, 0.125, 0.120, "decoder\nconvolution",
                face=C.PALE_CORAL, edge=C.CORAL, fontsize=7.6)
    C.arrow(ax, (0.815, 0.310), (0.835, 0.310), color=C.CORAL)
    ax.text(0.610, 0.135,
            r"$+$ = element-wise Add   ·   $\odot$ = element-wise Multiply   ·   C = channel Concat",
            ha="center", fontsize=7.5, color=C.INK)
    ax.text(0.610, 0.075,
            r"$W_xx^l$ and $W_gg$ are spatially aligned before Add; $\alpha$ gates $x^l$, not $g$",
            ha="center", fontsize=7.4, color=C.NAVY)


def _nnunet_panel(ax: Axes) -> None:
    C.schema(ax)
    C.heading(ax, "(c)", "nnU-Net: data-driven experiment planning and locked inference")
    _image_anchor(ax, _feature(0, 0), 0.012, 0.43, 0.105, 0.38,
                  "training dataset")
    C.label_box(ax, 0.145, 0.635, 0.135, 0.135,
                "Dataset fingerprint\nspacing · shape\nmodality · labels",
                face=C.PALE_BLUE, edge=C.BLUE, fontsize=7.3)
    C.arrow(ax, (0.117, 0.635), (0.145, 0.695), color=C.BLUE)
    C.label_box(ax, 0.320, 0.635, 0.145, 0.135,
                "Rule-based planning\ntarget spacing · patch\nbatch · kernels",
                face=C.PALE_GRAY, edge=C.GRAY, fontsize=7.3)
    C.arrow(ax, (0.280, 0.702), (0.320, 0.702), color=C.NAVY)
    C.label_box(ax, 0.505, 0.650, 0.125, 0.105,
                "Applied\npreprocessing",
                face=C.PALE_GRAY, edge=C.GRAY, fontsize=7.5)
    C.arrow(ax, (0.465, 0.702), (0.505, 0.702), color=C.GRAY)

    candidates = [
        (0.500, 0.405, 0.120, 0.130, "2-D U-Net\ncandidate"),
        (0.650, 0.405, 0.135, 0.130, "3-D full-res\ncandidate"),
    ]
    for x, y, w, h, text in candidates:
        C.label_box(ax, x, y, w, h, text, face=C.PALE_BLUE,
                    edge=C.BLUE, fontsize=7.5)
        C.arrow(ax, (0.565, 0.650), (x + w / 2, y + h), color=C.BLUE,
                connection="arc3,rad=0.08")

    C.rounded_panel(ax, 0.815, 0.370, 0.170, 0.205,
                    face=C.PALE_BLUE_2, edge=C.BLUE, radius=0.012)
    ax.text(0.900, 0.548, "3-D cascade candidate", ha="center", va="center",
            fontsize=7.5, weight="bold", color=C.NAVY)
    C.label_box(ax, 0.830, 0.475, 0.060, 0.045, "low-res",
                face=C.WHITE, edge=C.BLUE, fontsize=6.9)
    C.label_box(ax, 0.910, 0.475, 0.060, 0.045, "↑ coarse\nseg.",
                face=C.WHITE, edge=C.GRAY, fontsize=6.5)
    C.label_box(ax, 0.865, 0.395, 0.075, 0.050, "full-res\nmodel",
                face=C.WHITE, edge=C.BLUE, fontsize=6.9)
    C.arrow(ax, (0.890, 0.498), (0.910, 0.498), color=C.BLUE)
    C.arrow(ax, (0.940, 0.475), (0.902, 0.445), color=C.BLUE,
            connection="arc3,rad=0.10")
    C.arrow(ax, (0.630, 0.702), (0.865, 0.575), color=C.BLUE,
            connection="arc3,rad=-0.08")
    ax.text(0.741, 0.600, "feasible candidate plans",
            ha="center", fontsize=7.4, color=C.NAVY)

    C.label_box(ax, 0.455, 0.205, 0.250, 0.105,
                "Default five-fold cross-validation\nout-of-fold predictions",
                face=C.PALE_GRAY, edge=C.GRAY, fontsize=7.4)
    for x, y, w, _, _ in candidates:
        C.arrow(ax, (x + w / 2, y), (0.550, 0.310), color=C.GRAY,
                connection="arc3,rad=-0.10")
    C.arrow(ax, (0.900, 0.370), (0.660, 0.310), color=C.GRAY,
            connection="arc3,rad=0.12")
    C.label_box(ax, 0.735, 0.210, 0.230, 0.095,
                "Select configuration; ensemble\nonly if validation supports it",
                face=C.PALE_CORAL_2, edge=C.CORAL, fontsize=7.3)
    C.arrow(ax, (0.705, 0.257), (0.735, 0.257), color=C.CORAL)
    C.label_box(ax, 0.735, 0.075, 0.230, 0.085,
                "Retain postprocessing only if CV improves it",
                face=C.PALE_CORAL_2, edge=C.CORAL, fontsize=7.2)
    C.arrow(ax, (0.850, 0.210), (0.850, 0.160), color=C.CORAL)
    C.label_box(ax, 0.475, 0.060, 0.190, 0.085,
                "Locked inference\nconfiguration",
                face=C.PALE_CORAL, edge=C.CORAL, fontsize=7.5)
    C.arrow(ax, (0.735, 0.117), (0.665, 0.102), color=C.CORAL)
    _output_overlay(ax, 0.355, 0.045, 0.075, 0.125, "test prediction")
    C.arrow(ax, (0.475, 0.102), (0.430, 0.108), color=C.CORAL)
    ax.plot([0.690, 0.690], [0.035, 0.185], color=C.CORAL, lw=0.8,
            linestyle="--", zorder=2)
    ax.text(0.690, 0.025, "unseen test: no feedback to planning",
            ha="center", va="top", fontsize=7.2, color=C.CORAL)


def build_fig05() -> None:
    title = "Dense, attention-gated, and self-configuring U-Net mechanisms"
    fig, axes = plt.subplots(3, 1, figsize=(C.FIGURE_WIDTH_IN, 8.05))
    fig.subplots_adjust(left=0.025, right=0.985, top=0.940, bottom=0.025,
                        hspace=0.075)
    fig.suptitle(title, y=0.987, fontsize=11.2, weight="bold", color=C.INK)
    _dense_panel(axes[0])
    _attention_panel(axes[1])
    _nnunet_panel(axes[2])
    C.save(
        fig, "fig05_dense_attention_nnunet", title,
        ["Dense U-Net", "Attention U-Net", "nnU-Net"],
        assertions=[
            "Every dense-layer Concat has all preceding feature operands, an output into H_l, and a labeled x_l output.",
            "The attention gate shows aligned encoder and gating projections, additive coefficient estimation, multiplication of alpha with x_l, then Concat with the decoder stream.",
            "nnU-Net is represented as fingerprinting, planning, applied preprocessing, feasible candidate evaluation, validation-based selection, optional validated postprocessing, and locked inference.",
            "The cascade candidate explicitly passes an upsampled low-resolution segmentation to a full-resolution model; the unseen test set provides no feedback.",
        ],
    )


def _preln_block(ax: Axes, x: float, y: float, w: float, h: float,
                 attention: str) -> tuple[float, float]:
    """Draw a two-row pre-LN Transformer block with explicit residual Adds."""
    C.rounded_panel(ax, x, y, w, h, face=C.PALE_GRAY, edge=C.GRAY,
                    radius=0.012, lw=0.8, zorder=1)
    row1 = y + h * 0.68
    row2 = y + h * 0.30
    ln_w = w * 0.105
    att_w = w * 0.260
    ln1_x = x + w * 0.095
    att_x = x + w * 0.285
    add1_x = x + w * 0.760
    ln2_x = x + w * 0.095
    mlp_x = x + w * 0.315
    add2_x = x + w * 0.760
    C.label_box(ax, ln1_x, row1 - h * 0.105, ln_w, h * 0.21, "LN",
                face=C.WHITE, edge=C.GRAY, fontsize=7.3)
    C.label_box(ax, att_x, row1 - h * 0.105, att_w, h * 0.21, attention,
                face=C.WHITE, edge=C.GRAY, fontsize=7.2)
    C.op(ax, add1_x, row1, "+", r=min(0.018, h * 0.085), edge=C.NAVY,
         fontsize=7.7)
    C.label_box(ax, ln2_x, row2 - h * 0.105, ln_w, h * 0.21, "LN",
                face=C.WHITE, edge=C.GRAY, fontsize=7.3)
    C.label_box(ax, mlp_x, row2 - h * 0.105, w * 0.205, h * 0.21, "MLP",
                face=C.WHITE, edge=C.GRAY, fontsize=7.3)
    C.op(ax, add2_x, row2, "+", r=min(0.018, h * 0.085), edge=C.NAVY,
         fontsize=7.7)

    in1 = (x + w * 0.025, row1)
    C.arrow(ax, in1, (ln1_x, row1), color=C.INK, lw=0.72)
    C.arrow(ax, (ln1_x + ln_w, row1), (att_x, row1), color=C.INK, lw=0.72)
    C.arrow(ax, (att_x + att_w, row1), (add1_x - 0.020, row1),
            color=C.INK, lw=0.72)
    C.arrow(ax, (in1[0], row1 + h * 0.06), (add1_x, row1 + 0.020),
            color=C.NAVY, lw=0.72, connection="arc3,rad=-0.22")
    C.arrow(ax, (add1_x + 0.020, row1),
            (ln2_x, row2), color=C.INK, lw=0.72,
            connection="arc3,rad=0.12")
    C.arrow(ax, (ln2_x + ln_w, row2), (mlp_x, row2), color=C.INK, lw=0.72)
    C.arrow(ax, (mlp_x + w * 0.205, row2), (add2_x - 0.020, row2),
            color=C.INK, lw=0.72)
    C.arrow(ax, (add1_x + 0.020, row1 - h * 0.03),
            (add2_x, row2 + 0.020), color=C.NAVY, lw=0.72,
            connection="arc3,rad=0.25")
    C.arrow(ax, (add2_x + 0.020, row2), (x + w * 0.965, row2),
            color=C.INK, lw=0.72)
    return x + w * 0.965, row2


def _window_grid(ax: Axes, x: float, y: float, s: float, *, shifted: bool) -> None:
    ax.add_patch(Rectangle((x, y), s, s, facecolor=C.WHITE,
                           edgecolor=C.NAVY, linewidth=0.85, zorder=3))
    for i in range(1, 8):
        ax.plot([x + i * s / 8] * 2, [y, y + s], color=C.GRID,
                lw=0.38, zorder=4)
        ax.plot([x, x + s], [y + i * s / 8] * 2, color=C.GRID,
                lw=0.38, zorder=4)
    if shifted:
        for p in (s / 4, 3 * s / 4):
            ax.plot([x + p] * 2, [y, y + s], color=C.NAVY, lw=0.9,
                    linestyle="--", zorder=5)
            ax.plot([x, x + s], [y + p] * 2, color=C.NAVY, lw=0.9,
                    linestyle="--", zorder=5)
        band = s / 8
        for rx, ry, rw, rh in [
            (x, y, s, band), (x, y + s - band, s, band),
            (x, y, band, s), (x + s - band, y, band, s),
        ]:
            ax.add_patch(Rectangle((rx, ry), rw, rh, facecolor=C.PALE_CORAL,
                                   edgecolor="none", alpha=0.52, zorder=3.5))
    else:
        ax.plot([x + s / 2] * 2, [y, y + s], color=C.NAVY, lw=0.95, zorder=5)
        ax.plot([x, x + s], [y + s / 2] * 2, color=C.NAVY, lw=0.95, zorder=5)


def _patch_merge_inset(ax: Axes, x: float, y: float, w: float, h: float) -> None:
    C.rounded_panel(ax, x, y, w, h, face=C.OFF_WHITE, edge=C.GRID,
                    radius=0.010)
    cell = min(w * 0.13, h * 0.18)
    ox, oy = x + w * 0.08, y + h * 0.45
    colors = [C.PALE_BLUE, C.PALE_BLUE_2, C.PALE_CORAL_2, C.PALE_GRAY]
    for j in range(2):
        for i in range(2):
            ax.add_patch(Rectangle((ox + i * cell, oy + j * cell), cell, cell,
                                   facecolor=colors[j * 2 + i], edgecolor=C.BLUE,
                                   linewidth=0.6, zorder=4))
    C.arrow(ax, (ox + 2.2 * cell, oy + cell),
            (x + w * 0.52, oy + cell), color=C.GRAY, lw=0.72)
    C.label_box(ax, x + w * 0.54, y + h * 0.40, w * 0.18, h * 0.26,
                "Concat", face=C.WHITE, edge=C.GRAY, fontsize=7.0)
    C.arrow(ax, (x + w * 0.72, oy + cell),
            (x + w * 0.79, oy + cell), color=C.GRAY, lw=0.72)
    C.feature_slab(ax, x + w * 0.80, y + h * 0.39, w * 0.11, h * 0.28,
                   face=C.PALE_BLUE, edge=C.BLUE, depth=2)
    ax.text(x + w / 2, y + h * 0.15, "2×2 grouping → Concat → linear projection",
            ha="center", va="center", fontsize=7.1, color=C.INK)


def _vit_panel(ax: Axes) -> None:
    C.schema(ax)
    C.heading(ax, "(a)", "Vision Transformer: patch tokens and global self-attention")
    _image_anchor(ax, _feature(0, 0), 0.018, 0.515, 0.145, 0.385,
                  "2-D MRI patch example")
    C.label_box(ax, 0.200, 0.650, 0.115, 0.105,
                "nonoverlapping\npatches + flatten",
                face=C.PALE_BLUE, edge=C.BLUE, fontsize=7.5)
    C.arrow(ax, (0.163, 0.705), (0.200, 0.705), color=C.BLUE)
    C.label_box(ax, 0.350, 0.650, 0.105, 0.105, "linear\nprojection",
                face=C.PALE_BLUE_2, edge=C.BLUE, fontsize=7.5)
    C.arrow(ax, (0.315, 0.705), (0.350, 0.705), color=C.BLUE)
    token_end = C.token_strip(ax, 0.500, 0.682, 5, w=0.026, h=0.070,
                              gap=0.006, face=C.PALE_BLUE, edge=C.BLUE)
    pos_end = C.token_strip(ax, 0.500, 0.550, 5, w=0.026, h=0.055,
                            gap=0.006, face=C.PALE_GRAY, edge=C.GRAY)
    ax.text((0.500 + token_end) / 2, 0.765, "content tokens",
            ha="center", fontsize=7.3)
    ax.text((0.500 + pos_end) / 2, 0.520, "learned positional embeddings",
            ha="center", fontsize=7.3)
    C.arrow(ax, (0.455, 0.705), (0.500, 0.717), color=C.BLUE)
    C.op(ax, 0.700, 0.650, "+", r=0.025, edge=C.NAVY)
    C.arrow(ax, (token_end, 0.717), (0.678, 0.662), color=C.BLUE)
    C.arrow(ax, (pos_end, 0.578), (0.690, 0.628), color=C.GRAY)
    out_end = C.token_strip(ax, 0.755, 0.615, 5, w=0.026, h=0.070,
                            gap=0.006, face=C.PALE_BLUE, edge=C.NAVY)
    C.arrow(ax, (0.725, 0.650), (0.755, 0.650), color=C.NAVY)
    ax.text((0.755 + out_end) / 2, 0.720, "position-aware tokens",
            ha="center", fontsize=7.3, color=C.NAVY)

    token_mid = (0.755 + out_end) / 2
    # Route the token stream outside the mechanism magnifier so it cannot be
    # confused with either residual branch inside the pre-LN block.
    ax.plot([token_mid, token_mid, 0.215, 0.215],
            [0.615, 0.490, 0.490, 0.337], color=C.NAVY, lw=0.90,
            solid_capstyle="round", zorder=2.4)
    C.arrow(ax, (0.215, 0.337), (0.257, 0.337), color=C.NAVY)
    block_out = _preln_block(ax, 0.245, 0.170, 0.500, 0.245, "global MHSA")
    ax.text(0.495, 0.130, "pre-LN Transformer encoder block × L",
            ha="center", fontsize=7.8, weight="bold", color=C.NAVY)
    C.label_box(ax, 0.790, 0.205, 0.105, 0.135,
                "task head\nor dense decoder",
                face=C.PALE_CORAL, edge=C.CORAL, fontsize=7.4)
    C.arrow(ax, block_out, (0.790, 0.273), color=C.CORAL)
    _output_overlay(ax, 0.925, 0.190, 0.062, 0.165, "task output")
    C.arrow(ax, (0.895, 0.273), (0.925, 0.273), color=C.CORAL)
    ax.text(0.510, 0.050,
            "ViT is a token encoder; dense MS lesion prediction still requires spatial decoding",
            ha="center", fontsize=7.6, color=C.INK)


def _swin_panel(ax: Axes) -> None:
    C.schema(ax)
    C.heading(ax, "(b)", "Swin Transformer: shifted windows and hierarchical features")
    _window_grid(ax, 0.055, 0.590, 0.190, shifted=False)
    ax.text(0.150, 0.550, "W-MSA: nonoverlapping local windows",
            ha="center", fontsize=7.4, weight="bold", color=C.NAVY)
    _window_grid(ax, 0.365, 0.590, 0.190, shifted=True)
    ax.text(0.460, 0.550, "SW-MSA: cyclic shift M/2 + attention mask",
            ha="center", fontsize=7.4, weight="bold", color=C.NAVY)
    _patch_merge_inset(ax, 0.675, 0.575, 0.290, 0.235)
    ax.text(0.820, 0.835, "between stages: Patch Merging",
            ha="center", fontsize=7.4, weight="bold", color=C.NAVY)

    C.label_box(ax, 0.018, 0.225, 0.080, 0.105, "patch\nembedding",
                face=C.PALE_BLUE, edge=C.BLUE, fontsize=7.2)
    w_out = _preln_block(ax, 0.120, 0.155, 0.280, 0.235, "W-MSA")
    sw_out = _preln_block(ax, 0.445, 0.155, 0.280, 0.235, "SW-MSA")
    C.arrow(ax, (0.098, 0.278), (0.120, 0.315), color=C.BLUE)
    C.arrow(ax, w_out, (0.445, 0.315), color=C.NAVY)
    C.label_box(ax, 0.765, 0.225, 0.095, 0.105, "Patch\nMerging",
                face=C.PALE_GRAY, edge=C.GRAY, fontsize=7.2)
    C.arrow(ax, sw_out, (0.765, 0.278), color=C.NAVY)
    C.feature_slab(ax, 0.900, 0.205, 0.055, 0.145,
                   face=C.PALE_BLUE, edge=C.BLUE, depth=3,
                   label="stage\nl+1")
    C.arrow(ax, (0.860, 0.278), (0.900, 0.278), color=C.BLUE)
    C.link(ax, (0.150, 0.550), (0.260, 0.390), color=C.GRAY,
           style="--", connection="arc3,rad=-0.12")
    C.link(ax, (0.460, 0.550), (0.585, 0.390), color=C.GRAY,
           style="--", connection="arc3,rad=-0.12")
    C.link(ax, (0.820, 0.575), (0.812, 0.330), color=C.GRAY,
           style="--", connection="arc3,rad=0.05")
    ax.text(0.420, 0.090, "stage l: alternating local-window blocks enable cross-window exchange",
            ha="center", fontsize=7.5, color=C.INK)
    ax.text(0.840, 0.090, "↓ spatial resolution\n↑ feature channels",
            ha="center", va="center", fontsize=7.3, color=C.NAVY)


def build_fig06() -> None:
    title = "Transformer mechanisms for MRI representation and segmentation"
    fig, axes = plt.subplots(2, 1, figsize=(C.FIGURE_WIDTH_IN, 6.55))
    fig.subplots_adjust(left=0.025, right=0.985, top=0.930, bottom=0.035,
                        hspace=0.105)
    fig.suptitle(title, y=0.985, fontsize=11.2, weight="bold", color=C.INK)
    _vit_panel(axes[0])
    _swin_panel(axes[1])
    C.save(
        fig, "fig06_vit_swin", title,
        ["Vision Transformer", "Swin Transformer"],
        assertions=[
            "ViT explicitly adds positional embeddings to projected patch tokens and uses two pre-LN residual Add operations per block.",
            "The ViT panel distinguishes a token encoder from its task-specific head or dense decoder.",
            "Swin alternates W-MSA and SW-MSA within a stage; shifted windows show a half-window cyclic shift and masked wrap regions.",
            "Patch Merging appears between stages and groups neighboring tokens before concatenation and linear projection.",
        ],
    )


def _skip_transform(ax: Axes, x: float, y: float, label: str) -> tuple[float, float]:
    C.label_box(ax, x, y, 0.090, 0.095,
                f"{label}\nreshape · project\n· upsample",
                face=C.PALE_BLUE_2, edge=C.BLUE, fontsize=6.9)
    return x + 0.090, y + 0.0475


def _unetr_panel(ax: Axes) -> None:
    C.schema(ax)
    C.heading(ax, "(a)", "UNETR: volumetric tokens and multidepth Transformer skips")
    _image_anchor(ax, _feature(1, 0), 0.012, 0.455, 0.115, 0.385,
                  "3-D MRI volume")
    C.label_box(ax, 0.155, 0.590, 0.110, 0.135,
                "nonoverlapping\n3-D patches\n+ linear embedding",
                face=C.PALE_BLUE, edge=C.BLUE, fontsize=7.3)
    C.arrow(ax, (0.127, 0.650), (0.155, 0.657), color=C.BLUE)

    C.rounded_panel(ax, 0.305, 0.235, 0.125, 0.575,
                    face=C.PALE_GRAY, edge=C.GRAY, radius=0.012)
    ax.text(0.3675, 0.785, "Transformer encoder",
            ha="center", va="center", fontsize=7.6, weight="bold", color=C.NAVY)
    states = [
        ("z3", r"$z^3$", 0.675),
        ("z6", r"$z^6$", 0.555),
        ("z9", r"$z^9$", 0.435),
        ("z12", r"$z^{12}$", 0.315),
    ]
    for _, display, yy in states:
        C.label_box(ax, 0.325, yy - 0.038, 0.085, 0.076, display,
                    face=C.WHITE, edge=C.GRAY, fontsize=8.0, weight="bold")
    C.arrow(ax, (0.265, 0.657), (0.325, 0.700), color=C.NAVY)
    for (_, _, y0), (_, _, y1) in zip(states[:-1], states[1:]):
        C.arrow(ax, (0.3675, y0 - 0.038), (0.3675, y1 + 0.038),
                color=C.INK, lw=0.75)
    ax.text(0.3675, 0.265, "token depth 1 → L",
            ha="center", fontsize=7.1, color=C.GRAY)

    # Raw input reaches the highest-resolution decoder only through a shallow CNN stem.
    C.label_box(ax, 0.500, 0.785, 0.120, 0.090, "3-D shallow\nCNN stem",
                face=C.PALE_BLUE, edge=C.BLUE, fontsize=7.3)
    C.arrow(ax, (0.080, 0.840), (0.500, 0.830), color=C.BLUE,
            connection="arc3,rad=-0.08")

    transform_positions = [
        (0.460, 0.628, "z3", r"$z^3$"),
        (0.460, 0.508, "z6", r"$z^6$"),
        (0.460, 0.388, "z9", r"$z^9$"),
    ]
    transform_outputs: dict[str, tuple[float, float]] = {}
    state_y = {key: yy for key, _, yy in states}
    for tx, ty, key, display in transform_positions:
        out = _skip_transform(ax, tx, ty, display)
        transform_outputs[key] = out
        C.arrow(ax, (0.410, state_y[key]), (tx, ty + 0.0475),
                color=C.BLUE)
    C.label_box(ax, 0.460, 0.245, 0.100, 0.095,
                r"$z^{12}$" + "\nreshape · project",
                face=C.PALE_BLUE_2, edge=C.BLUE, fontsize=7.0)
    C.arrow(ax, (0.410, state_y["z12"]), (0.460, 0.292), color=C.BLUE)

    concat = [(0.585, 0.370), (0.685, 0.500), (0.785, 0.630), (0.875, 0.765)]
    decoder = [
        (0.615, 0.322, 0.055, 0.096),
        (0.715, 0.452, 0.055, 0.096),
        (0.815, 0.582, 0.055, 0.096),
        (0.905, 0.717, 0.050, 0.096),
    ]
    for cx, cy in concat:
        C.op(ax, cx, cy, "C", r=0.021, edge=C.NAVY, fontsize=7.6)
    for x, y, w, h in decoder:
        _slab(ax, x, y, w, h, "3-D CNN\ndecode", decoder=True, volume=True)
    # z12 initializes the deepest decoder stream through an explicit upsample.
    _edge_operator(ax, (0.560, 0.292), (0.572, 0.330),
                   (concat[0][0], concat[0][1] - 0.023), "↑2", color=C.CORAL)
    # z9, z6, z3 enter progressively higher decoder resolutions.
    for key, idx in [("z9", 0), ("z6", 1), ("z3", 2)]:
        out = transform_outputs[key]
        C.arrow(ax, out, (concat[idx][0], concat[idx][1] + 0.023),
                color=C.BLUE, connection="arc3,rad=-0.06")
    C.arrow(ax, (0.620, 0.830), (concat[3][0], concat[3][1] + 0.023),
            color=C.BLUE, connection="arc3,rad=-0.08")
    for (cx, cy), (dx, dy, _, dh) in zip(concat, decoder):
        C.arrow(ax, (cx + 0.021, cy), (dx, dy + dh / 2), color=C.CORAL)
    for i in range(1, 4):
        px, py, pw, ph = decoder[i - 1]
        cx, cy = concat[i]
        _edge_operator(ax, (px + pw, py + ph / 2),
                       ((px + pw + cx) / 2, (py + ph / 2 + cy) / 2),
                       (cx, cy - 0.023), "↑2", color=C.CORAL)

    C.label_box(ax, 0.958, 0.730, 0.032, 0.070, "1×1\nConv",
                face=C.PALE_GRAY, edge=C.GRAY, fontsize=6.2)
    C.arrow(ax, (decoder[-1][0] + decoder[-1][2], 0.765),
            (0.958, 0.765), color=C.CORAL)
    ax.add_patch(Polygon([(0.992, 0.730), (0.998, 0.743), (0.996, 0.778),
                          (0.989, 0.794), (0.984, 0.770), (0.985, 0.744)],
                         closed=True, facecolor=C.PALE_CORAL, edgecolor=C.CORAL,
                         linewidth=0.8, zorder=6))
    C.arrow(ax, (0.990, 0.765), (0.994, 0.765), color=C.CORAL, scale=6.5)
    ax.text(0.980, 0.705, "3-D mask", ha="center", va="top",
            fontsize=6.9, color=C.CORAL)
    ax.text(0.665, 0.145,
            "Every hidden state is reshaped to a spatial tensor and projected before channel Concat",
            ha="center", fontsize=7.5, color=C.INK)
    ax.text(0.665, 0.090,
            r"$z^{12}$ initializes decoding; $z^9\rightarrow z^6\rightarrow z^3$ → shallow CNN stem restore progressively finer detail",
            ha="center", fontsize=7.4, color=C.NAVY)


def _transunet_panel(ax: Axes) -> None:
    C.schema(ax)
    C.heading(ax, "(b)", "Representative CNN–Transformer hybrid: TransUNet")
    _image_anchor(ax, _mri(2, 0), 0.012, 0.470, 0.100, 0.340,
                  "2-D MRI input")
    enc = [
        (0.145, 0.685, 0.065, 0.100, r"$f^1$"),
        (0.245, 0.555, 0.058, 0.090, r"$f^2$"),
        (0.335, 0.435, 0.052, 0.082, r"$f^3$"),
        (0.415, 0.325, 0.047, 0.074, r"$f^4$"),
    ]
    C.arrow(ax, (0.112, 0.645), (enc[0][0], enc[0][1] + 0.050), color=C.BLUE)
    for x, y, w, h, text in enc:
        _slab(ax, x, y, w, h, f"CNN\n{text}")
    for i in range(3):
        sx, sy, sw, sh, _ = enc[i]
        ex, ey, _, eh, _ = enc[i + 1]
        _edge_operator(ax, (sx + sw, sy + sh / 2),
                       ((sx + sw + ex) / 2, (sy + sh / 2 + ey + eh / 2) / 2),
                       (ex, ey + eh / 2), "↓2", color=C.BLUE)
    ax.text(0.285, 0.820, "local multiscale CNN features",
            ha="center", fontsize=7.5, color=C.NAVY)

    C.label_box(ax, 0.485, 0.315, 0.090, 0.090,
                "tokenize " + r"$f^4$" + "\n+ linear map",
                face=C.PALE_BLUE_2, edge=C.BLUE, fontsize=7.1)
    C.arrow(ax, (0.462, 0.362), (0.485, 0.360), color=C.BLUE)
    token_end = C.token_strip(ax, 0.595, 0.342, 4, w=0.022, h=0.060,
                              gap=0.005, face=C.PALE_BLUE, edge=C.BLUE)
    pos_end = C.token_strip(ax, 0.595, 0.250, 4, w=0.022, h=0.045,
                            gap=0.005, face=C.PALE_GRAY, edge=C.GRAY)
    C.arrow(ax, (0.575, 0.360), (0.595, 0.372), color=C.BLUE)
    C.op(ax, 0.720, 0.330, "+", r=0.021, edge=C.NAVY)
    C.arrow(ax, (token_end, 0.372), (0.700, 0.340), color=C.BLUE)
    C.arrow(ax, (pos_end, 0.272), (0.710, 0.310), color=C.GRAY)
    C.label_box(ax, 0.755, 0.250, 0.105, 0.160,
                "Transformer\nencoder\n(global context)",
                face=C.PALE_GRAY, edge=C.GRAY, fontsize=7.3)
    C.arrow(ax, (0.741, 0.330), (0.755, 0.330), color=C.NAVY)
    C.label_box(ax, 0.875, 0.265, 0.090, 0.120,
                "reshape\nspatial feature",
                face=C.PALE_CORAL_2, edge=C.CORAL, fontsize=7.2)
    C.arrow(ax, (0.860, 0.330), (0.875, 0.325), color=C.CORAL)

    concat = [(0.725, 0.475), (0.815, 0.600), (0.900, 0.725)]
    decoder = [
        (0.752, 0.430, 0.050, 0.090),
        (0.842, 0.555, 0.050, 0.090),
        (0.927, 0.680, 0.045, 0.090),
    ]
    for cx, cy in concat:
        C.op(ax, cx, cy, "C", r=0.020, edge=C.NAVY, fontsize=7.3)
    for x, y, w, h in decoder:
        _slab(ax, x, y, w, h, "CNN\ndecode", decoder=True)
    _edge_operator(ax, (0.920, 0.385), (0.815, 0.410),
                   (concat[0][0], concat[0][1] - 0.022), "↑2", color=C.CORAL)
    for skip_idx, concat_idx in [(2, 0), (1, 1), (0, 2)]:
        sx, sy, sw, sh, _ = enc[skip_idx]
        cx, cy = concat[concat_idx]
        C.arrow(ax, (sx + sw / 2, sy + sh), (cx, cy + 0.022),
                color=C.NAVY, lw=0.78,
                connection=f"arc3,rad={-0.12 - 0.02 * concat_idx}")
    for (cx, cy), (dx, dy, _, dh) in zip(concat, decoder):
        C.arrow(ax, (cx + 0.020, cy), (dx, dy + dh / 2), color=C.CORAL)
    for i in range(1, 3):
        px, py, pw, ph = decoder[i - 1]
        cx, cy = concat[i]
        _edge_operator(ax, (px + pw, py + ph / 2),
                       ((px + pw + cx) / 2, (py + ph / 2 + cy) / 2),
                       (cx, cy - 0.022), "↑2", color=C.CORAL)
    ax.add_patch(Polygon([(0.979, 0.690), (0.991, 0.700), (0.994, 0.735),
                          (0.986, 0.758), (0.977, 0.740)],
                         closed=True, facecolor=C.PALE_CORAL, edgecolor=C.CORAL,
                         linewidth=0.8, zorder=6))
    C.arrow(ax, (decoder[-1][0] + decoder[-1][2], 0.725),
            (0.979, 0.725), color=C.CORAL, scale=6.5)
    ax.text(0.975, 0.665, "mask", ha="center", fontsize=6.9, color=C.CORAL)
    ax.text(0.565, 0.135,
            r"CNN feature extraction precedes tokenization; retained $f^3/f^2/f^1$ skips restore local detail",
            ha="center", fontsize=7.5, color=C.INK)
    ax.text(0.565, 0.080,
            "C = channel Concat of a shape-aligned CNN skip and an upsampled decoder feature",
            ha="center", fontsize=7.4, color=C.NAVY)


def build_fig07() -> None:
    title = "Transformer–decoder integration patterns in 3-D and hybrid segmentation"
    fig, axes = plt.subplots(2, 1, figsize=(C.FIGURE_WIDTH_IN, 6.85))
    fig.subplots_adjust(left=0.025, right=0.988, top=0.930, bottom=0.030,
                        hspace=0.085)
    fig.suptitle(title, y=0.985, fontsize=11.2, weight="bold", color=C.INK)
    _unetr_panel(axes[0])
    _transunet_panel(axes[1])
    C.save(
        fig, "fig07_unetr_transunet", title,
        ["UNETR", "TransUNet"],
        assertions=[
            "UNETR accepts a 3-D volume, tokenizes nonoverlapping 3-D patches, and sends z12, z9, z6, z3, and a shallow CNN stem to progressively finer decoder stages.",
            "Every UNETR hidden-state skip is explicitly reshaped, projected, and upsampled as required before channel Concat.",
            "The TransUNet panel computes four scales of local CNN features before tokenizing the deepest feature and adding positional embeddings.",
            "TransUNet decodes reshaped Transformer context through three explicit fusion stages with retained higher-resolution CNN skips.",
        ],
    )


def _unfolding_panel(ax: Axes) -> None:
    C.schema(ax)
    C.heading(ax, "(a)", "Deep unfolding: learned prior alternating with measured-data consistency")
    _image_anchor(ax, _feature(1, 1), 0.012, 0.390, 0.145, 0.440,
                  "measurement-domain anchor")
    C.label_box(ax, 0.185, 0.660, 0.105, 0.100, "measured\nk-space y",
                face=C.PALE_BLUE, edge=C.BLUE, fontsize=7.5)
    C.label_box(ax, 0.325, 0.660, 0.090, 0.100,
                "adjoint " + r"$A^H$" + "\n/ zero-fill",
                face=C.PALE_GRAY, edge=C.GRAY, fontsize=7.3)
    C.arrow(ax, (0.157, 0.675), (0.185, 0.710), color=C.BLUE)
    C.arrow(ax, (0.290, 0.710), (0.325, 0.710), color=C.BLUE)
    _image_anchor(ax, _mri(2, 0), 0.445, 0.610, 0.070, 0.150,
                  "initial " + r"$x^0$")
    C.arrow(ax, (0.415, 0.710), (0.445, 0.685), color=C.BLUE)

    stage_x = [0.550, 0.705, 0.860]
    prior_y, dc_y, output_y = 0.655, 0.470, 0.365
    stage_outputs: list[tuple[float, float]] = []
    for k, x in enumerate(stage_x, 1):
        C.rounded_panel(ax, x - 0.018, 0.350, 0.125, 0.415,
                        face=C.OFF_WHITE, edge=C.GRID, radius=0.018)
        ax.text(x + 0.044, 0.748, f"stage {k}", ha="center", va="center",
                fontsize=7.4, weight="bold", color=C.NAVY)
        C.label_box(ax, x, prior_y, 0.090, 0.070,
                    "learned prior\n" + rf"$P_{{\theta,{k}}}$",
                    face=C.PALE_BLUE, edge=C.BLUE, fontsize=7.1)
        C.label_box(ax, x, dc_y, 0.090, 0.085, "DC(·; y, A)",
                    face=C.PALE_GRAY, edge=C.GRAY, fontsize=7.2)
        C.arrow(ax, (x + 0.045, prior_y), (x + 0.045, dc_y + 0.085),
                color=C.INK)
        C.label_box(ax, x + 0.020, output_y, 0.050, 0.060, rf"$x^{k}$",
                    face=C.PALE_CORAL_2, edge=C.CORAL, fontsize=7.5,
                    weight="bold")
        C.arrow(ax, (x + 0.045, dc_y), (x + 0.045, output_y + 0.060),
                color=C.CORAL)
        stage_outputs.append((x + 0.070, output_y + 0.030))
    C.arrow(ax, (0.515, 0.685), (stage_x[0], prior_y + 0.035), color=C.BLUE)
    for k in range(2):
        C.arrow(ax, stage_outputs[k], (stage_x[k + 1], prior_y + 0.035),
                color=C.CORAL, connection="arc3,rad=-0.20")

    # The measured-data bus supplies every DC, never a learned prior.
    ax.plot([0.238, 0.238, 0.930], [0.660, 0.290, 0.290],
            color=C.NAVY, lw=0.85, linestyle="--", zorder=2)
    for x in stage_x:
        # Bring the measured-data bus into the side of DC so the constraint
        # path cannot be mistaken for a connection to the reconstructed x^k.
        riser_x = x - 0.010
        ax.plot([riser_x, riser_x], [0.290, dc_y + 0.0425],
                color=C.NAVY, lw=0.80, linestyle="--", zorder=2.2)
        C.arrow(ax, (riser_x, dc_y + 0.0425),
                (x, dc_y + 0.0425), color=C.NAVY, lw=0.80, style="--")
    ax.text(0.590, 0.245,
            "physical constraint: the same measured y and forward operator A enter every DC",
            ha="center", fontsize=7.4, color=C.NAVY)
    _output_overlay(ax, 0.955, 0.335, 0.038, 0.125, r"$x^K$")
    C.arrow(ax, stage_outputs[-1], (0.955, 0.398), color=C.CORAL)
    ax.text(0.590, 0.115,
            r"Representative order: $x^{k-1}$ → learned prior → data consistency → $x^k$",
            ha="center", fontsize=7.5, color=C.INK)
    ax.text(0.590, 0.065, "No arrow carries k-space y directly into a learned image prior",
            ha="center", fontsize=7.4, color=C.CORAL)


def _generative_panel(ax: Axes) -> None:
    C.schema(ax)
    C.heading(ax, "(b)", "Generative mechanisms: distinct training and sampling semantics")
    columns = [(0.010, 0.315), (0.340, 0.315), (0.670, 0.320)]
    for x, w in columns:
        C.rounded_panel(ax, x, 0.075, w, 0.795, face=C.OFF_WHITE,
                        edge=C.GRID, radius=0.014)

    # VAE
    ax.text(0.168, 0.830, "VAE", ha="center", fontsize=8.2,
            weight="bold", color=C.NAVY)
    C.image_box(ax, _mri(2, 0), 0.025, 0.600, 0.050, 0.145, edge=C.BLUE)
    ax.text(0.050, 0.570, r"$x$", ha="center", fontsize=7.3, weight="bold")
    C.label_box(ax, 0.092, 0.620, 0.070, 0.090, "encoder",
                face=C.PALE_BLUE, edge=C.BLUE, fontsize=7.1)
    C.arrow(ax, (0.075, 0.672), (0.092, 0.665), color=C.BLUE)
    C.label_box(ax, 0.190, 0.675, 0.050, 0.052, r"$\mu$",
                face=C.WHITE, edge=C.BLUE, fontsize=7.4)
    C.label_box(ax, 0.190, 0.600, 0.050, 0.052, r"$\log\sigma^2$",
                face=C.WHITE, edge=C.BLUE, fontsize=6.8)
    C.arrow(ax, (0.162, 0.665), (0.190, 0.701), color=C.BLUE)
    C.arrow(ax, (0.162, 0.665), (0.190, 0.626), color=C.BLUE)
    C.label_box(ax, 0.075, 0.405, 0.150, 0.115,
                "reparameterize\n" + r"$\sigma=\exp(\frac{1}{2}\log\sigma^2)$" +
                "\n" + r"$z=\mu+\sigma\odot\epsilon$",
                face=C.PALE_GRAY, edge=C.GRAY, fontsize=7.0)
    C.arrow(ax, (0.215, 0.600), (0.190, 0.520), color=C.GRAY,
            connection="arc3,rad=-0.08")
    C.arrow(ax, (0.215, 0.675), (0.160, 0.520), color=C.GRAY,
            connection="arc3,rad=0.08")
    ax.text(0.060, 0.450, r"$\epsilon\sim\mathcal{N}(0,I)$", ha="center",
            fontsize=6.9, color=C.GRAY)
    C.label_box(ax, 0.235, 0.420, 0.065, 0.085, "decoder",
                face=C.PALE_CORAL, edge=C.CORAL, fontsize=7.0)
    C.arrow(ax, (0.225, 0.462), (0.235, 0.462), color=C.CORAL)
    C.image_box(ax, _mri(2, 0), 0.250, 0.225, 0.050, 0.130, edge=C.CORAL)
    ax.text(0.275, 0.195, r"$\hat{x}$", ha="center", fontsize=7.3, weight="bold")
    C.arrow(ax, (0.267, 0.420), (0.275, 0.355), color=C.CORAL)
    C.label_box(ax, 0.055, 0.145, 0.150, 0.065, "ELBO: reconstruction + KL",
                face=C.WHITE, edge=C.GRAY, fontsize=6.8)
    C.link(ax, (0.050, 0.600), (0.090, 0.210), color=C.GRAY, style="--",
           connection="arc3,rad=0.08")
    C.link(ax, (0.275, 0.225), (0.170, 0.210), color=C.GRAY, style="--",
           connection="arc3,rad=-0.08")
    C.link(ax, (0.215, 0.675), (0.195, 0.210), color=C.GRAY, style="--",
           connection="arc3,rad=-0.16")
    C.link(ax, (0.215, 0.600), (0.185, 0.210), color=C.GRAY, style="--",
           connection="arc3,rad=-0.10")

    # Conditional GAN
    ax.text(0.498, 0.830, "Conditional GAN", ha="center", fontsize=8.2,
            weight="bold", color=C.NAVY)
    C.image_box(ax, _mri(0, 0), 0.355, 0.605, 0.050, 0.140, edge=C.BLUE)
    ax.text(0.380, 0.570, r"source / condition $c$", ha="center", fontsize=6.9)
    C.label_box(ax, 0.430, 0.625, 0.070, 0.085, "Generator\nG",
                face=C.PALE_BLUE, edge=C.BLUE, fontsize=7.0)
    C.arrow(ax, (0.405, 0.675), (0.430, 0.667), color=C.BLUE)
    C.image_box(ax, _mri(2, 0), 0.525, 0.605, 0.050, 0.140, edge=C.CORAL)
    ax.text(0.550, 0.570, r"generated $\hat{x}$", ha="center", fontsize=6.9)
    C.arrow(ax, (0.500, 0.667), (0.525, 0.675), color=C.CORAL)
    C.label_box(ax, 0.520, 0.405, 0.080, 0.095, "Discriminator\nD",
                face=C.PALE_GRAY, edge=C.GRAY, fontsize=6.9)
    C.arrow(ax, (0.550, 0.605), (0.560, 0.500), color=C.CORAL)
    C.image_box(ax, _mri(2, 0), 0.365, 0.370, 0.050, 0.130, edge=C.BLUE)
    ax.text(0.390, 0.340, "real target x", ha="center", fontsize=6.8)
    C.arrow(ax, (0.415, 0.435), (0.520, 0.452), color=C.BLUE)
    C.label_box(ax, 0.605, 0.420, 0.040, 0.065, "real /\nfake",
                face=C.WHITE, edge=C.GRAY, fontsize=6.4)
    C.arrow(ax, (0.600, 0.452), (0.605, 0.452), color=C.GRAY)
    C.arrow(ax, (0.555, 0.405), (0.465, 0.625), color=C.CORAL,
            style="--", connection="arc3,rad=0.28")
    ax.text(0.475, 0.295, "dashed: adversarial training gradient to G",
            ha="center", fontsize=6.8, color=C.CORAL)
    C.label_box(ax, 0.385, 0.155, 0.225, 0.080,
                "D receives both real target and generated image",
                face=C.WHITE, edge=C.GRAY, fontsize=6.8)

    # Diffusion
    ax.text(0.830, 0.830, "Conditional diffusion", ha="center", fontsize=8.2,
            weight="bold", color=C.NAVY)
    ax.text(0.690, 0.760, "training forward process", ha="left", fontsize=7.0,
            weight="bold", color=C.NAVY)
    C.label_box(ax, 0.690, 0.640, 0.060, 0.075, r"clean $x_0$",
                face=C.PALE_BLUE, edge=C.BLUE, fontsize=6.9)
    C.label_box(ax, 0.780, 0.640, 0.080, 0.075,
                r"$q(x_t|x_0)$" + "\n" + r"$+\;\mathrm{noise}\;\epsilon$",
                face=C.PALE_GRAY, edge=C.GRAY, fontsize=6.6)
    C.label_box(ax, 0.890, 0.640, 0.060, 0.075, r"noisy $x_t$",
                face=C.PALE_GRAY, edge=C.GRAY, fontsize=6.9)
    C.arrow(ax, (0.750, 0.677), (0.780, 0.677), color=C.GRAY)
    C.arrow(ax, (0.860, 0.677), (0.890, 0.677), color=C.GRAY)
    ax.text(0.690, 0.545, "iterative reverse sampling", ha="left", fontsize=7.0,
            weight="bold", color=C.CORAL)
    C.label_box(ax, 0.690, 0.410, 0.060, 0.080, r"$x_T\sim\mathcal{N}$",
                face=C.PALE_GRAY, edge=C.GRAY, fontsize=6.8)
    C.label_box(ax, 0.775, 0.390, 0.105, 0.120,
                r"denoiser $\epsilon_\theta$" + "\n" + r"input: $x_t,t,c$",
                face=C.PALE_CORAL_2, edge=C.CORAL, fontsize=6.9)
    C.label_box(ax, 0.905, 0.410, 0.060, 0.080, r"$x_{t-1}$",
                face=C.PALE_CORAL, edge=C.CORAL, fontsize=6.9)
    C.arrow(ax, (0.750, 0.450), (0.775, 0.450), color=C.CORAL)
    C.arrow(ax, (0.880, 0.450), (0.905, 0.450), color=C.CORAL)
    C.arrow(ax, (0.935, 0.410), (0.825, 0.390), color=C.CORAL,
            connection="arc3,rad=0.28")
    ax.text(0.895, 0.345, "repeat t=T,…,1", ha="center", fontsize=6.8,
            color=C.CORAL)
    C.image_box(ax, _mri(2, 0), 0.790, 0.155, 0.070, 0.140, edge=C.CORAL)
    ax.text(0.825, 0.125, r"final $\hat{x}_0$", ha="center", fontsize=7.0,
            weight="bold")
    C.arrow(ax, (0.935, 0.410), (0.850, 0.295), color=C.CORAL,
            connection="arc3,rad=-0.08")
    ax.text(0.500, 0.035,
            "Dashed paths are training dependencies; lesion-fidelity checks are safety endpoints, not model modules",
            ha="center", fontsize=7.4, color=C.INK)


def _ssm_panel(ax: Axes) -> None:
    C.schema(ax)
    C.heading(ax, "(c)", "Selective state-space mechanism for ordered spatial tokens")
    _image_anchor(ax, _feature(0, 0), 0.012, 0.390, 0.135, 0.440,
                  "MRI patch lattice")
    # Declared serpentine scan order.
    gx, gy, gs = 0.185, 0.560, 0.115
    for i in range(4):
        for j in range(4):
            ax.add_patch(Rectangle((gx + i * gs / 4, gy + j * gs / 4),
                                   gs / 4, gs / 4, facecolor=C.PALE_BLUE_2,
                                   edgecolor=C.BLUE, linewidth=0.5, zorder=3))
    scan = [
        (gx + gs * 0.125, gy + gs * 0.125),
        (gx + gs * 0.875, gy + gs * 0.125),
        (gx + gs * 0.875, gy + gs * 0.375),
        (gx + gs * 0.125, gy + gs * 0.375),
        (gx + gs * 0.125, gy + gs * 0.625),
        (gx + gs * 0.875, gy + gs * 0.625),
        (gx + gs * 0.875, gy + gs * 0.875),
        (gx + gs * 0.125, gy + gs * 0.875),
    ]
    for p0, p1 in zip(scan[:-1], scan[1:]):
        C.arrow(ax, p0, p1, color=C.NAVY, lw=0.62, scale=6.0)
    ax.text(gx + gs / 2, gy - 0.040, "declared scan order",
            ha="center", fontsize=7.2, color=C.NAVY)
    C.arrow(ax, (0.147, 0.610), (gx, gy + gs / 2), color=C.BLUE)

    token_end = C.token_strip(ax, 0.335, 0.590, 5, w=0.025, h=0.080,
                              gap=0.006, face=C.PALE_BLUE, edge=C.BLUE)
    C.arrow(ax, (gx + gs, gy + gs / 2), (0.335, 0.630), color=C.BLUE)
    ax.text((0.335 + token_end) / 2, 0.705, r"ordered tokens $x_t$",
            ha="center", fontsize=7.3)
    C.label_box(ax, 0.485, 0.675, 0.150, 0.105,
                "selective parameters\n" + r"$\Delta_t,B_t,C_t=s(x_t)$",
                face=C.PALE_BLUE_2, edge=C.BLUE, fontsize=7.3)
    C.arrow(ax, (token_end, 0.630), (0.485, 0.727), color=C.BLUE,
            connection="arc3,rad=-0.10")
    C.label_box(ax, 0.675, 0.675, 0.165, 0.105,
                r"$\mathrm{discretize}(A,B_t,\Delta_t)$" + "\n" +
                r"$\rightarrow\bar{A}_t,\bar{B}_t$",
                face=C.PALE_GRAY, edge=C.GRAY, fontsize=7.3)
    C.arrow(ax, (0.635, 0.727), (0.675, 0.727), color=C.GRAY)

    C.label_box(ax, 0.420, 0.360, 0.120, 0.090,
                "previous state\n" + r"$h_{t-1}$",
                face=C.PALE_BLUE, edge=C.BLUE, fontsize=7.3)
    C.label_box(ax, 0.595, 0.315, 0.225, 0.165,
                "selective recurrence\n" +
                r"$h_t=\bar{A}_t h_{t-1}+\bar{B}_t x_t$",
                face=C.PALE_GRAY, edge=C.GRAY, fontsize=7.5)
    C.arrow(ax, (0.540, 0.405), (0.595, 0.405), color=C.BLUE)
    C.arrow(ax, (0.757, 0.675), (0.735, 0.480), color=C.GRAY)
    C.arrow(ax, ((0.335 + token_end) / 2, 0.590), (0.625, 0.480),
            color=C.BLUE, connection="arc3,rad=0.15")
    C.label_box(ax, 0.850, 0.350, 0.105, 0.110,
                "output token\n" + r"$y_t=C_t h_t+D x_t$",
                face=C.PALE_CORAL, edge=C.CORAL, fontsize=7.1)
    C.arrow(ax, (0.820, 0.397), (0.850, 0.405), color=C.CORAL)
    C.label_box(ax, 0.850, 0.175, 0.105, 0.100,
                "reshape +\ntask head",
                face=C.PALE_CORAL_2, edge=C.CORAL, fontsize=7.3)
    C.arrow(ax, (0.902, 0.350), (0.902, 0.275), color=C.CORAL)
    ax.text(0.510, 0.090,
            "Generic selective SSM shown; multidirectional scans or Mamba gates require a model-specific citation",
            ha="center", fontsize=7.4, color=C.INK)


def _longitudinal_panel(ax: Axes) -> None:
    C.schema(ax)
    C.heading(ax, "(d)", "Registered longitudinal model with shared encoders and task-specific heads")
    _image_anchor(ax, _longitudinal(0), 0.012, 0.570, 0.105, 0.285,
                  "baseline " + r"$I_0$" + " (fixed)")
    _image_anchor(ax, _longitudinal(1), 0.012, 0.210, 0.105, 0.285,
                  "follow-up " + r"$I_1$" + " (moving)")
    C.label_box(ax, 0.170, 0.365, 0.145, 0.140,
                "registration\nestimate " + r"$T_{1\rightarrow0}$" +
                " from\n" + r"$(I_0,I_1)$",
                face=C.PALE_GRAY, edge=C.GRAY, fontsize=7.3)
    C.arrow(ax, (0.117, 0.700), (0.170, 0.455), color=C.GRAY,
            connection="arc3,rad=0.12")
    C.arrow(ax, (0.117, 0.350), (0.170, 0.405), color=C.GRAY)
    _image_anchor(ax, _longitudinal(2), 0.345, 0.245, 0.105, 0.285,
                  "registered " + r"$I_1\circ T_{1\rightarrow0}$")
    C.arrow(ax, (0.315, 0.435), (0.345, 0.390), color=C.GRAY)

    C.label_box(ax, 0.480, 0.635, 0.125, 0.110,
                "encoder " + r"$f_\theta$" + "\nbaseline feature",
                face=C.PALE_BLUE, edge=C.BLUE, fontsize=7.4)
    C.label_box(ax, 0.480, 0.300, 0.125, 0.110,
                "encoder " + r"$f_\theta$" + "\nfollow-up feature",
                face=C.PALE_BLUE, edge=C.BLUE, fontsize=7.4)
    C.arrow(ax, (0.117, 0.720), (0.480, 0.690), color=C.BLUE)
    C.arrow(ax, (0.450, 0.388), (0.480, 0.355), color=C.BLUE)
    C.link(ax, (0.465, 0.355), (0.465, 0.690), color=C.NAVY, style="--")
    ax.text(0.445, 0.520, r"shared $\theta$", ha="right", va="center",
            fontsize=7.3, color=C.NAVY)

    C.label_box(ax, 0.660, 0.440, 0.155, 0.155,
                "feature comparison\nchoose one:\n" +
                r"$\Delta$  OR  $|\Delta|$  OR  Concat",
                face=C.PALE_GRAY, edge=C.GRAY, fontsize=7.3)
    C.arrow(ax, (0.605, 0.690), (0.660, 0.555), color=C.BLUE)
    C.arrow(ax, (0.605, 0.355), (0.660, 0.475), color=C.BLUE)
    C.label_box(ax, 0.845, 0.605, 0.105, 0.090, "change-map\nhead",
                face=C.PALE_CORAL, edge=C.CORAL, fontsize=7.3)
    C.label_box(ax, 0.845, 0.305, 0.105, 0.100,
                "future-risk head\n(post-index)",
                face=C.PALE_CORAL, edge=C.CORAL, fontsize=7.1)
    C.arrow(ax, (0.815, 0.540), (0.845, 0.650), color=C.CORAL,
            connection="arc3,rad=-0.10")
    C.arrow(ax, (0.815, 0.490), (0.845, 0.355), color=C.CORAL,
            connection="arc3,rad=0.10")
    C.image_box(ax, _longitudinal(3), 0.965, 0.585, 0.030, 0.135, edge=C.CORAL)
    C.arrow(ax, (0.950, 0.650), (0.965, 0.650), color=C.CORAL)
    C.op(ax, 0.978, 0.355, "r", r=0.020, face=C.PALE_CORAL, edge=C.CORAL,
         fontsize=7.5)
    C.arrow(ax, (0.950, 0.355), (0.958, 0.355), color=C.CORAL, scale=6.5)
    ax.text(0.600, 0.145,
            "Registration receives both fixed and moving images; only the aligned pair reaches shared encoders",
            ha="center", fontsize=7.5, color=C.INK)
    ax.text(0.600, 0.090,
            "Change localization and post-index prognosis are separate outputs. Synthetic anatomy—not patient data.",
            ha="center", fontsize=7.4, color=C.CORAL)


def build_fig08() -> None:
    title = "Measurement-constrained, generative, state-space, and longitudinal architectures"
    fig, axes = plt.subplots(4, 1, figsize=(C.FIGURE_WIDTH_IN, 9.45))
    fig.subplots_adjust(left=0.025, right=0.988, top=0.948, bottom=0.025,
                        hspace=0.080)
    fig.suptitle(title, y=0.990, fontsize=11.2, weight="bold", color=C.INK)
    _unfolding_panel(axes[0])
    _generative_panel(axes[1])
    _ssm_panel(axes[2])
    _longitudinal_panel(axes[3])
    C.save(
        fig, "fig08_emerging_models", title,
        ["deep unfolding", "VAE/GAN/diffusion", "selective state-space model",
         "registered longitudinal model"],
        assertions=[
            "Measured k-space is first mapped to x0 by an adjoint or zero-filled initialization and supplies every data-consistency operator, never a learned prior directly.",
            "The VAE includes x, encoder, mu/log-variance, reparameterization, decoder, x-hat, reconstruction, and KL dependencies.",
            "The GAN discriminator receives real and generated images; diffusion separates forward noising from iterative conditioned reverse sampling.",
            "The selective SSM declares scan order, input-dependent Delta/B/C, discretization, recurrent state, and output-token equation without claiming a fixed Mamba implementation.",
            "Longitudinal registration receives baseline and follow-up, produces an aligned follow-up, and feeds shared-weight encoders before separate change-map and post-index risk heads.",
        ],
    )


def build_all() -> None:
    build_fig04()
    build_fig05()
    build_fig06()
    build_fig07()
    build_fig08()


if __name__ == "__main__":
    build_all()
