# AU Dealer Math V1 - DaVinci Resolve auto-build script (Phase 1 + 2)
#
# Assembles V1 timeline from manifest. Phase 1+2 features:
#   - VOs placed back-to-back at their actual cumulative durations (no gaps)
#   - Visual track re-timed per scene to match actual VO durations
#   - Motion clips pre-baked (ffmpeg tpad) to fixed slot durations
#   - Stills replaced with Ken Burns videos (ffmpeg zoompan) at slot durations
#   - Post-motion auto-stills (PNG of motion's last frame) for smooth transitions
#   - Music bed on audio track 2 (placed from Downloads, full timeline length)
#
# Pre-bake helpers:
#   - generator/au-dealer-math/bake-motion-clips.sh — ffmpeg tpad for motion extension
#   - (Ken Burns videos are baked ad-hoc; see comments below for the ffmpeg cmd)
#
# RUN INSIDE DaVinci Resolve 20 Py3 Console:
#   exec(open(r"C:\dev\Claude\generator\au-dealer-math\build-v1-davinci.py").read())

from pathlib import Path

# ============================================================
# CONFIGURATION
# ============================================================

REPO = Path(r"C:\dev\Claude")
RENDERS = REPO / "content" / "au-dealer-math" / "scripts" / "v01-renders"
DOWNLOADS = Path.home() / "Downloads"

PROJECT_NAME = "AUDM_V1_PaymentNotPrice"
TIMELINE_NAME = "V1_main"
WIDTH, HEIGHT = 1920, 1080
FPS = 24

# Music bed: single looped track, pre-ducked + softened (-8dB extra reduction).
# Pre-processed via ffmpeg to cover full V1 duration (587.18s exact match).
# Levels: mean -44.8dB / max -32.2dB — sits well under VO without overpowering.
# Source: YT Audio Library (Underbelly & Ty Mayer — "Wide Boys"). CID-safe.
# Inspector adjustment in DaVinci no longer required — file is bake-ready.
MUSIC_FILES = [
    "wide-boys-looped-ducked-soft.mp3",
]
MUSIC_DIR_REL = "music"  # relative to RENDERS

# Dollar-figure text overlays on V2 (upper-third, above main video).
# Timestamps locked via Whisper word-level transcription of the actual VO mp3s
# (see generator/au-dealer-math/transcribe-vos.py + vo-transcriptions.json).
# Format: (start_sec, duration_sec, overlay_filename)
OVERLAYS = [
    # FINAL 2026-04-30: positions shifted to match master VO crossfade output.
    # Mac's word at original time T (in untrimmed VO) plays in master at
    # T - (scene_idx - 1) * 0.2s. Scene S4 -> -0.6s shift, S5 -> -0.8s.
    # Hook: "$300/WEEK" appears as Mac asks "what's your weekly budget?"
    (2.5,      4.0,  "01-hook-300-week.png"),       # S1 (no shift)
    # Loan trick math (scene 4):
    (169.5,    3.0,  "02-four-years.png"),           # "300 a week over four years"
    (173.5,    3.0,  "03-seven-years.png"),          # "300 a week over seven years"
    (178.0,    3.5,  "04-46k-more.png"),             # "$46,000 more out of your pocket"
    # Aftercare math (scene 5):
    (362.2,    3.0,  "05-aftercare-retail.png"),     # "fifteen hundred to three thousand"
    (368.9,    2.5,  "06-aftercare-cost.png"),       # "up to five hundred"
    (370.6,    3.5,  "07-aftercare-gross.png"),      # "one-thousand to twenty-five-hundred dollar gross"
]
OVERLAY_DIR_REL = "overlays"  # relative to RENDERS

# ============================================================
# SCENE TIMINGS — actual VO durations (probed via ffprobe 2026-04-30 after re-render)
# Plus scripted target duration so we can scale visuals proportionally.
# Scenes are placed back-to-back starting at 0; actual_start computed dynamically.
# ============================================================

