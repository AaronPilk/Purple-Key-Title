#!/usr/bin/env python3
"""Purple Key Title & Escrow - responsive image pipeline.

Reads the selected frames out of the Higgsfield library, crops them to the
aspect each slot needs, applies one light consistent grade so the set reads as
a single shoot, and writes WebP + JPEG at every width the markup asks for.

    python3 prepare_assets.py [library_dir] [out_dir]
"""
import os
import sys

from PIL import Image, ImageEnhance

LIB = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser("~/mnt/higgsfieldimages")
OUT = sys.argv[2] if len(sys.argv) > 2 else "assets/img"
INDEX = os.path.join(LIB, "_bts_previews", "index.txt")

# slot -> library index, target aspect, output widths, vertical crop anchor
SLOTS = {
    "hero":        dict(idx=142, ratio=(16, 9), widths=[1800, 1200, 800], fy=0.56),
    "about":       dict(idx=169, ratio=(4, 3),  widths=[1400, 900, 600],        fy=0.50),
    "residential": dict(idx=165, ratio=(3, 2),  widths=[1200, 800, 600],        fy=0.50),
    "investors":   dict(idx=182, ratio=(3, 2),  widths=[1200, 800, 600],        fy=0.52),
    "land":        dict(idx=179, ratio=(3, 2),  widths=[1200, 800, 600],        fy=0.50),
    "commercial":  dict(idx=188, ratio=(3, 2),  widths=[1200, 800, 600],        fy=0.50),
    "escrow":      dict(idx=180, ratio=(3, 2),  widths=[1200, 800, 600],        fy=0.50),
    "detail":      dict(idx=132, ratio=(3, 4),  widths=[900, 600],              fy=0.46),
    "process":     dict(idx=123, ratio=(16, 9), widths=[1600, 1000, 700],       fy=0.50),
    "contact":     dict(idx=209, ratio=(3, 2),  widths=[1200, 800],             fy=0.50),
    "coverage":    dict(idx=71,  ratio=(16, 9), widths=[1600, 1000, 700],       fy=0.52),
    "colonial":    dict(idx=70,  ratio=(3, 2),  widths=[1200, 800, 600],        fy=0.54),
}


def load_index():
    m = {}
    with open(INDEX) as fh:
        for line in fh:
            line = line.rstrip("\n")
            if not line:
                continue
            n, name = line.split("\t", 1)
            m[int(n)] = os.path.join(LIB, name)
    return m


def grade(im):
    """One light pass applied to every frame so the set is consistent: a touch
    of warmth, a touch of contrast, nothing that reads as a filter."""
    im = ImageEnhance.Color(im).enhance(1.03)
    im = ImageEnhance.Contrast(im).enhance(1.04)
    im = ImageEnhance.Brightness(im).enhance(1.015)
    r, g, b = im.split()
    r = r.point(lambda v: min(255, int(v * 1.012)))
    b = b.point(lambda v: int(v * 0.992))
    return Image.merge("RGB", (r, g, b))


def crop_to(im, ratio, fy):
    tw, th = ratio
    target = tw / th
    w, h = im.size
    cur = w / h
    if cur > target:                       # too wide -> trim the sides
        nw = int(round(h * target))
        x = (w - nw) // 2
        box = (x, 0, x + nw, h)
    else:                                  # too tall -> trim top/bottom to anchor
        nh = int(round(w / target))
        y = int(round((h - nh) * fy))
        y = max(0, min(h - nh, y))
        box = (0, y, w, y + nh)
    return im.crop(box)


def main():
    idx = load_index()
    os.makedirs(OUT, exist_ok=True)
    manifest = []
    for slot, cfg in SLOTS.items():
        src = idx.get(cfg["idx"])
        if not src or not os.path.exists(src):
            print("MISSING", slot, cfg["idx"])
            continue
        im = Image.open(src).convert("RGB")
        im = grade(crop_to(im, cfg["ratio"], cfg["fy"]))
        tw, th = cfg["ratio"]
        for w in cfg["widths"]:
            if w > im.width:
                continue
            h = int(round(w * th / tw))
            r = im.resize((w, h), Image.LANCZOS)
            r.save(os.path.join(OUT, "%s-%d.webp" % (slot, w)), "WEBP", quality=74, method=6)
            r.save(os.path.join(OUT, "%s-%d.jpg" % (slot, w)), "JPEG",
                   quality=78, optimize=True, progressive=True, subsampling=2)
        big = max(w for w in cfg["widths"] if w <= im.width)
        manifest.append((slot, big, int(round(big * th / tw))))
        print("%-12s %s  %dx%d  -> %s" % (slot, os.path.basename(src), im.width, im.height,
                                          ", ".join(str(w) for w in cfg["widths"] if w <= im.width)))
    with open(os.path.join(OUT, "manifest.txt"), "w") as fh:
        for slot, w, h in manifest:
            fh.write("%s\t%d\t%d\n" % (slot, w, h))


if __name__ == "__main__":
    main()
