"""Generate side-by-side comparison of v1 vs v2 brand assets.
Output: brand/au-dealer-math/_compare-v1-vs-v2.png

For Adrian's review when AFK comes back.
"""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

REPO = Path(r"C:\dev\Claude")
BRAND = REPO / "brand" / "au-dealer-math"
OUT = BRAND / "_compare-v1-vs-v2.png"

CHARCOAL = (43, 43, 43)
CREAM = (245, 239, 230)
ORANGE = (209, 122, 61)

# Layout: 2 banners stacked vertically (each at half-size for compare),
# 2 logos side-by-side underneath at decent size
W = 1600
banner_w = 1280
banner_h = int(banner_w * 1440 / 2560)  # ~720
logo_size = 300
margin = 40
label_h = 50

H = margin + label_h + banner_h + margin + label_h + banner_h + margin + label_h + logo_size + margin

img = Image.new("RGB", (W, H), CHARCOAL)
draw = ImageDraw.Draw(img)

FONTS_DIR = REPO / "fonts"
DMSANS_BOLD = FONTS_DIR / "DM_Sans" / "DMSans-Bold.ttf"
INTER = FONTS_DIR / "Inter" / "Inter-Regular.ttf"
label_font = ImageFont.truetype(str(DMSANS_BOLD), 36)
small_font = ImageFont.truetype(str(INTER), 22)

y = margin

# v1 banner
draw.text((margin, y), "v1 — placeholder (subpar per Adrian 2026-05-01)", font=label_font, fill=CREAM)
y += label_h
b1 = Image.open(BRAND / "channel-banner-v1.png").convert("RGB")
b1 = b1.resize((banner_w, banner_h), Image.LANCZOS)
img.paste(b1, ((W - banner_w) // 2, y))
y += banner_h + margin

# v2 banner
draw.text((margin, y), "v2 — showstopper redesign", font=label_font, fill=ORANGE)
y += label_h
b2 = Image.open(BRAND / "channel-banner-v2.png").convert("RGB")
b2 = b2.resize((banner_w, banner_h), Image.LANCZOS)
img.paste(b2, ((W - banner_w) // 2, y))
y += banner_h + margin

# Logo compare
draw.text((margin, y), "Logo:  v1   →   v2 (highlight stroke = cheatsheet motif)", font=label_font, fill=CREAM)
y += label_h

l1 = Image.open(BRAND / "channel-logo.png").convert("RGB")
l1 = l1.resize((logo_size, logo_size), Image.LANCZOS)
l2 = Image.open(BRAND / "channel-logo-v2.png").convert("RGB")
l2 = l2.resize((logo_size, logo_size), Image.LANCZOS)

logo_gap = 100
total_w = logo_size * 2 + logo_gap
logo_x = (W - total_w) // 2
img.paste(l1, (logo_x, y))
img.paste(l2, (logo_x + logo_size + logo_gap, y))

# Label under each
draw.text((logo_x + logo_size // 2 - 10, y + logo_size + 10),
          "v1", font=label_font, fill=(120, 120, 120))
draw.text((logo_x + logo_size + logo_gap + logo_size // 2 - 10, y + logo_size + 10),
          "v2", font=label_font, fill=ORANGE)

img.save(OUT, "PNG", optimize=True)
print(f"[OK] Compare: {OUT}  ({OUT.stat().st_size // 1024}KB)")
