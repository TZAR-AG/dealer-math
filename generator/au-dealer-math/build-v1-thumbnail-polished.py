"""V1 thumbnail — POLISHED (not redesigned).

Adrian feedback 2026-05-01: "our first thumbnail was better than the ones after,
it just needed to be polished."

Original Template A composition is correct. Polish targets:
- "NEVER" hero word: bigger, tighter, more punch
- Stacked headline: tighter spacing, bigger fonts
- Arrow: hand-drawn marker style (curved, tapered) not generic block
- "$46,800": brightest element — pure cream-yellow, max stroke
- Background: subtle contract-photo texture UNDER the gradient (depth without noise)
- Slight grain for editorial feel

Output: content/au-dealer-math/scripts/v01-thumbnail-polished.png
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageOps
from pathlib import Path
import random

REPO = Path(r"C:\dev\Claude")
OUT_DIR = REPO / "content" / "au-dealer-math" / "scripts"

CHARCOAL = (43, 43, 43)
OUTBACK_ORANGE = (209, 122, 61)
CREAM = (245, 239, 230)
WHITE = (255, 255, 255)
YELLOW = (255, 215, 0)

BACKDROP = REPO / "content" / "au-dealer-math" / "scripts" / "v01-renders" / "stills" / "v2" / "kit-hero-cheatsheet-bg.png"

FONTS_DIR = REPO / "fonts"
DMSANS_BOLD = FONTS_DIR / "DM_Sans" / "DMSans-Bold.ttf"
DMSANS_REGULAR = FONTS_DIR / "DM_Sans" / "DMSans-Regular.ttf"
ARIAL_BLACK = Path("C:/Windows/Fonts/ariblk.ttf")
display_font = ARIAL_BLACK if ARIAL_BLACK.exists() else DMSANS_BOLD

W, H = 1280, 720


def font(path, size):
    return ImageFont.truetype(str(path), size)


def measure(draw, text, f):
    bb = draw.textbbox((0, 0), text, font=f)
    return bb[2] - bb[0], bb[3] - bb[1]


def fit_text(draw, text, max_w, max_h, font_path, start_size=200, min_size=40):
    size = start_size
    while size > min_size:
        f = font(font_path, size)
        w, h = measure(draw, text, f)
        if w <= max_w and h <= max_h:
            return f, w, h
        size -= 4
    f = font(font_path, min_size)
    return f, *measure(draw, text, f)


def draw_text_punch(draw, position, text, f, fill, stroke_w=6, stroke_fill=(0, 0, 0), shadow=8):
    """Stroke + shadow for max readability."""
    sx, sy = position[0] + shadow, position[1] + shadow
    draw.text((sx, sy), text, font=f, fill=(0, 0, 0, 200),
              stroke_width=stroke_w, stroke_fill=(0, 0, 0, 200))
    draw.text(position, text, font=f, fill=fill,
              stroke_width=stroke_w, stroke_fill=stroke_fill)


def draw_marker_arrow(draw, x1, y, x2, color, thickness=20, head_length=55):
    """Hand-drawn-style tapered marker arrow.
    Slight curve at start + head, organic feel vs generic block.
    """
    # Slight downward curve mid-shaft, upward at end (organic marker stroke)
    mid_x = (x1 + x2 - head_length) / 2
    points = []
    # Build a tapered polygon for the shaft (thinner at start, fatter mid)
    seg_count = 20
    for i in range(seg_count + 1):
        t = i / seg_count
        x = x1 + t * (x2 - head_length - x1)
        # Slight wobble
        wobble = -2 if i % 2 == 0 else 2
        # Taper thickness — narrower at start, fatter mid, narrower near head
        taper = 1 - 0.5 * abs(t - 0.5) * 2
        h = int(thickness * (0.6 + 0.4 * taper))
        if i == 0:
            top_pts_left = (x, y - h // 2 + wobble)
            bot_pts_left = (x, y + h // 2 + wobble)
            top_pts = [top_pts_left]
            bot_pts = [bot_pts_left]
        else:
            top_pts.append((x, y - h // 2 + wobble))
            bot_pts.append((x, y + h // 2 + wobble))

    # Build polygon: top points left-to-right, then bottom points right-to-left
    poly = top_pts + list(reversed(bot_pts))
    draw.polygon(poly, fill=color)

    # Arrow head — chunky, slightly tilted
    head_tip_x = x2
    head_tip_y = y
    head_back_x = x2 - head_length
    head_top = (head_back_x, y - thickness * 1.4)
    head_bot = (head_back_x, y + thickness * 1.4)
    draw.polygon([(head_tip_x, head_tip_y), head_top, head_bot], fill=color)


# ============================================================
# Step 1: Backdrop layer — subtle contract texture, heavily darkened
# ============================================================
if BACKDROP.exists():
    bg = Image.open(BACKDROP).convert("RGB")
    bg = ImageOps.fit(bg, (W, H), Image.LANCZOS, centering=(0.5, 0.6))
    # Heavy darken — texture only, not subject
    bg = ImageEnhance.Brightness(bg).enhance(0.18)
    bg = bg.filter(ImageFilter.GaussianBlur(radius=8))
    img = bg.convert("RGBA")
else:
    img = Image.new("RGBA", (W, H), CHARCOAL + (255,))

# Step 2: Charcoal base layer over photo (60% opacity — keeps texture visible but mutes it)
base = Image.new("RGBA", (W, H), CHARCOAL + (180,))
img = Image.alpha_composite(img, base)

# Step 3: Left-half deeper darken for headline legibility (gradient)
left_overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
lo = ImageDraw.Draw(left_overlay)
for x in range(W):
    # Strongest darken on left third, fading to right
    alpha = int(180 * max(0, 1 - x / (W * 0.55)) ** 1.3)
    lo.line([(x, 0), (x, H)], fill=(43, 43, 43, alpha))
img = Image.alpha_composite(img, left_overlay)

# Step 4: Subtle radial glow in bottom-right (warmth)
glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
gd = ImageDraw.Draw(glow)
gd.ellipse([W * 0.55, H * 0.4, W * 1.1, H * 1.2],
           fill=(*OUTBACK_ORANGE, 30))
glow = glow.filter(ImageFilter.GaussianBlur(radius=200))
img = Image.alpha_composite(img, glow)

draw = ImageDraw.Draw(img)

# ============================================================
# LEFT — stacked headline
# Hero word "NEVER" in outback orange (bigger, tighter)
# Then "ANSWER / THIS / ONE / QUESTION" stacked in cream
# ============================================================
LEFT_PADDING = 50
LEFT_WIDTH = 540

# Hero "NEVER" — biggest, orange
hero_size = 200
hero_f = font(display_font, hero_size)
hero_w, hero_h = measure(draw, "NEVER", hero_f)
while hero_w > LEFT_WIDTH and hero_size > 100:
    hero_size -= 5
    hero_f = font(display_font, hero_size)
    hero_w, hero_h = measure(draw, "NEVER", hero_f)

y_cursor = 50
draw_text_punch(draw, (LEFT_PADDING, y_cursor), "NEVER", hero_f,
                OUTBACK_ORANGE, stroke_w=7, shadow=8)
y_cursor += hero_h - 10  # slight overlap for tighter feel

# Stacked words below in cream — slightly smaller, tight line height
stack_words = ["ANSWER", "THIS", "ONE", "QUESTION"]
stack_size = 96
stack_f = font(display_font, stack_size)
# Find max width to ensure all fit
biggest = max(stack_words, key=len)
biggest_w, biggest_h = measure(draw, biggest, stack_f)
while biggest_w > LEFT_WIDTH and stack_size > 60:
    stack_size -= 4
    stack_f = font(display_font, stack_size)
    biggest_w, biggest_h = measure(draw, biggest, stack_f)

line_height = int(biggest_h * 0.95)  # tight
for word in stack_words:
    draw_text_punch(draw, (LEFT_PADDING, y_cursor), word, stack_f,
                    CREAM, stroke_w=5, shadow=6)
    y_cursor += line_height

# ============================================================
# RIGHT — dollar reveal
# "$300/WK" → big arrow → "$46,800 MORE" (yellow) → "OUT OF YOUR POCKET"
# ============================================================
R_LEFT = W // 2 + 20
R_RIGHT = W - 50
R_CENTER = (R_LEFT + R_RIGHT) // 2

def centre_r(tw):
    return R_CENTER - tw // 2

# "$300/WK" big cream
d1_f, d1_w, d1_h = fit_text(draw, "$300/WK", R_RIGHT - R_LEFT, 200, display_font, start_size=180)
d1_y = 70
draw_text_punch(draw, (centre_r(d1_w), d1_y), "$300/WK", d1_f,
                CREAM, stroke_w=6, shadow=8)

# Tapered marker arrow
arrow_y = d1_y + d1_h + 50
draw_marker_arrow(draw, R_LEFT + 20, arrow_y, R_RIGHT - 20, OUTBACK_ORANGE,
                  thickness=26, head_length=60)

# "$46,800 MORE" — biggest, brightest (yellow with thicker stroke)
d2_y = arrow_y + 60
d2_f, d2_w, d2_h = fit_text(draw, "$46,800 MORE", R_RIGHT - R_LEFT, 180,
                            display_font, start_size=140)
draw_text_punch(draw, (centre_r(d2_w), d2_y), "$46,800 MORE", d2_f,
                YELLOW, stroke_w=7, shadow=9)

# Subtitle "OUT OF YOUR POCKET" — small cream
sub_f, sub_w, sub_h = fit_text(draw, "OUT OF YOUR POCKET", R_RIGHT - R_LEFT, 60,
                               display_font, start_size=58)
sub_y = d2_y + d2_h + 20
draw_text_punch(draw, (centre_r(sub_w), sub_y), "OUT OF YOUR POCKET", sub_f,
                CREAM, stroke_w=3, shadow=5)

# ============================================================
# AU pill bottom-left
# ============================================================
au_f = font(display_font, 38)
au_w, au_h = measure(draw, "AU", au_f)
pill_pad_x, pill_pad_y = 14, 10
pill_x, pill_y = 30, H - 30 - au_h - pill_pad_y * 2
draw.rounded_rectangle(
    [pill_x, pill_y, pill_x + au_w + pill_pad_x * 2, pill_y + au_h + pill_pad_y * 2],
    radius=10, fill=OUTBACK_ORANGE)
draw.text((pill_x + pill_pad_x, pill_y + pill_pad_y - 4), "AU",
          font=au_f, fill=CHARCOAL)

# ============================================================
# Subtle film grain overlay — adds editorial polish, kills the digital flatness
# ============================================================
random.seed(42)
grain = Image.new("RGBA", (W, H), (0, 0, 0, 0))
gd = ImageDraw.Draw(grain)
for _ in range(W * H // 80):
    x = random.randint(0, W - 1)
    y = random.randint(0, H - 1)
    val = random.randint(0, 30)
    gd.point((x, y), fill=(255, 255, 255, val))
img = Image.alpha_composite(img, grain)

# ============================================================
# Save
# ============================================================
out = OUT_DIR / "v01-thumbnail-polished.png"
img.convert("RGB").save(out, "PNG", optimize=True)
print(f"[OK] Polished thumbnail: {out}")
print(f"     Size: {out.stat().st_size // 1024}KB")
