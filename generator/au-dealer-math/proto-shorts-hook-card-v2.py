"""AUDM Shorts hook-card prototype — 4 layout variants for V2 Shorts opener.

Why: V1 Shorts had top-positioned text that clipped on the YouTube Shorts grid
(safe zone y=340-1600). V2 Shorts already centre the text but use cream-on-charcoal
with no stroke, which reads too quiet to stop scroll. Adrian wants brighter +
centred + outlined — Luca / MrBeast pattern, swapped to AUDM brand colours.

This script generates 4 candidate layouts as 1080x1920 PNGs (Shorts safe zone),
each rendered against two real V2 hooks ($4,800 and 3 ROOMS) so we can compare
how layouts scale across number-only and word-only hooks.

Variants:
  A — Orange-on-charcoal punch + thick cream stroke (Luca-style, brightest)
  B — Highlighter strip: orange rect behind charcoal text on cream (brand-DNA: highlight one thing)
  C — Number + label stack on charcoal (orange number top, cream label bottom)
  D — Orange-on-cream punch + thick charcoal stroke (premium / contract-paper feel)

Outputs:
  content/au-dealer-math/scripts/v02-renders/hook-card-proto/
    full/                  — 8 PNGs (4 variants × 2 hooks)
    contact-sheet.png      — single image showing all 8 side-by-side
    animated-variant-a.mp4 — 2s prototype of variant A (most likely winner)

Run: python generator/au-dealer-math/proto-shorts-hook-card-v2.py
"""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import subprocess
import sys

REPO = Path(r"C:\dev\Claude")
OUT_DIR = REPO / "content" / "au-dealer-math" / "scripts" / "v02-renders" / "hook-card-proto"
FULL = OUT_DIR / "full"
FULL.mkdir(parents=True, exist_ok=True)

# Brand palette LOCKED
CHARCOAL = (43, 43, 43)
ORANGE   = (209, 122, 61)
CREAM    = (245, 239, 230)

# Fonts
DMSANS_BOLD = REPO / "fonts" / "DM_Sans" / "DMSans-Bold.ttf"
ARIAL_BLACK = Path("C:/Windows/Fonts/ariblk.ttf")
DISPLAY_FONT = ARIAL_BLACK if ARIAL_BLACK.exists() else DMSANS_BOLD

# Shorts canvas
W, H = 1080, 1920

# Real V2 Short hooks + a dealer-vocab sublabel for hybrid variants
# (Adrian 2026-05-06: "the word DEALER MARGIN lands hard")
HOOKS = ["$4,800", "3 ROOMS"]
HOOK_LABELS = {
    "$4,800":  "DEALER MARGIN",
    "3 ROOMS": "F&I PIPELINE",
    "$3,000":  "RATE LOAD",
    "+4 POINTS": "RATE LOAD",
}

# ffmpeg
FFMPEG = (
    r"C:\Users\adria\AppData\Local\Microsoft\WinGet\Packages"
    r"\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe"
    r"\ffmpeg-8.1-full_build\bin\ffmpeg.exe"
)


# ============================================================
# Helpers
# ============================================================
def fit_font(text, font_path, max_w, max_h=None, start=440, min_size=80, step=8):
    """Largest size where text fits within max_w (and optionally max_h)."""
    size = start
    while size > min_size:
        f = ImageFont.truetype(str(font_path), size)
        bbox = f.getbbox(text)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        if tw <= max_w and (max_h is None or th <= max_h):
            return f, bbox
        size -= step
    return ImageFont.truetype(str(font_path), min_size), ImageFont.truetype(str(font_path), min_size).getbbox(text)


def hook_slug(hook):
    return hook.replace("$", "").replace(",", "").replace(" ", "-").lower()


# ============================================================
# Helper: divider bar + sublabel below the main hook
# ============================================================
def _draw_sublabel(draw, label, hook_bottom_y, label_color, divider_color):
    """Centered orange/charcoal divider bar + dealer-vocab label below the hook."""
    sub_f = ImageFont.truetype(str(DMSANS_BOLD), 110)
    bb = sub_f.getbbox(label.upper())
    sub_tw = bb[2] - bb[0]
    sub_x = (W - sub_tw) // 2 - bb[0]

    bar_w, bar_h = 80, 8
    bar_x = (W - bar_w) // 2
    bar_y = hook_bottom_y + 50
    draw.rectangle([bar_x, bar_y, bar_x + bar_w, bar_y + bar_h], fill=divider_color)

    sub_y = bar_y + bar_h + 30 - bb[1]
    draw.text((sub_x, sub_y), label.upper(), font=sub_f, fill=label_color)


