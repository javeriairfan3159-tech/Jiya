#!/usr/bin/env python3
"""Place the exact Ready Set Go invitation onto racing scenes (no AI redraw)."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent
ORIGINALS = ROOT.parent / "originals"
OUT = ROOT
SIZE = 2000
RATIO = 5 / 7

CARD_PATH = ORIGINALS / "03-leo-ready-set-go.png"
ASPHALT = ROOT / "scene-asphalt-empty.png"
REDFLAG = ROOT / "scene-red-flag-empty.png"

FONT_BOLD = Path("/usr/share/fonts/truetype/macos/Inter-Bold.ttf")
FONT_SEMI = Path("/usr/share/fonts/truetype/macos/Inter-SemiBold.ttf")

TEAL = (13, 148, 136, 255)
GOLD = (245, 215, 110, 255)
RED = (220, 38, 38, 255)
INK = (17, 17, 17, 255)
WHITE = (255, 255, 255, 255)


def as_5x7(im: Image.Image) -> Image.Image:
    im = im.convert("RGBA")
    w, h = im.size
    if abs((w / h) - RATIO) < 0.02:
        return im
    if w / h > RATIO:
        new_w = int(h * RATIO)
        left = (w - new_w) // 2
        return im.crop((left, 0, left + new_w, h))
    new_h = int(w / RATIO)
    top = (h - new_h) // 2
    return im.crop((0, top, w, top + new_h))


def paper_stack(card: Image.Image) -> Image.Image:
    w, h = card.size
    pad = 90
    canvas = Image.new("RGBA", (w + pad * 2, h + pad * 2), (0, 0, 0, 0))

    thickness = Image.new("RGBA", (w, h), (236, 228, 214, 255))
    canvas.paste(thickness, (pad + 6, pad + 9))

    shadow = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.rounded_rectangle(
        (pad - 8, pad + 14, pad + w + 22, pad + h + 36),
        radius=8,
        fill=(10, 12, 16, 120),
    )
    shadow = shadow.filter(ImageFilter.GaussianBlur(26))
    canvas = Image.alpha_composite(canvas, shadow)

    edge = Image.new("RGBA", (w + 10, h + 10), (0, 0, 0, 0))
    ed = ImageDraw.Draw(edge)
    ed.rounded_rectangle((0, 0, w + 9, h + 9), radius=6, fill=(255, 255, 255, 255))
    canvas.paste(edge, (pad - 5, pad - 5), edge)
    canvas.paste(card, (pad, pad), card)
    return canvas


def checkered_bar(width: int, height: int, cell: int = 40) -> Image.Image:
    bar = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(bar)
    for y in range(0, height, cell):
        for x in range(0, width, cell):
            fill = (15, 15, 15, 255) if ((x // cell) + (y // cell)) % 2 == 0 else (245, 245, 245, 255)
            draw.rectangle((x, y, x + cell, y + cell), fill=fill)
    return bar


def pill(text: str, fill, color, font: ImageFont.FreeTypeFont, pad_x=28, pad_y=16) -> Image.Image:
    tmp = Image.new("RGBA", (10, 10), (0, 0, 0, 0))
    d = ImageDraw.Draw(tmp)
    x0, y0, x1, y1 = d.textbbox((0, 0), text, font=font)
    tw, th = x1 - x0, y1 - y0
    img = Image.new("RGBA", (tw + pad_x * 2, th + pad_y * 2), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle((0, 0, img.width - 1, img.height - 1), radius=img.height // 2, fill=fill)
    draw.text((pad_x - x0, pad_y - y0), text, font=font, fill=color)
    return img


def compose(scene_path: Path, angle: float, card_w: int, y_shift: int) -> Image.Image:
    scene = Image.open(scene_path).convert("RGBA").resize((SIZE, SIZE), Image.Resampling.LANCZOS)
    card = as_5x7(Image.open(CARD_PATH))
    card_h = int(card_w / RATIO)
    card = card.resize((card_w, card_h), Image.Resampling.LANCZOS)
    stacked = paper_stack(card)
    stacked = stacked.rotate(angle, resample=Image.Resampling.BICUBIC, expand=True)

    x = (SIZE - stacked.width) // 2
    y = (SIZE - stacked.height) // 2 + y_shift
    scene.alpha_composite(stacked, (x, y))
    return scene


def add_chrome(base: Image.Image, banner: str) -> Image.Image:
    img = base.convert("RGBA")
    top = checkered_bar(SIZE, 56, 28)
    img.alpha_composite(top, (0, 0))
    bottom = checkered_bar(SIZE, 56, 28)
    img.alpha_composite(bottom, (0, SIZE - 56))

    # red banner just above bottom checkers
    banner_h = 92
    band = Image.new("RGBA", (SIZE, banner_h), (0, 0, 0, 0))
    bd = ImageDraw.Draw(band)
    bd.rectangle((0, 0, SIZE, banner_h), fill=(185, 18, 27, 235))
    font = ImageFont.truetype(str(FONT_BOLD), 42)
    x0, y0, x1, y1 = bd.textbbox((0, 0), banner, font=font)
    tx = (SIZE - (x1 - x0)) // 2
    ty = (banner_h - (y1 - y0)) // 2 - y0
    bd.text((tx, ty), banner, font=font, fill=WHITE)
    img.alpha_composite(band, (0, SIZE - 56 - banner_h))

    font_s = ImageFont.truetype(str(FONT_BOLD), 28)
    inst = pill("INSTANT DOWNLOAD", INK, GOLD, font_s, pad_x=26, pad_y=14)
    edit = pill("EDITABLE CANVA TEMPLATE", TEAL, WHITE, font_s, pad_x=26, pad_y=14)
    img.alpha_composite(inst, (36, 72))
    img.alpha_composite(edit, (SIZE - edit.width - 36, 72))
    return img


def save_pair(im: Image.Image, stem: str) -> None:
    rgb = im.convert("RGB")
    rgb.save(OUT / f"{stem}.png", optimize=True)
    rgb.save(OUT / f"{stem}.jpg", quality=95, subsampling=0, optimize=True)
    print("wrote", stem, rgb.size)


def square_readable() -> Image.Image:
    """Photo 2: exact card, fully readable, racing frame."""
    canvas = Image.new("RGBA", (SIZE, SIZE), (127, 29, 29, 255))
    # diagonal checkered corners
    chk = checkered_bar(SIZE, SIZE, 48)
    mask = Image.new("L", (SIZE, SIZE), 0)
    md = ImageDraw.Draw(mask)
    md.polygon([(0, 0), (520, 0), (0, 520)], fill=255)
    md.polygon([(SIZE, SIZE), (SIZE - 520, SIZE), (SIZE, SIZE - 520)], fill=255)
    md.polygon([(SIZE, 0), (SIZE - 520, 0), (SIZE, 520)], fill=255)
    md.polygon([(0, SIZE), (520, SIZE), (0, SIZE - 520)], fill=255)
    canvas.paste(chk, (0, 0), mask)

    card = as_5x7(Image.open(CARD_PATH)).resize((1180, int(1180 / RATIO)), Image.Resampling.LANCZOS)
    stacked = paper_stack(card)
    x = (SIZE - stacked.width) // 2
    y = (SIZE - stacked.height) // 2 - 18
    canvas.alpha_composite(stacked, (x, y))
    return add_chrome(canvas, "RACE CAR BIRTHDAY INVITE")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    asphalt = compose(ASPHALT, angle=-5.4, card_w=1120, y_shift=-28)
    save_pair(add_chrome(asphalt, "RACE CAR BIRTHDAY INVITE"), "01-etsy-thumb-asphalt-2000")

    red = compose(REDFLAG, angle=4.8, card_w=1100, y_shift=-20)
    save_pair(add_chrome(red, "EDITABLE CANVA TEMPLATE"), "02-etsy-thumb-redflag-2000")

    save_pair(square_readable(), "03-etsy-thumb-square-card-2000")


if __name__ == "__main__":
    main()
