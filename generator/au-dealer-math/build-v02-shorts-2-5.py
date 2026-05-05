"""Build AUDM V2 Shorts 2, 3, 4, 5 — same path-(a) pattern as Short 1.

Each Short = bespoke OPEN VO + lifted V2 middle + bespoke CLOSE VO,
spliced and (optionally) burned with captions, finalized to -14 LUFS.

Pattern lifted from build-v02-short-1.py — extended to handle 4 Shorts
parameterised by SHORTS dict. Each entry encodes:
  - lift window (start/end seconds in V2 source)
  - hook frame text (first-frame number/phrase)
  - bookend filenames (open/close)
  - source scene index in vo-transcriptions.json (for middle word timings)

Run: python generator/au-dealer-math/build-v02-shorts-2-5.py [--only 2|3|4|5] [--no-captions]

--no-captions: skip Step 7 (running sentence-block captions). Locked 2026-05-05
per option C — frame-1 number hook delivers sound-off lift; running captions
clash with Mac calm-authority + document-forensics DNA. V3+ default.

Outputs: video/out/shorts/audm-v2-short-{2,3,4,5}.mp4
"""

import argparse
import json
import re
import subprocess
import sys
import tempfile
import os
import importlib.util
from pathlib import Path

REPO = Path(r"C:\dev\Claude")
VIDEO_OUT = REPO / "video" / "out"
SHORTS_OUT = VIDEO_OUT / "shorts"
SHORTS_OUT.mkdir(parents=True, exist_ok=True)

V02_RENDERS = REPO / "content" / "au-dealer-math" / "scripts" / "v02-renders"
VOICE_SHORTS = V02_RENDERS / "voice-shorts"

# Pre-caption V2 master (audio pre-finalize but final loudnorm normalizes splice)
V2_FINAL = VIDEO_OUT / "audm-v2-finance-managers-office.mp4"   # 1920x1080 24fps

# Music bed (V2's locked HAAWK-safe YT Audio Library track)
MUSIC_BED = V02_RENDERS / "music" / "a-hand-in-the-dark-looped-ducked-soft-578s-v3.mp3"

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

CHARCOAL = "#2B2B2B"
CREAM    = "#F5EFE6"

HOOK_FRAME_DUR = 0.5
CLOSE_TAIL = 0.4

# Per-Short parameter table
# scene_idx is 0-based index in vo-transcriptions.json (Scene 4 = idx 3)
SHORTS = {
    2: {
        "label": "rate-range-3k",
        # V2 scene 4 (rateGame) — the $3k math beat
        # "But you only find out the floor exists if you push hard enough..."
        # → "...the additional interest cost on your side is roughly two to $3,000..."
        # Sentence-bounded: 218.36 → 241.24
        "lift_start": 218.36,
        "lift_end":   241.24,
        "scene_idx": 3,   # rateGame (scene_id=4, list index 3)
        "hook_text": "$3,000",
        "hook_fontsize": 240,
        "open_vo":  "short2-open.mp3",
        "close_vo": "short2-close.mp3",
    },
    3: {
        "label": "same-bank-different-outcomes",
        # V2 scene 4 — "Same bank, same approval, different outcomes" beat
        # "Not on some objective fair rate the finance manager arrived at on your pushback..."
        # → "...different outcomes. That's not a conspiracy."
        # Sentence-bounded: 281.68 → 301.00
        "lift_start": 281.68,
        "lift_end":   301.00,
        "scene_idx": 3,
        # Hook anchors on the 4-percentage-point spread (5% bank → 9% dealer pitch).
        # `%` is a drawtext special char that breaks rendering — use "POINTS" instead.
        "hook_text": "+4 POINTS",
        "hook_fontsize": 200,
        "open_vo":  "short3-open.mp3",
        "close_vo": "short3-close.mp3",
    },
    4: {
        "label": "aftercare-3k",
        # V2 scene 7 (signoff) — aftercare margin reveal
        # "After the medal gets agreed, and before you reach the finance manager..."
        # → "...at margins that make the front end gross look modest."
        # Sentence-bounded: 532.55 → 552.34
        "lift_start": 532.55,
        "lift_end":   552.34,
        "scene_idx": 6,   # signoff (scene_id=7, list index 6)
        "hook_text": "$3,000",
        "hook_fontsize": 240,
        "open_vo":  "short4-open.mp3",
        "close_vo": "short4-close.mp3",
    },
    5: {
        "label": "three-rooms",
        # V2 scene 3 (fnioffice) — "negotiated with three in sequence" beat
        # "Every finance manager I ever worked with was a commissioned salesperson..."
        # → "...They negotiated with three in sequence."
        # Sentence-bounded: 150.79 → 173.13 (= 22.34s)
        "lift_start": 150.79,
        "lift_end":   173.13,
        "scene_idx": 2,   # fnioffice (scene_id=3, list index 2)
        # 280pt overflows 1080 width — drop to 220pt to fit "3 ROOMS" with margin.
        "hook_text": "3 ROOMS",
        "hook_fontsize": 220,
        "open_vo":  "short5-open.mp3",
        "close_vo": "short5-close.mp3",
    },
}


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
# Caption module — load once, override y position per Short
# ---------------------------------------------------------------------------

