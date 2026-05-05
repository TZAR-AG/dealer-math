"""Bake AUDM V3 (The Aftercare Room) KB-animated MP4s from the 63 MJ stills
in v03-renders/stills/v1/.

Pipeline position:
    MJ stills (63 PNGs, default MJ filenames, 2026-05-05 batch)
        -> THIS SCRIPT (categorize by filename keyword + bake KB MP4)
        -> motion/baked/kb-v3/<scene-slot-id>-kb.mp4
        -> build-v3-davinci.py imports each baked clip into DaVinci timeline

Categorization strategy:
    Each PNG filename starts with `audealermath_<truncated-prompt-prefix>_<uuid>.png`.
    The prefix (~50 chars after `audealermath_`) is the head of the V3-NNN prompt
    body. We map each prefix to a scene by keyword match against the V3 script
    structure (HOOK / AUTHORITY / MENU / MATH / WHY-HIGH / WHAT-TO-DO / SIGNOFF).

Distribution (sums to 63):
    Scene 1 HOOK:        4 stills, 27.92s,   prefix h
    Scene 2 AUTHORITY:   7 stills, 61.28s,   prefix a
    Scene 3 MENU:       11 stills, 109.02s,  prefix m
    Scene 4 MATH:       14 stills, 150.16s,  prefix t
    Scene 5 WHY-HIGH:   14 stills, 147.51s,  prefix w
    Scene 6 WHAT-TO-DO:  9 stills, 138.60s,  prefix d
    Scene 7 SIGNOFF:     4 stills, 48.96s,   prefix z

Per-scene slot durations are spread evenly within the scene.
Each MP4 is baked +0.10s longer than its slot for adjacency safety.
"""

import shutil
import subprocess
from pathlib import Path

REPO = Path(r"C:\dev\Claude")
RENDERS = REPO / "content" / "au-dealer-math" / "scripts" / "v03-renders"
STILLS_SRC = RENDERS / "stills" / "v1"            # 63 MJ stills (default filenames)
STILLS_OUT = RENDERS / "stills" / "auto-v3"       # renamed slot-id PNGs
KB_OUT = RENDERS / "motion" / "baked" / "kb-v3"   # baked KB MP4s
STILLS_OUT.mkdir(parents=True, exist_ok=True)
KB_OUT.mkdir(parents=True, exist_ok=True)

FFMPEG = r"C:\Users\adria\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1-full_build\bin\ffmpeg.exe"

FPS = 24

# --- Scene durations (master VO = 683.45s, fresh-render so scripted == actual) ---
SCENE_DURS = {
    1: 27.92,
    2: 61.28,
    3: 109.02,
    4: 150.16,
    5: 147.51,
    6: 138.60,
    7: 48.96,
}

