#!/usr/bin/env python3
"""Build Etsy listing mockups, vertical promo video frames, and encoded MP4 for Jiya."""

from __future__ import annotations

import math
import os
import subprocess
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps

ROOT = Path("/workspace/etsy-listing")
SHOTS = ROOT / "screenshots"
ASSETS = ROOT / "assets"
MOCKUPS = ROOT / "mockups"
VIDEO = ROOT / "video"
FRAMES = VIDEO / "frames"
DEBUG = ROOT / "debug"
ART = Path("/opt/cursor/artifacts/assets")

for p in (MOCKUPS, VIDEO, FRAMES, DEBUG, ASSETS):
    p.mkdir(parents=True, exist_ok=True)

# Copy any newly generated artifacts
if ART.exists():
    for f in ART.glob("*.png"):
        dest = ASSETS / f.name
        if not dest.exists() or dest.stat().st_mtime < f.stat().st_mtime:
            dest.write_bytes(f.read_bytes())

NAVY = (28, 37, 38, 255)
NAVY_RGB = (28, 37, 38)
GOLD = (184, 148, 98, 255)
GOLD_RGB = (184, 148, 98)
CREAM = (246, 241, 232, 255)
CREAM_RGB = (246, 241, 232)
IVORY = (252, 249, 244, 255)
BLUSH = (232, 210, 190, 255)
WHITE = (255, 255, 255, 255)
CHARCOAL = (45, 45, 45, 255)
MUTED = (110, 102, 94, 255)
OK_GREEN = (90, 140, 110, 255)

SERIF = "/usr/share/fonts/truetype/noto/NotoSerifDisplay-Regular.ttf"
SERIF_B = "/usr/share/fonts/truetype/noto/NotoSerifDisplay-Bold.ttf"
SERIF_I = "/usr/share/fonts/truetype/noto/NotoSerifDisplay-Italic.ttf"
SERIF_BI = "/usr/share/fonts/truetype/noto/NotoSerifDisplay-BoldItalic.ttf"
SANS = "/usr/share/fonts/truetype/macos/Inter-Regular.ttf"
SANS_M = "/usr/share/fonts/truetype/macos/Inter-Medium.ttf"
SANS_SB = "/usr/share/fonts/truetype/macos/Inter-SemiBold.ttf"
SANS_B = "/usr/share/fonts/truetype/macos/Inter-Bold.ttf"

SHOT = {
    "dashboard": SHOTS / "ec413993-97d4-4478-ad4c-6354fb4124f8.jpg",
    "schedule": SHOTS / "34707300-fd34-4baf-b33d-8c84194286bd.jpg",
    "guests": SHOTS / "d7e5c28d-c9a7-4e28-9f92-54aa6d825558.jpg",
    "ai": SHOTS / "ae8a6ba3-a082-4271-9eda-68930a4f93b2.jpg",
    "ocr": SHOTS / "102b8714-8170-4b46-aade-dab0a92e12f7.jpg",
    "budget": SHOTS / "17c1dbac-ed40-4b4c-b4d2-e1bbaa0077c7.jpg",
    "allocation": SHOTS / "bc9d53ff-339e-4920-b071-08a4304ef14a.jpg",
}


def font(path: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size)


def load(path: Path | str) -> Image.Image:
    return Image.open(path).convert("RGBA")


def to_rgb(im: Image.Image, bg=(246, 241, 232)) -> Image.Image:
    if im.mode != "RGBA":
        return im.convert("RGB")
    base = Image.new("RGB", im.size, bg)
    base.paste(im, mask=im.split()[-1])
    return base


def save_jpg(im: Image.Image, path: Path, quality=94) -> None:
    to_rgb(im).save(path, "JPEG", quality=quality, optimize=True, subsampling=1)
    print(f"  wrote {path.name} {im.size}")


def rounded_mask(size, radius: int) -> Image.Image:
    m = Image.new("L", size, 0)
    d = ImageDraw.Draw(m)
    d.rounded_rectangle((0, 0, size[0] - 1, size[1] - 1), radius=radius, fill=255)
    return m


def drop_shadow(im: Image.Image, offset=(18, 28), blur=28, opacity=110) -> Image.Image:
    w, h = im.size
    canvas = Image.new("RGBA", (w + abs(offset[0]) + blur * 2, h + abs(offset[1]) + blur * 2), (0, 0, 0, 0))
    shadow = Image.new("RGBA", im.size, (0, 0, 0, 0))
    alpha = im.split()[-1].point(lambda p: opacity if p > 10 else 0)
    shadow.putalpha(alpha)
    sx = blur + max(offset[0], 0)
    sy = blur + max(offset[1], 0)
    canvas.paste(shadow, (sx + offset[0], sy + offset[1]), shadow)
    canvas = canvas.filter(ImageFilter.GaussianBlur(blur))
    canvas.paste(im, (sx, sy), im)
    return canvas


