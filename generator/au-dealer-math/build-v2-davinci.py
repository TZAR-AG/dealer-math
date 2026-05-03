# AU Dealer Math V2 (Finance Manager's Office) — DaVinci Resolve auto-build script
#
# Assembles V2 timeline:
#   - Master VO (acrossfade-blended, 528.08s) on audio track 1, single placement
#   - Music bed on audio track 2 (a-hand-in-the-dark-looped-ducked, 528s — YT Audio Library)
#   - 53 visual entries on video track 1 (50 unique stills + 3 motif callbacks)
#   - All visuals are pre-baked KB MP4s (ffmpeg zoompan) — DaVinci just places them
#
# Frame-accurate adjacency, no-adjacent-same-image rule satisfied.
#
# RUN INSIDE DaVinci Resolve 20 Py3 Console (use the standard load pattern):
#   exec( open(r"C:\dev\Claude\generator\au-dealer-math\build-v2-davinci.py").read() )

from pathlib import Path

REPO = Path(r"C:\dev\Claude")
RENDERS = REPO / "content" / "au-dealer-math" / "scripts" / "v02-renders"

PROJECT_NAME = "AUDM_V2_FinanceManagersOffice"
TIMELINE_NAME = "V2_main"
WIDTH, HEIGHT = 1920, 1080
FPS = 24

MUSIC_FILES = [
    # Pre-baked at -8dB on top of original duck (mean -46.2dB / max -32.8dB).
    # Loop-extended to 581.90s to match LOCKED-Macca V2 timeline (post-sign-off
    # update 2026-05-03 — added like+subscribe CTA, +3.30s on S7).
    # Source: Underbelly & Ty Mayer "A Hand In The Dark" (YT Audio Library, zero CID risk).
    "a-hand-in-the-dark-looped-ducked-soft-578s-v3.mp3",
]
MUSIC_DIR_REL = "music"

# Strategic dollar/rate overlay PNGs on V2 (upper-third, above main video).
# Timestamps locked via Whisper word-level transcription of the master VO
# (see vo-transcriptions.json). Format: (start_sec, duration_sec, fname).
# PNGs generated via generator/au-dealer-math/generate-overlays-v2.py.
OVERLAYS = [
    # Hook — finance rate visual sets the scene as Macca opens
    (1.0,    4.0, "01-hook-9-percent.png"),       # FINANCE RATE: 9.00%
    # Rate Range Game (S4) — the spread mechanic. Timestamps refreshed against
    # the post-stutter-fix transcription 2026-05-03.
    (188.5,  3.5, "02-bank-5-percent.png"),        # "approved you at 5%" @188.88
    (205.8,  3.5, "03-dealer-9-percent.png"),      # "written at 9%" @206.30
    (241.5,  4.0, "04-spread-cost.png"),           # "cost on your side" @242.10
    # Commission Pool (S5) — the income mechanic
    (323.0,  3.5, "05-commission-pool.png"),       # "10 to 15" @323.53
    # The Fix (S6) — the customer move
    (444.5,  4.0, "06-ask-floor-rate.png"),        # "ask this" @445.12
    # V3 Tease (S7) — aftercare cost preview
    (543.5,  4.0, "07-aftercare-tease.png"),       # "1,500" @544.38
]
OVERLAY_DIR_REL = "overlays"

# Per-scene durations adjusted for 0.20s acrossfade compression (per
# reference_audm_video_production_pipeline.md):
#   - Boundary scenes (S1, S7) lose 0.10s (one half of one crossfade)
#   - Middle scenes (S2-S6) lose 0.20s (full crossfade trailing)
# Sum of actual_dur values = 528.08s = master VO duration (verified ffprobe).
# scripted_dur = OLD coordinate (V2 first-build at Speed 0.95 / Stability 0.55).
# actual_dur   = NEW VO renders at LOCKED Macca (Speed 0.90 / Stability 0.40, 2026-05-03).
# scale_to_actual() proportionally re-times VISUAL_TRACK entries so visuals
# stay anchored to their narrative beats even though the VO got ~9.5% longer.
SCENES = [
    {"id": 1, "name": "hook",       "scripted_dur": 16.20, "actual_dur": 14.62, "vo": "vo-scene-1-hook.mp3"},
    {"id": 2, "name": "authority",  "scripted_dur": 47.12, "actual_dur": 50.65, "vo": "vo-scene-2-authority.mp3"},
    {"id": 3, "name": "fnioffice",  "scripted_dur": 100.62,"actual_dur": 111.02,"vo": "vo-scene-3-fnioffice.mp3"},
    {"id": 4, "name": "rateGame",   "scripted_dur": 116.88,"actual_dur": 130.57,"vo": "vo-scene-4-rate-game.mp3"},
    {"id": 5, "name": "commission", "scripted_dur": 105.87,"actual_dur": 111.67,"vo": "vo-scene-5-commission.mp3"},
    {"id": 6, "name": "fix",        "scripted_dur": 95.51, "actual_dur": 104.29,"vo": "vo-scene-6-fix.mp3"},
    {"id": 7, "name": "signoff",    "scripted_dur": 45.88, "actual_dur": 55.02, "vo": "vo-scene-7-signoff.mp3"},
]