SCENES = [
    # FINAL 2026-04-30: VOs concatenated into ONE master file via ffmpeg
    # acrossfade chain (200ms crossfades, tri curve). Each scene's tail blends
    # smoothly with next scene's lead — no clipped words, no model holds, no
    # abrupt boundaries. Total master VO = 587.176s.
    #
    # Per-scene VOs are kept on disk (originals restored from _pre-trim) but
    # the build script places ONLY the master VO on track 1.
    #
    # Scene durations below = original VO duration MINUS per-scene crossfade
    # contribution (0.1s for boundary scenes S1/S7, 0.2s for middle S2-S6).
    # These define the VISUAL timeline scene boundaries (at crossfade
    # midpoints). Total = 587.176s = master VO duration.
    {"id": 1, "name": "hook",      "scripted_dur": 20.0085, "actual_dur": 20.0085, "vo": "vo-scene-1-hook.mp3"},
    {"id": 2, "name": "authority", "scripted_dur": 32.8652, "actual_dur": 32.8652, "vo": "vo-scene-2-authority.mp3"},
    {"id": 3, "name": "question",  "scripted_dur": 93.3300, "actual_dur": 93.3300, "vo": "vo-scene-3-question.mp3"},
    {"id": 4, "name": "loantrick", "scripted_dur": 133.2683,"actual_dur": 133.2683,"vo": "vo-scene-4-loan-trick.mp3"},
    {"id": 5, "name": "whydealer", "scripted_dur": 157.0455,"actual_dur": 157.0455,"vo": "vo-scene-5-why-dealer.mp3"},
    {"id": 6, "name": "fix",       "scripted_dur": 138.4231,"actual_dur": 138.4231,"vo": "vo-scene-6-fix.mp3"},
    {"id": 7, "name": "signoff",   "scripted_dur": 12.2353, "actual_dur": 12.2353, "vo": "vo-scene-7-signoff.mp3"},
]

# Master VO file (single concatenated audio with crossfaded boundaries).
MASTER_VO_FILE = "voice/master-vo.mp3"
MASTER_VO_DUR = 587.1759

# Strictly back-to-back placement on BOTH tracks. VOs and visuals end at the
# same timeline frame — no trailing black at the end of the video.
# VO mp3s are silence-trimmed + rendered without stitching, so back-to-back
# transitions sound clean without needing a breath gap.
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
ACTUAL_STARTS = VISUAL_STARTS  # visuals scale against gap-free starts
TOTAL_RUNTIME = VO_STARTS[-1]

# ============================================================
# VISUAL TRACK MANIFEST
# Format: (scripted_start, scripted_end, asset_relpath, clip_type)
# Asset paths relative to RENDERS dir.
#
# clip_type:
#   "motion"       — baked MP4 at exact slot duration (ffmpeg tpad), placed once
#   "still_kb"     — Ken Burns animated MP4 (ffmpeg zoompan), placed once
#   "still_freeze" — PNG of motion's last frame, looped on timeline (smooth post-motion hold)
#
# Scene 5 + 6 visuals re-ordered 2026-04-30 to match script narrative
# (finance before aftercare in S5; total-cost before bank-letter in S6).
# ============================================================

