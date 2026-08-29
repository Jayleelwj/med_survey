from pathlib import Path
import sys

from PIL import Image, ImageDraw


source = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("tmp/docx_render")
pages = sorted(source.glob("page-*.png"), key=lambda p: int(p.stem.split("-")[1]))
destination = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("tmp/contact")
destination.mkdir(exist_ok=True)

for group_index, start in enumerate(range(0, len(pages), 8), start=1):
    group = pages[start:start + 8]
    thumbnails = []
    for path in group:
        image = Image.open(path).convert("RGB")
        image.thumbnail((360, 500))
        canvas = Image.new("RGB", (380, 540), "white")
        canvas.paste(image, ((380 - image.width) // 2, 25))
        ImageDraw.Draw(canvas).text((10, 8), path.stem, fill="black")
        thumbnails.append(canvas)
    sheet = Image.new("RGB", (760, 540 * ((len(thumbnails) + 1) // 2)), (225, 225, 225))
    for index, thumb in enumerate(thumbnails):
        sheet.paste(thumb, ((index % 2) * 380, (index // 2) * 540))
    sheet.save(destination / f"contact-{group_index}.jpg", quality=88)

print(f"pages={len(pages)} sheets={(len(pages) + 7) // 8}")