MASTER_VO_FILE = "voice/master-vo.mp3"
MASTER_VO_DUR = 577.8592  # ffprobed 2026-05-03 — script edited for stutter (em-dashes/quotes/lists fixed)
VO_GAP_SEC = 0.0


def _compute_starts():
    scripted = [0.0]
    visual = [0.0]
    vo = [0.0]
    for i, s in enumerate(SCENES):
        scripted.append(scripted[-1] + s["scripted_dur"])
        visual.append(visual[-1] + s["actual_dur"])
        trailing_gap = VO_GAP_SEC if i < len(SCENES) - 1 else 0
        vo.append(vo[-1] + s["actual_dur"] + trailing_gap)
    return scripted, visual, vo


SCRIPTED_STARTS, VISUAL_STARTS, VO_STARTS = _compute_starts()
ACTUAL_STARTS = VISUAL_STARTS
TOTAL_RUNTIME = VO_STARTS[-1]


# 53 visual placements across 50 unique stills (3 motif callbacks).
# All entries are "still_kb" — pre-baked KB MP4s from bake-v2-finance-managers-stills.py.
# No-adjacent-same-image rule verified: all consecutive cuts use different source UUIDs.
VISUAL_TRACK = [
    # === SCENE 1 — HOOK (0.00 → 16.20s, 5 cuts) ==============================
    (0.00,    3.50,  "motion/baked/kb-v2/s1-h1-cream-contract-kb.mp4",          "still_kb"),
    (3.50,    6.50,  "motion/baked/kb-v2/s1-h2-orange-band-rescue-kb.mp4",      "still_kb"),
    (6.50,    9.80,  "motion/baked/kb-v2/s1-h3-hand-pointing-kb.mp4",           "still_kb"),
    (9.80,   12.80,  "motion/baked/kb-v2/s1-h4-black-close-kb.mp4",             "still_kb"),
    (12.80,  16.20,  "motion/baked/kb-v2/s1-h5-chiaroscuro-kb.mp4",             "still_kb"),

    # === SCENE 2 — AUTHORITY (16.20 → 63.32s, 7 cuts) ========================
    (16.20,  22.20,  "motion/baked/kb-v2/s2-a1-aerial-1-kb.mp4",                "still_kb"),
    (22.20,  28.20,  "motion/baked/kb-v2/s2-a2-aerial-2-kb.mp4",                "still_kb"),
    (28.20,  35.30,  "motion/baked/kb-v2/s2-a3-frontal-symmetric-kb.mp4",       "still_kb"),
    (35.30,  42.30,  "motion/baked/kb-v2/s2-a4-low-wide-along-kb.mp4",          "still_kb"),
    (42.30,  49.30,  "motion/baked/kb-v2/s2-a5-low-angle-up-kb.mp4",            "still_kb"),
    (49.30,  56.30,  "motion/baked/kb-v2/s2-a6-eye-street-kb.mp4",              "still_kb"),
    (56.30,  63.32,  "motion/baked/kb-v2/s2-a7-low-wide-across-kb.mp4",         "still_kb"),

    # === SCENE 3 — F&I OFFICE (63.32 → 163.94s, 9 cuts) ======================
    (63.32,  70.70,  "motion/baked/kb-v2/s3-f1-wide-two-chairs-kb.mp4",         "still_kb"),
    (70.70,  80.70,  "motion/baked/kb-v2/s3-f2-modern-topdown-kb.mp4",          "still_kb"),
    (80.70,  90.70,  "motion/baked/kb-v2/s3-f3-modern-desk-kb.mp4",             "still_kb"),
    (90.70, 100.70,  "motion/baked/kb-v2/s3-f4-hand-close-1-kb.mp4",            "still_kb"),
    (100.70,111.70,  "motion/baked/kb-v2/s3-f5-clean-modern-kb.mp4",            "still_kb"),
    (111.70,123.70,  "motion/baked/kb-v2/s3-f6-wide-modern-1-kb.mp4",           "still_kb"),
    (123.70,134.70,  "motion/baked/kb-v2/s3-f7-hand-close-2-kb.mp4",            "still_kb"),
    (134.70,147.70,  "motion/baked/kb-v2/s3-f8-wide-modern-2-kb.mp4",           "still_kb"),
    (147.70,163.94,  "motion/baked/kb-v2/s3-f9-interior-au-1-kb.mp4",           "still_kb"),

    # === SCENE 4 — RATE RANGE (163.94 → 280.82s, 10 cuts) ====================
    (163.94,171.50,  "motion/baked/kb-v2/s4-r1-interior-au-2-kb.mp4",           "still_kb"),
    (171.50,183.50,  "motion/baked/kb-v2/s4-r2-cinema-hand-kb.mp4",             "still_kb"),
    (183.50,193.50,  "motion/baked/kb-v2/s4-r3-hand-close-3-kb.mp4",            "still_kb"),
    (193.50,204.50,  "motion/baked/kb-v2/s4-r4-hand-close-4-kb.mp4",            "still_kb"),
    (204.50,216.50,  "motion/baked/kb-v2/s4-r5-plain-cream-1-kb.mp4",           "still_kb"),
    (216.50,228.50,  "motion/baked/kb-v2/s4-r6-directly-overhead-kb.mp4",       "still_kb"),
    (228.50,240.50,  "motion/baked/kb-v2/s4-r7-male-hand-kb.mp4",               "still_kb"),
    (240.50,252.50,  "motion/baked/kb-v2/s4-r8-ink-macro-kb.mp4",               "still_kb"),
    (252.50,265.50,  "motion/baked/kb-v2/s4-r9-medium-wide-kb.mp4",             "still_kb"),
    (265.50,280.82,  "motion/baked/kb-v2/s4-r10-pen-close-rescue-kb.mp4",       "still_kb"),

    # === SCENE 5 — COMMISSION POOL (280.82 → 386.69s, 9 cuts) ================
    (280.82,290.30,  "motion/baked/kb-v2/s5-c1-printed-rescue-kb.mp4",          "still_kb"),
    (290.30,301.30,  "motion/baked/kb-v2/s5-c2-hand-close-reuse-kb.mp4",        "still_kb"),
    (301.30,312.30,  "motion/baked/kb-v2/s5-c3-hand-holding-1-kb.mp4",          "still_kb"),
    (312.30,324.30,  "motion/baked/kb-v2/s5-c4-hand-holding-2-kb.mp4",          "still_kb"),
    (324.30,336.30,  "motion/baked/kb-v2/s5-c5-low-side-close-kb.mp4",          "still_kb"),
    (336.30,349.30,  "motion/baked/kb-v2/s5-c6-hand-close-5-kb.mp4",            "still_kb"),
    (349.30,361.30,  "motion/baked/kb-v2/s5-c7-au-vehicle-1-kb.mp4",            "still_kb"),
    (361.30,375.30,  "motion/baked/kb-v2/s5-c8-au-vehicle-2-kb.mp4",            "still_kb"),
    (375.30,386.69,  "motion/baked/kb-v2/s5-c9-au-vehicle-3-kb.mp4",            "still_kb"),

    # === SCENE 6 — FIX (386.69 → 482.20s, 9 cuts) ============================
    (386.69,396.00,  "motion/baked/kb-v2/s6-x1-plain-cream-2-kb.mp4",           "still_kb"),
    (396.00,405.00,  "motion/baked/kb-v2/s6-x2-rear-shoulders-kb.mp4",          "still_kb"),
    (405.00,414.00,  "motion/baked/kb-v2/s6-x3-pov-from-seat-kb.mp4",           "still_kb"),
    (414.00,424.00,  "motion/baked/kb-v2/s6-x4-studio-interior-1-kb.mp4",       "still_kb"),
    (424.00,434.00,  "motion/baked/kb-v2/s6-x5-studio-interior-2-kb.mp4",       "still_kb"),
    (434.00,445.00,  "motion/baked/kb-v2/s6-x6-side-angle-charcoal-kb.mp4",     "still_kb"),
    (445.00,456.00,  "motion/baked/kb-v2/s6-x7-vehicle-wide-1-kb.mp4",          "still_kb"),
    (456.00,469.00,  "motion/baked/kb-v2/s6-x8-vehicle-wide-2-kb.mp4",          "still_kb"),
    (469.00,482.20,  "motion/baked/kb-v2/s6-x9-studio-dramatic-kb.mp4",         "still_kb"),

    # === SCENE 7 — SIGNOFF (482.20 → 528.08s, 4 cuts, calm CTA) ==============
    (482.20,492.50,  "motion/baked/kb-v2/s7-z1-studio-wide-au-kb.mp4",          "still_kb"),
    (492.50,506.50,  "motion/baked/kb-v2/s7-z2-rear-vehicle-kb.mp4",            "still_kb"),
    (506.50,520.50,  "motion/baked/kb-v2/s7-z3-chiaroscuro-reuse-kb.mp4",       "still_kb"),
    (520.50,528.08,  "motion/baked/kb-v2/s7-z4-cream-contract-reuse-kb.mp4",    "still_kb"),
]


