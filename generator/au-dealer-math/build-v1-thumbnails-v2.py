"""V1 thumbnail v2 — three world-class variants for YouTube A/B test.

Three different visual story angles, all using the same brand palette and the
kit-hero-cheatsheet contract photo as backdrop. YouTube Studio native A/B test
will pick the CTR winner across the first ~24h of impressions.

Variants:
  A — "DON'T SAY THIS" — quote with red strikethrough + $46,800 reveal
  B — "$46,800 MORE"   — big-number-dominant, contract bg, minimal text
  C — "1 QUESTION = $46K" — equation storytelling, clean math layout

Output: content/au-dealer-math/scripts/v01-thumbnail-v2-{a,b,c}.png

Run: python generator/au-dealer-math/build-v1-thumbnails-v2.py
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
from pathlib import Path

REPO = Path(r"C:\dev\Claude")
OUT_DIR = REPO / "content" / "au-dealer-math" / "scripts"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Brand palette LOCKED
CHARCOAL = (43, 43, 43)
OUTBACK_ORANGE = (209, 122, 61)
CREAM = (245, 239, 230)
WHITE = (255, 255, 255)
RED = (220, 50, 50)
YELLOW = (255, 215, 0)

# Backdrop — same contract photo we use everywhere (cross-surface brand consistency)
BACKDROP = REPO / "content" / "au-dealer-math" / "scripts" / "v01-renders" / "stills" / "v2" / "kit-hero-cheatsheet-bg.png"

# Fonts
FONTS_DIR = REPO / "fonts"
DMSANS_BOLD = FONTS_DIR / "DM_Sans" / "DMSans-Bold.ttf"
INTER_BOLD = FONTS_DIR / "Inter" / "Inter-Bold.ttf"  # may not exist, fallback
ARIAL_BLACK = Path("C:/Windows/Fonts/ariblk.ttf")
IMPACT = Path("C:/Windows/Fonts/impact.ttf")
display_font_path = ARIAL_BLACK if ARIAL_BLACK.exists() else DMSANS_BOLD

W, H = 1280, 720


def font(path, size):
    return ImageFont.truetype(str(path), size)


def measure(draw, text, f):
    bb = draw.textbbox((0, 0), text, font=f)
    return bb[2] - bb[0], bb[3] - bb[1]


def load_backdrop(darken_factor=0.40, blur_radius=2):
    """Load contract bg, cover-fit to 1280x720, darken, slight blur."""
    img = Image.open(BACKDROP).convert("RGB")
    # Cover-fit
    src_w, src_h = img.size
    target_aspect = W / H
    src_aspect = src_w / src_h
    if src_aspect > target_aspect:
        new_w = int(src_h * target_aspect)
        offset = (src_w - new_w) // 2
        img = img.crop((offset, 0, offset + new_w, src_h))
    else:
        new_h = int(src_w / target_aspect)
        offset = (src_h - new_h) // 2
        img = img.crop((0, offset, src_w, offset + new_h))
    img = img.resize((W, H), Image.LANCZOS)
    # Darken
    img = ImageEnhance.Brightness(img).enhance(darken_factor)
    # Slight blur for depth
    if blur_radius:
        img = img.filter(ImageFilter.GaussianBlur(radius=blur_radius))
    return img.convert("RGBA")


def draw_text_punch(draw, position, text, f, fill, stroke_w=8, stroke_fill=(0, 0, 0), shadow=10):
    """Heavy stroke + drop shadow for max readability over photo bg."""
    sx, sy = position[0] + shadow, position[1] + shadow
    draw.text((sx, sy), text, font=f, fill=(0, 0, 0, 220),
              stroke_width=stroke_w, stroke_fill=(0, 0, 0, 220))
    draw.text(position, text, font=f, fill=fill,
              stroke_width=stroke_w, stroke_fill=stroke_fill)


def draw_marker_strike(draw, x1, y1, x2, y2, color=RED, thickness=18):
    """Hand-drawn-style red marker strikethrough — slightly tilted, organic."""
    # Multiple slightly-offset strokes for marker pen feel
    for dy in range(-3, 4):
        draw.line([(x1, y1 + dy), (x2, y2 + dy)], fill=color + (200,) if len(color) == 3 else color, width=thickness - abs(dy))


def draw_arrow_curved(draw, points, color, thickness=14):
    """Curved arrow path through given points — feels less mechanical."""
    for i in range(len(points) - 1):
        draw.line([points[i], points[i + 1]], fill=color, width=thickness)


def draw_au_badge(draw, x, y):
    """Small AU stamp."""
    bf = font(display_font_path, 32)
    bbox = draw.textbbox((0, 0), "AU", font=bf)
    bw, bh = bbox[2] - bbox[0], bbox[3] - bbox[1]
    pad = 10
    draw.rounded_rectangle(
        [x, y, x + bw + pad * 2, y + bh + pad * 2],
        radius=8, fill=OUTBACK_ORANGE)
    draw.text((x + pad, y + pad - 4), "AU", font=bf, fill=CHARCOAL)


# ============================================================
# VARIANT A — "DON'T SAY THIS" (strikethrough on quote)
# Tells the V1 story in one image: this question = $46K loss
# ============================================================
def variant_a():
    img = load_backdrop(darken_factor=0.35, blur_radius=2)
    # Side gradient overlay (left dark for text)
    overlay = Image.new("RGBA", (W, H), (43, 43, 43, 0))
    od = ImageDraw.Draw(overlay)
    for x in range(W):
        alpha = int(180 * (1 - x / W) ** 1.5)
        od.line([(x, 0), (x, H)], fill=(43, 43, 43, alpha))
    img = Image.alpha_composite(img, overlay)
    draw = ImageDraw.Draw(img)

    # Top: "What's your weekly budget?" in italic-ish quote style
    q_font = font(display_font_path, 60)
    q_text = '"What\'s your weekly budget?"'
    qw, qh = measure(draw, q_text, q_font)
    qx = 50
    qy = 140
    draw_text_punch(draw, (qx, qy), q_text, q_font, CREAM, stroke_w=4, shadow=6)

    # RED MARKER STRIKETHROUGH across the question
    strike_y = qy + qh // 2 + 8
    for dy in range(-4, 5):
        draw.line([(qx - 10, strike_y + dy), (qx + qw + 20, strike_y + dy + 5)],
                  fill=RED, width=15)

    # BIG "= $46,800" reveal below
    eq_font = font(display_font_path, 200)
    eq_text = "= $46,800"
    ew, eh = measure(draw, eq_text, eq_font)
    if ew > W - 100:
        eq_font = font(display_font_path, int(200 * (W - 100) / ew))
        ew, eh = measure(draw, eq_text, eq_font)
    ex = (W - ew) // 2
    ey = qy + qh + 60
    draw_text_punch(draw, (ex, ey), eq_text, eq_font, YELLOW, stroke_w=8, shadow=10)

    # Subtitle
    sub_font = font(display_font_path, 56)
    sub_text = "OUT OF YOUR POCKET"
    sw, sh = measure(draw, sub_text, sub_font)
    sx = (W - sw) // 2
    sy = ey + eh + 20
    draw_text_punch(draw, (sx, sy), sub_text, sub_font, OUTBACK_ORANGE, stroke_w=4, shadow=6)

    draw_au_badge(draw, 30, H - 80)

    out = OUT_DIR / "v01-thumbnail-v2-a.png"
    img.convert("RGB").save(out, "PNG", optimize=True)
    return out


# ============================================================
# VARIANT B — "$46,800 MORE" big-number-dominant
# Cleanest, most punch — number IS the thumbnail
# ============================================================
def variant_b():
    img = load_backdrop(darken_factor=0.30, blur_radius=3)
    # Vignette
    vignette = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    vd = ImageDraw.Draw(vignette)
    for r in range(0, 300, 4):
        alpha = int(150 * (r / 300) ** 2)
        vd.rectangle([r, r, W - r, H - r], outline=(0, 0, 0, alpha), width=4)
    vignette = vignette.filter(ImageFilter.GaussianBlur(radius=40))
    img = Image.alpha_composite(img, vignette)
    draw = ImageDraw.Draw(img)

    # Top tag: "ASK A DEALER" small
    tag_font = font(display_font_path, 52)
    tag_text = "WHEN A DEALER ASKS:"
    tw, th = measure(draw, tag_text, tag_font)
    draw_text_punch(draw, ((W - tw) // 2, 60), tag_text, tag_font, CREAM, stroke_w=3, shadow=5)

    # Massive dollar number
    num_font = font(display_font_path, 320)
    num_text = "$46,800"
    nw, nh = measure(draw, num_text, num_font)
    if nw > W - 80:
        num_font = font(display_font_path, int(320 * (W - 80) / nw))
        nw, nh = measure(draw, num_text, num_font)
    nx = (W - nw) // 2
    ny = 180
    draw_text_punch(draw, (nx, ny), num_text, num_font, YELLOW, stroke_w=10, shadow=12)

    # Orange highlight stroke under the number (brand motif)
    stroke_y = ny + nh - 40
    stroke_h = 24
    draw.rectangle([nx + 20, stroke_y, nx + nw - 20, stroke_y + stroke_h],
                   fill=OUTBACK_ORANGE)

    # Subtitle
    sub_font = font(display_font_path, 80)
    sub_text = "MORE OUT OF YOUR POCKET"
    sw, sh = measure(draw, sub_text, sub_font)
    if sw > W - 80:
        sub_font = font(display_font_path, int(80 * (W - 80) / sw))
        sw, sh = measure(draw, sub_text, sub_font)
    draw_text_punch(draw, ((W - sw) // 2, ny + nh + 50), sub_text, sub_font, CREAM, stroke_w=5, shadow=6)

    draw_au_badge(draw, 30, H - 80)

    out = OUT_DIR / "v01-thumbnail-v2-b.png"
    img.convert("RGB").save(out, "PNG", optimize=True)
    return out


# ============================================================
# VARIANT C — "1 QUESTION = $46K" equation storytelling
# Simplest, most curiosity-gap (what's the question?)
# ============================================================
def variant_c():
    img = load_backdrop(darken_factor=0.32, blur_radius=2)
    # Diagonal split overlay (left dark, right slightly lighter for visual contrast)
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    for x in range(W):
        # Left half darker, right slightly lighter
        alpha = int(140 * (1 - abs(x - W // 2) / (W // 2)))
        od.line([(x, 0), (x, H)], fill=(43, 43, 43, alpha))
    img = Image.alpha_composite(img, overlay)
    draw = ImageDraw.Draw(img)

    # LEFT side: big "1" with caption
    one_font = font(display_font_path, 360)
    one_text = "1"
    ow, oh = measure(draw, one_text, one_font)
    ox = 80
    oy = (H - oh) // 2 - 30
    draw_text_punch(draw, (ox, oy), one_text, one_font, CREAM, stroke_w=10, shadow=12)

    # Caption under "1"
    cap_font = font(display_font_path, 64)
    cap_text = "QUESTION"
    cw, ch = measure(draw, cap_text, cap_font)
    cx = ox + (ow - cw) // 2
    cy = oy + oh - 30
    draw_text_punch(draw, (cx, cy), cap_text, cap_font, OUTBACK_ORANGE, stroke_w=4, shadow=6)

    # CENTER: equals sign
    eq_font = font(display_font_path, 220)
    eq_text = "="
    eqw, eqh = measure(draw, eq_text, eq_font)
    eqx = ox + ow + 50
    eqy = (H - eqh) // 2
    draw_text_punch(draw, (eqx, eqy), eq_text, eq_font, OUTBACK_ORANGE, stroke_w=8, shadow=10)

    # RIGHT side: big "$46K" with caption
    dollar_font = font(display_font_path, 240)
    dollar_text = "$46K"
    dw, dh = measure(draw, dollar_text, dollar_font)
    dx = eqx + eqw + 50
    if dx + dw > W - 50:
        # Refit
        dollar_font = font(display_font_path, int(240 * (W - 50 - dx) / dw))
        dw, dh = measure(draw, dollar_text, dollar_font)
    dy = (H - dh) // 2 - 30
    draw_text_punch(draw, (dx, dy), dollar_text, dollar_font, YELLOW, stroke_w=10, shadow=12)

    # Caption under $46K
    lcap_font = font(display_font_path, 48)
    lcap_text = "GONE"
    lcw, lch = measure(draw, lcap_text, lcap_font)
    lcx = dx + (dw - lcw) // 2
    lcy = dy + dh - 30
    draw_text_punch(draw, (lcx, lcy), lcap_text, lcap_font, RED, stroke_w=4, shadow=6)

    # Top headline
    h_font = font(display_font_path, 48)
    h_text = "WHAT THE DEALER ASKS FIRST:"
    hw_, hh_ = measure(draw, h_text, h_font)
    draw_text_punch(draw, ((W - hw_) // 2, 50), h_text, h_font, CREAM, stroke_w=3, shadow=5)

    draw_au_badge(draw, 30, H - 80)

    out = OUT_DIR / "v01-thumbnail-v2-c.png"
    img.convert("RGB").save(out, "PNG", optimize=True)
    return out


# ============================================================
# Build all 3 variants + a side-by-side compare
# ============================================================
print("Building V1 thumbnail v2 — 3 variants for A/B test...")
a_path = variant_a()
print(f"  [A] DON'T-SAY-THIS strikethrough:  {a_path.name}  ({a_path.stat().st_size // 1024}KB)")
b_path = variant_b()
print(f"  [B] $46,800 big-number dominant:    {b_path.name}  ({b_path.stat().st_size // 1024}KB)")
c_path = variant_c()
print(f"  [C] 1 QUESTION = $46K equation:     {c_path.name}  ({c_path.stat().st_size // 1024}KB)")

# Compare image — 3 variants stacked vertically with labels
COMPARE_W = 1280
COMPARE_H = 720 * 3 + 80 * 3
compare = Image.new("RGB", (COMPARE_W, COMPARE_H), CHARCOAL)
cd = ImageDraw.Draw(compare)
labels = [
    ("A  —  Don't say this  +  $46,800 strikethrough reveal", a_path),
    ("B  —  $46,800 big-number dominant", b_path),
    ("C  —  1 question = $46K equation", c_path),
]
y = 0
label_font = font(display_font_path, 36)
for label, path in labels:
    cd.text((30, y + 20), label, font=label_font, fill=CREAM)
    img = Image.open(path).convert("RGB")
    compare.paste(img, (0, y + 80))
    y += 720 + 80

compare_path = OUT_DIR / "v01-thumbnail-v2-compare.png"
compare.save(compare_path, "PNG", optimize=True)
print(f"\nCompare image: {compare_path.name}  ({compare_path.stat().st_size // 1024}KB)")
