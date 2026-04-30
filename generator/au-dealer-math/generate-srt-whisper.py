# Generate AUDM V1 SRT subtitle file via faster-whisper.
# Transcribes each scene VO + adjusts timestamps to timeline positions.
# Run from repo root: python generator/au-dealer-math/generate-srt-whisper.py

from pathlib import Path
from faster_whisper import WhisperModel

REPO = Path(r"C:\dev\Claude")
VO_DIR = REPO / "content" / "au-dealer-math" / "scripts" / "v01-renders" / "voice"
SRT_OUT = REPO / "video" / "out" / "audm-v1-payment-not-price-pivot.srt"
SRT_OUT.parent.mkdir(parents=True, exist_ok=True)

# Scene order + actual durations (from build-v1-davinci.py SCENES dict).
# These cumulative starts are where each VO sits on the final timeline.
SCENES = [
    ("vo-scene-1-hook.mp3",      20.1085),
    ("vo-scene-2-authority.mp3", 33.0652),
    ("vo-scene-3-question.mp3",  93.5300),
    ("vo-scene-4-loan-trick.mp3", 133.4683),
    ("vo-scene-5-why-dealer.mp3", 157.2455),
    ("vo-scene-6-fix.mp3",       138.6231),
    ("vo-scene-7-signoff.mp3",   12.4100),
]

scene_starts = [0.0]
for _, dur in SCENES:
    scene_starts.append(scene_starts[-1] + dur)


def srt_timestamp(seconds):
    """Convert seconds to SRT format HH:MM:SS,mmm."""
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int((seconds - int(seconds)) * 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


print("Loading faster-whisper small.en model...")
model = WhisperModel("small.en", device="cpu", compute_type="int8")
print("Loaded.\n")

# Custom dictionary — terms whisper often mishears that we want corrected.
# We'll do a simple post-transcription replace.
DICT = {
    "Mark": "Mac",
    "Mc.": "Mac.",
    "Mc,": "Mac,",
    " Mc ": " Mac ",
    "drive away": "drive-away",
    "drive-away ": "drive-away ",
    "Hi-Lux": "HiLux",
    "Volkswagen": "Volkswagen",
    "GFV": "GFV",
}


def fix_transcription(text):
    for bad, good in DICT.items():
        text = text.replace(bad, good)
    return text


print(f"Transcribing {len(SCENES)} VOs and building SRT...")
srt_entries = []  # list of (start_sec, end_sec, text)

for i, (fname, _) in enumerate(SCENES):
    audio_path = VO_DIR / fname
    if not audio_path.exists():
        print(f"  [skip] {fname} missing")
        continue
    scene_offset = scene_starts[i]
    print(f"  [{i+1}/{len(SCENES)}] {fname} (offset {scene_offset:.2f}s)...")
    segments, info = model.transcribe(
        str(audio_path),
        language="en",
        beam_size=5,
        # Sentence-level segments are what Whisper returns by default
    )
    seg_count = 0
    for seg in segments:
        text = fix_transcription(seg.text.strip())
        if not text:
            continue
        srt_entries.append((
            scene_offset + seg.start,
            scene_offset + seg.end,
            text,
        ))
        seg_count += 1
    print(f"      -> {seg_count} segments")

# Write SRT
print(f"\nWriting SRT to {SRT_OUT}...")
with open(SRT_OUT, "w", encoding="utf-8", newline="\n") as f:
    for idx, (start, end, text) in enumerate(srt_entries, 1):
        f.write(f"{idx}\n")
        f.write(f"{srt_timestamp(start)} --> {srt_timestamp(end)}\n")
        f.write(f"{text}\n\n")

print(f"Wrote {len(srt_entries)} subtitle entries.")
print(f"\nSRT: {SRT_OUT}")
print(f"\nUpload this alongside the MP4 in YouTube Studio:")
print(f"  Video: {REPO / 'video' / 'out' / 'audm-v1-payment-not-price-pivot.mp4'}")
print(f"  SRT:   {SRT_OUT}")
