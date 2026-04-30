"""Re-trim VOs from pre-trim backup — TRAILING silence ONLY.

Previous pass also trimmed leading silence (72-120ms per scene), which made
Mac's first word sound clipped — natural 100ms breath was eaten.

This pass:
  1. Restores S1-S6 from voice/_pre-trim/ backup
  2. Trims trailing silence only (the "model expecting continuation" tail)
  3. Leaves S7 alone (already at v3 ideal state)
  4. Reports new durations + cumulative shifts for OVERLAYS update
"""

import shutil
import subprocess
from pathlib import Path

REPO = Path(r"C:\dev\Claude")
VO_DIR = REPO / "content" / "au-dealer-math" / "scripts" / "v01-renders" / "voice"
BACKUP_DIR = VO_DIR / "_pre-trim"

FFMPEG = r"C:\Users\adria\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1-full_build\bin\ffmpeg.exe"
FFPROBE = r"C:\Users\adria\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1-full_build\bin\ffprobe.exe"

# Process S1-S6 (S7 stays at v3)
SCENES_ORDER = [
    ("vo-scene-1-hook.mp3",       1),
    ("vo-scene-2-authority.mp3",  2),
    ("vo-scene-3-question.mp3",   3),
    ("vo-scene-4-loan-trick.mp3", 4),
    ("vo-scene-5-why-dealer.mp3", 5),
    ("vo-scene-6-fix.mp3",        6),
]


def probe_dur(p):
    r = subprocess.run([FFPROBE, "-v", "error", "-show_entries", "format=duration",
                        "-of", "csv=p=0", str(p)], capture_output=True, text=True)
    return float(r.stdout.strip())


def trim_trailing_only(src, dst):
    """Trim trailing silence below -40dB peak (50ms min run). Leading untouched."""
    af = (
        "areverse,"
        "silenceremove=start_periods=1:start_silence=0:start_duration=0.05:"
        "start_threshold=-40dB:detection=peak,"
        "areverse"
    )
    cmd = [
        FFMPEG, "-y", "-loglevel", "error",
        "-i", str(src),
        "-af", af,
        "-c:a", "libmp3lame", "-b:a", "128k", "-ar", "44100",
        str(dst),
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"ffmpeg trim failed: {r.stderr}")


def main():
    print("=" * 70)
    print("AUDM V1 - re-trim VOs (TRAILING ONLY) from backup")
    print("=" * 70)

    print(f"\n{'#':3s} {'file':30s} {'pre':>8s} {'after':>8s} {'shift':>7s} {'cum_pre':>8s}")
    print("-" * 70)

    cumulative = 0.0
    new_durs = []
    for fname, scene_id in SCENES_ORDER:
        bkp = BACKUP_DIR / fname
        dst = VO_DIR / fname
        if not bkp.exists():
            print(f"  [skip] backup missing: {bkp}")
            continue

        before = probe_dur(bkp)
        # Trim from backup -> tmp -> overwrite live
        tmp = dst.with_suffix(dst.suffix + ".trim2.mp3")
        trim_trailing_only(bkp, tmp)
        after = probe_dur(tmp)
        shift = before - after

        # Replace
        if dst.exists():
            dst.unlink()
        tmp.rename(dst)

        cum_pre = cumulative
        cumulative += shift
        new_durs.append((scene_id, fname, before, after, shift, cum_pre))
        print(f"  {scene_id:<3d} {fname:30s} {before:>7.3f}s {after:>7.3f}s "
              f"{-shift:>6.3f}s {cum_pre:>7.3f}s")

    print("-" * 70)
    print("\nNew SCENES.actual_dur values (trailing-trim only):")
    for sid, _, _, after, _, _ in new_durs:
        print(f"  scene {sid}: actual_dur = {after:.4f}")
    print(f"  scene 7: actual_dur = 12.3353  (unchanged, v3 already trimmed)")

    print("\nNew cum_pre for OVERLAYS:")
    cum = 0.0
    print(f"  S1 overlays: shift = 0.000s (no preceding scenes)")
    cum += new_durs[0][4]
    print(f"  S2 overlays: shift = {cum:.3f}s")
    cum += new_durs[1][4]
    print(f"  S3 overlays: shift = {cum:.3f}s")
    cum += new_durs[2][4]
    print(f"  S4 overlays: shift = {cum:.3f}s")
    cum += new_durs[3][4]
    print(f"  S5 overlays: shift = {cum:.3f}s")
    cum += new_durs[4][4]
    print(f"  S6 overlays: shift = {cum:.3f}s")

    total = sum(d[3] for d in new_durs) + 12.3353
    print(f"\nNew total runtime: {total:.3f}s ({int(total//60)}:{int(total%60):02d})")


if __name__ == "__main__":
    main()
