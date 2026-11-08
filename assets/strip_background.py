"""Remove only the flat background from each logo.

Logo pixels are copied unchanged. Background pixels become fully transparent.
Antialiased edge pixels get alpha equal to their measured coverage and are
unblended against the background, so no dark halo or tinted edge remains.
The file's colour profile is preserved.
"""

from pathlib import Path

import numpy as np
from PIL import Image

SRC = Path("/Users/sp/Desktop/oss")
OUT = Path("/Users/sp/Desktop/oss/Snehal-Pradhan/assets")
BG = np.array([13.0, 14.0, 18.0])
EDGE = 14.0  # distance below which a pixel is treated as partially background


def strip_background(path):
    im = Image.open(path)
    icc = im.info.get("icc_profile")
    rgb = np.asarray(im.convert("RGB"), dtype=np.float64)

    dist = np.abs(rgb - BG).max(axis=2)
    alpha = np.ones_like(dist)
    alpha[dist <= 1.0] = 0.0
    partial = (dist > 1.0) & (dist < EDGE)
    alpha[partial] = dist[partial] / EDGE

    safe = np.maximum(alpha, 1e-6)[..., None]
    colour = np.clip(BG + (rgb - BG) / safe, 0.0, 255.0)
    colour[alpha == 0.0] = BG  # irrelevant, fully transparent

    out = np.dstack([colour, alpha * 255.0]).round().astype(np.uint8)
    logo = Image.fromarray(out, "RGBA")

    bbox = logo.getbbox()
    if bbox:
        logo = logo.crop(bbox)

    kwargs = {}
    if icc:
        kwargs["icc_profile"] = icc
    return logo, kwargs


for project in ("covo", "nflix", "k8o", "mainLine"):
    src = SRC / project / "public" / "logo-readme.png"
    logo, kwargs = strip_background(src)
    dst = OUT / f"{project}.png"
    logo.save(dst, optimize=True, **kwargs)
    print(dst.name, logo.size)