# V2 v1 has no Kling/MJ motion clips with tpad-extended durations.
# All entries above are baked KB stills; every clip is exactly slot_dur+0.10s on disk.
BAKED_MOTION_DURATIONS = {}


# ============================================================
# HELPERS
# ============================================================

def sec_to_frame(sec, fps=FPS):
    return int(round(sec * fps))


def find_clip_in_pool(media_pool, filename):
    return _walk_for_clip(media_pool.GetRootFolder(), filename)


def _walk_for_clip(folder, filename):
    for clip in folder.GetClipList() or []:
        if clip.GetClipProperty("File Name") == filename:
            return clip
    for sub in folder.GetSubFolderList() or []:
        found = _walk_for_clip(sub, filename)
        if found:
            return found
    return None


def find_scene(scripted_sec):
    for i in range(len(SCENES)):
        if SCRIPTED_STARTS[i] <= scripted_sec < SCRIPTED_STARTS[i + 1]:
            return i
    return len(SCENES) - 1


def scale_to_actual(scripted_sec, scene_idx):
    scene = SCENES[scene_idx]
    in_scene = scripted_sec - SCRIPTED_STARTS[scene_idx]
    scale = scene["actual_dur"] / scene["scripted_dur"]
    return ACTUAL_STARTS[scene_idx] + in_scene * scale


