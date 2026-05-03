"""Bake AUDM V2 (Finance Manager's Office) KB-animated MP4s from the 50
curated stills in v02-renders/stills/v2/.

Pipeline position:
    MJ stills (curated 2026-05-04, 49 keepers + 1 _nea rescue)
        -> THIS SCRIPT
        -> motion/baked/kb-v2/<slot-id>-kb.mp4
        -> build-v2-davinci.py imports each baked clip into DaVinci timeline

Each slot defines:
    (slot_id, source_uuid_substring, duration_sec, kb_direction, zoom_pct)

Source matching is on the LAST 8 chars of the MJ UUID (always unique inside the
v2/ folder). Direct match avoids the brittle prompt-fragment globbing the V1
bake script used.

53 slot entries across 50 unique stills. The 3 reuses (motif callbacks across
scenes) get distinct slot IDs so each gets its own baked MP4 with appropriate
KB direction + duration.

Sums to 528.08s (master VO duration). No-adjacent-same-image rule satisfied
across all scene boundaries (verified 2026-05-04 build).
"""

import shutil
import subprocess
from pathlib import Path

REPO = Path(r"C:\dev\Claude")
RENDERS = REPO / "content" / "au-dealer-math" / "scripts" / "v02-renders"
STILLS_SRC = RENDERS / "stills" / "v2"           # 50 curated MJ stills
STILLS_OUT = RENDERS / "stills" / "auto-v2"      # renamed slot-id PNGs (build-script convention)
KB_OUT = RENDERS / "motion" / "baked" / "kb-v2"  # baked KB MP4s
STILLS_OUT.mkdir(parents=True, exist_ok=True)
KB_OUT.mkdir(parents=True, exist_ok=True)

FFMPEG = r"C:\Users\adria\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1-full_build\bin\ffmpeg.exe"

