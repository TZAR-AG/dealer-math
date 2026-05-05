"""Re-render AUDM V2 Shorts (1-5) with FIXED audio chain.

Diagnosis (2026-05-05):
  - Original Shorts had a 12-15 dB music-level jump at bookend->middle splice
    seams (bookends used [0:a]volume=0.18 to duck V2's mixed audio; middle used
    V2 audio at volume=1.0).
  - 4-stage compression chain (dynaudnorm + loudnorm + alimiter + +1.5dB) was
    pumping + raising noise floor.
  - Output sample rate was 96 kHz (unintentional).

Fix architecture:
  Each Short = 4 audio segments concatenated with 100ms acrossfade between:
    1. Hook frame (0.5s)         — music_bed slice only, fade-in 0.1s
    2. Bookend OPEN (~3s)        — music_bed (continued slice) + bookend_open_VO mixed
    3. Lifted MIDDLE (~22-26s)   — V2's mixed audio at full level (Mac VO + same music)
    4. Bookend CLOSE (~3s)       — music_bed (continued slice) + bookend_close_VO mixed,
                                   afade out 1.5s before end

  Music continuity: music_bed file is the SAME track that V2 has internally.
  Both bookends and V2 middle play this track at the same pre-ducked level
  (music bed solo = -44 LUFS, V2 mix middle = -24 LUFS dominated by Mac VO at
  ~-22 LUFS solo). Bookend mix lands at ~-22 LUFS. No level cliff at seams.

  Single loudnorm-twopass at the end -> -14 LUFS / TP -1.0 / LRA 7.
  No dynaudnorm pre-compress. No alimiter post. No volume boost.

  Output sample rate locked to 48 kHz (V2 source rate).

Video stream is UNCHANGED. We re-use existing per-segment intermediate MP4s
(01-hook-card.mp4, 02-open.mp4, 03-middle.mp4, 04-close.mp4) for VIDEO only,
strip their audio, build new audio per segment, mux, concat with acrossfade,
loudnorm.

Run:  python generator/au-dealer-math/build-v02-shorts-audiofix.py [--only N]

Outputs (overwrite): video/out/shorts/audm-v2-short-{1..5}.mp4
Verify dir:          content/au-dealer-math/scripts/v02-renders/short{N}-build/audio-verify/
"""

import argparse
import json
import re
import subprocess
import sys
import os
from pathlib import Path

REPO = Path(r"C:\dev\Claude")
VIDEO_OUT = REPO / "video" / "out"
SHORTS_OUT = VIDEO_OUT / "shorts"
SHORTS_OUT.mkdir(parents=True, exist_ok=True)

V02_RENDERS = REPO / "content" / "au-dealer-math" / "scripts" / "v02-renders"
VOICE_SHORTS = V02_RENDERS / "voice-shorts"

V2_FINAL = VIDEO_OUT / "audm-v2-finance-managers-office.mp4"
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

HOOK_FRAME_DUR = 0.5
CLOSE_TAIL = 0.4
SEAM_XFADE = 0.10  # 100ms acrossfade at every concat boundary

# Music bed source-time anchor per Short. We pull a contiguous slice from the
# bed starting at this offset for the WHOLE Short (hook + open + close use the
# same continuous slice, so the bed feels like one piece of music). The middle
# uses V2's mix which has the SAME track inside, at the same ducked level.
# Different start offsets per Short so each Short has a different musical phrase
# at its hook (avoids 5 Shorts all starting on the exact same bar).
MUSIC_BED_START = {
    1:  60.0,
    2: 120.0,
    3: 200.0,
    4: 280.0,
    5: 360.0,
}

# Bookend music level: the bed file's solo level (filename "ducked-soft") sits
# at ~-47 dB mean. V2's master mix has the same track at ~-45 dB mean during
# bed-alone moments (e.g. V2 t=180.0). To match V2's internal bed level during
# bookend VO pauses (the audible-music-cliff problem), play bed at 0.6 (~-4 dB
# down from unity) so bookend pauses sit at ~-50 dB mean, matching V2's quietest
# bed moments. Bookend VO stays at full level — its solo LUFS (~-22) already
# matches V2 middle's mixed LUFS (~-24).
BED_VOLUME = 0.6
VO_VOLUME = 1.0