def compute_scaled_track():
    """V2 v1: scripted_dur = actual_dur for all scenes, so this is a passthrough.
    Kept for forward-compat if/when motion clips with tpad get re-introduced."""
    scaled = []
    for entry in VISUAL_TRACK:
        scripted_start, scripted_end, asset, ctype = entry
        scene_idx = find_scene(scripted_start)
        new_start = scale_to_actual(scripted_start, scene_idx)
        new_end = scale_to_actual(scripted_end, scene_idx)
        scaled.append([new_start, new_end, asset, ctype])

    # Motion-baked-shorter-than-slot absorption (no-op in V2 v1 since
    # BAKED_MOTION_DURATIONS is empty)
    for i in range(len(scaled) - 1):
        start, end, asset, ctype = scaled[i]
        if ctype != "motion":
            continue
        baked = BAKED_MOTION_DURATIONS.get(Path(asset).name)
        if baked is None:
            continue
        scaled_dur = end - start
        if baked < scaled_dur - 0.01:
            actual_motion_end = start + baked
            scaled[i][1] = actual_motion_end
            scaled[i + 1][0] = actual_motion_end

    return [tuple(e) for e in scaled]


# ============================================================
# CONNECT TO RESOLVE
# ============================================================

print("=" * 60)
print("AUDM V2 (Finance Manager's Office) — DaVinci auto-build")
print("=" * 60)

if 'resolve' not in dir():
    raise RuntimeError("'resolve' global not found. Run inside DaVinci Resolve Py3 Console.")

