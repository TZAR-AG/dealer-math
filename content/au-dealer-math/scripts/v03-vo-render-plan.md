# V3 VO Render Plan — ElevenLabs Mac

**Script:** [v03-the-aftercare-room.md](v03-the-aftercare-room.md)
**Voice:** Mac (ElevenLabs Paul · Voice ID `WLKp2jV6nrS8aMkPPDRO`)
**Settings:** Multilingual v2 / Stability 0.40 / Similarity 0.75 / Style 0.25 / Speaker Boost ON / Speed 0.90
**Total target runtime:** ~9:10 (per script word-count estimate)
**Total segments:** 6
**Render mechanism:** `generator/au-dealer-math/regenerate-vo.js` with request stitching (`previous_text`, `next_text`, `previous_request_ids`)

---

## Why segment + splice (not single-render)

Per `content/au-dealer-math/saas-prompts/elevenlabs-paul.md` § Chunk strategy:

> **Verdict: keep one-scene-per-call AND add stitching params. Don't split scenes further.**
>
> Scene typical size: 400-700 chars → already in the 250-800 sweet spot. What was missing: each scene was sent as isolated request with no context → tone drift between scenes. Stitching solves drift better than smaller chunks would.

Each segment = one act/scene from the script body. Each render call passes:
- The current segment's text
- Last 200 chars of the previous segment as `previous_text`
- First 200 chars of the next segment as `next_text`
- Previous segment's `request-id` in `previous_request_ids` (valid 2 hours, capture from response header)

This produces 6 separate MP3s with continuous tone across the boundaries. Splice via ffmpeg `acrossfade` chain per `reference_audm_video_production_pipeline.md`.

---

## Segment table

Word counts are approximate; final char counts will round to 250-800 sweet spot.

| Seg | Script section | Approx words | Approx chars | Approx runtime @ 0.90 |
|---|---|---|---|---|
| 01 | [0:00–0:30] HOOK | 75 | ~470 | ~30s |
| 02 | [0:30–1:30] AUTHORITY ANCHOR + THREE-ROOM REANCHOR | 175 | ~1,050 | ~1:00 |
| 03 | [1:30–3:00] WHAT THE AFTERCARE ROOM SELLS | 270 | ~1,650 | ~1:30 |
| 04 | [3:00–5:00] THE MATH REVEAL | 365 | ~2,200 | ~2:00 |
| 05 | [5:00–7:00] WHY PENETRATION IS HIGH | 350 | ~2,100 | ~1:55 |
| 06 | [7:00–9:00] WHAT TO DO + V4 PREVIEW + LOCKED ENDING | 275 | ~1,650 | ~1:35 |
| **Total** | | **~1,510** | **~9,120** | **~8:30 spoken + buffers + pauses ≈ 9:10** |

**Note on segment-04 size:** 2,200 chars exceeds the 250-800 sweet spot. Split into two sub-segments at the natural beat where the script transitions from "margin numbers" to "penetration rate" comparison:
- 04a: paint protection + tint + stacked margin (~3:00–4:00, ~1,100 chars)
- 04b: penetration rate comparison + average aftercare gross conclusion (~4:00–5:00, ~1,100 chars)

Adjusted total: 7 segments instead of 6.

| Seg | Script section | Approx chars |
|---|---|---|
| 01 | HOOK | ~470 |
| 02 | AUTHORITY ANCHOR + THREE-ROOM | ~1,050 |
| 03 | AFTERCARE MENU | ~1,650 |
| 04a | MATH REVEAL — margins on each product | ~1,100 |
| 04b | MATH REVEAL — penetration rate + average aftercare gross | ~1,100 |
| 05 | WHY PENETRATION IS HIGH | ~2,100 |
| 06 | WHAT TO DO + V4 PREVIEW + LOCKED ENDING | ~1,650 |

