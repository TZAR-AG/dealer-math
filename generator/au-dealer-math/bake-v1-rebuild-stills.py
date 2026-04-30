# Bake all V1 rebuild MJ stills into KB-animated MP4s.
# Reads MJ-named PNGs from Downloads, renames to slot names, runs ffmpeg zoompan
# at duration-scaled zoom % per the locked AUDM cadence research.

import shutil
import subprocess
from pathlib import Path

REPO = Path(r"C:\dev\Claude")
DOWNLOADS = Path.home() / "Downloads"
RENDERS = REPO / "content" / "au-dealer-math" / "scripts" / "v01-renders"
STILLS_OUT = RENDERS / "stills" / "auto-v2"
KB_OUT = RENDERS / "motion" / "baked" / "kb-v2"
STILLS_OUT.mkdir(parents=True, exist_ok=True)
KB_OUT.mkdir(parents=True, exist_ok=True)

FFMPEG = r"C:\Users\adria\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1-full_build\bin\ffmpeg.exe"

# Slot definitions: (slot_id, source_pattern, duration_sec, kb_direction, zoom_pct, comment)
# kb_direction: "in" (zoom-in 1.0->1+z), "out" (1+z->1.0), "panR", "panL", "panU", "panD"
SLOTS = [
    # === Hook (Section 1) — 3-4s clips, 14-18% zoom ===
    ("s1-h2-pen-on-contract",       "extreme_close-up_of_a_sales", 3.0, "in",   16, "Hand pointing at contract column"),
    # ("s1-h3-showroom-dusk", ...) — MISSING, will add when H3 lands
    ("s1-h4-clock-papers",          "still_life_photograph_an_analog_clock", 3.0, "in",   16, "Clock + papers gold light"),
    ("s1-h5-dealership-perspective","deep_one-point_perspective",  3.0, "panR", 15, "One-point perspective dealership"),
    ("s1-h6-customer-doorway",      "low_angle_behind_silhouette", 2.0, "in",   18, "Silhouette through doorway"),
    ("s1-h7-corridor",              "cinema-verit_interior_view",  4.0, "in",   14, "Three-doors corridor"),

    # === Authority (Section 2) — 5-7s clips, 12-14% zoom ===
    ("s2-a1-floor-golden",          "wide_low-angle_view_across__a0a12b69", 5.0, "in",   14, "Golden hour dealership floor"),
    ("s2-a2-mass-market",           "mid-range_automotive_dealer", 5.0, "panR", 12, "Mass-market interior"),
    ("s2-a3-luxury-showroom",       "upmarket_European-style_aut", 5.0, "in",   14, "Luxury European showroom"),
    ("s2-a4-executive-desk",        "still_life_photograph_an_empty_modern", 7.0, "in", 12, "Empty exec office desk"),
    ("s2-a5-paper-stack",           "still_life_photograph_a_tall_stack_of", 6.0, "panD", 13, "Stack of files / unseen process"),
    ("s2-a6-three-windows-night",   "exterior_architectural_nigh", 5.0, "out",  14, "Three illuminated office windows night"),

    # === Question (Section 3) — 5-7s clips, 12-15% zoom ===
    ("s3-q1-salesperson-silhouette","wide_low-angle_view_across__6408cbde", 5.0, "in", 14, "Salesperson approaching across showroom"),
    ("s3-q2-hands-across-desk",     "two_pairs_of_hands_meeting_", 5.0, "in",   13, "Two pairs of hands meeting"),
    ("s3-q3-clasped-hands",         "extreme_close-up_of_a_custo", 5.0, "out",  13, "Customer hands clasped tense"),
    ("s3-q4-calculator-paper",      "still_life_photograph_a_black_anodised", 5.0, "panD", 14, "Calculator + scratch paper"),
    ("s3-q5-weekly-column",         "three-quarter_overhead_view",  7.0, "in",  12, "Weekly column highlighted"),
    ("s3-q6-contract-overhead",     "top-down_90-degree_overhead", 6.0, "out",  12, "Overhead with marker"),
    ("s3-q7-training-binder",       "an_open_three-ring_vinyl-bo", 6.0, "in",   13, "Training binder open"),
    ("s3-q8-handshake-silhouettes", "two_business-attire_silhoue", 5.0, "in",   14, "Handshake silhouettes"),
    ("s3-q9-clipboard-checklist",   "top-down_view_of_a_charcoal", 6.0, "in",   14, "Clipboard with checklist"),
    ("s3-q10-arrow-flowchart",      "extreme_close-up_of_a_hand__1b461d37", 5.0, "panR", 14, "Arrow drawn on flowchart"),
    ("s3-q11-three-boxes-diagram",  "top-down_view_of_a_hand-dra", 5.0, "in",   13, "Three boxes diagram"),
    ("s3-q12-corridor-side-angle",  "low_side-angle_view_of_a_lo", 5.0, "panR", 12, "Corridor side angle"),
    ("s3-q13-corridor-walk-away",   "a_single_silhouette_figure_", 7.0, "in",   13, "Silhouette walking down corridor"),
    ("s3-q14-three-glass-offices",  "exterior_view_through_three", 6.0, "out",  13, "Three glass-walled offices"),
    ("s3-q15-calculator-screen",    "extreme_close-up_of_a_black", 6.0, "in",   15, "Calculator screen close-up"),
    ("s3-q16-pen-midair",           "extreme_close-up_of_a_hand__719880b0", 5.0, "in", 14, "Pen mid-air about to sign"),
    ("s3-q17-end-of-day",           "wide_view_across_a_long_AU_", 4.0, "out",  12, "Dealership at end of day"),
]


