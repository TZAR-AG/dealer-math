"""Build master VO via ffmpeg acrossfade chain.

Elegant solution to the "transitions not smooth" / "VOs cut out" problem:
each scene's tail crossfades with the next scene's lead over 200ms. Mac's
word decay blends smoothly with the next scene's natural breath — no abrupt
cuts, no model-hold tail, no clipped word tails.

Crossfade curve: tri (linear triangular) on both sides — fastest perceptual
match for natural breath transitions.

Output: voice/master-vo.mp3 (single file, 6 crossfades · 0.2s each).
Total duration = sum(scenes) - 6*0.2 = sum - 1.2s.
"""

import subprocess
from pathlib import Path

REPO = Path(r"C:\dev\Claude")
VO_DIR = REPO / "content" / "au-dealer-math" / "scripts" / "v02-renders" / "voice"
FFMPEG = r"C:\Users\adria\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1-full_build\bin\ffmpeg.exe"
FFPROBE = r"C:\Users\adria\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1-full_build\bin\ffprobe.exe"

D = 0.20  # crossfade duration in seconds

# V2 scene filenames — match regenerate-vo-v02.js SCENE_FILES output names
VOS = [
    "vo-scene-1-hook.mp3",
    "vo-scene-2-authority.mp3",
    "vo-scene-3-fnioffice.mp3",
    "vo-scene-4-rate-game.mp3",
    "vo-scene-5-commission.mp3",
    "vo-scene-6-fix.mp3",
    "vo-scene-7-signoff.mp3",
]

OUT = VO_DIR / "master-vo.mp3"


def probe(p):
    r = subprocess.run([FFPROBE, "-v", "error", "-show_entries", "format=duration",
                        "-of", "csv=p=0", str(p)], capture_output=True, text=True)
    return float(r.stdout.strip())


def main():
    print("=" * 70)
    print(f"Building master VO via acrossfade chain (d={D}s, tri curve)")
    print("=" * 70)

    # Probe individual durations
    durs = []
    for vo in VOS:
        p = VO_DIR / vo
        if not p.exists():
            raise FileNotFoundError(p)
        d = probe(p)
        durs.append(d)
        print(f"  {vo:32s} {d:.4f}s")

    sum_dur = sum(durs)
    expected_master = sum_dur - 6 * D
    print(f"\n  sum(VOs)        = {sum_dur:.4f}s")
    print(f"  expected master = {expected_master:.4f}s (sum - 6*{D})")

    # Build acrossfade chain.
    # Each acrossfade overlaps last D seconds of A with first D seconds of B.
    # tri curve = linear triangular fade (perceptual neutral).
    # Chain: ((((((s1<>s2)<>s3)<>s4)<>s5)<>s6)<>s7)
    inputs = []
    for vo in VOS:
        inputs += ["-i", str(VO_DIR / vo)]

    # Build filter graph
    parts = [f"[0:a][1:a]acrossfade=d={D}:c1=tri:c2=tri[a01]"]
    prev_label = "a01"
    for i in range(2, 7):
        new_label = f"a0{i}"
        parts.append(f"[{prev_label}][{i}:a]acrossfade=d={D}:c1=tri:c2=tri[{new_label}]")
        prev_label = new_label
    filter_complex = ";".join(parts)
    final_label = prev_label

    # 2026-05-05: append mono->stereo upmix BEFORE export. ElevenLabs renders
    # mono. DaVinci on a stereo timeline puts mono on LEFT only — silent right.
    # Fix: explicitly upmix master VO to stereo via pan=stereo|c0=c0|c1=c0.
    # See feedback_audm_mono_vo_stereo_upmix_2026-05-05.md
    filter_complex_stereo = (
        f"{filter_complex};"
        f"[{final_label}]aformat=channel_layouts=mono,"
        f"pan=stereo|c0=c0|c1=c0,"
        f"aformat=sample_fmts=fltp:sample_rates=44100:channel_layouts=stereo"
        f"[aout]"
    )

    cmd = [
        FFMPEG, "-y", "-loglevel", "error",
        *inputs,
        "-filter_complex", filter_complex_stereo,
        "-map", "[aout]",
        "-c:a", "libmp3lame", "-b:a", "192k", "-ar", "44100",
        str(OUT),
    ]

    print(f"\n  ffmpeg filter: {filter_complex[:80]}...")
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(f"\n  FFMPEG STDERR:\n{r.stderr}")
        raise RuntimeError("acrossfade failed")

    actual_master = probe(OUT)
    print(f"\n  master duration = {actual_master:.4f}s ({int(actual_master//60)}:{actual_master%60:05.2f})")
    print(f"  expected        = {expected_master:.4f}s")
    print(f"  diff            = {actual_master - expected_master:+.4f}s")
    print(f"\nWritten: {OUT}")
    print("\nScene start positions in master (where pure scene N audio begins):")
    cum = 0
    for i, (vo, dur) in enumerate(zip(VOS, durs)):
        # Pure scene N starts at cum_prev_master_end (end of preceding crossfade)
        # For scene 1: 0
        # For scene N>1: scene_(N-1)_end_in_master = cum_old(N) - (N-1)*d
        start = cum - i * D if i > 0 else 0
        print(f"  S{i+1}: master start = {start:.4f}s  (original cum = {cum:.4f}s, shift = {-i*D:+.2f}s)")
        cum += dur


if __name__ == "__main__":
    main()