pm = resolve.GetProjectManager()
print(f"Resolve: {resolve.GetProductName()} {resolve.GetVersionString()}")

project = pm.LoadProject(PROJECT_NAME) or pm.CreateProject(PROJECT_NAME)
if not project:
    raise RuntimeError(f"Could not create/load project {PROJECT_NAME}")
print(f"Project: {project.GetName()}")

project.SetSetting("timelineResolutionWidth", str(WIDTH))
project.SetSetting("timelineResolutionHeight", str(HEIGHT))
project.SetSetting("timelineFrameRate", str(FPS))
project.SetSetting("timelinePlaybackFrameRate", str(FPS))
print(f"Project resolution: {WIDTH}x{HEIGHT} @ {FPS}fps")

mp = project.GetMediaPool()

scaled_track = compute_scaled_track()
print(f"\nScene timing (scripted -> actual):")
for i, s in enumerate(SCENES):
    drift = ACTUAL_STARTS[i] - SCRIPTED_STARTS[i]
    print(f"  Scene {s['id']} {s['name']:10s} {SCRIPTED_STARTS[i]:6.2f}s -> {ACTUAL_STARTS[i]:6.2f}s "
          f"(scripted {s['scripted_dur']:.2f}s, actual {s['actual_dur']:.2f}s, drift {drift:+.2f}s)")
print(f"  Total runtime: {TOTAL_RUNTIME:.2f}s ({TOTAL_RUNTIME/60:.1f}min)")

all_paths = []
missing = []

master_vo_path = RENDERS / MASTER_VO_FILE
if master_vo_path.exists():
    all_paths.append(str(master_vo_path))
else:
    missing.append(str(master_vo_path))

for entry in scaled_track:
    if entry[2] is None:
        continue
    p = RENDERS / entry[2]
    (all_paths if p.exists() else missing).append(str(p))

print(f"\nMusic bed:")
for m in MUSIC_FILES:
    p = RENDERS / MUSIC_DIR_REL / m
    if p.exists():
        all_paths.append(str(p))
        print(f"  {m}")
    else:
        print(f"  [warn] missing: {p}")

print(f"\nDollar-figure overlays:")
if not OVERLAYS:
    print(f"  (none — V2 v1 ships caption-only)")
for _, _, fname in OVERLAYS:
    p = RENDERS / OVERLAY_DIR_REL / fname
    if p.exists():
        all_paths.append(str(p))
        print(f"  {fname}")
    else:
        print(f"  [warn] missing: {p}")

if missing:
    print(f"\n[warn] {len(missing)} assets missing:")
    for m in missing[:8]:
        print(f"   {m}")
    if len(missing) > 8:
        print(f"   ... and {len(missing) - 8} more")

all_paths = list(dict.fromkeys(all_paths))

# CRITICAL — order matters here. To force fresh re-import of media (which
# defeats DaVinci's filename-dedupe cache that keeps stale duration metadata),
# we must:
#   1. Delete any existing timeline that references the cached clips
#   2. Then DeleteClips on cached media-pool entries
#   3. Then ImportMedia for fresh
# DeleteClips silently FAILS if a clip is referenced by an active timeline, so
# step 1 must happen before step 2. Caught V2 2026-05-03 — voice cut at 8:45.

# Step 1: Delete old timeline (frees clip references)
for i in range(1, project.GetTimelineCount() + 1):
    tl = project.GetTimelineByIndex(i)
    if tl and tl.GetName() == TIMELINE_NAME:
        print(f"\nDeleting existing timeline (must precede media-pool nuke): {TIMELINE_NAME}")
        mp.DeleteTimelines([tl])
        break

# Step 2: Nuke any media-pool clips with names matching files we're about to
# import. Without this, DaVinci silently keeps stale metadata (e.g. old VO
# duration after a regen) and our explicit endFrame gets clipped to it.
import_filenames = {Path(p).name for p in all_paths}
existing = []
def _collect_existing(folder):
    for clip in folder.GetClipList() or []:
        if clip.GetClipProperty("File Name") in import_filenames:
            existing.append(clip)
    for sub in folder.GetSubFolderList() or []:
        _collect_existing(sub)
_collect_existing(mp.GetRootFolder())
if existing:
    print(f"Nuking {len(existing)} cached media-pool clips (force fresh re-import)...")
    delete_result = mp.DeleteClips(existing)
    print(f"  DeleteClips returned: {delete_result}")

