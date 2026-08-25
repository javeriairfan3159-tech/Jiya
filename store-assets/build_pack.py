#!/usr/bin/env python3
"""Build Play Store / App Store marketing pack for Kite Master."""

from __future__ import annotations

import math
import os
import shutil
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent
SRC_SCREENS = ROOT / "source" / "app-screens"
SRC_GEN = ROOT / "source" / "generated"
OUT_ICON = ROOT / "icon"
OUT_BANNER = ROOT / "banners"
OUT_SS = ROOT / "screenshots"
OUT_VID = ROOT / "videos"
TMP = ROOT / ".build-tmp"

FONT_BOLD = "/usr/share/fonts/truetype/macos/Inter-Bold.ttf"
FONT_SEMI = "/usr/share/fonts/truetype/macos/Inter-SemiBold.ttf"
FONT_REG = "/usr/share/fonts/truetype/macos/Inter-Regular.ttf"

# Original captures (738x1599)
HOME = SRC_SCREENS / "832582d9-75e4-4519-ad1e-4e9ef9ec807a.jpg"
DASH = SRC_SCREENS / "287cb277-a1b6-4318-8f4f-a07c0aaf345b.jpg"
MASTER = SRC_SCREENS / "37227092-2eaf-4232-9884-3fc71b789cfb.jpg"
SAFETY = SRC_SCREENS / "00412e44-bfc0-406e-b5e8-b0a8cd0e21ce.jpg"
ACHIEVE = SRC_SCREENS / "ec086674-1c36-4dea-9e7b-fd7929b18cbe.jpg"

BG = (10, 6, 18)
CYAN = (0, 229, 255)
MAGENTA = (232, 70, 255)
WHITE = (255, 255, 255)
MUTED = (186, 176, 214)


def font(path: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size)


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(len(a)))


def vertical_gradient(size, top, bottom):
    w, h = size
    img = Image.new("RGB", size, top)
    px = img.load()
    for y in range(h):
        c = lerp(top, bottom, y / max(h - 1, 1))
        for x in range(w):
            px[x, y] = c
    return img


def radial_glow(base: Image.Image, center, radius, color, strength=0.55):
    overlay = Image.new("RGBA", base.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    cx, cy = center
    steps = 36
    for i in range(steps, 0, -1):
        t = i / steps
        r = int(radius * t)
        a = int(255 * strength * (1 - t) ** 2)
        draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(*color, a))
    overlay = overlay.filter(ImageFilter.GaussianBlur(42))
    out = base.convert("RGBA")
    out.alpha_composite(overlay)
    return out


def rounded_mask(size, radius):
    m = Image.new("L", size, 0)
    d = ImageDraw.Draw(m)
    d.rounded_rectangle((0, 0, size[0] - 1, size[1] - 1), radius=radius, fill=255)
    return m


