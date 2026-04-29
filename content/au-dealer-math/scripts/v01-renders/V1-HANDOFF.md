# V1 Handoff — 2026-04-29

> **STATUS: SHIP DEFERRED 2026-04-29 evening.** Adrian's call: "not shipping a half product. Find the best way forward."
>
> **➡ THE RESUMPTION DOC IS [`v01-production-master.md`](../v01-production-master.md)** — the engineered prompt sheet for the full SaaS stack (Nano Banana Pro · Midjourney · Kling 3.0 · InVideo AI Max · Storyblocks). Read THAT to plan V1 production. This handoff doc is now archive-only.
>
> **What changed in the evening reset:**
> - VO speed locked at **0.90** (was 0.85 — felt dragged; 0.95 = auctioneer; 0.90 = sweet spot at 10:58 runtime)
> - All 7 VO scenes re-rendered at 0.90 — files in `voice/`, old 0.85 backups in `voice/_backup-204wpm-0.85/`
> - Production strategy expanded from "Kling-heavy" to "full-stack layered" (Kling = ~10% of motion only)
> - 7-layer architecture documented in production-master.md
> - 12 NEW Nano Banana stills + 6 NEW Midjourney stills + 12 Kling motion clips planned with engineered prompts
> - Mascot integration deferred to V2+ (V1 stays clean-faceless, prompts preserve negative space)
>
> **CapCut project URL** (auto-saved by CapCut, resume from same state):
> `https://www.capcut.com/editor/850B1E75-2E07-41C0-8EBD-650CFFB6EBEC?scenario=custom`
>
> **Why deferred:** real visual depth gap across 12 min runtime — single stills holding for 2-3 min each is too thin for AUDM positioning. Need additional Kling clips OR Storyblocks B-roll, dollar-figure text overlays, and music bed before this is ship-quality.

---

State of the V1 build at deferral. Read top to bottom.

---

## What changed while you were away

1. **Script expanded from 1,614 → 2,480 words** with real dealer-knowledge content in scenes 3, 4, 5, 6 (no padding). File: `content/au-dealer-math/scripts/v01-payment-not-price-pivot.md`. Diff shows 4 inserted blocks under the existing scene headers.
2. **All 7 VO scenes re-rendered** via ElevenLabs API at speed **0.85** (down from locked 0.95) with locked Paul settings (stability 0.40, similarity 0.75, style 0.25, speaker boost on). New durations measured via ffmpeg-static.
3. **Total runtime: 12:10** — sits in YouTube's max-ROI window (≥8:00 unlocks 1 mid-roll, ≥10:00 unlocks 2 mid-rolls). You wanted "stretch to maximize" — done.
4. **Old VOs backed up** to `content/au-dealer-math/scripts/v01-renders/voice/_backup-326wpm/` in case you want to A/B compare. Don't need them in CapCut.
5. **Locked Macca voice memory updated** — speed 0.85 is now the canonical setting for V2-V100 renders.
6. **Re-render automation built** — `generator/au-dealer-math/regenerate-vo.js`. Reusable for V2 onwards (currently hardcoded to V1 path; parameterize when V2 lands).
7. **CapCut prepped** — 16:9 ratio set, all 9 new assets uploaded to Media panel (7 new VOs + 2 renamed clean Kling clips). Old assets still there but distinguishable.

---

## Per-scene VO durations (the new spine)

| Scene | File | New duration | Cumulative end |
|---|---|---|---|
| 1 Hook | `vo-scene-1-hook.mp3` | 0:24 | 0:24 |
| 2 Authority | `vo-scene-2-authority.mp3` | 0:42 | 1:06 |
| 3 Question | `vo-scene-3-question.mp3` | 1:56 | 3:02 |
| 4 Loan trick | `vo-scene-4-loan-trick.mp3` | 2:44 | 5:46 |
| 5 Why dealer | `vo-scene-5-why-dealer.mp3` | 3:06 | 8:52 |
| 6 Fix | `vo-scene-6-fix.mp3` | 2:45 | 11:37 |
| 7 Sign-off | `vo-scene-7-signoff.mp3` | 0:33 | **12:10** |

---

## CapCut state when you return

- URL open: `https://www.capcut.com/editor?scenario=custom`
- 16:9 ratio set ✅
- Empty timeline (fresh project)
- Media panel has the **new** 7 VOs (with the longer durations above) at the **top of the panel** — newer uploads go to top.
- Old 326wpm VOs are still in the panel below the new ones with shorter durations (0:19, 0:33, etc). **Identify by duration** — drag the newer/longer one for each scene.
- Both Kling clips have **TWO entries each** — old default-name version (`kling_20260429_Image_to_Video_*`) and new clean-name version (`kling-clip-1-hook.mp4` + `kling-clip-3-cars-parallax.mp4`). Use the clean-name versions.
- Stills (1-5 + still-kling-clip-1-input) are unchanged from earlier session.

