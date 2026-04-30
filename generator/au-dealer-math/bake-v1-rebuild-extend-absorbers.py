"""Re-bake the 3 absorber KB clips with slightly extended durations so each
scene's clip total >= scene's actual VO duration (no slot/source overrun).

Replaces in-place:
  s1-h7-corridor-kb.mp4    4.00s -> 4.10s
  s2-a6-three-windows-night-kb.mp4   5.00s -> 5.10s
  s3-q17-end-of-day-kb.mp4 4.00s -> 4.55s
"""

import subprocess
from pathlib import Path

REPO = Path(r"C:\dev\Claude")
RENDERS = REPO / "content" / "au-dealer-math" / "scripts" / "v01-renders"
STILLS = RENDERS / "stills" / "auto-v2"
KB_OUT = RENDERS / "motion" / "baked" / "kb-v2"
FFMPEG = r"C:\Users\adria\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1-full_build\bin\ffmpeg.exe"

# (slot_id, duration_sec, kb_direction, zoom_pct)
# Durations bumped 0.05-0.10s above their slot need to absorb sub-frame rounding
# safely. The "still_kb" path in build-v1-davinci.py uses endFrame=target_frames;
# if endFrame exceeds source frames, AppendToTimeline rejects the placement.
ABSORBERS = [
    ("s1-h7-corridor",            4.20, "in",  14),
    ("s2-a6-three-windows-night", 5.20, "out", 14),
    ("s3-q17-end-of-day",         4.65, "out", 12),
]


def kb_filter(direction, zoom_pct, total_frames):
    z = zoom_pct / 100.0
    base_scale = "scale=7680:-1:flags=lanczos"
    if direction == "in":
        zexpr = f"1.0+{z}*on/{total_frames}"
        x, y = "iw/2-(iw/zoom/2)", "ih/2-(ih/zoom/2)"
    elif direction == "out":
        zexpr = f"1.0+{z}-{z}*on/{total_frames}"
        x, y = "iw/2-(iw/zoom/2)", "ih/2-(ih/zoom/2)"
    else:
        raise ValueError(direction)
    return f"{base_scale},zoompan=z='{zexpr}':d=1:x='{x}':y='{y}':s=1920x1080:fps=24"


for slot_id, duration, direction, zoom_pct in ABSORBERS:
    src = STILLS / f"{slot_id}.png"
    dst = KB_OUT / f"{slot_id}-kb.mp4"
    if not src.exists():
        print(f"[skip] missing source PNG: {src}")
        continue
    total_frames = int(duration * 24)
    vf = kb_filter(direction, zoom_pct, total_frames)
    cmd = [
        FFMPEG, "-y", "-loglevel", "error",
        "-loop", "1", "-i", str(src),
        "-vf", vf,
        "-t", str(duration),
        "-c:v", "libx264", "-preset", "medium", "-crf", "18",
        "-pix_fmt", "yuv420p", "-r", "24", "-an",
        str(dst),
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode == 0:
        sz = dst.stat().st_size // 1024
        print(f"[OK] {slot_id:30s} {duration:.2f}s {direction:4s} {zoom_pct}% ({sz}KB)")
    else:
        print(f"[FAIL] {slot_id}: {r.stderr.strip()[:200]}")

print("\nDone.")
