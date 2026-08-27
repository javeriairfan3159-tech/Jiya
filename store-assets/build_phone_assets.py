#!/usr/bin/env python3
"""Build realistic phone mockups from the real Kite Master screenshots."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "source" / "app-screens"
OUT = ROOT / "phone-assets"
STORE = OUT / "store-1080x1920"
ISO = OUT / "isolated"
LINEUP = OUT / "lineups"
DL = ROOT / "downloads"

FONT_BOLD = "/usr/share/fonts/truetype/macos/Inter-Bold.ttf"
FONT_SEMI = "/usr/share/fonts/truetype/macos/Inter-SemiBold.ttf"
FONT_REG = "/usr/share/fonts/truetype/macos/Inter-Regular.ttf"

SCREENS = [
    ("832582d9-75e4-4519-ad1e-4e9ef9ec807a.jpg", True, "01-home", "Know the wind. Then fly.", "Live flying conditions"),
    ("287cb277-a1b6-4318-8f4f-a07c0aaf345b.jpg", True, "02-dashboard", "Perfect days, perfect wind.", "Live forecast + alerts"),
    ("37227092-2eaf-4232-9884-3fc71b789cfb.jpg", False, "03-masterclass", "Master the Pech.", "Launch, fight, fly like a pro"),
    ("00412e44-bfc0-406e-b5e8-b0a8cd0e21ce.jpg", False, "04-safety", "Fly smart. Stay safe.", "Hazards & emergency knots"),
    ("ec086674-1c36-4dea-9e7b-fd7929b18cbe.jpg", False, "05-achievements", "Keep the streak alive.", "Badges for every flight"),
]


def font(path, size):
    return ImageFont.truetype(path, size)


def crop_screen(path: Path, has_ad: bool) -> Image.Image:
    im = Image.open(path).convert("RGB")
    w, h = im.size
    top = 0  # keep status bar so it looks like a real phone
    bottom = 1456 if has_ad else 1564
    return im.crop((0, top, w, min(bottom, h)))


def rounded_mask(size, radius):
    m = Image.new("L", size, 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, size[0] - 1, size[1] - 1), radius=radius, fill=255)
    return m


def make_phone(screen: Image.Image, screen_w=780) -> Image.Image:
    """Premium flagship phone: thin bezel, dynamic island, side buttons, cyan rim."""
    ratio = screen.height / screen.width
    screen_h = int(screen_w * ratio)
    screen_r = screen.resize((screen_w, screen_h), Image.Resampling.LANCZOS)

    bezel = 22
    top_bar = 34
    bottom_bar = 42
    device_w = screen_w + bezel * 2
    device_h = screen_h + top_bar + bottom_bar
    r_outer = 82
    r_screen = 48

    canvas_w = device_w + 56
    canvas_h = device_h + 64
    canvas = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))
    ox, oy = 28, 24

    # drop shadow
    shadow = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.rounded_rectangle((ox + 12, oy + 28, ox + device_w + 12, oy + device_h + 28), radius=r_outer, fill=(0, 0, 0, 180))
    canvas.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(20)))

    # cyan glow rim
    glow = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.rounded_rectangle((ox - 8, oy - 8, ox + device_w + 8, oy + device_h + 8), radius=r_outer + 8, fill=(0, 229, 255, 70))
    canvas.alpha_composite(glow.filter(ImageFilter.GaussianBlur(12)))

    body = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(body)
    # titanium outer rim
    d.rounded_rectangle((ox, oy, ox + device_w - 1, oy + device_h - 1), radius=r_outer, fill=(168, 176, 192, 255))
    # dark inner chassis
    d.rounded_rectangle((ox + 7, oy + 7, ox + device_w - 8, oy + device_h - 8), radius=r_outer - 8, fill=(12, 10, 18, 255))

    # side buttons (titanium)
    d.rounded_rectangle((ox + device_w - 2, oy + 220, ox + device_w + 8, oy + 318), radius=4, fill=(190, 196, 210, 255))
    d.rounded_rectangle((ox - 8, oy + 190, ox + 3, oy + 258), radius=4, fill=(190, 196, 210, 255))
    d.rounded_rectangle((ox - 8, oy + 272, ox + 3, oy + 352), radius=4, fill=(190, 196, 210, 255))

    canvas.alpha_composite(body)

    # screen
    sx, sy = ox + bezel, oy + top_bar
    screen_rgba = screen_r.convert("RGBA")
    smask = rounded_mask(screen_r.size, r_screen)
    canvas.paste(screen_rgba, (sx, sy), smask)

    # dynamic island
    island_w, island_h = 148, 36
    ix = ox + (device_w - island_w) // 2
    iy = oy + 16
    d2 = ImageDraw.Draw(canvas)
    d2.rounded_rectangle((ix, iy, ix + island_w, iy + island_h), radius=18, fill=(6, 4, 10, 255))
    # camera dots
    d2.ellipse((ix + island_w - 42, iy + 8, ix + island_w - 14, iy + 28), fill=(18, 28, 48, 255))
    d2.ellipse((ix + island_w - 34, iy + 12, ix + island_w - 22, iy + 24), fill=(40, 90, 160, 255))

    # home indicator on bezel
    hw, hh = 140, 6
    hx = ox + (device_w - hw) // 2
    hy = oy + device_h - 18
    d2.rounded_rectangle((hx, hy, hx + hw, hy + hh), radius=3, fill=(230, 230, 240, 220))

    return canvas


def store_frame(phone: Image.Image, headline: str, sub: str, outfile: Path):
    W, H = 1080, 1920
    bg = Image.new("RGB", (W, H), (10, 6, 18))
    # gradient-ish orbs
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    od.ellipse((-200, -120, 520, 560), fill=(180, 40, 255, 50))
    od.ellipse((500, 700, 1300, 1600), fill=(0, 200, 255, 40))
    bg = Image.alpha_composite(bg.convert("RGBA"), overlay.filter(ImageFilter.GaussianBlur(60)))

    # fit phone
    max_h = 1380
    max_w = 860
    s = min(max_w / phone.width, max_h / phone.height)
    ph = phone.resize((int(phone.width * s), int(phone.height * s)), Image.Resampling.LANCZOS)
    px = (W - ph.width) // 2
    py = 430
    bg.alpha_composite(ph, (px, py))

    draw = ImageDraw.Draw(bg)
    def center(y, text, fnt, fill):
        bbox = draw.textbbox((0, 0), text, font=fnt)
        tw = bbox[2] - bbox[0]
        draw.text(((W - tw) / 2, y), text, font=fnt, fill=fill)

    center(78, "KITE MASTER", font(FONT_SEMI, 28), (0, 229, 255))
    # wrap headline
    words = headline.split()
    lines, cur = [], ""
    f1 = font(FONT_BOLD, 58)
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=f1) < 960:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    y = 140
    for line in lines:
        center(y, line, f1, (255, 255, 255))
        y += 70
    center(y + 8, sub, font(FONT_REG, 30), (186, 176, 214))
    bg.convert("RGB").save(outfile, "PNG", optimize=True)
    print("store", outfile.name)


def lineup_vertical(phones, outfile: Path):
    W, H = 1080, 1920
    bg = Image.new("RGBA", (W, H), (10, 6, 18, 255))
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    od.ellipse((200, 200, 900, 1100), fill=(160, 40, 255, 55))
    od.ellipse((-100, 1100, 700, 2000), fill=(0, 200, 255, 40))
    bg.alpha_composite(overlay.filter(ImageFilter.GaussianBlur(70)))

    pick = [phones[0], phones[2], phones[3]]  # home, pech, safety
    # scale
    target_h = 1180
    scaled = []
    for p in pick:
        s = target_h / p.height
        scaled.append(p.resize((int(p.width * s), target_h), Image.Resampling.LANCZOS))

    positions = [
        (int(W * 0.12) - scaled[0].width // 2, 520),
        (int(W * 0.50) - scaled[1].width // 2, 400),
        (int(W * 0.88) - scaled[2].width // 2, 520),
    ]
    # draw back phones first
    order = [0, 2, 1]
    for i in order:
        bg.alpha_composite(scaled[i], positions[i])

    draw = ImageDraw.Draw(bg)
    def center(y, text, fnt, fill):
        bbox = draw.textbbox((0, 0), text, font=fnt)
        tw = bbox[2] - bbox[0]
        draw.text(((W - tw) / 2, y), text, font=fnt, fill=fill)

    center(90, "KITE MASTER", font(FONT_SEMI, 28), (0, 229, 255))
    center(150, "Your kite flying hub", font(FONT_BOLD, 56), (255, 255, 255))
    center(230, "Wind · Pech · Safety — on your phone", font(FONT_REG, 28), (186, 176, 214))
    bg.convert("RGB").save(outfile, "PNG", optimize=True)
    print("lineup", outfile.name)


def lineup_wide(phones, outfile: Path):
    W, H = 1920, 1080
    bg = Image.new("RGBA", (W, H), (10, 6, 18, 255))
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    od.ellipse((900, -100, 2100, 1100), fill=(140, 40, 255, 70))
    od.ellipse((700, 200, 1700, 1200), fill=(0, 210, 255, 40))
    bg.alpha_composite(overlay.filter(ImageFilter.GaussianBlur(80)))

    pick = phones[:3]
    target_h = 860
    scaled = []
    for p in pick:
        s = target_h / p.height
        scaled.append(p.resize((int(p.width * s), target_h), Image.Resampling.LANCZOS))

    xs = [980, 1280, 1580]
    for i, p in enumerate(scaled):
        x = xs[i] - p.width // 2
        y = (H - p.height) // 2 + 20
        bg.alpha_composite(p, (x, y))

    draw = ImageDraw.Draw(bg)
    icon = Image.open(ROOT / "icon" / "kite-master-icon-512.png").convert("RGBA").resize((96, 96), Image.Resampling.LANCZOS)
    mask = rounded_mask((96, 96), 22)
    icon.putalpha(mask)
    bg.alpha_composite(icon, (80, 220))
    draw.text((200, 230), "KITE MASTER", font=font(FONT_BOLD, 72), fill=(255, 255, 255, 255))
    draw.text((200, 330), "Live wind  ·  Pech tactics  ·  Safety", font=font(FONT_SEMI, 28), fill=(0, 229, 255, 255))
    draw.text((80, 480), "The utility hub\nfor kite flyers.", font=font(FONT_BOLD, 44), fill=(255, 255, 255, 255), spacing=8)
    bg.convert("RGB").save(outfile, "PNG", optimize=True)
    print("wide", outfile.name)


def main():
    for p in (OUT, STORE, ISO, LINEUP, DL):
        p.mkdir(parents=True, exist_ok=True)

    phones = []
    for file, has_ad, slug, headline, sub in SCREENS:
        screen = crop_screen(SRC / file, has_ad)
        phone = make_phone(screen, 780)
        iso = ISO / f"phone-{slug}.png"
        phone.save(iso, "PNG")
        print("isolated", iso.name)
        store_frame(phone, headline, sub, STORE / f"{slug}.png")
        phones.append(phone)

    lineup_vertical(phones, LINEUP / "phone-lineup-9x16.png")
    lineup_wide(phones, LINEUP / "phone-lineup-16x9.png")
    # also copy wide lineup as extra banner
    Image.open(LINEUP / "phone-lineup-16x9.png").save(ROOT / "banners" / "phone-lineup-banner-1920x1080.png")
    print("done")


if __name__ == "__main__":
    main()