# --- Categorization keywords per scene ---
# Match against the lower-cased filename. First scene to match wins.
# Order matters: more-specific scenes go first within each "natural home" cluster.
SCENE_KEYWORDS = {
    # Scene 1 HOOK — paint protection invoice + three doors + brochures-received hands
    1: [
        "glossy_mirror-finish_bonnet",     # V3-001 (paint hook)
        "three_fros",                       # V3-002 (three frosted doors hook)
    ],
    # Scene 2 AUTHORITY + three-room reanchor — glass-walled, showroom, AU exteriors
    2: [
        "glass-walled_office",              # V3-004
        "mid-wide_au_dealership_glas",      # V3-009 / V3-040 family
        "mid-wide_glass-fronted_au_d",      # V3-040 family
        "wide_documentary_photograph_from_showroom_floor",  # V3-009
        "top-down_architectural_still_photograph_three_fros",  # V3-002 (already)
        "top-down_architectural_still_photograph_polished_p",  # V3-006 / V3-053 doors restated
    ],
    # Scene 3 MENU — brochures, aftercare technician, salesperson hands, ceramic, tint, dash cam
    3: [
        "single_glossy_brochu",             # V3-011
        "three_glossy_brochur",             # V3-021 / V3-010 family
        "aftercare_technici",               # V3-059 (tint application)
        "salesperson_hands",                # V3-032 (brochure slid)
        "extreme_close-up_macro_of_a",      # V3-060 tint detail / macro brochure
    ],
    # Scene 4 MATH REVEAL — extreme macro top-down on dark grey laminate, calculator, alpine highlighter, splits
    4: [
        "extreme_macro_top-down_photograph_polished_dark_gr",  # V3-018, V3-022, V3-024
        "macro_photograph_low-angle_close-up_of_a_single_al",  # V3-016 alpine wheel/highlighter
        "extreme_macro_photograph_polished_dark_grey_lamina",  # V3-024
        "top-down_photograph_split_composition",               # V3-019 split
        "top-down_macro_photograph_polished_dark_grey_lamin",  # V3-013 / V3-015 macro
        "top-down_photograph_polished_dark_grey_laminate_of",  # V3-005, V3-010, V3-012, V3-014, V3-028
        "top-down_view_of_a_polished",                          # V3-029 stack contracts (math beat)
        "documentary_photograph_top-down_polished_dark_grey",   # generic top-down doc
        "top-down_polished_dark_grey",                          # generic top-down catch
    ],
    # Scene 5 WHY-HIGH — vehicles (Hilux/LandCruiser/Ranger), AU dealership ext/int, streetscape, flag, dusk room
    5: [
        "current-generation_toyota",        # V3-054 trade-in tease (current-gen sedan/SUV)
        "2024_ford_ranger_next-gen",        # V3-058
        "2024_toyota_land_cruiser_30",      # V3-057
        "mid-distance_three-quarter",       # V3-030 Hilux / V3-038 Tucson / V3-042 Camry
        "mid-distance_broad-shoulder",      # V3-007, V3-039 (man silhouette walking customer)
        "mid-wide_au_low-rise_commer",      # V3-041 streetscape
        "mid-wide_modern_au_independ",      # V3-046 detail shop
        "three-quarter_angle_of_a_du",      # V3-026 dual-monitor / vehicle three-quarter
        "three-quarter_angle_of_a_si",      # V3-037 single monitor
        "mid-wide_low-angle_single_a",      # V3-043 AU flag
        "wide_documentary_photograph_from_showroom_floor",  # V3-034 wide showroom (also S2)
        "three-quarter_top-down_view",      # V3-025 F&I workstation
        "documentary_photograph_extreme_close-up_macro_of_a",  # V3-060 tint macro
    ],
    # Scene 6 WHAT-TO-DO — F&I-adjacent computer, faceless customer, key fob, contract signature, atmospheric office
    6: [
        "mid-wide_angle_of_an_fi-adj",      # V3-026
        "mid-wide_faceless_customer",       # V3-050 walking out
        "cinema_verit_photograph_faceless_dealership_fi_fin",  # V3-044 dusk room
        "cropped_at_lap_height_facel",      # V3-035 tired hands on lap
        "extreme_macro_top-down_photograph_single_closed_gl",  # V3-061 key fob
        "documentary_photograph_top-down_view_of_a_polished",  # V3-029 contract stack (also S4)
    ],
    # Scene 7 SIGNOFF — atmospheric reset, dusk dealership, contract waiting, paint-protected close-up
    7: [
        "cinema_verit_photograph_current-generation_toyota",  # V3-054 wheel hand (close)
        "studio_documentary_photograph_top-down_composition", # V3-056 cheatsheet fan
        "top-down_split_composition",       # V3-019 (alt placement)
        "studio_documentary_photograph_top-down_polished_da", # V3-023 / V3-056 fan-out
    ],
}

# Fallback bucket for filenames that don't match any keyword cleanly
# (mostly "cropped_at_chest_height_fac..." stills — distribute across menu/math/what-to-do).
FALLBACK_DIST = [3, 4, 6, 4, 6, 3, 4, 6]  # rotation order — favours doc-heavy scenes


