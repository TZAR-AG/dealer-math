# Submagic — AUDM canonical prompt reference

> **🟠 ACTION ITEM: Add Magic Clips add-on (+$12/mo).**
> Bare Starter has a 2-min export cap that kills the AUDM Shorts workflow on a 12-min long-form. Magic Clips ($12/mo) unlocks long-video upload + auto-cut. Total ~$32/mo (vs current $27.59 Starter). **One-line decision: yes, add it.**

**Engine:** Custom ASR pipeline (almost certainly Whisper-derived + proprietary tuning). 96-99% accuracy on natural speech.
**Tier (currently):** Starter $27.59 AUD/mo
**Tier (recommended):** Starter + Magic Clips add-on = ~$32 AUD/mo
**Use AUDM for:** Generate 3 Shorts cutdowns from V1 long-form + apply kinetic captions to those Shorts. NOT for long-form captions (YouTube auto-CC is enough).

---

## What Submagic actually does (the engine)

**Released March 2025 (Submagic 2.0):** 60% upload-speed improvement, smarter speaker/tone detection, music-sync, auto-emphasis.

**Strong on:** tech jargon (Pomodoro, asynchronous), business terminology, clean studio audio.
**Weaker on:** heavy AU accents, dialects, slang. **Plan to manually correct AU vernacular** ("ute", "rego", "drive-away", "Macca", "spruiker") via the in-editor transcript + add to **Custom Dictionary** so they auto-correct on every future upload.

**The Custom Dictionary is spelling-only, applied post-transcription.** No phonetic / pronunciation control (that's ElevenLabs' job).

---

## Caption style for AUDM (locked recipe)

**Style choice: Hormozi 4** (or Hormozi 3) — re-skinned with AUDM palette.

The only Submagic preset that gives the dollar-figure punch we need: bold uppercase, one-or-two-words-at-a-time, pop-in animation, yellow active-word highlight with shadow + stroke. We re-skin to brand:

