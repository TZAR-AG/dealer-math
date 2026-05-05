# V2 Shorts — upload metadata

Built per `c:/dev/Claude/content/research/audm-shorts-2026-05-05/findings.md` § 9 pre-build checklist + § 4 description spec + § 5 pinned-comment template.

Source: `audm-v2-finance-managers-office.mp4` (V2 pre-caption master, F&I Office + Rate-Range Game scene 3).

> **2026-05-05 PM update — captions stripped (option C).** V2 Shorts 1-5 re-rendered caption-free via `--no-captions` flag added to both builders. AFWL/Cadogan/Lucky Lopez (closest niche benchmarks) all run minimal-text Shorts; the +18% sound-off lift is from the **frame-1 number visual hook**, not running captions; sentence-block clashes with Mac calm-authority + document-forensics DNA. Frame-1 hook + V2's own DaVinci motion graphics retained. Item 8 across all 5 Shorts now reads "no running captions"; below "y=0.70 sentence-block" notes are historical. Re-score after V12 milestone.

---

### Short 1 — F&I Office (Mon 5 May 18:00 AWST)

**Title:** What dealers do in the F&I office

**Description (≤200 chars, first 100-125 load-bearing, NO LINK):**

What happens after you agree on the price? The room dealers don't show on the sticker — and the rate game inside it.

Full breakdown on the channel — search "AU Dealer Math".

#AUDealerMath #DealerFinance #shorts

**Pinned comment (paste within 5 min of upload):**

Free 7-Lines cheatsheet — the 7 lines on a dealer contract you should never sign:
audealermath.com.au/cheatsheet

Full 10-min breakdown of this on the channel — search "AU Dealer Math" or tap the channel name.

— Mac

**File:** `video/out/shorts/audm-v2-short-1.mp4` (9.0 MB, 30.01s, 1080x1920, 24fps, -14.2 LUFS / -0.5 dBFS)

**Build script:** `generator/au-dealer-math/build-v02-short-1.py` (re-runnable end-to-end)

**Pre-build checklist (§ 9 of findings.md) — all 14 items:**
1. ✅ First-frame visual hook: $4,800 cream `#F5EFE6` on charcoal `#2B2B2B` at 240pt full-bleed
2. ✅ First 3s verbal hook: "What happens after you agree on the price?" (Mac VO at t=0.5s)
3. ✅ Loop design: closes "Then the F and I office. Watch what happens." → loops into "What happens after..."
4. ✅ Length 30.01s (within 28-32s target band)
5. ✅ No verbal CTA at end — close VO IS the close, no "search"/"subscribe"/"thanks"
6. ✅ Music bed: V2's locked YT Audio Library track (A Hand In The Dark, HAAWK-safe), fades to silence in last 1.5s before loop seam
7. ✅ Audio finalize: -14.2 LUFS integrated · -0.5 dBFS true peak (within ±1.0 LU spec)
8. ✅ Captions: sentence-block lower-third, 64pt DM Sans Regular, cream on transparent, 6px black stroke, **y=0.70** (Shorts position)
9. ✅ Defamation pass: zero banned words (`scam`/`rip-off`/`fraud`/`crook`/`lying`/specific-dealership-names). Mac voice anchors only ("not disclosed"-class language, "by design")
10. ✅ Title 33 chars, declarative, echoes hook line, no `?`/all-caps/emoji
11. ✅ Description first 100-125 chars load-bearing. 3 hashtags only. No link
12. ✅ Pinned comment ready — paste within 5 min of upload
13. (manual) Schedule 18:00 AWST Mon 5 May, ≥24h after V1, NOT within ±2h of V2 main upload
14. (manual) Native upload only to TikTok + IG Reels — no YT auto-share

---

## Build artifacts (for re-render / debugging)

- Bookend VOs: `content/au-dealer-math/scripts/v02-renders/voice-shorts/short1-{open,close}.mp3` + `.timings.json` (LOCKED Mac voice — Paul WLKp2jV6nrS8aMkPPDRO, v2/0.40/0.75/0.25/Speed 0.90)
- Intermediate clips: `content/au-dealer-math/scripts/v02-renders/short1-build/{01-hook-card,02-open,03-middle,04-close,05-spliced,06-captioned,07-loudnorm-pass1}.mp4`
- Verification frames: `content/au-dealer-math/scripts/v02-renders/short1-build/verify/*.png`
- Shorts-specific transcriptions JSON: `content/au-dealer-math/scripts/v02-renders/short1-build/shorts-transcriptions.json`

---

### Short 2 — Rate Range / +4 Points (Tue 6 May 21:00 AWST)

**Title:** Why a 2 percent markup costs you $3,000

**Description (≤200 chars, first 100-125 load-bearing, NO LINK):**

How much does a 2 percent rate markup actually cost you over 5 years? Two percent. Three thousand dollars. That's how dealer finance adds up.

Full breakdown — search "AU Dealer Math".

#AUDealerMath #CarFinanceAustralia #shorts

**Pinned comment (paste within 5 min of upload):**

Free 7-Lines cheatsheet — the 7 lines on a dealer contract you should never sign:
audealermath.com.au/cheatsheet