# Per-Short config (V2 lift windows + bookend filenames)
SHORTS = {
    1: {
        "label": "fni-office",
        "lift_start": 180.54, "lift_end": 203.58,
        "open_vo": "short1-open.mp3", "close_vo": "short1-close.mp3",
    },
    2: {
        "label": "rate-range-3k",
        "lift_start": 218.36, "lift_end": 241.24,
        "open_vo": "short2-open.mp3", "close_vo": "short2-close.mp3",
    },
    3: {
        "label": "same-bank-different-outcomes",
        "lift_start": 281.68, "lift_end": 301.00,
        "open_vo": "short3-open.mp3", "close_vo": "short3-close.mp3",
    },
    4: {
        "label": "aftercare-3k",
        "lift_start": 532.55, "lift_end": 552.34,
        "open_vo": "short4-open.mp3", "close_vo": "short4-close.mp3",
    },
    5: {
        "label": "three-rooms",
        "lift_start": 150.79, "lift_end": 173.13,
        "open_vo": "short5-open.mp3", "close_vo": "short5-close.mp3",
    },
}


def run(cmd: list, what: str, fatal: bool = True) -> bool:
    print(f"  [run] {what}")
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="ignore")
    if r.returncode != 0:
        print(f"  [FAIL] {what}")
        print("  STDERR:", r.stderr.strip()[-2000:])
        if fatal:
            sys.exit(1)
        return False
    return True


def probe_dur(p: Path) -> float:
    cmd = [FFPROBE, "-v", "error", "-show_entries", "format=duration",
           "-of", "csv=p=0", str(p)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    return float(r.stdout.strip())


def measure_simple(src: Path):
    cmd = [FFMPEG, "-i", str(src), "-af", "ebur128=peak=true", "-f", "null", "-"]
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="ignore")
    m_i = re.search(r"Integrated loudness:\s*\n\s*I:\s*(-?[\d.]+)", r.stderr)
    m_p = re.search(r"True peak:\s*\n\s*Peak:\s*(-?[\d.]+)", r.stderr)
    return (float(m_i.group(1)) if m_i else None,
            float(m_p.group(1)) if m_p else None)


# ---------------------------------------------------------------------------
# Per-segment audio builders. Output 48 kHz stereo AAC, locked level.
# Each returns a path to a video+audio MP4 segment ready to concat.
# ---------------------------------------------------------------------------

def build_hook_segment(short_id: int, build_dir: Path,
                       bed_offset: float) -> Path:
    """0.5s segment: existing hook video frames + music_bed slice (faded in)."""
    src_video = build_dir / "01-hook-card.mp4"
    out = build_dir / "audiofix-01-hook.mp4"
    cmd = [
        FFMPEG, "-y", "-loglevel", "error",
        "-i", str(src_video),                    # video source (will discard audio)
        "-ss", f"{bed_offset:.3f}",
        "-i", str(MUSIC_BED),
        "-t", f"{HOOK_FRAME_DUR:.3f}",
        "-filter_complex", (
            f"[1:a]atrim=0:{HOOK_FRAME_DUR:.3f},asetpts=PTS-STARTPTS,"
            f"aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=stereo,"
            f"volume={BED_VOLUME},"
            f"afade=t=in:st=0:d=0.10[a]"
        ),
        "-map", "0:v:0", "-map", "[a]",
        "-c:v", "libx264", "-preset", "medium", "-crf", "18",
        "-pix_fmt", "yuv420p", "-r", "24",
        "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
        "-t", f"{HOOK_FRAME_DUR:.3f}",
        str(out),
    ]
    run(cmd, f"audiofix hook segment ({HOOK_FRAME_DUR}s, bed@{bed_offset:.1f}s)")
    return out


