"""Swap V2 master audio: build final mix with YT Audio Library music bed.

Process:
1. Stitch 3 Underbelly & Ty Mayer tracks with 2s crossfades
2. Loop-extend if shorter than V2 video duration
3. Mix VO + new music bed (music ducked to -18dB under VO)
4. Mux new audio with existing video stream (no video re-encode = fast + lossless)
5. Output: video/out/audm-v2-finance-managers-office-v2.mp4

YT Content ID safe — YT Audio Library tracks can't conflict with YT's own DB.

Run: python generator/au-dealer-math/swap-v2-music.py
"""
import subprocess
from pathlib import Path

REPO = Path(r"C:\dev\Claude")
DOWNLOADS = Path(r"C:\Users\adria\Downloads")

VO = REPO / "content/au-dealer-math/scripts/v02-renders/voice/master-vo.mp3"
V2_VIDEO = REPO / "video/out/audm-v2-finance-managers-office.mp4"

# TODO V2: replace with V2 content from P14 of build plan
# V1 reference values preserved below — DO NOT run this script as-is
# (Adrian selects 3 YT Audio Library tracks during P14 — update TRACKS list then)
TRACKS = [
    DOWNLOADS / "A Hand In The Dark - Underbelly & Ty Mayer.mp3",
    DOWNLOADS / "Wide Boys - Underbelly & Ty Mayer.mp3",
    DOWNLOADS / "Moorland - Underbelly & Ty Mayer.mp3",
]

OUT_DIR = REPO / "video/out"
OUT_MUSIC = OUT_DIR / "_audm-v2-music-bed-v2.mp3"
OUT_AUDIO = OUT_DIR / "_audm-v2-audio-v2.mp3"
OUT_VIDEO = OUT_DIR / "audm-v2-finance-managers-office-v2.mp4"


def probe_duration(path):
    """Return media duration in seconds."""
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nw=1:nk=1", str(path)],
        capture_output=True, text=True, check=True,
    )
    return float(result.stdout.strip())


# Pre-flight checks
for f in [VO, V2_VIDEO, *TRACKS]:
    if not f.exists():
        print(f"[FAIL] Missing: {f}")
        exit(1)

target_duration = probe_duration(V2_VIDEO)
print(f"V2 video duration: {target_duration:.2f}s ({target_duration/60:.2f} min)")
for t in TRACKS:
    d = probe_duration(t)
    print(f"  {t.name}: {d:.2f}s")

# ============================================================
# Step 1: Stitch 3 tracks with crossfades + loop-extend to fill duration
# ============================================================
print("\n[1/3] Stitching music bed (3 tracks -> continuous bed)...")

inputs = []
for t in TRACKS:
    inputs.extend(["-i", str(t)])

# acrossfade chain: t0 + t1 + t2 with 2s triangular crossfades
filter_chain = (
    "[0:a][1:a]acrossfade=d=2:c1=tri:c2=tri[ab];"
    "[ab][2:a]acrossfade=d=2:c1=tri:c2=tri[stitched];"
    f"[stitched]aloop=loop=-1:size=2e9,atrim=0:{target_duration},"
    f"afade=t=out:st={target_duration-3:.2f}:d=3[final]"
)

cmd = [
    "ffmpeg", "-y",
    *inputs,
    "-filter_complex", filter_chain,
    "-map", "[final]",
    "-c:a", "libmp3lame",
    "-b:a", "192k",
    str(OUT_MUSIC),
]
subprocess.run(cmd, check=True)
print(f"  -> {OUT_MUSIC.name} ({OUT_MUSIC.stat().st_size // 1024}KB)")

# ============================================================
# Step 2: Mix VO + music bed (music at -18dB under VO for clarity)
# ============================================================
print("\n[2/3] Mixing VO + new music bed...")

mix_cmd = [
    "ffmpeg", "-y",
    "-i", str(VO),
    "-i", str(OUT_MUSIC),
    "-filter_complex",
    "[1:a]volume=-23dB[m];"
    "[0:a][m]amix=inputs=2:duration=longest:dropout_transition=0:normalize=0[mixed]",
    "-map", "[mixed]",
    "-c:a", "libmp3lame",
    "-b:a", "192k",
    str(OUT_AUDIO),
]
subprocess.run(mix_cmd, check=True)
print(f"  -> {OUT_AUDIO.name} ({OUT_AUDIO.stat().st_size // 1024}KB)")

# ============================================================
# Step 3: Mux new audio with existing video stream (no video re-encode)
# ============================================================
print("\n[3/3] Muxing video + new audio (lossless, no re-encode)...")

mux_cmd = [
    "ffmpeg", "-y",
    "-i", str(V2_VIDEO),
    "-i", str(OUT_AUDIO),
    "-c:v", "copy",       # video stream unchanged
    "-c:a", "aac",         # YouTube prefers AAC for audio
    "-b:a", "320k",
    "-map", "0:v:0",
    "-map", "1:a:0",
    "-shortest",
    str(OUT_VIDEO),
]
subprocess.run(mux_cmd, check=True)

size_mb = OUT_VIDEO.stat().st_size / 1024 / 1024
final_dur = probe_duration(OUT_VIDEO)
print(f"\n[OK] V2-v2 master ready:")
print(f"  Path:     {OUT_VIDEO}")
print(f"  Size:     {size_mb:.1f} MB")
print(f"  Duration: {final_dur:.2f}s ({final_dur/60:.2f} min)")
print(f"  Music:    Underbelly & Ty Mayer trio (YT Audio Library, Content-ID safe)")
print(f"  Status:   Upload to YT, no Storyblocks/HAAWK Content ID claim expected")
