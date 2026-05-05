# AU Dealer Math V3 (The Aftercare Room) - DaVinci Resolve auto-build script
#
# Assembles V3 timeline:
#   - Master VO (acrossfade-blended, 683.45s) on audio track 1, single placement
#   - Music bed on audio track 2 (underbelly-trio-splice-ducked-684s-v1.mp3 - 3-track splice, YT Audio Library)
#   - 63 visual entries on video track 1 (63 unique stills, no motif callbacks needed)
#   - All visuals are pre-baked KB MP4s (ffmpeg zoompan) - DaVinci just places them
#   - No PNG overlays this iteration (deferred - V3 v1 ships caption-only)
#
# Frame-accurate adjacency, no-adjacent-same-image rule satisfied.
#
# RUN INSIDE DaVinci Resolve 20 Py3 Console:
#   exec(open(r"C:\dev\Claude\generator\au-dealer-math\build-v3-davinci.py").read())

from pathlib import Path

REPO = Path(r"C:\dev\Claude")
RENDERS = REPO / "content" / "au-dealer-math" / "scripts" / "v03-renders"

PROJECT_NAME = "AUDM_V3_AftercareRoom"
TIMELINE_NAME = "V3_main"
WIDTH, HEIGHT = 1920, 1080
FPS = 24

MUSIC_FILES = [
    # 3-track Underbelly splice (Hand In The Dark -> Moorland -> Wide Boys ->
    # Hand loop -> Moorland partial), 3s acrossfade between adjacent tracks,
    # 1s fade-in / 2s fade-out at 679s, -33dB duck (matches V2 music at
    # -45 LUFS integrated; raw -8dB was leaving music 25dB too hot vs V2),
    # trimmed to 681.08s to match V3 master VO duration.
    # Sequence (approximate):
    #   00:00-02:42  A Hand In The Dark        (HOOK + AUTHORITY)
    #   02:42-05:14  Moorland                  (AFTERCARE-MENU)
    #   05:14-07:51  Wide Boys                 (MATH REVEAL)
    #   07:51-10:31  A Hand In The Dark loop   (WHY-HIGH -> Hand reanchor)
    #   10:31-11:21  Moorland partial fade-out (WHAT TO DO + SIGNOFF)
    # Source: YT Audio Library Underbelly & Ty Mayer trio - zero CID risk.
    "underbelly-trio-splice-ducked-681s-v1.mp3",
]
MUSIC_DIR_REL = "music"

# V3 v2 OVERLAYS — 13 dollar-figure / percent callouts on V2 track.
# Timestamps anchored to Whisper word-level data in vo-transcriptions.json.
# Rule: start = first_word_timeline_start - 0.10s (eye registers BEFORE Mac
# says it). Duration = (last_word_te - first_word_ts) + 1.5s read buffer,
# capped at 5.0s. All values rounded to 2 decimal places.
# Cross-verified 2026-05-05 against
# content/au-dealer-math/scripts/v03-renders/vo-transcriptions.json.
OVERLAYS = [
    # SCENE 1 HOOK
    ( 16.56, 3.70, "01-hook-margin-tease.png"),     # "$1,500-$3,000 MARGIN" @ Mac says "$1 ,500 and $3 ,000 a margin" (16.66 -> 18.86)
    # SCENE 4 MATH — paint protection
    (208.85, 3.08, "02-paint-retail.png"),          # "RETAIL: $1,500-$2,500" @ "$1 ,500 to $2 ,500" (208.95 -> 210.53)
    (220.33, 2.80, "03-paint-cost.png"),            # "DEALER COST: $400-$600" @ "$400 to $600." (220.43 -> 221.73)
    (224.01, 3.32, "04-paint-margin.png"),          # "MARGIN: 70-75%" @ "70 to 75%." (224.11 -> 225.93)
    # SCENE 4 MATH — window tint
    (228.11, 2.94, "05-tint-retail.png"),           # "RETAIL: $600-$700" @ "$600 to $700" (228.21 -> 229.65)
    (238.13, 2.48, "06-tint-cost.png"),             # "DEALER COST: $200-$300" @ "$200 to $300," (238.23 -> 239.21)
    (241.13, 3.26, "07-tint-margin.png"),           # "MARGIN: 50-60%" @ "50 to 60%." (241.23 -> 242.99)
    # SCENE 4 MATH — stack
    (247.19, 2.24, "08-stack-customer.png"),        # "CUSTOMER PAYS: $2,700" @ "$2 ,700" (247.29 -> 248.03)
    (250.59, 2.08, "09-stack-dealer-gross.png"),    # "DEALER GROSS: $1,900" @ "$1 ,900" (250.69 -> 251.27)
    (265.91, 2.84, "10-full-attach.png"),           # "FULL ATTACH: $3,000-$4,000" @ "$3 ,000 to $4 ,000" (266.01 -> 267.35)
    # SCENE 4 MATH — penetration
    (289.41, 3.20, "11-aftercare-attach.png"),      # "AFTERCARE ATTACH: 60-80%" @ "60 and 80%." (289.51 -> 291.21)
    (304.23, 3.70, "12-finance-attach.png"),        # "FINANCE ATTACH: 20-30%" @ "20 and 30%." (304.33 -> 306.53)
    (328.65, 4.78, "13-avg-gross.png"),             # "AVG AFTERCARE GROSS: $1,500-$3,000/CAR" @ "$1 ,500 and $3 ,000 per car sold." (328.75 -> 332.03)
]
OVERLAY_DIR_REL = "overlays"

