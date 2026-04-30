# Generate AUDM V1 subtitles via DaVinci's on-device STT, then export as SRT.
#
# Run inside DaVinci Resolve 20 Py3 Console after the V1 timeline is built.
# Paste the standard one-line invocation pattern with this file path.
#
# This:
# 1. Triggers Timeline.CreateSubtitlesFromAudio() on the active timeline
# 2. Polls until subtitle items appear (STT typically takes 1-3 min for 10-min video)
# 3. Reads each subtitle item's start/end + text
# 4. Writes SRT to video/out/audm-v1-payment-not-price-pivot.srt

import time
from pathlib import Path

REPO = Path(r"C:\dev\Claude")
SRT_OUT = REPO / "video" / "out" / "audm-v1-payment-not-price-pivot.srt"
SRT_OUT.parent.mkdir(parents=True, exist_ok=True)

print("=" * 60)
print("AUDM V1 - Generate subtitles + export SRT")
print("=" * 60)

if 'resolve' not in dir():
    raise RuntimeError("'resolve' global not found. Run inside DaVinci Resolve Py3 Console.")

pm = resolve.GetProjectManager()
project = pm.GetCurrentProject()
if not project:
    project = pm.LoadProject("AUDM_V1_PaymentNotPrice")
print(f"Project: {project.GetName()}")

timeline = project.GetCurrentTimeline()
if not timeline:
    raise RuntimeError("No active timeline")
print(f"Timeline: {timeline.GetName()}")

fps = float(project.GetSetting("timelineFrameRate"))
print(f"Frame rate: {fps} fps")
tl_start = timeline.GetStartFrame()
print(f"Timeline start frame: {tl_start}")

resolve.OpenPage("edit")

existing_count = 0
try:
    existing_items = timeline.GetItemListInTrack("subtitle", 1) or []
    existing_count = len(existing_items)
except Exception:
    pass
print(f"Existing subtitle items: {existing_count}")

if existing_count == 0:
    print("\nTriggering Create Subtitles from Audio...")
    settings = {
        "trackIndex": 1,
        "language": "en-AU",
        "captionPreset": "default",
        "charsPerCaption": 42,
        "wordsPerLine": 8,
    }
    try:
        result = timeline.CreateSubtitlesFromAudio(settings)
    except Exception as e:
        print(f"  CreateSubtitlesFromAudio with settings failed: {e}")
        try:
            result = timeline.CreateSubtitlesFromAudio({})
        except Exception as e2:
            print(f"  Fallback failed: {e2}")
            result = None
    print(f"  CreateSubtitlesFromAudio returned: {result}")

    print("\nPolling for subtitles (this may take 2-5 min for a 10-min video)...")
    for attempt in range(120):
        time.sleep(2)
        try:
            items = timeline.GetItemListInTrack("subtitle", 1) or []
            count = len(items)
        except Exception:
            count = 0
        if count > 0:
            time.sleep(3)
            items = timeline.GetItemListInTrack("subtitle", 1) or []
            print(f"  Subtitles ready: {len(items)} items")
            break
        if attempt % 5 == 0:
            print(f"  ...still processing (attempt {attempt + 1}/120)")
    else:
        print("[warn] Timed out waiting for subtitles")

items = timeline.GetItemListInTrack("subtitle", 1) or []
print(f"\nFound {len(items)} subtitle items")
if not items:
    raise RuntimeError("No subtitle items - STT may have failed")


def frame_to_srt_time(frame_offset_from_tl, fps):
    total_seconds = frame_offset_from_tl / fps
    h = int(total_seconds // 3600)
    m = int((total_seconds % 3600) // 60)
    s = int(total_seconds % 60)
    ms = int((total_seconds - int(total_seconds)) * 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def get_subtitle_text(item):
    for prop in ["Text", "Subtitle Text", "Subtitle", "Caption Text"]:
        try:
            t = item.GetClipProperty(prop)
            if t and t.strip():
                return t.strip()
        except Exception:
            continue
    try:
        n = item.GetName()
        if n and n.strip() and n != "Subtitle":
            return n.strip()
    except Exception:
        pass
    return None


print(f"\nWriting SRT to {SRT_OUT}...")
written = 0
with open(SRT_OUT, "w", encoding="utf-8", newline="\n") as f:
    for i, item in enumerate(items, 1):
        text = get_subtitle_text(item)
        if not text:
            print(f"  [warn] item {i}: no text extracted")
            continue
        start_offset = item.GetStart() - tl_start
        end_offset = item.GetEnd() - tl_start
        f.write(f"{i}\n")
        f.write(f"{frame_to_srt_time(start_offset, fps)} --> {frame_to_srt_time(end_offset, fps)}\n")
        f.write(f"{text}\n\n")
        written += 1

print(f"Wrote {written} / {len(items)} subtitle entries to SRT")
print(f"\n{'=' * 60}")
print(f"SRT file: {SRT_OUT}")
print(f"{'=' * 60}")
print()
print("Next step: upload this SRT to YouTube alongside the MP4.")
print("YouTube Studio - upload video - Subtitles - Upload SRT")