def paste_rounded(dst, src, xy, radius, outline=None, outline_width=3):
    x, y = xy
    w, h = src.size
    mask = rounded_mask((w, h), radius)
    dst.paste(src, (x, y), mask)
    if outline:
        ring = Image.new("RGBA", dst.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(ring)
        d.rounded_rectangle(
            (x, y, x + w - 1, y + h - 1),
            radius=radius,
            outline=outline,
            width=outline_width,
        )
        dst.alpha_composite(ring)


def text_center(draw, xy, text, fnt, fill, stroke=None):
    x, y = xy
    bbox = draw.textbbox((0, 0), text, font=fnt)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    kw = {"stroke_width": 2, "stroke_fill": (0, 0, 0, 160)} if stroke else {}
    draw.text((x - tw / 2, y), text, font=fnt, fill=fill, **kw)
    return th


def wrap_center(draw, y, text, fnt, fill, max_width, canvas_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    for line in lines:
        h = text_center(draw, (canvas_w / 2, y), line, fnt, fill)
        y += h + 10
    return y


def crop_app_screen(path: Path, has_ad: bool) -> Image.Image:
    im = Image.open(path).convert("RGB")
    w, h = im.size
    top = 52  # status bar
    bottom = 1456 if has_ad else 1564  # ads / home indicator
    return im.crop((0, top, w, min(bottom, h)))


def make_phone_shot(screen: Image.Image, phone_w=780) -> Image.Image:
    ratio = screen.height / screen.width
    phone_h = int(phone_w * ratio)
    screen_r = screen.resize((phone_w, phone_h), Image.Resampling.LANCZOS)
    pad = 14
    bezel = Image.new("RGB", (phone_w + pad * 2, phone_h + pad * 2), (6, 4, 12))
    bezel.paste(screen_r, (pad, pad))
    return bezel


def store_screenshot(screen: Image.Image, headline: str, sub: str, accent, outfile: Path):
    W, H = 1080, 1920
    bg = vertical_gradient((W, H), (8, 5, 16), (18, 8, 36))
    bg = radial_glow(bg, (280, 240), 520, MAGENTA, 0.38)
    bg = radial_glow(bg, (820, 860), 640, CYAN, 0.32)
    bg = radial_glow(bg, (540, 1700), 420, accent, 0.22)

    phone = make_phone_shot(screen, 780)
    max_h = 1280
    if phone.height > max_h:
        s = max_h / phone.height
        phone = phone.resize((int(phone.width * s), max_h), Image.Resampling.LANCZOS)

    px = (W - phone.width) // 2
    py = 430

    # glow behind phone
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.rounded_rectangle(
        (px - 30, py - 30, px + phone.width + 30, py + phone.height + 30),
        radius=70,
        fill=(*accent, 70),
    )
    glow = glow.filter(ImageFilter.GaussianBlur(28))
    bg.alpha_composite(glow)

    paste_rounded(bg, phone.convert("RGBA"), (px, py), 48, outline=(*accent, 220), outline_width=4)

    draw = ImageDraw.Draw(bg)
    brand = font(FONT_SEMI, 28)
    h1 = font(FONT_BOLD, 62)
    h2 = font(FONT_REG, 30)

    text_center(draw, (W / 2, 78), "KITE MASTER", brand, CYAN)
    y = 140
    y = wrap_center(draw, y, headline, h1, WHITE, 940, W)
    wrap_center(draw, y + 18, sub, h2, MUTED, 900, W)

    bg.convert("RGB").save(outfile, "PNG", optimize=True)
    print("wrote", outfile)


def make_icons():
    src = Image.open(SRC_GEN / "kite-master-icon-clean.png").convert("RGBA")
    # tighten: crop a bit of empty margin then fit
    for size, name in [(1024, "kite-master-icon-1024.png"), (512, "kite-master-icon-512.png")]:
        canvas = Image.new("RGBA", (size, size), (10, 6, 18, 255))
        icon = src.resize((size, size), Image.Resampling.LANCZOS)
        canvas.alpha_composite(icon)
        out = OUT_ICON / name
        canvas.convert("RGB").save(out, "PNG", optimize=True)
        print("wrote", out)
    shutil.copy2(SRC_GEN / "kite-master-icon-alt.png", OUT_ICON / "kite-master-icon-alt-1024.png")
    shutil.copy2(SRC_GEN / "kite-master-icon.png", OUT_ICON / "kite-master-icon-neon-1024.png")


def make_feature_graphic():
    """Exact Play Store 1024x500 feature graphic using the real home screen."""
    W, H = 1024, 500
    bg = vertical_gradient((W, H), (8, 5, 18), (16, 8, 40))
    bg = radial_glow(bg, (780, 250), 380, (140, 40, 255), 0.5)
    bg = radial_glow(bg, (780, 250), 260, CYAN, 0.28)

    draw = ImageDraw.Draw(bg)
    icon = Image.open(SRC_GEN / "kite-master-icon-clean.png").convert("RGBA").resize((88, 88), Image.Resampling.LANCZOS)
    bg.alpha_composite(icon, (48, 70))

    draw.text((150, 84), "KITE MASTER", font=font(FONT_BOLD, 54), fill=WHITE)
    draw.text((150, 154), "Live wind  •  Pech tactics  •  Safety", font=font(FONT_SEMI, 22), fill=CYAN)
    draw.text(
        (48, 250),
        "Know the wind.\nMaster the pech.\nFly safer every day.",
        font=font(FONT_BOLD, 28),
        fill=WHITE,
        spacing=8,
    )

    screen = crop_app_screen(HOME, has_ad=True)
    phone = make_phone_shot(screen, 230)
    # scale to fit
    target_h = 460
    s = target_h / phone.height
    phone = phone.resize((int(phone.width * s), target_h), Image.Resampling.LANCZOS)
    px, py = W - phone.width - 36, (H - phone.height) // 2
    paste_rounded(bg, phone.convert("RGBA"), (px, py), 28, outline=(*CYAN, 200), outline_width=3)

    out = OUT_BANNER / "play-store-feature-1024x500.png"
    bg.convert("RGB").save(out, "PNG", optimize=True)
    bg.convert("RGB").save(OUT_BANNER / "play-store-feature-1024x500.jpg", "JPEG", quality=92)
    print("wrote", out)

    # 16:9 promo banner
    W2, H2 = 1920, 1080
    wide = vertical_gradient((W2, H2), (8, 5, 16), (18, 8, 38))
    wide = radial_glow(wide, (1400, 540), 700, (160, 40, 255), 0.45)
    wide = radial_glow(wide, (1400, 540), 420, CYAN, 0.28)
    d2 = ImageDraw.Draw(wide)
    icon2 = Image.open(SRC_GEN / "kite-master-icon-clean.png").convert("RGBA").resize((140, 140), Image.Resampling.LANCZOS)
    wide.alpha_composite(icon2, (90, 200))
    d2.text((260, 220), "KITE MASTER", font=font(FONT_BOLD, 92), fill=WHITE)
    d2.text((260, 340), "Live wind  •  Pech tactics  •  Safety", font=font(FONT_SEMI, 36), fill=CYAN)
    d2.text((90, 500), "The utility hub for kite flyers.", font=font(FONT_BOLD, 44), fill=WHITE)
    d2.text(
        (90, 570),
        "Real-time flying conditions, masterclass\nguides, knots, and community safety.",
        font=font(FONT_REG, 32),
        fill=MUTED,
        spacing=10,
    )
    phone2 = make_phone_shot(screen, 420)
    th = 920
    s = th / phone2.height
    phone2 = phone2.resize((int(phone2.width * s), th), Image.Resampling.LANCZOS)
    px2, py2 = W2 - phone2.width - 80, (H2 - phone2.height) // 2
    paste_rounded(wide, phone2.convert("RGBA"), (px2, py2), 42, outline=(*CYAN, 210), outline_width=4)
    wide.convert("RGB").save(OUT_BANNER / "promo-banner-1920x1080.png", "PNG", optimize=True)
    print("wrote promo banner")

    shutil.copy2(SRC_GEN / "play-store-feature-accurate.png", OUT_BANNER / "feature-graphic-cinematic.png")
    shutil.copy2(SRC_GEN / "youtube-thumbnail.png", OUT_BANNER / "youtube-thumbnail.png")
    shutil.copy2(SRC_GEN / "kite-master-feature-banner.png", OUT_BANNER / "hero-banner-cinematic.png")
    shutil.copy2(SRC_GEN / "promo-cinematic-kite.png", OUT_BANNER / "lifestyle-kite-dusk.png")


def make_store_screenshots():
    specs = [
        (HOME, True, "Know the wind.\nThen fly.", "Live flying conditions in one tap", CYAN, "01-home-wind.png"),
        (DASH, True, "Perfect days,\nperfect wind.", "Live forecast + wind alerts", (190, 80, 255), "02-conditions-alerts.png"),
        (MASTER, False, "Master the Pech.", "Launch, fight, and fly like a pro", (190, 90, 255), "03-masterclass-pech.png"),
        (SAFETY, False, "Fly smart.\nStay safe.", "Hazard warnings & emergency knots", (255, 140, 50), "04-safety-knots.png"),
        (ACHIEVE, False, "Keep the streak\nalive.", "Badges for every flight", (255, 210, 70), "05-achievements.png"),
    ]
    for path, has_ad, headline, sub, accent, name in specs:
        screen = crop_app_screen(path, has_ad)
        store_screenshot(screen, headline.replace("\n", " "), sub, accent, OUT_SS / name)

    # extra designed promo shots (not the real UI — lifestyle)
    for src, dest in [
        ("store-ss-01-wind.png", "promo-shot-wind.png"),
        ("store-ss-02-pech.png", "promo-shot-pech.png"),
        ("store-ss-03-safety.png", "promo-shot-safety.png"),
        ("store-ss-04-streaks.png", "promo-shot-streaks.png"),
        ("store-ss-05-toolbox.png", "promo-shot-toolbox.png"),
    ]:
        shutil.copy2(SRC_GEN / src, OUT_SS / dest)


def letterbox(im: Image.Image, size, fill=(8, 5, 16)) -> Image.Image:
    tw, th = size
    canvas = Image.new("RGB", size, fill)
    im = im.convert("RGB")
    s = min(tw / im.width, th / im.height)
    nw, nh = int(im.width * s), int(im.height * s)
    im = im.resize((nw, nh), Image.Resampling.LANCZOS)
    canvas.paste(im, ((tw - nw) // 2, (th - nh) // 2))
    return canvas


def cover(im: Image.Image, size) -> Image.Image:
    tw, th = size
    im = im.convert("RGB")
    s = max(tw / im.width, th / im.height)
    nw, nh = int(im.width * s), int(im.height * s)
    im = im.resize((nw, nh), Image.Resampling.LANCZOS)
    x = (nw - tw) // 2
    y = (nh - th) // 2
    return im.crop((x, y, x + tw, y + th))


def overlay_title(im: Image.Image, title: str, sub: str | None = None) -> Image.Image:
    im = im.convert("RGBA")
    shade = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(shade)
    w, h = im.size
    d.rectangle((0, int(h * 0.62), w, h), fill=(0, 0, 0, 150))
    shade = shade.filter(ImageFilter.GaussianBlur(8))
    im.alpha_composite(shade)
    draw = ImageDraw.Draw(im)
    title_size = 72 if h > w else 64
    text_center(draw, (w / 2, int(h * 0.72)), title, font(FONT_BOLD, title_size), WHITE, stroke=True)
    if sub:
        text_center(draw, (w / 2, int(h * 0.80)), sub, font(FONT_SEMI, 34), CYAN, stroke=True)
    return im.convert("RGB")


def run(cmd):
    subprocess.run(cmd, check=True)


def make_zoom_clip(img: Path, out: Path, seconds: float, size):
    w, h = size
    frames = int(seconds * 30)
    # scale up then zoompan
    vf = (
        f"scale={w}:{h}:force_original_aspect_ratio=increase,"
        f"crop={w}:{h},"
        f"zoompan=z='min(zoom+0.00115,1.10)':d={frames}:"
        f"x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s={w}x{h}:fps=30,"
        "format=yuv420p"
    )
    run(
        [
            "ffmpeg",
            "-y",
            "-loop",
            "1",
            "-i",
            str(img),
            "-vf",
            vf,
            "-t",
            f"{seconds:.2f}",
            "-r",
            "30",
            "-c:v",
            "libx264",
            "-pix_fmt",
            "yuv420p",
            "-an",
            str(out),
        ]
    )


def concat_xfade(clips: list[Path], out: Path, clip_len=3.0, fade=0.6):
    if len(clips) == 1:
        shutil.copy2(clips[0], out)
        return
    inputs = []
    for c in clips:
        inputs += ["-i", str(c)]
    n = len(clips)
    filters = []
    last = "0:v"
    acc = clip_len
    for i in range(1, n):
        offset = acc - fade
        out_v = f"v{i}"
        filters.append(f"[{last}][{i}:v]xfade=transition=fade:duration={fade}:offset={offset:.3f}[{out_v}]")
        last = out_v
        acc = acc + clip_len - fade
    fc = ";".join(filters)
    run(
        [
            "ffmpeg",
            "-y",
            *inputs,
            "-filter_complex",
            fc,
            "-map",
            f"[{last}]",
            "-c:v",
            "libx264",
            "-pix_fmt",
            "yuv420p",
            "-movflags",
            "+faststart",
            "-crf",
            "20",
            str(out),
        ]
    )


def add_wind_audio(video: Path, out: Path, duration: float):
    # Brown-noise wind bed + a low swell. Original, no copyrighted music.
    afilter = (
        "anoisesrc=color=brown:amplitude=0.18:d={d}[n];"
        "sine=frequency=196:d={d}[s1];"
        "sine=frequency=98:d={d}[s2];"
        "[s1]volume=0.03,lowpass=f=400[s1b];"
        "[s2]volume=0.05,lowpass=f=250[s2b];"
        "[n]highpass=f=180,lowpass=f=1800,volume=0.55[wind];"
        "[wind][s1b][s2b]amix=inputs=3:normalize=0,afade=t=in:st=0:d=0.8,afade=t=out:st={out}:d=1.2[a]"
    ).format(d=duration + 0.4, out=max(duration - 1.2, 0.2))
    run(
        [
            "ffmpeg",
            "-y",
            "-i",
            str(video),
            "-filter_complex",
            afilter,
            "-map",
            "0:v",
            "-map",
            "[a]",
            "-c:v",
            "copy",
            "-c:a",
            "aac",
            "-b:a",
            "160k",
            "-shortest",
            "-movflags",
            "+faststart",
            str(out),
        ]
    )


def make_videos():
    TMP.mkdir(parents=True, exist_ok=True)

    # --- 9:16 ---
    vsize = (1080, 1920)
    frames_v = [
        ("video-frame-01-soar.png", "KITE MASTER", "The sky is calling"),
        ("video-frame-02-spool.png", "Feel the wind", "Live conditions, live alerts"),
        ("video-frame-03-pech.png", "Master the Pech", "Tactics for every duel"),
        (None, "Know before you fly", "Real-time flying conditions"),
        (None, "Safety first", "Hazards, knots, and smart flying"),
        ("video-frame-06-endcard.png", None, None),
    ]
    # bake app screens as frames 4-5
    home_frame = cover(crop_app_screen(HOME, True), vsize)
    safety_frame = cover(crop_app_screen(SAFETY, False), vsize)

    v_stills = []
    for i, (src, title, sub) in enumerate(frames_v):
        if src:
            im = cover(Image.open(SRC_GEN / src), vsize)
        elif i == 3:
            im = home_frame
        else:
            im = safety_frame
        if title:
            im = overlay_title(im, title, sub)
        p = TMP / f"v9_{i:02d}.png"
        im.save(p, "PNG")
        v_stills.append(p)

    clips = []
    for i, p in enumerate(v_stills):
        c = TMP / f"v9_{i:02d}.mp4"
        make_zoom_clip(p, c, 3.0, vsize)
        clips.append(c)

    silent = TMP / "promo-9x16-silent.mp4"
    concat_xfade(clips, silent, clip_len=3.0, fade=0.5)
    # last clip is longer; probe duration
    dur = probe_duration(silent)
    add_wind_audio(silent, OUT_VID / "kite-master-promo-9x16.mp4", dur)
    print("wrote 9:16 video", dur)

    # --- 16:9 ---
    hsize = (1920, 1080)
    wide_stills = []
    items = [
        (SRC_GEN / "promo-cinematic-kite.png", "KITE MASTER", "Fly smarter. Fight better."),
        (SRC_GEN / "video-frame-04-festival.png", "A sky full of kites", "Basant energy. Pro tools."),
        (SRC_GEN / "video-frame-05-rooftop.png", "Feel every gust", "Live wind. Live alerts."),
        (OUT_BANNER / "promo-banner-1920x1080.png", None, None),
        (SRC_GEN / "play-store-feature-accurate.png", None, None),
    ]
    for i, (src, title, sub) in enumerate(items):
        im = cover(Image.open(src), hsize)
        if title:
            im = overlay_title(im, title, sub)
        p = TMP / f"v16_{i:02d}.png"
        im.save(p, "PNG")
        wide_stills.append(p)

    clips16 = []
    for i, p in enumerate(wide_stills):
        c = TMP / f"v16_{i:02d}.mp4"
        make_zoom_clip(p, c, 3.0, hsize)
        clips16.append(c)
    silent16 = TMP / "promo-16x9-silent.mp4"
    concat_xfade(clips16, silent16, clip_len=3.0, fade=0.55)
    dur16 = probe_duration(silent16)
    add_wind_audio(silent16, OUT_VID / "kite-master-promo-16x9.mp4", dur16)
    print("wrote 16:9 video", dur16)

    # short screenshot slideshow 9:16
    ss_clips = []
    for i, name in enumerate(sorted(OUT_SS.glob("0*.png"))):
        im = cover(Image.open(name), vsize)
        p = TMP / f"ss_{i:02d}.png"
        im.save(p)
        c = TMP / f"ss_{i:02d}.mp4"
        make_zoom_clip(p, c, 2.4, vsize)
        ss_clips.append(c)
    silent_ss = TMP / "screens-silent.mp4"
    concat_xfade(ss_clips, silent_ss, clip_len=2.4, fade=0.4)
    dur_ss = probe_duration(silent_ss)
    add_wind_audio(silent_ss, OUT_VID / "kite-master-screens-tour-9x16.mp4", dur_ss)
    print("wrote screens tour", dur_ss)


def probe_duration(path: Path) -> float:
    out = subprocess.check_output(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=nw=1:nk=1",
            str(path),
        ],
        text=True,
    ).strip()
    return float(out)


def main():
    for p in (OUT_ICON, OUT_BANNER, OUT_SS, OUT_VID, TMP):
        p.mkdir(parents=True, exist_ok=True)
    make_icons()
    make_store_screenshots()
    make_feature_graphic()
    make_videos()
    print("done")


if __name__ == "__main__":
    main()
