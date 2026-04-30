"""Generate AU Dealer Math YouTube channel banner v1 (placeholder, pre-mascot).

Spec from content/au-dealer-math/scripts/v01-channel-banner-v1.md.
2048x1152 PNG, charcoal bg + cream typography + outback orange accent.
All critical text inside the 1235x338 mobile-safe centre zone.

Run: python generator/au-dealer-math/generate-channel-banner.py
Output: brand/au-dealer-math/channel-banner-v1.png
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter
from pathlib import Path

REPO = Path(r"C:\dev\Claude")
OUT_DIR = REPO / "brand" / "au-dealer-math"
OUT_DIR.mkdir(parents=True, exist_ok=True)
OUT_FILE = OUT_DIR / "channel-banner-v1.png"

# Brand palette (LOCKED)
CHARCOAL = (43, 43, 43, 255)         # #2B2B2B
OUTBACK_ORANGE = (209, 122, 61, 255)  # #D17A3D
CREAM = (245, 239, 230, 255)         # #F5EFE6

# Banner dimensions: YouTube RECOMMENDED 2560x1440 (2048x1152 is minimum).
# 2026 research confirms 2560x1440 displays cleanly on TV (1546x423 TV-safe).
W, H = 2560, 1440
# Mobile-safe centre zone (text + logo MUST live here — outside cropped on mobile)
SAFE_W, SAFE_H = 1235, 338
SAFE_X = (W - SAFE_W) // 2
SAFE_Y = (H - SAFE_H) // 2

# Fonts (using DMSans-Bold + Inter-Regular from repo)
FONTS_DIR = REPO / "fonts"
DMSANS_BOLD = FONTS_DIR / "DM_Sans" / "DMSans-Bold.ttf"
DMSANS_REGULAR = FONTS_DIR / "DM_Sans" / "DMSans-Regular.ttf"
INTER_REGULAR = FONTS_DIR / "Inter" / "Inter-Regular.ttf"
ARIAL_BLACK = Path("C:/Windows/Fonts/ariblk.ttf")  # heavy fallback

assert DMSANS_BOLD.exists(), DMSANS_BOLD
assert DMSANS_REGULAR.exists(), DMSANS_REGULAR
assert INTER_REGULAR.exists(), INTER_REGULAR


def font(path, size):
    return ImageFont.truetype(str(path), size)


def measure(draw, text, f):
    bb = draw.textbbox((0, 0), text, font=f)
    return bb[2] - bb[0], bb[3] - bb[1]


# ============================================================
# Step 1: Solid charcoal background
# ============================================================
img = Image.new("RGBA", (W, H), CHARCOAL)

# ============================================================
# Step 2: Subtle radial gradient toward outback orange in bottom-right
# (~5% opacity, almost imperceptible — adds depth)
# ============================================================
gradient_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
gd = ImageDraw.Draw(gradient_layer)
# Draw a circle in bottom-right with orange fill, then blur heavily
glow_x = int(W * 0.85)
glow_y = int(H * 0.85)
glow_r = int(W * 0.5)
gd.ellipse([glow_x - glow_r, glow_y - glow_r, glow_x + glow_r, glow_y + glow_r],
           fill=(*OUTBACK_ORANGE[:3], 32))  # ~12% opacity, will blur down
gradient_layer = gradient_layer.filter(ImageFilter.GaussianBlur(radius=300))
img = Image.alpha_composite(img, gradient_layer)

draw = ImageDraw.Draw(img)

# ============================================================
# Step 3: Wordmark "AU DEALER MATH"
# Heavy display font, cream, centre-left within safe zone, vertically centred
# ============================================================
# Use Arial Black if available (heaviest), else DMSans-Bold
wordmark_font_path = ARIAL_BLACK if ARIAL_BLACK.exists() else DMSANS_BOLD
# Auto-fit: start at desired size, shrink until fits within safe zone with 60px buffer
wordmark = "AU DEALER MATH"
wordmark_size = 160
target_max_w = SAFE_W - 60
while wordmark_size > 80:
    wmf_test = font(wordmark_font_path, wordmark_size)
    test_w, _ = measure(draw, wordmark, wmf_test)
    if test_w <= target_max_w:
        break
    wordmark_size -= 4

wmf = font(wordmark_font_path, wordmark_size)
wm_w, wm_h = measure(draw, wordmark, wmf)
print(f"Wordmark fit: {wordmark_size}pt -> width {wm_w}px (target <={target_max_w}px)")

# Get accurate ascent/descent for underline placement
ascent, descent = wmf.getmetrics()
# Total visible text height = ascent + descent
# When drawn at y, baseline is at y + ascent, descender bottom at y + ascent + descent

# Position: left-aligned within safe zone
wm_x = SAFE_X
# Vertically: position so wordmark + tagline + cadence all fit within safe zone
# Reserve ~120px for tagline+gap, ~50px for cadence, leave ~25px gap before tagline
wm_y = SAFE_Y + 25

draw.text((wm_x, wm_y), wordmark, font=wmf, fill=CREAM)

# ============================================================
# Step 4: Underline under "AU DEALER" only (partial underline)
# 8pt orange stroke, drawn just below descender bottom
# ============================================================
underline_text = "AU DEALER"
ul_w, _ = measure(draw, underline_text, wmf)
# Bottom of text rendered at wm_y is wm_y + ascent + descent
ul_y = wm_y + ascent + descent - 4  # 4px above absolute bottom for tighter look
ul_thickness = 12
draw.rectangle([wm_x, ul_y, wm_x + ul_w, ul_y + ul_thickness],
               fill=OUTBACK_ORANGE)

# ============================================================
# Step 5: Tagline "What dealers don't tell you about the math."
# DM Sans Regular 60pt, cream 70% opacity
# ============================================================
tagline = "What dealers don't tell you about the math."
tag_size = 56
tagf = font(DMSANS_REGULAR, tag_size)
tag_w, tag_h = measure(draw, tagline, tagf)
tag_x = SAFE_X
tag_y = ul_y + ul_thickness + 28

# 70% opacity cream
cream_70 = (CREAM[0], CREAM[1], CREAM[2], int(255 * 0.7))
draw.text((tag_x, tag_y), tagline, font=tagf, fill=cream_70)

# ============================================================
# Step 6: Cadence line "New explainers Mon · Wed · Fri  6pm AWST"
# Inter Regular 36pt, cream 50% opacity, bottom of safe zone
# ============================================================
cadence = "New explainers Mon · Wed · Fri    6pm AWST"
cad_size = 34
cadf = font(INTER_REGULAR, cad_size)
cad_w, cad_h = measure(draw, cadence, cadf)
cad_x = SAFE_X
cad_y = SAFE_Y + SAFE_H - cad_h - 8  # bottom of safe zone, 8px margin

cream_50 = (CREAM[0], CREAM[1], CREAM[2], int(255 * 0.5))
draw.text((cad_x, cad_y), cadence, font=cadf, fill=cream_50)

# ============================================================
# Optional: subtle outline around safe zone for QC (commented out for production)
# ============================================================
# draw.rectangle([SAFE_X, SAFE_Y, SAFE_X + SAFE_W, SAFE_Y + SAFE_H],
#                outline=(255, 0, 0, 100), width=2)

# Save
img.convert("RGB").save(OUT_FILE, "PNG", optimize=True)
print(f"Banner saved: {OUT_FILE}")
print(f"Size: {OUT_FILE.stat().st_size // 1024}KB")
print(f"Dimensions: {W}x{H} (safe zone: {SAFE_W}x{SAFE_H} centre)")
