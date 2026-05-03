# Transcribe AUDM V2 voiceovers with word-level timestamps via faster-whisper.
# Outputs JSON file with words + start/end times per scene.
# Used to find exact timestamps for dollar-figure overlays.

import json
import subprocess
from pathlib import Path
from faster_whisper import WhisperModel

REPO = Path(r"C:\dev\Claude")
VO_DIR = REPO / "content" / "au-dealer-math" / "scripts" / "v02-renders" / "voice"
OUT_FILE = REPO / "content" / "au-dealer-math" / "scripts" / "v02-renders" / "vo-transcriptions.json"
FFPROBE = r"C:\Users\adria\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1-full_build\bin\ffprobe.exe"

# CPU "small" model is fast + accurate enough for this. ~250MB download first time.
print("Loading faster-whisper small.en model...")
model = WhisperModel("small.en", device="cpu", compute_type="int8")
print("Loaded.\n")

# V2 scene list — durations probed at runtime (no hardcoded table per V1).
# Order must match regenerate-vo-v02.js SCENE_FILES output sequence.
SCENE_LIST = [
    ("hook",       "vo-scene-1-hook.mp3"),
    ("authority",  "vo-scene-2-authority.mp3"),
    ("fnioffice",  "vo-scene-3-fnioffice.mp3"),
    ("rateGame",   "vo-scene-4-rate-game.mp3"),
    ("commission", "vo-scene-5-commission.mp3"),
    ("fix",        "vo-scene-6-fix.mp3"),
    ("signoff",    "vo-scene-7-signoff.mp3"),
]


def probe_dur(p: Path) -> float:
    r = subprocess.run([FFPROBE, "-v", "error", "-show_entries", "format=duration",
                        "-of", "csv=p=0", str(p)], capture_output=True, text=True)
    return float(r.stdout.strip())


SCENES = []
for name, fname in SCENE_LIST:
    p = VO_DIR / fname
    if not p.exists():
        print(f"  [skip] {fname} missing — exclude from SCENES")
        continue
    SCENES.append((name, probe_dur(p), fname))

# Crossfade compression: master VO is built via build-master-vo-v02.py with
# D=0.20s acrossfade between each scene pair. Each crossfade shortens the master
# timeline by D relative to raw cumulative durations. Scene N's true start in
# the master timeline is (cumulative raw start) - (N-1) * D. Caption alignment
# requires master-relative timestamps, so we apply that shift here. Without it,
# scene 7 captions drift ~1.2s late vs the audio.
D_CROSSFADE = 0.20

scene_starts = [0.0]
for i, (_, dur, _) in enumerate(SCENES):
    # Crossfade applies between scene i and scene i+1 (so at the END of each
    # non-last scene). Subtract D after every scene except the last.
    has_following_crossfade = i < len(SCENES) - 1
    next_start = scene_starts[-1] + dur - (D_CROSSFADE if has_following_crossfade else 0)
    scene_starts.append(next_start)

results = {"scenes": []}
for i, (name, dur, fname) in enumerate(SCENES):
    audio_path = VO_DIR / fname
    if not audio_path.exists():
        print(f"  [skip] {fname} missing")
        continue
    print(f"Transcribing scene {i+1} {name} ({fname})...")
    segments, info = model.transcribe(
        str(audio_path),
        language="en",
        word_timestamps=True,
        beam_size=5,
    )
    words = []
    for seg in segments:
        if not seg.words:
            continue
        for w in seg.words:
            words.append({
                "word": w.word.strip(),
                "scene_start": round(w.start, 3),
                "scene_end": round(w.end, 3),
                "timeline_start": round(scene_starts[i] + w.start, 3),
                "timeline_end": round(scene_starts[i] + w.end, 3),
            })
    results["scenes"].append({
        "scene_id": i + 1,
        "name": name,
        "vo_file": fname,
        "scene_start_in_timeline": round(scene_starts[i], 3),
        "scene_duration": dur,
        "word_count": len(words),
        "words": words,
    })
    print(f"  {len(words)} words transcribed")

OUT_FILE.write_text(json.dumps(results, indent=2))
print(f"\nWrote: {OUT_FILE}")
print(f"\nNow searching for dollar-figure tokens...")

# V2 key terms — rates + dollar ranges from finance manager's office video
KEY_TERMS = [
    "nine", "5", "five", "percent",
    "forty", "thousand", "dollars",
    "two", "three", "ten", "fifteen",
    "loan", "rate", "spread", "approved",
    "commission", "pool",
]
print()
for scene in results["scenes"]:
    print(f"--- Scene {scene['scene_id']} {scene['name']} ---")
    for w in scene["words"]:
        wl = w["word"].lower().strip(",.!?")
        for term in KEY_TERMS:
            if term in wl or wl in term:
                print(f"  {w['timeline_start']:7.2f}s  '{w['word']}'")
                break
