"""Render 5 vertical Shorts from V1 final MP4 via ffmpeg.

Locked cut points + caption overlays. Each Short:
  - 9:16 vertical (1080x1920)
  - 30-50 sec
  - Source clip is centre-cropped from the 16:9 master (NOT scaled — preserves
    1080p quality)
  - Burnt-in caption at top + "Full breakdown — search AU Dealer Math" CTA
    overlay at bottom for last 5 sec

Run AFTER V1 export. Output: video/out/shorts/audm-v1-short-N.mp4

Source: video/out/audm-v1-payment-not-price-pivot.mp4 (587.18s master)

Cuts (all timestamps in source MP4):
  Short 1 — The hook         (0:00.0  -> 0:30.0,  30s)  "Never answer this question"
  Short 2 — The $46K reveal  (2:48.0  -> 3:18.0,  30s)  "Why weekly payments cost you $46K"
  Short 3 — The two-sentence (7:15.0  -> 7:50.0,  35s)  "What to actually say at a dealership"
  Short 4 — Three rooms      (4:38.0  -> 5:08.0,  30s)  "Three rooms dealerships hide from you"
  Short 5 — Aftercare margin (5:58.0  -> 6:28.0,  30s)  "$1,000-$2,500 dealer profit on aftercare"
"""

import subprocess
from pathlib import Path

REPO = Path(r"C:\dev\Claude")
SRC = REPO / "video" / "out" / "audm-v1-payment-not-price-pivot-v2.mp4"  # v2 = YT Audio Library music swap, Content-ID safe
OUT_DIR = REPO / "video" / "out" / "shorts"
OUT_DIR.mkdir(parents=True, exist_ok=True)

FFMPEG = r"C:\Users\adria\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1-full_build\bin\ffmpeg.exe"
FONTS_DIR = REPO / "fonts"
DMSANS_BOLD = FONTS_DIR / "DM_Sans" / "DMSans-Bold.ttf"

# (slot_id, start_sec, dur_sec, top_line_1, top_line_2, cta_text)
# Captions broken into 2 lines because ffmpeg drawtext doesn't handle \n inside
# filter strings reliably. Each line gets its own drawtext filter.
SHORTS = [
    ("audm-v1-short-1-hook",
     0.0, 30.0,
     "NEVER ANSWER",
     "THIS QUESTION",
     "Search AU Dealer Math"),
    ("audm-v1-short-2-46k-reveal",
     168.0, 30.0,
     "$46\\,800 MORE",
     "OUT OF YOUR POCKET",
     "Search AU Dealer Math"),
    ("audm-v1-short-3-two-sentence-fix",
     435.0, 35.0,
     "WHAT TO SAY",
     "AT A DEALERSHIP",
     "Search AU Dealer Math"),
    ("audm-v1-short-4-three-rooms",
     278.0, 30.0,
     "THREE ROOMS",
     "DEALERSHIPS HIDE",
     "Search AU Dealer Math"),
    ("audm-v1-short-5-aftercare-margin",
     358.0, 30.0,
     "$1000-$2500",
     "DEALER PROFIT",
     "Search AU Dealer Math"),
]