# Step 3: Fresh import — DaVinci now reads actual file metadata, not cache
print(f"\nImporting {len(all_paths)} media files...")
imported = mp.ImportMedia(all_paths)
print(f"Imported {len(imported) if imported else 0} clips into media pool")

DEFAULT_STILL_FRAMES = 120
for entry in scaled_track:
    if entry[3] != "still_freeze":
        continue
    test = find_clip_in_pool(mp, Path(entry[2]).name)
    if not test:
        continue
    dur_tc = test.GetClipProperty("Duration")
    if dur_tc and ":" in dur_tc:
        parts = dur_tc.split(":")
        if len(parts) == 4:
            try:
                h, mi, s, f = [int(x) for x in parts]
                detected = (h * 3600 + mi * 60 + s) * FPS + f
                if detected > 1:
                    DEFAULT_STILL_FRAMES = detected
                    break
            except ValueError:
                pass
print(f"Default still source duration: {DEFAULT_STILL_FRAMES} frames ({DEFAULT_STILL_FRAMES / FPS:.1f}s)")

# (Old timeline already deleted above, before media-pool nuke + import.)
timeline = mp.CreateEmptyTimeline(TIMELINE_NAME)
if not timeline:
    raise RuntimeError(f"Could not create timeline {TIMELINE_NAME}")
project.SetCurrentTimeline(timeline)
timeline.SetStartTimecode("00:00:00:00")
TL_START = timeline.GetStartFrame()
print(f"Timeline: {TIMELINE_NAME} (start frame {TL_START}, TC 00:00:00:00)")

audio_count = timeline.GetTrackCount("audio")
while audio_count < 2:
    if not timeline.AddTrack("audio", "stereo"):
        break
    audio_count = timeline.GetTrackCount("audio")
print(f"Audio tracks: {audio_count}")

video_count = timeline.GetTrackCount("video")
while video_count < 2:
    if not timeline.AddTrack("video"):
        break
    video_count = timeline.GetTrackCount("video")
print(f"Video tracks: {video_count}")

print(f"\nPlacing master VO ({MASTER_VO_DUR:.2f}s -- single clip with crossfaded scene boundaries)...")
master_vo_clip = find_clip_in_pool(mp, Path(MASTER_VO_FILE).name)
if master_vo_clip:
    # CRITICAL: explicit startFrame=0 + endFrame=MASTER_VO_DUR forces DaVinci to use
    # the script-declared duration, NOT whatever was cached in media pool from a
    # prior import. Without this, re-imported VOs play their old cached length and
    # the audio cuts short of the visual track. Caught 2026-05-03 after V2 audio
    # ended at 8:45 instead of 9:38.
    vo_end_frame = sec_to_frame(MASTER_VO_DUR)
    info = {
        "mediaPoolItem": master_vo_clip,
        "startFrame": 0,
        "endFrame": vo_end_frame,
        "trackIndex": 1,
        "recordFrame": TL_START,
    }
    if mp.AppendToTimeline([info]):
        print(f"  [vo] master-vo @ 0.00s ({MASTER_VO_DUR:.2f}s, {vo_end_frame}fr)")
    else:
        print(f"  [fail] master VO placement")
else:
    print(f"  [fail] master VO not in pool -- run build-master-vo-v02.py first")

print(f"\nPlacing music bed on track 2...")
music_cursor_sec = 0.0
music_remaining = TOTAL_RUNTIME
for music_file in MUSIC_FILES:
    if music_remaining <= 0.05:
        print(f"  [skip] {music_file} (timeline full)")
        continue
    music_clip = find_clip_in_pool(mp, music_file)
    if not music_clip:
        print(f"  [skip] {music_file} not in pool")
        continue
    dur_tc = music_clip.GetClipProperty("Duration")
    if not dur_tc or ":" not in dur_tc:
        print(f"  [skip] could not read duration for {music_file}")
        continue
    parts = dur_tc.split(":")
    h, mi, s, f = [int(x) for x in parts]
    track_frames = (h * 3600 + mi * 60 + s) * FPS + f
    place_frames = min(track_frames, sec_to_frame(music_remaining))
    info = {
        "mediaPoolItem": music_clip,
        "startFrame": 0,
        "endFrame": place_frames,
        "trackIndex": 2,
        "recordFrame": TL_START + sec_to_frame(music_cursor_sec),
    }
    if mp.AppendToTimeline([info]):
        used_sec = place_frames / FPS
        print(f"  [music] {music_file} @ {music_cursor_sec:6.2f}s ({used_sec:.2f}s)")
        music_cursor_sec += used_sec
        music_remaining -= used_sec
    else:
        print(f"  [fail] could not place {music_file}")