def build_open_segment(short_id: int, build_dir: Path,
                       bed_offset: float) -> tuple[Path, float]:
    """OPEN bookend: existing OPEN video frames + (music_bed + bookend_open_VO) mixed.

    NOTE 2026-05-05: ElevenLabs Mac VO renders MONO. Without explicit upmix,
    ffmpeg amix pads mono VO to LEFT channel only and silences RIGHT. We
    explicitly upmix mono -> stereo via pan filter (c0=c0, c1=c0) BEFORE amix.
    Always apply this pattern for any mono-into-stereo audio chain.
    """
    cfg = SHORTS[short_id]
    src_video = build_dir / "02-open.mp4"
    open_vo_path = VOICE_SHORTS / cfg["open_vo"]
    seg_dur = probe_dur(src_video)   # use the EXISTING segment duration (video already correct)
    out = build_dir / "audiofix-02-open.mp4"
    cmd = [
        FFMPEG, "-y", "-loglevel", "error",
        "-i", str(src_video),
        "-ss", f"{bed_offset:.3f}",
        "-i", str(MUSIC_BED),
        "-t", f"{seg_dur:.3f}",
        "-i", str(open_vo_path),
        "-filter_complex", (
            # Bed slice trimmed to seg_dur, normalised, leveled
            f"[1:a]atrim=0:{seg_dur:.3f},asetpts=PTS-STARTPTS,"
            f"aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=stereo,"
            f"volume={BED_VOLUME}[bed];"
            # VO MUST be upmixed mono->stereo BEFORE amix. pan=stereo|c0=c0|c1=c0
            # explicitly says: out-L = in-L (mono), out-R = in-L (mono). Both
            # stereo channels carry the mono VO at full level. Without this,
            # amix pads to LEFT only and Right is silent during VO.
            f"[2:a]aformat=channel_layouts=mono,"
            f"pan=stereo|c0=c0|c1=c0,"
            f"aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=stereo,"
            f"volume={VO_VOLUME},apad,atrim=0:{seg_dur:.3f},"
            f"asetpts=PTS-STARTPTS[vo];"
            # Mix WITHOUT renormalisation — preserve absolute level. dropout=0
            # so when VO drops out, bed doesn't suddenly boost (which is the
            # entire problem we're fixing).
            f"[bed][vo]amix=inputs=2:duration=longest:dropout_transition=0:normalize=0[a]"
        ),
        "-map", "0:v:0", "-map", "[a]",
        "-c:v", "libx264", "-preset", "medium", "-crf", "18",
        "-pix_fmt", "yuv420p", "-r", "24",
        "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
        "-t", f"{seg_dur:.3f}",
        str(out),
    ]
    run(cmd, f"audiofix open segment ({seg_dur:.2f}s)")
    return out, seg_dur