def iphone_mock(screenshot: Image.Image, screen_h: int = 1180) -> Image.Image:
    """Draw a graphite iPhone-style device around a real screenshot."""
    shot = screenshot.convert("RGB")
    aspect = shot.width / shot.height
    screen_w = int(screen_h * aspect)
    screen = shot.resize((screen_w, screen_h), Image.Resampling.LANCZOS)

    bezel = max(10, int(screen_w * 0.042))
    top = int(bezel * 1.15)
    bottom = int(bezel * 1.25)
    device_w = screen_w + bezel * 2
    device_h = screen_h + top + bottom
    radius = int(device_w * 0.13)
    screen_r = int(screen_w * 0.10)

    device = Image.new("RGBA", (device_w, device_h), (0, 0, 0, 0))
    d = ImageDraw.Draw(device)

    # outer metal
    d.rounded_rectangle((0, 0, device_w - 1, device_h - 1), radius=radius, fill=(42, 44, 46, 255))
    # inner highlight
    d.rounded_rectangle((2, 2, device_w - 3, device_h - 3), radius=radius - 2, fill=(58, 60, 62, 255))
    d.rounded_rectangle((4, 4, device_w - 5, device_h - 5), radius=radius - 3, fill=(22, 23, 24, 255))

    # screen well
    sx, sy = bezel, top
    well = Image.new("RGBA", (screen_w, screen_h), (0, 0, 0, 255))
    well_m = rounded_mask((screen_w, screen_h), screen_r)
    device.paste(well, (sx, sy), well_m)
    screen_rgba = screen.convert("RGBA")
    screen_rgba.putalpha(well_m)
    device.paste(screen_rgba, (sx, sy), screen_rgba)

    # dynamic island
    island_w = int(screen_w * 0.34)
    island_h = int(screen_w * 0.075)
    ix = sx + (screen_w - island_w) // 2
    iy = sy + int(screen_w * 0.028)
    d.rounded_rectangle((ix, iy, ix + island_w, iy + island_h), radius=island_h // 2, fill=(8, 8, 8, 255))

    # side buttons
    bw = max(3, int(device_w * 0.012))
    d.rounded_rectangle((-1, int(device_h * 0.18), bw, int(device_h * 0.26)), radius=2, fill=(90, 90, 92, 255))
    d.rounded_rectangle((-1, int(device_h * 0.30), bw, int(device_h * 0.40)), radius=2, fill=(90, 90, 92, 255))
    d.rounded_rectangle((device_w - bw, int(device_h * 0.28), device_w + 1, int(device_h * 0.40)), radius=2, fill=(90, 90, 92, 255))

    return device


def rotate(im: Image.Image, angle: float) -> Image.Image:
    return im.rotate(angle, resample=Image.Resampling.BICUBIC, expand=True)


def paste(base: Image.Image, overlay: Image.Image, xy, center=False) -> None:
    x, y = xy
    if center:
        x -= overlay.width // 2
        y -= overlay.height // 2
    base.alpha_composite(overlay, (int(x), int(y)))


def text_size(draw: ImageDraw.ImageDraw, text: str, fnt) -> tuple[int, int]:
    b = draw.textbbox((0, 0), text, font=fnt)
    return b[2] - b[0], b[3] - b[1]


def draw_centered(draw, text, y, fnt, fill, canvas_w, tracking=0):
    if tracking == 0:
        w, h = text_size(draw, text, fnt)
        draw.text(((canvas_w - w) / 2, y), text, font=fnt, fill=fill)
        return h
    # letterspacing
    widths = [text_size(draw, ch, fnt)[0] for ch in text]
    total = sum(widths) + tracking * (len(text) - 1)
    x = (canvas_w - total) / 2
    h = text_size(draw, text, fnt)[1]
    for ch, ww in zip(text, widths):
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += ww + tracking
    return h


def gold_rule(draw, cx, y, width, canvas_w=None):
    x0 = cx - width // 2
    draw.rectangle((x0, y, x0 + width, y + 2), fill=GOLD_RGB)


def pill(draw, text, xy, fnt, fg=NAVY_RGB, bg=(255, 255, 255, 230), pad_x=22, pad_y=10):
    tw, th = text_size(draw, text, fnt)
    x, y = xy
    box = (x, y, x + tw + pad_x * 2, y + th + pad_y * 2)
    draw.rounded_rectangle(box, radius=22, fill=bg, outline=GOLD_RGB, width=1)
    draw.text((x + pad_x, y + pad_y - 2), text, font=fnt, fill=fg)
    return box


def cover_resize(im: Image.Image, size) -> Image.Image:
    return ImageOps.fit(im, size, method=Image.Resampling.LANCZOS, centering=(0.5, 0.45))


def marble_canvas(size=(2400, 2400)) -> Image.Image:
    src = load(ASSETS / "bg-marble-texture.png")
    return cover_resize(src, size)


def floral_canvas(size=(2400, 2400)) -> Image.Image:
    src = load(ASSETS / "bg-marble-floral-square.png")
    return cover_resize(src, size)


def dim_overlay(im: Image.Image, alpha=40, color=(28, 37, 38)) -> Image.Image:
    overlay = Image.new("RGBA", im.size, (*color, alpha))
    out = im.convert("RGBA")
    out.alpha_composite(overlay)
    return out


def cream_panel(size, radius=36, fill=(255, 255, 255, 210)) -> Image.Image:
    p = Image.new("RGBA", size, (0, 0, 0, 0))
    d = ImageDraw.Draw(p)
    d.rounded_rectangle((0, 0, size[0] - 1, size[1] - 1), radius=radius, fill=fill)
    d.rounded_rectangle((1, 1, size[0] - 2, size[1] - 2), radius=radius, outline=(184, 148, 98, 90), width=2)
    return p


def order_quad(pts: np.ndarray) -> np.ndarray:
    pts = np.array(pts, dtype=np.float32)
    s = pts.sum(axis=1)
    diff = np.diff(pts, axis=1).reshape(-1)
    tl = pts[np.argmin(s)]
    br = pts[np.argmax(s)]
    tr = pts[np.argmin(diff)]
    bl = pts[np.argmax(diff)]
    return np.array([tl, tr, br, bl], dtype=np.float32)


def inset_quad(quad: np.ndarray, frac=0.035) -> np.ndarray:
    c = quad.mean(axis=0)
    return c + (quad - c) * (1 - frac)


def find_black_quads(img_rgb: Image.Image, min_area_frac=0.03) -> list[np.ndarray]:
    arr = np.array(img_rgb.convert("RGB"))
    bgr = cv2.cvtColor(arr, cv2.COLOR_RGB2BGR)
    mask = cv2.inRange(bgr, (0, 0, 0), (38, 38, 38))
    k = cv2.getStructuringElement(cv2.MORPH_RECT, (11, 11))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, k, iterations=2)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, k, iterations=1)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    h, w = mask.shape
    min_area = w * h * min_area_frac
    quads = []
    for c in contours:
        area = cv2.contourArea(c)
        if area < min_area:
            continue
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        if len(approx) == 4:
            q = order_quad(approx.reshape(4, 2))
        else:
            rect = cv2.minAreaRect(c)
            q = order_quad(cv2.boxPoints(rect))
        # phone-like aspect
        width = np.linalg.norm(q[0] - q[1])
        height = np.linalg.norm(q[0] - q[3])
        if height < 1 or width < 1:
            continue
        aspect = height / width
        if 1.4 < aspect < 2.6:
            quads.append(inset_quad(q, 0.03))
    quads.sort(key=lambda q: q[0][0])
    return quads


