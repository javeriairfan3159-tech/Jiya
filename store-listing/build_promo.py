#!/usr/bin/env python3
"""Export store banners and compose a short promo video."""

from __future__ import annotations

import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

from build_screenshots import (
    FONT_BOLD,
    FONT_MED,
    FONT_SEMI,
    SRC,
    drop_shadow,
    font,
    phone_frame,
    vertical_gradient,
    wrap_text,
)

ROOT = Path(__file__).resolve().parent
BANNER_DIR = ROOT / "banner"
VIDEO_DIR = ROOT / "video"
FRAMES_L = VIDEO_DIR / "frames-16x9"
FRAMES_V = VIDEO_DIR / "frames-9x16"
ICON = ROOT / "icon" / "ic_launcher_512.png"

LW, LH = 1920, 1080
VW, VH = 1080, 1920


def cover_resize(img: Image.Image, size: tuple[int, int]) -> Image.Image:
    tw, th = size
    scale = max(tw / img.width, th / img.height)
    nw, nh = int(img.width * scale), int(img.height * scale)
    resized = img.resize((nw, nh), Image.Resampling.LANCZOS)
    left = (nw - tw) // 2
    top = (nh - th) // 2
    return resized.crop((left, top, left + tw, top + th))


def export_banners() -> None:
    BANNER_DIR.mkdir(parents=True, exist_ok=True)
    wide = Image.open("/opt/cursor/artifacts/assets/v380-banner-16x9.png").convert("RGB")
    safe = Image.open("/opt/cursor/artifacts/assets/v380-banner-playstore-safe.png").convert("RGB")

    cover_resize(wide, (1920, 1080)).save(BANNER_DIR / "banner_youtube_1920x1080.png", "PNG")
    cover_resize(safe, (1024, 500)).save(BANNER_DIR / "banner_playstore_1024x500.png", "PNG")
    # Also refresh the official Play feature graphic used in the listing pack
    cover_resize(safe, (1024, 500)).save(
        ROOT / "feature-graphic" / "feature_graphic_1024x500.png", "PNG"
    )
    # Website / Facebook-style strip
    cover_resize(wide, (1920, 600)).save(BANNER_DIR / "banner_strip_1920x600.png", "PNG")
    print("exported banners")


def rounded_icon(size: int = 280) -> Image.Image:
    icon = Image.open(ICON).convert("RGBA").resize((size, size), Image.Resampling.LANCZOS)
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, size - 1, size - 1), radius=int(size * 0.22), fill=255)
    out = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    out.paste(icon, (0, 0), mask)
    return out


def landscape_intro() -> Image.Image:
    bg = cover_resize(Image.open(BANNER_DIR / "banner_youtube_1920x1080.png").convert("RGB"), (LW, LH))
    return bg


