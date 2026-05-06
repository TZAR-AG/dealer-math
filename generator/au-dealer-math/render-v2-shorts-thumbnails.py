"""Render variant B hook-card thumbnails for all 5 V2 Shorts.

Per-Short mapping resolved 2026-05-06 by reading scene topics in
build-v02-shorts-2-5.py SHORTS config:

  Short 1: $4,800     DEALER MARGIN     (F&I rate-range reveal)
  Short 2: $3,000     RATE LOAD         (rate-game interest-cost beat)
  Short 3: +4 POINTS  RATE SPREAD       (4-point bank-vs-dealer spread)
  Short 4: $3,000     AFTERCARE MARGIN  (aftercare margin reveal)
  Short 5: 3 ROOMS    F&I PIPELINE      (three-negotiators-in-sequence)

Output: content/au-dealer-math/scripts/v02-renders/hook-card-proto/v2-thumbs/

Run: python generator/au-dealer-math/render-v2-shorts-thumbnails.py
"""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import sys

REPO = Path(r"C:\dev\Claude")
sys.path.insert(0, str(REPO / "generator" / "au-dealer-math"))
from hook_card import render_card, DMSANS_BOLD

OUT = REPO / "content" / "au-dealer-math" / "scripts" / "v02-renders" / "hook-card-proto" / "v2-thumbs"
OUT.mkdir(parents=True, exist_ok=True)

SHORTS = [
    (1, "$4,800",    "DEALER PROFIT"),
    (2, "$3,000",    "EXTRA INTEREST"),
    (3, "+4 POINTS", "HIGHER RATE"),
    (4, "$3,000",    "ADD-ON PROFIT"),
    (5, "3 ROOMS",   "PROFIT STAGES"),
]


def main():
    print(f"Rendering {len(SHORTS)} V2 Short thumbnails -> {OUT}\n")
    rendered = []
    for idx, hook, label in SHORTS:
        out_png = OUT / f"short-{idx}.png"
        render_card(hook, label, out_png)
        print(f"  [ok] Short {idx}: {hook} / {label}  ->  {out_png.name}")
        rendered.append((idx, hook, label, out_png))

    print("\nBuilding contact sheet...")
    THUMB_W, THUMB_H = 480, 854
    PAD = 30
    LABEL_H = 60
    HEADER_H = 80

    cols = 5
    sheet_w = PAD + cols * (THUMB_W + PAD)
    sheet_h = HEADER_H + PAD + THUMB_H + LABEL_H + PAD
    sheet = Image.new("RGB", (sheet_w, sheet_h), (240, 240, 240))
    draw = ImageDraw.Draw(sheet)
    head_f = ImageFont.truetype(str(DMSANS_BOLD), 32)
    label_f = ImageFont.truetype(str(DMSANS_BOLD), 22)

    draw.text((PAD, 25),
              "AUDM V2 Shorts - variant B hook-card thumbnails (5 of 5)",
              font=head_f, fill=(40, 40, 40))

    y0 = HEADER_H + PAD
    for ci, (idx, hook, label, png) in enumerate(rendered):
        img = Image.open(png).resize((THUMB_W, THUMB_H), Image.LANCZOS)
        x = PAD + ci * (THUMB_W + PAD)
        sheet.paste(img, (x, y0))
        draw.text((x, y0 + THUMB_H + 10),
                  f"Short {idx}: {hook} / {label}",
                  font=label_f, fill=(60, 60, 60))

    sheet_path = OUT / "contact-sheet.png"
    sheet.save(sheet_path, optimize=True)
    print(f"  [ok] {sheet_path}")
    print(f"\n{'='*60}")
    print(f"Done. {len(SHORTS)} V2 Short thumbnails ready for review.")
    print(f"  Folder         : {OUT}")
    print(f"  Contact sheet  : {sheet_path}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
