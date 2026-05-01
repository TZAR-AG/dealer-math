"""Generate AU Dealer Math YouTube channel banner v2 — showstopper.

v2 changes vs v1 (placeholder):
- Contract-photo backdrop (the brand cheatsheet hero image, dimmed) — no longer
  flat-charcoal void
- Bigger, bolder wordmark (~280pt) with cream/orange color-split for visual punch
- Locked tagline from channel-config.md: "Run the numbers. Walk in fluent."
- Orange highlight bar grounding the wordmark
- Subtle vignette to focus eye on text
- All critical text inside 1546x423 TV-safe zone (per 2026 YT research)

Run: python generator/au-dealer-math/generate-channel-banner-v2.py
Output: brand/au-dealer-math/channel-banner-v2.png
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
from pathlib import Path

REPO = Path(r"C:\dev\Claude")
OUT_DIR = REPO / "brand" / "au-dealer-math"
OUT_DIR.mkdir(parents=True, exist_ok=True)
OUT_FILE = OUT_DIR / "channel-banner-v2.png"

# Brand palette (LOCKED per design-system-audm.md)
CHARCOAL = (43, 43, 43)
CHARCOAL_RGBA = (43, 43, 43, 255)
OUTBACK_ORANGE = (209, 122, 61)
OUTBACK_ORANGE_RGBA = (209, 122, 61, 255)
CREAM = (245, 239, 230)
CREAM_RGBA = (245, 239, 230, 255)

# YouTube banner: 2560x1440 recommended (TV-safe 1546x423 centred)
W, H = 2560, 1440
SAFE_W, SAFE_H = 1546, 423
SAFE_X = (W - SAFE_W) // 2
SAFE_Y = (H - SAFE_H) // 2

# Backdrop image (the contract photo we use on the cheatsheet landing page)
BACKDROP = REPO / "content" / "au-dealer-math" / "scripts" / "v01-renders" / "stills" / "v2" / "kit-hero-cheatsheet-bg.png"

# Fonts
FONTS_DIR = REPO / "fonts"
DMSANS_BOLD = FONTS_DIR / "DM_Sans" / "DMSans-Bold.ttf"
DMSANS_REGULAR = FONTS_DIR / "DM_Sans" / "DMSans-Regular.ttf"
INTER_REGULAR = FONTS_DIR / "Inter" / "Inter-Regular.ttf"
ARIAL_BLACK = Path("C:/Windows/Fonts/ariblk.ttf")

assert DMSANS_BOLD.exists()
assert DMSANS_REGULAR.exists()

display_font_path = ARIAL_BLACK if ARIAL_BLACK.exists() else DMSANS_BOLD


def font(path, size):
    return ImageFont.truetype(str(path), size)


def measure(draw, text, f):
    bb = draw.textbbox((0, 0), text, font=f)
    return bb[2] - bb[0], bb[3] - bb[1]


# ============================================================
# Step 1: Backdrop layer — contract photo, heavily dimmed
# ============================================================
if BACKDROP.exists():
    backdrop = Image.open(BACKDROP).convert("RGB")
    # Cover-fit to 2560x1440 (crop to fill, preserve aspect)
    src_w, src_h = backdrop.size
    target_aspect = W / H
    src_aspect = src_w / src_h
    if src_aspect > target_aspect:
        # Source wider — crop horizontally
        new_w = int(src_h * target_aspect)
        offset = (src_w - new_w) // 2
        backdrop = backdrop.crop((offset, 0, offset + new_w, src_h))
    else:
        new_h = int(src_w / target_aspect)
        offset = (src_h - new_h) // 2
        backdrop = backdrop.crop((0, offset, src_w, offset + new_h))
    backdrop = backdrop.resize((W, H), Image.LANCZOS)
    # Darken — multiply by 0.30 (deep moody backdrop, photo barely visible)
    enhancer = ImageEnhance.Brightness(backdrop)
    backdrop = enhancer.enhance(0.30)
    # Slight blur for depth
    backdrop = backdrop.filter(ImageFilter.GaussianBlur(radius=4))
    img = backdrop.convert("RGBA")
else:
    img = Image.new("RGBA", (W, H), CHARCOAL_RGBA)

# Charcoal overlay on top — pull deeper into shadow on edges (vignette)
overlay = Image.new("RGBA", (W, H), (CHARCOAL[0], CHARCOAL[1], CHARCOAL[2], 80))
img = Image.alpha_composite(img, overlay)

# Vignette: dark gradient from edges
vignette = Image.new("RGBA", (W, H), (0, 0, 0, 0))
vd = ImageDraw.Draw(vignette)
for r in range(0, 600, 6):
    alpha = int(120 * (r / 600) ** 2)
    vd.rectangle([r, r, W - r, H - r], outline=(0, 0, 0, alpha), width=6)
vignette = vignette.filter(ImageFilter.GaussianBlur(radius=80))
img = Image.alpha_composite(img, vignette)

draw = ImageDraw.Draw(img)

# ============================================================
# Step 2: Wordmark "AU DEALER MATH"
# Cream "AU DEALER" + outback-orange "MATH" — color split for punch
# ============================================================
wm_size = 280
# Auto-fit if needed
target_max_w = SAFE_W - 80
while wm_size > 120:
    wmf_test = font(display_font_path, wm_size)
    test_w, _ = measure(draw, "AU DEALER MATH", wmf_test)
    if test_w <= target_max_w:
        break
    wm_size -= 6

wmf = font(display_font_path, wm_size)

# Measure each segment
seg1 = "AU DEALER "  # trailing space for kerning
seg2 = "MATH"
s1_w, s1_h = measure(draw, seg1, wmf)
s2_w, s2_h = measure(draw, seg2, wmf)
total_w = s1_w + s2_w
text_h = max(s1_h, s2_h)

# Centred horizontally in safe zone
wm_x = SAFE_X + (SAFE_W - total_w) // 2
# Vertically: place in upper half of safe zone, leaving ~140px below for tagline + line
wm_y = SAFE_Y + 30

# Get accurate metrics for underline placement
ascent, descent = wmf.getmetrics()

# Draw segments
draw.text((wm_x, wm_y), seg1, font=wmf, fill=CREAM_RGBA)
draw.text((wm_x + s1_w, wm_y), seg2, font=wmf, fill=OUTBACK_ORANGE_RGBA)

# ============================================================
# Step 3: Orange highlight stroke under "MATH" only
# Thick block (16-20% of letter height) — feels like the cheatsheet highlight
# ============================================================
highlight_y = wm_y + ascent + descent - 6
highlight_thickness = max(14, int(text_h * 0.06))
highlight_x_start = wm_x + s1_w
highlight_x_end = highlight_x_start + s2_w
draw.rectangle([highlight_x_start, highlight_y,
                highlight_x_end, highlight_y + highlight_thickness],
               fill=OUTBACK_ORANGE_RGBA)

# ============================================================
# Step 4: Tagline "Run the numbers. Walk in fluent."
# DM Sans Regular ~88pt, cream 90% opacity, centred, below wordmark
# ============================================================
tagline = "Run the numbers. Walk in fluent."
tag_size = 76
tagf = font(DMSANS_REGULAR, tag_size)
tag_w, tag_h = measure(draw, tagline, tagf)

# Centred horizontally
tag_x = SAFE_X + (SAFE_W - tag_w) // 2
tag_y = highlight_y + highlight_thickness + 36

cream_90 = (CREAM[0], CREAM[1], CREAM[2], int(255 * 0.90))
draw.text((tag_x, tag_y), tagline, font=tagf, fill=cream_90)

# ============================================================
# Cadence + URL line removed 2026-05-01 per Adrian — re-add when website
# is live + automated posting pipeline is running. Don't advertise a
# cadence we haven't proven or a URL that doesn't yet have a real homepage.
# ============================================================

# ============================================================
# Save
# ============================================================
img.convert("RGB").save(OUT_FILE, "PNG", optimize=True)
size_kb = OUT_FILE.stat().st_size // 1024
print(f"[OK] Banner v2: {OUT_FILE}  ({size_kb}KB · {W}x{H} · TV-safe {SAFE_W}x{SAFE_H} centred)")
print(f"     Wordmark fit: {wm_size}pt   ({total_w}px wide)")
print(f"     Backdrop: {BACKDROP.name if BACKDROP.exists() else '(none — flat charcoal)'}")