# (slot_id, uuid_short, duration_sec, kb_direction, zoom_pct, comment)
SLOTS = [
    # === S1 HOOK (0.00-16.20s, 5 cuts, 14-17% zoom, 2.5-3.5s) =================
    ("s1-h1-cream-contract",         "b6dde562", 3.50, "panR", 16, "Cream contract opening establish"),
    ("s1-h2-orange-band-rescue",     "765cc848", 3.00, "in",   17, "Orange-banded contract DOF blur (rescue)"),
    ("s1-h3-hand-pointing",          "877e80ce", 3.30, "in",   16, "Hand close finger to line"),
    ("s1-h4-black-close",            "1c724184", 3.00, "panD", 15, "Dark grey laminate desk anchor"),
    ("s1-h5-chiaroscuro",            "4f7e89c5", 3.40, "out",  14, "Studio chiaroscuro pre-wordmark"),

    # === S2 AUTHORITY (16.20-63.32s, 7 cuts, 11-14% zoom, 6-7s) ===============
    ("s2-a1-aerial-1",               "fba79fbb", 6.00, "panR", 13, "Aerial dealership floor establish"),
    ("s2-a2-aerial-2",               "d13affb1", 6.00, "in",   12, "Aerial alt — different angle"),
    ("s2-a3-frontal-symmetric",      "c74105db", 7.10, "panL", 13, "Frontal symmetric building / three doors"),
    ("s2-a4-low-wide-along",         "0f5605c7", 7.00, "in",   12, "Low wide along corridor"),
    ("s2-a5-low-angle-up",           "87a4deab", 7.00, "panU", 13, "Low-angle up — building exterior"),
    ("s2-a6-eye-street",             "5b6d85e8", 7.00, "out",  14, "Eye-level street view"),
    ("s2-a7-low-wide-across",        "bced541c", 7.02, "panR", 11, "Low-angle wide across — section close"),

    # === S3 F&I OFFICE (63.32-163.94s, 9 cuts, 8-12% zoom, 7-16s) ============
    ("s3-f1-wide-two-chairs",        "0a984138", 7.38, "in",   12, "F&I WIDE establishing two chairs (KEY anchor)"),
    ("s3-f2-modern-topdown",         "633a30df", 10.00, "panD", 10, "Cinema verite modern desk top-down"),
    ("s3-f3-modern-desk",            "1b024c4d", 10.00, "panL", 10, "Modern desk top-down"),
    ("s3-f4-hand-close-1",           "8e81b2ca", 10.00, "in",   9, "Hand close — paperwork moment"),
    ("s3-f5-clean-modern",           "67dfbc48", 11.00, "out",  10, "Clean modern desk surface"),
    ("s3-f6-wide-modern-1",          "48b2af16", 12.00, "panR",  9, "Top-down wide modern"),
    ("s3-f7-hand-close-2",           "7b3d59b6", 11.00, "in",   11, "Hand close alt"),
    ("s3-f8-wide-modern-2",          "fde83261", 13.00, "panU",  8, "Top-down wide modern alt"),
    ("s3-f9-interior-au-1",          "3034f985", 16.24, "out",   8, "Wide interior AU showroom — close section"),

    # === S4 RATE RANGE (163.94-280.82s, 10 cuts, 9-12% zoom, 7-15s) ==========
    ("s4-r1-interior-au-2",          "c2aeeb48", 7.56, "in",   12, "Wide interior AU — section pivot"),
    ("s4-r2-cinema-hand",            "4cdcffc9", 12.00, "panR", 10, "Cinema verite hand top-down"),
    ("s4-r3-hand-close-3",           "2a159018", 10.00, "panD", 10, "Hand close"),
    ("s4-r4-hand-close-4",           "615ab304", 11.00, "in",   10, "Hand close — calculator beat"),
    ("s4-r5-plain-cream-1",          "df7102a9", 12.00, "out",  10, "Plain cream paper"),
    ("s4-r6-directly-overhead",      "4093bc8c", 12.00, "panL", 11, "Directly overhead — rate sheet"),
    ("s4-r7-male-hand",              "746dca78", 12.00, "in",    9, "Male hand top-down (anchor for drift)"),
    ("s4-r8-ink-macro",              "e6e3d37d", 12.00, "panU", 10, "Macro ink stroke — signing reveal"),
    ("s4-r9-medium-wide",            "8ca006eb", 13.00, "out",  11, "Cinema verite medium-wide top-down"),
    ("s4-r10-pen-close-rescue",     "24bcdafd", 15.32, "in",    9, "Pen close (KEEP rescue) — section close"),

    # === S5 COMMISSION (280.82-386.69s, 9 cuts, 8-11% zoom, 9-14s) ===========
    ("s5-c1-printed-rescue",         "2420ec44", 9.48, "panR", 11, "Printed (KEEP rescue) — brochure fan-out"),
    ("s5-c2-hand-close-reuse",       "877e80ce", 11.00, "in",   10, "REUSE hand close (motif callback, 4.7min apart)"),
    ("s5-c3-hand-holding-1",         "3dbfe118", 11.00, "panD", 10, "Hand holding"),
    ("s5-c4-hand-holding-2",         "9a2005c0", 12.00, "out",  10, "Hand holding alt"),
    ("s5-c5-low-side-close",         "9b9124bf", 12.00, "panU",  9, "Low side-angle close-up"),
    ("s5-c6-hand-close-5",           "3c35a527", 13.00, "in",    9, "Hand close — product stack moment"),
    ("s5-c7-au-vehicle-1",           "0a742524", 12.00, "panL", 10, "AU vehicle 3/4 — cash-buyer mention"),
    ("s5-c8-au-vehicle-2",           "5b880412", 14.00, "out",  10, "AU vehicle 3/4 alt"),
    ("s5-c9-au-vehicle-3",           "989e9dc8", 11.39, "in",    8, "AU vehicle 3/4 — novated lease nod"),

    # === S6 FIX (386.69-482.20s, 9 cuts, 11-13% zoom, 9-13s) =================
    ("s6-x1-plain-cream-2",          "fd09a18c", 9.31, "in",   13, "Plain cream — restart on doc-forensics"),
    ("s6-x2-rear-shoulders",         "24853820", 9.00, "panR", 12, "Rear shoulders — customer in chair"),
    ("s6-x3-pov-from-seat",          "63a7cc73", 9.00, "in",   13, "POV from seat — customer perspective"),
    ("s6-x4-studio-interior-1",      "b157651c", 10.00, "panD",11, "Studio interior 3/4 — F&I office"),
    ("s6-x5-studio-interior-2",      "5f86a55a", 10.00, "out", 12, "Studio interior 3/4 alt"),
    ("s6-x6-side-angle-charcoal",    "794e5e56", 11.00, "panL",12, "Side-angle charcoal — calm authority"),
    ("s6-x7-vehicle-wide-1",         "0ceb1475", 11.00, "in",  11, "Vehicle 3/4 wide"),
    ("s6-x8-vehicle-wide-2",         "58f0f424", 13.00, "panU",11, "Vehicle 3/4 wide alt"),
    ("s6-x9-studio-dramatic",        "a66ec6d0", 13.20, "out", 13, "Studio dramatic — heavy reveal moment"),

    # === S7 SIGNOFF (482.20-528.08s, 4 cuts, 12-14% zoom, 8-14s, calm) =======
    ("s7-z1-studio-wide-au",         "148f5a9c", 10.30, "panR",13, "Studio wide AU auto — V3 setup"),
    ("s7-z2-rear-vehicle",           "10f5fced", 14.00, "in",  14, "Rear 3/4 vehicle — driving away"),
    ("s7-z3-chiaroscuro-reuse",      "4f7e89c5", 14.00, "panD",13, "REUSE chiaroscuro — Macca silhouette closing"),
    ("s7-z4-cream-contract-reuse",   "b6dde562",  7.58, "out", 12, "REUSE cream contract — closing motif callback to s1-h1"),
]


