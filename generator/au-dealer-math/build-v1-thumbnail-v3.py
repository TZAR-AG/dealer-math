"""V1 thumbnail v3 — editorial discipline.

Critique of v2: too many competing elements (yellow + red + orange + cream + drop shadows everywhere). Read as "slapped together" not "designed."

v3 design rules:
- ONE accent color (orange), nothing else
- ONE photo element (tight contract crop, not full scene mush)
- ONE big typographic idea (the dollar number)
- ZERO drop shadows on text (drop shadows scream "engineer used PIL")
- DM Sans Bold, not Arial Black (more editorial, less "finance bro YT")
- Asymmetric composition with intentional negative space
- AUDM logo tiny bottom-right (brand mark, not headline)

Reference aesthetic: Bloomberg Businessweek / Wired cover style.

Output: content/au-dealer-math/scripts/v01-thumbnail-v3.png
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageOps
from pathlib import Path

REPO = Path(r"C:\dev\Claude")
OUT_DIR = REPO / "content" / "au-dealer-math" / "scripts"

CHARCOAL = (43, 43, 43)
OUTBACK_ORANGE = (209, 122, 61)
CREAM = (245, 239, 230)

BACKDROP = REPO / "content" / "au-dealer-math" / "scripts" / "v01-renders" / "stills" / "v2" / "kit-hero-cheatsheet-bg.png"
LOGO = REPO / "brand" / "au-dealer-math" / "channel-logo-v2.png"

FONTS_DIR = REPO / "fonts"
DMSANS_BOLD = FONTS_DIR / "DM_Sans" / "DMSans-Bold.ttf"
DMSANS_REGULAR = FONTS_DIR / "DM_Sans" / "DMSans-Regular.ttf"

W, H = 1280, 720


def font(path, size):
    return ImageFont.truetype(str(path), size)


def measure(draw, text, f):
    bb = draw.textbbox((0, 0), text, font=f)
    return bb[2] - bb[0], bb[3] - bb[1]


# ============================================================
# Backdrop: tight crop on the most dramatic part of kit-hero
# (the pen + contract + orange highlight stroke), heavily darkened
# ============================================================
src = Image.open(BACKDROP).convert("RGB")
sw, sh = src.size

# Tight crop on the right-bottom area where the pen + paper + orange highlight live
# kit-hero is roughly 1456x816 — pen is around (60-70%, 60-80%)
crop_left = int(sw * 0.10)
crop_right = int(sw * 0.95)
crop_top = int(sh * 0.30)
crop_bottom = int(sh * 0.95)
src = src.crop((crop_left, crop_top, crop_right, crop_bottom))

# Resize to thumbnail dims
src = ImageOps.fit(src, (W, H), Image.LANCZOS, centering=(0.5, 0.5))

# Darken aggressively — photo is texture, not subject
src = ImageEnhance.Brightness(src).enhance(0.32)

# Very slight blur for depth
src = src.filter(ImageFilter.GaussianBlur(radius=2))

img = src.convert("RGBA")

# Vignette — pull edges deeper into shadow
vignette = Image.new("RGBA", (W, H), (0, 0, 0, 0))
vd = ImageDraw.Draw(vignette)
for r in range(0, 250, 3):
    alpha = int(160 * (r / 250) ** 2)
    vd.rectangle([r, r, W - r, H - r], outline=(0, 0, 0, alpha), width=3)
vignette = vignette.filter(ImageFilter.GaussianBlur(radius=60))
img = Image.alpha_composite(img, vignette)

# Right-side gradient deepening (where the type lives)
right_overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
ro = ImageDraw.Draw(right_overlay)
for x in range(W):
    # Stronger darkening on right 60%
    alpha = int(120 * max(0, (x - W * 0.4) / (W * 0.6)) ** 1.2)
    ro.line([(x, 0), (x, H)], fill=(0, 0, 0, alpha))
img = Image.alpha_composite(img, right_overlay)

draw = ImageDraw.Draw(img)

# ============================================================
# Tiny editorial header (top-left): "AU DEALER MATH · EP. 01"
# Small caps, cream 60%, intentionally restrained
# ============================================================
header_font = font(DMSANS_BOLD, 28)
header_text = "AU DEALER MATH   ·   EPISODE 01"
hw, hh = measure(draw, header_text, header_font)
draw.text((60, 50), header_text, font=header_font,
          fill=(CREAM[0], CREAM[1], CREAM[2], 160))

# Small horizontal orange rule under the header (editorial cue)
draw.rectangle([60, 50 + hh + 16, 60 + 80, 50 + hh + 22], fill=OUTBACK_ORANGE)

# ============================================================
# Subhead (small italic-feel): "if a dealer asks…"
# ============================================================
sub_font = font(DMSANS_REGULAR, 36)
sub_text = "If a dealer asks what your weekly budget is —"
sw_, sh_ = measure(draw, sub_text, sub_font)
draw.text((60, 180), sub_text, font=sub_font,
          fill=(CREAM[0], CREAM[1], CREAM[2], 200))

# ============================================================
# THE big number — single hero element, restrained colour (cream, NOT yellow)
# Orange highlight stroke under it (brand motif from logo v2)
# ============================================================
num_font_size = 280
num_font = font(DMSANS_BOLD, num_font_size)
num_text = "$46,800"
nw, nh = measure(draw, num_text, num_font)

# Auto-fit to safe width
while nw > W - 120 and num_font_size > 100:
    num_font_size -= 8
    num_font = font(DMSANS_BOLD, num_font_size)
    nw, nh = measure(draw, num_text, num_font)

nx = 60
ny = 250
draw.text((nx, ny), num_text, font=num_font, fill=CREAM)

# Orange highlight stroke under the number — brand motif from logo v2
# Thick enough to read at 240×135, positioned just under the baseline
ascent, descent = num_font.getmetrics()
stroke_y = ny + ascent - 10
stroke_h = 26
draw.rectangle([nx, stroke_y, nx + nw + 6, stroke_y + stroke_h], fill=OUTBACK_ORANGE)

# ============================================================
# Caption under the number: tiny refined caption
# ============================================================
cap_font = font(DMSANS_REGULAR, 38)
cap_text = "more out of your pocket. The question that does it →"
cw, ch = measure(draw, cap_text, cap_font)
# Auto-fit
while cw > W - 120:
    cap_font = font(DMSANS_REGULAR, cap_font.size - 2)
    cw, ch = measure(draw, cap_text, cap_font)
draw.text((60, ny + nh + stroke_h + 30), cap_text, font=cap_font,
          fill=(CREAM[0], CREAM[1], CREAM[2], 220))

# ============================================================
# Bottom-right: AUDM logo small as brand mark
# ============================================================
if LOGO.exists():
    logo = Image.open(LOGO).convert("RGBA")
    logo_size = 110
    logo = logo.resize((logo_size, logo_size), Image.LANCZOS)
    img.paste(logo, (W - logo_size - 40, H - logo_size - 40), logo)

# ============================================================
# Save
# ============================================================
out = OUT_DIR / "v01-thumbnail-v3.png"
img.convert("RGB").save(out, "PNG", optimize=True)
print(f"[OK] v3 thumbnail: {out}")
print(f"     Size: {out.stat().st_size // 1024}KB")
print(f"     Design: editorial-cover discipline")
print(f"     Colors: charcoal + cream + orange (no yellow, no red)")
print(f"     Type: DM Sans Bold (no Arial Black, no drop shadows)")