(Segment 03 + 05 are still over the 800-char top of the sweet spot. Acceptable per the canonical reference: *"chunk size: ≤2000 chars (we send full scenes, ~400-700 chars each). Sweet spot 250-800 chars per chunk; >1000 = tone drift; <250 = inconsistency."* If tone drift shows in segments 03/05 on render, split them at natural paragraph boundaries.)

**Final segment count: 7.** Adjust `regenerate-vo.js` segment array accordingly.

---

## Output paths (per AUDM convention)

```
voice/v03-vo-seg-01-hook.mp3
voice/v03-vo-seg-02-three-room.mp3
voice/v03-vo-seg-03-aftercare-menu.mp3
voice/v03-vo-seg-04a-margins.mp3
voice/v03-vo-seg-04b-penetration.mp3
voice/v03-vo-seg-05-why-high.mp3
voice/v03-vo-seg-06-what-to-do.mp3
voice/v03-master-vo.mp3        # spliced final
```

---

## Splice pipeline (after all 7 segments render)

Per `reference_audm_video_production_pipeline.md`:

```bash
ffmpeg -y \
  -i voice/v03-vo-seg-01-hook.mp3 \
  -i voice/v03-vo-seg-02-three-room.mp3 \
  -i voice/v03-vo-seg-03-aftercare-menu.mp3 \
  -i voice/v03-vo-seg-04a-margins.mp3 \
  -i voice/v03-vo-seg-04b-penetration.mp3 \
  -i voice/v03-vo-seg-05-why-high.mp3 \
  -i voice/v03-vo-seg-06-what-to-do.mp3 \
  -filter_complex "
    [0:a][1:a]acrossfade=d=0.35:c1=tri:c2=tri[a01];
    [a01][2:a]acrossfade=d=0.35:c1=tri:c2=tri[a02];
    [a02][3:a]acrossfade=d=0.35:c1=tri:c2=tri[a03];
    [a03][4:a]acrossfade=d=0.35:c1=tri:c2=tri[a04];
    [a04][5:a]acrossfade=d=0.35:c1=tri:c2=tri[a05];
    [a05][6:a]acrossfade=d=0.35:c1=tri:c2=tri[out]" \
  -map "[out]" -c:a libmp3lame -q:a 2 voice/v03-master-vo.mp3
```

**Why 0.35s acrossfade:** balances clean handoff against perceptible cut. V1 + V2 used 0.35s as the locked default. Don't deviate.

---

## ElevenLabs API call template (per segment)

Per `content/au-dealer-math/saas-prompts/elevenlabs-paul.md` § Canonical API request body:

```javascript
const body = {
  text: segmentText,                             // 470-2200 chars per segment
  model_id: "eleven_multilingual_v2",
  language_code: "en",                           // forces English path, locks AU accent

  voice_settings: {
    stability: 0.40,
    similarity_boost: 0.75,
    style: 0.25,
    use_speaker_boost: true,
    speed: 0.90
  },

  apply_text_normalization: "on",                // forces $1,800 → "one thousand eight hundred dollars" — though the script already spells dollar figures out, defence-in-depth
  seed: 42424243,                                // V2 used 42424242; V3 uses 42424243 + i for each segment
  previous_text: prevSnippet,                    // last 200 chars of prior segment
  next_text: nextSnippet,                        // first 200 chars of next segment
  previous_request_ids: prevReqId ? [prevReqId] : []
};

// Query params:
// ?output_format=mp3_44100_128 (default — Starter tier)
```

Capture the response header `request-id` from each call → pass as `previous_request_ids` to the next call within the same render run. Request ID chain is valid for 2 hours.

---

## Phonetic respelling check

Per `content/au-dealer-math/saas-prompts/elevenlabs-paul.md` § Phonetic respelling fallback (Starter tier):

Scan the V3 script for any of the dictionary words → swap to phonetic spelling.