| Element | AUDM value |
|---|---|
| Primary color (text) | cream `#FAF7F2` |
| Highlight 1 (dollar figures + reveal phrases) | outback orange `#C8612C` |
| Highlight 2 (proper nouns: Macca, ATO, Mercedes, etc) | white `#FFFFFF` |
| Highlight 3 | unused (don't dilute the orange) |
| Stroke | charcoal `#2B2B2B` 6px |
| Font | DM Sans Bold uppercase (Submagic library) — fallback Inter Black |

**Submagic supports up to 3 highlight colours simultaneously** — this matches our 3-color palette exactly.

**Emphasis Mode: ON** + manually re-tag every dollar figure and key reveal in orange. Submagic's auto-emphasis catches ~70% of money words; we need 100%, so manual sweep is mandatory pre-export.

---

## Magic Clips settings for 12-min AUDM long-form

(Requires the +$12/mo Magic Clips add-on — see action item above.)

| Setting | Value | Why |
|---|---|---|
| Number of clips | 5-10 (ask for 10, ship best 3) | Get options |
| Target Shorts length | 45-60s | Sweet spot for retention + dwell time on YT Shorts/Reels/TikTok |
| Aspect | 9:16 | Vertical for Shorts/Reels/TikTok |
| Auto-features ON | captions, silence-cut, filler-word removal, zooms | Time-saver |
| AI B-roll | **OFF for V1** | Failure mode: generic "businessman shaking hands" / "city skyline" clips obliterate AUDM doc-cinema look |

**How Magic Clips picks moments:** transcript hook density + emotion/tone shifts + pause detection. **To bias it toward our reveals:** end every video section with a self-contained payoff line ("That's where the $4,200 holdback sits") — Magic Clips reliably picks complete-thought sections that resolve a number.

---

## AUDM Custom Dictionary (one-time setup)

Add these to Submagic's Custom Dictionary on V1; persists across all future projects:

```
Macca
ATO
holdback
GFV
ute
rego
drive-away
spruiker
HiLux
D-Max
MU-X
BT-50
Mercedes-Benz
Hyundai
Volkswagen
Peugeot
Renault
Porsche
volume rebate
Guaranteed Future Value
manufacturer kickback
recon allocation
changeover
finance manager
aftercare manager
```

Note: this dictionary is for **transcript spelling**, not pronunciation. ElevenLabs handles pronunciation via its own pronunciation_dictionary (see `elevenlabs-paul.md`).

---

## The 3-Shorts AUDM SOP (V1 onwards)

```
1. Render long-form in CapCut (12 min, Macca VO, brand grade)
2. Upload to Submagic via "Magic Clips" upload
   (paste YouTube URL after long-form is published unlisted, or upload MP4)
3. Generate 10 candidate Shorts, length 45-60s
4. Manually select 3 with highest dollar-figure density + self-contained reveal
5. Apply preset: Hormozi 4, re-skinned with AUDM palette
6. Manual sweep: every $X,XXX and reveal phrase → orange highlight
7. Add AUDM dictionary terms (one-time on V1; persists)
8. Export each Short at 1080p 30fps MP4 (Starter cap)
9. Export the SRT for the long-form (separate from Shorts)
   → upload to YouTube alongside the long-form for accessibility + SEO
10. Distribute:
    - Long-form → YouTube (with separate SRT upload)
    - 3 Shorts → YT Shorts + IG Reels + TikTok via Blotato
```

**Time budget per episode after V1:** ~25 min in Submagic. First episode (V1): ~60 min including dictionary setup + palette save.

---

## Caption file export

| Format | Submagic supports? | Use for |
|---|---|---|
| SRT | ✅ | YouTube long-form accessibility upload |
| VTT | ✅ | Web playback alternative |
| TXT | ✅ | Transcript reference |
| ASS | ❌ | (CapCut native if needed) |

**Always upload the SRT separately to YouTube** alongside the burned-in render. Burned-in captions are visual-only and don't count for YouTube's caption layer / search index. SRT counts for both.

IG and TikTok ignore SRT — those rely on the burned-in captions only.

---

## Tier comparison (the math for downgrade/upgrade)

| Plan | Price | Export cap | Magic Clips | Long-video upload | Verdict |
|---|---|---|---|---|---|
| Free | $0 | watermarked | no | no | Skip |
| **Starter $19/mo + Magic Clips $12/mo = $31/mo** | $31/mo | 2 min/clip | yes | yes | **AUDM target** |
| Pro | $39/mo | 5 min/clip | yes | yes | Upgrade if shipping daily Shorts to multiple channels |
| Business | $69/mo | 4K + 60fps | yes | yes | Irrelevant — YT Shorts caps render benefit at 1080p anyway |

**Recommendation:** Add Magic Clips next billing cycle ($12/mo). Total ~$32/mo. Hold there for first 90 days. Re-evaluate at V12.

---

## Failure modes + mitigations

| Symptom | Cause | Fix |
|---|---|---|
| AU vernacular transcribed wrong (Macca → "Marker", ute → "you") | ASR weak on AU accent + slang | Add to Custom Dictionary; persists across projects |
| Magic Clips picks clips that don't resolve a number | Section endings are weak | Restructure script so every ~90s section ends with a self-contained payoff line that names a dollar figure |
| Caption emphasis misses 30% of dollar figures | Auto-emphasis is ~70% accurate | Manual sweep pre-export — every $X,XXX gets orange tag |
| AI B-roll injects generic stock | AUDM aesthetic doesn't match Submagic's stock library bias | Keep AI B-roll OFF for V1; long-form B-roll done in CapCut layer separately |
| Hormozi 4 preset looks too "bro hustle" | Default colors are gym-bro yellow/black | Re-skin per AUDM palette table above |

---

## Validated patterns log

- 2026-04-29: not yet used for AUDM (V1 still in production). Magic Clips add-on pending Adrian approval.
- *(append validated patterns after each render batch)*

---

## Sources

- [Submagic Pricing](https://www.submagic.co/pricing)
- [Magic Clips feature](https://www.submagic.co/features/magic-clips)
- [Submagic Hormozi caption guide](https://www.submagic.co/blog/how-to-make-alex-hormozi-captions)
- [How to apply highlighting colours](https://care.submagic.co/en/article/how-to-apply-highlighting-colors-to-your-words-16ttppq/)
- [How to do emphasis captions](https://care.submagic.co/en/article/how-to-do-emphasis-captions-1p5w99b/)
- [How to export only subtitles](https://care.submagic.co/en/article/how-to-export-only-subtitles-in-submagic-yb02cn/)
- [Subtitles download (SRT/VTT/TXT)](https://www.submagic.co/use-cases/subtitles-download)
- [Submagic Pricing 2026 breakdown — fluxnote](https://fluxnote.io/guides/submagic-pricing-guide-2026)
- [Submagic vs Opus Clip — wavel.ai](https://wavel.ai/compare/submagic-vs-opusclip)
- [Submagic Review 2025 — businessdive](https://thebusinessdive.com/submagic-review)
- [Submagic Review — Unite.AI](https://www.unite.ai/submagic-review/)
- [Submagic 2.0 features — max-productive](https://max-productive.ai/ai-tools/submagic/)