def categorize_stills():
    """Walk STILLS_SRC, assign each PNG to a scene via keyword match.
    Returns dict: scene_id (int) -> list[Path]"""
    by_scene = {sid: [] for sid in SCENE_DURS}
    fallback = []

    files = sorted(STILLS_SRC.glob("audealermath_*.png"))
    for f in files:
        lower = f.name.lower()
        matched = False
        for sid, kws in SCENE_KEYWORDS.items():
            for kw in kws:
                if kw in lower:
                    by_scene[sid].append(f)
                    matched = True
                    break
            if matched:
                break
        if not matched:
            fallback.append(f)

    # Rebalance to target distribution: [4, 7, 11, 14, 14, 9, 4]
    target = {1: 4, 2: 7, 3: 11, 4: 14, 5: 14, 6: 9, 7: 4}

    # Pass 1: spill over-allocated scenes into fallback
    for sid in [1, 2, 3, 4, 5, 6, 7]:
        if len(by_scene[sid]) > target[sid]:
            extras = by_scene[sid][target[sid]:]
            by_scene[sid] = by_scene[sid][:target[sid]]
            fallback.extend(extras)

    # Pass 2: fill under-allocated scenes from fallback
    fb_idx = 0
    for sid in [4, 5, 3, 6, 2, 7, 1]:  # priority — biggest/most-versatile scenes first
        while len(by_scene[sid]) < target[sid] and fb_idx < len(fallback):
            by_scene[sid].append(fallback[fb_idx])
            fb_idx += 1

    # Pass 3: any leftover fallbacks → distribute round-robin among scenes that
    # still have headroom against the natural-cap (target + 2)
    remaining = fallback[fb_idx:]
    rr_order = [3, 4, 5, 6, 2, 1, 7]
    for f in remaining:
        for sid in rr_order:
            if len(by_scene[sid]) < target[sid] + 2:
                by_scene[sid].append(f)
                break

    return by_scene


def kb_filter(direction, zoom_pct, total_frames):
    """ffmpeg zoompan filter (V2 pattern verbatim, 7680px lanczos pre-scale)."""
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


# Direction rotation (varies every cut, no two zoom-ins adjacent)
DIRECTIONS = ["panR", "in", "panD", "out", "panL", "in", "panU", "out"]

# Section-aware zoom intensity (V1 playbook):
#   Hook  14-17%   Authority 11-14%   Body 8-12%   Reveals 12-15%   CTA 12-14%
ZOOM_INTENSITY = {
    1: [16, 15, 17, 14],                           # HOOK higher zoom
    2: [13, 12, 14, 13, 12, 11, 13],               # AUTHORITY medium
    3: [10, 11, 10, 9, 11, 10, 9, 12, 10, 11, 10], # MENU body cadence
    4: [10, 11, 10, 9, 12, 10, 11, 9, 10, 11, 10, 9, 12, 11],   # MATH (most cuts, body)
    5: [11, 10, 12, 9, 11, 10, 12, 9, 11, 10, 11, 9, 12, 10],   # WHY (vehicle/exterior heavier zoom)
    6: [12, 11, 13, 10, 12, 11, 13, 10, 12],       # WHAT-TO-DO reveal cadence
    7: [13, 14, 13, 12],                           # SIGNOFF calm CTA
}


