#!/usr/bin/env python3
"""Build Etsy listing photos from rendered exports + the lifestyle scene."""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageEnhance

ROOT = Path(__file__).resolve().parents[1]
EXPORTS = ROOT / "exports"
ASSETS = ROOT / "assets"
PHOTOS = ROOT / "listing" / "photos"
PHOTOS.mkdir(parents=True, exist_ok=True)


def load(name: str) -> Image.Image:
    return Image.open(EXPORTS / name).convert("RGBA")


def fit(im: Image.Image, w: int, h: int) -> Image.Image:
    im = im.copy()
    im.thumbnail((w, h), Image.Resampling.LANCZOS)
    return im


def drop_shadow(card: Image.Image, offset=(18, 22), blur=28, opacity=90) -> Image.Image:
    shadow = Image.new("RGBA", (card.width + abs(offset[0]) + blur * 2, card.height + abs(offset[1]) + blur * 2), (0, 0, 0, 0))
    sh = Image.new("RGBA", card.size, (40, 32, 24, opacity))
    mask = card.split()[-1]
    shadow.paste(sh, (blur + max(offset[0], 0), blur + max(offset[1], 0)), mask)
    shadow = shadow.filter(ImageFilter.GaussianBlur(blur // 2))
    out = Image.new("RGBA", shadow.size, (0, 0, 0, 0))
    out.alpha_composite(shadow)
    out.alpha_composite(card, (blur, blur))
    return out


def save_jpg(im: Image.Image, name: str, size: int | None = 2000) -> None:
    rgb = Image.new("RGB", im.size, (251, 247, 241))
    rgb.paste(im, mask=im.split()[-1] if im.mode == "RGBA" else None)
    if size:
        rgb.thumbnail((size, size), Image.Resampling.LANCZOS)
        canvas = Image.new("RGB", (size, size), (251, 247, 241))
        canvas.paste(rgb, ((size - rgb.width) // 2, (size - rgb.height) // 2))
        rgb = canvas
    rgb.save(PHOTOS / name, "JPEG", quality=92, optimize=True)
    print("wrote", PHOTOS / name, rgb.size)


def lifestyle() -> Image.Image:
    scene = Image.open(ASSETS / "mockup-scene.png").convert("RGBA")
    # Upscale scene to a wide listing plate
    scene = scene.resize((2400, 1800), Image.Resampling.LANCZOS)
    card = fit(load("invite-5x7.png"), 720, 1008)
    stacked = drop_shadow(card)
    x = (scene.width - stacked.width) // 2
    y = (scene.height - stacked.height) // 2 + 10
    scene.alpha_composite(stacked, (x, y))
    return scene


def bundle() -> Image.Image:
    canvas = Image.new("RGBA", (2400, 1800), (251, 247, 241, 255))
    pieces = [
        ("invite-5x7.png", 0.42, (180, 90)),
        ("details-card.png", 0.32, (980, 160)),
        ("invite-mobile.png", 0.28, (1680, 80)),
        ("welcome-sign.png", 0.22, (1540, 980)),
        ("books-for-baby.png", 0.18, (980, 1120)),
        ("favor-tag.png", 0.16, (1380, 1180)),
        ("diaper-raffle.png", 0.20, (180, 1280)),
    ]
    for name, scale, pos in pieces:
        im = load(name)
        w = int(im.width * scale)
        h = int(im.height * scale)
        im = im.resize((w, h), Image.Resampling.LANCZOS)
        stacked = drop_shadow(im, offset=(10, 12), blur=18, opacity=70)
        canvas.alpha_composite(stacked, pos)
    return canvas


def square_card(name: str) -> Image.Image:
    card = load(name)
    side = max(card.size)
    canvas = Image.new("RGBA", (side, side), (251, 247, 241, 255))
    canvas.paste(card, ((side - card.width) // 2, (side - card.height) // 2), card)
    return canvas


def extras_plate() -> Image.Image:
    canvas = Image.new("RGBA", (2400, 1800), (251, 247, 241, 255))
    books = fit(load("books-for-baby.png"), 980, 980)
    raffle = fit(load("diaper-raffle.png"), 1100, 660)
    tag = fit(load("favor-tag.png"), 620, 620)
    canvas.alpha_composite(drop_shadow(books), (120, 280))
    canvas.alpha_composite(drop_shadow(raffle), (1180, 180))
    canvas.alpha_composite(drop_shadow(tag), (1500, 980))
    return canvas


def main() -> None:
    save_jpg(lifestyle(), "01-lifestyle-hero-2000.jpg", 2000)
    save_jpg(square_card("invite-5x7.png"), "02-invite-5x7-2000.jpg", 2000)
    save_jpg(square_card("invite-mobile.png"), "03-mobile-evite-2000.jpg", 2000)
    save_jpg(square_card("details-card.png"), "04-details-card-2000.jpg", 2000)
    save_jpg(square_card("welcome-sign.png"), "05-welcome-sign-2000.jpg", 2000)
    save_jpg(extras_plate(), "06-books-raffle-tag-2000.jpg", 2000)
    save_jpg(square_card("favor-tag.png"), "07-favor-tag-2000.jpg", 2000)
    save_jpg(bundle(), "08-bundle-overview-2000.jpg", 2000)
    # also dump a print-size jpg of the 5x7 for easy listing upload
    card = load("invite-5x7.png").convert("RGB")
    card.save(PHOTOS / "invite-5x7-print.jpg", "JPEG", quality=94, optimize=True)
    print("done")


if __name__ == "__main__":
    main()
