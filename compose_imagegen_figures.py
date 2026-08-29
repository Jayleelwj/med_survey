from __future__ import annotations

from pathlib import Path
from typing import Iterable

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent
RAW = ROOT / "assets" / "imagegen_redesign"
OUT = ROOT / "output" / "figures_ieee"

FONT_REG = "/System/Library/Fonts/Supplemental/Arial.ttf"
FONT_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"

NAVY = (37, 69, 100)
BLUE = (84, 126, 174)
PALE_BLUE = (231, 239, 248)
RED = (205, 101, 94)
PALE_RED = (251, 234, 231)
GRAY = (100, 108, 116)
LIGHT = (247, 249, 251)
WHITE = (255, 255, 255)


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT_BOLD if bold else FONT_REG, size)


def centered(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], text: str,
             size: int = 22, bold: bool = True, fill=NAVY) -> None:
    fnt = font(size, bold)
    left, top, right, bottom = box
    bb = draw.multiline_textbbox((0, 0), text, font=fnt, spacing=3, align="center")
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    draw.multiline_text(((left + right - tw) / 2, (top + bottom - th) / 2), text,
                        font=fnt, fill=fill, spacing=3, align="center")


def label(draw: ImageDraw.ImageDraw, xy: tuple[int, int], text: str,
          size: int = 18, bold: bool = False, fill=NAVY,
          anchor: str = "la") -> None:
    draw.text(xy, text, font=font(size, bold), fill=fill, anchor=anchor)


def header_band(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], text: str,
                tone: str = "blue", size: int = 22) -> None:
    fill = PALE_RED if tone == "red" else PALE_BLUE if tone == "blue" else LIGHT
    draw.rounded_rectangle(box, radius=10, fill=fill, outline=(173, 187, 201), width=1)
    centered(draw, box, text, size=size, bold=True)


def footer(im: Image.Image, text: str, height: int = 54) -> Image.Image:
    canvas = Image.new("RGB", (im.width, im.height + height), WHITE)
    canvas.paste(im, (0, 0))
    draw = ImageDraw.Draw(canvas)
    draw.line((20, im.height + 2, im.width - 20, im.height + 2), fill=(207, 215, 223), width=1)
    fnt = font(16, False)
    max_width = im.width - 70
    lines: list[str] = []
    current = ""
    for word in text.split():
        candidate = word if not current else f"{current} {word}"
        if draw.textbbox((0, 0), candidate, font=fnt)[2] <= max_width:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    centered(draw, (25, im.height + 5, im.width - 25, im.height + height - 4), "\n".join(lines),
             size=16, bold=False, fill=GRAY)
    return canvas


def add_top(im: Image.Image, height: int = 70) -> tuple[Image.Image, ImageDraw.ImageDraw]:
    canvas = Image.new("RGB", (im.width, im.height + height), WHITE)
    canvas.paste(im, (0, height))
    return canvas, ImageDraw.Draw(canvas)


def add_left(im: Image.Image, width: int = 155) -> tuple[Image.Image, ImageDraw.ImageDraw]:
    canvas = Image.new("RGB", (im.width + width, im.height), WHITE)
    canvas.paste(im, (width, 0))
    return canvas, ImageDraw.Draw(canvas)


