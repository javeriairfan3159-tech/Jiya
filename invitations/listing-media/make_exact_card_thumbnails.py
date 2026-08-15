#!/usr/bin/env python3
"""Exact-card mockups. Card pixels are only resized/rotated/pasted — never redrawn."""

from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent
ORIGINALS = ROOT.parent / "originals"
OUT = ROOT
SIZE = 2000
RATIO = 5 / 7

# Do not swap this path. This is the listing card — paste as-is.
CARD_PATH = ORIGINALS / "alex-ready-set-go.png"

FONT_BOLD = Path("/usr/share/fonts/truetype/macos/Inter-Bold.ttf")
TEAL = (13, 148, 136, 255)
GOLD = (245, 215, 110, 255)
INK = (17, 17, 17, 255)
WHITE = (255, 255, 255, 255)


def load_card() -> Image.Image:
    return Image.open(CARD_PATH).convert("RGBA")


def as_5x7(im: Image.Image) -> Image.Image:
    """Crop letterboxing only if the file is not already 5:7. No content redraw."""
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
        fill=(10, 12, 16, 130),
    )
    shadow = shadow.filter(ImageFilter.GaussianBlur(26))
    canvas = Image.alpha_composite(canvas, shadow)
    edge = Image.new("RGBA", (w + 10, h + 10), (0, 0, 0, 0))
    ImageDraw.Draw(edge).rounded_rectangle((0, 0, w + 9, h + 9), radius=6, fill=(255, 255, 255, 255))
    canvas.paste(edge, (pad - 5, pad - 5), edge)
    canvas.paste(card, (pad, pad), card)
    return canvas


def checkered_bar(width: int, height: int, cell: int = 28) -> Image.Image:
    bar = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(bar)
    for y in range(0, height, cell):
        for x in range(0, width, cell):
            fill = (15, 15, 15, 255) if ((x // cell) + (y // cell)) % 2 == 0 else (245, 245, 245, 255)
            draw.rectangle((x, y, x + cell, y + cell), fill=fill)
    return bar


def pill(text: str, fill, color, font, pad_x=26, pad_y=14) -> Image.Image:
    tmp = Image.new("RGBA", (8, 8), (0, 0, 0, 0))
    d = ImageDraw.Draw(tmp)
    x0, y0, x1, y1 = d.textbbox((0, 0), text, font=font)
    tw, th = x1 - x0, y1 - y0
    img = Image.new("RGBA", (tw + pad_x * 2, th + pad_y * 2), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle((0, 0, img.width - 1, img.height - 1), radius=img.height // 2, fill=fill)
    draw.text((pad_x - x0, pad_y - y0), text, font=font, fill=color)
    return img


def add_chrome(base: Image.Image, banner: str) -> Image.Image:
    img = base.convert("RGBA")
    img.alpha_composite(checkered_bar(SIZE, 56), (0, 0))
    img.alpha_composite(checkered_bar(SIZE, 56), (0, SIZE - 56))
    banner_h = 92
    band = Image.new("RGBA", (SIZE, banner_h), (185, 18, 27, 235))
    bd = ImageDraw.Draw(band)
    font = ImageFont.truetype(str(FONT_BOLD), 42)
    x0, y0, x1, y1 = bd.textbbox((0, 0), banner, font=font)
    bd.text(((SIZE - (x1 - x0)) // 2, (banner_h - (y1 - y0)) // 2 - y0), banner, font=font, fill=WHITE)
    img.alpha_composite(band, (0, SIZE - 56 - banner_h))
    font_s = ImageFont.truetype(str(FONT_BOLD), 28)
    inst = pill("INSTANT DOWNLOAD", INK, GOLD, font_s)
    edit = pill("EDITABLE CANVA TEMPLATE", TEAL, WHITE, font_s)
    img.alpha_composite(inst, (36, 72))
    img.alpha_composite(edit, (SIZE - edit.width - 36, 72))
    return img


def place_card_on_scene(scene: Image.Image, angle: float, card_w: int, y_shift: int) -> Image.Image:
    card = as_5x7(load_card())
    card_h = int(card_w / RATIO)
    card = card.resize((card_w, card_h), Image.Resampling.LANCZOS)
    stacked = paper_stack(card).rotate(angle, resample=Image.Resampling.BICUBIC, expand=True)
    x = (SIZE - stacked.width) // 2
    y = (SIZE - stacked.height) // 2 + y_shift
    scene = scene.convert("RGBA")
    scene.alpha_composite(stacked, (x, y))
    return scene


def white_screen_box(phone: Image.Image) -> tuple[int, int, int, int]:
    a = np.array(phone.convert("RGB"))
    mask = (a[:, :, 0] > 230) & (a[:, :, 1] > 230) & (a[:, :, 2] > 230)
    ys, xs = np.where(mask)
    pad = 6
    return int(xs.min()) + pad, int(ys.min()) + pad, int(xs.max()) - pad, int(ys.max()) - pad


def phone_mockup(scene_path: Path) -> Image.Image:
    scene = Image.open(scene_path).convert("RGBA").resize((SIZE, SIZE), Image.Resampling.LANCZOS)
    x0, y0, x1, y1 = white_screen_box(scene)
    # scale box from 1024 detect... wait we already resized. Detect on 2000 image.
    x0, y0, x1, y1 = white_screen_box(scene)
    box_w, box_h = x1 - x0, y1 - y0
    card = as_5x7(load_card())
    # Fit the FULL card (contain) so nothing is cropped.
    scale = min(box_w / card.width, box_h / card.height)
    nw, nh = int(card.width * scale), int(card.height * scale)
    card = card.resize((nw, nh), Image.Resampling.LANCZOS)
    px = x0 + (box_w - nw) // 2
    py = y0 + (box_h - nh) // 2
    scene.paste(card, (px, py), card)
    return scene


def save_pair(im: Image.Image, stem: str) -> None:
    rgb = im.convert("RGB")
    rgb.save(OUT / f"{stem}.png", optimize=True)
    rgb.save(OUT / f"{stem}.jpg", quality=95, subsampling=0, optimize=True)
    print("wrote", stem, rgb.size)


def main() -> None:
    wood = Image.open(ROOT / "scene-wood-table-empty.png").convert("RGBA").resize((SIZE, SIZE), Image.Resampling.LANCZOS)
    track = Image.open(ROOT / "scene-track-bokeh-empty.png").convert("RGBA").resize((SIZE, SIZE), Image.Resampling.LANCZOS)
    save_pair(add_chrome(place_card_on_scene(wood, -4.6, 1080, -18), "RACE CAR BIRTHDAY INVITE"), "04-etsy-thumb-wood-2000")
    save_pair(add_chrome(place_card_on_scene(track, -7.2, 1140, -10), "RACE CAR BIRTHDAY INVITE"), "05-etsy-thumb-track-2000")
    save_pair(add_chrome(phone_mockup(ROOT / "scene-phone-empty-screen.png"), "EDITABLE CANVA TEMPLATE"), "06-etsy-thumb-phone-2000")


if __name__ == "__main__":
    main()
