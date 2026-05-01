"""
Build the AUDM palette swatch — locked colors per .claude/rules/design-system-audm.md

Used as MidJourney --sref (style reference) for every AUDM still prompt.
Locks color consistency across V1-V12 + thumbnails + future video sets.

Output: content/au-dealer-math/saas-prompts/_assets/audm-palette-swatch.png
        1024x1024 — three flat horizontal bars, NO text.
"""
from pathlib import Path
from PIL import Image, ImageDraw

REPO = Path(__file__).resolve().parents[2]
OUT = REPO / "content" / "au-dealer-math" / "saas-prompts" / "_assets" / "audm-palette-swatch.png"

# LOCKED palette — matches .claude/rules/design-system-audm.md + channel-banner generator
CHARCOAL = (43, 43, 43)        # #2B2B2B
CREAM = (245, 239, 230)        # #F5EFE6
OUTBACK_ORANGE = (209, 122, 61) # #D17A3D

SIZE = 1024

img = Image.new("RGB", (SIZE, SIZE), CHARCOAL)
draw = ImageDraw.Draw(img)
third = SIZE // 3
draw.rectangle([(0, 0), (SIZE, third)], fill=CHARCOAL)
draw.rectangle([(0, third), (SIZE, 2 * third)], fill=CREAM)
draw.rectangle([(0, 2 * third), (SIZE, SIZE)], fill=OUTBACK_ORANGE)

OUT.parent.mkdir(parents=True, exist_ok=True)
img.save(OUT, "PNG")
print(f"Built {OUT}")
print(f"  Charcoal:       #{'%02X%02X%02X' % CHARCOAL}")
print(f"  Cream:          #{'%02X%02X%02X' % CREAM}")
print(f"  Outback Orange: #{'%02X%02X%02X' % OUTBACK_ORANGE}")
