# Generate dollar-figure / percent overlay PNGs for AU Dealer Math V3
# (The Aftercare Room).
#
# Outputs transparent 1920x1080 PNGs with bold text + drop shadow + thin
# stroke. All overlays positioned in upper-third so captions can sit at
# bottom. Visual style matches V1/V2 exactly (Impact font, color codes
# yellow=hook/emphasis, white=neutral, red=cost-to-customer, green=dealer-
# saves, orange=CTA).
#
# Source phrases + timestamps cross-verified against
# content/au-dealer-math/scripts/v03-renders/vo-transcriptions.json
# (Whisper word-level). Timing wired up in build-v3-davinci.py OVERLAYS list.

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

REPO = Path(r"C:\dev\Claude")
OUT_DIR = REPO / "content" / "au-dealer-math" / "scripts" / "v03-renders" / "overlays"
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
    """Anti-aliased text with drop shadow + black stroke. V1/V2 design pattern."""
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
#   yellow (255, 215, 0)   - hook / emphasis / customer-facing total
#   white  (255, 255, 255) - neutral retail numbers
#   red    (255, 100, 100) - cost-to-customer / lower attach (relative comp)
#   green  (100, 255, 100) - dealer gross / margin earned
#   orange (255, 165, 0)   - CTA / outback orange brand
#
# Font sizes calibrated so the longest text (entry 13) fits within frame
# without wrapping — Impact at 90px renders that string at ~1700px wide.
OVERLAYS = [
    # SCENE 1 HOOK
    ("01-hook-margin-tease",     "$1,500-$3,000 MARGIN",         150, 0.30, (255, 215, 0)),    # yellow hook

    # SCENE 4 MATH — paint protection
    ("02-paint-retail",          "RETAIL: $1,500-$2,500",        140, 0.30, (255, 255, 255)),  # white neutral
    ("03-paint-cost",            "DEALER COST: $400-$600",       135, 0.30, (255, 100, 100)),  # red cost
    ("04-paint-margin",          "MARGIN: 70-75%",               170, 0.30, (100, 255, 100)),  # green margin

    # SCENE 4 MATH — window tint
    ("05-tint-retail",           "RETAIL: $600-$700",            150, 0.30, (255, 255, 255)),
    ("06-tint-cost",             "DEALER COST: $200-$300",       135, 0.30, (255, 100, 100)),
    ("07-tint-margin",           "MARGIN: 50-60%",               170, 0.30, (100, 255, 100)),

    # SCENE 4 MATH — stack
    ("08-stack-customer",        "CUSTOMER PAYS: $2,700",        140, 0.30, (255, 215, 0)),    # yellow stack reveal
    ("09-stack-dealer-gross",    "DEALER GROSS: $1,900",         140, 0.30, (100, 255, 100)),  # green
    ("10-full-attach",           "FULL ATTACH: $3,000-$4,000",   125, 0.30, (255, 215, 0)),    # yellow ceiling

    # SCENE 4 MATH — penetration
    ("11-aftercare-attach",      "AFTERCARE ATTACH: 60-80%",     130, 0.30, (255, 215, 0)),    # yellow (the headline)
    ("12-finance-attach",        "FINANCE ATTACH: 20-30%",       135, 0.30, (255, 100, 100)),  # red (relative comp)
    ("13-avg-gross",             "AVG AFTERCARE GROSS: $1,500-$3,000/CAR", 90, 0.30, (255, 215, 0)),
]

print(f"Generating {len(OVERLAYS)} V3 overlays -> {OUT_DIR}")
for name, text, size, yfrac, color in OVERLAYS:
    path = render_overlay(text, size, yfrac, name, color=color)
    print(f"  {path.name:35s} '{text}'  ({path.stat().st_size // 1024}KB)")
print(f"\nDone.")