def save(im: Image.Image, stem: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    # Twofold resampling gives sufficient effective resolution at IEEE double-column width.
    hi = im.resize((im.width * 2, im.height * 2), Image.Resampling.LANCZOS).convert("RGB")
    hi.save(OUT / f"{stem}.png", dpi=(300, 300), optimize=True)
    hi.save(OUT / f"{stem}.pdf", "PDF", resolution=300.0, quality=95)


def open_raw(number: int) -> Image.Image:
    return Image.open(RAW / f"fig{number:02d}_raw.png").convert("RGB")


def figure1() -> None:
    raw = open_raw(1).crop((0, 0, 1672, 820))  # remove ImageGen's unreliable legend text
    im, draw = add_top(raw, 76)
    xs = [0, 390, 905, 1234, 1672]
    titles = ["MRI inputs and representation", "Model families", "Imaging targets", "Evidence hierarchy"]
    for i, title in enumerate(titles):
        header_band(draw, (xs[i] + 8, 8, xs[i + 1] - 8, 65), title,
                    tone="red" if i == 2 else "blue", size=20)
    im = footer(
        im,
        "Interpretation unit: population + MRI input + target + architecture + metric + validation level; "
        "benchmark accuracy alone is not clinical utility.",
        58,
    )
    save(im, "fig01_survey_map")


def figure2() -> None:
    raw = open_raw(2)
    im, draw = add_top(raw, 75)
    bounds = [(0, 190), (190, 365), (365, 545), (545, 720), (720, 880), (880, 1315), (1315, 1536)]
    names = ["T1-weighted", "T2-weighted", "FLAIR", "Post-contrast T1", "DIR", "SWI/QSM: CVS and PRL", "Cervical cord"]
    for (left, right), name in zip(bounds, names):
        header_band(draw, (left + 4, 8, right - 4, 64), name,
                    tone="red" if "contrast" in name or "PRL" in name else "blue", size=17)
    im, draw = add_left(im, 160)
    centered(draw, (5, 130, 150, 410), "Sequence-specific\nMS biomarkers", size=19)
    centered(draw, (5, 445, 150, 695), "2-D, 2.5-D, 3-D and\nmultisequence tensors", size=18)
    centered(draw, (5, 720, 150, 1090), "Bias correction, registration,\nresampling, normalization,\naugmentation and domain shift", size=17)
    save(im, "fig02_mri_inputs")


def figure3() -> None:
    im = open_raw(3)
    draw = ImageDraw.Draw(im)
    top_bounds = [(66, 368), (465, 783), (902, 1200), (1326, 1614)]
    top_names = ["Open challenge benchmark", "Multicentre research cohort", "Longitudinal trial archive", "Routine PACS data"]
    for i, (box, name) in enumerate(zip(top_bounds, top_names)):
        header_band(draw, (box[0], 22, box[1], 56), name, tone="red" if i == 2 else "blue", size=17)
    lower = [(14, 319, "Patient-level split"), (330, 626, "Invalid: slice/timepoint leakage"),
             (640, 972, "Scanner/protocol domain shift"), (982, 1320, "Expert masks and probabilistic consensus"),
             (1329, 1662, "Experimental control  <->  clinical realism")]
    for left, right, name in lower:
        header_band(draw, (left + 4, 474, right - 4, 510), name,
                    tone="red" if "Invalid" in name else "blue", size=15)
    im = footer(im, "All visits from one patient must remain in one partition; a public leaderboard is not an external clinical test.", 50)
    save(im, "fig03_data_realism")


def _replace_circle_with_c(draw: ImageDraw.ImageDraw, x: int, y: int) -> None:
    draw.ellipse((x - 14, y - 14, x + 14, y + 14), fill=WHITE, outline=NAVY, width=2)
    centered(draw, (x - 14, y - 14, x + 14, y + 14), "C", size=16, bold=True)


def figure4() -> None:
    raw = open_raw(4)
    draw = ImageDraw.Draw(raw)
    # U-Net and 3D U-Net use channel concatenation at long skip junctions.
    for x, y in [(398, 167), (359, 335), (320, 477), (923, 168), (884, 342), (853, 488)]:
        _replace_circle_with_c(draw, x, y)
    # Remove three spurious input stubs that ImageGen placed beside lower residual blocks.
    for y in (317, 432, 548):
        draw.rectangle((1180, y - 11, 1240, y + 11), fill=WHITE)
    # Residual U-Net retains long concatenating skips and short additive identity paths.
    for x, y in [(1451, 166), (1418, 307), (1379, 432), (1345, 557)]:
        _replace_circle_with_c(draw, x, y)
    raw = raw.crop((0, 0, 1717, 775))
    draw = ImageDraw.Draw(raw)
    for box, name, tone in [((9, 8, 563, 53), "(a) U-Net (2-D)", "blue"),
                            ((578, 8, 1136, 53), "(b) 3D U-Net", "blue"),
                            ((1151, 8, 1707, 53), "(c) Residual U-Net", "red")]:
        header_band(draw, box, name, tone=tone, size=21)
    raw = footer(raw, "Blue: encoder; coral: decoder; gray: bottleneck.  C = channel concatenation;  + = residual addition; down/up arrows = down/up-sampling.", 58)
    save(raw, "fig04_unet_3d_residual")


def figure5() -> None:
    im = open_raw(5)
    draw = ImageDraw.Draw(im)
    for box, name, tone in [((7, 8, 571, 52), "(a) Dense U-Net", "blue"),
                            ((584, 8, 1137, 52), "(b) Attention U-Net", "red"),
                            ((1150, 8, 1664, 52), "(c) nnU-Net self-configuration", "blue")]:
        header_band(draw, box, name, tone=tone, size=21)
    im = footer(
        im,
        "Dense block: each layer receives the concatenation of all earlier feature maps.   "
        "Attention gate: alpha = sigmoid(psi(ReLU(Wx*x + Wg*g))); weighted skip = alpha * x.   "
        "nnU-Net: dataset fingerprint -> rules -> 2-D/3-D/cascade plans -> cross-validation/ensemble -> validation-selected postprocessing.",
        70,
    )
    save(im, "fig05_dense_attention_nnunet")


def figure6() -> None:
    im = open_raw(6)
    # Titles generated in the header are correct; add a concise, controlled mechanism legend.
    im = footer(
        im,
        "ViT: patches -> linear embeddings + positional encoding -> global MHSA/MLP blocks -> task-specific head.   "
        "Swin: patch partition -> W-MSA -> shifted-window MSA -> patch merging -> hierarchical features.",
        64,
    )
    save(im, "fig06_vit_swin")


def figure7() -> None:
    raw = open_raw(7).crop((0, 0, 1672, 785))
    draw = ImageDraw.Draw(raw)
    header_band(draw, (8, 7, 835, 48), "(a) UNETR: 3-D tokens and multiscale Transformer skips", tone="blue", size=21)
    header_band(draw, (849, 7, 1663, 48), "(b) CNN–Transformer hybrid (TransUNet)", tone="red", size=21)
    raw = footer(raw, "UNETR taps Transformer hidden states for a CNN decoder; TransUNet tokenizes the deepest CNN feature map and retains high-resolution CNN skips.  C = concatenation; + = residual addition.", 65)
    save(raw, "fig07_unetr_transunet")


def figure8() -> None:
    im = open_raw(8)
    draw = ImageDraw.Draw(im)
    items = [((13, 12, 828, 43), "(a) Deep unfolding: learned prior + measured-data consistency", "blue"),
             ((842, 12, 1658, 43), "(b) Generative models: VAE | GAN | diffusion", "red"),
             ((13, 486, 828, 519), "(c) Selective state-space / Mamba", "blue"),
             ((842, 486, 1658, 519), "(d) Longitudinal shared-weight model", "red")]
    for box, name, tone in items:
        header_band(draw, box, name, tone=tone, size=18)
    im = footer(im, "Arrows denote data flow or state/time updates. Synthesis must be audited for lesion deletion, deformation, or hallucination; measured k-space remains fixed at every consistency stage.", 58)
    save(im, "fig08_emerging_models")


def figure9() -> None:
    im = open_raw(9)
    draw = ImageDraw.Draw(im)
    top = [(15, 245, "Reference and predictions"), (258, 532, "Voxel-wise error"),
           (548, 792, "Region overlap"), (808, 1086, "FP/FN weighting"),
           (1105, 1301, "Boundary distance"), (1315, 1517, "Lesion matching")]
    for i, (left, right, name) in enumerate(top):
        header_band(draw, (left, 13, right, 43), name, tone="red" if i in (3, 4) else "blue", size=15)
    middle = [(15, 475, "Reconstruction losses"), (484, 1115, "Representation learning"), (1128, 1518, "Prognosis and temporal losses")]
    for i, (left, right, name) in enumerate(middle):
        header_band(draw, (left, 528, right, 558), name, tone="red" if i == 2 else "blue", size=15)
    bottom = [(15, 370, "Reconstruction metrics"), (385, 795, "Segmentation metrics"),
              (810, 1128, "Classification: discrimination + calibration + utility"),
              (1143, 1518, "Prognosis: C-index + calibration + net benefit")]
    for i, (left, right, name) in enumerate(bottom):
        header_band(draw, (left, 778, right, 808), name, tone="red" if i >= 2 else "blue", size=14)
    im = footer(im, "Optimization losses and reporting metrics are complementary: overlap alone does not capture tiny-lesion detection, boundary fidelity, calibration, or clinical net benefit.", 58)
    save(im, "fig09_losses_metrics")


def figure10() -> None:
    im = open_raw(10)
    draw = ImageDraw.Draw(im)
    items = [((6, 7, 566, 47), "(a) Multicentre external validation", "blue"),
             ((579, 7, 1088, 47), "(b) Scanner and protocol domain shift", "red"),
             ((1099, 7, 1664, 47), "(c) Label uncertainty and small lesions", "blue"),
             ((6, 478, 566, 518), "(d) Missing modalities and longitudinal change", "red"),
             ((579, 478, 1088, 518), "(e) Calibration, fairness, and net benefit", "blue"),
             ((1099, 478, 1664, 518), "(f) Deployment, monitoring, and governed updates", "red")]
    for box, name, tone in items:
        header_band(draw, box, name, tone=tone, size=17)
    # Clarify that the held-out site receives a locked model, not transferred patient data.
    draw.rounded_rectangle((325, 143, 390, 183), radius=7, fill=WHITE, outline=NAVY, width=1)
    centered(draw, (325, 143, 390, 183), "Frozen\nmodel", size=13, bold=True)
    draw.rounded_rectangle((1305, 817, 1545, 849), radius=7, fill=WHITE, outline=RED, width=1)
    centered(draw, (1305, 817, 1545, 849), "Revalidate before release", size=13, bold=True, fill=RED)
    im = footer(im, "Future studies should predefine patient-level splits, held-out centres, subgroup calibration, failure handling, outcome-linked utility, and post-deployment drift thresholds.", 58)
    save(im, "fig10_challenges_future")


def main() -> None:
    for fn in (figure1, figure2, figure3, figure4, figure5, figure6, figure7, figure8, figure9, figure10):
        fn()
    print(f"Composed and exported 10 audited figures to {OUT}")


if __name__ == "__main__":
    main()
