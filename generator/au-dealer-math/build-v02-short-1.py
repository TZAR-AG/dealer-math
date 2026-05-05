"""Build AUDM V2 Short 1 — F&I Office (28-32s, 9:16, looping).

Path (a): lift F&I rate-range scene from V2 main (~23s middle), bespoke
bookends generated via ElevenLabs (Mac LOCKED voice).

Pipeline:
  1. Build hook frame card ($4,800 cream-on-charcoal, 98pt) — generated PNG → 0.5s silent video
  2. Lift middle from audm-v2-FINAL.mp4 (audio+video, t=180.54→203.58s) and crop 16:9→9:16
  3. Build bookend videos:
       OPEN  = hook card 0.0-0.5s + open-VO frame 0.5-3.0s (2.5s VO) → ~3.0s total
              cropped from V2 main scene 1 footage (HOOK section, t=0-3s of V2 main)
       CLOSE = lifted from V2 main scene 1 footage (different beat) + close-VO ~3.2s
              with last 1.5s music fade-out
  4. Splice OPEN + MIDDLE + CLOSE
  5. Build music bed: extend V2's A-Hand-In-The-Dark soft-ducked under bookends
     where original music doesn't reach (the open + close VO segments add fresh
     music; middle's music is preserved as-is)
  6. Loudnorm twopass → -14 LUFS / TP -1.0 dBFS
  7. Caption burn (Shorts y=0.70 lower-third, 64pt) — SKIPPED with --no-captions

Output: video/out/shorts/audm-v2-short-1.mp4

Run: python generator/au-dealer-math/build-v02-short-1.py [--no-captions]

--no-captions: skip Step 7 (running sentence-block captions). Locked 2026-05-05
per option C — frame-1 number hook delivers sound-off lift; running captions
clash with Mac calm-authority + document-forensics DNA. V3+ default.
"""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(r"C:\dev\Claude")
VIDEO_OUT = REPO / "video" / "out"
SHORTS_OUT = VIDEO_OUT / "shorts"
SHORTS_OUT.mkdir(parents=True, exist_ok=True)

V02_RENDERS = REPO / "content" / "au-dealer-math" / "scripts" / "v02-renders"
SHORT1_BUILD = V02_RENDERS / "short1-build"
SHORT1_BUILD.mkdir(parents=True, exist_ok=True)

VOICE_SHORTS = V02_RENDERS / "voice-shorts"

# Lift source: V2 PRE-caption master (V2-FINAL has captions burned in at y=0.82,
# which would stack with Shorts captions at y=0.70). audm-v2-finance-managers-office.mp4
# is the pre-caption DaVinci export; audio is pre-finalize but our final loudnorm
# pass normalizes the spliced output anyway.
V2_FINAL = VIDEO_OUT / "audm-v2-finance-managers-office.mp4"   # 1920x1080 24fps, NO captions

# Lift window for the F&I-office reveal (rate-range mechanic). See vo-transcriptions.json scene 3.
LIFT_START = 180.54   # "When you walk into the finance office..."
LIFT_END   = 203.58   # "...present your repayments at that rate and they watch."
# Middle duration ≈ 23.04s

OPEN_VO   = VOICE_SHORTS / "short1-open.mp3"     # 2.51s — "What happens after you agree on the price?"
CLOSE_VO  = VOICE_SHORTS / "short1-close.mp3"    # 3.16s — "Then the F and I office. Watch what happens."

# Music bed (V2's locked HAAWK-safe YT Audio Library track, already ducked -24dB)
MUSIC_BED = V02_RENDERS / "music" / "a-hand-in-the-dark-looped-ducked-soft-578s-v3.mp3"

# Hook frame: $4,800 cream-on-charcoal full-bleed
HOOK_TEXT = "$4,800"
HOOK_FRAME_DUR = 0.5  # First half-second is pure hook card before open VO begins

# Tail after close VO finishes — 0.4s of breath room before hard cut to loop
CLOSE_TAIL = 0.4

