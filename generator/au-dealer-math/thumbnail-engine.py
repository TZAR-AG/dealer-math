"""AU Dealer Math thumbnail engine — locked V2+ playbook.

Three reusable templates (research-backed for AU finance/automotive faceless):
  Template A — Big-Number Reveal:  dollar figure + 1-line headline, MJ backdrop
  Template B — Comparison Split:    two-panel "what dealer says" vs "what's true"
  Template C — Document Forensics:  zoomed contract clause + red highlight + arrow

Each template takes a config dict and produces a 1280x720 PNG. Designed to be
called via per-video script that supplies (mj_image, headline, dollar_figure,
template).

Usage example:
    from thumbnail_engine import render_thumbnail
    render_thumbnail(
        out_path="content/au-dealer-math/scripts/v02-thumbnail.png",
        template="A",
        mj_background="C:/Users/adria/Downloads/audealermath_v2_mj_0.png",
        headline_left="THE TRADE-IN\\nLOWBALL TRICK",
        dollar_right="$3,500\\nLOST",
        subtitle="OUT OF YOUR\\nPOCKET",
    )

Critical rules (research 2026):
  - Max 4-6 words on screen (7+ underperforms in the niche)
  - 2-3 brand colours only (charcoal + cream + outback orange + accent yellow)
  - AU finance niche: NO all-caps screaming, calmer authority style
  - YouTube Studio A/B test: produce 3 variants per video (A1, A2, B1 or A1, B1, C1)
"""

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

REPO = Path(r"C:\dev\Claude")

# Brand palette LOCKED
WHITE = (255, 255, 255, 255)
CREAM = (245, 239, 230, 255)
OUTBACK_ORANGE = (209, 122, 61, 255)
CHARCOAL = (43, 43, 43, 255)
YELLOW_ACCENT = (255, 215, 0, 255)
RED_HIGHLIGHT = (220, 50, 50, 255)

# Fonts
FONTS_DIR = REPO / "fonts"
DMSANS_BOLD = FONTS_DIR / "DM_Sans" / "DMSans-Bold.ttf"
INTER_REGULAR = FONTS_DIR / "Inter" / "Inter-Regular.ttf"
ARIAL_BLACK = Path("C:/Windows/Fonts/ariblk.ttf")
IMPACT = Path("C:/Windows/Fonts/impact.ttf")
display_font_path = ARIAL_BLACK if ARIAL_BLACK.exists() else DMSANS_BOLD

W, H = 1280, 720


def load_font(path, size):
    return ImageFont.truetype(str(path), size)


def measure(draw, text, f):
    bb = draw.textbbox((0, 0), text, font=f)
    return bb[2] - bb[0], bb[3] - bb[1]


def fit_text(draw, text, max_w, max_h, font_path, start_size=200, min_size=40):
    size = start_size
    while size > min_size:
        f = load_font(font_path, size)
        w, h = measure(draw, text, f)
        if w <= max_w and h <= max_h:
            return f, w, h
        size -= 6
    f = load_font(font_path, min_size)
    return f, *measure(draw, text, f)


def draw_text_with_stroke(draw, position, text, font, fill, stroke_w=4,
                          stroke_fill=(0, 0, 0, 255), shadow_offset=6):
    """Heavy stroke + shadow for max readability against any background."""
    sx, sy = position[0] + shadow_offset, position[1] + shadow_offset
    draw.text((sx, sy), text, font=font, fill=(0, 0, 0, 200),
              stroke_width=stroke_w, stroke_fill=(0, 0, 0, 200))
    draw.text(position, text, font=font, fill=fill,
              stroke_width=stroke_w, stroke_fill=stroke_fill)


def draw_arrow(draw, x1, y, x2, color, thickness=22, head_length=40):
    """Draw a chunky right-pointing arrow from (x1,y) to (x2,y)."""
    shaft_top = y - thickness // 2
    shaft_bot = y + thickness // 2
    shaft_end = x2 - head_length
    points = [
        (x1, shaft_top),
        (shaft_end, shaft_top),
        (shaft_end, y - thickness),
        (x2, y),
        (shaft_end, y + thickness),
        (shaft_end, shaft_bot),
        (x1, shaft_bot),
    ]
    draw.polygon(points, fill=color)