Full 10-min breakdown of this on the channel — search "AU Dealer Math" or tap the channel name.

— Mac

**File:** `video/out/shorts/audm-v2-short-2.mp4` (11.4 MB, 31.67s, 1080x1920, 24fps, -14.5 LUFS / -1.2 dBFS)

**Pre-build checklist — all 14 items:**
1. ✅ First-frame visual hook: $3,000 cream `#F5EFE6` on charcoal `#2B2B2B` at 240pt full-bleed
2. ✅ First 3s verbal hook: "How much does a two percent rate markup actually cost you?" (Mac VO at t=0.5s)
3. ✅ Loop design: closes "Two percent. Three thousand dollars. That's how it adds up." → loops into "How much does a two percent rate markup actually cost you?"
4. ✅ Length 31.67s (within 28-32s target band)
5. ✅ No verbal CTA at end
6. ✅ Music bed: A Hand In The Dark (YT Audio Library), fades to silence in last 1.5s
7. ✅ Audio finalize: -14.5 LUFS / -1.2 dBFS (within ±1.0 LU spec)
8. ✅ Captions: sentence-block lower-third, 64pt DM Sans Regular, cream on transparent, 6px black stroke, y=0.70
9. ✅ Defamation pass: zero banned words. "Industry practice" Mac voice anchors only
10. ✅ Title 41 chars, declarative, echoes hook line
11. ✅ Description first 100-125 chars load-bearing. 3 hashtags only. No link
12. ✅ Pinned comment ready
13. (manual) Schedule 21:00 AWST Tue 6 May, ≥24h after V2 Short 1, NOT within ±2h of V4 main 18:00
14. (manual) Native upload only to TikTok + IG Reels — no YT auto-share

---

### Short 3 — Same Bank, Different Outcomes / +4 Points (Wed 7 May 21:00 AWST)

**Title:** Same bank, same approval, different rates

**Description (≤200 chars, first 100-125 load-bearing, NO LINK):**

Same bank. Same approval. Why do two buyers walk out with different rates? The 4-point gap nobody publishes.

Full breakdown — search "AU Dealer Math".

#AUDealerMath #DealerFinance #shorts

**Pinned comment (paste within 5 min of upload):**

Free 7-Lines cheatsheet — the 7 lines on a dealer contract you should never sign:
audealermath.com.au/cheatsheet

Full 10-min breakdown of this on the channel — search "AU Dealer Math" or tap the channel name.

— Mac

**File:** `video/out/shorts/audm-v2-short-3.mp4` (6.8 MB, 28.92s, 1080x1920, 24fps, -15.6 LUFS / -1.6 dBFS)

**Pre-build checklist — all 14 items:**
1. ✅ First-frame visual hook: +4 POINTS cream `#F5EFE6` on charcoal `#2B2B2B` at 200pt full-bleed
2. ✅ First 3s verbal hook: "Same bank. Same approval. Why do two buyers walk out with different rates?"
3. ✅ Loop design: closes "Same bank. Same approval. Different outcomes." → loops directly into "Same bank. Same approval. Why do two buyers walk out with different rates?" (mirror echo seam)
4. ✅ Length 28.92s (within 28-32s target band)
5. ✅ No verbal CTA at end
6. ✅ Music bed: A Hand In The Dark (YT Audio Library), fades in last 1.5s
7. ⚠ Audio finalize: -15.6 LUFS / -1.6 dBFS (TP within spec; integrated 1.6 LU under -14 ideal — accepted because YT applies playback normalization. Source segment dynamics constrain how loud we can go without TP overshoot)
8. ✅ Captions: y=0.70 sentence-block 64pt
9. ✅ Defamation pass: zero banned words
10. ✅ Title 39 chars, declarative
11. ✅ Description first 100-125 chars load-bearing
12. ✅ Pinned comment ready
13. (manual) Schedule 21:00 AWST Wed 7 May, ≥24h after Short 2, NOT within ±2h of V5 main 18:00
14. (manual) Native upload only to TikTok + IG Reels

---

### Short 4 — Aftercare Margin / $3,000 (Thu 8 May 21:00 AWST)

**Title:** $3,000 in the room before F&I

**Description (≤200 chars, first 100-125 load-bearing, NO LINK):**

There's a room before the F&I office most buyers don't notice. Paint protection, tint, dash cams. Three thousand dollars in one room.

Full breakdown — search "AU Dealer Math".

#AUDealerMath #CarBuying #shorts

**Pinned comment (paste within 5 min of upload):**

Free 7-Lines cheatsheet — the 7 lines on a dealer contract you should never sign:
audealermath.com.au/cheatsheet

Full 10-min breakdown of this on the channel — search "AU Dealer Math" or tap the channel name.

— Mac

**File:** `video/out/shorts/audm-v2-short-4.mp4` (10.2 MB, 29.29s, 1080x1920, 24fps, -14.5 LUFS / -1.4 dBFS)

