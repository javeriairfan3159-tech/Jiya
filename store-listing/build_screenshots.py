#!/usr/bin/env python3
"""Compose Play Store phone screenshots (1080x1920) from real app captures."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "source"
OUT = ROOT / "screenshots"
W, H = 1080, 1920

FONT_DIR = Path("/usr/share/fonts/truetype/macos")
FONT_BOLD = FONT_DIR / "Inter-Bold.ttf"
FONT_SEMI = FONT_DIR / "Inter-SemiBold.ttf"
FONT_MED = FONT_DIR / "Inter-Medium.ttf"
FONT_REG = FONT_DIR / "Inter-Regular.ttf"


def font(path: Path, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(path), size)


def lerp(a: tuple[int, ...], b: tuple[int, ...], t: float) -> tuple[int, ...]:
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(len(a)))


def vertical_gradient(size: tuple[int, int], top: tuple[int, int, int], bottom: tuple[int, int, int]) -> Image.Image:
    img = Image.new("RGB", size)
    px = img.load()
    w, h = size
    for y in range(h):
        c = lerp(top, bottom, y / (h - 1))
        for x in range(w):
            px[x, y] = c
    return img


def rounded_mask(size: tuple[int, int], radius: int) -> Image.Image:
    mask = Image.new("L", size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((0, 0, size[0] - 1, size[1] - 1), radius=radius, fill=255)
    return mask


def wrap_text(draw: ImageDraw.ImageDraw, text: str, fnt: ImageFont.FreeTypeFont, max_width: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        trial = f"{current} {word}".strip()
        if draw.textlength(trial, font=fnt) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_centered(draw: ImageDraw.ImageDraw, text: str, y: int, fnt: ImageFont.FreeTypeFont, fill, max_width: int) -> int:
    lines = wrap_text(draw, text, fnt, max_width)
    line_h = int(fnt.size * 1.18)
    for i, line in enumerate(lines):
        tw = draw.textlength(line, font=fnt)
        draw.text(((W - tw) / 2, y + i * line_h), line, font=fnt, fill=fill)
    return len(lines) * line_h


def phone_frame(screenshot: Image.Image, frame_w: int) -> Image.Image:
    """Return a framed phone image with shadow-ready RGBA canvas."""
    src = screenshot.convert("RGB")
    sw, sh = src.size
    # Strip the live Android status bar (WhatsApp/YouTube icons, clock).
    crop_top = int(sh * 0.036)
    crop_bottom = max(sh - 18, crop_top + 100)
    src = src.crop((0, crop_top, sw, crop_bottom))
    sw, sh = src.size
    aspect = sh / sw
    inner_w = frame_w - 28
    inner_h = int(inner_w * aspect)
    inner = src.resize((inner_w, inner_h), Image.Resampling.LANCZOS)

    bezel = 14
    radius = 56
    phone_w = inner_w + bezel * 2
    phone_h = inner_h + bezel * 2 + 8
    phone = Image.new("RGBA", (phone_w, phone_h), (0, 0, 0, 0))
    pdraw = ImageDraw.Draw(phone)
    pdraw.rounded_rectangle((0, 0, phone_w - 1, phone_h - 1), radius=radius, fill=(18, 22, 32, 255))
    # Side buttons hint
    pdraw.rounded_rectangle((phone_w - 6, 220, phone_w + 4, 320), radius=4, fill=(18, 22, 32, 255))

    screen_mask = rounded_mask(inner.size, radius - 10)
    screen = Image.new("RGBA", (phone_w, phone_h), (0, 0, 0, 0))
    screen.paste(inner, (bezel, bezel + 4), screen_mask)
    phone.alpha_composite(screen)

    # Notch / speaker
    pdraw.rounded_rectangle(
        ((phone_w - 140) // 2, 16, (phone_w + 140) // 2, 28),
        radius=8,
        fill=(8, 10, 16, 255),
    )
    return phone


def drop_shadow(img: Image.Image, offset: tuple[int, int] = (0, 28), blur: int = 36, opacity: int = 120) -> Image.Image:
    shadow = Image.new("RGBA", (img.width + blur * 4, img.height + blur * 4), (0, 0, 0, 0))
    alpha = img.split()[-1]
    layer = Image.new("RGBA", img.size, (0, 0, 0, opacity))
    layer.putalpha(alpha.point(lambda a: int(a * opacity / 255)))
    shadow.paste(layer, (blur * 2 + offset[0], blur * 2 + offset[1]), layer)
    shadow = shadow.filter(ImageFilter.GaussianBlur(blur))
    shadow.alpha_composite(img, (blur * 2, blur * 2))
    return shadow


def compose(spec: dict) -> Image.Image:
    canvas = vertical_gradient((W, H), spec["top"], spec["bottom"]).convert("RGBA")
    draw = ImageDraw.Draw(canvas)

    # Soft highlight orb
    orb = Image.new("RGBA", (700, 700), (0, 0, 0, 0))
    od = ImageDraw.Draw(orb)
    od.ellipse((0, 0, 699, 699), fill=(*spec.get("orb", (255, 255, 255)), 28))
    canvas.alpha_composite(orb.filter(ImageFilter.GaussianBlur(40)), (-80, -160))

    pad = 72
    y = 78
    eyebrow = spec["eyebrow"].upper()
    ef = font(FONT_SEMI, 26)
    tw = draw.textlength(eyebrow, font=ef)
    chip_w = tw + 36
    chip_h = 44
    chip_x = (W - chip_w) / 2
    draw.rounded_rectangle(
        (chip_x, y, chip_x + chip_w, y + chip_h),
        radius=22,
        fill=(255, 255, 255, 36),
    )
    draw.text((chip_x + 18, y + 8), eyebrow, font=ef, fill=(255, 255, 255, 230))
    y += 68

    y += draw_centered(draw, spec["title"], y, font(FONT_BOLD, 62), (255, 255, 255, 255), W - pad * 2)
    y += 14
    y += draw_centered(draw, spec["subtitle"], y, font(FONT_MED, 30), (255, 255, 255, 210), W - pad * 2 - 20)
    y += 28

    shot = Image.open(SRC / spec["file"])
    frame_w = 780
    phone = phone_frame(shot, frame_w)
    # Scale phone to remaining height
    max_phone_h = H - y - 70
    scale = min(frame_w / phone.width, max_phone_h / phone.height)
    new_size = (int(phone.width * scale), int(phone.height * scale))
    phone = phone.resize(new_size, Image.Resampling.LANCZOS)
    shadowed = drop_shadow(phone)
    px = (W - shadowed.width) // 2
    py = y - 40
    canvas.alpha_composite(shadowed, (px, py))

    return canvas.convert("RGB")


SPECS = [
    {
        "out": "01-home-command-center.png",
        "file": "home-modules.jpg",
        "eyebrow": "All-in-one companion",
        "title": "Your V380 Pro command center",
        "subtitle": "Setup, PC integration, and error solving — organized in one tap.",
        "top": (13, 56, 168),
        "bottom": (8, 28, 92),
    },
    {
        "out": "02-smart-tools.png",
        "file": "smart-tools.jpg",
        "eyebrow": "Diagnostic suite",
        "title": "Tools that actually fix issues",
        "subtitle": "Error solver, IP scanner, Wi-Fi meter, RTSP URLs, and IR glare help.",
        "top": (12, 28, 68),
        "bottom": (232, 93, 18),
    },
    {
        "out": "03-camera-pairing.png",
        "file": "pairing.jpg",
        "eyebrow": "Camera pairing",
        "title": "Pair in 3 simple ways",
        "subtitle": "AP Hotspot, Wi-Fi Smart-Link, and QR Code — with time and difficulty shown.",
        "top": (67, 56, 202),
        "bottom": (36, 32, 120),
    },
    {
        "out": "04-guides-overview.png",
        "file": "guides-all.jpg",
        "eyebrow": "Step-by-step guides",
        "title": "Find the right fix fast",
        "subtitle": "Search pairing, SD format, recovery, and bookmark guides for later.",
        "top": (21, 101, 192),
        "bottom": (15, 52, 120),
    },
    {
        "out": "05-storage-cloud.png",
        "file": "storage.jpg",
        "eyebrow": "Storage & recording",
        "title": "SD, cloud, and 24/7 modes",
        "subtitle": "Format MicroSD, set loop or motion recording, and enable cloud backup.",
        "top": (14, 116, 144),
        "bottom": (10, 58, 90),
    },
    {
        "out": "06-firmware-recovery.png",
        "file": "firmware.jpg",
        "eyebrow": "Firmware & recovery",
        "title": "Update or unbrick safely",
        "subtitle": "Guided OTA updates and hard-reset recovery for red-LED or frozen cameras.",
        "top": (88, 36, 140),
        "bottom": (48, 18, 88),
    },
]


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for spec in SPECS:
        print(f"Building {spec['out']}...")
        img = compose(spec)
        dest = OUT / spec["out"]
        img.save(dest, "PNG", optimize=True)
        print(f"  wrote {dest} {img.size}")


if __name__ == "__main__":
    main()