VISUAL_TRACK = [
    # Rebuilt 2026-04-30 PM with the locked principle:
    #   NEVER place two clips of the same source image as adjacent cuts.
    # When motion + KB-still of the same source need to both appear, a different
    # image (motif callback or merged-clip) is inserted between them so the
    # eye perceives them as distinct beats — no frame-jump.
    #
    # All entries written in actual seconds (SCENES.scripted_dur = actual_dur,
    # so scaling is identity 1.0 — frame-perfect adjacency).
    # Cadence: section-aware per research (hook 2-4s, body 8-12s, reveals 4-8s).
    # KB direction varied every clip; zoom % scaled by duration to hit
    # 2-2.5%/sec velocity target.

    # === SCENE 1 — HOOK (6 cuts · 20.0085s) — last cut shrunk -0.10s for crossfade
    (0.00000,   5.00000, "motion/kling-clip-1-hook.mp4",                              "motion"),    # M1 5s
    (5.00000,   8.00000, "motion/baked/kb-v2/s1-h2-pen-on-contract-kb.mp4",           "still_kb"),  # H2 3s in 16%
    (8.00000,  11.00000, "motion/baked/kb-v2/s1-h4-clock-papers-kb.mp4",              "still_kb"),  # H4 3s in 16%
    (11.00000, 14.00000, "motion/baked/kb-v2/s1-h5-dealership-perspective-kb.mp4",    "still_kb"),  # H5 3s panR 15%
    (14.00000, 16.00000, "motion/baked/kb-v2/s1-h6-customer-doorway-kb.mp4",          "still_kb"),  # H6 2s in 18%
    (16.00000, 20.00850, "motion/baked/kb-v2/s1-h7-corridor-kb.mp4",                  "still_kb"),  # H7 4.0085s in 14%

    # === SCENE 2 — AUTHORITY (6 cuts · 32.8652s) — last cut shrunk -0.20s for crossfade
    (20.00850, 25.00850, "motion/baked/kb-v2/s2-a1-floor-golden-kb.mp4",              "still_kb"),  # A1 5s
    (25.00850, 30.00850, "motion/baked/kb-v2/s2-a2-mass-market-kb.mp4",               "still_kb"),  # A2 5s
    (30.00850, 35.00850, "motion/baked/kb-v2/s2-a3-luxury-showroom-kb.mp4",           "still_kb"),  # A3 5s
    (35.00850, 42.00850, "motion/baked/kb-v2/s2-a4-executive-desk-kb.mp4",            "still_kb"),  # A4 7s
    (42.00850, 48.00850, "motion/baked/kb-v2/s2-a5-paper-stack-kb.mp4",               "still_kb"),  # A5 6s
    (48.00850, 52.87370, "motion/baked/kb-v2/s2-a6-three-windows-night-kb.mp4",       "still_kb"),  # A6 4.87s

    # === SCENE 3 — QUESTION (17 cuts · 93.3300s)
    (52.87370,  57.87370, "motion/baked/kb-v2/s3-q1-salesperson-silhouette-kb.mp4",   "still_kb"),  # Q1 5s
    (57.87370,  62.87370, "motion/baked/kb-v2/s3-q2-hands-across-desk-kb.mp4",        "still_kb"),  # Q2 5s
    (62.87370,  67.87370, "motion/baked/kb-v2/s3-q3-clasped-hands-kb.mp4",            "still_kb"),  # Q3 5s
    (67.87370,  72.87370, "motion/baked/kb-v2/s3-q4-calculator-paper-kb.mp4",         "still_kb"),  # Q4 5s
    (72.87370,  79.87370, "motion/baked/kb-v2/s3-q5-weekly-column-kb.mp4",            "still_kb"),  # Q5 7s
    (79.87370,  85.87370, "motion/baked/kb-v2/s3-q6-contract-overhead-kb.mp4",        "still_kb"),  # Q6 6s
    (85.87370,  91.87370, "motion/baked/kb-v2/s3-q7-training-binder-kb.mp4",          "still_kb"),  # Q7 6s
    (91.87370,  96.87370, "motion/baked/kb-v2/s3-q8-handshake-silhouettes-kb.mp4",    "still_kb"),  # Q8 5s
    (96.87370, 102.87370, "motion/baked/kb-v2/s3-q9-clipboard-checklist-kb.mp4",      "still_kb"),  # Q9 6s
    (102.87370,107.87370, "motion/baked/kb-v2/s3-q10-arrow-flowchart-kb.mp4",         "still_kb"),  # Q10 5s
    (107.87370,112.87370, "motion/baked/kb-v2/s3-q11-three-boxes-diagram-kb.mp4",     "still_kb"),  # Q11 5s
    (112.87370,117.87370, "motion/baked/kb-v2/s3-q12-corridor-side-angle-kb.mp4",     "still_kb"),  # Q12 5s
    (117.87370,124.87370, "motion/baked/kb-v2/s3-q13-corridor-walk-away-kb.mp4",      "still_kb"),  # Q13 7s
    (124.87370,130.87370, "motion/baked/kb-v2/s3-q14-three-glass-offices-kb.mp4",     "still_kb"),  # Q14 6s
    (130.87370,136.87370, "motion/baked/kb-v2/s3-q15-calculator-screen-kb.mp4",       "still_kb"),  # Q15 6s
    (136.87370,141.87370, "motion/baked/kb-v2/s3-q16-pen-midair-kb.mp4",              "still_kb"),  # Q16 5s
    (141.87370,146.20370, "motion/baked/kb-v2/s3-q17-end-of-day-kb.mp4",              "still_kb"),  # Q17 4.33s

    # === SCENE 4 — LOAN TRICK (14 cuts · 133.2683s)
    (146.20370, 154.20370, "motion/baked/kb/still-3-cars-comparison-kb-8s.mp4",                "still_kb"),  # 8s cars
    (154.20370, 165.20370, "motion/baked/kb-v3/s4-4B-commission-flow-panR-11s-kb.mp4",         "still_kb"),  # 11s commission
    (165.20370, 176.20370, "motion/baked/v2-kling/kling-v2-4A-stacks-pan-baked.mp4",           "motion"),    # 11s stacks motion
    (176.20370, 182.20370, "motion/baked/kb-v2/s3-q5-weekly-column-kb.mp4",                    "still_kb"),  # 6s MOTIF weekly
    (182.20370, 194.20370, "motion/baked/kb/still-v2-4A-split-stacks-kb.mp4",                  "still_kb"),  # 12s split-stacks
    (194.20370, 208.20370, "motion/baked/merged/s4-cars-parallax-merged.mp4",                  "still_kb"),  # 14s parallax
    (208.20370, 214.20370, "motion/baked/kb-v2/s3-q15-calculator-screen-kb.mp4",               "still_kb"),  # 6s MOTIF calc
    (214.20370, 226.20370, "motion/baked/merged/s4-luxury-treadmill-merged.mp4",               "still_kb"),  # 12s luxury-merged
    (226.20370, 232.20370, "motion/baked/kb-v2/s2-a4-executive-desk-kb.mp4",                   "still_kb"),  # 6s MOTIF desk
    (232.20370, 245.20370, "motion/baked/v2-kling/kling-v2-4D-luxury-treadmill-baked.mp4",     "motion"),    # 13s luxury motion
    (245.20370, 251.20370, "motion/baked/kb-v2/s2-a5-paper-stack-kb.mp4",                      "still_kb"),  # 6s MOTIF paper
    (251.20370, 260.20370, "motion/baked/kb/still-3-cars-comparison-kb-14s.mp4",               "still_kb"),  # 9s cars-14s
    (260.20370, 265.20370, "motion/baked/kb-v2/s2-a6-three-windows-night-kb.mp4",              "still_kb"),  # 5s MOTIF windows
    (265.20370, 279.47200, "motion/baked/kb-v3/s4-3-cars-comparison-out-15s-kb.mp4",           "still_kb"),  # 14.27s cars-out closing

    # === SCENE 5 — WHY DEALER (16 cuts · 157.0455s)
    (279.47200, 290.47200, "motion/baked/kb/still-4-three-rooms-kb.mp4",                       "still_kb"),  # 11s rooms
    (290.47200, 303.47200, "motion/baked/v2-mj/mj-v2-5A-three-offices-dolly-baked.mp4",        "motion"),    # 13s offices motion
    (303.47200, 309.47200, "motion/baked/kb-v2/s2-a4-executive-desk-kb.mp4",                   "still_kb"),  # 6s MOTIF desk
    (309.47200, 320.47200, "motion/baked/kb-v3/s5-5A-three-glass-offices-out-11s-kb.mp4",      "still_kb"),  # 11s offices out
    (320.47200, 331.47200, "motion/baked/kb-v3/s5-5C-finance-desk-panR-11s-kb.mp4",            "still_kb"),  # 11s finance panR
    (331.47200, 337.47200, "motion/baked/kb-v2/s2-a5-paper-stack-kb.mp4",                      "still_kb"),  # 6s MOTIF paper
    (337.47200, 352.47200, "motion/baked/v2-mj/mj-v2-5C-finance-zoom-baked.mp4",               "motion"),    # 15s finance motion
    (352.47200, 364.47200, "motion/baked/kb/still-v2-5B-paint-protection-bottle-kb.mp4",       "still_kb"),  # 12s paint [overlay 362.2 lands here]
    (364.47200, 369.47200, "motion/baked/kb-v2/s3-q4-calculator-paper-kb.mp4",                 "still_kb"),  # 5s MOTIF calc-paper
    (369.47200, 380.47200, "motion/baked/kb-v3/s5-5B-paint-protection-bottle-panL-11s-kb.mp4", "still_kb"),  # 11s paint panL
    (380.47200, 391.47200, "motion/baked/kb-v3/s5-5D-holdback-three-tier-in-11s-kb.mp4",       "still_kb"),  # 11s holdback in
    (391.47200, 396.47200, "motion/baked/kb-v2/s3-q3-clasped-hands-kb.mp4",                    "still_kb"),  # 5s MOTIF hands
    (396.47200, 413.47200, "motion/baked/v2-kling/kling-v2-5D-holdback-chiaroscuro-baked.mp4", "motion"),    # 17s holdback motion
    (413.47200, 425.47200, "motion/baked/kb/still-v2-5E-cash-stack-kb.mp4",                    "still_kb"),  # 12s cash
    (425.47200, 430.47200, "motion/baked/kb-v2/s3-q5-weekly-column-kb.mp4",                    "still_kb"),  # 5s MOTIF weekly
    (430.47200, 436.51750, "motion/baked/kb-v3/s5-5E-cash-stack-panD-16s-kb.mp4",              "still_kb"),  # 6.05s cash panD closing

    # === SCENE 6 — FIX REVEALS (17 cuts · 138.4231s)
    (436.51750, 444.51750, "motion/baked/kb/still-5-confident-customer-kb-12s.mp4",            "still_kb"),  # 8s customer
    (444.51750, 448.51750, "motion/baked/kb-v2/s1-h7-corridor-kb.mp4",                         "still_kb"),  # 4s MOTIF corridor
    (448.51750, 459.51750, "motion/baked/kb-v3/s6-6B-total-cost-comparison-panR-11s-kb.mp4",   "still_kb"),  # 11s total panR
    (459.51750, 462.51750, "motion/baked/kb-v2/s1-h2-pen-on-contract-kb.mp4",                  "still_kb"),  # 3s MOTIF pen
    (462.51750, 470.51750, "motion/baked/kb/still-v2-6B-total-cost-comparison-kb.mp4",         "still_kb"),  # 8s total
    (470.51750, 475.51750, "motion/baked/kb-v2/s3-q15-calculator-screen-kb.mp4",               "still_kb"),  # 5s MOTIF calc
    (475.51750, 486.51750, "motion/baked/kb-v3/s6-6A-bank-letter-in-11s-kb.mp4",               "still_kb"),  # 11s bank in
    (486.51750, 489.51750, "motion/baked/kb-v2/s1-h4-clock-papers-kb.mp4",                     "still_kb"),  # 3s MOTIF clock
    (489.51750, 504.51750, "motion/baked/v2-mj/mj-v2-6A-bank-letter-tilt-baked.mp4",           "motion"),    # 15s bank motion
    (504.51750, 516.51750, "motion/baked/kb/still-5-confident-customer-kb-29s.mp4",            "still_kb"),  # 12s customer-29
    (516.51750, 521.51750, "motion/baked/kb-v2/s3-q3-clasped-hands-kb.mp4",                    "still_kb"),  # 5s MOTIF hands
    (521.51750, 532.51750, "motion/baked/kb-v3/s6-6C-window-banner-panR-11s-kb.mp4",           "still_kb"),  # 11s window panR
    (532.51750, 537.51750, "motion/baked/kb-v2/s3-q5-weekly-column-kb.mp4",                    "still_kb"),  # 5s MOTIF weekly
    (537.51750, 555.51750, "motion/baked/v2-mj/mj-v2-6C-window-banner-pull_0-baked.mp4",       "motion"),    # 18s window motion
    (555.51750, 566.51750, "motion/baked/kb-v3/s6-6B-total-cost-comparison-out-11s-kb.mp4",    "still_kb"),  # 11s total-out
    (566.51750, 570.51750, "motion/baked/kb-v2/s3-q4-calculator-paper-kb.mp4",                 "still_kb"),  # 4s MOTIF calc-paper
    (570.51750, 574.94060, "motion/baked/kb-v3/s6-6C-window-banner-out-5s-kb.mp4",             "still_kb"),  # 4.42s window-out closing

    # === SCENE 7 — SIGNOFF (2 cuts · 12.2353s)
    (574.94060, 580.94060, "motion/baked/kb/still-v2-7A-laptop-cheatsheet-kb.mp4",             "still_kb"),  # 6s laptop
    (580.94060, 587.17590, "motion/baked/kb/still-v2-7B-dealership-dusk-kb.mp4",               "still_kb"),  # 6.24s dealership-dusk
]