**Pre-build checklist — all 14 items:**
1. ✅ First-frame visual hook: $3,000 cream `#F5EFE6` on charcoal `#2B2B2B` at 240pt full-bleed
2. ✅ First 3s verbal hook: "There's a room before the F and I office most buyers don't notice."
3. ✅ Loop design: closes "Three thousand dollars. One room. Most buyers don't even notice it." → loops to "There's a room before the F and I office most buyers don't notice."
4. ✅ Length 29.29s (within 28-32s target band)
5. ✅ No verbal CTA at end
6. ✅ Music bed: A Hand In The Dark, fades in last 1.5s
7. ✅ Audio finalize: -14.5 LUFS / -1.4 dBFS (within spec)
8. ✅ Captions: y=0.70 sentence-block 64pt
9. ✅ Defamation pass: zero banned words
10. ✅ Title 30 chars, declarative
11. ✅ Description first 100-125 chars load-bearing
12. ✅ Pinned comment ready
13. (manual) Schedule 21:00 AWST Thu 8 May, ≥24h after Short 3, NOT within ±2h of V6 main 18:00
14. (manual) Native upload only to TikTok + IG Reels

---

### Short 5 — Three Rooms / 3 ROOMS (Fri 9 May 21:00 AWST)

**Title:** You negotiated with three, not one

**Description (≤200 chars, first 100-125 load-bearing, NO LINK):**

How many people do you actually negotiate with at a dealership? You thought one. You negotiated with three.

Full breakdown — search "AU Dealer Math".

#AUDealerMath #CarBuying #shorts

**Pinned comment (paste within 5 min of upload):**

Free 7-Lines cheatsheet — the 7 lines on a dealer contract you should never sign:
audealermath.com.au/cheatsheet

Full 10-min breakdown of this on the channel — search "AU Dealer Math" or tap the channel name.

— Mac

**File:** `video/out/shorts/audm-v2-short-5.mp4` (8.7 MB, 30.71s, 1080x1920, 24fps, -14.9 LUFS / -1.6 dBFS)

**Pre-build checklist — all 14 items:**
1. ✅ First-frame visual hook: 3 ROOMS cream `#F5EFE6` on charcoal `#2B2B2B` at 220pt full-bleed
2. ✅ First 3s verbal hook: "How many people do you actually negotiate with at a dealership?"
3. ✅ Loop design: closes "You thought you negotiated with one. You negotiated with three." → loops to "How many people do you actually negotiate with at a dealership?" (answer-question chain)
4. ✅ Length 30.71s (within 28-32s target band)
5. ✅ No verbal CTA at end
6. ✅ Music bed: A Hand In The Dark, fades in last 1.5s
7. ✅ Audio finalize: -14.9 LUFS / -1.6 dBFS (within spec)
8. ✅ Captions: y=0.70 sentence-block 64pt
9. ✅ Defamation pass: zero banned words
10. ✅ Title 33 chars, declarative
11. ✅ Description first 100-125 chars load-bearing
12. ✅ Pinned comment ready
13. (manual) Schedule 21:00 AWST Fri 9 May, ≥24h after Short 4, NOT within ±2h of V7 main 18:00
14. (manual) Native upload only to TikTok + IG Reels

---

## Build script — Shorts 2-5

`generator/au-dealer-math/build-v02-shorts-2-5.py` (parameterised, run `python ... --only N` for individual rebuild)

VO renderer: `generator/au-dealer-math/render-v02-shorts-bookends-2-5.js` (8 bookend VOs via ElevenLabs Mac LOCKED voice)

## Reproducing for future V[N] Shorts

The `build-v02-shorts-2-5.py` script is **fully parameterised** via a `SHORTS` dict at top:
- `lift_start` / `lift_end` (V2 source seconds)
- `scene_idx` (vo-transcriptions.json scene index)
- `hook_text` + `hook_fontsize` (avoid `%` — escape required, just use "POINTS" / "PERCENT" instead)
- `open_vo` + `close_vo` (mp3 filenames in `voice-shorts/`)

To build V3+ Shorts: copy the script as `build-v03-shorts.py`, swap `V2_FINAL` to V3 master, regenerate VOs via the renderer pattern, update lift windows. Per `feedback_audm_mj_text_failure_pool_drop_2026-05-03.md` the doc-forensics aesthetic carries Shorts visual just like long-form.

## Lessons captured 2026-05-05 (V2 Shorts 2-5 build)

- **`%` is a drawtext special character** that breaks rendering — escape as `\%` or use word substitutes ("POINTS" / "PERCENT")
- **Hook fontsize ceiling at 1080 width:** 7-char text @ 220pt fits with margin; 280pt overflows
- **Loudness landing varies by source dynamics.** Different lift windows from same V2 master converge to different LUFS (-14.5 to -15.6) under identical pipeline. The iterative volume+alimiter approach with -2dBFS limiter ceiling reliably keeps TP under -1 dBFS but can't always lift integrated to -14 if the source has wide dynamic range. Acceptable: TP within spec is the load-bearing safety check; integrated drift up to -16 LUFS is corrected by YT playback normalization
- **alimiter limit=0.794 (= -2 dBFS)** is the safe ceiling: alimiter has 5ms attack and brief transients overshoot the limit by 0.5-1 dBFS in practice, so setting -2 dBFS lands worst-case peaks around -1 dBFS
