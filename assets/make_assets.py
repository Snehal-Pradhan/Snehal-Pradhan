"""Build profile project tiles from each repo's public/logo-readme.png.

Each tile keeps the original logo pixels untouched (exact brand colours) on the
logo's own dark background, rounded and lightly outlined so it reads as a badge
on both GitHub themes.
"""

from pathlib import Path

from PIL import Image, ImageDraw

SRC = Path("/Users/sp/Desktop/oss")
OUT = Path("/Users/sp/Desktop/oss/Snehal-Pradhan/assets")
BG = (13, 14, 18)
BORDER = (255, 255, 255, 22)
PAD_X = 34
PAD_Y = 22
RADIUS = 18
SCALE = 2  # supersample for smooth corners


def build(path):
    logo = Image.open(path).convert("RGB")
    bbox = logo.getbbox()
    if bbox:
        logo = logo.crop(bbox)

    w = logo.width + PAD_X * 2
    h = logo.height + PAD_Y * 2
    size = (w * SCALE, h * SCALE)

    mask = Image.new("L", size, 0)
    ImageDraw.Draw(mask).rounded_rectangle(
        (0, 0, size[0] - 1, size[1] - 1), radius=RADIUS * SCALE, fill=255
    )

    tile = Image.new("RGBA", size, BG + (0,))
    tile.paste(logo.resize((logo.width * SCALE, logo.height * SCALE), Image.LANCZOS),
               (PAD_X * SCALE, PAD_Y * SCALE))
    tile.putalpha(mask)

    border = Image.new("RGBA", size, (0, 0, 0, 0))
    ImageDraw.Draw(border).rounded_rectangle(
        (0, 0, size[0] - 1, size[1] - 1),
        radius=RADIUS * SCALE,
        outline=BORDER,
        width=2 * SCALE,
    )
    tile = Image.alpha_composite(tile, border)
    return tile.resize((w, h), Image.LANCZOS)


for project in ("covo", "nflix", "k8o", "mainLine"):
    src = SRC / project / "public" / "logo-readme.png"
    img = build(src)
    dst = OUT / f"{project}.png"
    img.save(dst, optimize=True)
    print(dst.name, img.size)
