from PIL import Image
import os, sys

SRC = "/Users/sp/Desktop/oss"
OUT = "/Users/sp/Desktop/oss/Snehal-Pradhan/assets"
BG = (13, 14, 18)
DARK_TEXT = (26, 26, 26)

def process(path, light, name):
    im = Image.open(path).convert("RGBA")
    px = im.load()
    w, h = im.size
    out = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    op = out.load()
    for y in range(h):
        for x in range(w):
            r, g, b, _ = px[x, y]
            mx, mn = max(r, g, b), min(r, g, b)
            sat = mx - mn
            if sat <= 28:
                # neutral: alpha from luminance above background
                lum = (r * 299 + g * 587 + b * 114) // 1000
                a = (lum - 18) / (255 - 18)
                a = max(0.0, min(1.0, a))
                if a <= 0.02:
                    continue
                col = DARK_TEXT if light else (214, 214, 212)
                op[x, y] = (col[0], col[1], col[2], int(a * 255))
            else:
                a = (mx - 14) / (255 - 14)
                a = max(0.0, min(1.0, a))
                if a <= 0.02:
                    continue
                # colored accent: keep hue, slight darkening for light theme
                if light:
                    f = 0.78
                    op[x, y] = (int(r * f), int(g * f), int(b * f), int(a * 255))
                else:
                    op[x, y] = (r, g, b, int(a * 255))
    bbox = out.getbbox()
    if bbox:
        pad = 6
        bbox = (max(0, bbox[0]-pad), max(0, bbox[1]-pad),
                min(w, bbox[2]+pad), min(h, bbox[3]+pad))
        out = out.crop(bbox)
    suffix = "light" if light else "dark"
    dst = os.path.join(OUT, f"{name}-{suffix}.png")
    out.save(dst)
    print(dst, out.size)

for proj in ("covo", "nflix", "k8o", "mainLine"):
    src = os.path.join(SRC, proj, "public", "logo-readme.png")
    process(src, False, proj)
    process(src, True, proj)
