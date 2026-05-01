"""Generate AU Dealer Math channel logo v2 — punchier, brand-coherent.

v2 changes vs v1 (placeholder):
- Tighter "AUDM" wordmark (bigger, less padding waste at small sizes)
- Replace flat orange underline with HIGHLIGHT STROKE — orange marker bar that
  overlaps the bottom 1/3 of the letters. Visual metaphor: "the highlighted
  clause" — exact same motif as the cheatsheet hero image. Brand consistency
  across all surfaces.
- Stays readable at 16x16 sub-feed avatar size (the killer test)

Outputs:
- brand/au-dealer-math/channel-logo-v2.png (800x800, charcoal circle BG)
- brand/au-dealer-math/channel-logo-v2-transparent.png (transparent BG)
- brand/au-dealer-math/channel-watermark-v2-150.png (video watermark)
- brand/au-dealer-math/channel-logo-v2-16x16-preview.png (sanity check)
"""

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

REPO = Path(r"C:\dev\Claude")
OUT_DIR = REPO / "brand" / "au-dealer-math"
OUT_DIR.mkdir(parents=True, exist_ok=True)

CHARCOAL = (43, 43, 43, 255)
OUTBACK_ORANGE = (209, 122, 61, 230)  # 90% alpha so it reads as marker over letters
CREAM = (245, 239, 230, 255)
TRANSPARENT = (0, 0, 0, 0)

FONTS_DIR = REPO / "fonts"
DMSANS_BOLD = FONTS_DIR / "DM_Sans" / "DMSans-Bold.ttf"
ARIAL_BLACK = Path("C:/Windows/Fonts/ariblk.ttf")
display_font_path = ARIAL_BLACK if ARIAL_BLACK.exists() else DMSANS_BOLD


def measure(draw, text, f):
    bb = draw.textbbox((0, 0), text, font=f)
    return bb[2] - bb[0], bb[3] - bb[1]


def fit_text(draw, text, max_w, max_h, font_path, start_size=600):
    size = start_size
    while size > 50:
        f = ImageFont.truetype(str(font_path), size)
        w, h = measure(draw, text, f)
        if w <= max_w and h <= max_h:
            return f, w, h
        size -= 8
    f = ImageFont.truetype(str(font_path), 50)
    return f, *measure(draw, text, f)


def render_logo(size=800, with_circle_bg=True):
    """Render the AUDM logo with highlight-stroke motif at any square size."""
    img = Image.new("RGBA", (size, size), TRANSPARENT)
    draw = ImageDraw.Draw(img)

    # Optional charcoal circle BG (full bleed, slight inset for clean edge)
    if with_circle_bg:
        edge = max(2, int(size * 0.015))
        draw.ellipse([edge, edge, size - edge, size - edge], fill=CHARCOAL)

    # Inner area — aggressive (8% padding) so wordmark dominates at small sizes
    pad = int(size * 0.08)
    inner_w = size - 2 * pad
    inner_h = size - 2 * pad
    cx = size // 2
    cy = size // 2

    # Auto-fit "AUDM" — fill ~98% of inner width, ~85% of inner height
    target_w = int(inner_w * 0.98)
    target_h = int(inner_h * 0.85)
    f, _, _ = fit_text(draw, "AUDM", target_w, target_h, display_font_path,
                       start_size=int(size * 0.65))

    # Render text to temp image to get actual rendered pixel bbox
    temp_w = size * 2
    temp_h = size * 2
    temp = Image.new("L", (temp_w, temp_h), 0)
    temp_draw = ImageDraw.Draw(temp)
    temp_draw.text((temp_w // 2, temp_h // 2), "AUDM", font=f, fill=255, anchor="mm")
    pixel_bbox = temp.getbbox()
    pixel_w = pixel_bbox[2] - pixel_bbox[0]
    pixel_h = pixel_bbox[3] - pixel_bbox[1]

    # Cy_offset: nudge text slightly up so highlight stroke balances visually
    cy_offset = cy - int(size * 0.02)

    # Compute the bbox of where the text WILL render at (cx, cy_offset) anchor mm
    text_left = cx - pixel_w // 2
    text_right = cx + pixel_w // 2
    text_top = cy_offset - pixel_h // 2
    text_bottom = cy_offset + pixel_h // 2

    # ============================================================
    # HIGHLIGHT STROKE — orange marker bar that overlaps bottom of letters
    # This is the brand visual element (same as cheatsheet image's clause marker)
    # Bumped to 50% of letter height + 8% extension so it reads at 16x16
    # ============================================================
    stroke_extend = int(pixel_w * 0.08)
    stroke_x_start = text_left - stroke_extend
    stroke_x_end = text_right + stroke_extend
    # Vertical: covers bottom 50% of text height (more prominent at small sizes)
    stroke_y_start = text_bottom - int(pixel_h * 0.50)
    stroke_y_end = text_bottom + int(pixel_h * 0.08)
    # Slight tilt? No — keep level for digital crispness at small sizes.
    draw.rectangle([stroke_x_start, stroke_y_start,
                    stroke_x_end, stroke_y_end],
                   fill=OUTBACK_ORANGE)

    # Now draw the wordmark on TOP so cream letters sit cleanly over the stroke
    draw.text((cx, cy_offset), "AUDM", font=f, fill=CREAM, anchor="mm")

    return img


# ============================================================
# Render outputs
# ============================================================

# Master logo (800x800, charcoal circle BG, for profile pic)
master = render_logo(size=800, with_circle_bg=True)
master_path = OUT_DIR / "channel-logo-v2.png"
master.save(master_path, "PNG", optimize=True)
print(f"[OK] v2 master logo (profile pic): {master_path}  ({master_path.stat().st_size // 1024}KB · 800x800)")

# Transparent BG version (for end screens, overlays, intros)
master_no_bg = render_logo(size=800, with_circle_bg=False)
master_no_bg_path = OUT_DIR / "channel-logo-v2-transparent.png"
master_no_bg.save(master_no_bg_path, "PNG", optimize=True)
print(f"[OK] v2 transparent logo: {master_no_bg_path}  ({master_no_bg_path.stat().st_size // 1024}KB · 800x800)")

# Watermark 150x150
watermark = render_logo(size=150, with_circle_bg=True)
watermark_path = OUT_DIR / "channel-watermark-v2-150.png"
watermark.save(watermark_path, "PNG", optimize=True)
print(f"[OK] v2 watermark (150x150): {watermark_path}  ({watermark_path.stat().st_size // 1024}KB · 150x150)")

# 16x16 sanity check (sub-feed avatar test)
preview_16 = master.resize((16, 16), Image.LANCZOS)
preview_path = OUT_DIR / "channel-logo-v2-16x16-preview.png"
preview_16.save(preview_path, "PNG")
print(f"[OK] v2 16x16 preview: {preview_path}")

# 64x64 (medium scale check)
preview_64 = master.resize((64, 64), Image.LANCZOS)
preview_64_path = OUT_DIR / "channel-logo-v2-64x64-preview.png"
preview_64.save(preview_64_path, "PNG")
print(f"[OK] v2 64x64 preview: {preview_64_path}")
