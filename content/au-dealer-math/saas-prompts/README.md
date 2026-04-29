# AUDM SaaS Prompt Engineering — Canonical Reference

> **Source of truth for every prompt-driven tool in the AU Dealer Math production stack.** Built from 6 parallel deep-research agents 2026-04-29. Update after every video ships with what worked / what failed.

**The principle:** every paid SaaS only earns its keep if we know its engine, prompt syntax, parameter ranges, failure modes, and the AUDM-specific brand-locked patterns. This folder is that knowledge — the "world-class advanced user" reference for AUDM.

---

## Files in this folder

| Tool | File | Tier | Purpose |
|---|---|---|---|
| Nano Banana Pro | [`nano-banana-pro.md`](nano-banana-pro.md) | $? on Artlist | AU dealership scenes, paper/document close-ups, brand-locked stills (16:9) |
| Midjourney | [`midjourney.md`](midjourney.md) | Standard $46/mo | Cinematic photo-real hero shots, products, V2+ Macca mascot via `--oref` |
| Kling 3.0 | [`kling.md`](kling.md) | Starter $11.17/mo | Image-to-video motion punctuation (5-8s clips) |
| InVideo AI | [`invideo-ai.md`](invideo-ai.md) | **REVIEW Max → Plus** | Final assembler / B-roll matching (license blocks clip extraction) |
| Submagic | [`submagic.md`](submagic.md) | **Add Magic Clips +$12/mo** | Shorts auto-cut + kinetic captions + SRT export |
| ElevenLabs Paul | [`elevenlabs-paul.md`](elevenlabs-paul.md) | Creator $99/mo (shared SS) | VO render — locked Paul voice, API-driven |

---

## Critical action items from research (2026-04-29)

### 🔴 INVIDEO AI MAX — DOWNGRADE TO PLUS
The clip-extraction-to-CapCut workflow is **license-blocked**. Max-only feature you actually need is API access for n8n, which isn't built yet. Plus tier covers AUDM scale. **Saves ~$119 AUD/mo.** Refund window: act before next billing cycle. See [`invideo-ai.md`](invideo-ai.md) § Honest assessment.

### 🟠 SUBMAGIC — ADD MAGIC CLIPS ADD-ON (+$12/mo)
Bare Starter has a 2-min export cap that kills the Shorts workflow. Magic Clips ($12/mo) unlocks the auto-cut feature for our 12-min long-form. Total ~$32/mo. See [`submagic.md`](submagic.md) § Tier honesty.

### 🟢 ELEVENLABS API — CRITICAL PIPELINE UPGRADE
We're missing the highest-leverage feature: `previous_text` / `next_text` / `previous_request_ids` for scene-to-scene voice continuity. Plus `seed` for reproducibility, `apply_text_normalization: "on"` for guaranteed dollar/percent handling, `mp3_44100_192` for free quality bump. **One ~30 min change to `regenerate-vo.js` = highest-leverage VO quality lift.** See [`elevenlabs-paul.md`](elevenlabs-paul.md) § (a) Canonical API request body.

### 🟢 AUDM PRONUNCIATION DICTIONARY
Upload `.pls` XML to ElevenLabs once with: Macca→Mack-uh, ute→yoot, rego→redge-oh, plus all car brand respellings (Mercedes→Mer-SAY-deez, Hyundai→HUN-day, etc). Attach locator to every render. One-time setup; persists across V1-V100. See [`elevenlabs-paul.md`](elevenlabs-paul.md) § (c).

---

## Brand-lock that carries across ALL prompt-driven tools

These phrases appear in every NB / Midjourney / Kling / InVideo / Submagic prompt for AUDM:

- **Palette (60/30/10 weighting):** charcoal `#2B2B2B` (60%) · cream `#FAF7F2` (30%) · outback orange `#C8612C` (10%)
- **Light:** `low warm Australian afternoon sun raking from upper-left, oblique 30-degree shadow angle, ~16:00 light angle`
- **Era + film stock:** `Kodak Portra 400, 35mm` (default), `CineStill 800T` (dusk/showroom interiors)
- **Photographer/style anchors:** Alec Soth · Stephen Shore · Trent Parke (AU-specific) · Wim Wenders · Joel Sternfeld
- **Faceless lock (triple redundant):** `unpopulated scene, no figures, no people, no human silhouettes, no reflections of people in glass or chrome surfaces`
- **Text suppression:** `no text, no typography, no readable words, no logos, no brand names, no captions burned in`
- **Geography:** `Australian context, RHD vehicles if visible, AU number plates, suburban dealership / coastal city / outback highway acceptable; reject US dealership exteriors, LHD interiors, European number plates`

