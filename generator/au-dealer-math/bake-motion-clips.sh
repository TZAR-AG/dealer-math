#!/usr/bin/env bash
# Bake AU Dealer Math motion clips to their target slot durations.
#
# Why: AI-generated motion (Kling/MJ) renders at ~5 sec, but the V1 manifest
# specifies slots up to 22 sec. Resolve has no scriptable freeze-frame API,
# so we extend each motion clip externally with ffmpeg's tpad=stop_mode=clone
# filter — the last frame is held until the slot duration is reached.
#
# Output: motion/baked/v2-mj/*-baked.mp4 + motion/baked/v2-kling/*-baked.mp4
# Format: H.264 yuv420p @ 24fps, no audio (VO is on a separate track).
#
# Re-run this whenever a motion clip is regenerated or the slot duration
# changes in build-v1-davinci.py's VISUAL_TRACK.

set -euo pipefail

FFMPEG="${FFMPEG:-/c/Users/adria/AppData/Local/Microsoft/WinGet/Packages/Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe/ffmpeg-8.1-full_build/bin/ffmpeg.exe}"
RENDERS="/c/dev/Claude/content/au-dealer-math/scripts/v01-renders"

if [ ! -x "$FFMPEG" ] && ! command -v ffmpeg >/dev/null 2>&1; then
  echo "ffmpeg not found at $FFMPEG and not in PATH" >&2
  echo "Install: winget install Gyan.FFmpeg --silent --scope user" >&2
  exit 1
fi
[ -x "$FFMPEG" ] || FFMPEG="ffmpeg"

cd "$RENDERS"
mkdir -p motion/baked/v2-mj motion/baked/v2-kling

# Format: source_relpath:target_seconds:output_relpath
# Match these against VISUAL_TRACK in build-v1-davinci.py.
JOBS=(
  "motion/v2-mj/mj-v2-3D-three-rooms-pull.mp4:10.0:motion/baked/v2-mj/mj-v2-3D-three-rooms-pull-baked.mp4"
  "motion/v2-kling/kling-v2-4A-stacks-pan.mp4:22.0:motion/baked/v2-kling/kling-v2-4A-stacks-pan-baked.mp4"
  "motion/v2-kling/kling-v2-4D-luxury-treadmill.mp4:13.0:motion/baked/v2-kling/kling-v2-4D-luxury-treadmill-baked.mp4"
  "motion/v2-mj/mj-v2-5A-three-offices-dolly.mp4:13.0:motion/baked/v2-mj/mj-v2-5A-three-offices-dolly-baked.mp4"
  "motion/v2-mj/mj-v2-5C-finance-zoom.mp4:15.0:motion/baked/v2-mj/mj-v2-5C-finance-zoom-baked.mp4"
  "motion/v2-kling/kling-v2-5D-holdback-chiaroscuro.mp4:17.0:motion/baked/v2-kling/kling-v2-5D-holdback-chiaroscuro-baked.mp4"
  "motion/v2-mj/mj-v2-6A-bank-letter-tilt.mp4:15.0:motion/baked/v2-mj/mj-v2-6A-bank-letter-tilt-baked.mp4"
  "motion/v2-mj/mj-v2-6C-window-banner-pull_0.mp4:18.0:motion/baked/v2-mj/mj-v2-6C-window-banner-pull_0-baked.mp4"
)

ok=0
fail=0
for job in "${JOBS[@]}"; do
  IFS=':' read -r src target out <<< "$job"
  printf "  baking %-55s -> %ss ... " "$(basename "$src")" "$target"
  if [ ! -f "$src" ]; then
    echo "MISSING SOURCE"
    fail=$((fail + 1))
    continue
  fi
  if "$FFMPEG" -y -loglevel error -i "$src" \
      -vf "tpad=stop_mode=clone:stop_duration=${target}" \
      -t "$target" \
      -c:v libx264 -pix_fmt yuv420p -r 24 -an \
      "$out"; then
    echo "ok"
    ok=$((ok + 1))
  else
    echo "FAIL"
    fail=$((fail + 1))
  fi
done

echo
echo "Baked: $ok ok, $fail failed"
[ "$fail" -eq 0 ]
