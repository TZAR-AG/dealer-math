# Bake KB variants from existing v01-renders source PNGs for the S4-S6
# redistribution rebuild (2026-04-30). Adds 14 new KB clips so each long
# merged/baked clip in body+reveals sections gets visual variety via
# different KB direction + zoom on the same source PNG.
#
# Velocity rule applied (2-2.5%/sec):
#   - 11s body cuts: 9-10% zoom
#   - 12-15s body cuts: 8-9% zoom
#   - 16s+ slow cuts: 8% zoom + pan
#   - 5s reveals cuts: ~10% zoom
# Direction varied to avoid two consecutive same-direction cuts.
#
# Each baked duration is +0.10s above slot need to absorb sub-frame rounding.

import subprocess
from pathlib import Path

REPO = Path(r"C:\dev\Claude")
RENDERS = REPO / "content" / "au-dealer-math" / "scripts" / "v01-renders"
KB_OUT = RENDERS / "motion" / "baked" / "kb-v3"
KB_OUT.mkdir(parents=True, exist_ok=True)

FFMPEG = r"C:\Users\adria\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1-full_build\bin\ffmpeg.exe"

# (out_slot_id, source_png_relpath, duration_sec, kb_direction, zoom_pct, comment)
SLOTS = [
    # === S4 LOAN TRICK (4 new variants) ===
    ("s4-4B-commission-flow-panR-11s",  "stills/v2/still-v2-4B-commission-flow.png",      11.10, "panR", 10, "S4 #2 commission flow pan right"),
    ("s4-4D-luxury-treadmill-in-11s",   "stills/v2/still-v2-4D-luxury-treadmill.png",     11.10, "in",    9, "S4 #7 luxury zoom in"),
    ("s4-4D-luxury-treadmill-panL-12s", "stills/v2/still-v2-4D-luxury-treadmill.png",     12.10, "panL",  8, "S4 #9 luxury pan left variant"),
    ("s4-3-cars-comparison-out-15s",    "stills/still-3-cars-comparison.png",             15.50, "out",   7, "S4 #12 closing zoom out"),

    # === S5 WHY DEALER (5 new variants) ===
    ("s5-5A-three-glass-offices-out-11s",        "stills/v2/still-v2-5A-three-glass-offices.png",      11.10, "out",  9, "S5 #3 glass offices zoom out"),
    ("s5-5C-finance-desk-panR-11s",              "stills/v2/still-v2-5C-finance-desk.png",             11.10, "panR", 9, "S5 #5 finance desk pan right"),
    ("s5-5B-paint-protection-bottle-panL-11s",   "stills/v2/still-v2-5B-paint-protection-bottle.png",  11.10, "panL", 9, "S5 #9 paint protection variant"),
    ("s5-5D-holdback-three-tier-in-11s",         "stills/v2/still-v2-5D-holdback-three-tier.png",      11.10, "in",   9, "S5 #10 holdback zoom in"),
    ("s5-5E-cash-stack-panD-16s",                "stills/v2/still-v2-5E-cash-stack.png",               16.35, "panD", 8, "S5 #14 cash stack pan down closing"),

    # === S6 FIX (5 new variants) ===
    ("s6-6B-total-cost-comparison-panR-11s", "stills/v2/still-v2-6B-total-cost-comparison.png", 11.10, "panR", 10, "S6 #3 total-cost pan right"),
    ("s6-6A-bank-letter-in-11s",             "stills/v2/still-v2-6A-bank-letter.png",           11.10, "in",   10, "S6 #7 bank letter zoom in"),
    ("s6-6C-window-banner-panR-11s",         "stills/v2/still-v2-6C-window-banner.png",         11.10, "panR", 10, "S6 #12 window banner pan right"),
    ("s6-6B-total-cost-comparison-out-11s",  "stills/v2/still-v2-6B-total-cost-comparison.png", 11.10, "out",  10, "S6 #14 total-cost zoom out variant"),
    ("s6-6C-window-banner-out-5s",           "stills/v2/still-v2-6C-window-banner.png",          5.10, "out",   9, "S6 #16 window banner closing zoom out"),
]


def kb_filter(direction, zoom_pct, total_frames):
    z = zoom_pct / 100.0
    base_scale = "scale=7680:-1:flags=lanczos"
    if direction == "in":
        zexpr = f"1.0+{z}*on/{total_frames}"
        x, y = "iw/2-(iw/zoom/2)", "ih/2-(ih/zoom/2)"
    elif direction == "out":
        zexpr = f"1.0+{z}-{z}*on/{total_frames}"
        x, y = "iw/2-(iw/zoom/2)", "ih/2-(ih/zoom/2)"
    elif direction == "panR":
        zexpr = f"1.0+{z}"
        x, y = f"(iw-iw/zoom)*on/{total_frames}", "ih/2-(ih/zoom/2)"
    elif direction == "panL":
        zexpr = f"1.0+{z}"
        x, y = f"(iw-iw/zoom)*(1-on/{total_frames})", "ih/2-(ih/zoom/2)"
    elif direction == "panU":
        zexpr = f"1.0+{z}"
        x, y = "iw/2-(iw/zoom/2)", f"(ih-ih/zoom)*(1-on/{total_frames})"
    elif direction == "panD":
        zexpr = f"1.0+{z}"
        x, y = "iw/2-(iw/zoom/2)", f"(ih-ih/zoom)*on/{total_frames}"
    else:
        raise ValueError(direction)
    return f"{base_scale},zoompan=z='{zexpr}':d=1:x='{x}':y='{y}':s=1920x1080:fps=24"


print("=" * 70)
print(f"AUDM V1 rebuild — bake {len(SLOTS)} KB variants for S4-S6 redistribution")
print("=" * 70)

baked = 0
skipped = 0
for slot_id, src_rel, duration, direction, zoom_pct, comment in SLOTS:
    src = RENDERS / src_rel
    dst = KB_OUT / f"{slot_id}-kb.mp4"
    if not src.exists():
        print(f"  [SKIP] {slot_id}: source missing ({src.relative_to(RENDERS)})")
        skipped += 1
        continue
    total_frames = int(duration * 24)
    vf = kb_filter(direction, zoom_pct, total_frames)
    cmd = [
        FFMPEG, "-y", "-loglevel", "error",
        "-loop", "1", "-i", str(src),
        "-vf", vf,
        "-t", str(duration),
        "-c:v", "libx264", "-preset", "medium", "-crf", "18",
        "-pix_fmt", "yuv420p", "-r", "24", "-an",
        str(dst),
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode == 0:
        sz = dst.stat().st_size // 1024
        print(f"  [OK]   {slot_id:48s} {duration:5.2f}s {direction:5s} {zoom_pct}% ({sz}KB)  -- {comment}")
        baked += 1
    else:
        print(f"  [FAIL] {slot_id}: {r.stderr.strip()[:200]}")
        skipped += 1

print(f"\nBaked: {baked} / {len(SLOTS)}, skipped: {skipped}")
print(f"Output: {KB_OUT}")