---

## Build plan — drag in this order

### Step 1 — audio track (lower row)

Drag in scene order, end-to-end. Use the **longer** versions:

1. `vo-scene-1-hook.mp3` (0:24)
2. `vo-scene-2-authority.mp3` (0:42)
3. `vo-scene-3-question.mp3` (1:56)
4. `vo-scene-4-loan-trick.mp3` (2:44)
5. `vo-scene-5-why-dealer.mp3` (3:06)
6. `vo-scene-6-fix.mp3` (2:45)
7. `vo-scene-7-signoff.mp3` (0:33)

Total at end of step 1: timeline shows **12:10**.

### Step 2 — video track (upper row)

| # | Drop at | Stretch right edge to | File |
|---|---|---|---|
| 1 | 0:00 | 0:05 (auto, no stretch) | `kling-clip-1-hook.mp4` *(clean version)* |
| 2 | 0:05 | 0:24 | `still-kling-clip-1-input.png` |
| 3 | 0:24 | 1:06 | `still-1-dealership-floor.png` |
| 4 | 1:06 | 3:02 | `still-2-customer-confusion.png` |
| 5 | 3:02 | 3:07 (auto) | `kling-clip-3-cars-parallax.mp4` *(clean version)* |
| 6 | 3:07 | 5:46 | `still-3-cars-comparison.png` |
| 7 | 5:46 | 8:52 | `still-4-three-rooms.png` |
| 8 | 8:52 | 12:10 | `still-5-confident-customer.png` |

**Polish hint:** scenes 4-7 each hold a single still for 1:56–3:06 — that's a long time on one image. Click each still on the timeline → right panel → **Animation → Slow zoom in** (Ken Burns). Adds subtle motion so the eye doesn't go dead.

### Step 3 — captions

Left nav → **Captions** → **Auto Captions** → English. Style: bold sans-serif, white with black stroke, position bottom-third. CapCut Online's auto-caption is decent but proofread the dollar figures — those are make-or-break for credibility.

### Step 4 — export

Top right → Export. Resolution **1080p**, frame rate **30**, format **MP4**, quality **High**. Save to:
`C:\dev\Claude\content\au-dealer-math\scripts\v01-renders\final\v1-payment-not-price-pivot.mp4`