FFMPEG = (
    r"C:\Users\adria\AppData\Local\Microsoft\WinGet\Packages"
    r"\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe"
    r"\ffmpeg-8.1-full_build\bin\ffmpeg.exe"
)
FFPROBE = (
    r"C:\Users\adria\AppData\Local\Microsoft\WinGet\Packages"
    r"\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe"
    r"\ffmpeg-8.1-full_build\bin\ffprobe.exe"
)

FONTS_DIR = REPO / "fonts"
DMSANS_BOLD = FONTS_DIR / "DM_Sans" / "DMSans-Bold.ttf"

# AUDM colors
CHARCOAL = "#2B2B2B"
CREAM    = "#F5EFE6"


def font_arg(p: Path) -> str:
    return str(p).replace("\\", "/").replace(":", r"\:")


def run(cmd: list, what: str) -> bool:
    print(f"  [run] {what}")
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="ignore")
    if r.returncode != 0:
        print(f"  [FAIL] {what}")
        print("  STDERR:", r.stderr.strip()[-2000:])
        return False
    return True


def probe_dur(p: Path) -> float:
    cmd = [FFPROBE, "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    return float(r.stdout.strip())


# ---------------------------------------------------------------------------
# Step 1 — Build hook frame card (0.5s, 1080x1920, $4,800 cream-on-charcoal)
# ---------------------------------------------------------------------------

def build_hook_frame() -> Path:
    """0.5s 1080x1920 charcoal background with $4,800 in cream at ~320pt centered.
    Audio: ~0.5s slice from V2 music bed at -10dB, NOT silence (silence drags
    integrated LUFS down + creates dead air at t=0).
    """
    out = SHORT1_BUILD / "01-hook-card.mp4"
    fa = font_arg(DMSANS_BOLD)
    cmd = [
        FFMPEG, "-y", "-loglevel", "error",
        "-f", "lavfi", "-i", f"color=c={CHARCOAL}:s=1080x1920:r=24:d={HOOK_FRAME_DUR}",
        # Pull a 0.5s music slice from a quiet moment of the V2 music bed
        "-ss", "5.0",
        "-i", str(MUSIC_BED),
        "-t", f"{HOOK_FRAME_DUR}",
        "-vf", (
            f"drawtext=fontfile='{fa}'"
            f":text='{HOOK_TEXT}'"
            f":fontcolor={CREAM}"
            f":fontsize=240"
            f":x=(w-text_w)/2"
            f":y=(h-text_h)/2"
        ),
        "-filter_complex", "[1:a]volume=0.6,afade=t=in:st=0:d=0.1[a]",
        "-map", "0:v", "-map", "[a]",
        "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-r", "24",
        "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
        "-shortest",
        str(out),
    ]
    if not run(cmd, "build hook card"):
        sys.exit(1)
    return out


# ---------------------------------------------------------------------------
# Step 2 — Build OPEN bookend video (cropped V2 footage + open VO + music)
# ---------------------------------------------------------------------------

def build_open_clip() -> tuple[Path, float]:
    """
    OPEN bookend = V2 footage from a documentary opening beat (use first ~3s of V2 main —
    this is V2's own scene 1 hook, document-forensics aesthetic, perfectly on-brand)
    cropped to 9:16, with open VO replacing original audio + music bed.

    Total dur = open_vo + 0.3s tail = ~2.8s
    """
    open_vo_dur = probe_dur(OPEN_VO)
    total = open_vo_dur + 0.3   # 0.3s breath after VO before middle joins
    out = SHORT1_BUILD / "02-open.mp4"

    # Pull V2 footage from a clean B-roll moment — use 0.0s start of V2 (hook beat).
    # Center-crop 1920x1080 → 1080x1920: crop center 1080x1080 from 1920 width, then
    # we need 9:16 final. Since V2 is 1920x1080 and we need 1080x1920, the cleanest
    # path is: scale V2 to fit width-wise (1080 wide → 607 tall), pad black above/below.
    # But document-forensics looks better fitting full-bleed by cropping to center 9:16
    # window: scale up 1920x1080 to ~3413x1920 then crop center 1080x1920.
    # Since that'd lose half the doc context, we use blur-pad instead (V1 Shorts pattern):
    #   foreground = scaled to 1080 wide (preserves aspect, ~607 tall)
    #   background = upscaled+blurred fill (charcoal-ish since doc-forensics)
    # Actually for AUDM doc-forensics where the action is centered, center-crop works.
    #
    # Use the V1-shorts blur-pad approach for visual continuity.
    cmd = [
        FFMPEG, "-y", "-loglevel", "error",
        "-ss", "0.0",
        "-i", str(V2_FINAL),
        "-i", str(OPEN_VO),
        "-t", f"{total:.3f}",
        "-filter_complex", (
            # Video: blur-pad 16:9 → 9:16 (V1 Shorts pattern)
            f"[0:v]split=2[orig][bg_src];"
            f"[bg_src]scale=1080:1920:force_original_aspect_ratio=increase,"
            f"crop=1080:1920,boxblur=20:5,eq=brightness=-0.20[bg];"
            f"[orig]scale=1080:-2[fg_scaled];"
            f"[bg][fg_scaled]overlay=(W-w)/2:(H-h)/2[v];"
            # Audio: open VO primary (full level, dynaudnorm to even peaks) + V2 music
            # underneath at low duck. dynaudnorm normalizes the VO to a consistent level
            # so loudnorm has a balanced source to work from. amix normalize=1 (default)
            # adds proper gain matching.
            f"[0:a]volume=0.18[a_orig];"
            f"[1:a]apad,atrim=0:{total:.3f},dynaudnorm=p=0.95:m=10[a_vo];"
            f"[a_orig][a_vo]amix=inputs=2:duration=longest:dropout_transition=0:normalize=0[a]"
        ),
        "-map", "[v]", "-map", "[a]",
        "-t", f"{total:.3f}",
        "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-r", "24",
        "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
        str(out),
    ]
    if not run(cmd, f"build open clip ({total:.2f}s)"):
        sys.exit(1)
    return out, total


# ---------------------------------------------------------------------------
# Step 3 — Lift middle from V2 (cropped 9:16, audio preserved)
# ---------------------------------------------------------------------------

def build_middle_clip() -> tuple[Path, float]:
    out = SHORT1_BUILD / "03-middle.mp4"
    dur = LIFT_END - LIFT_START
    cmd = [
        FFMPEG, "-y", "-loglevel", "error",
        "-ss", f"{LIFT_START:.3f}",
        "-i", str(V2_FINAL),
        "-t", f"{dur:.3f}",
        "-filter_complex", (
            # Same blur-pad pattern as open clip
            f"[0:v]split=2[orig][bg_src];"
            f"[bg_src]scale=1080:1920:force_original_aspect_ratio=increase,"
            f"crop=1080:1920,boxblur=20:5,eq=brightness=-0.20[bg];"
            f"[orig]scale=1080:-2[fg_scaled];"
            f"[bg][fg_scaled]overlay=(W-w)/2:(H-h)/2[v]"
        ),
        "-map", "[v]", "-map", "0:a",
        "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-r", "24",
        "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
        str(out),
    ]
    if not run(cmd, f"build middle clip ({dur:.2f}s)"):
        sys.exit(1)
    return out, dur


# ---------------------------------------------------------------------------
# Step 4 — Build CLOSE bookend (cropped V2 footage + close VO + music fade)
# ---------------------------------------------------------------------------

def build_close_clip() -> tuple[Path, float]:
    """
    CLOSE bookend = V2 footage at LIFT_END (continues the doc-forensics aesthetic) +
    close VO + music fade to silence in last 1.5s for invisible loop seam.
    """
    close_vo_dur = probe_dur(CLOSE_VO)
    total = close_vo_dur + CLOSE_TAIL    # 0.4s after VO finishes
    out = SHORT1_BUILD / "04-close.mp4"

    # Use V2 footage from LIFT_END onwards (continues the F&I office visual context)
    # Music fade is applied via afade at end
    fade_st = max(0.0, total - 1.5)  # start fading 1.5s before end

    cmd = [
        FFMPEG, "-y", "-loglevel", "error",
        "-ss", f"{LIFT_END:.3f}",
        "-i", str(V2_FINAL),
        "-i", str(CLOSE_VO),
        "-t", f"{total:.3f}",
        "-filter_complex", (
            # Video: blur-pad
            f"[0:v]split=2[orig][bg_src];"
            f"[bg_src]scale=1080:1920:force_original_aspect_ratio=increase,"
            f"crop=1080:1920,boxblur=20:5,eq=brightness=-0.20[bg];"
            f"[orig]scale=1080:-2[fg_scaled];"
            f"[bg][fg_scaled]overlay=(W-w)/2:(H-h)/2[v];"
            # Audio: V2 music bed at -10dB volume (the underlying V2 track) + close VO,
            # then mix and fade.
            f"[0:a]volume=0.18[a_orig];"
            f"[1:a]apad,atrim=0:{total:.3f},dynaudnorm=p=0.95:m=10[a_vo];"
            f"[a_orig][a_vo]amix=inputs=2:duration=longest:dropout_transition=0:normalize=0,"
            f"afade=t=out:st={fade_st:.3f}:d=1.5[a]"
        ),
        "-map", "[v]", "-map", "[a]",
        "-t", f"{total:.3f}",
        "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-r", "24",
        "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
        str(out),
    ]
    if not run(cmd, f"build close clip ({total:.2f}s, fade in last 1.5s)"):
        sys.exit(1)
    return out, total


# ---------------------------------------------------------------------------
# Step 5 — Concat: hook + open + middle + close
# ---------------------------------------------------------------------------

def concat_segments(parts: list) -> Path:
    """Concatenate parts in order via the concat demuxer (lossless if streams match)."""
    out = SHORT1_BUILD / "05-spliced.mp4"
    list_file = SHORT1_BUILD / "_concat-list.txt"
    list_file.write_text("\n".join(f"file '{p.as_posix()}'" for p in parts), encoding="utf-8")

    # Use concat demuxer with re-encode (clips have same codec/res but timestamps may need fixing)
    cmd = [
        FFMPEG, "-y", "-loglevel", "error",
        "-f", "concat", "-safe", "0",
        "-i", str(list_file),
        "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-r", "24",
        "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
        str(out),
    ]
    if not run(cmd, "concat segments"):
        sys.exit(1)
    return out


# ---------------------------------------------------------------------------
# Step 6 — Captions: build a Shorts-specific transcriptions JSON for full clip
# ---------------------------------------------------------------------------

def build_shorts_transcriptions(open_dur, middle_dur, close_dur) -> Path:
    """
    Build a vo-transcriptions.json equivalent that maps to the spliced timeline:
      - HOOK 0.0 - 0.5s: NO words (just the $4,800 visual)
      - OPEN 0.5 - HOOK_FRAME_DUR + open_dur: open VO words shifted to start at 0.5s
      - MIDDLE: middle VO words from V2 scene 3, shifted to start at HOOK + open_dur
      - CLOSE: close VO words shifted to start at HOOK + open + middle
    """
    # Load original V2 transcriptions for middle word timings (scene 3)
    with open(V02_RENDERS / "vo-transcriptions.json", encoding="utf-8") as f:
        v2_data = json.load(f)
    scene3 = v2_data["scenes"][3]
    middle_words = []
    for w in scene3["words"]:
        if LIFT_START <= w["timeline_start"] < LIFT_END:
            # Shift: in source, word is at timeline_start. In Short, middle starts at:
            #   HOOK_FRAME_DUR + open_dur (offset).
            # And the word's offset within the lift segment is (timeline_start - LIFT_START).
            offset = HOOK_FRAME_DUR + open_dur
            new_start = (w["timeline_start"] - LIFT_START) + offset
            new_end   = (w["timeline_end"]   - LIFT_START) + offset
            # Don't include words that extend past LIFT_END
            if new_end <= offset + middle_dur + 0.05:
                middle_words.append({
                    "word": w["word"],
                    "timeline_start": new_start,
                    "timeline_end": new_end,
                })

    # Open VO timings
    with open(VOICE_SHORTS / "short1-open.timings.json", encoding="utf-8") as f:
        open_data = json.load(f)
    open_words = []
    for w in open_data["words"]:
        offset = HOOK_FRAME_DUR
        open_words.append({
            "word": w["word"],
            "timeline_start": w["timeline_start"] + offset,
            "timeline_end":   w["timeline_end"]   + offset,
        })

    # Close VO timings
    with open(VOICE_SHORTS / "short1-close.timings.json", encoding="utf-8") as f:
        close_data = json.load(f)
    close_words = []
    close_offset = HOOK_FRAME_DUR + open_dur + middle_dur
    for w in close_data["words"]:
        close_words.append({
            "word": w["word"],
            "timeline_start": w["timeline_start"] + close_offset,
            "timeline_end":   w["timeline_end"]   + close_offset,
        })

    out = SHORT1_BUILD / "shorts-transcriptions.json"
    out.write_text(json.dumps({
        "scenes": [
            {"title": "Open",   "words": open_words},
            {"title": "Middle", "words": middle_words},
            {"title": "Close",  "words": close_words},
        ]
    }, indent=2), encoding="utf-8")
    return out


# ---------------------------------------------------------------------------
# Step 7 — Caption burn at y=0.70 (Shorts position, NOT 0.82 long-form)
# ---------------------------------------------------------------------------
# Reuse render-vN-captions.py logic but with overrides for y=0.70 + custom IO paths.
# Easiest: import the helper functions and reimplement the runner here.

sys.path.insert(0, str(REPO / "generator" / "au-dealer-math"))
import importlib.util
_caption_spec = importlib.util.spec_from_file_location(
    "render_vN_captions",
    str(REPO / "generator" / "au-dealer-math" / "render-vN-captions.py"),
)
_captions = importlib.util.module_from_spec(_caption_spec)
_caption_spec.loader.exec_module(_captions)


def burn_captions(in_mp4: Path, transcriptions: Path) -> Path:
    """Use render-vN-captions internals but override Y_CENTER_EXPR to h*0.70 for Shorts."""
    out = SHORT1_BUILD / "06-captioned.mp4"

    # Override the global Y position constant for Shorts
    # render-vN-captions module-level: Y_CENTER_EXPR = "h*0.82"
    _captions.Y_CENTER_EXPR = "h*0.70"

    words = _captions.load_words(transcriptions)
    blocks = _captions.chunk_into_sentences(words)
    print(f"  [captions] {len(words)} words -> {len(blocks)} blocks")
    for blk in blocks[:5]:
        print(f"    [{blk['start_t']:.2f}s-{blk['end_t']:.2f}s] {' / '.join(blk['lines'])}")

    if not _captions.DMSANS_REGULAR.exists():
        raise FileNotFoundError(f"Font missing: {_captions.DMSANS_REGULAR}")
    fa = _captions.font_path_arg(_captions.DMSANS_REGULAR)

    chain = _captions.build_filter_chain(blocks, fa)
    if not chain:
        # No captions — passthrough
        cmd = [FFMPEG, "-y", "-loglevel", "error", "-i", str(in_mp4),
               "-c", "copy", str(out)]
        if not run(cmd, "passthrough (no captions)"):
            sys.exit(1)
        return out

    # Write filter chain to temp, then run ffmpeg
    import tempfile, os as _os
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False, encoding="utf-8") as tf:
        tf.write(chain)
        fpath = tf.name
    try:
        cmd = [
            FFMPEG, "-y", "-loglevel", "error",
            "-i", str(in_mp4),
            "-filter_complex_script", fpath,
            "-map", "[vout]", "-map", "0:a",
            "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-r", "24",
            "-c:a", "copy",
            str(out),
        ]
        if not run(cmd, f"burn captions ({len(blocks)} blocks at y=0.70)"):
            sys.exit(1)
    finally:
        try:
            _os.unlink(fpath)
        except OSError:
            pass
    return out