def warp_screenshot_onto(bg: Image.Image, shot: Image.Image, quad: np.ndarray) -> Image.Image:
    canvas = np.array(bg.convert("RGBA"))
    src = np.array(shot.convert("RGBA"))
    sh, sw = src.shape[:2]
    src_pts = np.float32([[0, 0], [sw, 0], [sw, sh], [0, sh]])
    M = cv2.getPerspectiveTransform(src_pts, quad.astype(np.float32))
    warped = cv2.warpPerspective(src, M, (canvas.shape[1], canvas.shape[0]), flags=cv2.INTER_LINEAR)
    # mask of warped content
    gray = cv2.cvtColor(warped[..., :3], cv2.COLOR_RGB2GRAY)
    alpha = warped[..., 3]
    mask = (alpha > 8).astype(np.uint8) * 255
    # feather
    mask = cv2.GaussianBlur(mask, (5, 5), 0)
    inv = (255 - mask).astype(np.float32) / 255.0
    m = mask.astype(np.float32) / 255.0
    out = canvas.astype(np.float32)
    warped_f = warped.astype(np.float32)
    for i in range(4):
        out[..., i] = out[..., i] * inv + warped_f[..., i] * m
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8), "RGBA")


def composite_phones(bg_path: Path, shot_keys: list[str], out_name: str) -> Image.Image | None:
    bg = load(bg_path)
    quads = find_black_quads(bg, min_area_frac=0.02 if len(shot_keys) > 1 else 0.04)
    debug = bg.copy()
    dd = ImageDraw.Draw(debug)
    for i, q in enumerate(quads):
        dd.polygon([tuple(p) for p in q], outline=(255, 0, 0, 255))
        dd.text(tuple(q[0]), str(i), fill=(255, 0, 0, 255), font=font(SANS_B, 28))
    debug.convert("RGB").save(DEBUG / f"{out_name}_quads.jpg", quality=85)
    print(f"  {out_name}: found {len(quads)} phone screens (wanted {len(shot_keys)})")
    if len(quads) < len(shot_keys):
        return None
    # pick largest N
    quads = sorted(quads, key=lambda q: cv2.contourArea(q.astype(np.int32)), reverse=True)[: len(shot_keys)]
    quads = sorted(quads, key=lambda q: q[:, 0].mean())
    out = bg
    for q, key in zip(quads, shot_keys):
        out = warp_screenshot_onto(out, load(SHOT[key]), q)
    return out


# ---------------------------------------------------------------------------
# Listing images
# ---------------------------------------------------------------------------

