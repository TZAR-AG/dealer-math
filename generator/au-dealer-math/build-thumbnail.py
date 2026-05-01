"""AUDM thumbnail builder — locked V1+ spec.

Builds 1280x720 YT thumbnails with the approved V1 composition:
- MJ photo backdrop (right-weighted action, left negative space — engineered via the
  locked thumbnail MJ prompt)
- Left-side stacked headline (hero word in outback orange, supporting words cream)
- Slot-based layout — mathematically zero overlap, even spacing
- 92%-of-slot fill = tight but breathing
- Subtle vignette + film grain for editorial finish
- NO AU pill (channel name carries the geo-anchor)

Usage as module:
    from build_thumbnail import render
    render(
        mj_image="C:/Users/adria/Downloads/audealermath_v04_handpulling_xxx.png",
        hero_word="STOP",
        stack_words=["LOWBALLING", "YOUR", "TRADE", "IN"],
        output_path="content/au-dealer-math/scripts/v04-thumbnail.png",
    )

Usage as CLI:
    python build-thumbnail.py <mj_image> <hero> <stack...> <output>

V2-V12 workflow:
1. Render MJ image with the AUDM thumbnail-engineered prompt (right-weighted
   subject, left negative space) — see saas-prompts/midjourney.md
2. Upscale Subtle, download to Downloads/
3. Call render() with image path + 1 hero word + 2-4 stack words

Spec locked 2026-05-01 after V1 thumbnail iteration.
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
from pathlib import Path
import random
import sys

REPO = Path(r"C:\dev\Claude")

# Brand palette LOCKED per design-system-audm.md
CHARCOAL = (43, 43, 43)
OUTBACK_ORANGE = (209, 122, 61)
CREAM = (245, 239, 230)

FONTS_DIR = REPO / "fonts"
DMSANS_BOLD = FONTS_DIR / "DM_Sans" / "DMSans-Bold.ttf"
ARIAL_BLACK = Path("C:/Windows/Fonts/ariblk.ttf")
DISPLAY_FONT = ARIAL_BLACK if ARIAL_BLACK.exists() else DMSANS_BOLD

W, H = 1280, 720


def _font(size):
    return ImageFont.truetype(str(DISPLAY_FONT), size)


def _measure(draw, text, f):
    bb = draw.textbbox((0, 0), text, font=f)
    return bb[2] - bb[0], bb[3] - bb[1]


def _draw_text_punch(draw, position, text, f, fill, stroke_w=6, shadow=8):
    """Stroke + drop shadow for legibility over photo."""
    sx, sy = position[0] + shadow, position[1] + shadow
    draw.text((sx, sy), text, font=f, fill=(0, 0, 0, 220),
              stroke_width=stroke_w, stroke_fill=(0, 0, 0, 220))
    draw.text(position, text, font=f, fill=fill,
              stroke_width=stroke_w, stroke_fill=(0, 0, 0))


def render(mj_image, hero_word, stack_words, output_path):
    """Build the AUDM thumbnail. Returns output Path.

    Args:
        mj_image: Path to MJ-generated photo backdrop (will be cover-fit to 1280x720)
        hero_word: Single word for top, rendered in outback orange (e.g. "NEVER", "STOP", "AVOID")
        stack_words: List of 2-4 supporting words rendered in cream below hero
        output_path: Where to save the 1280x720 PNG
    """
    mj_image = Path(mj_image)
    output_path = Path(output_path)
    assert mj_image.exists(), f"MJ image not found: {mj_image}"
    assert isinstance(stack_words, list) and 2 <= len(stack_words) <= 4, \
        "stack_words must be a list of 2-4 supporting words"

    # ============================================================
    # Backdrop — cover-fit MJ image
    # ============================================================
    src = Image.open(mj_image).convert("RGB")
    src = ImageOps.fit(src, (W, H), Image.LANCZOS, centering=(0.55, 0.5))
    img = src.convert("RGBA")

    # Left-side darkening gradient (text legibility on left negative space)
    left_overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    lo = ImageDraw.Draw(left_overlay)
    for x in range(W):
        t = max(0, 1 - x / (W * 0.55)) ** 1.4
        alpha = int(220 * t)
        lo.line([(x, 0), (x, H)], fill=(0, 0, 0, alpha))
    img = Image.alpha_composite(img, left_overlay)

    # Subtle vignette
    vignette = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    vd = ImageDraw.Draw(vignette)
    for r in range(0, 220, 3):
        alpha = int(120 * (r / 220) ** 2)
        vd.rectangle([r, r, W - r, H - r], outline=(0, 0, 0, alpha), width=3)
    vignette = vignette.filter(ImageFilter.GaussianBlur(radius=50))
    img = Image.alpha_composite(img, vignette)

    draw = ImageDraw.Draw(img)

    # ============================================================
    # Slot-based headline layout (zero overlap)
    # ============================================================
    LEFT_PAD = 50
    LEFT_W = 500
    TOP_PAD = 40
    BOTTOM_PAD = 40

    n_total = 1 + len(stack_words)
    hero_share = 1.3
    total_shares = hero_share + len(stack_words)
    available_h = H - TOP_PAD - BOTTOM_PAD
    unit_h = available_h / total_shares
    hero_slot_h = int(unit_h * hero_share)
    stack_slot_h = int(unit_h)

    # Hero word — fill 92% of slot
    hero_target_h = int(hero_slot_h * 0.92)
    hero_size = 240
    while hero_size > 100:
        hero_f = _font(hero_size)
        hw, hh = _measure(draw, hero_word, hero_f)
        if hw <= LEFT_W and hh <= hero_target_h:
            break
        hero_size -= 4
    hero_f = _font(hero_size)
    hw, hh = _measure(draw, hero_word, hero_f)

    # Stack words — fill 92% of stack slot, fit largest
    stack_target_h = int(stack_slot_h * 0.92)
    biggest = max(stack_words, key=len)
    stack_size = 130
    while stack_size > 50:
        stack_f = _font(stack_size)
        sw, sh = _measure(draw, biggest, stack_f)
        if sw <= LEFT_W and sh <= stack_target_h:
            break
        stack_size -= 4
    stack_f = _font(stack_size)

    # Draw — each word vertically centered in its slot
    y = TOP_PAD

    # Hero in orange
    hero_y = y + (hero_slot_h - hh) // 2
    _draw_text_punch(draw, (LEFT_PAD, hero_y), hero_word, hero_f,
                     OUTBACK_ORANGE, stroke_w=7, shadow=8)
    y += hero_slot_h

    # Stack in cream
    for word in stack_words:
        _, word_h = _measure(draw, word, stack_f)
        word_y = y + (stack_slot_h - word_h) // 2
        _draw_text_punch(draw, (LEFT_PAD, word_y), word, stack_f,
                         CREAM, stroke_w=5, shadow=6)
        y += stack_slot_h

    # ============================================================
    # Subtle film grain — editorial polish
    # ============================================================
    random.seed(42)
    grain = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(grain)
    for _ in range(W * H // 100):
        gx = random.randint(0, W - 1)
        gy = random.randint(0, H - 1)
        val = random.randint(0, 25)
        gd.point((gx, gy), fill=(255, 255, 255, val))
    img = Image.alpha_composite(img, grain)

    # Save
    output_path.parent.mkdir(parents=True, exist_ok=True)
    img.convert("RGB").save(output_path, "PNG", optimize=True)
    return output_path


# ============================================================
# CLI usage
# ============================================================
if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Usage: build-thumbnail.py <mj_image> <hero> <stack1> <stack2> [stack3] [stack4] <output>")
        print("Example: build-thumbnail.py v04.png STOP LOWBALLING YOUR TRADE IN v04-thumb.png")
        sys.exit(1)

    mj_path = sys.argv[1]
    hero = sys.argv[2]
    out = sys.argv[-1]
    stack = sys.argv[3:-1]

    result = render(
        mj_image=mj_path,
        hero_word=hero,
        stack_words=stack,
        output_path=out,
    )
    print(f"[OK] Thumbnail: {result} ({result.stat().st_size // 1024}KB)")