# Per-scene durations - V3 was first rendered then re-rendered after a script
# edit ("last week" -> "in my last video" in S2 + S4) which shifted S2 and S4
# durations. KB MP4s were baked against the FIRST render (scripted_dur). The
# RE-RENDERED master VO defines actual_dur. compute_scaled_track() proportionally
# re-times visuals so they stay anchored to narrative beats.
#   S2: VO grew +2.36s (script edit added 7 chars). Visuals stretch.
#   S4: VO shrunk -4.74s (Mac pacing variance even at locked seed). Visuals compress.
# Sum of actual_dur = 681.08s = master VO duration after V2-recipe re-splice
# (192k CBR + mono->stereo upmix, verified ffprobe 2026-05-05 PM).
SCENES = [
    {"id": 1, "name": "hook",            "scripted_dur": 27.92,  "actual_dur": 27.93,  "vo": "vo-scene-1-hook.mp3"},
    {"id": 2, "name": "authority",       "scripted_dur": 61.28,  "actual_dur": 63.64,  "vo": "vo-scene-2-authority.mp3"},
    {"id": 3, "name": "aftercare-menu",  "scripted_dur": 109.02, "actual_dur": 109.02, "vo": "vo-scene-3-aftercare-menu.mp3"},
    {"id": 4, "name": "math",            "scripted_dur": 150.16, "actual_dur": 145.42, "vo": "vo-scene-4-math.mp3"},
    {"id": 5, "name": "why-high",        "scripted_dur": 147.51, "actual_dur": 147.51, "vo": "vo-scene-5-why-high.mp3"},
    {"id": 6, "name": "what-to-do",      "scripted_dur": 138.60, "actual_dur": 138.60, "vo": "vo-scene-6-what-to-do.mp3"},
    {"id": 7, "name": "signoff",         "scripted_dur": 48.96,  "actual_dur": 48.96,  "vo": "vo-scene-7-signoff.mp3"},
]

MASTER_VO_FILE = "voice/v03-master-vo.mp3"
MASTER_VO_DUR = 681.08  # ffprobed 681.077506 after V2-recipe re-splice (192k CBR stereo)
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