# ============================================================
# Variant A — Orange-on-charcoal punch + thick cream stroke + sublabel
# ============================================================
def variant_a(hook, label=None):
    img = Image.new("RGB", (W, H), CHARCOAL)
    draw = ImageDraw.Draw(img)

    f, bbox = fit_font(hook, DISPLAY_FONT, max_w=int(W * 0.82), start=440)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]

    # Lift hook upward when sublabel is present so composite stays centred
    cy = H // 2 - (110 if label else 0)
    x = (W - tw) // 2 - bbox[0]
    y = cy - th // 2 - bbox[1]

    shadow = (15, 15, 15)
    draw.text((x + 8, y + 10), hook, font=f, fill=shadow,
              stroke_width=14, stroke_fill=shadow)
    draw.text((x, y), hook, font=f, fill=ORANGE,
              stroke_width=14, stroke_fill=CREAM)

    if label:
        hook_bottom = y + bbox[1] + th
        _draw_sublabel(draw, label, hook_bottom, label_color=CREAM, divider_color=ORANGE)

    return img


# ============================================================
# Variant B — Highlighter strip + sublabel
# ============================================================
def variant_b(hook, label=None):
    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)

    f, bbox = fit_font(hook, DISPLAY_FONT, max_w=int(W * 0.78), start=440)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]

    cy = H // 2 - (110 if label else 0)
    x = (W - tw) // 2 - bbox[0]
    y = cy - th // 2 - bbox[1]

    pad_x = 32
    pad_y = 18
    rect_x0 = x + bbox[0] - pad_x
    rect_x1 = x + bbox[0] + tw + pad_x
    rect_y0 = y + bbox[1] + int(th * 0.40)
    rect_y1 = y + bbox[1] + th + pad_y
    draw.rectangle([rect_x0, rect_y0, rect_x1, rect_y1], fill=ORANGE)

    draw.text((x, y), hook, font=f, fill=CHARCOAL)

    if label:
        hook_bottom = y + bbox[1] + th + pad_y
        _draw_sublabel(draw, label, hook_bottom, label_color=CHARCOAL, divider_color=ORANGE)

    return img


# ============================================================
# Variant C — Number + Label stack (charcoal BG)
# ============================================================
def variant_c(hook):
    """Splits hook into BIG part + LABEL.
    For numbers like '$4,800' → big '$4,800' top, generic label 'SURPRISE FEE' bottom.
    For words like '3 ROOMS' → big '3' top, 'ROOMS' bottom.
    """
    img = Image.new("RGB", (W, H), CHARCOAL)
    draw = ImageDraw.Draw(img)

    # Determine split
    if hook.startswith("$") or hook[0].isdigit() and " " not in hook:
        big = hook
        label = "DEALER MARGIN"
    elif " " in hook:
        parts = hook.split(" ", 1)
        big, label = parts[0], parts[1]
    else:
        big = hook
        label = "AUDM"

    # Big part — orange Arial Black, taller
    big_f, big_bb = fit_font(big, DISPLAY_FONT, max_w=int(W * 0.82), start=520)
    big_tw = big_bb[2] - big_bb[0]
    big_th = big_bb[3] - big_bb[1]

    # Label — cream DM Sans Bold, smaller
    label_f, label_bb = fit_font(label, DMSANS_BOLD, max_w=int(W * 0.75), start=140)
    label_tw = label_bb[2] - label_bb[0]
    label_th = label_bb[3] - label_bb[1]

    gap = 60
    total_h = big_th + gap + label_th
    top = (H - total_h) // 2

    big_x = (W - big_tw) // 2 - big_bb[0]
    big_y = top - big_bb[1]
    label_x = (W - label_tw) // 2 - label_bb[0]
    label_y = top + big_th + gap - label_bb[1]

    # Big number with thick cream stroke for punch
    draw.text((big_x, big_y), big, font=big_f, fill=ORANGE,
              stroke_width=10, stroke_fill=CREAM)
    # Label cream, slight letter-spacing feel via uppercase
    draw.text((label_x, label_y), label.upper(), font=label_f, fill=CREAM)

    # Tiny orange accent bar above label
    bar_w = 80
    bar_h = 8
    bar_x = (W - bar_w) // 2
    bar_y = label_y + label_bb[1] - 30
    draw.rectangle([bar_x, bar_y, bar_x + bar_w, bar_y + bar_h], fill=ORANGE)

    return img


# ============================================================
# Variant D — Orange-on-cream punch + thick charcoal stroke + sublabel
# ============================================================
def variant_d(hook, label=None):
    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)

    f, bbox = fit_font(hook, DISPLAY_FONT, max_w=int(W * 0.82), start=440)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]

    cy = H // 2 - (110 if label else 0)
    x = (W - tw) // 2 - bbox[0]
    y = cy - th // 2 - bbox[1]

    shadow = (180, 175, 165)
    draw.text((x + 6, y + 8), hook, font=f, fill=shadow,
              stroke_width=12, stroke_fill=shadow)
    draw.text((x, y), hook, font=f, fill=ORANGE,
              stroke_width=12, stroke_fill=CHARCOAL)

    if label:
        hook_bottom = y + bbox[1] + th
        _draw_sublabel(draw, label, hook_bottom, label_color=CHARCOAL, divider_color=ORANGE)

    return img