def find_source(uuid_short):
    """Find the curated PNG matching the UUID short ID in v2/ folder."""
    candidates = list(STILLS_SRC.glob(f"*{uuid_short}*.png"))
    if not candidates:
        return None
    if len(candidates) > 1:
        raise RuntimeError(f"Ambiguous UUID match for {uuid_short}: {[c.name for c in candidates]}")
    return candidates[0]


def kb_filter(direction, zoom_pct, total_frames):
    """Build ffmpeg zoompan filter string for given direction + zoom %."""
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
print(f"AUDM V2 (Finance Manager's Office) — bake KB MP4s from 50 curated stills")
print(f"Slots: {len(SLOTS)}  ·  Output: {KB_OUT}")
print("=" * 70)

baked = 0
skipped = 0
total_dur = 0.0
for slot_id, uuid_short, duration, direction, zoom_pct, comment in SLOTS:
    src = find_source(uuid_short)
    if not src:
        print(f"  [SKIP] {slot_id}: source not found (uuid_short: {uuid_short})")
        skipped += 1
        continue

    # Copy + rename source PNG to project folder (slot-id naming for traceability)
    dst_png = STILLS_OUT / f"{slot_id}.png"
    if not dst_png.exists() or dst_png.stat().st_mtime < src.stat().st_mtime:
        shutil.copy2(src, dst_png)

    # Bake KB MP4 — bake +0.10s longer than slot to absorb 1-frame rounding
    bake_dur = duration + 0.10
    out_mp4 = KB_OUT / f"{slot_id}-kb.mp4"
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
        total_dur += duration
        print(f"  [OK]   {slot_id:36s} {duration:5.2f}s {direction:5s} {zoom_pct:>2}% ({sz:>5d}KB)")
        baked += 1
    else:
        print(f"  [FAIL] {slot_id}: {result.stderr.strip()[:200]}")
        skipped += 1

print(f"\nBaked: {baked} / {len(SLOTS)}, skipped: {skipped}")
print(f"Total visual track duration: {total_dur:.2f}s (target master VO: 528.08s)")
print(f"\nOutput KB clips: {KB_OUT}")
print(f"Source PNGs (slot-id renamed): {STILLS_OUT}")