if OVERLAYS:
    print(f"\nPlacing {len(OVERLAYS)} overlays on V2...")
    for start_sec, dur_sec, fname in OVERLAYS:
        clip = find_clip_in_pool(mp, fname)
        if not clip:
            print(f"  [skip] {fname} not in pool")
            continue
        info = {
            "mediaPoolItem": clip,
            "startFrame": 0,
            "endFrame": sec_to_frame(dur_sec),
            "trackIndex": 2,
            "recordFrame": TL_START + sec_to_frame(start_sec),
        }
        if mp.AppendToTimeline([info]):
            print(f"  [overlay] {fname} @ {start_sec:6.2f}s ({dur_sec:.1f}s)")
        else:
            print(f"  [fail] could not place {fname}")

print("\nPlacing visuals...")
placed = 0
fail = 0
freeze_chunks = 0
for entry in scaled_track:
    new_start, new_end, asset_path, clip_type = entry
    if asset_path is None:
        continue

    filename = Path(asset_path).name
    clip = find_clip_in_pool(mp, filename)
    if not clip:
        print(f"  [skip] not in pool: {filename}")
        fail += 1
        continue

    # Frame-accurate adjacency (frame indices THEN diff, not rounded diff)
    end_frame = sec_to_frame(new_end)
    start_frame = sec_to_frame(new_start)
    target_frames = end_frame - start_frame
    timeline_start = TL_START + start_frame

    if clip_type in ("motion", "still_kb"):
        info = {
            "mediaPoolItem": clip,
            "startFrame": 0,
            "endFrame": target_frames,
            "trackIndex": 1,
            "recordFrame": timeline_start,
        }
        if mp.AppendToTimeline([info]):
            placed += 1
        else:
            print(f"  [fail] {clip_type} {filename} @ {new_start:.2f}s ({target_frames}fr)")
            fail += 1
    else:
        chunk_size = max(2, DEFAULT_STILL_FRAMES)
        cursor = timeline_start
        remaining = target_frames
        success = True
        while remaining >= 1:
            chunk = min(chunk_size, remaining)
            info = {
                "mediaPoolItem": clip,
                "startFrame": 0,
                "endFrame": chunk,
                "trackIndex": 1,
                "recordFrame": cursor,
            }
            if mp.AppendToTimeline([info]):
                cursor += chunk
                remaining -= chunk
                freeze_chunks += 1
            else:
                print(f"  [fail] still_freeze loop {filename} @ frame {cursor} (chunk={chunk})")
                success = False
                break
        if success:
            placed += 1
        else:
            fail += 1

print(f"\n{placed} placed ({freeze_chunks} freeze chunks), {fail} failed")

print("\n" + "=" * 60)
print("BUILD COMPLETE")
print("=" * 60)
print(f"Project: {project.GetName()}")
print(f"Timeline: {timeline.GetName()}")
print(f"Resolution: {WIDTH}x{HEIGHT} @ {FPS}fps")
print(f"Total runtime: {TOTAL_RUNTIME:.2f} sec ({int(TOTAL_RUNTIME/60)}:{int(TOTAL_RUNTIME%60):02d})")
print(f"VO: master-vo.mp3 (single clip, 6 acrossfade boundaries) on audio track 1")
print(f"Music bed: track 2")
print(f"Visual entries placed: {placed} / {len(scaled_track)} on video track 1")
print()
print("NEXT STEPS:")
print("  1. Edit page -> Shift+Z (zoom to fit) -> Home -> Spacebar (play through)")
print("  2. Adjust music volume in Inspector (target -22 to -26 dB under VO)")
print("  3. If playback chokes, Playback -> Render Cache -> Smart")
print("  4. Run render-v2-davinci.py to export 1080p MP4 to video/out/")
print("  5. Then: python generator/au-dealer-math/transcribe-vos-v02.py")
print("  6. Then: python generator/au-dealer-math/render-vN-captions.py 2")
print()