# 63 visual placements - topic-aligned to Mac's voiceover (Whisper word-level
# timestamps + V3-NNN MJ prompt content). Replaces the original "evenly spread
# within scene" track. Each slot now lands within +/- 3s of the topic Mac is
# narrating (paint protection, window tint, dash cam, ceramic, AU vehicles, etc).
#
# Slot durations vary 6-12s (hook + math fast topic transitions) up to ~15s
# (slower scene 6 narration). Sum = 683.45s scripted timeline length.
# All entries are "still_kb" - pre-baked KB MP4s from bake-v3-aftercare-stills.py.
# Source PNGs unchanged; only timeline placement reordered. No-adjacent-same-image
# rule satisfied (cross-checked, all 63 unique).
#
# Topic alignment ground truth: vo-transcriptions.json word-level timestamps.
# Cross-references kept in inline comments next to each entry.
VISUAL_TRACK = [
    # === SCENE 1 - HOOK (0.00 -> 27.92s, 4 cuts, topic-aligned) =================
    (  0.0000,   7.0000,  "motion/baked/kb-v3/s2-a1-documentary_photograph_g-kb.mp4", "still_kb"),  # glass-walled FI office (Mac negates "starts in finance")
    (  7.0000,  14.0000,  "motion/baked/kb-v3/s1-h2-top-down_architectural-kb.mp4",   "still_kb"),  # three-doors establishing ("a room before that")
    ( 14.0000,  22.0000,  "motion/baked/kb-v3/s1-h3-top-down_photograph-kb.mp4",      "still_kb"),  # split invoice + brochures ($1500-$3000 margin reveal)
    ( 22.0000,  27.9200,  "motion/baked/kb-v3/s1-h1-documentary-kb.mp4",              "still_kb"),  # paint protection brochure (closes hook into menu)

    # === SCENE 2 - AUTHORITY + THREE-ROOM (27.92 -> 89.20s, 7 cuts, topic-aligned) ===
    ( 27.9200,  37.0000,  "motion/baked/kb-v3/s1-h4-documentary-kb.mp4",              "still_kb"),  # FI workstation 3q ("last video covered finance manager's office")
    ( 37.0000,  45.5000,  "motion/baked/kb-v3/s2-a6-wide_documentary_photogr-kb.mp4", "still_kb"),  # showroom-wide ("take you back one room")
    ( 45.5000,  54.0000,  "motion/baked/kb-v3/s2-a4-top-down_architectural-kb.mp4",   "still_kb"),  # three-doors door 2 lit ("It's three rooms")
    ( 54.0000,  62.5000,  "motion/baked/kb-v3/s3-m3-documentary_photograph-kb.mp4",   "still_kb"),  # salesperson brochure handoff ("hands you to aftercare manager first")
    ( 62.5000,  71.0000,  "motion/baked/kb-v3/s2-a3-documentary_photograph-kb.mp4",   "still_kb"),  # AU glass-fronted ("then aftercare hands you to finance")
    ( 71.0000,  80.0000,  "motion/baked/kb-v3/s2-a2-documentary_photograph-kb.mp4",   "still_kb"),  # AU dealership ("three commissioned salespeople, one customer")
    ( 80.0000,  89.2000,  "motion/baked/kb-v3/s2-a7-top-down_photograph_poli-kb.mp4", "still_kb"),  # desk doc ("paint protection looks like a line on invoice")

    # === SCENE 3 - AFTERCARE MENU (89.20 -> 198.22s, 11 cuts, topic-aligned) ===
    ( 89.2000, 100.0000,  "motion/baked/kb-v3/s3-m5-studio_documentary-kb.mp4",       "still_kb"),  # three-brochures stack (aftercare manager intro)
    (100.0000, 111.0000,  "motion/baked/kb-v3/s3-m6-documentary_photograph_c-kb.mp4", "still_kb"),  # customer hands ("menu sits in a few categories")
    (111.0000, 122.0000,  "motion/baked/kb-v3/s3-m4-studio_documentary-kb.mp4",       "still_kb"),  # single-brochure paint -- PAINT PROTECTION @ 112.5 ✓
    (122.0000, 131.0000,  "motion/baked/kb-v3/s3-m2-documentary-kb.mp4",              "still_kb"),  # tint-application technician -- WINDOW TINT @ 129.1 ✓
    (131.0000, 140.0000,  "motion/baked/kb-v3/s3-m1-documentary_photograph_e-kb.mp4", "still_kb"),  # tint-detail macro -- INTERIOR PROTECTION @ 138.7 transition
    (140.0000, 149.0000,  "motion/baked/kb-v3/s3-m7-documentary_photograph_c-kb.mp4", "still_kb"),  # customer hands -- DASH CAMERAS @ 148.4
    (149.0000, 157.0000,  "motion/baked/kb-v3/s3-m8-documentary_photograph_c-kb.mp4", "still_kb"),  # customer hands -- CERAMIC COATING @ 156.5
    (157.0000, 167.0000,  "motion/baked/kb-v3/s3-m9-documentary_photograph_c-kb.mp4", "still_kb"),  # customer hands -- TYRE/RIM @ 166.8
    (167.0000, 176.0000,  "motion/baked/kb-v3/s3-m10-documentary_photograph_c-kb.mp4","still_kb"),  # customer hands -- fabric / alloy / nudge bars
    (176.0000, 187.0000,  "motion/baked/kb-v3/s3-m11-documentary_photograph_c-kb.mp4","still_kb"),  # customer hands -- "that's the menu"
    (187.0000, 198.2200,  "motion/baked/kb-v3/s2-a5-top-down_architectural-kb.mp4",   "still_kb"),  # three-doors alt ("math once they're stacked" transition)

    # === SCENE 4 - MATH REVEAL (198.22 -> 348.38s, 14 cuts, topic-aligned) ===
    (198.2200, 208.0000,  "motion/baked/kb-v3/s4-t1-documentary_photograph-kb.mp4",   "still_kb"),  # desk laminate -- PAINT PROTECTION plan @ 203 ✓
    (208.0000, 218.5000,  "motion/baked/kb-v3/s4-t11-top-down_photograph_poli-kb.mp4","still_kb"),  # desk laminate -- paint cost basis $400-600 / margin 70-75%
    (218.5000, 227.0000,  "motion/baked/kb-v3/s4-t3-extreme_macro_photograph-kb.mp4", "still_kb"),  # invoice line finger -- WINDOW TINT $600-700 @ 226 ✓
    (227.0000, 237.5000,  "motion/baked/kb-v3/s4-t12-top-down_photograph_poli-kb.mp4","still_kb"),  # desk laminate -- tint cost $200-300 / margin 50-60%
    (237.5000, 247.0000,  "motion/baked/kb-v3/s4-t8-macro_photograph_low-ang-kb.mp4", "still_kb"),  # alloy wheel -- "Stack two together" @ 243 (alloy wheel as math/stack visual + tyre callback)
    (247.0000, 257.0000,  "motion/baked/kb-v3/s4-t4-extreme_macro_top-down-kb.mp4",   "still_kb"),  # macro doc -- "dealer's gross $1900" @ 247 ✓
    (257.0000, 266.0000,  "motion/baked/kb-v3/s4-t9-top-down_macro_photograp-kb.mp4", "still_kb"),  # dash-cam-or-ceramic macro -- DASH CAM @ 254.8 / CERAMIC @ 258 ✓
    (266.0000, 275.5000,  "motion/baked/kb-v3/s4-t10-top-down_macro_photograp-kb.mp4","still_kb"),  # dash-cam-or-ceramic alt -- "fully attached customer $3-4K" @ 261
    (275.5000, 286.0000,  "motion/baked/kb-v3/s4-t5-extreme_macro_top-down-kb.mp4",   "still_kb"),  # macro doc -- "margin stack" @ 272 / penetration intro @ 276
    (286.0000, 296.5000,  "motion/baked/kb-v3/s4-t13-top-down_photograph_poli-kb.mp4","still_kb"),  # desk laminate -- AFTERCARE ATTACH 60-80% @ 286 ✓
    (296.5000, 307.0000,  "motion/baked/kb-v3/s4-t6-extreme_macro_top-down-kb.mp4",   "still_kb"),  # macro doc -- FINANCE ATTACH 20-30% @ 300 ✓
    (307.0000, 317.5000,  "motion/baked/kb-v3/s4-t14-top-down_photograph_poli-kb.mp4","still_kb"),  # desk laminate -- aftercare 2-3x more attached @ 307 ✓
    (317.5000, 328.0000,  "motion/baked/kb-v3/s4-t2-documentary_photograph_t-kb.mp4", "still_kb"),  # contract stack reach -- weighted across customer population @ 320
    (328.0000, 348.3800,  "motion/baked/kb-v3/s4-t7-extreme_macro_top-down-kb.mp4",   "still_kb"),  # macro doc -- avg aftercare gross $1500-3000 / front-end gross

    # === SCENE 5 - WHY HIGH (348.38 -> 495.89s, 14 cuts, topic-aligned) ======
    (348.3800, 358.0000,  "motion/baked/kb-v3/s5-w7-documentary-kb.mp4",              "still_kb"),  # AU vehicle 3q -- "by the time you walk into aftercare manager's office"
    (358.0000, 368.5000,  "motion/baked/kb-v3/s5-w13-documentary_photograph_t-kb.mp4","still_kb"),  # F&I dual-monitor -- "three things have already happened"
    (368.5000, 379.0000,  "motion/baked/kb-v3/s5-w5-documentary-kb.mp4",              "still_kb"),  # salesperson silhouette -- "agreed on price / hard part of negotiation over"
    (379.0000, 389.5000,  "motion/baked/kb-v3/s5-w6-documentary-kb.mp4",              "still_kb"),  # salesperson silhouette 2 -- SIGNPOSTED @ 373 / "calm low-friction line"
    (389.5000, 400.0000,  "motion/baked/kb-v3/s5-w14-documentary_photograph_t-kb.mp4","still_kb"),  # F&I single monitor -- "frames the next room as extension of purchase"
    (400.0000, 410.5000,  "motion/baked/kb-v3/s5-w12-documentary_photograph-kb.mp4",  "still_kb"),  # independent detailer -- "you're tired" / decision fatigue @ 404-408
    (410.5000, 421.0000,  "motion/baked/kb-v3/s5-w1-cinema_verit-kb.mp4",             "still_kb"),  # current-gen Toyota -- "sitting in front of someone whose only job is the menu" @ 418
    (421.0000, 431.5000,  "motion/baked/kb-v3/s5-w2-cinema_verit-kb.mp4",             "still_kb"),  # current-gen Toyota 2 -- COMMISSIONED SALESPERSON @ 424-431
    (431.5000, 442.0000,  "motion/baked/kb-v3/s5-w8-documentary-kb.mp4",              "still_kb"),  # AU vehicle 3q 2 -- "bundling pitches / paint protection alongside showroom photo at 5 years" @ 443-451
    (442.0000, 452.5000,  "motion/baked/kb-v3/s5-w4-documentary_photograph_2-kb.mp4", "still_kb"),  # LandCruiser 2024 -- WINDOW TINT @ 452.4 (vehicle context for tint pitch)
    (452.5000, 463.0000,  "motion/baked/kb-v3/s5-w3-documentary_photograph_2-kb.mp4", "still_kb"),  # Ford Ranger 2024 -- INTERIOR PROTECTION @ 456 (vehicle context)
    (463.0000, 473.5000,  "motion/baked/kb-v3/s5-w9-documentary-kb.mp4",              "still_kb"),  # AU vehicle 3q 3 -- "structural reason attach is high"
    (473.5000, 484.0000,  "motion/baked/kb-v3/s5-w10-documentary_photograph-kb.mp4",  "still_kb"),  # AU streetscape -- "60-80% of buyers walk out adding $1500-3000"
    (484.0000, 495.8900,  "motion/baked/kb-v3/s5-w11-documentary_photograph-kb.mp4",  "still_kb"),  # AU flag -- closing scene 5 statement / national context

    # === SCENE 6 - WHAT TO DO (495.89 -> 634.49s, 9 cuts, topic-aligned) =======
    (495.8900, 510.5000,  "motion/baked/kb-v3/s6-d6-documentary_photograph_c-kb.mp4", "still_kb"),  # customer hands -- "First move: decide before you walk in"
    (510.5000, 526.0000,  "motion/baked/kb-v3/s6-d4-documentary_photograph-kb.mp4",   "still_kb"),  # customer walking out -- "make decisions at home, with a quote in front of you"
    (526.0000, 541.5000,  "motion/baked/kb-v3/s6-d3-documentary_photograph_m-kb.mp4", "still_kb"),  # F&I office wide -- INDEPENDENT DETAILER @ 514 / dealer comparison
    (541.5000, 557.0000,  "motion/baked/kb-v3/s6-d7-documentary_photograph_c-kb.mp4", "still_kb"),  # customer hands -- "Second move: ask for each on its own piece of paper"
    (557.0000, 572.5000,  "motion/baked/kb-v3/s6-d5-extreme_macro_top-down-kb.mp4",   "still_kb"),  # key fob macro -- handover detail / "$2000 product on its own piece of paper"
    (572.5000, 588.0000,  "motion/baked/kb-v3/s6-d2-documentary_photograph_c-kb.mp4", "still_kb"),  # customer tired lap -- "Third move: slow down. Take this OVERNIGHT @ 591"
    (588.0000, 603.5000,  "motion/baked/kb-v3/s6-d1-cinema_verit_photograph-kb.mp4",  "still_kb"),  # atmospheric dusk F&I -- "soft pressure tactic / car price is locked / aftercare can be added later"
    (603.5000, 619.0000,  "motion/baked/kb-v3/s6-d8-documentary_photograph_c-kb.mp4", "still_kb"),  # customer hands -- "if they won't let you add later, that itself tells you something"
    (619.0000, 634.4900,  "motion/baked/kb-v3/s6-d9-documentary_photograph_c-kb.mp4", "still_kb"),  # customer hands -- "customer who asks slowly gets the better outcome"

    # === SCENE 7 - SIGNOFF (634.49 -> 683.45s, 4 cuts, topic-aligned) ==========
    (634.4900, 647.0000,  "motion/baked/kb-v3/s7-z2-studio_documentary-kb.mp4",       "still_kb"),  # brochure stack chiaroscuro -- V4 trade-in tease intro
    (647.0000, 664.0000,  "motion/baked/kb-v3/s7-z3-studio_documentary-kb.mp4",       "still_kb"),  # invoices fan -- "two stacked deals (new car + used car)"
    (664.0000, 676.0000,  "motion/baked/kb-v3/s7-z1-studio-kb.mp4",                   "still_kb"),  # cheatsheet fan -- CHEATSHEET / link in description @ 664 ✓
    (676.0000, 683.4500,  "motion/baked/kb-v3/s7-z4-top-down_photograph_poli-kb.mp4", "still_kb"),  # closed brochure on contract -- sign-off / "I'm Mac on AU Dealer Math"
]