# Baked motion durations (must match what bake-motion-clips.sh produces)
BAKED_MOTION_DURATIONS = {
    "kling-clip-1-hook.mp4": 5.04,                                 # original 5s motion (no bake)
    "mj-v2-2A-binder-tilt-down.mp4": 5.21,                          # original (no bake)
    "mj-v2-3B-binder-dolly.mp4": 5.21,                              # original (no bake)
    "mj-v2-3D-three-rooms-pull-baked.mp4": 10.0,
    "kling-v2-4A-stacks-pan-baked.mp4": 22.0,
    "kling-clip-3-cars-parallax.mp4": 5.04,                         # original (no bake)
    "kling-v2-4D-luxury-treadmill-baked.mp4": 13.0,
    "mj-v2-5A-three-offices-dolly-baked.mp4": 13.0,
    "mj-v2-5C-finance-zoom-baked.mp4": 15.0,
    "kling-v2-5D-holdback-chiaroscuro-baked.mp4": 17.0,
    "mj-v2-6A-bank-letter-tilt-baked.mp4": 15.0,
    "mj-v2-6C-window-banner-pull_0-baked.mp4": 18.0,
}

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
    """Return scene index for a given scripted timestamp."""
    for i in range(len(SCENES)):
        if SCRIPTED_STARTS[i] <= scripted_sec < SCRIPTED_STARTS[i + 1]:
            return i
    return len(SCENES) - 1  # clamp to last scene


