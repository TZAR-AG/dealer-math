# Find exact timestamps for dollar-figure overlays from transcribed VOs.
# Uses the JSON output of transcribe-vos.py.

import json
from pathlib import Path

REPO = Path(r"C:\dev\Claude")
TRANSCRIPT = REPO / "content" / "au-dealer-math" / "scripts" / "v01-renders" / "vo-transcriptions.json"

data = json.loads(TRANSCRIPT.read_text())

# Build a flat list of all words with timeline positions
all_words = []
for scene in data["scenes"]:
    for w in scene["words"]:
        all_words.append({
            "word": w["word"].strip(),
            "lower": w["word"].lower().strip(",.!?\"'"),
            "start": w["timeline_start"],
            "end": w["timeline_end"],
            "scene": scene["name"],
        })


def find_phrase(target_words, after_sec=0):
    """Find the timeline_start of the first word in a target_words sequence (lowercased).
    Search starts after the given timestamp. Returns (start_sec, matched_text) or None."""
    n = len(target_words)
    for i in range(len(all_words) - n + 1):
        if all_words[i]["start"] < after_sec:
            continue
        match = True
        for j in range(n):
            if all_words[i + j]["lower"] != target_words[j].lower():
                match = False
                break
        if match:
            return (all_words[i]["start"], " ".join(all_words[i + j]["word"] for j in range(n)))
    return None


# Targets for each overlay
SEARCHES = [
    # (overlay_filename, [phrase to find], after_seconds)
    ("01-hook-300-week",      ["weekly", "budget"],                              0.0),    # hook opens with budget question
    ("02-four-years",         ["four", "years"],                                146.0),   # scene 4 starts ~146s
    ("03-seven-years",        ["seven", "years"],                                146.0),
    ("04-46k-more",           ["forty-six", "thousand"],                        146.0),
    ("05-aftercare-retail",   ["fifteen", "hundred"],                            280.0),  # scene 5 starts ~280s
    ("06-aftercare-cost",     ["five", "hundred"],                               280.0),
    ("07-aftercare-gross",    ["one-thousand"],                                  280.0),
]

print("=" * 60)
print("Overlay timestamp lookup")
print("=" * 60)
for overlay, phrase, after in SEARCHES:
    result = find_phrase(phrase, after)
    if result:
        ts, matched = result
        print(f"  {overlay:30s} -> {ts:7.2f}s  ('{matched}')")
    else:
        # Fall back: try first word only
        single_result = find_phrase([phrase[0]], after)
        if single_result:
            ts, matched = single_result
            print(f"  {overlay:30s} -> {ts:7.2f}s  (partial match: '{matched}')")
        else:
            print(f"  {overlay:30s} -> NOT FOUND  (searched for {phrase!r} after {after}s)")

# Also dump the relevant scenes' word lists for manual inspection
print("\n" + "=" * 60)
print("Scene 1 (hook) words:")
print("=" * 60)
for w in all_words:
    if w["scene"] == "hook":
        print(f"  {w['start']:6.2f}s  {w['word']}")

print("\n" + "=" * 60)
print("Scene 4 (loan trick) — first 80 words for math timestamps:")
print("=" * 60)
loan_words = [w for w in all_words if w["scene"] == "loantrick"][:80]
for w in loan_words:
    print(f"  {w['start']:6.2f}s  {w['word']}")

print("\n" + "=" * 60)
print("Scene 5 (why dealer) — words around aftercare section (offset ~155s into scene):")
print("=" * 60)
# Scene 5 starts at 280.18s. Aftercare segment is roughly 60-80% in (~340-360s timeline)
relevant = [w for w in all_words if w["scene"] == "whydealer" and 320 < w["start"] < 380]
for w in relevant:
    print(f"  {w['start']:6.2f}s  {w['word']}")