def build_middle_segment(short_id: int, build_dir: Path) -> tuple[Path, float]:
    """MIDDLE: existing middle video + V2's mixed audio at full level (NO duck).

    NOTE 2026-05-05: V2 master audio was rendered MONO-ON-LEFT (FL ~-24 dB,
    FR ~-46 dB — 22 dB delta). The V2 source itself has the same mono-on-left
    bug as the bookend VO chain. We must upmix the V2 left channel to both
    stereo channels here too, otherwise the lifted middle plays VO+music on
    LEFT only. Use channelsplit + pan-from-FL pattern.
    """
    cfg = SHORTS[short_id]
    src_video = build_dir / "03-middle.mp4"
    seg_dur = probe_dur(src_video)
    lift_start = cfg["lift_start"]
    out = build_dir / "audiofix-03-middle.mp4"
    # V2 audio is already at -24 LUFS mixed (Mac VO + music) on LEFT channel.
    # Take only the LEFT channel of V2 and duplicate it into both stereo
    # channels via pan. This guarantees L=R for the middle segment.
    cmd = [
        FFMPEG, "-y", "-loglevel", "error",
        "-i", str(src_video),                       # video frames (we keep them)
        "-ss", f"{lift_start:.3f}",
        "-i", str(V2_FINAL),                        # V2 audio (re-extract at lift point)
        "-t", f"{seg_dur:.3f}",
        "-filter_complex", (
            # Take V2 input's stereo audio. V2 left has the actual content
            # (Mac VO + music ~-24 LUFS); right is near-silent (~-46 LUFS).
            # pan=stereo|c0=c0|c1=c0 reads only input channel 0 (left) and
            # writes it to both output channels (centre-mono).
            f"[1:a]atrim=0:{seg_dur:.3f},asetpts=PTS-STARTPTS,"
            f"pan=stereo|c0=c0|c1=c0,"
            f"aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=stereo[a]"
        ),
        "-map", "0:v:0", "-map", "[a]",
        "-c:v", "libx264", "-preset", "medium", "-crf", "18",
        "-pix_fmt", "yuv420p", "-r", "24",
        "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
        "-t", f"{seg_dur:.3f}",
        str(out),
    ]
    run(cmd, f"audiofix middle segment ({seg_dur:.2f}s, V2 audio full level)")
    return out, seg_dur


def build_close_segment(short_id: int, build_dir: Path,
                        bed_offset: float) -> tuple[Path, float]:
    """CLOSE bookend: existing CLOSE video + (music_bed + close_VO) mixed,
       afade out 1.5s before end.

    NOTE 2026-05-05: Same mono->stereo upmix as build_open_segment. Bookend VO
    is mono; must be upmixed via pan=stereo|c0=c0|c1=c0 BEFORE amix.
    """
    cfg = SHORTS[short_id]
    src_video = build_dir / "04-close.mp4"
    close_vo_path = VOICE_SHORTS / cfg["close_vo"]
    seg_dur = probe_dur(src_video)
    fade_st = max(0.0, seg_dur - 1.5)
    out = build_dir / "audiofix-04-close.mp4"
    cmd = [
        FFMPEG, "-y", "-loglevel", "error",
        "-i", str(src_video),
        "-ss", f"{bed_offset:.3f}",
        "-i", str(MUSIC_BED),
        "-t", f"{seg_dur:.3f}",
        "-i", str(close_vo_path),
        "-filter_complex", (
            f"[1:a]atrim=0:{seg_dur:.3f},asetpts=PTS-STARTPTS,"
            f"aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=stereo,"
            f"volume={BED_VOLUME}[bed];"
            # Mono VO -> stereo upmix BEFORE amix (see build_open_segment notes)
            f"[2:a]aformat=channel_layouts=mono,"
            f"pan=stereo|c0=c0|c1=c0,"
            f"aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=stereo,"
            f"volume={VO_VOLUME},apad,atrim=0:{seg_dur:.3f},"
            f"asetpts=PTS-STARTPTS[vo];"
            f"[bed][vo]amix=inputs=2:duration=longest:dropout_transition=0:normalize=0,"
            f"afade=t=out:st={fade_st:.3f}:d=1.5[a]"
        ),
        "-map", "0:v:0", "-map", "[a]",
        "-c:v", "libx264", "-preset", "medium", "-crf", "18",
        "-pix_fmt", "yuv420p", "-r", "24",
        "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
        "-t", f"{seg_dur:.3f}",
        str(out),
    ]
    run(cmd, f"audiofix close segment ({seg_dur:.2f}s, fade in last 1.5s)")
    return out, seg_dur


# ---------------------------------------------------------------------------
# Concat with acrossfade between adjacent segments — single ffmpeg pass.
# ---------------------------------------------------------------------------