def listing_01_hero():
    W = H = 2400
    base = floral_canvas((W, H))
    # soft vignette so phones pop
    vig = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    vd = ImageDraw.Draw(vig)
    vd.rectangle((0, 0, W, 420), fill=(246, 241, 232, 70))
    vd.rectangle((0, H - 380, W, H), fill=(246, 241, 232, 90))
    base.alpha_composite(vig)

    dash = drop_shadow(rotate(iphone_mock(load(SHOT["dashboard"]), 1280), -9), (10, 30), 32, 120)
    sched = drop_shadow(iphone_mock(load(SHOT["schedule"]), 1380), (0, 36), 36, 140)
    guests = drop_shadow(rotate(iphone_mock(load(SHOT["guests"]), 1280), 9), (10, 30), 32, 120)

    paste(base, dash, (W * 0.27, H * 0.54), center=True)
    paste(base, guests, (W * 0.73, H * 0.54), center=True)
    paste(base, sched, (W * 0.50, H * 0.52), center=True)

    d = ImageDraw.Draw(base)
    draw_centered(d, "Jiya", 70, font(SERIF_B, 52), GOLD_RGB, W)
    draw_centered(d, "The Desi Wedding Planner", 140, font(SERIF_B, 78), NAVY_RGB, W)
    draw_centered(d, "Mehndi  ·  Barat  ·  Nikkah  ·  Walima", 250, font(SANS_M, 32), MUTED[:3], W)
    gold_rule(d, W // 2, 318, 180)

    # bottom feature strip
    strip = cream_panel((1960, 92), 46, (255, 255, 255, 225))
    paste(base, strip, (W // 2, H - 118), center=True)
    draw_centered(
        d,
        "AI Studio   ·   Budget & OCR   ·   RSVPs & Seating   ·   Multi-Event Run Sheets",
        H - 148,
        font(SANS_M, 28),
        NAVY_RGB,
        W,
    )
    save_jpg(base, MOCKUPS / "01-hero-three-phones.jpg")


def listing_02_lifestyle_dashboard():
    preferred = MOCKUPS / "composite-hand-dashboard.png"
    src_path = preferred if preferred.exists() else ASSETS / "ai-hand-dashboard.png"
    src = cover_resize(load(src_path), (2000, 2667))
    # square crop for etsy + keep a 4:5 version
    sq = ImageOps.fit(src, (2400, 2400), centering=(0.5, 0.42))
    overlay = Image.new("RGBA", sq.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    d.rectangle((0, 2120, 2400, 2400), fill=(28, 37, 38, 210))
    sq.alpha_composite(overlay)
    d = ImageDraw.Draw(sq)
    draw_centered(d, "Budget, countdown & RSVPs — at a glance", 2200, font(SERIF_I, 42), CREAM_RGB[:3], 2400)
    draw_centered(d, "Designed for multi-day South Asian weddings", 2278, font(SANS, 26), (220, 208, 190), 2400)
    save_jpg(sq, MOCKUPS / "02-lifestyle-dashboard.jpg")
    src.save(MOCKUPS / "02b-lifestyle-dashboard-portrait.png")


def listing_03_whats_included():
    W = H = 2400
    base = marble_canvas((W, H))
    veil = Image.new("RGBA", (W, H), (252, 249, 244, 70))
    base.alpha_composite(veil)
    d = ImageDraw.Draw(base)
    draw_centered(d, "WHAT'S INSIDE", 70, font(SANS_M, 26), GOLD_RGB, W, tracking=10)
    draw_centered(d, "One planner for the whole shaadi", 118, font(SERIF_B, 64), NAVY_RGB, W)
    gold_rule(d, W // 2, 210, 140)

    items = [
        ("dashboard", "Command Dashboard", "Budget, countdown & quick actions"),
        ("schedule", "Multi-Event Schedule", "Mehndi, Barat, Nikkah, Walima"),
        ("allocation", "Smart Budget Engine", "Auto-allocation by category"),
        ("ocr", "AI / OCR Scanner", "Snap receipts, log expenses"),
        ("guests", "Guests & RSVPs", "CSV import + seating canvas"),
        ("ai", "AI Wedding Studio", "Themes, décor & attire advice"),
    ]
    phones = []
    for key, _, _ in items:
        phones.append(iphone_mock(load(SHOT[key]), 620))

    # 2 rows of 3
    positions = [
        (420, 620),
        (1200, 620),
        (1980, 620),
        (420, 1480),
        (1200, 1480),
        (1980, 1480),
    ]
    for (x, y), phone, (_, title, sub) in zip(positions, phones, items):
        p = drop_shadow(phone, (8, 16), 20, 90)
        paste(base, p, (x, y - 40), center=True)
        tw, _ = text_size(d, title, font(SANS_SB, 28))
        d.text((x - tw / 2, y + 300), title, font=font(SANS_SB, 28), fill=NAVY_RGB)
        sw, _ = text_size(d, sub, font(SANS, 20))
        d.text((x - sw / 2, y + 340), sub, font=font(SANS, 20), fill=MUTED[:3])

    save_jpg(base, MOCKUPS / "03-whats-included.jpg")


def listing_04_schedule():
    W = H = 2400
    # prefer composited real screenshot if possible
    photo = None
    empty = ASSETS / "bg-single-phone-desk.png"
    if empty.exists():
        photo = composite_phones(empty, ["schedule"], "schedule-desk")
    if photo is None:
        photo = load(ASSETS / "ai-schedule-desk.png")
    base = cover_resize(photo, (W, H))
    panel = cream_panel((1040, 2100), 40, (255, 252, 248, 232))
    paste(base, panel, (28, 150))
    d = ImageDraw.Draw(base)
    x = 90
    d.text((x, 220), "MULTI-EVENT", font=font(SANS_M, 24), fill=GOLD_RGB)
    d.text((x, 270), "Master every\nfunction day", font=font(SERIF_B, 62), fill=NAVY_RGB)
    d.rectangle((x, 500, x + 90, 503), fill=GOLD_RGB)
    bullets = [
        ("Mehndi Night", "Venue, lead & run-sheet progress"),
        ("Barat & Nikkah", "Ceremony countdown + 50% tracker"),
        ("Walima Reception", "Separate lead, venue & timeline"),
        ("Family leads", "Assign Uncle, Aunt, cousin as owners"),
        ("One tap add", "Grow the schedule as events lock in"),
    ]
    y = 560
    for title, sub in bullets:
        d.ellipse((x, y + 10, x + 14, y + 24), fill=GOLD_RGB)
        d.text((x + 36, y), title, font=font(SANS_SB, 30), fill=NAVY_RGB)
        d.text((x + 36, y + 42), sub, font=font(SANS, 22), fill=MUTED[:3])
        y += 130
    d.text((x, 1980), "Built for Desi multi-day weddings", font=font(SERIF_I, 26), fill=GOLD_RGB)
    save_jpg(base, MOCKUPS / "04-multi-event-schedule.jpg")


def listing_05_budget_ocr():
    W = H = 2400
    base = floral_canvas((W, H))
    veil = Image.new("RGBA", (W, H), (246, 241, 232, 40))
    base.alpha_composite(veil)
    d = ImageDraw.Draw(base)
    draw_centered(d, "MONEY, WITHOUT THE CHAOS", 70, font(SANS_M, 24), GOLD_RGB, W, tracking=8)
    draw_centered(d, "Budget calculator + receipt OCR", 120, font(SERIF_B, 58), NAVY_RGB, W)

    left = drop_shadow(rotate(iphone_mock(load(SHOT["budget"]), 1240), -6), (12, 28), 28, 120)
    right = drop_shadow(rotate(iphone_mock(load(SHOT["ocr"]), 1240), 6), (12, 28), 28, 120)
    paste(base, left, (W * 0.30, H * 0.54), center=True)
    paste(base, right, (W * 0.70, H * 0.54), center=True)

    # captions
    cap_f = font(SANS_SB, 26)
    draw_centered(d, "Auto-allocation & rebalancing", H - 160, font(SANS_M, 26), NAVY_RGB, W)
    save_jpg(base, MOCKUPS / "05-budget-and-ocr.jpg")


def listing_06_guests():
    W = H = 2400
    photo = cover_resize(load(ASSETS / "ai-hand-guests.png"), (W, H))
    # left text panel
    panel = cream_panel((1020, 2100), 40, (255, 252, 248, 228))
    paste(photo, panel, (40, 150))
    d = ImageDraw.Draw(photo)
    x = 100
    d.text((x, 230), "GUESTS  ·  RSVPs  ·  SEATING", font=font(SANS_M, 22), fill=GOLD_RGB)
    d.text((x, 290), "Your full\nguest office", font=font(SERIF_B, 60), fill=NAVY_RGB)
    d.rectangle((x, 530, x + 90, 533), fill=GOLD_RGB)
    bullets = [
        "Searchable guest list",
        "One-tap Add Guest",
        "CSV import for big baraats",
        "Seating canvas for halls",
        "Confirmed / declined / pending",
        "Digital RSVP tracking",
    ]
    y = 590
    for b in bullets:
        d.ellipse((x, y + 12, x + 14, y + 26), fill=GOLD_RGB)
        d.text((x + 36, y), b, font=font(SANS, 30), fill=NAVY_RGB)
        y += 88
    save_jpg(photo, MOCKUPS / "06-guests-rsvp-seating.jpg")


def listing_07_ai_studio():
    W = H = 2400
    photo = cover_resize(load(ASSETS / "ai-vertical-ai-assistant.png"), (W, H))
    # bottom caption bar
    bar = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    bd = ImageDraw.Draw(bar)
    bd.rectangle((0, 0, W, 280), fill=(28, 37, 38, 200))
    photo.alpha_composite(bar)
    d = ImageDraw.Draw(photo)
    draw_centered(d, "SMART AI WEDDING ASSISTANT", 48, font(SANS_M, 22), GOLD_RGB, W, tracking=6)
    draw_centered(d, "Ask for pastel Barat themes. Add the task. Done.", 110, font(SERIF_I, 40), CREAM_RGB[:3], W)
    draw_centered(d, "Context-aware décor, attire & checklist advice", 190, font(SANS, 24), (220, 208, 190), W)
    save_jpg(photo, MOCKUPS / "07-ai-wedding-studio.jpg")


def listing_08_features():
    W = H = 2400
    base = marble_canvas((W, H))
    veil = Image.new("RGBA", (W, H), (252, 249, 244, 80))
    base.alpha_composite(veil)
    d = ImageDraw.Draw(base)
    draw_centered(d, "Jiya", 64, font(SERIF_I, 42), GOLD_RGB, W)
    draw_centered(d, "Everything a Desi wedding needs", 130, font(SERIF_B, 56), NAVY_RGB, W)
    gold_rule(d, W // 2, 220, 140)

    cards = [
        ("01", "Multi-event timeline", "Separate Mehndi, Barat, Nikkah and Walima with venues, leads and run-sheet %."),
        ("02", "Live budget health", "$50k-ready categories, remaining cash, and green OK badges under 80%."),
        ("03", "OCR expense capture", "Photograph invoices — vendor, total and tax extract, then log in one tap."),
        ("04", "Guest command center", "Search, CSV import, digital RSVPs and a seating canvas for big halls."),
        ("05", "AI planning studio", "Theme, décor and attire prompts that understand daytime Barat culture."),
        ("06", "Family-proof workflow", "Assign Uncle Tariq, Aunt Sara, Cousin Ali — everyone owns a lane."),
    ]
    cols, rows = 2, 3
    gap_x, gap_y = 48, 40
    margin = 90
    card_w = (W - margin * 2 - gap_x) // 2
    card_h = 560
    start_y = 280
    for i, (num, title, body) in enumerate(cards):
        c, r = i % cols, i // cols
        x = margin + c * (card_w + gap_x)
        y = start_y + r * (card_h + gap_y)
        card = cream_panel((card_w, card_h), 28, (255, 255, 255, 230))
        paste(base, card, (x, y))
        d.text((x + 40, y + 36), num, font=font(SERIF_I, 36), fill=GOLD_RGB)
        d.text((x + 40, y + 110), title, font=font(SANS_SB, 34), fill=NAVY_RGB)
        # wrap body
        words = body.split()
        lines, cur = [], ""
        fnt = font(SANS, 24)
        for w in words:
            test = (cur + " " + w).strip()
            if text_size(d, test, fnt)[0] < card_w - 80:
                cur = test
            else:
                lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
        yy = y + 180
        for line in lines:
            d.text((x + 40, yy), line, font=fnt, fill=MUTED[:3])
            yy += 38
    save_jpg(base, MOCKUPS / "08-feature-grid.jpg")


def listing_09_who():
    W = H = 2400
    photo = cover_resize(load(ASSETS / "ai-hero-three-phones.png"), (W, H))
    dim = Image.new("RGBA", (W, H), (28, 37, 38, 70))
    photo.alpha_composite(dim)
    panel = cream_panel((2100, 1680), 36, (255, 252, 248, 236))
    paste(photo, panel, (W // 2, H // 2 + 40), center=True)
    d = ImageDraw.Draw(photo)
    draw_centered(d, "WHO IT'S FOR", 430, font(SANS_M, 24), GOLD_RGB, W, tracking=8)
    draw_centered(d, "Made for real Desi weddings", 490, font(SERIF_B, 56), NAVY_RGB, W)
    gold_rule(d, W // 2, 580, 120)
    rows = [
        ("The couple", "Track every rupee, guest and function without 14 WhatsApp groups."),
        ("The family committee", "Give each event a named lead — Mehndi, Barat, Walima stay owned."),
        ("Planners & coordinators", "Run sheets, seating canvas, vendors and OCR receipts in one mobile hub."),
        ("NRI & destination shaadis", "USD budget, multi-venue, countdown to Barat — plan from anywhere."),
    ]
    y = 640
    for title, body in rows:
        d.text((280, y), "✦  " + title, font=font(SANS_SB, 32), fill=NAVY_RGB)
        d.text((340, y + 52), body, font=font(SANS, 24), fill=MUTED[:3])
        y += 170
    save_jpg(photo, MOCKUPS / "09-who-its-for.jpg")


def listing_10_how():
    W = H = 2400
    base = floral_canvas((W, H))
    veil = Image.new("RGBA", (W, H), (246, 241, 232, 55))
    base.alpha_composite(veil)
    d = ImageDraw.Draw(base)
    draw_centered(d, "HOW IT WORKS", 80, font(SANS_M, 24), GOLD_RGB, W, tracking=8)
    draw_centered(d, "Download. Plan. Breathe.", 140, font(SERIF_B, 64), NAVY_RGB, W)

    steps = [
        ("1", "Open Jiya", "Set your target budget, currency and wedding scale."),
        ("2", "Add every event", "Mehndi, Barat, Nikkah, Walima — venues and family leads."),
        ("3", "Fill the guest world", "CSV import, RSVPs, seating canvas."),
        ("4", "Ask the studio", "AI themes, décor, attire — tap to add tasks."),
    ]
    y = 280
    for num, title, body in steps:
        card = cream_panel((2040, 280), 28, (255, 255, 255, 225))
        paste(base, card, (180, y))
        # number circle
        d.ellipse((230, y + 78, 330, y + 178), outline=GOLD_RGB, width=3)
        nw, nh = text_size(d, num, font(SERIF_B, 40))
        d.text((280 - nw / 2, y + 100), num, font=font(SERIF_B, 40), fill=NAVY_RGB)
        d.text((380, y + 70), title, font=font(SANS_SB, 36), fill=NAVY_RGB)
        d.text((380, y + 130), body, font=font(SANS, 26), fill=MUTED[:3])
        y += 310

    draw_centered(d, "Instant digital download  ·  Mobile-first  ·  Keep forever", 2140, font(SANS_M, 26), NAVY_RGB, W)
    save_jpg(base, MOCKUPS / "10-how-it-works.jpg")


def extra_collage_and_pinterest():
    """Bonus listing/Pinterest assets."""
    W, H = 2400, 2400
    base = marble_canvas((W, H))
    d = ImageDraw.Draw(base)
    draw_centered(d, "Jiya  ·  Desi Wedding Planner", 80, font(SANS_M, 26), GOLD_RGB, W)
    phones = [
        drop_shadow(rotate(iphone_mock(load(SHOT["dashboard"]), 980), -14), (8, 22), 24, 110),
        drop_shadow(rotate(iphone_mock(load(SHOT["schedule"]), 1040), -5), (8, 22), 24, 110),
        drop_shadow(iphone_mock(load(SHOT["ai"]), 1100), (0, 24), 26, 120),
        drop_shadow(rotate(iphone_mock(load(SHOT["ocr"]), 1040), 5), (8, 22), 24, 110),
        drop_shadow(rotate(iphone_mock(load(SHOT["guests"]), 980), 14), (8, 22), 24, 110),
    ]
    xs = [0.14, 0.32, 0.50, 0.68, 0.86]
    for p, x in zip(phones, xs):
        paste(base, p, (W * x, H * 0.52), center=True)
    draw_centered(d, "7 screens. One calm plan.", 2140, font(SERIF_I, 44), NAVY_RGB, W)
    save_jpg(base, MOCKUPS / "11-screen-collage.jpg")

    # Pinterest 1000x1500-ish 2:3
    pin_w, pin_h = 1600, 2400
    pin = floral_canvas((pin_w, pin_h))
    phone = drop_shadow(iphone_mock(load(SHOT["dashboard"]), 1500), (0, 40), 36, 130)
    paste(pin, phone, (pin_w // 2, pin_h * 0.55), center=True)
    pd = ImageDraw.Draw(pin)
    draw_centered(pd, "Jiya", 90, font(SERIF_I, 40), GOLD_RGB, pin_w)
    draw_centered(pd, "The Desi Wedding\nPlanner App", 150, font(SERIF_B, 64), NAVY_RGB, pin_w)
    save_jpg(pin, MOCKUPS / "pinterest-desi-wedding-planner.jpg")


def composite_lifestyle_extras():
    mapping = [
        (ASSETS / "bg-hand-holding-empty-phone.png", ["dashboard"], "composite-hand-dashboard"),
        (ASSETS / "bg-vertical-hand-phone.png", ["ai"], "composite-hand-ai"),
        (ASSETS / "bg-vertical-bridal-scene.png", ["dashboard"], "composite-vertical-dashboard"),
        (ASSETS / "bg-desk-three-phones-empty.png", ["schedule", "dashboard", "guests"], "composite-three-phones"),
        (ASSETS / "bg-single-phone-desk.png", ["allocation"], "composite-allocation"),
        (ASSETS / "bg-desk-two-phones.png", ["budget", "ocr"], "composite-two-finance"),
    ]
    for path, keys, name in mapping:
        if not path.exists():
            print(f"  skip missing {path.name}")
            continue
        out = composite_phones(path, keys, name)
        if out is None:
            continue
        save_jpg(out, MOCKUPS / f"{name}.jpg")
        out.save(MOCKUPS / f"{name}.png")


# ---------------------------------------------------------------------------
# Vertical video
# ---------------------------------------------------------------------------

def vertical_title_card() -> Image.Image:
    W, H = 1080, 1920
    base = floral_canvas((W, H))
    dim = Image.new("RGBA", (W, H), (28, 37, 38, 88))
    base.alpha_composite(dim)
    d = ImageDraw.Draw(base)
    draw_centered(d, "Jiya", 640, font(SERIF_B, 56), GOLD_RGB, W)
    gold_rule(d, W // 2, 730, 90)
    draw_centered(d, "Plan the whole shaadi", 770, font(SERIF_B, 56), CREAM_RGB[:3], W)
    draw_centered(d, "in one calm app", 850, font(SERIF_I, 46), CREAM_RGB[:3], W)
    draw_centered(d, "Mehndi  ·  Barat  ·  Nikkah  ·  Walima", 1020, font(SANS_M, 24), (220, 208, 190), W)
    return base


def vertical_end_card() -> Image.Image:
    W, H = 1080, 1920
    base = floral_canvas((W, H))
    veil = Image.new("RGBA", (W, H), (28, 37, 38, 70))
    base.alpha_composite(veil)
    phone = drop_shadow(iphone_mock(load(SHOT["dashboard"]), 980), (0, 28), 28, 130)
    paste(base, phone, (W // 2, 900), center=True)
    d = ImageDraw.Draw(base)
    draw_centered(d, "Jiya", 150, font(SERIF_B, 48), GOLD_RGB, W)
    draw_centered(d, "The Desi Wedding Planner", 230, font(SERIF_B, 42), NAVY_RGB, W)
    draw_centered(d, "Instant download on Etsy", 1680, font(SANS_SB, 28), NAVY_RGB, W)
    draw_centered(d, "AI  ·  Budget OCR  ·  RSVPs  ·  Run sheets", 1740, font(SANS, 22), MUTED[:3], W)
    return base


def vertical_feature(shot_key: str, kicker: str, headline: str, sub: str, photo: Path | None = None) -> Image.Image:
    W, H = 1080, 1920
    if photo and photo.exists():
        base = cover_resize(load(photo), (W, H))
        dim = Image.new("RGBA", (W, H), (246, 241, 232, 30))
        base.alpha_composite(dim)
    else:
        base = floral_canvas((W, H))
    phone = drop_shadow(iphone_mock(load(SHOT[shot_key]), 1120), (0, 30), 30, 130)
    paste(base, phone, (W // 2, 980), center=True)
    d = ImageDraw.Draw(base)
    draw_centered(d, kicker, 90, font(SANS_M, 20), GOLD_RGB, W, tracking=6)
    draw_centered(d, headline, 140, font(SERIF_B, 44), NAVY_RGB, W)
    draw_centered(d, sub, 220, font(SANS, 22), MUTED[:3], W)
    return base


def ken_burns_clip(im: Image.Image, seconds: float, fps=30, zoom_end=1.08) -> list[Image.Image]:
    """Return RGB frames with a slow zoom-in."""
    n = int(seconds * fps)
    rgb = to_rgb(im)
    W, H = rgb.size
    frames = []
    for i in range(n):
        t = i / max(n - 1, 1)
        z = 1.0 + (zoom_end - 1.0) * t
        cw, ch = int(W / z), int(H / z)
        # slight pan upward
        left = (W - cw) // 2
        top = int((H - ch) * (0.35 + 0.15 * t))
        crop = rgb.crop((left, top, left + cw, top + ch)).resize((W, H), Image.Resampling.BILINEAR)
        frames.append(crop)
    return frames


def build_video():
    print("Building vertical video frames…")
    slides = [
        (vertical_title_card(), 2.4),
        (
            vertical_feature(
                "dashboard",
                "DASHBOARD",
                "Your shaadi, on one screen",
                "$50k budget  ·  114 days to Barat  ·  RSVPs",
                ASSETS / "ai-hand-dashboard.png",
            ),
            2.8,
        ),
        (
            vertical_feature(
                "schedule",
                "MULTI-EVENT",
                "Mehndi. Barat. Walima.",
                "Venues, family leads & run-sheet progress",
                ASSETS / "ai-schedule-desk.png",
            ),
            2.8,
        ),
        (
            vertical_feature(
                "ocr",
                "BUDGET + OCR",
                "Snap the receipt. Logged.",
                "Auto-allocation  ·  vendor, tax & total",
                None,
            ),
            2.6,
        ),
        (
            vertical_feature(
                "guests",
                "GUESTS",
                "RSVPs & seating canvas",
                "CSV import for the full baraat",
                ASSETS / "ai-hand-guests.png",
            ),
            2.6,
        ),
        (
            vertical_feature(
                "ai",
                "AI STUDIO",
                "Ask for a pastel Barat",
                "Themes, décor, attire — then add the task",
                ASSETS / "ai-vertical-ai-assistant.png",
            ),
            2.8,
        ),
        (vertical_end_card(), 2.6),
    ]

    # save stills for review
    for i, (im, _) in enumerate(slides, 1):
        save_jpg(im, VIDEO / f"slide-{i:02d}.jpg")

    fps = 30
    raw_frames: list[Image.Image] = []
    for im, sec in slides:
        raw_frames.extend(ken_burns_clip(im, sec, fps=fps, zoom_end=1.07))

    # crossfade 10 frames between clips would be nicer; simple concat is OK
    # Write numbered pngs
    for i, fr in enumerate(raw_frames):
        fr.save(FRAMES / f"f{i:04d}.jpg", quality=88, optimize=True)
    print(f"  {len(raw_frames)} frames @ {fps} fps")

    out = VIDEO / "jiya-desi-wedding-planner-vertical.mp4"
    cmd = [
        "ffmpeg",
        "-y",
        "-framerate",
        str(fps),
        "-i",
        str(FRAMES / "f%04d.jpg"),
        "-c:v",
        "libx264",
        "-pix_fmt",
        "yuv420p",
        "-vf",
        "scale=1080:1920",
        "-crf",
        "18",
        "-movflags",
        "+faststart",
        str(out),
    ]
    subprocess.check_call(cmd)
    print(f"  video -> {out}")


def copy_ai_lifestyle():
    names = [
        "ai-hero-three-phones.png",
        "ai-hand-dashboard.png",
        "ai-vertical-ai-assistant.png",
        "ai-schedule-desk.png",
        "ai-budget-desk.png",
        "ai-ocr-desk.png",
        "ai-hand-guests.png",
    ]
    for n in names:
        src = ASSETS / n
        if src.exists():
            im = load(src)
            save_jpg(im, MOCKUPS / n.replace(".png", "-raw.jpg"))


def main():
    print("=== Compositing real screenshots onto lifestyle photos ===")
    composite_lifestyle_extras()
    print("=== Designed listing mockups ===")
    listing_01_hero()
    listing_02_lifestyle_dashboard()
    listing_03_whats_included()
    listing_04_schedule()
    listing_05_budget_ocr()
    listing_06_guests()
    listing_07_ai_studio()
    listing_08_features()
    listing_09_who()
    listing_10_how()
    extra_collage_and_pinterest()
    copy_ai_lifestyle()
    print("=== Vertical video ===")
    build_video()
    print("DONE")


if __name__ == "__main__":
    main()
