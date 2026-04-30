# Transcribe AUDM V1 voiceovers with word-level timestamps via faster-whisper.
# Outputs JSON file with words + start/end times per scene.
# Used to find exact timestamps for dollar-figure overlays.

import json
import os
from pathlib import Path
from faster_whisper import WhisperModel

REPO = Path(r"C:\dev\Claude")
VO_DIR = REPO / "content" / "au-dealer-math" / "scripts" / "v01-renders" / "voice"
OUT_FILE = REPO / "content" / "au-dealer-math" / "scripts" / "v01-renders" / "vo-transcriptions.json"

# CPU "small" model is fast + accurate enough for this. ~250MB download first time.
print("Loading faster-whisper small.en model...")
model = WhisperModel("small.en", device="cpu", compute_type="int8")
print("Loaded.\n")

# SCENE actual durations (from build-v1-davinci.py SCENES dict)
# Used to compute cumulative scene start positions in the final timeline.
SCENES = [
    ("hook",      20.1085, "vo-scene-1-hook.mp3"),
    ("authority", 33.0652, "vo-scene-2-authority.mp3"),
    ("question",  93.5300, "vo-scene-3-question.mp3"),
    ("loantrick", 133.4683, "vo-scene-4-loan-trick.mp3"),
    ("whydealer", 157.2455, "vo-scene-5-why-dealer.mp3"),
    ("fix",       138.6231, "vo-scene-6-fix.mp3"),
    ("signoff",   12.4100,  "vo-scene-7-signoff.mp3"),
]

scene_starts = [0.0]
for _, dur, _ in SCENES:
    scene_starts.append(scene_starts[-1] + dur)

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

# Quick search for key dollar terms
KEY_TERMS = [
    "weekly", "three hundred", "300",
    "sixty-two", "62", "thousand",
    "hundred and nine", "109",
    "forty-six", "46,800",
    "fifteen hundred", "1,500",
    "three thousand", "3,000",
    "five hundred", "500",
    "one thousand", "twenty-five hundred", "2,500",
    "sixty to eighty", "60", "80",
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