def scale_to_actual(scripted_sec, scene_idx):
    """Scale a scripted timestamp into actual timeline space (proportional within scene)."""
    scene = SCENES[scene_idx]
    in_scene = scripted_sec - SCRIPTED_STARTS[scene_idx]
    scale = scene["actual_dur"] / scene["scripted_dur"]
    return ACTUAL_STARTS[scene_idx] + in_scene * scale


def compute_scaled_track():
    """Apply proportional per-scene scaling to VISUAL_TRACK + absorb motion-baked-shorter-than-slot
    into the immediately-following still entry."""
    scaled = []
    for entry in VISUAL_TRACK:
        scripted_start, scripted_end, asset, ctype = entry
        scene_idx = find_scene(scripted_start)
        new_start = scale_to_actual(scripted_start, scene_idx)
        new_end = scale_to_actual(scripted_end, scene_idx)
        scaled.append([new_start, new_end, asset, ctype])

    # Absorb motion baked-shorter-than-scaled into next entry
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
            scaled[i + 1][0] = actual_motion_end  # next entry starts at motion's actual end

    return [tuple(e) for e in scaled]


# ============================================================
# CONNECT TO RESOLVE
# ============================================================

print("=" * 60)
print("AUDM V1 - DaVinci auto-build (Phase 1 + 2)")
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