def build_filter(top_line_1, top_line_2, cta_text, dur):
    """ffmpeg filter:
       1. Source 1920x1080 -> blur-pad to 1080x1920 (Shorts vertical)
       2. Two-line caption at top (separate drawtext per line — \\n unreliable)
       3. CTA v2 last 5 sec — branded design:
          - Dim bottom-third dark band
          - "SEARCH" small cream caption
          - "AU DEALER MATH" big cream BOLD
          - Orange highlight stroke under "AU DEALER MATH" (logo v2 motif)
          - No orange box bg — clean type-on-video
    """
    font_arg = str(DMSANS_BOLD).replace('\\', '/').replace(':', r'\:')
    cta_start = max(0, dur - 5.0)
    enable_cta = f"enable='gte(t,{cta_start})'"

    # CTA layout positions (Y from top of 1920px frame)
    cta_bg_top = 1500       # top of dim band
    cta_search_y = 1560     # "SEARCH" small label
    cta_brand_y = 1640      # "AU DEALER MATH" big bold
    cta_stroke_y = 1810     # orange highlight stroke under brand text
    cta_stroke_h = 16

    f = (
        # 1. Blur-pad 16:9 -> 9:16
        f"[0:v]split=2[orig][bg_src];"
        f"[bg_src]scale=1080:1920:force_original_aspect_ratio=increase,"
        f"crop=1080:1920,boxblur=20:5,eq=brightness=-0.20[bg];"
        f"[orig]scale=1080:-2[fg_scaled];"
        f"[bg][fg_scaled]overlay=(W-w)/2:(H-h)/2[base];"
        # 2a. Caption line 1 — top
        f"[base]drawtext=fontfile='{font_arg}'"
        f":text='{top_line_1}'"
        f":fontcolor=#F5EFE6"
        f":fontsize=72"
        f":bordercolor=#000000:borderw=5"
        f":x=(w-text_w)/2"
        f":y=140"
        f":box=1:boxcolor=#000000CC:boxborderw=18[cap1];"
        # 2b. Caption line 2 — directly below line 1
        f"[cap1]drawtext=fontfile='{font_arg}'"
        f":text='{top_line_2}'"
        f":fontcolor=#F5EFE6"
        f":fontsize=72"
        f":bordercolor=#000000:borderw=5"
        f":x=(w-text_w)/2"
        f":y=240"
        f":box=1:boxcolor=#000000CC:boxborderw=18[capped];"
        # 3a. CTA dim bottom band (last 5 sec) — pulls eye to brand name
        f"[capped]drawbox=x=0:y={cta_bg_top}:w=1080:h={1920 - cta_bg_top}"
        f":color=#000000@0.55:t=fill"
        f":{enable_cta}[ctabg];"
        # 3b. "SEARCH" small label
        f"[ctabg]drawtext=fontfile='{font_arg}'"
        f":text='SEARCH'"
        f":fontcolor=#F5EFE6"
        f":fontsize=48"
        f":bordercolor=#000000:borderw=3"
        f":x=(w-text_w)/2"
        f":y={cta_search_y}"
        f":{enable_cta}[ctasearch];"
        # 3c. "AU DEALER MATH" big bold brand line
        f"[ctasearch]drawtext=fontfile='{font_arg}'"
        f":text='AU DEALER MATH'"
        f":fontcolor=#F5EFE6"
        f":fontsize=96"
        f":bordercolor=#000000:borderw=5"
        f":x=(w-text_w)/2"
        f":y={cta_brand_y}"
        f":{enable_cta}[ctabrand];"
        # 3d. Orange highlight stroke under brand text (logo v2 motif)
        f"[ctabrand]drawbox=x=140:y={cta_stroke_y}:w=800:h={cta_stroke_h}"
        f":color=#D17A3D:t=fill"
        f":{enable_cta}"
    )
    return f


def render_short(slot_id, start_sec, dur_sec, top_line_1, top_line_2, cta_text):
    out = OUT_DIR / f"{slot_id}.mp4"
    vf = build_filter(top_line_1, top_line_2, cta_text, dur_sec)
    cmd = [
        FFMPEG, "-y", "-loglevel", "error",
        "-ss", f"{start_sec:.3f}",
        "-i", str(SRC),
        "-t", f"{dur_sec:.3f}",
        "-filter_complex", vf,
        "-map", "0:a",
        "-c:v", "libx264", "-preset", "medium", "-crf", "20",
        "-pix_fmt", "yuv420p", "-r", "24",
        "-c:a", "aac", "-b:a", "192k",
        str(out),
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode == 0:
        sz_mb = out.stat().st_size / (1024 * 1024)
        print(f"  [OK] {slot_id:42s} {dur_sec:.1f}s ({sz_mb:.1f}MB)")
    else:
        print(f"  [FAIL] {slot_id}: {r.stderr.strip()[:300]}")


if __name__ == "__main__":
    if not SRC.exists():
        raise FileNotFoundError(f"V1 master not found: {SRC}")

    print("=" * 70)
    print(f"Rendering {len(SHORTS)} vertical Shorts from V1 master")
    print(f"Source: {SRC.name}")
    print(f"Output: {OUT_DIR}")
    print("=" * 70)

    for slot_id, start, dur, top1, top2, cta in SHORTS:
        render_short(slot_id, start, dur, top1, top2, cta)

    print(f"\nDone. {len(SHORTS)} Shorts in {OUT_DIR}")
    print("\nNext steps:")
    print("  1. Schedule one Short per day Day 0-4 (Sun 3 May - Thu 7 May)")
    print("  2. Title format: 'The question Aussie car dealers don't want you to answer #shorts'")
    print("  3. Description: 'Full breakdown on the channel - link in bio.' + 3 hashtags")
    print("  4. Vertical thumbnail: same template as Shorts caption (auto-grabbed by YT)")
