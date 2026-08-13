#!/usr/bin/env python3
"""Place the exact invitation file onto the marble scene (no AI redraw)."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parent
SCENE = ROOT / "mockup-scene-empty-marble.png"
DEFAULT_CARD = Path("/workspace/invitations/5x7-print/03-aria-listing-hero-5x7-600dpi.png")
CLIENT_CARD = Path("/workspace/invitations/client-card.png")
OUT_PNG = ROOT / "04-exact-card-mockup-2000.png"
OUT_JPG = ROOT / "04-exact-card-mockup-2000.jpg"


def find_card() -> Path:
    for path in (
        CLIENT_CARD,
        Path("/workspace/invitations/client-card.jpg"),
        Path("/workspace/invitations/client-card.jpeg"),
        DEFAULT_CARD,
    ):
        if path.exists():
            return path
    raise FileNotFoundError("No card file found")


def as_5x7(card: Image.Image) -> Image.Image:
    card = card.convert("RGBA")
    w, h = card.size
    target_ratio = 5 / 7
    if abs((w / h) - target_ratio) < 0.02:
        return card
    if w / h > target_ratio:
        new_w = int(h * target_ratio)
        left = (w - new_w) // 2
        return card.crop((left, 0, left + new_w, h))
    new_h = int(w / target_ratio)
    top = (h - new_h) // 2
    return card.crop((0, top, w, top + new_h))


def paper_stack(card: Image.Image) -> Image.Image:
    """Exact artwork plus a thin paper edge and drop shadow."""
    w, h = card.size
    pad = 80
    canvas = Image.new("RGBA", (w + pad * 2, h + pad * 2), (0, 0, 0, 0))

    thickness = Image.new("RGBA", (w, h), (236, 228, 214, 255))
    canvas.paste(thickness, (pad + 5, pad + 7))

    shadow = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.rounded_rectangle(
        (pad - 6, pad + 10, pad + w + 18, pad + h + 28),
        radius=6,
        fill=(40, 48, 62, 95),
    )
    shadow = shadow.filter(ImageFilter.GaussianBlur(22))
    canvas = Image.alpha_composite(canvas, shadow)
    canvas.paste(card, (pad, pad), card)
    return canvas


def main() -> None:
    scene = Image.open(SCENE).convert("RGBA").resize((2000, 2000), Image.Resampling.LANCZOS)
    card_path = find_card()
    card = as_5x7(Image.open(card_path))
    card = card.resize((1080, 1512), Image.Resampling.LANCZOS)
    stacked = paper_stack(card)
    stacked = stacked.rotate(-4.2, resample=Image.Resampling.BICUBIC, expand=True)

    x = (scene.width - stacked.width) // 2
    y = (scene.height - stacked.height) // 2 - 20
    scene.alpha_composite(stacked, (x, y))

    rgb = scene.convert("RGB")
    rgb.save(OUT_PNG)
    rgb.save(OUT_JPG, quality=95, subsampling=0)
    print(f"card: {card_path}")
    print(f"wrote {OUT_JPG} {rgb.size}")


if __name__ == "__main__":
    main()