| Word in script | Phonetic respelling needed? |
|---|---|
| Mac | ❌ NO — single syllable, ElevenLabs Multilingual v2 renders cleanly first try (per `feedback_audm_no_overpromising_signoff.md` § Handle locked: "Mac") |
| Hilux | (not in script body, only listed in MJ prompts) |
| Tucson | (not in script body) |
| Toyota | (not in script body) |
| Hyundai | (not in script body — "HUN-day" would apply if used) |

**No phonetic respellings required for V3.** Script renders directly.

---

## Per-segment edits before render

Before sending each segment to ElevenLabs, scan for:

| Risk | Check | Fix |
|---|---|---|
| Audio tag bleed | Any `[pause]` or `[excited]` text | None expected — script doesn't use audio tags |
| Ellipsis trail-off | Any `...` in scene text | None present — checked QC, script uses em-dashes and full stops only |
| Long break tag | More than 2 `<break>` tags per segment | Don't add any to V3 segments. Natural punctuation carries the cadence at speed 0.90. |
| ALL-CAPS bleed | Any all-caps word for emphasis | None — script uses no all-caps. (DaVinci on-screen text is rendered separately at edit, not in the VO script.) |
| Banned phrase | scam / fraud / rip-off / hidden / secret / trick / lying | None present — verified in QC pass |
| Sign-off block | Verify segments 06 ends with locked 5-block | Confirmed: segment 06 ends with `Thank you for watching. / If you found this helpful, please like and subscribe. / I'm Mac on A. U. Dealer Math.` |

**Critical for segment 06:** the period+space pattern `A. U.` MUST be preserved verbatim (forces letter-spelling "AY-YOO"). Period after "Math." gives final-beat inflection. NO ellipsis anywhere in the sign-off.

---

## Render execution

**Adrian runs:**

```bash
cd c:/dev/Claude/generator/au-dealer-math

# Edit regenerate-vo.js to point at the V3 script + 7 segments above
# Then run:
node regenerate-vo.js v03

# Verifies each segment renders cleanly + captures request-ids for stitching
# Total wall-time: ~7 segments × ~30s render each = ~3-5 min
```

After all 7 segments render, run the splice pipeline above to produce `voice/v03-master-vo.mp3`.

**QC pass after splice:**
1. Listen to the full master VO end-to-end (~9:10)
2. Verify no audible cut artifacts at acrossfade boundaries
3. Verify no tone drift — Mac sounds like one continuous narrator, not 7 stitched chunks
4. Verify dollar figures rendered correctly — *"fifteen hundred to two and a half thousand dollars"*, *"four to six hundred dollars"*, *"six hundred to seven hundred dollars"*, *"seventy to seventy-five percent"*, *"sixty to eighty percent"*, *"twenty to thirty percent"*
5. Verify sign-off lands clean — *"I'm Mac on A. U. Dealer Math."* with full inflection on "Math"

If any segment drifts, re-render that segment alone with adjusted `previous_text` / `next_text` and re-splice.

---

## Time budget for VO

| Phase | Wall-time |
|---|---|
| Segment text-prep + segment array config | 5 min |
| Render 7 segments via `regenerate-vo.js` | 5 min |
| Splice via ffmpeg acrossfade chain | 1 min |
| QC pass (listen to master) | 10 min |
| Re-render any drift segment + re-splice | 5 min (contingency) |
| **Total** | **~25 min** |

---

## Reference

- Canonical: `content/au-dealer-math/saas-prompts/elevenlabs-paul.md`
- Pipeline: `reference_audm_video_production_pipeline.md`
- V2 render script: `generator/au-dealer-math/regenerate-vo-v02.js` (use as template, copy to `regenerate-vo-v03.js` and edit segment array per parameterisation decision in `reference_audm_v1_inside_out_verification_2026-05-02.md`)
- Voice settings lock: `feedback_audm_no_overpromising_signoff.md` § ElevenLabs phonetic locks
- Audio finalize (post-DaVinci): `reference_audm_audio_finalize_lock_2026-05-04.md`
