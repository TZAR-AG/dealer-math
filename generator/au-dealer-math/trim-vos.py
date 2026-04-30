"""Trim trailing silence (and any leading silence) from each AUDM V1 VO.

Each ElevenLabs render leaves 250-420ms of sub-(-40dB) tail (model "expecting
continuation") that creates an audibly long pause at scene boundaries. With
VO_GAP_SEC=0 the result is: word → 350ms quiet → next-scene-word — which sounds
like Mac is hesitating mid-paragraph.

This script:
  1. Probes each VO's true speech end via silenceremove (areverse trick).
  2. Writes a trimmed copy back to the same path (originals backed up to
     voice/_pre-trim/ for safety).
  3. Reports new durations for SCENES dict + computes cumulative shift for
     OVERLAYS list update.

Threshold: -40dB peak with 50ms min silence duration. Tested empirically against
Mac's quietest beats — won't clip speech.

Run: python generator/au-dealer-math/trim-vos.py
"""

import shutil
import subprocess
from pathlib import Path

REPO = Path(r"C:\dev\Claude")
VO_DIR = REPO / "content" / "au-dealer-math" / "scripts" / "v01-renders" / "voice"
BACKUP_DIR = VO_DIR / "_pre-trim"
BACKUP_DIR.mkdir(exist_ok=True)

FFMPEG = r"C:\Users\adria\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1-full_build\bin\ffmpeg.exe"
FFPROBE = r"C:\Users\adria\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1-full_build\bin\ffprobe.exe"

SCENES_ORDER = [
    ("vo-scene-1-hook.mp3",       1),
    ("vo-scene-2-authority.mp3",  2),
    ("vo-scene-3-question.mp3",   3),
    ("vo-scene-4-loan-trick.mp3", 4),
    ("vo-scene-5-why-dealer.mp3", 5),
    ("vo-scene-6-fix.mp3",        6),
    ("vo-scene-7-signoff.mp3",    7),
]


def probe_dur(p):
    r = subprocess.run([FFPROBE, "-v", "error", "-show_entries", "format=duration",
                        "-of", "csv=p=0", str(p)], capture_output=True, text=True)
    return float(r.stdout.strip())


def trim(src, dst):
    """Trim leading + trailing silence below -40dB peak, requiring 50ms min run."""
    # Two-pass: trim leading, reverse, trim leading (= original trailing), reverse back.
    af = (
        "silenceremove=start_periods=1:start_silence=0:start_duration=0.05:"
        "start_threshold=-40dB:detection=peak,"
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
    print(f"AUDM V1 — trim leading + trailing silence on {len(SCENES_ORDER)} VOs")
    print("=" * 70)

    new_durs = []
    cumulative_shift = 0.0
    print(f"\n{'#':3s} {'file':30s} {'before':>8s} {'after':>8s} {'shift':>7s} {'cum_pre':>8s}")
    print("-" * 70)
    for fname, scene_id in SCENES_ORDER:
        src = VO_DIR / fname
        if not src.exists():
            print(f"  [skip] {fname} missing")
            continue

        # Backup original (only once)
        bkp = BACKUP_DIR / fname
        if not bkp.exists():
            shutil.copy2(src, bkp)

        before = probe_dur(src)
        # Trim into a temp file, then atomic-replace
        tmp = src.with_suffix(src.suffix + ".trim.mp3")
        trim(src, tmp)
        after = probe_dur(tmp)
        shift = before - after

        # cum_pre = cumulative shift of all PREVIOUS scenes (affects overlays
        # whose absolute timestamp is in this scene)
        cum_pre = cumulative_shift
        cumulative_shift += shift

        # Replace original
        src.unlink()
        tmp.rename(src)

        new_durs.append((scene_id, fname, before, after, shift, cum_pre))
        print(f"  {scene_id:<3d} {fname:30s} {before:>7.3f}s {after:>7.3f}s "
              f"{-shift:>6.3f}s {cum_pre:>7.3f}s")

    print("-" * 70)
    print(f"\nNew SCENES.actual_dur values (paste into build-v1-davinci.py):")
    for sid, _, _, after, _, _ in new_durs:
        print(f"  scene {sid}: actual_dur = {after:.4f}")

    print(f"\nCumulative pre-scene shifts (apply to OVERLAYS in those scenes):")
    cum = 0.0
    print(f"  S1 (overlay times unchanged): cum_pre = 0.000s")
    cum += new_durs[0][4]
    print(f"  S2: cum_pre = {cum:.3f}s")
    cum += new_durs[1][4]
    print(f"  S3: cum_pre = {cum:.3f}s")
    cum += new_durs[2][4]
    print(f"  S4: cum_pre = {cum:.3f}s")
    cum += new_durs[3][4]
    print(f"  S5: cum_pre = {cum:.3f}s")
    cum += new_durs[4][4]
    print(f"  S6: cum_pre = {cum:.3f}s")
    cum += new_durs[5][4]
    print(f"  S7: cum_pre = {cum:.3f}s")
    print(f"\nNew TOTAL_RUNTIME ≈ {sum(d[3] for d in new_durs):.3f}s")
    print(f"\nOriginals backed up to: {BACKUP_DIR}")


if __name__ == "__main__":
    main()