def concat_with_xfade(parts: list, durs: list, build_dir: Path) -> Path:
    """Concat 4 segments with 100ms acrossfade at each boundary.

    Use the ffmpeg concat demuxer for VIDEO (lossless if streams match), but
    render an audio-only chain that does acrossfade between segments. Then mux
    audio onto the concatenated video.

    Cleanest path: single ffmpeg call with 4 inputs, building both:
      - video chain: concat filter (fast, no re-encode of internal codec data)
      - audio chain: acrossfade ladder

    But concat filter requires all videos to have same stream params + would
    re-encode anyway. Simpler and equally good: encode the full thing with one
    filter_complex.
    """
    out = build_dir / "audiofix-05-spliced.mp4"

    # Build filter_complex:
    #   videos: [0:v][1:v][2:v][3:v]concat=n=4:v=1:a=0[vout]
    #   audios: ladder of acrossfade
    n = len(parts)
    if n != 4:
        raise RuntimeError(f"Expected 4 segments, got {n}")

    # Video concat (no transition needed — video should cut hard, music covers seam).
    # Force SAR=1:1 on each input — segments from blur-pad have SAR 10240:10239,
    # hook card has SAR 1:1, and concat filter rejects mismatched SARs.
    v_norm = "".join(f"[{i}:v]setsar=1[v{i}];" for i in range(n))
    v_concat_in = "".join(f"[v{i}]" for i in range(n))
    v_concat = v_norm + v_concat_in + f"concat=n={n}:v=1:a=0[vout]"

    # Audio acrossfade ladder:
    #   [0:a][1:a]acrossfade=d=X[a01]
    #   [a01][2:a]acrossfade=d=X[a012]
    #   [a012][3:a]acrossfade=d=X[aout]
    a_steps = []
    prev = "[0:a]"
    for i in range(1, n):
        if i == n - 1:
            label = "[aout]"
        else:
            label = f"[a0{i}]"
        a_steps.append(f"{prev}[{i}:a]acrossfade=d={SEAM_XFADE}:c1=tri:c2=tri{label}")
        prev = label
    a_chain = ";".join(a_steps)

    fc = f"{v_concat};{a_chain}"

    cmd_inputs = []
    for p in parts:
        cmd_inputs += ["-i", str(p)]

    cmd = [FFMPEG, "-y", "-loglevel", "error"] + cmd_inputs + [
        "-filter_complex", fc,
        "-map", "[vout]", "-map", "[aout]",
        "-c:v", "libx264", "-preset", "medium", "-crf", "18",
        "-pix_fmt", "yuv420p", "-r", "24",
        "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
        str(out),
    ]
    run(cmd, f"concat with {SEAM_XFADE*1000:.0f}ms acrossfade ({n} segments)")

    # acrossfade SHORTENS the timeline by xfade_dur per join. Verify duration.
    actual = probe_dur(out)
    expected_no_xfade = sum(durs)
    expected_with_xfade = expected_no_xfade - SEAM_XFADE * (n - 1)
    print(f"  [verify] concat duration: {actual:.3f}s "
          f"(expected ~{expected_with_xfade:.3f}s, naive sum {expected_no_xfade:.3f}s)")
    return out


# ---------------------------------------------------------------------------
# Single loudnorm-twopass to -14 LUFS / TP -1.0 / LRA 7. Force 48 kHz output.
# ---------------------------------------------------------------------------

