# Generate dollar-figure overlay PNGs for AU Dealer Math V1.
# Outputs transparent 1920x1080 PNGs with bold text + drop shadow + thin stroke.
# All overlays positioned in upper-third so Submagic captions can sit at bottom.

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

REPO = Path(r"C:\dev\Claude")
OUT_DIR = REPO / "content" / "au-dealer-math" / "scripts" / "v01-renders" / "overlays"
OUT_DIR.mkdir(parents=True, exist_ok=True)

FONT_CANDIDATES = [
    r"C:\Windows\Fonts\impact.ttf",
    r"C:\Windows\Fonts\ariblk.ttf",
    r"C:\Windows\Fonts\arialbd.ttf",
    r"C:\Windows\Fonts\arial.ttf",
]


def get_font(size):
    for path in FONT_CANDIDATES:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def render_overlay(text, fontsize, y_fraction, output_name, color=(255, 255, 255)):
    """Clean professional text overlay:
    - PIL anti-aliased stroke (4px) for crisp edges
    - Drop shadow (offset 6px, semi-transparent black) for depth
    - Centered horizontally, positioned at y_fraction (0=top, 1=bottom)
    """
    W, H = 1920, 1080
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    font = get_font(fontsize)

    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    x = (W - tw) // 2 - bbox[0]
    y = int(H * y_fraction) - th // 2 - bbox[1]

    # Drop shadow (anti-aliased, semi-transparent black, 6px offset)
    shadow_offset = 6
    draw.text(
        (x + shadow_offset, y + shadow_offset),
        text,
        font=font,
        fill=(0, 0, 0, 180),
        stroke_width=4,
        stroke_fill=(0, 0, 0, 180),
    )
    # Main text with thin black stroke for crisp readable edge
    draw.text(
        (x, y),
        text,
        font=font,
        fill=color,
        stroke_width=4,
        stroke_fill=(0, 0, 0),
    )

    out_path = OUT_DIR / f"{output_name}.png"
    img.save(out_path, "PNG")
    return out_path


# All overlays positioned in upper-third (y=0.30) so Submagic captions
# can sit at bottom (y=0.85+). Hook + emphasis overlays slightly lower
# at y=0.40 since they're standalone moments without competing captions.
#
# Math accuracy verified:
#   $300/wk × 52wks × 4yr = $62,400
#   $300/wk × 52wks × 7yr = $109,200
#   $109,200 - $62,400 = $46,800 (the "more" amount)
#   Aftercare retail $1,500-$3,000 - cost $500 = gross $1,000-$2,500
OVERLAYS = [
    ("01-hook-300-week",       "$300/WEEK",                  280, 0.40, (255, 215, 0)),    # yellow hook
    ("02-four-years",          "4 YEARS = $62,400",          130, 0.30, (255, 255, 255)),  # white
    ("03-seven-years",         "7 YEARS = $109,200",         130, 0.30, (255, 255, 255)),
    ("04-46k-more",            "$46,800 MORE",               200, 0.40, (255, 215, 0)),    # yellow emphasis
    ("05-aftercare-retail",    "$1,500-$3,000 RETAIL",       120, 0.30, (255, 255, 255)),  # FIXED: was $2,000
    ("06-aftercare-cost",      "$500 DEALER COST",           120, 0.30, (255, 100, 100)),  # red for cost
    ("07-aftercare-gross",     "$1,000-$2,500 GROSS",        140, 0.30, (100, 255, 100)),  # green - FIXED: was $1,500
]

print(f"Generating {len(OVERLAYS)} overlays -> {OUT_DIR}")
for name, text, size, yfrac, color in OVERLAYS:
    path = render_overlay(text, size, yfrac, name, color=color)
    print(f"  {path.name:30s} '{text}'  ({path.stat().st_size // 1024}KB)")
print(f"\nDone.")
