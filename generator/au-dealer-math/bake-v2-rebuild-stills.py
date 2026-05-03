# AU Dealer Math V2 — bake KB-animated MP4s from the 50 curated v2/ stills.
#
# Reads from content/au-dealer-math/scripts/v02-renders/stills/v2/ (NOT Downloads).
# Each slot maps to one PNG via 8-char UUID prefix.
# Output: motion/baked/kb-v2/{slot_id}-kb.mp4 at section-aware cadence.
#
# Slot allocation across the 7 V2 sections (50 unique stills, no callbacks here —
# motif callbacks live in the timeline VISUAL_TRACK, not the bake):
#   HOOK        4 stills @ 4s 14-16%   (hook cadence — fast cuts, larger zoom)
#   AUTHORITY   6 stills @ 8s 12-13%
#   FNIOFFICE  11 stills @ 9-10s 11-12%
#   RATEGAME   13 stills @ 9s 11-12%
#   COMMISSION 11 stills @ 9.5s 11-12%
#   FIX         5 stills @ 9.5s 12-13%
#   SIGNOFF     0 unique (reuses AUTH baked clips for ext/showroom)

import shutil
import subprocess
from pathlib import Path

REPO = Path(r"C:\dev\Claude")
RENDERS = REPO / "content" / "au-dealer-math" / "scripts" / "v02-renders"
SOURCE = RENDERS / "stills" / "v2"
STILLS_OUT = RENDERS / "stills" / "auto-v2"
KB_OUT = RENDERS / "motion" / "baked" / "kb-v2"
STILLS_OUT.mkdir(parents=True, exist_ok=True)
KB_OUT.mkdir(parents=True, exist_ok=True)

FFMPEG = r"C:\Users\adria\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1-full_build\bin\ffmpeg.exe"

# (slot_id, uuid8, duration_sec, kb_direction, zoom_pct, comment)
# kb_direction: "in", "out", "panR", "panL", "panU", "panD"
SLOTS = [
    # === HOOK (4 stills · 4s @ 14-16% · varied directions) ===
    ("hook-c1", "877e80ce", 4.0, "in",   16, "Top-down hand close-up — open"),
    ("hook-c2", "e6e3d37d", 4.0, "panR", 16, "Ink stroke macro"),
    ("hook-c3", "b6dde562", 4.0, "panL", 15, "Cream-colored top-down"),
    ("hook-c4", "765cc848", 4.3, "in",   14, "Orange-banded contract + pen sharp (rescue)"),

    # === AUTHORITY (6 stills · 8s @ 12-13%) ===
    ("auth-c1", "87a4deab", 8.0, "in",   13, "Low-angle looking up at building"),
    ("auth-c2", "5b6d85e8", 8.0, "panR", 12, "Eye-level AU street view"),
    ("auth-c3", "3034f985", 8.0, "in",   13, "AU showroom interior wide"),
    ("auth-c4", "0f5605c7", 8.0, "panR", 12, "Wide along corridor / dealership"),
    ("auth-c5", "5f86a55a", 8.0, "in",   13, "Vehicle 3/4 studio interior"),
    ("auth-c6", "8ca006eb", 8.5, "in",   12, "F&I office medium-wide top-down"),

    # === FNIOFFICE (11 stills · 9-10s @ 11-12%) ===
    ("fnio-c1", "633a30df", 10.0, "panD", 11, "Top-down modern desk"),
    ("fnio-c2", "24bcdafd", 10.0, "in",   12, "Pen on cream paper"),
    ("fnio-c3", "3c35a527",  9.0, "in",   11, "Top-down hand close-up"),
    ("fnio-c4", "2420ec44", 10.0, "panR", 11, "Printed pages on desk"),
    ("fnio-c5", "1b024c4d",  9.0, "in",   11, "Modern desk wide view"),
    ("fnio-c6", "3dbfe118", 10.0, "in",   12, "Hand holding pen"),
    ("fnio-c7", "4093bc8c",  9.0, "panD", 11, "Directly overhead docs"),
    ("fnio-c8", "1c724184", 10.0, "in",   12, "Black calculator close-up"),
    ("fnio-c9", "4cdcffc9",  9.0, "panL", 11, "Top-down hand close-up"),
    ("fnio-c10","67dfbc48",  9.0, "panR", 11, "Top-down clean modern"),
    ("fnio-c11","4f7e89c5",  6.5, "out",  12, "Studio chiaroscuro"),

    # === RATEGAME (13 stills · 9s @ 11-12%) ===
    ("rate-c1", "a66ec6d0", 9.0, "in",   12, "Studio chiaroscuro single-source"),
    ("rate-c2", "794e5e56", 9.0, "panR", 11, "Charcoal side-angle"),
    ("rate-c3", "7b3d59b6", 9.0, "in",   11, "Top-down hand close-up"),
    ("rate-c4", "8e81b2ca", 9.0, "panL", 11, "Top-down hand"),
    ("rate-c5", "615ab304", 9.0, "in",   12, "Top-down hand close-up"),
    ("rate-c6", "2a159018", 9.0, "panD", 11, "Top-down hand"),
    ("rate-c7", "746dca78", 9.0, "in",   12, "Male hand"),
    ("rate-c8", "9a2005c0", 9.0, "panR", 11, "Hand holding"),
    ("rate-c9", "df7102a9", 9.0, "panL", 11, "Plain cream top-down"),
    ("rate-c10","fd09a18c", 9.0, "out",  11, "Plain cream"),
    ("rate-c11","48b2af16", 9.0, "in",   12, "Modern desk wide"),
    ("rate-c12","fde83261", 9.0, "panR", 11, "Wide modern desk"),
    ("rate-c13","24853820", 9.0, "in",   12, "Person shoulders rear"),

    # === COMMISSION (11 stills · 9.5s @ 11-12%) ===
    ("comm-c1", "fba79fbb", 9.5, "panD", 11, "High aerial top-down"),
    ("comm-c2", "0a984138", 9.5, "in",   11, "Wide establishing"),
    ("comm-c3", "63a7cc73", 9.5, "panR", 11, "POV from seat"),
    ("comm-c4", "10f5fced", 9.5, "in",   12, "Vehicle 3/4 rear"),
    ("comm-c5", "d13affb1", 9.5, "panD", 11, "Aerial top-down"),
    ("comm-c6", "148f5a9c", 9.5, "in",   12, "AU automotive interior wide"),
    ("comm-c7", "b157651c", 9.5, "in",   12, "Vehicle 3/4 studio"),
    ("comm-c8", "58f0f424", 9.5, "panR", 11, "Three-quarter wide view"),
    ("comm-c9", "0ceb1475", 9.5, "panL", 11, "Three-quarter wide view"),
    ("comm-c10","bced541c", 9.5, "in",   12, "Showroom low-angle"),
    ("comm-c11","c74105db", 9.5, "out",  11, "Vehicle frontal"),

    # === FIX (5 stills · 9.5s @ 12-13%) ===
    ("fix-c1",  "989e9dc8", 9.5, "in",   13, "AU vehicle 3/4"),
    ("fix-c2",  "c2aeeb48", 9.5, "panR", 12, "AU showroom interior wide"),
    ("fix-c3",  "5b880412", 9.5, "in",   13, "AU 3/4"),
    ("fix-c4",  "0a742524", 9.5, "panR", 12, "AU 3/4 vehicle"),
    ("fix-c5",  "9b9124bf", 9.5, "in",   13, "Low side-angle close-up door"),
]


