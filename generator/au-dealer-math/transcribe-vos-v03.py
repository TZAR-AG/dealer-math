# Transcribe AUDM V3 voiceovers with word-level timestamps via faster-whisper.
# Outputs JSON file with words + start/end times per scene.
# Used to find exact timestamps for topic-aligned still placement (window tint,
# paint protection, dash cam, ceramic coating, etc.) and dollar-figure overlays.

import json
import subprocess
from pathlib import Path
from faster_whisper import WhisperModel

REPO = Path(r"C:\dev\Claude")
VO_DIR = REPO / "content" / "au-dealer-math" / "scripts" / "v03-renders" / "voice"
OUT_FILE = REPO / "content" / "au-dealer-math" / "scripts" / "v03-renders" / "vo-transcriptions.json"
FFPROBE = r"C:\Users\adria\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1-full_build\bin\ffprobe.exe"

print("Loading faster-whisper small.en model...")
model = WhisperModel("small.en", device="cpu", compute_type="int8")
print("Loaded.\n")

# V3 scene list — must match regenerate-vo-v03.js SCENE_FILES output sequence.
SCENE_LIST = [
    ("hook",            "vo-scene-1-hook.mp3"),
    ("authority",       "vo-scene-2-authority.mp3"),
    ("aftercare-menu",  "vo-scene-3-aftercare-menu.mp3"),
    ("math",            "vo-scene-4-math.mp3"),
    ("why-high",        "vo-scene-5-why-high.mp3"),
    ("what-to-do",      "vo-scene-6-what-to-do.mp3"),
    ("signoff",         "vo-scene-7-signoff.mp3"),
]


def probe_dur(p: Path) -> float:
    r = subprocess.run([FFPROBE, "-v", "error", "-show_entries", "format=duration",
                        "-of", "csv=p=0", str(p)], capture_output=True, text=True)
    return float(r.stdout.strip())


SCENES = []
for name, fname in SCENE_LIST:
    p = VO_DIR / fname
    if not p.exists():
        print(f"  [skip] {fname} missing")
        continue
    SCENES.append((name, probe_dur(p), fname))

# V3 master VO uses 0.35s acrossfade (vs V2's 0.20s). Each crossfade compresses
# the master timeline by D relative to raw cumulative durations.
D_CROSSFADE = 0.35

scene_starts = [0.0]
for i, (_, dur, _) in enumerate(SCENES):
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

# V3 key topic terms — aftercare products, margin numbers, penetration rate
KEY_TERMS = [
    # Aftercare products (Scene 3 + 4)
    "paint", "protection", "tint", "window", "interior", "dash", "camera",
    "ceramic", "coating", "tyre", "rim", "fabric", "alloy", "warranty",
    # Margin / dollar figures (Scene 4)
    "fifteen", "hundred", "thousand", "two", "three", "four", "five", "six",
    "percent", "margin", "retail", "cost", "stack",
    # Penetration rate (Scene 4 + 5)
    "penetration", "attach", "sixty", "seventy", "eighty", "twenty", "thirty",
    "finance", "average", "gross",
    # Sign-off / brand
    "Mac", "aftercare", "subscribe",
]
print(f"\nSearching for topic-aligned timestamps:\n")
for scene in results["scenes"]:
    print(f"--- Scene {scene['scene_id']} {scene['name']} ({scene['scene_start_in_timeline']:.2f}s start) ---")
    for w in scene["words"]:
        wl = w["word"].lower().strip(",.!?")
        for term in KEY_TERMS:
            if term in wl or wl in term:
                print(f"  {w['timeline_start']:7.2f}s  '{w['word']}'")
                break