**Phrases BANNED across all tools** (pull toward generic stock / luxury ad):
- `professional`, `corporate`, `business`, `high quality`, `4K masterpiece`
- `happy`, `smiling`, `team`, `diverse group`, `confident customer`
- `beautiful`, `stunning`, `amazing`, `epic`, `cinematic` (too generic)
- `cozy`, `warm and inviting`, `welcoming`
- `studio lighting`, `white background`, `commercial photography`
- `octane render`, `unreal engine`, `hyperdetailed`, `8K`
- `Wes Anderson`, `Christopher Nolan` (overused, pull to mean cinematic)
- `Roger Deakins` (lighting only — fine; full style anchor — overused)
- `shot on iPhone` (flattens look — use Fujifilm or Kodak instead)
- `luxury car ad`, `glamour shot`, `promotional`

---

## Per-tool one-line summary

**Nano Banana Pro:** subject-first prompts. Hex codes work. 60/30/10 palette weighting. Negation = positive framing ("empty street" not "no cars"). 16:9 set in Artlist UI.

**Midjourney v7:** `--style raw --v 7 --ar 16:9 --s 80 --chaos 0 --sref [palette-swatch-url] --sw 200 --no [block-list]`. Use `--oref` not `--cref` (deprecated). Build a permanent palette swatch URL once, reuse forever.

**Kling 3.0:** I2V always. 20-50 word prompt, 5-part order: Camera → Scene → Action → Vibe → Time. ONE camera move per clip. "Slow / subtle / micro" mandatory speed adjective. Continuity guardrail: "preserve silhouette, maintain label text, keep proportions". Tick "No watermark" on every download.

**InVideo AI:** scene-by-scene literal sentence prompts. Cannot extract individual clips (license). Use as final assembler OR shotlist tool only. Downgrade Max → Plus until n8n.

**Submagic:** Hormozi 4 style + brand palette re-skin. Magic Clips add-on required for auto-cuts. SRT separately + always upload to YouTube alongside the burned-in render.

**ElevenLabs Paul:** Multilingual v2 / Stability 0.40 / Similarity 0.75 / Style 0.25 / Speaker Boost ON / Speed 0.90. Add `previous_text`/`next_text`/`previous_request_ids` for scene continuity. Pronunciation dict via alias substitution (not phoneme — v2 doesn't support it).

---

## How to use this folder

**When drafting any prompt for any tool:**
1. Open the relevant tool file in this folder
2. Apply the **prompt skeleton** at the top
3. Pull from the **AUDM example prompts** at the bottom as starting templates
4. Apply the brand-lock phrases from this README
5. Run + iterate

**When a render fails or behaves unexpectedly:**
1. Check the **failure modes** section of the tool's file
2. Apply the documented mitigation
3. If new failure mode → append to the file with what fixed it

**When researching adds a new pattern:**
1. Update the relevant tool file with the new pattern + source link
2. Test the pattern on next render
3. Promote to "validated" only after 2+ successful renders

---

## Update cadence

- **Per video:** add a one-line learning to each tool file's "validated patterns" section if a render landed first try OR a failure mode was caught
- **Monthly:** review tool docs/changelogs for new features; update files accordingly
- **Per major model release:** full re-research (e.g. Kling 4.0, Midjourney v8 stable, Nano Banana Pro 2)

---

## Reference

- **Created:** 2026-04-29 evening, after V1 ship deferred + Adrian directive for "world-class advanced user" research
- **Research method:** 6 parallel general-purpose research agents pulling current docs + creator forums + community threads (late 2025 / early 2026 sources)
- **Memory pointer:** `project_audm_saas_prompts_canon_2026-04-29` indexes this folder
- **Replaces / extends:** `reference_nano_banana_prompting.md` (SS-specific — kept for SS work, AUDM uses different style anchors)
- **Lives in repo at:** `content/au-dealer-math/saas-prompts/`

This folder IS our standard.
