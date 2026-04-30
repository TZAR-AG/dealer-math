"""Generate AU Dealer Math channel logo + watermark.

Research-backed (faceless education channel best practice 2026):
- Wordmark over mascot (mascots blur to mush at 16x16 sub feed avatar)
- Tight 4-letter monogram "AUDM" centred
- 15%+ edge padding (YouTube circular crop eats corners)
- Single PNG asset, transparent BG, 800x800 master

Outputs:
- brand/au-dealer-math/channel-logo.png (800x800, transparent BG, master)
- brand/au-dealer-math/channel-logo-bg.png (800x800, charcoal circle BG, for profile pic upload)
- brand/au-dealer-math/channel-watermark-150.png (150x150, transparent BG, for video watermark)

Run: python generator/au-dealer-math/generate-channel-logo.py
"""

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

REPO = Path(r"C:\dev\Claude")
OUT_DIR = REPO / "brand" / "au-dealer-math"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Brand palette
CHARCOAL = (43, 43, 43, 255)
OUTBACK_ORANGE = (209, 122, 61, 255)
CREAM = (245, 239, 230, 255)
TRANSPARENT = (0, 0, 0, 0)

FONTS_DIR = REPO / "fonts"
DMSANS_BOLD = FONTS_DIR / "DM_Sans" / "DMSans-Bold.ttf"
ARIAL_BLACK = Path("C:/Windows/Fonts/ariblk.ttf")
display_font_path = ARIAL_BLACK if ARIAL_BLACK.exists() else DMSANS_BOLD


def measure(draw, text, f):
    bb = draw.textbbox((0, 0), text, font=f)
    return bb[2] - bb[0], bb[3] - bb[1]


def fit_text(draw, text, max_w, max_h, font_path, start_size=400):
    size = start_size
    while size > 50:
        f = ImageFont.truetype(str(font_path), size)
        w, h = measure(draw, text, f)
        if w <= max_w and h <= max_h:
            return f, w, h
        size -= 8
    f = ImageFont.truetype(str(font_path), 50)
    return f, *measure(draw, text, f)


# ============================================================
# Logo design: "AU" stacked over "DM" with orange "$" accent
# Reads as "AUDM" but visually distinctive at small sizes.
# Square crop friendly (YouTube circular crop preserves the centre).
# ============================================================

def render_logo(size=800, with_circle_bg=True, padding_pct=0.18):
    """Render the AUDM monogram logo at any square size.

    Design: tight 4-letter monogram "AUDM" centred, with orange underline,
    on optional charcoal circle background. Per 2026 faceless-channel
    research: simpler reads better at 16x16 sub-feed avatar size.
    """
    img = Image.new("RGBA", (size, size), TRANSPARENT)
    draw = ImageDraw.Draw(img)

    # Optional charcoal circle BG
    if with_circle_bg:
        edge = int(size * 0.02)
        draw.ellipse([edge, edge, size - edge, size - edge], fill=CHARCOAL)

    pad = int(size * padding_pct)
    inner_w = size - 2 * pad
    inner_h = size - 2 * pad
    cx = size // 2
    cy = size // 2

    # Auto-fit "AUDM" — fill ~85% of inner area
    target_w = int(inner_w * 0.92)
    target_h = int(inner_h * 0.65)
    f, _, _ = fit_text(draw, "AUDM", target_w, target_h, display_font_path, start_size=int(size * 0.55))

    # Render text to a temp transparent image to get the ACTUAL rendered pixel bbox
    # (PIL textbbox returns font metric bbox, which includes phantom descender
    # space for caps-only — causes underline to land mid-letter)
    temp_w = size * 2
    temp_h = size * 2
    temp = Image.new("L", (temp_w, temp_h), 0)
    temp_draw = ImageDraw.Draw(temp)
    temp_draw.text((temp_w // 2, temp_h // 2), "AUDM", font=f, fill=255, anchor="mm")
    pixel_bbox = temp.getbbox()  # actual rendered pixel bbox
    pixel_w = pixel_bbox[2] - pixel_bbox[0]
    pixel_h = pixel_bbox[3] - pixel_bbox[1]

    # Now draw centred at (cx, cy) using anchor="mm" — text is positioned
    # such that its actual rendered pixel centre lands at (cx, cy_offset)
    cy_offset = cy - int(size * 0.04)  # slightly above middle to leave underline space
    draw.text((cx, cy_offset), "AUDM", font=f, fill=CREAM, anchor="mm")

    # Compute actual rendered text bottom: cy_offset + pixel_h//2
    actual_text_bottom = cy_offset + pixel_h // 2

    # Orange underline below actual rendered bottom
    underline_y = actual_text_bottom + int(size * 0.04)
    underline_w = int(pixel_w * 0.7)
    underline_thickness = max(5, int(size * 0.022))
    draw.rectangle([cx - underline_w // 2, underline_y,
                    cx + underline_w // 2, underline_y + underline_thickness],
                   fill=OUTBACK_ORANGE)

    return img


# ============================================================
# Render all three outputs
# ============================================================

# Master logo (800x800, charcoal circle BG, for profile pic upload)
master = render_logo(size=800, with_circle_bg=True)
master_path = OUT_DIR / "channel-logo.png"
master.save(master_path, "PNG", optimize=True)
print(f"[OK] Master logo (profile pic): {master_path}  ({master_path.stat().st_size // 1024}KB · 800x800)")

# Transparent BG version (for use over varied backgrounds, end screens, intros)
master_no_bg = render_logo(size=800, with_circle_bg=False)
master_no_bg_path = OUT_DIR / "channel-logo-transparent.png"
master_no_bg.save(master_no_bg_path, "PNG", optimize=True)
print(f"[OK] Transparent logo: {master_no_bg_path}  ({master_no_bg_path.stat().st_size // 1024}KB · 800x800)")

# Watermark 150x150 (YouTube branding watermark — bottom-right of every video)
watermark = render_logo(size=150, with_circle_bg=True)
watermark_path = OUT_DIR / "channel-watermark-150.png"
watermark.save(watermark_path, "PNG", optimize=True)
print(f"[OK] Watermark (150x150): {watermark_path}  ({watermark_path.stat().st_size // 1024}KB · 150x150)")

# Tiny preview (16x16 - sub feed avatar size — sanity check that it reads at small)
preview_16 = master.resize((16, 16), Image.LANCZOS)
preview_path = OUT_DIR / "channel-logo-16x16-preview.png"
preview_16.save(preview_path, "PNG")
print(f"[OK] 16x16 preview (sub feed test): {preview_path}")