def find_source(uuid8):
    """Find PNG by 8-char UUID prefix in v2/ folder."""
    candidates = list(SOURCE.glob(f"*_{uuid8}-*.png"))
    if not candidates:
        # fallback: any file containing the uuid8
        candidates = list(SOURCE.glob(f"*{uuid8}*.png"))
    if not candidates:
        return None
    return max(candidates, key=lambda p: p.stat().st_size)


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
        raise ValueError(f"Unknown direction: {direction}")
    return f"{base_scale},zoompan=z='{zexpr}':d=1:x='{x}':y='{y}':s=1920x1080:fps=24"


print("=" * 70)
print("AUDM V2 Rebuild — bake KB MP4s from v2/ curated stills (50 keepers)")
print("=" * 70)

baked = 0
skipped = 0
for slot_id, uuid8, duration, direction, zoom_pct, comment in SLOTS:
    src = find_source(uuid8)
    if not src:
        print(f"  [SKIP] {slot_id}: source not found (uuid8: {uuid8})")
        skipped += 1
        continue

    dst_png = STILLS_OUT / f"{slot_id}.png"
    if not dst_png.exists() or dst_png.stat().st_mtime < src.stat().st_mtime:
        shutil.copy2(src, dst_png)

    out_mp4 = KB_OUT / f"{slot_id}-kb.mp4"
    # Bake +0.10s longer than slot needs (per playbook — guards against rounding overflow)
    bake_dur = duration + 0.10
    total_frames = int(bake_dur * 24)
    vf = kb_filter(direction, zoom_pct, total_frames)
    cmd = [
        FFMPEG, "-y", "-loglevel", "error",
        "-loop", "1", "-i", str(dst_png),
        "-vf", vf,
        "-t", str(bake_dur),
        "-c:v", "libx264", "-preset", "medium", "-crf", "18",
        "-pix_fmt", "yuv420p", "-r", "24", "-an",
        str(out_mp4),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        sz = out_mp4.stat().st_size // 1024
        print(f"  [OK]   {slot_id:12s} {duration:.1f}s {direction:5s} {zoom_pct:>3d}% ({sz}KB)")
        baked += 1
    else:
        print(f"  [FAIL] {slot_id}: {result.stderr.strip()[:200]}")
        skipped += 1

print(f"\nBaked: {baked} / {len(SLOTS)}, skipped: {skipped}")
print(f"Output: {KB_OUT}")
print(f"Source PNGs (renamed): {STILLS_OUT}")
