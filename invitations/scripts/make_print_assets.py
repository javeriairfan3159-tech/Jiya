#!/usr/bin/env python3
"""Crop racing invites to exact 5x7 and export print + listing files."""

from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
ORIGINALS = ROOT / "originals"
PRINT_DIR = ROOT / "5x7-print"
LISTING_DIR = ROOT / "listing-jpg"

RATIO = 5 / 7
PRINT_300 = (1500, 2100)
PRINT_600 = (3000, 4200)
LISTING = (1500, 2100)

CARDS = [
    ("01-leo-start-your-engines.png", "01-leo-start-your-engines"),
    ("02-leo-race-on-over.png", "02-leo-race-on-over"),
    ("03-leo-ready-set-go.png", "03-leo-ready-set-go"),
    ("04-leo-need-speed.png", "04-leo-need-speed"),
]


def as_5x7(im: Image.Image) -> Image.Image:
    im = im.convert("RGB")
    w, h = im.size
    if abs((w / h) - RATIO) < 0.01:
        return im
    if w / h > RATIO:
        new_w = int(round(h * RATIO))
        left = (w - new_w) // 2
        return im.crop((left, 0, left + new_w, h))
    new_h = int(round(w / RATIO))
    top = (h - new_h) // 2
    return im.crop((0, top, w, top + new_h))


def save_png(im: Image.Image, path: Path, size: tuple[int, int], dpi: int) -> None:
    out = im.resize(size, Image.Resampling.LANCZOS)
    out.save(path, "PNG", dpi=(dpi, dpi), optimize=True)


def save_jpg(im: Image.Image, path: Path, size: tuple[int, int], dpi: int) -> None:
    out = im.resize(size, Image.Resampling.LANCZOS)
    out.save(path, "JPEG", quality=95, subsampling=0, dpi=(dpi, dpi), optimize=True)


def main() -> None:
    PRINT_DIR.mkdir(parents=True, exist_ok=True)
    LISTING_DIR.mkdir(parents=True, exist_ok=True)

    mockup = ORIGINALS / "etsy-mockup-asphalt.png"
    if mockup.exists():
        m = Image.open(mockup).convert("RGB")
        square = m.resize((2000, 2000), Image.Resampling.LANCZOS)
        square.save(LISTING_DIR / "00-etsy-thumbnail-mockup-2000.jpg", "JPEG", quality=95, subsampling=0, optimize=True)
        print("wrote listing thumbnail mockup")

    for src_name, stem in CARDS:
        src = ORIGINALS / src_name
        card = as_5x7(Image.open(src))
        save_png(card, PRINT_DIR / f"{stem}-5x7-300dpi.png", PRINT_300, 300)
        save_png(card, PRINT_DIR / f"{stem}-5x7-600dpi.png", PRINT_600, 600)
        save_jpg(card, LISTING_DIR / f"{stem}-5x7-300dpi.jpg", LISTING, 300)
        print(f"wrote {stem}  {card.size[0]}x{card.size[1]} -> 5x7")


if __name__ == "__main__":
    main()