def loudnorm_final(in_mp4: Path, out_mp4: Path, build_dir: Path) -> tuple:
    """Single loudnorm-twopass. No pre-compression, no post-limiter, no boost.
    Force 48 kHz output by re-running through ffmpeg if needed.
    """
    intermediate = build_dir / "audiofix-06-loudnorm.mp4"
    cmd = [
        sys.executable,
        str(REPO / "generator" / "au-dealer-math" / "loudnorm-twopass.py"),
        str(in_mp4), str(intermediate),
        "--video-copy",
    ]
    print(f"  [run] loudnorm-twopass -> {intermediate.name}")
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="ignore")
    print(r.stdout)
    if r.returncode != 0:
        print("  STDERR:", r.stderr.strip()[-2000:])
        sys.exit(1)

    # Verify sample rate; if not 48 kHz, re-encode audio to 48 kHz (video copy).
    probe_cmd = [FFPROBE, "-v", "error", "-select_streams", "a:0",
                 "-show_entries", "stream=sample_rate", "-of", "csv=p=0",
                 str(intermediate)]
    sr_str = subprocess.run(probe_cmd, capture_output=True, text=True).stdout.strip()
    sr = int(sr_str) if sr_str.isdigit() else 0
    print(f"  [verify] intermediate sample_rate = {sr} Hz")

    if sr != 48000:
        print(f"  [fix] re-encoding audio to 48 kHz")
        fix_cmd = [
            FFMPEG, "-y", "-loglevel", "error",
            "-i", str(intermediate),
            "-c:v", "copy",
            "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
            str(out_mp4),
        ]
        run(fix_cmd, "force 48 kHz audio")
    else:
        # Just copy intermediate to final
        cp_cmd = [FFMPEG, "-y", "-loglevel", "error", "-i", str(intermediate),
                  "-c", "copy", str(out_mp4)]
        run(cp_cmd, "copy intermediate to final")

    fi, fp = measure_simple(out_mp4)
    print(f"  [final] integrated = {fi} LUFS · true peak = {fp} dBFS")
    return fi, fp


# ---------------------------------------------------------------------------
# RMS plot for verify
# ---------------------------------------------------------------------------

