"""V1 thumbnail FINAL — MJ photo backdrop + brand-coherent text overlay.

Backdrop: MJ-generated photo of buyer's hand with pen on dealer contract,
two hands interacting, orange highlight strokes on clauses (matches brand motif).
Brand-engineered: subject right-weighted, left negative space for text overlay.

Composition:
- LEFT 35%: stacked headline "NEVER ANSWER THIS ONE QUESTION" (NEVER in orange)
- AU pill bottom-left
- Subtle vignette + grain for editorial finish
- Photo carries visual weight, text supports

Output: content/au-dealer-math/scripts/v01-thumbnail-final.png

Run: python generator/au-dealer-math/build-v1-thumbnail-final.py
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageOps
from pathlib import Path
import random

REPO = Path(r"C:\dev\Claude")
OUT_DIR = REPO / "content" / "au-dealer-math" / "scripts"
DOWNLOADS = Path(r"C:\Users\adria\Downloads")

# Brand palette LOCKED
CHARCOAL = (43, 43, 43)
OUTBACK_ORANGE = (209, 122, 61)
CREAM = (245, 239, 230)
YELLOW = (255, 215, 0)

# Backdrop — find latest upscaled MJ image
candidates = sorted(
    DOWNLOADS.glob("audealermath_Top-down_close-up_of_a_buyers_hand_holding_a_black_*.png"),
    key=lambda p: p.stat().st_mtime, reverse=True,
)
assert candidates, "No upscaled MJ image found in Downloads"
BACKDROP = candidates[0]
print(f"Backdrop: {BACKDROP.name}")

FONTS_DIR = REPO / "fonts"
DMSANS_BOLD = FONTS_DIR / "DM_Sans" / "DMSans-Bold.ttf"
ARIAL_BLACK = Path("C:/Windows/Fonts/ariblk.ttf")
display_font = ARIAL_BLACK if ARIAL_BLACK.exists() else DMSANS_BOLD

W, H = 1280, 720


def font(path, size):
    return ImageFont.truetype(str(path), size)


def measure(draw, text, f):
    bb = draw.textbbox((0, 0), text, font=f)
    return bb[2] - bb[0], bb[3] - bb[1]


def fit_text(draw, text, max_w, font_path, start_size=200, min_size=60):
    size = start_size
    while size > min_size:
        f = font(font_path, size)
        w, _ = measure(draw, text, f)
        if w <= max_w:
            return f
        size -= 4
    return font(font_path, min_size)


def draw_text_punch(draw, position, text, f, fill, stroke_w=6, shadow=8):
    """Stroke + drop shadow for legibility over photo."""
    sx, sy = position[0] + shadow, position[1] + shadow
    draw.text((sx, sy), text, font=f, fill=(0, 0, 0, 220),
              stroke_width=stroke_w, stroke_fill=(0, 0, 0, 220))
    draw.text(position, text, font=f, fill=fill,
              stroke_width=stroke_w, stroke_fill=(0, 0, 0))


# ============================================================
# Step 1: Load MJ image, cover-fit to 1280x720
# ============================================================
src = Image.open(BACKDROP).convert("RGB")
src = ImageOps.fit(src, (W, H), Image.LANCZOS, centering=(0.55, 0.5))  # slight right-bias to keep subject in right 2/3
img = src.convert("RGBA")

# ============================================================
# Step 2: Left-side darkening gradient (text legibility)
# Strongest on left 25%, fading to 50% (where photo subject lives)
# ============================================================
left_overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
lo = ImageDraw.Draw(left_overlay)
for x in range(W):
    # Strong on left 25%, fade to 0 by 55%
    t = max(0, 1 - x / (W * 0.55)) ** 1.4
    alpha = int(220 * t)
    lo.line([(x, 0), (x, H)], fill=(0, 0, 0, alpha))
img = Image.alpha_composite(img, left_overlay)

# ============================================================
# Step 3: Subtle vignette
# ============================================================
vignette = Image.new("RGBA", (W, H), (0, 0, 0, 0))
vd = ImageDraw.Draw(vignette)
for r in range(0, 220, 3):
    alpha = int(120 * (r / 220) ** 2)
    vd.rectangle([r, r, W - r, H - r], outline=(0, 0, 0, alpha), width=3)
vignette = vignette.filter(ImageFilter.GaussianBlur(radius=50))
img = Image.alpha_composite(img, vignette)

draw = ImageDraw.Draw(img)

# ============================================================
# Step 4: LEFT — stacked headline (slot-based layout, ZERO overlap)
# Even slots vertically: hero gets bigger slot, stacked words get equal slots.
# Each word centered in its slot. Mathematically guaranteed: no word touches another.
# ============================================================
LEFT_PAD = 50
LEFT_W = 500
TOP_PAD = 40
BOTTOM_PAD = 40

stack_words = ["ANSWER", "THIS", "ONE", "QUESTION"]
n_total = 1 + len(stack_words)  # 5 lines

# Slots: hero gets 1.3 share, others get 1.0 share each
hero_share = 1.3
total_shares = hero_share + len(stack_words)  # 1.3 + 4 = 5.3
available_h = H - TOP_PAD - BOTTOM_PAD  # 640
unit_h = available_h / total_shares
hero_slot_h = int(unit_h * hero_share)
stack_slot_h = int(unit_h)

# Hero "NEVER" — fits to ~85% of its slot height + LEFT_W width
hero_target_h = int(hero_slot_h * 0.92)
hero_size = 240
hero_f = font(display_font, hero_size)
while hero_size > 100:
    hero_f = font(display_font, hero_size)
    hw, hh = measure(draw, "NEVER", hero_f)
    if hw <= LEFT_W and hh <= hero_target_h:
        break
    hero_size -= 4
hw, hh = measure(draw, "NEVER", hero_f)

# Stack font fits to ~80% of stack slot + LEFT_W
stack_target_h = int(stack_slot_h * 0.92)
biggest = max(stack_words, key=len)
stack_size = 130
while stack_size > 50:
    stack_f = font(display_font, stack_size)
    sw, sh = measure(draw, biggest, stack_f)
    if sw <= LEFT_W and sh <= stack_target_h:
        break
    stack_size -= 4
stack_f = font(display_font, stack_size)
_, stack_h_actual = measure(draw, biggest, stack_f)

# Draw — each word vertically centered in its slot
y_cursor = TOP_PAD

# NEVER (hero)
hero_y = y_cursor + (hero_slot_h - hh) // 2
draw_text_punch(draw, (LEFT_PAD, hero_y), "NEVER", hero_f,
                OUTBACK_ORANGE, stroke_w=7, shadow=8)
y_cursor += hero_slot_h

# Stack
for word in stack_words:
    _, word_h = measure(draw, word, stack_f)
    word_y = y_cursor + (stack_slot_h - word_h) // 2
    draw_text_punch(draw, (LEFT_PAD, word_y), word, stack_f,
                    CREAM, stroke_w=5, shadow=6)
    y_cursor += stack_slot_h

# AU pill removed 2026-05-01 — channel is "AU Dealer Math", badge is redundant.

# ============================================================
# Step 6: Subtle film grain for editorial polish
# ============================================================
random.seed(42)
grain = Image.new("RGBA", (W, H), (0, 0, 0, 0))
gd = ImageDraw.Draw(grain)
for _ in range(W * H // 100):
    x = random.randint(0, W - 1)
    y = random.randint(0, H - 1)
    val = random.randint(0, 25)
    gd.point((x, y), fill=(255, 255, 255, val))
img = Image.alpha_composite(img, grain)

# ============================================================
# Save
# ============================================================
out = OUT_DIR / "v01-thumbnail-final.png"
img.convert("RGB").save(out, "PNG", optimize=True)
print(f"[OK] V1 thumbnail FINAL: {out}")
print(f"     Size: {out.stat().st_size // 1024}KB")