def find_source(pattern):
    """Find the upscaled (2912x1632) PNG matching the pattern in Downloads."""
    candidates = list(DOWNLOADS.glob(f"audealermath_*{pattern}*.png"))
    # Filter to upscaled only — they have UUID + suffix structure (no _0/_1/_2/_3 grid suffix)
    upscaled = [c for c in candidates if not any(c.stem.endswith(f"_{i}") for i in range(4))]
    if not upscaled:
        return None
    # If multiple matches, pick the largest file (upscaled subtle vs creative)
    return max(upscaled, key=lambda p: p.stat().st_size)


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
print("AUDM V1 Rebuild — bake KB MP4s from MJ upscaled stills")
print("=" * 70)

baked = 0
skipped = 0
for slot_id, pattern, duration, direction, zoom_pct, comment in SLOTS:
    src = find_source(pattern)
    if not src:
        print(f"  [SKIP] {slot_id}: source not found (pattern: {pattern})")
        skipped += 1
        continue

    # Copy + rename source PNG to project folder
    dst_png = STILLS_OUT / f"{slot_id}.png"
    if not dst_png.exists() or dst_png.stat().st_mtime < src.stat().st_mtime:
        shutil.copy2(src, dst_png)

    # Bake KB MP4
    out_mp4 = KB_OUT / f"{slot_id}-kb.mp4"
    total_frames = int(duration * 24)
    vf = kb_filter(direction, zoom_pct, total_frames)
    cmd = [
        FFMPEG, "-y", "-loglevel", "error",
        "-loop", "1", "-i", str(dst_png),
        "-vf", vf,
        "-t", str(duration),
        "-c:v", "libx264", "-preset", "medium", "-crf", "18",
        "-pix_fmt", "yuv420p", "-r", "24", "-an",
        str(out_mp4),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        sz = out_mp4.stat().st_size // 1024
        print(f"  [OK]   {slot_id:35s} {duration:.1f}s {direction:5s} {zoom_pct}% ({sz}KB)")
        baked += 1
    else:
        print(f"  [FAIL] {slot_id}: {result.stderr.strip()[:200]}")
        skipped += 1

print(f"\nBaked: {baked} / {len(SLOTS)}, skipped: {skipped}")
print(f"\nOutput: {KB_OUT}")
print(f"Source PNGs: {STILLS_OUT}")