# ============================================================
# COMPUTE SCALED VISUAL TRACK
# ============================================================

scaled_track = compute_scaled_track()
print(f"\nScene timing (scripted -> actual):")
for i, s in enumerate(SCENES):
    drift = ACTUAL_STARTS[i] - SCRIPTED_STARTS[i]
    print(f"  Scene {s['id']} {s['name']:10s} {SCRIPTED_STARTS[i]:6.2f}s -> {ACTUAL_STARTS[i]:6.2f}s "
          f"(scripted {s['scripted_dur']:.2f}s, actual {s['actual_dur']:.2f}s, drift {drift:+.2f}s)")
print(f"  Total runtime: {TOTAL_RUNTIME:.2f}s ({TOTAL_RUNTIME/60:.1f}min)")

# ============================================================
# IMPORT MEDIA
# ============================================================

all_paths = []
missing = []

# Master VO (single concatenated audio with crossfaded boundaries)
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

# Music
print(f"\nMusic bed:")
for m in MUSIC_FILES:
    p = RENDERS / MUSIC_DIR_REL / m
    if p.exists():
        all_paths.append(str(p))
        print(f"  {m}")
    else:
        print(f"  [warn] missing: {p}")

# Dollar-figure overlays
print(f"\nDollar-figure overlays:")
for _, _, fname in OVERLAYS:
    p = RENDERS / OVERLAY_DIR_REL / fname
    if p.exists():
        all_paths.append(str(p))
        print(f"  {fname}")
    else:
        print(f"  [warn] missing: {p}")

if missing:
    print(f"\n[warn] {len(missing)} assets missing:")
    for m in missing[:5]:
        print(f"   {m}")
    if len(missing) > 5:
        print(f"   ... and {len(missing) - 5} more")

all_paths = list(dict.fromkeys(all_paths))

# CRITICAL — order matters here. To force fresh re-import of media (which
# defeats DaVinci's filename-dedupe cache that keeps stale duration metadata),
# we must:
#   1. Delete any existing timeline that references the cached clips
#   2. Then DeleteClips on cached media-pool entries
#   3. Then ImportMedia for fresh
# DeleteClips silently FAILS if a clip is referenced by an active timeline, so
# step 1 must happen before step 2. Pattern caught V2 2026-05-03.

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