def landscape_outro() -> Image.Image:
    canvas = cover_resize(Image.open(BANNER_DIR / "banner_youtube_1920x1080.png").convert("RGB"), (LW, LH)).convert("RGBA")
    overlay = Image.new("RGBA", (LW, LH), (6, 16, 48, 90))
    canvas.alpha_composite(overlay)
    draw = ImageDraw.Draw(canvas)
    icon = drop_shadow(rounded_icon(200), offset=(0, 16), blur=24, opacity=110)
    canvas.alpha_composite(icon, (120, (LH - icon.height) // 2))
    x = 400
    draw.text((x, 390), "V380 Pro Guide", font=font(FONT_BOLD, 72), fill=(255, 255, 255, 255))
    draw.text(
        (x, 490),
        "Setup  •  Pair  •  Troubleshoot  •  Recover",
        font=font(FONT_MED, 32),
        fill=(210, 226, 255, 255),
    )
    draw.text((x, 560), "Unofficial companion for V380 Pro cameras", font=font(FONT_MED, 26), fill=(180, 200, 230, 230))
    return canvas.convert("RGB")


def landscape_feature(shot_name: str, eyebrow: str, title: str, subtitle: str, top, bottom) -> Image.Image:
    canvas = vertical_gradient((LW, LH), top, bottom).convert("RGBA")
    orb = Image.new("RGBA", (820, 820), (0, 0, 0, 0))
    ImageDraw.Draw(orb).ellipse((0, 0, 819, 819), fill=(255, 255, 255, 22))
    canvas.alpha_composite(orb.filter(ImageFilter.GaussianBlur(36)), (1180, -180))

    draw = ImageDraw.Draw(canvas)
    left = 90
    y = 250
    ef = font(FONT_SEMI, 24)
    chip = eyebrow.upper()
    tw = draw.textlength(chip, font=ef)
    draw.rounded_rectangle((left, y, left + tw + 36, y + 46), radius=23, fill=(255, 255, 255, 230))
    draw.text((left + 18, y + 10), chip, font=ef, fill=(12, 32, 92, 255))
    y += 80

    tf = font(FONT_BOLD, 62)
    for line in wrap_text(draw, title, tf, 780):
        draw.text((left, y), line, font=tf, fill=(255, 255, 255, 255))
        y += 74
    y += 8
    sf = font(FONT_MED, 30)
    for line in wrap_text(draw, subtitle, sf, 760):
        draw.text((left, y), line, font=sf, fill=(220, 232, 255, 230))
        y += 40

    phone = phone_frame(Image.open(SRC / shot_name), 520)
    scale = 980 / phone.height
    phone = phone.resize((int(phone.width * scale), int(phone.height * scale)), Image.Resampling.LANCZOS)
    shadowed = drop_shadow(phone, offset=(0, 22), blur=28, opacity=120)
    canvas.alpha_composite(shadowed, (1120 - shadowed.width // 2, (LH - shadowed.height) // 2 + 10))
    return canvas.convert("RGB")


def vertical_card(eyebrow: str, title: str, subtitle: str, top, bottom, with_icon: bool = True) -> Image.Image:
    canvas = vertical_gradient((VW, VH), top, bottom).convert("RGBA")
    draw = ImageDraw.Draw(canvas)
    y = 420
    if with_icon:
        icon = drop_shadow(rounded_icon(260), offset=(0, 18), blur=28, opacity=120)
        canvas.alpha_composite(icon, ((VW - icon.width) // 2, 260))
        y = 620
    ef = font(FONT_SEMI, 26)
    chip = eyebrow.upper()
    tw = draw.textlength(chip, font=ef)
    cx = (VW - tw - 36) / 2
    draw.rounded_rectangle((cx, y, cx + tw + 36, y + 48), radius=24, fill=(255, 255, 255, 230))
    draw.text((cx + 18, y + 10), chip, font=ef, fill=(12, 32, 92, 255))
    y += 90
    tf = font(FONT_BOLD, 64)
    for line in wrap_text(draw, title, tf, 860):
        tw = draw.textlength(line, font=tf)
        draw.text(((VW - tw) / 2, y), line, font=tf, fill=(255, 255, 255, 255))
        y += 78
    y += 10
    sf = font(FONT_MED, 30)
    for line in wrap_text(draw, subtitle, sf, 820):
        tw = draw.textlength(line, font=sf)
        draw.text(((VW - tw) / 2, y), line, font=sf, fill=(220, 232, 255, 230))
        y += 42
    return canvas.convert("RGB")


FEATURES = [
    {
        "file": "home-modules.jpg",
        "shot": "01-home-command-center.png",
        "eyebrow": "All-in-one companion",
        "title": "Your V380 Pro command center",
        "subtitle": "Setup, PC integration, and error solving in one place.",
        "top": (13, 56, 168),
        "bottom": (8, 28, 92),
    },
    {
        "file": "pairing.jpg",
        "shot": "03-camera-pairing.png",
        "eyebrow": "Camera pairing",
        "title": "Pair in 3 simple ways",
        "subtitle": "AP Hotspot, Wi-Fi Smart-Link, and QR Code.",
        "top": (67, 56, 202),
        "bottom": (36, 32, 120),
    },
    {
        "file": "smart-tools.jpg",
        "shot": "02-smart-tools.png",
        "eyebrow": "Diagnostic suite",
        "title": "Tools that actually fix issues",
        "subtitle": "Error solver, IP scanner, Wi-Fi meter, and RTSP URLs.",
        "top": (12, 28, 68),
        "bottom": (180, 80, 24),
    },
    {
        "file": "storage.jpg",
        "shot": "05-storage-cloud.png",
        "eyebrow": "Storage & recording",
        "title": "SD, cloud, and 24/7 modes",
        "subtitle": "Format MicroSD, set loop or motion, enable cloud backup.",
        "top": (14, 116, 144),
        "bottom": (10, 58, 90),
    },
    {
        "file": "firmware.jpg",
        "shot": "06-firmware-recovery.png",
        "eyebrow": "Firmware & recovery",
        "title": "Update or unbrick safely",
        "subtitle": "Guided OTA updates and hard-reset recovery.",
        "top": (88, 36, 140),
        "bottom": (48, 18, 88),
    },
]


def write_frames() -> tuple[list[Path], list[Path]]:
    FRAMES_L.mkdir(parents=True, exist_ok=True)
    FRAMES_V.mkdir(parents=True, exist_ok=True)
    land: list[Path] = []
    vert: list[Path] = []

    p = FRAMES_L / "00-intro.png"
    landscape_intro().save(p, "PNG")
    land.append(p)

    vp = FRAMES_V / "00-intro.png"
    vertical_card(
        "V380 Pro Guide",
        "Setup, pair, and recover",
        "Unofficial companion for V380 Pro cameras",
        (13, 56, 168),
        (8, 24, 80),
        True,
    ).save(vp, "PNG")
    vert.append(vp)

    for i, spec in enumerate(FEATURES, start=1):
        lp = FRAMES_L / f"{i:02d}-scene.png"
        landscape_feature(spec["file"], spec["eyebrow"], spec["title"], spec["subtitle"], spec["top"], spec["bottom"]).save(lp, "PNG")
        land.append(lp)
        # Vertical promo uses the already-designed store screenshots
        src = Image.open(ROOT / "screenshots" / spec["shot"]).convert("RGB")
        cover_resize(src, (VW, VH)).save(FRAMES_V / f"{i:02d}-scene.png", "PNG")
        vert.append(FRAMES_V / f"{i:02d}-scene.png")

    p = FRAMES_L / "99-outro.png"
    landscape_outro().save(p, "PNG")
    land.append(p)
    vp = FRAMES_V / "99-outro.png"
    vertical_card(
        "Get started",
        "V380 Pro Guide",
        "Setup • Pair • Troubleshoot • Recover",
        (13, 56, 168),
        (8, 24, 80),
        True,
    ).save(vp, "PNG")
    vert.append(vp)
    return land, vert


def make_audio(path: Path, duration: float) -> None:
    # Original soft pad — no third-party music.
    expr = (
        "0.07*sin(2*PI*196*t)*(0.55+0.45*sin(2*PI*0.12*t))"
        "+0.05*sin(2*PI*246.94*t)*(0.5+0.5*sin(2*PI*0.09*t+1))"
        "+0.035*sin(2*PI*293.66*t)"
        "+0.025*sin(2*PI*392*t)*sin(2*PI*0.2*t)"
    )
    cmd = [
        "ffmpeg",
        "-y",
        "-f",
        "lavfi",
        "-i",
        f"aevalsrc={expr}:s=44100:d={duration:.2f}",
        "-af",
        "lowpass=f=1800,highpass=f=80,volume=1.35,afade=t=in:st=0:d=0.6,afade=t=out:st={:.2f}:d=1.2".format(
            max(duration - 1.2, 0.2)
        ),
        "-c:a",
        "aac",
        "-b:a",
        "160k",
        str(path),
    ]
    subprocess.check_call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def encode_xfade(frames: list[Path], audio: Path, out: Path, size: tuple[int, int], hold: float = 2.45, fade: float = 0.4) -> None:
    w, h = size
    n = len(frames)
    # Each still is held, then crossfaded into the next.
    inputs: list[str] = []
    for frame in frames:
        inputs += ["-loop", "1", "-t", f"{hold + fade:.2f}", "-i", str(frame)]
    inputs += ["-i", str(audio)]

    filters = [f"[{i}:v]scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h},format=yuv420p[v{i}]" for i in range(n)]
    last = "v0"
    offset = hold
    for i in range(1, n):
        nxt = f"x{i}"
        filters.append(
            f"[{last}][v{i}]xfade=transition=fade:duration={fade:.2f}:offset={offset:.2f}[{nxt}]"
        )
        last = nxt
        offset += hold
    filter_complex = ";".join(filters)

    total = hold * n + fade
    cmd = [
        "ffmpeg",
        "-y",
        *inputs,
        "-filter_complex",
        filter_complex,
        "-map",
        f"[{last}]",
        "-map",
        f"{n}:a",
        "-t",
        f"{total:.2f}",
        "-c:v",
        "libx264",
        "-preset",
        "fast",
        "-crf",
        "21",
        "-pix_fmt",
        "yuv420p",
        "-c:a",
        "aac",
        "-b:a",
        "160k",
        "-shortest",
        "-movflags",
        "+faststart",
        str(out),
    ]
    subprocess.check_call(cmd)
    print(f"wrote {out}")


def main() -> None:
    VIDEO_DIR.mkdir(parents=True, exist_ok=True)
    export_banners()
    land, vert = write_frames()
    print(f"frames landscape={len(land)} vertical={len(vert)}")

    hold, fade = 2.45, 0.40
    duration = hold * len(land) + fade + 0.3
    audio = VIDEO_DIR / "promo-audio.m4a"
    make_audio(audio, duration)

    encode_xfade(land, audio, VIDEO_DIR / "v380-pro-guide-promo-16x9.mp4", (LW, LH), hold, fade)
    encode_xfade(vert, audio, VIDEO_DIR / "v380-pro-guide-promo-9x16.mp4", (VW, VH), hold, fade)


if __name__ == "__main__":
    main()