# V3 v1 has no Kling/MJ motion clips with tpad-extended durations.
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
    """V3 v1: scripted_dur = actual_dur for all scenes, so this is a passthrough.
    Kept for forward-compat if/when motion clips with tpad get re-introduced."""
    scaled = []
    for entry in VISUAL_TRACK:
        scripted_start, scripted_end, asset, ctype = entry
        scene_idx = find_scene(scripted_start)
        new_start = scale_to_actual(scripted_start, scene_idx)
        new_end = scale_to_actual(scripted_end, scene_idx)
        scaled.append([new_start, new_end, asset, ctype])

    # Motion-baked-shorter-than-slot absorption (no-op in V3 v1 since
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
print("AUDM V3 (The Aftercare Room) - DaVinci auto-build")
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
    print(f"  Scene {s['id']} {s['name']:14s} {SCRIPTED_STARTS[i]:6.2f}s -> {ACTUAL_STARTS[i]:6.2f}s "
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
    print(f"  (none - V3 v1 ships caption-only)")
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

# CRITICAL - order matters here. To force fresh re-import of media (which
# defeats DaVinci's filename-dedupe cache that keeps stale duration metadata),
# we must:
#   1. Delete any existing timeline that references the cached clips
#   2. Then DeleteClips on cached media-pool entries
#   3. Then ImportMedia for fresh
# DeleteClips silently FAILS if a clip is referenced by an active timeline, so
# step 1 must happen before step 2. Caught V2 2026-05-03 - voice cut at 8:45.

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

# Step 3: Fresh import - DaVinci now reads actual file metadata, not cache
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
    # the audio cuts short of the visual track. Caught V2 2026-05-03 after audio
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
    print(f"  [fail] master VO not in pool -- run build-master-vo for V3 first")

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
print(f"VO: v03-master-vo.mp3 (single clip, 6 acrossfade boundaries) on audio track 1")
print(f"Music bed: track 2")
print(f"Visual entries placed: {placed} / {len(scaled_track)} on video track 1")
print()
print("NEXT STEPS:")
print("  1. Edit page -> Shift+Z (zoom to fit) -> Home -> Spacebar (play through)")
print("  2. Adjust music volume in Inspector (target -22 to -26 dB under VO)")
print("  3. If playback chokes, Playback -> Render Cache -> Smart")
print("  4. Run render-v3-davinci.py to export 1080p MP4 to video/out/")
print("  5. Then: python generator/au-dealer-math/transcribe-vos-v03.py")
print("  6. Then: python generator/au-dealer-math/render-vN-captions.py 3")
print("  7. Then: loudnorm-twopass.py to -14 LUFS / TP -1.0 dBFS per audio finalize lock")
print()