def build_slot_table(by_scene):
    """Construct (slot_id, src_path, duration, direction, zoom_pct, comment) tuples
    in build-script consumption order."""
    SCENE_PREFIX = {1: "h", 2: "a", 3: "m", 4: "t", 5: "w", 6: "d", 7: "z"}
    slots = []

    for sid in [1, 2, 3, 4, 5, 6, 7]:
        files = by_scene[sid]
        n = len(files)
        scene_dur = SCENE_DURS[sid]
        per_slot = scene_dur / n  # even spread within the scene

        for i, src_path in enumerate(files):
            prefix = SCENE_PREFIX[sid]
            slot_num = i + 1
            # Short descriptor extracted from MJ filename — between `audealermath_` and the UUID
            stem = src_path.stem
            mid = stem.replace("audealermath_", "").rsplit("_", 5)[0]  # drop 5-segment uuid
            mid = mid.lower().replace(" ", "_")[:24].rstrip("_-")
            slot_id = f"s{sid}-{prefix}{slot_num}-{mid}"

            direction = DIRECTIONS[(i + sid) % len(DIRECTIONS)]
            zoom_list = ZOOM_INTENSITY[sid]
            zoom_pct = zoom_list[i % len(zoom_list)]
            comment = f"Scene {sid} slot {slot_num}/{n} ({per_slot:.2f}s)"

            slots.append((slot_id, src_path, round(per_slot, 4), direction, zoom_pct, comment))

    return slots


def main():
    print("=" * 70)
    print("AUDM V3 (The Aftercare Room) — bake KB MP4s from MJ stills")
    print(f"Source dir: {STILLS_SRC}")
    print(f"Output dir: {KB_OUT}")
    print("=" * 70)

    by_scene = categorize_stills()
    total = sum(len(v) for v in by_scene.values())
    print(f"\nCategorization:")
    for sid in [1, 2, 3, 4, 5, 6, 7]:
        print(f"  Scene {sid} ({SCENE_DURS[sid]:6.2f}s): {len(by_scene[sid])} stills")
    print(f"  TOTAL: {total} stills")
    if total != 63:
        print(f"  [warn] expected 63, got {total}")

    slots = build_slot_table(by_scene)
    print(f"\nBuilt {len(slots)} slot definitions.\n")

    baked = 0
    skipped = 0
    total_dur = 0.0

    # Emit a manifest the build script can import (slot_id, scene, filename order)
    manifest_path = KB_OUT / "_manifest.txt"
    manifest_lines = []

    for slot_id, src_path, duration, direction, zoom_pct, comment in slots:
        if not src_path.exists():
            print(f"  [SKIP] {slot_id}: source not found: {src_path}")
            skipped += 1
            continue

        # Copy + rename source PNG to traceable slot-id name
        dst_png = STILLS_OUT / f"{slot_id}.png"
        if not dst_png.exists() or dst_png.stat().st_mtime < src_path.stat().st_mtime:
            shutil.copy2(src_path, dst_png)

        # Bake +0.10s longer than the slot to absorb 1-frame rounding
        bake_dur = duration + 0.10
        out_mp4 = KB_OUT / f"{slot_id}-kb.mp4"
        total_frames = int(bake_dur * FPS)
        vf = kb_filter(direction, zoom_pct, total_frames)

        cmd = [
            FFMPEG, "-y", "-loglevel", "error",
            "-loop", "1", "-i", str(dst_png),
            "-vf", vf,
            "-t", str(bake_dur),
            "-c:v", "libx264", "-preset", "medium", "-crf", "18",
            "-pix_fmt", "yuv420p", "-r", str(FPS), "-an",
            str(out_mp4),
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            sz = out_mp4.stat().st_size // 1024
            total_dur += duration
            print(f"  [OK]   {slot_id:48s} {duration:5.2f}s {direction:5s} {zoom_pct:>2}% ({sz:>5d}KB)")
            baked += 1
            manifest_lines.append(f"{slot_id}\t{duration:.4f}\t{src_path.name}")
        else:
            print(f"  [FAIL] {slot_id}: {result.stderr.strip()[:200]}")
            skipped += 1

    manifest_path.write_text("\n".join(manifest_lines) + "\n", encoding="utf-8")
    print(f"\nManifest: {manifest_path}")
    print(f"Baked: {baked} / {len(slots)}, skipped: {skipped}")
    print(f"Total visual-track duration: {total_dur:.2f}s (target master VO: 683.45s)")
    print(f"\nOutput KB clips: {KB_OUT}")
    print(f"Source PNGs (slot-id renamed): {STILLS_OUT}")


if __name__ == "__main__":
    main()