def export_rms_plot(short_id: int, mp4: Path, verify_dir: Path,
                    seam_timestamps: list):
    """Extract audio, compute 0.5s-window RMS via ffmpeg astats, plot."""
    import wave
    import struct
    try:
        import numpy as np
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print(f"  [skip] matplotlib/numpy missing — no RMS plot")
        return None

    # Decode audio to mono 8 kHz wav for fast RMS calc
    wav_path = verify_dir / f"_short{short_id}-rms-source.wav"
    decode_cmd = [
        FFMPEG, "-y", "-loglevel", "error",
        "-i", str(mp4),
        "-ac", "1", "-ar", "8000", "-c:a", "pcm_s16le",
        str(wav_path),
    ]
    run(decode_cmd, "decode audio for RMS plot", fatal=False)
    if not wav_path.exists():
        return None

    with wave.open(str(wav_path), "rb") as wf:
        n = wf.getnframes()
        raw = wf.readframes(n)
    samples = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0
    sr = 8000
    win_s = 0.10
    win = int(sr * win_s)
    if len(samples) < win:
        return None
    # RMS in dBFS, sliding hop = win/2
    hop = max(1, win // 2)
    rms_db = []
    times = []
    for i in range(0, len(samples) - win, hop):
        chunk = samples[i:i + win]
        rms = float(np.sqrt(np.mean(chunk * chunk)) + 1e-12)
        rms_db.append(20 * np.log10(rms))
        times.append(i / sr)
    times = np.array(times)
    rms_db = np.array(rms_db)

    fig, ax = plt.subplots(figsize=(12, 4))
    ax.plot(times, rms_db, lw=0.8, color="#2B2B2B")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("RMS (dBFS, 100ms window)")
    ax.set_title(f"Short {short_id} — audio RMS curve (continuity check)")
    ax.set_ylim(-60, 0)
    ax.grid(True, alpha=0.3)
    # Mark seam timestamps
    for t in seam_timestamps:
        ax.axvline(t, color="#D17A3D", lw=1.0, ls="--", alpha=0.6)
    fig.tight_layout()
    plot_path = verify_dir / f"short{short_id}-rms-curve.png"
    fig.savefig(plot_path, dpi=110)
    plt.close(fig)
    try:
        wav_path.unlink()
    except OSError:
        pass
    return plot_path


# ---------------------------------------------------------------------------
# Build one Short
# ---------------------------------------------------------------------------

def build_short(short_id: int) -> dict:
    cfg = SHORTS[short_id]
    print("=" * 70)
    print(f"AUDIO-FIX  Short {short_id} — {cfg['label']}")
    print("=" * 70)

    build_dir = V02_RENDERS / f"short{short_id}-build"
    if not build_dir.exists():
        print(f"[FAIL] build dir missing — original Short build never ran: {build_dir}")
        return {"short_id": short_id, "failed": True, "error": "build_dir missing"}

    # Verify all expected source segments exist
    expected = ["01-hook-card.mp4", "02-open.mp4", "03-middle.mp4", "04-close.mp4"]
    missing = [n for n in expected if not (build_dir / n).exists()]
    if missing:
        print(f"[FAIL] missing source segments: {missing}")
        return {"short_id": short_id, "failed": True, "error": f"missing: {missing}"}

    verify_dir = build_dir / "audio-verify"
    verify_dir.mkdir(parents=True, exist_ok=True)

    # Pick a music-bed offset for this Short. We use the SAME offset for hook,
    # open, and close (continuous-feeling music). The middle has its own music
    # inside V2's mix.
    bed_offset = MUSIC_BED_START.get(short_id, 60.0)

    # Derive bed offsets for each bookend so the bed feels CONTINUOUS:
    #   hook starts at bed_offset
    #   open continues from bed_offset + HOOK_FRAME_DUR
    #   close continues from bed_offset + HOOK_FRAME_DUR + open_dur
    # (We don't need the bed in the middle — V2's audio plays.)
    hook_offset = bed_offset
    # NOTE: we do NOT chain through middle — the bed slice that plays during the
    # close bookend doesn't need to align with where the bed inside V2's middle
    # finished. The track is ambient/loopy enough that a few seconds of musical
    # discontinuity at the middle->close seam is masked by Mac VO + the close VO
    # ducking the perceived position. The acrossfade smooths the level.

    # Stage 1 — Build per-segment audio-fixed videos
    print("\n--- Stage 1/3 — Build 4 segments with new audio chain ---")
    open_clip_dur_existing = probe_dur(build_dir / "02-open.mp4")
    close_clip_dur_existing = probe_dur(build_dir / "04-close.mp4")

    s1 = build_hook_segment(short_id, build_dir, bed_offset=hook_offset)
    open_offset = hook_offset + HOOK_FRAME_DUR
    s2, open_dur = build_open_segment(short_id, build_dir, bed_offset=open_offset)
    s3, mid_dur = build_middle_segment(short_id, build_dir)
    # For close, restart bed at a different offset (avoids re-using same musical
    # phrase). +open_dur+5s gives a fresh phrase that matches the source's
    # ducked level.
    close_offset = hook_offset + HOOK_FRAME_DUR + open_dur + 5.0
    if close_offset + close_clip_dur_existing > probe_dur(MUSIC_BED) - 1:
        # Wrap if we'd run off the end of the bed
        close_offset = (close_offset % (probe_dur(MUSIC_BED) - close_clip_dur_existing - 5))
    s4, close_dur = build_close_segment(short_id, build_dir, bed_offset=close_offset)

    # Per-segment audio level check
    print("\n  [per-seg audio levels (pre-loudnorm)]")
    for label, p in [("hook", s1), ("open", s2), ("middle", s3), ("close", s4)]:
        i_lufs, tp = measure_simple(p)
        print(f"    {label:6s}  I={i_lufs} LUFS  TP={tp} dBFS  ({probe_dur(p):.2f}s)")

    # Stage 2 — Concat with acrossfade
    print("\n--- Stage 2/3 — Concat with 100ms acrossfade between segments ---")
    durs = [HOOK_FRAME_DUR, open_dur, mid_dur, close_dur]
    spliced = concat_with_xfade([s1, s2, s3, s4], durs, build_dir)
    spliced_dur = probe_dur(spliced)
    print(f"  [OK] {spliced.name} ({spliced_dur:.2f}s)")

    # Compute seam timestamps (in concatenated timeline). acrossfade shortens by
    # xfade_dur each join, so seams sit at:
    #   t1 = HOOK - xfade/2          (between hook and open)
    #   t2 = HOOK + open - xfade*1.5  (between open and middle)
    #   t3 = HOOK + open + mid - xfade*2.5 (between middle and close)
    seams = [
        HOOK_FRAME_DUR - SEAM_XFADE / 2,
        HOOK_FRAME_DUR + open_dur - SEAM_XFADE * 1.5,
        HOOK_FRAME_DUR + open_dur + mid_dur - SEAM_XFADE * 2.5,
    ]

    # Stage 3 — Loudnorm to -14 LUFS, force 48 kHz
    print("\n--- Stage 3/3 — Loudnorm to -14 LUFS / TP -1.0 + lock 48 kHz ---")
    final = SHORTS_OUT / f"audm-v2-short-{short_id}.mp4"
    fi, fp = loudnorm_final(spliced, final, build_dir)

    # Verify final
    probe_audio = subprocess.run(
        [FFPROBE, "-v", "error", "-select_streams", "a:0",
         "-show_entries", "stream=codec_name,sample_rate,channels,bit_rate",
         "-of", "default=noprint_wrappers=1", str(final)],
        capture_output=True, text=True,
    ).stdout.strip()
    print(f"\n  [final audio probe]\n{probe_audio}")

    # Save loudnorm stats to verify dir
    stats_path = verify_dir / f"short{short_id}-loudnorm-stats.txt"
    stats_path.write_text(
        f"Short {short_id} — {cfg['label']}\n"
        f"Final: {final}\n"
        f"Duration: {probe_dur(final):.2f}s\n"
        f"Integrated LUFS: {fi}\n"
        f"True peak dBFS: {fp}\n"
        f"\n--- audio stream ---\n{probe_audio}\n"
        f"\n--- seam timestamps (post-acrossfade) ---\n"
        f"hook->open:    t≈{seams[0]:.3f}s\n"
        f"open->middle:  t≈{seams[1]:.3f}s\n"
        f"middle->close: t≈{seams[2]:.3f}s\n",
        encoding="utf-8",
    )

    # RMS plot
    plot_path = export_rms_plot(short_id, final, verify_dir, seams)
    if plot_path:
        print(f"  [plot] {plot_path}")

    final_dur = probe_dur(final)
    final_size_mb = final.stat().st_size / (1024 * 1024)

    print("=" * 70)
    print(f"DONE Short {short_id}: {final}")
    print(f"  Duration: {final_dur:.2f}s · Size: {final_size_mb:.1f} MB")
    print(f"  LUFS: {fi}  TP: {fp} dBFS")
    print("=" * 70)
    print()

    return {
        "short_id": short_id,
        "duration_s": final_dur,
        "size_mb": final_size_mb,
        "lufs": fi,
        "tp_dbfs": fp,
        "out_path": str(final),
        "verify_dir": str(verify_dir),
        "seams": seams,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", type=int, choices=[1, 2, 3, 4, 5], default=None,
                    help="Re-render only one Short. Default: all 5.")
    args = ap.parse_args()
    targets = [args.only] if args.only else [1, 2, 3, 4, 5]

    results = []
    for sid in targets:
        try:
            results.append(build_short(sid))
        except SystemExit as e:
            print(f"[FAIL] Short {sid} sys.exit({e.code}) — continuing")
            results.append({"short_id": sid, "failed": True})
        except Exception as e:
            print(f"[FAIL] Short {sid} exception: {e}")
            import traceback
            traceback.print_exc()
            results.append({"short_id": sid, "failed": True, "error": str(e)})

    print("\n" + "=" * 70)
    print("AUDIO-FIX BATCH SUMMARY")
    print("=" * 70)
    for r in results:
        if r.get("failed"):
            print(f"  Short {r['short_id']}: FAILED — {r.get('error', 'see log')}")
        else:
            print(f"  Short {r['short_id']}: {r['duration_s']:.2f}s · "
                  f"{r['size_mb']:.1f} MB · {r['lufs']} LUFS / {r['tp_dbfs']} dBFS")


if __name__ == "__main__":
    main()