# ---------------------------------------------------------------------------
# Step 8 — Loudnorm twopass to -14 LUFS
# ---------------------------------------------------------------------------

def loudnorm(in_mp4: Path, out_mp4: Path):
    """Two-pass loudnorm. Pre-compress with dynaudnorm to reduce dynamic range
    (Shorts have splice points → uneven loudness), then twopass to -14 LUFS,
    then corrective if still off-target.
    """
    # Pre-compress: dynaudnorm flattens the level so loudnorm can hit -14
    pre = SHORT1_BUILD / "07a-pre-dynaudnorm.mp4"
    pre_cmd = [
        FFMPEG, "-y", "-loglevel", "error",
        "-i", str(in_mp4),
        "-c:v", "copy",
        "-af", "dynaudnorm=p=0.92:m=15:s=20",
        "-c:a", "aac", "-b:a", "320k",
        str(pre),
    ]
    if not run(pre_cmd, "pre-compress dynaudnorm"):
        sys.exit(1)

    intermediate = SHORT1_BUILD / "07-loudnorm-pass1.mp4"
    cmd = [
        sys.executable,
        str(REPO / "generator" / "au-dealer-math" / "loudnorm-twopass.py"),
        str(pre), str(intermediate),
        "--video-copy",
    ]
    print(f"  [run] loudnorm twopass -> {intermediate.name}")
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="ignore")
    print(r.stdout)
    if r.returncode != 0:
        print("  STDERR:", r.stderr.strip()[-2000:])
        sys.exit(1)

    # Verify intermediate. If off-target, apply corrective pass.
    verify_cmd = [FFMPEG, "-i", str(intermediate), "-af", "ebur128=peak=true", "-f", "null", "-"]
    vr = subprocess.run(verify_cmd, capture_output=True, text=True, encoding="utf-8", errors="ignore")
    m = re.search(r"Integrated loudness:\s*\n\s*I:\s*(-?[\d.]+)", vr.stderr)
    measured = float(m.group(1)) if m else None
    print(f"  [verify pass1] integrated = {measured} LUFS")

    # Always apply: limiter-then-gain pass to land at -14 LUFS / TP ≤ -1.0 dBFS.
    # alimiter at limit=0.708 (= -3 dBFS) tames peaks aggressively; volume +1.5dB
    # recovers loudness. Empirically lands at -14.2 LUFS / -0.5 dBFS for splice
    # videos with mixed-source dynamics. (Single loudnorm twopass undershoots
    # because of the 0.5s hook frame's quiet music dragging integrated LUFS down.)
    print(f"  [post-loudnorm] applying alimiter+1.5dB to land at spec target")
    corrective_cmd = [
        FFMPEG, "-y", "-loglevel", "error",
        "-i", str(intermediate),
        "-c:v", "copy",
        "-af", "alimiter=limit=0.708:level=disabled,volume=+1.5dB",
        "-c:a", "aac", "-b:a", "320k",
        str(out_mp4),
    ]
    cr = subprocess.run(corrective_cmd, capture_output=True, text=True, encoding="utf-8", errors="ignore")
    if cr.returncode != 0:
        print("  STDERR:", cr.stderr.strip()[-1000:])
        sys.exit(1)

    # Final verify
    vr2 = subprocess.run([FFMPEG, "-i", str(out_mp4), "-af", "ebur128=peak=true", "-f", "null", "-"],
                          capture_output=True, text=True, encoding="utf-8", errors="ignore")
    m_i = re.search(r"Integrated loudness:\s*\n\s*I:\s*(-?[\d.]+)", vr2.stderr)
    m_p = re.search(r"True peak:\s*\n\s*Peak:\s*(-?[\d.]+)", vr2.stderr)
    fi = float(m_i.group(1)) if m_i else None
    fp = float(m_p.group(1)) if m_p else None
    print(f"  [final] integrated = {fi} LUFS · true peak = {fp} dBFS")
    if fi is not None and abs(fi + 14.0) > 1.0:
        print(f"  [WARN] still off-target by {fi+14.0:+.2f} LU after correction")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-captions", action="store_true",
                    help="Skip Step 7 (caption burn). Spliced video feeds directly into loudnorm.")
    args = ap.parse_args()

    print("=" * 70)
    print(f"AUDM V2 Short 1 — F&I Office build {'(NO CAPTIONS)' if args.no_captions else ''}")
    print("=" * 70)

    # Verify inputs
    for p in [V2_FINAL, OPEN_VO, CLOSE_VO]:
        if not p.exists():
            print(f"[FAIL] missing input: {p}")
            sys.exit(1)
    print(f"  V2 source : {V2_FINAL.name} ({probe_dur(V2_FINAL):.2f}s)")
    print(f"  Open VO   : {OPEN_VO.name} ({probe_dur(OPEN_VO):.2f}s)")
    print(f"  Close VO  : {CLOSE_VO.name} ({probe_dur(CLOSE_VO):.2f}s)")
    print()

    # 1. Hook frame
    print("--- 1/8 hook frame ($4,800 cream-on-charcoal) ---")
    hook = build_hook_frame()
    print(f"  [OK] {hook.name} ({probe_dur(hook):.2f}s)")
    print()

    # 2. Open clip (V2 footage + open VO)
    print("--- 2/8 OPEN clip ---")
    open_clip, open_dur = build_open_clip()
    print(f"  [OK] {open_clip.name} ({open_dur:.2f}s)")
    print()

    # 3. Middle clip (lifted from V2)
    print("--- 3/8 MIDDLE clip (lift V2 t=180.54-203.58s) ---")
    mid_clip, mid_dur = build_middle_clip()
    print(f"  [OK] {mid_clip.name} ({mid_dur:.2f}s)")
    print()

    # 4. Close clip (V2 footage + close VO + music fade)
    print("--- 4/8 CLOSE clip ---")
    close_clip, close_dur = build_close_clip()
    print(f"  [OK] {close_clip.name} ({close_dur:.2f}s)")
    print()

    # 5. Concat
    print("--- 5/8 splice (hook + open + middle + close) ---")
    spliced = concat_segments([hook, open_clip, mid_clip, close_clip])
    spliced_dur = probe_dur(spliced)
    print(f"  [OK] {spliced.name} ({spliced_dur:.2f}s)")
    print()

    if args.no_captions:
        # Skip Step 6 + 7 — feed spliced directly into loudnorm
        print("--- 6/8 SKIP transcriptions JSON (--no-captions) ---")
        print("--- 7/8 SKIP caption burn (--no-captions) ---")
        print()
        loudnorm_input = spliced
    else:
        # 6. Build Shorts transcriptions JSON
        print("--- 6/8 Shorts transcriptions JSON (mapped to spliced timeline) ---")
        trans = build_shorts_transcriptions(open_dur, mid_dur, close_dur)
        print(f"  [OK] {trans.name}")
        print()

        # 7. Burn captions
        print("--- 7/8 burn captions y=0.70 ---")
        captioned = burn_captions(spliced, trans)
        print(f"  [OK] {captioned.name} ({probe_dur(captioned):.2f}s)")
        print()
        loudnorm_input = captioned

    # 8. Loudnorm
    final = SHORTS_OUT / "audm-v2-short-1.mp4"
    print("--- 8/8 loudnorm twopass -> -14 LUFS ---")
    loudnorm(loudnorm_input, final)
    print()

    final_dur = probe_dur(final)
    final_size_mb = final.stat().st_size / (1024 * 1024)
    print("=" * 70)
    print(f"DONE: {final}")
    print(f"  Duration: {final_dur:.2f}s")
    print(f"  Size:     {final_size_mb:.1f} MB")
    print(f"  Captions: {'STRIPPED (option C)' if args.no_captions else 'burned y=0.70'}")
    print("=" * 70)


if __name__ == "__main__":
    main()