sys.path.insert(0, str(REPO / "generator" / "au-dealer-math"))
_caption_spec = importlib.util.spec_from_file_location(
    "render_vN_captions",
    str(REPO / "generator" / "au-dealer-math" / "render-vN-captions.py"),
)
_captions = importlib.util.module_from_spec(_caption_spec)
_caption_spec.loader.exec_module(_captions)


# ---------------------------------------------------------------------------
# Per-Short build steps
# ---------------------------------------------------------------------------

def build_hook_frame(short_id: int, build_dir: Path) -> Path:
    """0.5s 1080x1920 charcoal background with hook text in cream."""
    cfg = SHORTS[short_id]
    out = build_dir / "01-hook-card.mp4"
    fa = font_arg(DMSANS_BOLD)
    text = cfg["hook_text"]
    fontsize = cfg["hook_fontsize"]
    cmd = [
        FFMPEG, "-y", "-loglevel", "error",
        "-f", "lavfi", "-i", f"color=c={CHARCOAL}:s=1080x1920:r=24:d={HOOK_FRAME_DUR}",
        "-ss", "5.0",
        "-i", str(MUSIC_BED),
        "-t", f"{HOOK_FRAME_DUR}",
        "-vf", (
            f"drawtext=fontfile='{fa}'"
            f":text='{text}'"
            f":fontcolor={CREAM}"
            f":fontsize={fontsize}"
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
    if not run(cmd, f"build hook card '{text}' @ {fontsize}pt"):
        sys.exit(1)
    return out


def build_open_clip(short_id: int, build_dir: Path) -> tuple[Path, float]:
    """OPEN bookend = V2 footage from t=0-3s + open VO + music bed."""
    cfg = SHORTS[short_id]
    open_vo_path = VOICE_SHORTS / cfg["open_vo"]
    open_vo_dur = probe_dur(open_vo_path)
    total = open_vo_dur + 0.3
    out = build_dir / "02-open.mp4"
    cmd = [
        FFMPEG, "-y", "-loglevel", "error",
        "-ss", "0.0",
        "-i", str(V2_FINAL),
        "-i", str(open_vo_path),
        "-t", f"{total:.3f}",
        "-filter_complex", (
            f"[0:v]split=2[orig][bg_src];"
            f"[bg_src]scale=1080:1920:force_original_aspect_ratio=increase,"
            f"crop=1080:1920,boxblur=20:5,eq=brightness=-0.20[bg];"
            f"[orig]scale=1080:-2[fg_scaled];"
            f"[bg][fg_scaled]overlay=(W-w)/2:(H-h)/2[v];"
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
    if not run(cmd, f"build open clip Short {short_id} ({total:.2f}s)"):
        sys.exit(1)
    return out, total


def build_middle_clip(short_id: int, build_dir: Path) -> tuple[Path, float]:
    """Lift V2 middle, blur-pad to 9:16, audio preserved."""
    cfg = SHORTS[short_id]
    out = build_dir / "03-middle.mp4"
    dur = cfg["lift_end"] - cfg["lift_start"]
    cmd = [
        FFMPEG, "-y", "-loglevel", "error",
        "-ss", f"{cfg['lift_start']:.3f}",
        "-i", str(V2_FINAL),
        "-t", f"{dur:.3f}",
        "-filter_complex", (
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
    if not run(cmd, f"build middle Short {short_id} (lift t={cfg['lift_start']:.2f}-{cfg['lift_end']:.2f}s, {dur:.2f}s)"):
        sys.exit(1)
    return out, dur


def build_close_clip(short_id: int, build_dir: Path) -> tuple[Path, float]:
    """CLOSE bookend = V2 footage at LIFT_END + close VO + music fade."""
    cfg = SHORTS[short_id]
    close_vo_path = VOICE_SHORTS / cfg["close_vo"]
    close_vo_dur = probe_dur(close_vo_path)
    total = close_vo_dur + CLOSE_TAIL
    out = build_dir / "04-close.mp4"
    fade_st = max(0.0, total - 1.5)
    cmd = [
        FFMPEG, "-y", "-loglevel", "error",
        "-ss", f"{cfg['lift_end']:.3f}",
        "-i", str(V2_FINAL),
        "-i", str(close_vo_path),
        "-t", f"{total:.3f}",
        "-filter_complex", (
            f"[0:v]split=2[orig][bg_src];"
            f"[bg_src]scale=1080:1920:force_original_aspect_ratio=increase,"
            f"crop=1080:1920,boxblur=20:5,eq=brightness=-0.20[bg];"
            f"[orig]scale=1080:-2[fg_scaled];"
            f"[bg][fg_scaled]overlay=(W-w)/2:(H-h)/2[v];"
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
    if not run(cmd, f"build close clip Short {short_id} ({total:.2f}s, fade in last 1.5s)"):
        sys.exit(1)
    return out, total


def concat_segments(parts: list, build_dir: Path) -> Path:
    out = build_dir / "05-spliced.mp4"
    list_file = build_dir / "_concat-list.txt"
    list_file.write_text("\n".join(f"file '{p.as_posix()}'" for p in parts), encoding="utf-8")
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


def build_shorts_transcriptions(short_id: int, open_dur: float, middle_dur: float,
                                  close_dur: float, build_dir: Path) -> Path:
    """
    Build a transcriptions JSON mapped to spliced timeline.
      - HOOK 0.0-0.5s: NO words
      - OPEN 0.5 → HOOK + open_dur: open VO words shifted to start at 0.5s
      - MIDDLE: V2 scene words (cfg.scene_idx), shifted to start at HOOK + open_dur
      - CLOSE: close VO words shifted to start at HOOK + open + middle
    """
    cfg = SHORTS[short_id]

    # Middle words: V2 scene at scene_idx
    with open(V02_RENDERS / "vo-transcriptions.json", encoding="utf-8") as f:
        v2_data = json.load(f)
    scene = v2_data["scenes"][cfg["scene_idx"]]
    middle_words = []
    middle_offset = HOOK_FRAME_DUR + open_dur
    for w in scene["words"]:
        if cfg["lift_start"] <= w["timeline_start"] < cfg["lift_end"]:
            new_start = (w["timeline_start"] - cfg["lift_start"]) + middle_offset
            new_end   = (w["timeline_end"]   - cfg["lift_start"]) + middle_offset
            if new_end <= middle_offset + middle_dur + 0.05:
                middle_words.append({
                    "word": w["word"],
                    "timeline_start": new_start,
                    "timeline_end": new_end,
                })

    # Open VO words
    open_timings_path = VOICE_SHORTS / cfg["open_vo"].replace(".mp3", ".timings.json")
    with open(open_timings_path, encoding="utf-8") as f:
        open_data = json.load(f)
    open_words = []
    for w in open_data["words"]:
        offset = HOOK_FRAME_DUR
        open_words.append({
            "word": w["word"],
            "timeline_start": w["timeline_start"] + offset,
            "timeline_end":   w["timeline_end"]   + offset,
        })

    # Close VO words
    close_timings_path = VOICE_SHORTS / cfg["close_vo"].replace(".mp3", ".timings.json")
    with open(close_timings_path, encoding="utf-8") as f:
        close_data = json.load(f)
    close_words = []
    close_offset = HOOK_FRAME_DUR + open_dur + middle_dur
    for w in close_data["words"]:
        close_words.append({
            "word": w["word"],
            "timeline_start": w["timeline_start"] + close_offset,
            "timeline_end":   w["timeline_end"]   + close_offset,
        })

    out = build_dir / "shorts-transcriptions.json"
    out.write_text(json.dumps({
        "scenes": [
            {"title": "Open",   "words": open_words},
            {"title": "Middle", "words": middle_words},
            {"title": "Close",  "words": close_words},
        ]
    }, indent=2), encoding="utf-8")
    return out


def burn_captions(in_mp4: Path, transcriptions: Path, build_dir: Path) -> Path:
    """Use render-vN-captions internals but override Y_CENTER_EXPR to h*0.70."""
    out = build_dir / "06-captioned.mp4"
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
        cmd = [FFMPEG, "-y", "-loglevel", "error", "-i", str(in_mp4),
               "-c", "copy", str(out)]
        if not run(cmd, "passthrough (no captions)"):
            sys.exit(1)
        return out

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
            os.unlink(fpath)
        except OSError:
            pass
    return out


def measure_loudness_stats(src: Path) -> dict:
    """Pass-1 measurement: returns ffmpeg loudnorm JSON dict with measured stats."""
    cmd = [
        FFMPEG, "-i", str(src),
        "-af", "loudnorm=I=-14:TP=-1.0:LRA=11:print_format=json",
        "-f", "null", "-",
    ]
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="ignore")
    m = re.search(r"\{[^{]*input_i[^}]*\}", r.stderr, re.DOTALL)
    if not m:
        print("PASS-1 STDERR:", r.stderr[-2000:])
        raise RuntimeError("loudnorm pass-1 measurement failed")
    return json.loads(m.group(0))


def measure_simple(src: Path) -> tuple[float, float]:
    """Quick ebur128 measure: returns (integrated_lufs, true_peak_dbfs)."""
    cmd = [FFMPEG, "-i", str(src), "-af", "ebur128=peak=true", "-f", "null", "-"]
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="ignore")
    m_i = re.search(r"Integrated loudness:\s*\n\s*I:\s*(-?[\d.]+)", r.stderr)
    m_p = re.search(r"True peak:\s*\n\s*Peak:\s*(-?[\d.]+)", r.stderr)
    return (float(m_i.group(1)) if m_i else None,
            float(m_p.group(1)) if m_p else None)


def loudnorm(in_mp4: Path, out_mp4: Path, build_dir: Path):
    """Iterative volume-lift + alimiter approach with auto-tuning.

    Loudnorm filter undershoots when LRA is wide (splice videos with deep
    silence in hook frame). Direct approach: measure, compute exact gain
    needed, lift via volume filter, clamp peaks via alimiter, verify.
    Iterate up to 3 times if undershooting.
    """
    # Step 1: pre-compress dynamic range
    pre = build_dir / "07a-pre-dynaudnorm.mp4"
    pre_cmd = [
        FFMPEG, "-y", "-loglevel", "error",
        "-i", str(in_mp4),
        "-c:v", "copy",
        "-af", "dynaudnorm=p=0.93:m=10:s=15:g=15",
        "-c:a", "aac", "-b:a", "320k",
        str(pre),
    ]
    if not run(pre_cmd, "pre-compress dynaudnorm"):
        sys.exit(1)

    # Step 2: iterative lift loop — measure, compute gain, apply, repeat
    current = pre
    target_lufs = -14.0
    target_tp = -1.0
    # alimiter at limit=0.794 (= -2.0 dBFS) — extra margin since alimiter has
    # 5ms attack and brief transients can exceed limit by 0.5-1 dBFS in practice.
    # Setting -2 dBFS leaves headroom so worst-case peaks land around -1 dBFS.
    limiter_arg = "alimiter=limit=0.794:attack=2:release=30:level=disabled"

    fi = fp = None
    for attempt in range(1, 4):  # max 3 iterations
        cur_lufs, cur_tp = measure_simple(current)
        print(f"  [iter {attempt}] current I={cur_lufs} LUFS  TP={cur_tp} dBFS")

        # If within spec (and TP <= target), stop and copy current as final
        if cur_lufs is not None and abs(cur_lufs - target_lufs) <= 0.7 and \
           cur_tp is not None and cur_tp <= target_tp + 0.05:  # allow 0.05 dBFS slack
            print(f"  [iter {attempt}] within spec — copying to final")
            cp_cmd = [FFMPEG, "-y", "-loglevel", "error", "-i", str(current),
                      "-c", "copy", str(out_mp4)]
            if not run(cp_cmd, "copy to final"):
                sys.exit(1)
            return cur_lufs, cur_tp

        # Compute gain needed
        if cur_lufs is None:
            print(f"  [iter {attempt}] could not measure — aborting iteration")
            break
        gain_db = target_lufs - cur_lufs
        # Cap gain per iteration to avoid wild swings
        gain_db = max(-3.0, min(8.0, gain_db))
        print(f"  [iter {attempt}] applying volume {gain_db:+.2f} dB then alimiter@-1dBFS")

        nxt = build_dir / f"07{chr(ord('b') + attempt)}-iter{attempt}.mp4"
        af = f"volume={gain_db:+.2f}dB,{limiter_arg}"
        lift_cmd = [
            FFMPEG, "-y", "-loglevel", "error",
            "-i", str(current),
            "-c:v", "copy",
            "-af", af,
            "-c:a", "aac", "-b:a", "320k",
            str(nxt),
        ]
        if not run(lift_cmd, f"iter {attempt} lift+limit"):
            sys.exit(1)
        current = nxt
        fi, fp = measure_simple(current)

    # Last attempt — copy to final regardless
    print(f"  [final after iterations] I={fi}  TP={fp}")
    if current != out_mp4:
        cp_cmd = [FFMPEG, "-y", "-loglevel", "error", "-i", str(current),
                  "-c", "copy", str(out_mp4)]
        if not run(cp_cmd, "copy to final"):
            sys.exit(1)
    if fi is not None and abs(fi - target_lufs) > 2.0:
        print(f"  [WARN] off-target by {fi - target_lufs:+.2f} LU after iteration")
    # YouTube spec target_tp = -1.0 dBFS but tolerance is +1 dB (i.e. up to 0 dBFS
    # is accepted before clipping risk). Warn only if above 0 dBFS (actual clipping).
    if fp is not None and fp > 0.0:
        print(f"  [WARN] true peak {fp} dBFS exceeds 0 dBFS — CLIPPING RISK")
    elif fp is not None and fp > target_tp:
        print(f"  [info] true peak {fp} dBFS slightly above -1.0 spec but no clipping")
    return fi, fp


def build_short(short_id: int, no_captions: bool = False):
    cfg = SHORTS[short_id]
    print("=" * 70)
    print(f"AUDM V2 Short {short_id} — {cfg['label']} {'(NO CAPTIONS)' if no_captions else ''}")
    print("=" * 70)

    build_dir = V02_RENDERS / f"short{short_id}-build"
    build_dir.mkdir(parents=True, exist_ok=True)

    # Verify inputs
    open_vo_path  = VOICE_SHORTS / cfg["open_vo"]
    close_vo_path = VOICE_SHORTS / cfg["close_vo"]
    for p in [V2_FINAL, open_vo_path, close_vo_path]:
        if not p.exists():
            print(f"[FAIL] missing input: {p}")
            sys.exit(1)
    print(f"  V2 source : {V2_FINAL.name}")
    print(f"  Open VO   : {cfg['open_vo']} ({probe_dur(open_vo_path):.2f}s)")
    print(f"  Close VO  : {cfg['close_vo']} ({probe_dur(close_vo_path):.2f}s)")
    print(f"  Lift     : t={cfg['lift_start']:.2f}-{cfg['lift_end']:.2f}s ({cfg['lift_end']-cfg['lift_start']:.2f}s)")
    print(f"  Hook      : '{cfg['hook_text']}' @ {cfg['hook_fontsize']}pt")
    print()

    print(f"--- 1/8 hook frame ('{cfg['hook_text']}') ---")
    hook = build_hook_frame(short_id, build_dir)
    print(f"  [OK] {hook.name} ({probe_dur(hook):.2f}s)")
    print()

    print(f"--- 2/8 OPEN clip ---")
    open_clip, open_dur = build_open_clip(short_id, build_dir)
    print(f"  [OK] {open_clip.name} ({open_dur:.2f}s)")
    print()

    print(f"--- 3/8 MIDDLE clip ---")
    mid_clip, mid_dur = build_middle_clip(short_id, build_dir)
    print(f"  [OK] {mid_clip.name} ({mid_dur:.2f}s)")
    print()

    print(f"--- 4/8 CLOSE clip ---")
    close_clip, close_dur = build_close_clip(short_id, build_dir)
    print(f"  [OK] {close_clip.name} ({close_dur:.2f}s)")
    print()

    print(f"--- 5/8 splice (hook + open + middle + close) ---")
    spliced = concat_segments([hook, open_clip, mid_clip, close_clip], build_dir)
    spliced_dur = probe_dur(spliced)
    print(f"  [OK] {spliced.name} ({spliced_dur:.2f}s)")
    print()

    if no_captions:
        print(f"--- 6/8 SKIP transcriptions JSON (--no-captions) ---")
        print(f"--- 7/8 SKIP caption burn (--no-captions) ---")
        print()
        loudnorm_input = spliced
    else:
        print(f"--- 6/8 Shorts transcriptions JSON ---")
        trans = build_shorts_transcriptions(short_id, open_dur, mid_dur, close_dur, build_dir)
        print(f"  [OK] {trans.name}")
        print()

        print(f"--- 7/8 burn captions y=0.70 ---")
        captioned = burn_captions(spliced, trans, build_dir)
        print(f"  [OK] {captioned.name} ({probe_dur(captioned):.2f}s)")
        print()
        loudnorm_input = captioned

    final = SHORTS_OUT / f"audm-v2-short-{short_id}.mp4"
    print(f"--- 8/8 loudnorm twopass -> -14 LUFS ---")
    fi, fp = loudnorm(loudnorm_input, final, build_dir)
    print()

    final_dur = probe_dur(final)
    final_size_mb = final.stat().st_size / (1024 * 1024)
    print("=" * 70)
    print(f"DONE Short {short_id}: {final}")
    print(f"  Duration: {final_dur:.2f}s")
    print(f"  Size:     {final_size_mb:.1f} MB")
    print(f"  Loudness: {fi} LUFS · {fp} dBFS")
    print(f"  Captions: {'STRIPPED (option C)' if no_captions else 'burned y=0.70'}")
    print("=" * 70)
    print()
    return {
        "short_id": short_id,
        "duration_s": final_dur,
        "size_mb": final_size_mb,
        "lufs": fi,
        "tp_dbfs": fp,
        "out_path": str(final),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", type=int, choices=[2, 3, 4, 5], default=None,
                    help="Build only one Short (2, 3, 4, or 5). Default: all.")
    ap.add_argument("--no-captions", action="store_true",
                    help="Skip Step 7 (caption burn). Spliced video feeds directly into loudnorm.")
    args = ap.parse_args()
    targets = [args.only] if args.only else [2, 3, 4, 5]

    results = []
    for sid in targets:
        try:
            results.append(build_short(sid, no_captions=args.no_captions))
        except SystemExit as e:
            # build_short calls sys.exit(1) on failure — capture and continue with remaining Shorts
            print(f"[FAIL] Short {sid} failed (sys.exit({e.code})) — continuing with remaining targets")
            results.append({"short_id": sid, "failed": True})
        except Exception as e:
            print(f"[FAIL] Short {sid} threw exception: {e}")
            results.append({"short_id": sid, "failed": True, "error": str(e)})

    print("\n" + "=" * 70)
    print("BATCH SUMMARY")
    print("=" * 70)
    for r in results:
        if r.get("failed"):
            print(f"  Short {r['short_id']}: FAILED — {r.get('error', 'see log')}")
        else:
            print(f"  Short {r['short_id']}: {r['duration_s']:.2f}s · {r['size_mb']:.1f} MB · {r['lufs']} LUFS / {r['tp_dbfs']} dBFS")


if __name__ == "__main__":
    main()
