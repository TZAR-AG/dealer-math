# Generate AUDM V1 thumbnail (LOCKED V1 — Adrian's chosen design 2026-04-30).
# Layout adapted for MJ background variant _0 (yellow on right):
#   RIGHT (yellow side) — Dollar reveal: $300/WK + arrow + $46,800 MORE + OUT OF YOUR POCKET
#   LEFT  (charcoal)   — Hook: NEVER + ANSWER/THIS/ONE/QUESTION (cream stack)
#   BOTTOM-LEFT corner — AU country badge

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

REPO = Path(r"C:\dev\Claude")
DOWNLOADS = Path.home() / "Downloads"
BG_FILE = DOWNLOADS / "audealermath_YouTube_thumbnail_background_169_aspect_ratio_so_e00e2cd6-b6e9-4288-a9bc-84129a548098_0.png"
OUT_FILE = REPO / "content" / "au-dealer-math" / "scripts" / "v01-thumbnail.png"
OUT_FILE.parent.mkdir(parents=True, exist_ok=True)

# Brand colors (from thumbnail brief)
WHITE = (255, 255, 255, 255)
CREAM = (245, 239, 230, 255)        # #F5EFE6
OUTBACK_ORANGE = (209, 122, 61, 255)  # #D17A3D
CHARCOAL = (43, 43, 43, 255)        # #2B2B2B
YELLOW = (255, 215, 0, 255)         # #FFD700

FONT_DIR = Path("C:/Windows/Fonts")
FONT_IMPACT = FONT_DIR / "impact.ttf"
FONT_ARIAL_BLACK = FONT_DIR / "ariblk.ttf"
FONT_ARIAL_BOLD = FONT_DIR / "arialbd.ttf"


def get_font(size, prefer="impact"):
    if prefer == "impact":
        candidates = [FONT_IMPACT, FONT_ARIAL_BLACK, FONT_ARIAL_BOLD]
    else:
        candidates = [FONT_ARIAL_BLACK, FONT_ARIAL_BOLD, FONT_IMPACT]
    for f in candidates:
        if f.exists():
            return ImageFont.truetype(str(f), size)
    return ImageFont.load_default()


def draw_text_with_shadow(draw, text, position, font, color, shadow_offset=8, stroke_width=4):
    sx, sy = position[0] + shadow_offset, position[1] + shadow_offset
    draw.text((sx, sy), text, font=font, fill=(0, 0, 0, 200), stroke_width=stroke_width, stroke_fill=(0, 0, 0, 200))
    draw.text(position, text, font=font, fill=color, stroke_width=stroke_width, stroke_fill=(0, 0, 0, 255))


# Load + resize MJ background to 1280x720
print(f"Loading MJ background: {BG_FILE.name}")
bg = Image.open(BG_FILE).convert("RGBA").resize((1280, 720), Image.LANCZOS)
img = bg.copy()
draw = ImageDraw.Draw(img)

# ============================================================
# RIGHT HALF (yellow side) — Dollar reveal
# ============================================================

R_LEFT = 670
R_RIGHT = 1250
R_CENTER = (R_LEFT + R_RIGHT) // 2

def center_in_right(tw):
    return R_CENTER - tw // 2

# "$300/WK" — top
text = "$300/WK"
font = get_font(140)
bbox = draw.textbbox((0, 0), text, font=font)
tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
x_300 = center_in_right(tw)
y_300 = 50
draw_text_with_shadow(draw, text, (x_300, y_300), font, WHITE, shadow_offset=6, stroke_width=6)

# Arrow — outback orange, points right
arrow_y = y_300 + th + 25
arrow_left = R_LEFT + 30
arrow_right = R_RIGHT - 30
arrow_height = 32
shaft_top = arrow_y + arrow_height // 4
shaft_bot = arrow_y + 3 * arrow_height // 4
arrow_points = [
    (arrow_left, shaft_top),
    (arrow_right - 50, shaft_top),
    (arrow_right - 50, arrow_y),
    (arrow_right, arrow_y + arrow_height // 2),
    (arrow_right - 50, arrow_y + arrow_height),
    (arrow_right - 50, shaft_bot),
    (arrow_left, shaft_bot),
]
draw.polygon(arrow_points, fill=OUTBACK_ORANGE)

# "$46,800 MORE" — below arrow
text = "$46,800 MORE"
font = get_font(95, prefer="impact")
bbox = draw.textbbox((0, 0), text, font=font)
tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
x = center_in_right(tw)
y_46k = arrow_y + arrow_height + 25
draw_text_with_shadow(draw, text, (x, y_46k), font, WHITE, shadow_offset=5, stroke_width=5)

# "OUT OF YOUR POCKET" — small subtitle
text = "OUT OF YOUR POCKET"
font = get_font(42, prefer="black")
bbox = draw.textbbox((0, 0), text, font=font)
tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
x = center_in_right(tw)
y_ofyp = y_46k + 95 + 15
draw_text_with_shadow(draw, text, (x, y_ofyp), font, CREAM, shadow_offset=3, stroke_width=3)

# ============================================================
# LEFT HALF (charcoal side) — Hook
# ============================================================

# "NEVER" — large, outback orange
text = "NEVER"
font = get_font(150)
bbox = draw.textbbox((0, 0), text, font=font)
tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
y_never = 80
draw_text_with_shadow(draw, text, (50, y_never), font, OUTBACK_ORANGE, shadow_offset=6, stroke_width=6)

# "ANSWER" "THIS" "ONE" "QUESTION" — stacked, cream
font_stack = get_font(90, prefer="black")
y_stack = y_never + th + 20
line_height = 100
for i, line in enumerate(["ANSWER", "THIS", "ONE", "QUESTION"]):
    draw_text_with_shadow(draw, line, (50, y_stack + i * line_height), font_stack, CREAM, shadow_offset=4, stroke_width=4)

# ============================================================
# BOTTOM-LEFT — AU badge
# ============================================================
text = "AU"
font = get_font(36, prefer="black")
bbox = draw.textbbox((0, 0), text, font=font)
tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
draw_text_with_shadow(draw, text, (40, 720 - th - 20), font, CREAM, shadow_offset=3, stroke_width=3)

img.convert("RGB").save(OUT_FILE, "PNG", optimize=True)
print(f"Thumbnail saved: {OUT_FILE}")
print(f"Size: {OUT_FILE.stat().st_size // 1024}KB")
