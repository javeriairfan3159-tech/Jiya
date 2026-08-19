#!/usr/bin/env python3
"""Build print sizes and Etsy listing mockups from rendered 5×7 cards."""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parent
EXPORTS = ROOT / "exports"
ASSETS = ROOT / "assets"
LISTING = ROOT / "listing"
PRINT300 = ROOT / "print-jpg"
PRINT600 = ROOT / "print-png"
FONTS = ROOT / "fonts"

LISTING.mkdir(exist_ok=True)
PRINT300.mkdir(exist_ok=True)
PRINT600.mkdir(exist_ok=True)


def load_card(name: str) -> Image.Image:
    return Image.open(EXPORTS / f"{name}.png").convert("RGB")


def save_print(name: str, card: Image.Image) -> None:
    card.resize((1500, 2100), Image.Resampling.LANCZOS).save(
        PRINT300 / f"{name}-5x7-300dpi.jpg", quality=95, subsampling=0
    )
    card.resize((3000, 4200), Image.Resampling.LANCZOS).save(
        PRINT600 / f"{name}-5x7-600dpi.png", optimize=True
    )


def drop_shadow(card: Image.Image, radius: int = 28, offset: tuple[int, int] = (18, 28), opacity: int = 140) -> Image.Image:
    w, h = card.size
    canvas = Image.new("RGBA", (w + offset[0] + radius * 2, h + offset[1] + radius * 2), (0, 0, 0, 0))
    shadow = Image.new("RGBA", card.size, (0, 0, 0, opacity))
    canvas.paste(shadow, (radius + offset[0], radius + offset[1]))
    canvas = canvas.filter(ImageFilter.GaussianBlur(radius))
    canvas.paste(card.convert("RGBA"), (radius, radius))
    return canvas


def rotate_card(card: Image.Image, angle: float, max_side: int) -> Image.Image:
    ratio = 5 / 7
    h = max_side
    w = int(h * ratio)
    resized = card.resize((w, h), Image.Resampling.LANCZOS)
    shadowed = drop_shadow(resized)
    return shadowed.rotate(angle, resample=Image.Resampling.BICUBIC, expand=True)


def lifestyle_mockup() -> None:
    scene = Image.open(ASSETS / "mockup-scene-empty.png").convert("RGB")
    scene = scene.resize((2000, 2000), Image.Resampling.LANCZOS)
    card = load_card("nocturne")
    placed = rotate_card(card, -2.4, 1080)
    x = (scene.width - placed.width) // 2 + 10
    y = (scene.height - placed.height) // 2 - 20
    base = scene.convert("RGBA")
    base.alpha_composite(placed, (x, y))
    out = base.convert("RGB")
    out = ImageEnhance.Contrast(out).enhance(1.04)
    out.save(LISTING / "01-lifestyle-nocturne-2000.jpg", quality=94, subsampling=0)
    out.save(EXPORTS / "listing-lifestyle.png", optimize=True)


def ivory_lifestyle() -> None:
    """Ivory card on a warm paper field — listing image for the light colorway."""
    canvas = Image.new("RGB", (2000, 2000), (236, 223, 205))
    # subtle vignette
    overlay = Image.new("RGB", (2000, 2000), (210, 190, 165))
    mask = Image.new("L", (2000, 2000), 0)
    d = ImageDraw.Draw(mask)
    d.ellipse((-200, -200, 2200, 2200), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(180))
    canvas = Image.composite(canvas, overlay, ImageOps.invert(mask))

    card = load_card("ivory")
    placed = rotate_card(card, 3.2, 1180)
    x = (2000 - placed.width) // 2
    y = (2000 - placed.height) // 2
    base = canvas.convert("RGBA")
    base.alpha_composite(placed, (x, y))
    base.convert("RGB").save(LISTING / "02-ivory-atelier-2000.jpg", quality=94, subsampling=0)


def trio_listing() -> None:
    canvas = Image.new("RGB", (2000, 2000), (18, 8, 10))
    # velvet-ish noise
    noise = Image.effect_noise((2000, 2000), 18).convert("L")
    tint = Image.new("RGB", (2000, 2000), (42, 14, 18))
    canvas = Image.blend(canvas, tint, 0.55)
    canvas = Image.composite(canvas, ImageEnhance.Brightness(canvas).enhance(1.12), noise.point(lambda p: p * 0.35))

    ivory = rotate_card(load_card("ivory"), -11.5, 980)
    forest = rotate_card(load_card("forest"), 11.0, 980)
    nocturne = rotate_card(load_card("nocturne"), -1.2, 1120)

    base = canvas.convert("RGBA")
    base.alpha_composite(ivory, (40, 420))
    base.alpha_composite(forest, (1040, 400))
    base.alpha_composite(nocturne, (430, 280))

    draw = ImageDraw.Draw(base)
    cinzel = ImageFont.truetype(str(FONTS / "Cinzel.ttf"), 42)
    script = ImageFont.truetype(str(FONTS / "GreatVibes-Regular.ttf"), 86)
    corm = ImageFont.truetype(str(FONTS / "CormorantGaramond.ttf"), 28)

    title = "VELVET GARDEN"
    tw = draw.textlength(title, font=cinzel)
    draw.text(((2000 - tw) / 2, 78), title, fill=(212, 180, 131), font=cinzel)
    sub = "birthday invitation suite"
    sw = draw.textlength(sub, font=script)
    draw.text(((2000 - sw) / 2, 128), sub, fill=(246, 237, 228), font=script)
    foot = "NOCTURNE  ·  FOREST  ·  IVORY ATELIER"
    fw = draw.textlength(foot, font=corm)
    draw.text(((2000 - fw) / 2, 1880), foot, fill=(212, 180, 131), font=corm)

    rgb = base.convert("RGB")
    rgb.save(LISTING / "00-etsy-thumbnail-trio-2000.jpg", quality=94, subsampling=0)
    rgb.save(EXPORTS / "listing-mockup.png", optimize=True)


def square_card(name: str, outfile: str) -> None:
    card = load_card(name)
    canvas = Image.new("RGB", (2000, 2000), card.getpixel((20, 20)))
    # fit 5x7 into square with generous margin
    h = 1680
    w = int(h * 5 / 7)
    resized = card.resize((w, h), Image.Resampling.LANCZOS)
    x = (2000 - w) // 2
    y = (2000 - h) // 2
    canvas.paste(resized, (x, y))
    canvas.save(LISTING / outfile, quality=94, subsampling=0)


def main() -> None:
    for name in ("nocturne", "forest", "ivory", "ivory-garden", "ivory-blank"):
        save_print(name, load_card(name))
    lifestyle_mockup()
    ivory_lifestyle()
    trio_listing()
    square_card("nocturne", "03-nocturne-square-2000.jpg")
    square_card("forest", "04-forest-square-2000.jpg")
    square_card("ivory", "05-ivory-square-2000.jpg")
    print("listing + print files ready")
    for p in sorted(LISTING.iterdir()):
        print(f"  {p.name:40} {p.stat().st_size:9}")


if __name__ == "__main__":
    main()
