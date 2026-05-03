# Generate dollar-figure / rate / CTA overlay PNGs for AU Dealer Math V2.
# Outputs transparent 1920x1080 PNGs with bold text + drop shadow + thin stroke.
# All overlays positioned in upper-third so captions can sit at bottom.

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

REPO = Path(r"C:\dev\Claude")
OUT_DIR = REPO / "content" / "au-dealer-math" / "scripts" / "v02-renders" / "overlays"
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
    """Anti-aliased text with drop shadow + black stroke. Same V1 design pattern."""
    W, H = 1920, 1080
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    font = get_font(fontsize)

    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    x = (W - tw) // 2 - bbox[0]
    y = int(H * y_fraction) - th // 2 - bbox[1]

    # Drop shadow
    shadow_offset = 6
    draw.text(
        (x + shadow_offset, y + shadow_offset),
        text,
        font=font,
        fill=(0, 0, 0, 180),
        stroke_width=4,
        stroke_fill=(0, 0, 0, 180),
    )
    # Main text with stroke
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


# Color codes:
#   yellow (255, 215, 0)   - hook / emphasis
#   white  (255, 255, 255) - neutral numbers
#   red    (255, 100, 100) - cost-to-customer / dealer pocket
#   green  (100, 255, 100) - dealer gross / what you save
#   orange (255, 165, 0)   - CTA / outback orange brand
OVERLAYS = [
    ("01-hook-9-percent",        "FINANCE RATE: 9.00%",        180, 0.40, (255, 215, 0)),    # yellow hook
    ("02-bank-5-percent",        "BANK APPROVED: 5%",          150, 0.30, (100, 255, 100)),  # green - what you should pay
    ("03-dealer-9-percent",      "DEALER OFFERS: 9%",          150, 0.30, (255, 100, 100)),  # red - what they ask
    ("04-spread-cost",           "+$2,000-$3,000 INTEREST",    140, 0.30, (255, 100, 100)),  # red - extra cost
    ("05-commission-pool",       "10-15% OF F&I GROSS",        140, 0.30, (255, 215, 0)),    # yellow - the mechanic
    ("06-ask-floor-rate",        "ASK FOR THE FLOOR RATE",     130, 0.40, (255, 165, 0)),    # outback orange CTA
    ("07-aftercare-tease",       "NEXT: $1,500-$3,000",        140, 0.30, (255, 215, 0)),    # yellow tease
]

print(f"Generating {len(OVERLAYS)} V2 overlays -> {OUT_DIR}")
for name, text, size, yfrac, color in OVERLAYS:
    path = render_overlay(text, size, yfrac, name, color=color)
    print(f"  {path.name:30s} '{text}'  ({path.stat().st_size // 1024}KB)")
print(f"\nDone.")
