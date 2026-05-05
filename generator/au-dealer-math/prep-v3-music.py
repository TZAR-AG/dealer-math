"""Prep V3 music bed — loop + duck Moorland (Underbelly & Ty Mayer) to 684s.

Input:  C:/Users/adria/Downloads/Moorland - Underbelly & Ty Mayer.mp3 (152s, YT Audio Library)
Output: content/au-dealer-math/scripts/v03-renders/music/moorland-looped-ducked-soft-684s-v1.mp3

Process:
    - Probe source duration (target ~152s — verify before run)
    - 5x acrossfade-loop (5 * 152 = 760s; ample headroom)
    - Apply -8 dB volume reduction on each layer (V2 'ducked-soft' pattern)
    - acrossfade=d=3:c1=tri:c2=tri between consecutive copies (matches V1 + V2 pipeline)
    - 1s fade-in at start, 1s fade-out ending at 683s (lands clean inside the 684s target)
    - Trim to exactly 684s
    - Encode libmp3lame -q:a 2 (matches V1/V2 music bed output)

Per `reference_audm_audio_finalize_lock_2026-05-04.md` — YouTube Audio Library
ONLY (no Storyblocks/HAAWK CID risk). Music bed is processed BEFORE final
loudnorm; the two-pass loudnorm to -14 LUFS happens at FINAL render stage.
"""

import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path(r"C:\dev\Claude")
RENDERS = REPO / "content" / "au-dealer-math" / "scripts" / "v03-renders"
MUSIC_OUT_DIR = RENDERS / "music"
MUSIC_OUT_DIR.mkdir(parents=True, exist_ok=True)

SOURCE = Path(r"C:\Users\adria\Downloads\Moorland - Underbelly & Ty Mayer.mp3")
TARGET_SEC = 684.0  # ~0.55s longer than master VO (683.45s) — safety pad
DUCK_DB = -8         # matches V2 'ducked-soft' (V2 source was already -46 dB mean → -8 dB further)
LOOPS = 5            # 5 × 152s = 760s, more than enough for 684s

OUT_FILE = MUSIC_OUT_DIR / "moorland-looped-ducked-soft-684s-v1.mp3"

FFMPEG = r"C:\Users\adria\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1-full_build\bin\ffmpeg.exe"
FFPROBE = r"C:\Users\adria\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1-full_build\bin\ffprobe.exe"

# Fall back to PATH-resolved binaries if the WinGet symlink isn't present
if not Path(FFMPEG).exists():
    FFMPEG = shutil.which("ffmpeg") or "ffmpeg"
if not Path(FFPROBE).exists():
    FFPROBE = shutil.which("ffprobe") or "ffprobe"


def probe_duration(path: Path) -> float:
    cmd = [FFPROBE, "-v", "error", "-show_entries", "format=duration",
           "-of", "default=noprint_wrappers=1:nokey=1", str(path)]
    out = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return float(out.stdout.strip())


def main():
    print("=" * 70)
    print("AUDM V3 -- prep music bed (Moorland to 684s looped+ducked)")
    print("=" * 70)

    if not SOURCE.exists():
        print(f"[FAIL] source music file not found: {SOURCE}")
        sys.exit(1)

    src_dur = probe_duration(SOURCE)
    print(f"Source: {SOURCE.name}")
    print(f"  Duration: {src_dur:.2f}s")
    print(f"  Size:     {SOURCE.stat().st_size // 1024} KB")
    print(f"Target:   {TARGET_SEC:.2f}s ducked at {DUCK_DB} dB")
    print(f"Output:   {OUT_FILE}")

    # Build a 5x acrossfade chain. ffmpeg filter_complex for N inputs:
    #   each input gets volume=-8dB
    #   pairs are crossfaded with d=3 triangular fade
    #   final output is faded in at start (1s) and out (1s, ending at 683s)

    # Inputs: -i SOURCE × LOOPS times (we re-use the same file as 5 separate inputs)
    inputs = []
    for _ in range(LOOPS):
        inputs.extend(["-i", str(SOURCE)])

    # Build filter graph
    filter_parts = []
    for i in range(LOOPS):
        filter_parts.append(f"[{i}:a]volume={DUCK_DB}dB[a{i}]")

    # Chain crossfades
    chain = "[a0]"
    for i in range(1, LOOPS):
        out_label = f"[ab{i}]"
        if i < LOOPS - 1:
            filter_parts.append(f"{chain}[a{i}]acrossfade=d=3:c1=tri:c2=tri{out_label}")
            chain = out_label
        else:
            # Final acrossfade -> apply fade-in + fade-out and trim to TARGET_SEC
            fade_st = TARGET_SEC - 1
            filter_parts.append(
                f"{chain}[a{i}]acrossfade=d=3:c1=tri:c2=tri,"
                f"afade=t=in:d=1,afade=t=out:d=1:st={fade_st:.2f}[out]"
            )

    filter_complex = ";".join(filter_parts)

    cmd = [
        FFMPEG, "-y", "-loglevel", "error",
        *inputs,
        "-filter_complex", filter_complex,
        "-map", "[out]",
        "-t", f"{TARGET_SEC}",
        "-c:a", "libmp3lame", "-q:a", "2",
        str(OUT_FILE),
    ]

    print(f"\nRunning ffmpeg ({LOOPS}x acrossfade loop)...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"[FAIL] ffmpeg returned {result.returncode}")
        print(f"  stderr: {result.stderr[-1500:]}")
        sys.exit(1)

    out_dur = probe_duration(OUT_FILE)
    print(f"\n[OK] {OUT_FILE.name}")
    print(f"  Duration: {out_dur:.2f}s (target {TARGET_SEC:.2f}s)")
    print(f"  Size:     {OUT_FILE.stat().st_size // 1024} KB")

    if abs(out_dur - TARGET_SEC) > 0.5:
        print(f"[warn] duration drift > 0.5s — investigate")
        sys.exit(2)


if __name__ == "__main__":
    main()
