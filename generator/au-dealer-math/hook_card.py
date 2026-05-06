"""AUDM Shorts hook-card production renderer (variant B locked).

Produces a 1080x1920 PNG with:
  - Cream BG #F5EFE6
  - Centred main hook in Arial Black, charcoal #2B2B2B
  - Orange #D17A3D highlighter strip behind the lower 60% of the hook
  - Orange divider bar + cream-on-charcoal? no — charcoal-on-cream sublabel
    (e.g. "DEALER MARGIN", "F&I PIPELINE", "RATE LOAD")

Variant chosen 2026-05-06 after Adrian reviewed the prototype contact sheet
([proto-shorts-hook-card-v2.py](proto-shorts-hook-card-v2.py)). Reasons:
  - Highlighter strip ties to brand DNA "highlight one thing" (design-system-audm.md)
  - Orange-on-cream-via-strip + dealer-vocab label = on-brand calm-authority +
    grid-thumb scroll-stop, neither bro-finance nor quiet-documentary
  - Composes with the existing doc-forensics opener cleanly (cream → charcoal cut)

Usage from a build script:
  from hook_card import render_card, HOOK_LABELS
  render_card(hook_text="$4,800", label=HOOK_LABELS["$4,800"], out_path=Path("card.png"))

Then ffmpeg-loop the PNG into the video segment (see build-v02-short-1.py).
"""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

REPO = Path(r"C:\dev\Claude")

# Brand palette LOCKED (design-system-audm.md)
CHARCOAL = (43, 43, 43)
ORANGE   = (209, 122, 61)
CREAM    = (245, 239, 230)

DMSANS_BOLD = REPO / "fonts" / "DM_Sans" / "DMSans-Bold.ttf"
ARIAL_BLACK = Path("C:/Windows/Fonts/ariblk.ttf")
DISPLAY_FONT = ARIAL_BLACK if ARIAL_BLACK.exists() else DMSANS_BOLD

# Shorts canvas
W, H = 1080, 1920

# Hook → dealer-vocab sublabel map. Extend as new V[N] Shorts ship.
HOOK_LABELS = {
    "$4,800":    "DEALER MARGIN",
    "$3,000":    "RATE LOAD",
    "+4 POINTS": "RATE LOAD",
    "3 ROOMS":   "F&I PIPELINE",
    "$2,000":    "AFTERCARE MARGIN",
}


def _fit_font(text, font_path, max_w, start=440, min_size=80, step=8):
    """Return largest font where `text` fits within `max_w`. Returns (font, bbox)."""
    size = start
    while size > min_size:
        f = ImageFont.truetype(str(font_path), size)
        bbox = f.getbbox(text)
        tw = bbox[2] - bbox[0]
        if tw <= max_w:
            return f, bbox
        size -= step
    f = ImageFont.truetype(str(font_path), min_size)
    return f, f.getbbox(text)


def _draw_sublabel(draw, label, hook_bottom_y):
    """Orange divider bar + charcoal sublabel below the main hook."""
    sub_f = ImageFont.truetype(str(DMSANS_BOLD), 110)
    bb = sub_f.getbbox(label.upper())
    sub_tw = bb[2] - bb[0]
    sub_x = (W - sub_tw) // 2 - bb[0]

    bar_w, bar_h = 80, 8
    bar_x = (W - bar_w) // 2
    bar_y = hook_bottom_y + 50
    draw.rectangle([bar_x, bar_y, bar_x + bar_w, bar_y + bar_h], fill=ORANGE)

    sub_y = bar_y + bar_h + 30 - bb[1]
    draw.text((sub_x, sub_y), label.upper(), font=sub_f, fill=CHARCOAL)


def render_card(hook_text: str, label: str | None, out_path: Path) -> Path:
    """Render variant B hook-card to `out_path` as 1080x1920 PNG."""
    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)

    f, bbox = _fit_font(hook_text, DISPLAY_FONT, max_w=int(W * 0.78), start=440)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]

    # Lift hook up if sublabel present so composite stays vertically centred
    cy = H // 2 - (110 if label else 0)
    x = (W - tw) // 2 - bbox[0]
    y = cy - th // 2 - bbox[1]

    # Orange highlighter strip behind lower 60% of the text
    pad_x, pad_y = 32, 18
    rect_x0 = x + bbox[0] - pad_x
    rect_x1 = x + bbox[0] + tw + pad_x
    rect_y0 = y + bbox[1] + int(th * 0.40)
    rect_y1 = y + bbox[1] + th + pad_y
    draw.rectangle([rect_x0, rect_y0, rect_x1, rect_y1], fill=ORANGE)

    # Charcoal hook on top of strip
    draw.text((x, y), hook_text, font=f, fill=CHARCOAL)

    if label:
        hook_bottom = y + bbox[1] + th + pad_y
        _draw_sublabel(draw, label, hook_bottom)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(out_path, optimize=True)
    return out_path


if __name__ == "__main__":
    # Self-test: render every known hook to a scratch dir.
    OUT = REPO / "content" / "au-dealer-math" / "scripts" / "v02-renders" / "hook-card-proto" / "production-test"
    OUT.mkdir(parents=True, exist_ok=True)
    for hook, label in HOOK_LABELS.items():
        slug = hook.replace("$", "").replace(",", "").replace(" ", "-").replace("+", "plus").lower()
        render_card(hook, label, OUT / f"card-{slug}.png")
        print(f"  [ok] {hook} -> {label}  ({slug}.png)")
    print(f"\nDone. {OUT}")
