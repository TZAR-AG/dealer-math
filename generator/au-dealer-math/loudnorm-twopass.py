"""Two-pass loudnorm helper.

Usage:
    python loudnorm-twopass.py <input> <output> [--video-copy]

Targets YouTube spec: I=-14 LUFS, TP=-1.0 dBFS, LRA=7.
Pass 1: measures input loudness, parses JSON output.
Pass 2: applies normalization with measured stats (much more accurate than single-pass).
"""

import json
import re
import subprocess
import sys
from pathlib import Path

FFMPEG = r"C:\Users\adria\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1-full_build\bin\ffmpeg.exe"


def measure(src):
    """Run pass 1 and return measured stats dict."""
    cmd = [
        FFMPEG, "-i", str(src),
        "-af", "loudnorm=I=-14:TP=-1.0:LRA=7:print_format=json",
        "-f", "null", "-",
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="ignore")
    text = result.stderr
    m = re.search(r"\{[^{]*input_i[^}]*\}", text, re.DOTALL)
    if not m:
        print("PASS 1 OUTPUT:")
        print(text[-2000:])
        raise RuntimeError("Could not find loudnorm JSON in pass 1 output")
    return json.loads(m.group(0))


def apply_loudnorm(src, dst, stats, video_copy=False, audio_codec="aac", audio_bitrate="320k"):
    """Run pass 2 with measured stats."""
    af = (
        f"loudnorm=I=-14:TP=-1.0:LRA=7"
        f":measured_I={stats['input_i']}"
        f":measured_TP={stats['input_tp']}"
        f":measured_LRA={stats['input_lra']}"
        f":measured_thresh={stats['input_thresh']}"
        f":offset={stats['target_offset']}"
        f":linear=true"
    )
    cmd = [FFMPEG, "-y", "-loglevel", "error", "-i", str(src)]
    if video_copy:
        cmd += ["-c:v", "copy"]
    cmd += ["-af", af]
    if audio_codec == "aac":
        cmd += ["-c:a", "aac", "-b:a", audio_bitrate]
    elif audio_codec == "libmp3lame":
        cmd += ["-c:a", "libmp3lame", "-q:a", "2"]
    else:
        cmd += ["-c:a", audio_codec]
    cmd += [str(dst)]
    result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="ignore")
    if result.returncode != 0:
        print("PASS 2 STDERR:")
        print(result.stderr)
        raise RuntimeError(f"Pass 2 failed for {dst}")


def verify(path):
    """Run ebur128 on output and return integrated LUFS + true peak."""
    cmd = [FFMPEG, "-i", str(path), "-af", "ebur128=peak=true", "-f", "null", "-"]
    result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="ignore")
    text = result.stderr
    i_match = re.search(r"Integrated loudness:\s*\n\s*I:\s*(-?[\d.]+)\s*LUFS", text)
    tp_match = re.search(r"True peak:\s*\n\s*Peak:\s*(-?[\d.]+)\s*dBFS", text)
    return (
        float(i_match.group(1)) if i_match else None,
        float(tp_match.group(1)) if tp_match else None,
    )


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    src = Path(sys.argv[1])
    dst = Path(sys.argv[2])
    video_copy = "--video-copy" in sys.argv

    if not src.exists():
        print(f"[fail] source not found: {src}")
        sys.exit(1)

    # Pick audio codec by output extension
    if dst.suffix.lower() in (".mp3",):
        audio_codec = "libmp3lame"
    else:
        audio_codec = "aac"

    print(f"[1/3] Measuring: {src.name}")
    stats = measure(src)
    print(f"      I={stats['input_i']}  TP={stats['input_tp']}  LRA={stats['input_lra']}")
    print(f"      thresh={stats['input_thresh']}  offset={stats['target_offset']}")

    print(f"[2/3] Applying loudnorm (target -14 LUFS) -> {dst.name}")
    apply_loudnorm(src, dst, stats, video_copy=video_copy, audio_codec=audio_codec)

    print(f"[3/3] Verifying...")
    lufs, peak = verify(dst)
    print(f"      Integrated: {lufs} LUFS")
    print(f"      True Peak:  {peak} dBFS")

    if lufs is None or peak is None:
        print(f"[warn] could not parse verification output")
    elif abs(lufs - (-14.0)) > 0.5:
        print(f"[warn] off-target by {lufs - (-14.0):.2f} LU — investigate")
    else:
        print(f"[OK] within 0.5 LU of -14 LUFS target")


if __name__ == "__main__":
    main()
