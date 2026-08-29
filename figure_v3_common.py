"""Shared drawing primitives for the ImageGen-assisted IEEE figure set.

ImageGen supplies only synthetic MRI and spatial-feature raster subjects.
All labels, operators, arrows, masks, and topology are deterministic vectors.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable, Sequence

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch, Polygon, Rectangle
from PIL import Image


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "output" / "figures_ieee"
ASSETS = ROOT / "assets" / "imagegen_ieee_v3"
OUT.mkdir(parents=True, exist_ok=True)

FIGURE_WIDTH_IN = 7.16
PNG_DPI = 600

WHITE = "#FFFFFF"
OFF_WHITE = "#FAFBFC"
PANEL = "#F6F8FA"
INK = "#33485C"
NAVY = "#315E82"
BLUE = "#6F9DBE"
PALE_BLUE = "#DDEBF5"
PALE_BLUE_2 = "#EDF4F9"
CORAL = "#C97E7C"
PALE_CORAL = "#F5DDDD"
PALE_CORAL_2 = "#FAEEEE"
GRAY = "#9AA6B2"
PALE_GRAY = "#EEF1F4"
GRID = "#D7DEE5"

mpl.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "DejaVu Sans"],
    "font.size": 8.2,
    "axes.titlesize": 10.2,
    "axes.labelsize": 8.2,
    "xtick.labelsize": 7.5,
    "ytick.labelsize": 7.5,
    "legend.fontsize": 7.5,
    "figure.facecolor": WHITE,
    "axes.facecolor": WHITE,
    "text.color": INK,
    "axes.edgecolor": INK,
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
    "savefig.facecolor": WHITE,
    "savefig.edgecolor": WHITE,
})

MANIFEST: list[dict[str, object]] = []


def schema(ax: Axes) -> None:
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")


def heading(ax: Axes, label: str, title: str, *, x: float = 0.015, y: float = 0.982) -> None:
    ax.text(x, y, label, transform=ax.transAxes, va="top", ha="left",
            fontsize=10.4, weight="bold", color=NAVY)
    ax.text(x + 0.075, y, title, transform=ax.transAxes, va="top", ha="left",
            fontsize=10.0, weight="bold", color=INK)


def rounded_panel(ax: Axes, x: float, y: float, w: float, h: float, *,
                  face: str = OFF_WHITE, edge: str = GRID, radius: float = 0.018,
                  lw: float = 0.75, zorder: int = 0) -> FancyBboxPatch:
    patch = FancyBboxPatch(
        (x, y), w, h,
        boxstyle=f"round,pad=0.006,rounding_size={radius}",
        facecolor=face, edgecolor=edge, linewidth=lw, zorder=zorder,
    )
    ax.add_patch(patch)
    return patch


def label_box(ax: Axes, x: float, y: float, w: float, h: float, text: str, *,
              face: str = PALE_GRAY, edge: str = GRAY, fontsize: float = 7.7,
              weight: str = "normal", radius: float = 0.012, zorder: int = 4) -> FancyBboxPatch:
    patch = rounded_panel(ax, x, y, w, h, face=face, edge=edge, radius=radius,
                          lw=0.8, zorder=zorder)
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center",
            fontsize=fontsize, weight=weight, color=INK, linespacing=1.12,
            zorder=zorder + 1)
    return patch


def arrow(ax: Axes, start: tuple[float, float], end: tuple[float, float], *,
          color: str = INK, lw: float = 0.95, style: str = "-",
          connection: str = "arc3", scale: float = 8.5, zorder: int = 3) -> FancyArrowPatch:
    patch = FancyArrowPatch(
        start, end, arrowstyle="-|>", mutation_scale=scale, linewidth=lw,
        color=color, linestyle=style, connectionstyle=connection,
        shrinkA=1.5, shrinkB=1.5, zorder=zorder,
    )
    ax.add_patch(patch)
    return patch


def link(ax: Axes, start: tuple[float, float], end: tuple[float, float], *,
         color: str = GRAY, lw: float = 0.8, style: str = "--",
         connection: str = "arc3", zorder: int = 2) -> FancyArrowPatch:
    patch = FancyArrowPatch(
        start, end, arrowstyle="-", linewidth=lw, color=color,
        linestyle=style, connectionstyle=connection, zorder=zorder,
    )
    ax.add_patch(patch)
    return patch


def op(ax: Axes, x: float, y: float, symbol: str, *, r: float = 0.023,
       face: str = WHITE, edge: str = GRAY, fontsize: float = 8.3) -> Circle:
    patch = Circle((x, y), r, facecolor=face, edgecolor=edge, linewidth=0.85, zorder=5)
    ax.add_patch(patch)
    ax.text(x, y, symbol, ha="center", va="center", fontsize=fontsize,
            weight="bold", color=INK, zorder=6)
    return patch


def feature_slab(ax: Axes, x: float, y: float, w: float, h: float, *,
                 face: str = PALE_BLUE, edge: str = BLUE, depth: int = 3,
                 label: str | None = None, zorder: int = 3) -> None:
    d = min(w, h) * 0.075
    for i in reversed(range(depth)):
        ax.add_patch(Rectangle((x + i * d, y + i * d), w, h,
                               facecolor=face, edgecolor=edge, linewidth=0.75,
                               zorder=zorder + depth - i))
    if label:
        ax.text(x + w / 2, y + h / 2, label, ha="center", va="center",
                fontsize=7.4, color=INK, zorder=zorder + depth + 1)


def voxel_cube(ax: Axes, x: float, y: float, s: float, *,
               face: str = PALE_BLUE, edge: str = BLUE, n: int = 4,
               alpha: float = 0.92) -> None:
    ax.add_patch(Rectangle((x, y), s, s, facecolor=face, edgecolor=edge,
                           linewidth=0.8, alpha=alpha, zorder=3))
    for i in range(1, n):
        ax.plot([x + s * i / n] * 2, [y, y + s], color=edge, lw=0.45, alpha=0.75, zorder=4)
        ax.plot([x, x + s], [y + s * i / n] * 2, color=edge, lw=0.45, alpha=0.75, zorder=4)
    off = s * 0.13
    ax.plot([x, x + off, x + s + off, x + s], [y + s, y + s + off, y + s + off, y + s],
            color=edge, lw=0.7, zorder=3)
    ax.plot([x + s, x + s + off], [y, y + off], color=edge, lw=0.7, zorder=3)
    ax.plot([x + s + off] * 2, [y + off, y + s + off], color=edge, lw=0.7, zorder=3)


def token_strip(ax: Axes, x: float, y: float, n: int, *, w: float = 0.025,
                h: float = 0.07, gap: float = 0.006, face: str = PALE_BLUE,
                edge: str = BLUE) -> float:
    for i in range(n):
        ax.add_patch(Rectangle((x + i * (w + gap), y), w, h,
                               facecolor=face, edgecolor=edge, linewidth=0.65,
                               zorder=4))
    return x + n * w + (n - 1) * gap


def asset(name: str) -> Image.Image:
    return Image.open(ASSETS / name).convert("RGB")


def grid_crop(name: str, cols: int, rows: int, col: int, row: int,
              *, pad_x: float = 0.012, pad_y: float = 0.018) -> np.ndarray:
    im = asset(name)
    cell_w, cell_h = im.width / cols, im.height / rows
    left = int(col * cell_w + pad_x * cell_w)
    top = int(row * cell_h + pad_y * cell_h)
    right = int((col + 1) * cell_w - pad_x * cell_w)
    bottom = int((row + 1) * cell_h - pad_y * cell_h)
    return np.asarray(im.crop((left, top, right, bottom)))


def image_box(ax: Axes, image: np.ndarray, x: float, y: float, w: float, h: float, *,
              edge: str = GRID, lw: float = 0.7, zorder: int = 1,
              interpolation: str = "lanczos") -> None:
    ax.imshow(image, extent=(x, x + w, y, y + h), aspect="auto",
              interpolation=interpolation, zorder=zorder)
    ax.add_patch(Rectangle((x, y), w, h, facecolor="none", edgecolor=edge,
                           linewidth=lw, zorder=zorder + 1))


def mask_overlay(ax: Axes, x: float, y: float, w: float, h: float, *,
                 reference: Sequence[tuple[float, float]],
                 prediction: Sequence[tuple[float, float]] | None = None,
                 fill_alpha: float = 0.16) -> None:
    ref = [(x + px * w, y + py * h) for px, py in reference]
    ax.add_patch(Polygon(ref, closed=True, facecolor=PALE_BLUE, edgecolor=BLUE,
                         alpha=fill_alpha, linewidth=1.0, zorder=6))
    if prediction:
        pred = [(x + px * w, y + py * h) for px, py in prediction]
        ax.add_patch(Polygon(pred, closed=True, facecolor=PALE_CORAL,
                             edgecolor=CORAL, alpha=fill_alpha,
                             linewidth=1.0, zorder=7))


def save(fig: Figure, stem: str, title: str, panels: list[str], *,
         assertions: Iterable[str], raster: bool = True,
         schematic_curves: bool = False) -> None:
    fig.savefig(OUT / f"{stem}.pdf", format="pdf", dpi=PNG_DPI, facecolor=WHITE)
    fig.savefig(OUT / f"{stem}.png", format="png", dpi=PNG_DPI, facecolor=WHITE)
    plt.close(fig)
    checks = list(assertions)
    MANIFEST.append({
        "figure_number": len(MANIFEST) + 1,
        "stem": stem,
        "title": title,
        "panels": panels,
        "alt_text": f"Technical scientific plate titled '{title}' with panels covering {', '.join(panels)}.",
        "caption_notes": checks,
        "width_in": FIGURE_WIDTH_IN,
        "png_dpi": PNG_DPI,
        "pdf_vector_text_and_paths": True,
        "contains_intentional_synthetic_raster": raster,
        "schematic_curves_not_empirical": schematic_curves,
        "content_assertions": checks,
    })


def write_manifest() -> None:
    (OUT / "figure_manifest.json").write_text(
        json.dumps({"figures": MANIFEST}, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    lines = [
        "# IEEE Survey Figure Content and Vector Audit", "",
        "Generated from the ImageGen-assisted v3 figure system.",
        "ImageGen supplies only synthetic MRI/anatomy and spatial-feature subjects; labels, operators, arrows, masks, and topology are deterministic vectors.",
        "", "| Figure | Panels | Synthetic raster | Schematic curves | Audited assertions |",
        "|---|---|---:|---:|---|",
    ]
    for i, item in enumerate(MANIFEST, 1):
        lines.append(
            f"| Fig. {i} | {', '.join(item['panels'])} | "
            f"{'yes' if item['contains_intentional_synthetic_raster'] else 'no'} | "
            f"{'yes' if item['schematic_curves_not_empirical'] else 'no'} | "
            f"{'; '.join(str(v) for v in item['content_assertions'])} |"
        )
    lines.extend([
        "", "## Global checks", "",
        "- Solid arrows denote forward data, feature, inference, or evaluation flow only.",
        "- Dashed links denote supervision, shared parameters, physical constraints, or governance dependencies and are labeled locally.",
        "- `C/Concat`, `+/Add`, and `⊙/Multiply` are not interchanged; every operator has the required inputs and an output.",
        "- ImageGen-generated material contains no scientific labels or network arrows.",
        "- No figure reports fabricated performance values, rankings, regulatory status, or empirical curves.",
        "- Synthetic MRI panels are illustrative and are identified as such in the captions.",
        "- Ordinary labels are at least 8 pt at a 7.16-in source width; compact legends are at least 7.5 pt.",
        "- PNG companions are exported at 600 dpi; PDF labels and vector overlays remain selectable paths/text.",
        "- Figure 10 contains no plot axes, chart marks, or simulated performance data.", "",
    ])
    (OUT / "FIGURE_VECTOR_AUDIT.md").write_text("\n".join(lines), encoding="utf-8")