# ============================================================
# DETECT DEFAULT STILL DURATION (for still_freeze chunk sizing)
# ============================================================

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

# ============================================================
# CREATE TIMELINE
# ============================================================

# (Old timeline already deleted above, before media-pool nuke + import.)

timeline = mp.CreateEmptyTimeline(TIMELINE_NAME)
if not timeline:
    raise RuntimeError(f"Could not create timeline {TIMELINE_NAME}")
project.SetCurrentTimeline(timeline)
timeline.SetStartTimecode("00:00:00:00")
TL_START = timeline.GetStartFrame()
print(f"Timeline: {TIMELINE_NAME} (start frame {TL_START}, TC 00:00:00:00)")

# Ensure audio track 2 exists for music bed + video track 2 for overlays
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

# ============================================================
# PLACE AUDIO (VOs back-to-back at actual cumulative durations)
# ============================================================

print(f"\nPlacing master VO ({MASTER_VO_DUR:.2f}s — single clip with crossfaded scene boundaries)...")
master_vo_clip = find_clip_in_pool(mp, Path(MASTER_VO_FILE).name)
if master_vo_clip:
    # CRITICAL: explicit startFrame=0 + endFrame=MASTER_VO_DUR forces DaVinci to use
    # the script-declared duration, NOT whatever was cached in media pool from a
    # prior import. Without this, re-imported VOs play their old cached length and
    # the audio cuts short of the visual track. Pattern caught on V2 2026-05-03.
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
    print(f"  [fail] master VO not in pool — run build-master-vo.py first")

# ============================================================
# PLACE MUSIC BED (audio track 2, full timeline length)
# Volume must be adjusted manually in Inspector — no API for audio levels.
# ============================================================

print(f"\nPlacing music bed on track 2 (3 tracks sequentially at -22dB)...")
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
    # Get track duration from clip
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
        "endFrame": place_frames,  # exclusive
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

# ============================================================
# PLACE DOLLAR-FIGURE OVERLAYS (video track 2, transparent PNGs)
# ============================================================

print(f"\nPlacing {len(OVERLAYS)} dollar-figure overlays on V2...")
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

# ============================================================
# PLACE VISUAL TRACK
# ============================================================

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

    # Frame-accurate adjacency: compute target_frames as the diff between
    # rounded end and start frames (NOT rounded diff). Otherwise adjacent
    # entries can overlap or gap by 1 frame depending on sub-frame rounding.
    end_frame = sec_to_frame(new_end)
    start_frame = sec_to_frame(new_start)
    target_frames = end_frame - start_frame
    timeline_start = TL_START + start_frame

    if clip_type in ("motion", "still_kb"):
        # Single placement — for motion, source matches slot; for KB videos,
        # endFrame trims if scaled slot < KB length (most cases <1s diff).
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
        # still_freeze: PNG looped in chunks. >= 1 (not >= 2) so we never leave
        # a 1-frame black flick at the end of the slot. endFrame=1 with
        # startFrame=0 is a valid 1-frame placement (only endFrame==startFrame
        # is rejected by Resolve).
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

# ============================================================
# SUMMARY
# ============================================================

print("\n" + "=" * 60)
print("BUILD COMPLETE")
print("=" * 60)
print(f"Project: {project.GetName()}")
print(f"Timeline: {timeline.GetName()}")
print(f"Resolution: {WIDTH}x{HEIGHT} @ {FPS}fps")
print(f"Total runtime: {TOTAL_RUNTIME:.2f} sec ({int(TOTAL_RUNTIME/60)}:{int(TOTAL_RUNTIME%60):02d})")
print(f"VO scenes (back-to-back): {len(SCENES)} on audio track 1")
print(f"Music bed: track 2")
print(f"Visual entries placed: {placed} / {len(scaled_track)} on video track 1")
print()
print("NEXT STEPS:")
print("  1. Edit page -> Shift+Z (zoom to fit) -> Home -> Spacebar (play through)")
print("  2. Adjust music volume in Inspector (target -18 to -24 dB under VO)")
print("  3. If playback chokes, Playback -> Render Cache -> Smart")
print("  4. Final QC + 1080p MP4 export from Deliver page")
print()