(Create the `final/` folder if it doesn't exist.)

---

## What I couldn't do (handoff items)

- **Timeline drag-and-drop is yours.** CapCut Online's React-DnD rejects synthetic events from dev tools. The drags above are manual. ~10-15 min total.
- **Auto-captions cleanup is yours.** I can drive the "generate" click via dev tools but ASS-style proofreading needs your eyeballs.
- **Final export click is yours.** I'll watch via dev tools if you want me to verify the render goes through.

---

## What you should NOT do

- Don't drag the OLD 326wpm VOs by mistake (the shorter-duration ones lower in the panel). The video falls apart if you mix old and new audio.
- Don't drag the watermarked Kling clips with the long default names — use the clean `kling-clip-1-hook.mp4` and `kling-clip-3-cars-parallax.mp4`.
- Don't change the 16:9 ratio (already set for YouTube long-form).
- Don't try to "speed up" the VO in CapCut — the 12:10 is intentional for 2 mid-roll ad eligibility.

---

## Script content recap (so you know what's in the new VO)

- **Scene 3** added: training origin of the budget question (the *Road to a Sale* doc), why it's locked at step 3 of every salesperson's training.
- **Scene 4** added: Guaranteed Future Value plans at the luxury end — manufacturer-backed buyback, why it's a recurring-revenue trap, why luxury car finance "feels like it never ends."
- **Scene 5** added: there are TWO offices behind the salesperson (aftercare + finance) — paint protection 75% margin, holdback layer ($1k+ on mass market, more on luxury), volume rebates ($30k on $350k wholesale buy at the Chinese-brand store you worked at last). Three commissioned salespeople in sequence.
- **Scene 6** added: bank-beat move (bring real pre-approval, demand total-cost comparison) + manufacturer fixed-rate campaign timing (1.99%, 4.9% windows when dealer flips from extracting margin to closing volume).

All sourced from `dealer-knowledge-bank.md` Q1-Q8. All applied with brand-naming policy (categories only, Mercedes named only for agency-model topic — not used here).

---

## When V1 ships

- Update `content/au-dealer-math/content-calendar.md` to mark V1 as published.
- Drop the YouTube URL into `project_audm_content_calendar_locked_2026-04-29` memory.
- Update progress doc.
- Plan V2 render via the same `regenerate-vo.js` (param-update needed for V2 path).

---

## Punch list before resuming (added 2026-04-29 evening, ship deferred)

### Decisions locked during the build

1. **Subtitles for V1 long-form: NOT BURNT** in. YouTube auto-CC is enough for accessibility. Submagic earns its keep on the **Shorts cutdowns** generated from V1 (per AUDM design spec step 14), not on the long-form itself. Don't spend Submagic credits on V1 long-form.
2. **Dollar-figure emphasis IS required** per script production notes line 159: *"every dollar figure must be burnt into the frame, not just spoken."* These are emphasis text overlays in CapCut, not transcription.
3. **Macca voice speed locked at 0.85** going forward (was 0.95). Memory updated.

### What's left to do for V1 ship

#### 1. Visual depth — eliminate long-static-still feel (BIGGEST GAP)
Current state: scenes 4-7 hold a single still for 2-3 min each. AUDM viewers expect visual change every 10-15 sec.

Options (pick ONE):
- **A. Generate 8-12 more Kling motion clips** from existing Nano Banana stills. Cost ~$2-3 in Kling Starter credits. Adds 5-10 sec of motion punctuation per scene. ~2 hr work. *(Recommended)*
- **B. Storyblocks B-roll** ($100/mo subscription you're paying for). Search "AU dealership floor", "loan paperwork", "money close-up", "AU street scenes". Drop in 5-10 sec cutaways between long stills. ~1.5 hr work.
- **C. Combination of A + B** — Kling for branded scene-specific motion + Storyblocks for generic cutaways.

Avoid Ken Burns alone — it's the lazy fix that audiences see as filler.

#### 2. Dollar-figure text overlays (script-mandated)
Burn these into the frame at the moments the VO says them. Use big bold yellow `#FFD700` per design system. Approximate timestamps (verify against final VO):

| Time | Overlay text | Source |
|---|---|---|
| ~0:02 | `$300/WEEK` | Script line 21 (cold-open hero figure) |
| ~3:35 | `$300/WK × 4 YRS = $62,400` | Scene 4 left-side comparison |
| ~3:42 | `$300/WK × 7 YRS = $109,200` | Scene 4 right-side comparison |
| ~3:48 | `$46,800 MORE` | Scene 4 difference highlight |
| ~6:30 | `$2,000 RETAIL · $500 COST · 75% MARGIN` | Scene 5 paint protection |
| ~7:15 | `$30K BACK ON $350K WHOLESALE` | Scene 5 volume rebate |
| ~10:30 | `1.99% / 4.9% / RATE CAMPAIGN` | Scene 6 manufacturer rate window |

(Re-time these by scrubbing the actual VO when you resume.)

#### 3. Music bed (script production notes line 157)
*"Charcoal-baseline music bed. Storyblocks 'calm-confrontation' instrumental tag. Fade to silence at sign-off. Volume profile: -23 LUFS for VO clarity."*

- Source via Storyblocks (subscription active)
- Loop or stitch to cover 12:10 minus the final 0:30 (fade to silence at sign-off per spec)
- Mix at -23 LUFS so VO sits clearly above

#### 4. Final QC pass
- Watch full V1 once before export. Listen for VO/music balance, watch for visual lulls, check dollar-figure overlay accuracy.
- Verify no Kling watermark crept back in.
- Verify all 16 visual cues match VO scene boundaries within 0.5 sec.

#### 5. Export + post-production
- Export 1080p MP4, 30fps, High quality → `v01-renders/final/v1-payment-not-price-pivot.mp4`
- YouTube upload → auto-CC enables automatically (no manual caption work)
- After upload, generate 3 Shorts cutdowns via Submagic (per AUDM pipeline step 14 — this is where Submagic earns its $27.59/mo)
- Cross-post Shorts to TikTok + IG Reels via Blotato

### Estimated time to V1 ship from this point

- Kling clip generation (option A): 2 hrs
- Dollar-figure overlays: 30 min
- Music bed sourcing + mix: 30 min
- QC + export: 30 min
- Submagic Shorts cutdowns: 30 min
- **Total: ~4 hrs of focused work**

Probably best as a single dedicated session vs piecemeal, so the QC continuity holds.

### Resume from where Adrian left off

When you come back to this:
1. Open the CapCut URL above (project state preserved)
2. Open this V1-HANDOFF.md
3. Start at Punch list item #1 (visual depth)
4. Skip everything in this doc above the punch list — that's already done