# ============================================================
# TEMPLATE A — Big-Number Reveal
# Layout:
#   LEFT 50%  — Hook headline (NEVER / ANSWER / THIS / ONE / QUESTION style)
#   RIGHT 50% — Dollar figure ($300/WK → $46,800 MORE) over MJ background
# ============================================================
def template_a_big_number(out_path, mj_background, headline_lines, dollar_main,
                          dollar_arrow_to=None, dollar_subtitle=None,
                          au_badge=True):
    """
    headline_lines: list of strings, drawn stacked on left. e.g. ["NEVER","ANSWER","THIS","ONE","QUESTION"]
    dollar_main:    primary dollar reveal, e.g. "$300/WK"
    dollar_arrow_to: optional second figure after arrow, e.g. "$46,800 MORE"
    dollar_subtitle: optional small sub, e.g. "OUT OF YOUR POCKET"
    """
    bg = Image.open(mj_background).convert("RGBA").resize((W, H), Image.LANCZOS)
    img = bg.copy()
    draw = ImageDraw.Draw(img)

    # Optional charcoal gradient overlay on left half for headline legibility
    overlay = Image.new("RGBA", (W // 2, H), (43, 43, 43, 180))
    img.paste(overlay, (0, 0), overlay)
    draw = ImageDraw.Draw(img)

    # LEFT — headline stacked
    line_count = len(headline_lines)
    # Auto-fit largest line to ~520px width and target line height
    max_line_w = 540
    max_line_h = (H - 80) // (line_count + 1)
    biggest = max(headline_lines, key=len)
    f, _, _ = fit_text(draw, biggest, max_line_w, max_line_h, display_font_path, start_size=160)

    # First line bigger as a "hero" word (often "NEVER")
    hero_f, _, _ = fit_text(draw, headline_lines[0], max_line_w, int(max_line_h * 1.3),
                            display_font_path, start_size=180)
    line_height = int(max_line_h)
    y_cursor = 60

    # Hero line in outback orange
    draw_text_with_stroke(draw, (50, y_cursor), headline_lines[0], hero_f,
                          OUTBACK_ORANGE, stroke_w=6, shadow_offset=6)
    _, hero_h = measure(draw, headline_lines[0], hero_f)
    y_cursor += hero_h + 20

    # Remaining lines in cream
    for line in headline_lines[1:]:
        draw_text_with_stroke(draw, (50, y_cursor), line, f, CREAM,
                              stroke_w=4, shadow_offset=4)
        y_cursor += line_height

    # RIGHT — dollar reveal
    R_LEFT, R_RIGHT = W // 2 + 30, W - 50
    R_CENTER = (R_LEFT + R_RIGHT) // 2

    def centre_in_right(tw):
        return R_CENTER - tw // 2

    df, dw, dh = fit_text(draw, dollar_main, R_RIGHT - R_LEFT, 200,
                          display_font_path, start_size=170)
    dy = 60
    draw_text_with_stroke(draw, (centre_in_right(dw), dy), dollar_main, df,
                          WHITE, stroke_w=6, shadow_offset=6)

    if dollar_arrow_to:
        # Arrow
        ay = dy + dh + 35
        draw_arrow(draw, R_LEFT + 20, ay + 10, R_RIGHT - 20, OUTBACK_ORANGE,
                   thickness=28, head_length=50)
        ay += 70

        # Arrow target dollar (often bigger / more dramatic)
        af, aw, ah = fit_text(draw, dollar_arrow_to, R_RIGHT - R_LEFT, 140,
                              display_font_path, start_size=110)
        draw_text_with_stroke(draw, (centre_in_right(aw), ay), dollar_arrow_to,
                              af, YELLOW_ACCENT, stroke_w=5, shadow_offset=5)
        sub_y = ay + ah + 20

        if dollar_subtitle:
            sf, sw, sh = fit_text(draw, dollar_subtitle, R_RIGHT - R_LEFT, 60,
                                  display_font_path, start_size=50)
            draw_text_with_stroke(draw, (centre_in_right(sw), sub_y),
                                  dollar_subtitle, sf, CREAM,
                                  stroke_w=3, shadow_offset=3)

    # AU badge bottom-left
    if au_badge:
        bf = load_font(display_font_path, 36)
        bbox = draw.textbbox((0, 0), "AU", font=bf)
        bw, bh = bbox[2] - bbox[0], bbox[3] - bbox[1]
        # Orange pill
        pad = 12
        pill_h = bh + pad * 2
        draw.rounded_rectangle(
            [30, H - pill_h - 30, 30 + bw + pad * 2, H - 30],
            radius=12, fill=OUTBACK_ORANGE)
        draw.text((30 + pad, H - pill_h - 30 + pad - 4), "AU",
                  font=bf, fill=CHARCOAL)

    img.convert("RGB").save(out_path, "PNG", optimize=True)
    return out_path


# ============================================================
# TEMPLATE B — Comparison Split
# Layout:
#   LEFT 50%  — "WHAT DEALER SAYS" with quote/dollar
#   RIGHT 50% — "WHAT'S TRUE" with reveal/dollar
#   Centre: vertical divider + chevron arrow pointing right
# ============================================================
def template_b_comparison(out_path, mj_background, left_label, left_value,
                          right_label, right_value, au_badge=True):
    """
    left_label:  e.g. "WHAT THEY SAY"
    left_value:  e.g. "$300/WK"
    right_label: e.g. "WHAT IT COSTS"
    right_value: e.g. "$109,200"
    """
    bg = Image.open(mj_background).convert("RGBA").resize((W, H), Image.LANCZOS)
    # Heavy darkening overlay (this template needs both panels readable)
    overlay = Image.new("RGBA", (W, H), (43, 43, 43, 200))
    img = Image.alpha_composite(bg, overlay)
    draw = ImageDraw.Draw(img)

    PANEL_W = W // 2

    # Left panel
    L_CX = PANEL_W // 2
    lf, lw, lh = fit_text(draw, left_label, PANEL_W - 60, 80,
                          display_font_path, start_size=60)
    draw_text_with_stroke(draw, (L_CX - lw // 2, 80), left_label, lf,
                          CREAM, stroke_w=3, shadow_offset=4)

    lvf, lvw, lvh = fit_text(draw, left_value, PANEL_W - 60, 280,
                             display_font_path, start_size=200)
    draw_text_with_stroke(draw, (L_CX - lvw // 2, H // 2 - lvh // 2 + 20),
                          left_value, lvf, WHITE, stroke_w=6, shadow_offset=6)

    # Right panel
    R_CX = PANEL_W + PANEL_W // 2
    rf, rw, rh = fit_text(draw, right_label, PANEL_W - 60, 80,
                          display_font_path, start_size=60)
    draw_text_with_stroke(draw, (R_CX - rw // 2, 80), right_label, rf,
                          OUTBACK_ORANGE, stroke_w=3, shadow_offset=4)

    rvf, rvw, rvh = fit_text(draw, right_value, PANEL_W - 60, 280,
                             display_font_path, start_size=200)
    draw_text_with_stroke(draw, (R_CX - rvw // 2, H // 2 - rvh // 2 + 20),
                          right_value, rvf, YELLOW_ACCENT, stroke_w=6, shadow_offset=6)

    # Chevron arrow at centre
    chev_size = 70
    cx, cy = W // 2, H // 2 + 20
    chev_points = [
        (cx - chev_size // 2, cy - chev_size),
        (cx + chev_size // 2, cy),
        (cx - chev_size // 2, cy + chev_size),
    ]
    draw.polygon(chev_points, fill=OUTBACK_ORANGE)

    # AU badge
    if au_badge:
        bf = load_font(display_font_path, 36)
        bbox = draw.textbbox((0, 0), "AU", font=bf)
        bw, bh = bbox[2] - bbox[0], bbox[3] - bbox[1]
        pad = 12
        pill_h = bh + pad * 2
        draw.rounded_rectangle(
            [30, H - pill_h - 30, 30 + bw + pad * 2, H - 30],
            radius=12, fill=OUTBACK_ORANGE)
        draw.text((30 + pad, H - pill_h - 30 + pad - 4), "AU",
                  font=bf, fill=CHARCOAL)

    img.convert("RGB").save(out_path, "PNG", optimize=True)
    return out_path


# ============================================================
# TEMPLATE C — Document Forensics
# Layout:
#   FULL FRAME — MJ contract/document close-up
#   Red highlight rectangle over a "clause" area
#   Right side: callout text + dollar figure
#   Macca-style stamp/badge: "WATCH OUT" or similar
# ============================================================
def template_c_document_forensics(out_path, mj_background, callout_top,
                                  callout_value, callout_subtitle=None,
                                  highlight_box=None, au_badge=True):
    """
    callout_top:      headline at top-right, e.g. "HIDDEN CLAUSE"
    callout_value:    big dollar reveal, e.g. "$3,500"
    callout_subtitle: optional sub, e.g. "PER CAR"
    highlight_box:    optional (x,y,w,h) tuple for the red highlight rectangle
    """
    bg = Image.open(mj_background).convert("RGBA").resize((W, H), Image.LANCZOS)
    img = bg.copy()

    # Dark gradient overlay on the right 45% for callout legibility
    overlay = Image.new("RGBA", (W * 45 // 100, H), (43, 43, 43, 195))
    img.paste(overlay, (W - W * 45 // 100, 0), overlay)
    draw = ImageDraw.Draw(img)

    # Red highlight on a clause area (caller-supplied or default centre-left)
    if highlight_box:
        hx, hy, hw, hh = highlight_box
    else:
        hx, hy, hw, hh = 60, H // 2 - 50, 480, 100
    hl = Image.new("RGBA", (hw, hh), (220, 50, 50, 90))
    img.paste(hl, (hx, hy), hl)
    # Red border
    draw = ImageDraw.Draw(img)
    border_thickness = 6
    for i in range(border_thickness):
        draw.rectangle([hx - i, hy - i, hx + hw + i, hy + hh + i],
                       outline=RED_HIGHLIGHT, width=1)

    # Right callout panel
    R_LEFT = W * 55 // 100
    R_RIGHT = W - 40
    R_CX = (R_LEFT + R_RIGHT) // 2

    def centre_r(tw):
        return R_CX - tw // 2

    # Top label
    tf, tw, th = fit_text(draw, callout_top, R_RIGHT - R_LEFT, 80,
                          display_font_path, start_size=70)
    ty = 80
    draw_text_with_stroke(draw, (centre_r(tw), ty), callout_top, tf,
                          OUTBACK_ORANGE, stroke_w=4, shadow_offset=5)

    # Big value
    vf, vw, vh = fit_text(draw, callout_value, R_RIGHT - R_LEFT, 240,
                          display_font_path, start_size=200)
    vy = ty + th + 50
    draw_text_with_stroke(draw, (centre_r(vw), vy), callout_value, vf,
                          YELLOW_ACCENT, stroke_w=6, shadow_offset=6)

    # Subtitle
    if callout_subtitle:
        sf, sw, sh = fit_text(draw, callout_subtitle, R_RIGHT - R_LEFT, 80,
                              display_font_path, start_size=60)
        sy = vy + vh + 30
        draw_text_with_stroke(draw, (centre_r(sw), sy), callout_subtitle, sf,
                              CREAM, stroke_w=3, shadow_offset=4)

    # AU badge
    if au_badge:
        bf = load_font(display_font_path, 36)
        bbox = draw.textbbox((0, 0), "AU", font=bf)
        bw_, bh_ = bbox[2] - bbox[0], bbox[3] - bbox[1]
        pad = 12
        pill_h = bh_ + pad * 2
        draw.rounded_rectangle(
            [30, H - pill_h - 30, 30 + bw_ + pad * 2, H - 30],
            radius=12, fill=OUTBACK_ORANGE)
        draw.text((30 + pad, H - pill_h - 30 + pad - 4), "AU",
                  font=bf, fill=CHARCOAL)

    img.convert("RGB").save(out_path, "PNG", optimize=True)
    return out_path


# ============================================================
# Public API
# ============================================================
def render_thumbnail(out_path, template, mj_background, **kwargs):
    """Dispatch to the correct template."""
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    if template == "A":
        return template_a_big_number(out_path, mj_background, **kwargs)
    elif template == "B":
        return template_b_comparison(out_path, mj_background, **kwargs)
    elif template == "C":
        return template_c_document_forensics(out_path, mj_background, **kwargs)
    else:
        raise ValueError(f"Unknown template '{template}'. Use A / B / C.")


# ============================================================
# Self-test: regenerate V1 thumbnail using template A
# ============================================================
if __name__ == "__main__":
    DOWNLOADS = Path.home() / "Downloads"
    BG_FILE = DOWNLOADS / "audealermath_YouTube_thumbnail_background_169_aspect_ratio_so_e00e2cd6-b6e9-4288-a9bc-84129a548098_0.png"
    OUT = REPO / "content" / "au-dealer-math" / "scripts" / "v01-thumbnail-engine-test.png"

    if BG_FILE.exists():
        render_thumbnail(
            out_path=OUT,
            template="A",
            mj_background=str(BG_FILE),
            headline_lines=["NEVER", "ANSWER", "THIS", "ONE", "QUESTION"],
            dollar_main="$300/WK",
            dollar_arrow_to="$46,800 MORE",
            dollar_subtitle="OUT OF YOUR POCKET",
        )
        print(f"[OK] Self-test thumbnail: {OUT}")
        print(f"     Size: {OUT.stat().st_size // 1024}KB")
    else:
        print(f"[skip] V1 MJ background not in Downloads — engine ready, no self-test render")