VARIANTS = {
    "a": ("Orange punch on charcoal", variant_a),
    "b": ("Highlighter strip on cream", variant_b),
    "c": ("Number + label stack", variant_c),
    "d": ("Orange punch on cream", variant_d),
}


# ============================================================
# Render all variants × all hooks
# ============================================================
def render_all():
    print(f"Rendering {len(VARIANTS)} variants x {len(HOOKS)} hooks -> {FULL}\n")
    rendered = []
    for hook in HOOKS:
        sublabel = HOOK_LABELS.get(hook)
        for vid, (vlabel, fn) in VARIANTS.items():
            # Variant C handles its own label split internally; A/B/D take the sublabel
            if vid == "c":
                img = fn(hook)
            else:
                img = fn(hook, label=sublabel)
            out = FULL / f"variant-{vid}-{hook_slug(hook)}.png"
            img.save(out, optimize=True)
            print(f"  [ok] variant-{vid} ({vlabel}) - {hook}  ->  {out.name}")
            rendered.append((vid, hook, out, img))
    return rendered


# ============================================================
# Contact sheet — 2 cols × 4 rows (variant per row, hook per col)
# ============================================================
def build_contact_sheet(rendered):
    print("\nBuilding contact sheet…")
    # Each thumb: scale 1080x1920 → 480x854
    THUMB_W, THUMB_H = 480, 854
    PAD = 30
    LABEL_H = 80

    cols = len(HOOKS)        # 2
    rows = len(VARIANTS)     # 4
    sheet_w = PAD + cols * (THUMB_W + PAD)
    sheet_h = PAD * 2 + LABEL_H + rows * (THUMB_H + PAD + LABEL_H // 2)

    sheet = Image.new("RGB", (sheet_w, sheet_h), (240, 240, 240))
    draw = ImageDraw.Draw(sheet)
    head_f = ImageFont.truetype(str(DMSANS_BOLD), 32)
    label_f = ImageFont.truetype(str(DMSANS_BOLD), 24)

    # Header
    draw.text((PAD, PAD // 2 + 10), "AUDM Shorts hook-card prototype — 4 layouts × 2 hooks",
              font=head_f, fill=(40, 40, 40))

    # Layout map: index by (variant_id, hook)
    by_key = {(vid, hook): img for vid, hook, _, img in rendered}

    y0 = PAD + LABEL_H
    for ri, (vid, (vlabel, _)) in enumerate(VARIANTS.items()):
        row_y = y0 + ri * (THUMB_H + PAD + LABEL_H // 2)
        # Variant label
        draw.text((PAD, row_y - 30), f"{vid.upper()}  {vlabel}",
                  font=label_f, fill=(60, 60, 60))
        for ci, hook in enumerate(HOOKS):
            img = by_key[(vid, hook)].resize((THUMB_W, THUMB_H), Image.LANCZOS)
            x = PAD + ci * (THUMB_W + PAD)
            sheet.paste(img, (x, row_y))
            draw.text((x, row_y + THUMB_H + 6), hook, font=label_f, fill=(60, 60, 60))

    out = OUT_DIR / "contact-sheet.png"
    sheet.save(out, optimize=True)
    print(f"  [ok] {out}")
    return out


# ============================================================
# Animated MP4 — variant A, 2s, fade-in + fade-out, no audio (silent preview)
# ============================================================
def build_animated_mp4(rendered):
    print("\nBuilding animated MP4 (variant A, $4,800, 2s)…")
    src_png = next(p for vid, hook, p, _ in rendered if vid == "a" and hook == "$4,800")
    out = OUT_DIR / "animated-variant-a.mp4"

    # 2s @ 30fps = 60 frames. Fade in 0-8 (0.27s), hold 8-52, fade out 52-60 (0.27s)
    cmd = [
        FFMPEG, "-y", "-loglevel", "error",
        "-loop", "1", "-i", str(src_png),
        "-t", "2",
        "-vf", "fade=in:0:8,fade=out:52:8,format=yuv420p",
        "-r", "30",
        "-c:v", "libx264", "-preset", "medium", "-crf", "18",
        str(out),
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(f"  [FAIL] {r.stderr.strip()[-1000:]}")
        sys.exit(1)
    print(f"  [ok] {out}")
    return out


# ============================================================
# Main
# ============================================================
if __name__ == "__main__":
    rendered = render_all()
    sheet = build_contact_sheet(rendered)
    mp4 = build_animated_mp4(rendered)
    print(f"\n{'='*60}")
    print(f"Done.")
    print(f"  Contact sheet  : {sheet}")
    print(f"  Animated MP4   : {mp4}")
    print(f"  Individual PNGs: {FULL}")
    print(f"{'='*60}")
