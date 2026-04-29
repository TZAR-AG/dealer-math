# AU Dealer Math — Prompt Engineering Reference

**Single source of truth** for every prompt sent to a credit-spending tool on this channel. Every future prompt MUST validate against this doc before submission.

**Standard:** First-shot precision. Re-rolls are a research failure, not a tool issue.

**Cost discipline:** Every credit burned on a sub-par prompt = wasted spend. Validate first, generate once.

---

## How this doc was built

Two inputs, fused:

1. **Empirical lessons from our 2026-04-29 V1 production run.** We generated 40+ Midjourney variants and 1 Kling clip during V1 prep. The wins, failures, and patterns from that actual output drive the rules below — these aren't theoretical, they're "what we learned watching what we generated."
2. **Research synthesis from 5 background agents** covering Midjourney v7, Kling 3.0, InVideo AI, Submagic, ElevenLabs PVC. Pulled from current 2026 documentation, faceless-channel community case studies, and validated working templates from successful 2026 channels.

---

## TOOL 1 — Midjourney v7

### Empirical lessons from our V1 stills

**What worked (replicate these patterns):**

| Still | Win condition |
|---|---|
| Still 5 _0 (confident customer) | Silhouette as the SUBJECT word + concrete body direction ("hands relaxed at sides, upright posture") + single mood cue ("soft natural lighting"). All 4 variants in this batch were strong. Tight, concrete, low descriptor count. |
| Still 4 _2 re-roll (glass offices) | Front-elevation isometric framing was concrete + per-office description was specific + architectural reference clear. Premium photogenic output, palette-locked. |
| Still 1 _2 original (outdoor lot at dusk) | Despite being off-brief (we wanted indoor showroom), this was the cleanest mood + palette match in the original batch. Less stacking = stronger output. |

**What failed (avoid these patterns):**

| Failure | Root cause | Fix |
|---|---|---|
| Still 1 originals produced BMW-recognizable cars | "rows of new cars" with no brand suppression → v7 backfilled with the most recognizable car silhouette in training data (BMW kidney grille) | Add specific brand names to `--no`: BMW, Lamborghini, Porsche, Mini, kidney grille, hood ornament |
| Still 1 re-roll produced photo-realistic 3D atriums | 110-word prompt + architectural words ("polished concrete," "double-height ceiling," "laser-cut aluminium") triggered v7's architectural-rendering photo prior. Style cues drowned by spec cues | Cap at 30-40 words. Architectural specs go in `--sref` reference, not prose. |
| Still 2 originals produced faces despite "silhouettes only" | "customer" + "salesperson" are person-words → v7 backfills faces. Negation alone doesn't suppress concepts that live in latent space | Use "back-of-head," "figure cropped at shoulders," "shoulder-up shadow" instead of person words. Add `--no face, facial features, eyes, mouth, portrait, head` |
| Still 3 produced recognizable Porsche / Lambo / Audi | "luxury SUV" maps to known brands. "compact" maps to MINI Cooper. v7 fills detail from training data when given archetype words | Use silhouette categories: "boxy mid-size SUV silhouette," "generic three-box sedan profile." Add specific brand names to `--no` |
| All early Still 1 batches lost the charcoal/cream palette | Palette was buried at position 7-8 of prompt. v7 weights by position; descriptors fought | Palette is the THIRD descriptor block, max. Limited to 4 named colours |

### Research findings (Midjourney v7, 2026)

**v7 default behavior:**
- v7 default = beautified photorealism. **`--style raw` is non-optional** for flat illustration.
- v7 weights words by position. Subject in **first 6-8 words.** Total prompt **30-40 words + parameters max.**
- `::` multi-prompt weights are deprecated in v7. Use `--sref`, `--cref`, `--no`.

**Critical parameters:**

| Parameter | Setting | Reason |
|---|---|---|
| `--style raw` | Always | Disables auto-beautification |
| `--stylize` | 50-150 | Editorial flat illustration. Above 200 reintroduces photo bias |
| `--sref <code>` | Channel-locked code | Single most powerful aesthetic-consistency lever |
| `--sv` | 4 | Recommended professional default |
| `--ar 16:9` | YouTube content | Match YT frame natively |
| `--v 7` | Always | Latest model |
| `--no` | Single flag, comma list | Multiple `--no` flags trigger "sum of weights must be positive" error |

**Negative prompt structure (single `--no`, comma-separated):**

```
--no logo, badge, brand, grille, text, gradient, shadow, photorealistic, 3D render, depth of field, face, facial features, eyes, mouth, portrait, BMW, Lamborghini, Porsche, Mini, kidney grille, hood ornament
```

Naming the specific brands you DON'T want is a known v7 trick — it pushes them out of latent space. Combine with positive shape direction.

### Locked v7 prompt template

```
[subject in 6-8 words], flat editorial illustration, [palette ≤4 colours], [composition cue]
--ar 16:9 --style raw --stylize 100 --sref <channel-code> --sv 4
--no logo, badge, brand, grille, text, face, facial features, gradient, shadow, photorealistic, 3D render, BMW, Lamborghini, Porsche, Mini
--v 7
```

### Channel-aesthetic lock workflow (do this once, reuse forever)

1. Run ONE Midjourney generation with 3 reference image URLs (Polymatter, Wendover, Cleo Abram frame examples) as `--sref <URL1> <URL2> <URL3>`
2. Pick the best output, note Midjourney's returned `--sref <code>`
3. **Every future prompt** uses `--sref <that-code> --sv 4`
4. Guarantees palette + lineweight + texture consistency across V1 → V100

This is the channel-consistency lever we didn't use on V1. Lock it before V2.

### Pre-submit checklist (Midjourney)

Before clicking Generate, validate:

- [ ] Subject is in first 6-8 words?
- [ ] Total prompt ≤40 words + parameters?
- [ ] No banned words ("photorealistic," "cinematic," "8K," "ultra-detailed")?
- [ ] No archetype words ("luxury SUV," "sports car") that map to brands?
- [ ] Used silhouette categories instead ("boxy mid-size SUV silhouette")?
- [ ] Palette named (≤4 colours)?
- [ ] `--style raw` present?
- [ ] `--stylize 50-150` set?
- [ ] `--sref <channel-code>` present?
- [ ] Single `--no` with comma list (not multiple `--no` flags)?
- [ ] Specific brand names in `--no`?
- [ ] Face suppression in `--no` if subject involves figures?

---

## TOOL 2 — Kling 3.0 (and 2.5)

### Empirical lesson from our V1 Clip 1

We generated one 5-second clip on Kling 3.0 at 40 credits. Output had multiple issues:

1. **Watermark** — Starter tier ships with bottom-right watermark
2. **Subject motion suspect** — without subject lock, scene elements may have drifted
3. **Cost** — 40 credits is 4× what 2.5 Pro Standard would have cost (~10 credits)

### Research findings (Kling 3.0, 2026)

**Critical structural rule:** Camera verb goes LAST in prompt, not first. Kling builds the scene first, then applies the camera move.

**Optimal prompt structure:**

```
Scene → Subject (with stillness lock) → Environment/Lighting → Camera verb (at end)
```

**Verb taxonomy (predictability ranking):**

| Verb | Reliability |
|---|---|
| `dolly` (push-in / pull-back) | High |
| `truck` (lateral) | High |
| `pan` | Medium-High (cap with "slow gentle pan") |
| `tilt` | Medium-High |
| `zoom-in / zoom-out` | Medium (often confused with dolly) |
| `pedestal` / `crane` / `jib` | Medium |
| `orbit` | LOW for static scenes (high deformation risk) — avoid |
| `parallax` (alone) | Doesn't parse — pair with "slow truck creating parallax depth" |
| `whip-pan` / `crash zoom` | Avoid — guaranteed hallucination on cars |

**Critical phrases to lock subject:**

```
"subject remains completely still, no character motion, no vehicle motion, locked subject"
"frozen background, exact textures maintained from source image"
```

These two phrases are the MOST POWERFUL anti-drift levers in 2026.

**Mandatory negative prompt for static-scene work:**

```
morphing, deforming, warped vehicle, melting cars, melting metal, extra figures, hallucinated people, hallucinated pedestrians, character motion, subject motion, sliding, rubber physics, distorted wheels, distorted grille, text morphing, double exposure, warped environment, low quality, flicker, compression artifacts, background drift
```

**Cost discipline:**

| Mode | Cost | When to use |
|---|---|---|
| Kling 2.5 Pro Standard | ~10 cr / 5s | DAILY DRIVER. Filler B-roll, slow camera moves on static stills. Quality strong at 1080p |
| Kling 3.0 Pro | ~35-40 cr / 5s | Hero shots only. Reserve for opener, close-up grille shots, moments where slight quality matters |
| Native Audio | +20 credits | Always OFF for our pipeline (audio added in edit) |
| Multi-Shot | n/a | Always OFF for our 5-sec single camera moves |

**Speed slider:** keep at 1-2 out of 5. Above 2 = morphing on cars/hard surfaces.

**Watermark behaviour by model (verified 2026-04-29):**
- **Kling 3.0** on Starter tier → **watermarks output** (bottom-right). Crop bottom 60-80px or cover with logo bug.
- **Kling 2.5 Turbo** on Starter tier → **NO watermark** (verified empirically on 2 generated clips). Another reason 2.5 Turbo is the daily driver.
- Behaviour may change as Kling updates — verify on first render of each new project before trusting.

**Duration:** controlled by UI, NEVER in prompt body. Writing "over 5 seconds" in prompt makes Kling rush motion.

### Locked Kling 3.0 prompt template

```
[Scene description with anchor], [subject state with stillness lock], [environment/lighting]. [Camera verb at end with speed and qualifier].
```

Negative prompt (always):

```
morphing, deforming, warped vehicle, melting cars, extra figures, hallucinated people, character motion, subject motion, distorted wheels, text morphing, double exposure, low quality, flicker, background drift
```

### Working Kling templates for AU Dealer Math

**Template A — Lateral truck on wide shot:**
```
Australian car-yard scene at golden hour, rows of generic vehicle silhouettes in sharp focus, warm rim light, dust haze in background. All vehicles remain completely still, no movement of any car, no doors opening, no figures present, locked subject, frozen background, exact textures maintained from source image. Slow lateral truck right, smooth tripod glide, gentle parallax depth, 1x speed, no rotation, no zoom.
```

**Template B — Dolly pull-back on subject:**
```
Close shot of [subject], [time-of-day light], sharp [detail anchor]. The [subject] remains completely still, no movement, locked subject, frozen environment. Slow dolly pull-back, smooth tripod glide, 1x speed, no rotation, no zoom.
```

**Template C — Push-in on signage / static element:**
```
[Scene] with bold [element], [light condition], sharp [text/logo detail]. Scene completely static, no figures, no vehicle motion, no door movement, frozen environment, exact textures maintained from source image. Slow dolly push-in toward the [element], smooth tripod glide, 1x speed, no rotation.
```

### Pre-submit checklist (Kling)

Before clicking Generate, validate:

- [ ] Camera verb is at the END of the positive prompt?
- [ ] Subject lock phrase included? ("subject remains completely still, locked subject, frozen environment")
- [ ] Negative prompt loaded with full anti-hallucination block?
- [ ] Single-Shot mode (Multi-Shot OFF)?
- [ ] Native Audio OFF?
- [ ] Speed slider 1-2?
- [ ] Using Kling 2.5 Pro for daily B-roll, NOT 3.0?
- [ ] Duration set in UI only (not in prompt body)?
- [ ] No "moves," "goes," "shifts" in prompt?
- [ ] No `orbit`, `whip-pan`, `crash zoom`?
- [ ] One camera move per clip (not "dolly in then pan right")?

---

## TOOL 3 — InVideo AI

### Research findings (InVideo AI Max plan, 2026)

**Best-use:** draft generator only. Pipeline: **Script (you) → InVideo (rough draft + voice + rough cut) → DaVinci Resolve (free) for finishing.** InVideo's output quality cap is below YouTube-monetisation grade for explainer niches without final polish.

**Critical rules:**

1. **Use script-to-video mode, not prompt-to-video.** Always feed your own written script. Prompt-only is for social <60 sec.
2. **Upload your existing Macca ElevenLabs PVC sample** into InVideo's Voice Clone slot (Max = 5 slots) so InVideo renders Macca natively. Do NOT use InVideo's default TTS — robotic output is the #1 user complaint.
3. **Override stock B-roll aggressively.** Pre-load Midjourney stills + Storyblocks downloads to project bin BEFORE generation. Magic-command per-scene swap any auto-pick misses.
4. **Plan for 25% command-failure rate** (industry baseline). Budget 3-5 Magic Command rounds per video.
5. **YouTube 2026 mandatory disclosure** — every AI-voice video must check "Altered or Synthetic Content" at upload. Permanent monetisation ineligibility if missed.

**InVideo prompt template:**

```
Create a [duration]-minute faceless YouTube explainer for [audience]. 
Tone: [calm/blunt/no-BS/ex-dealer authority]. 
Visual: [flat 2D editorial illustrations, no people on screen, charcoal/cream palette]. 
Script: [paste your full script verbatim]. 
Voice: my cloned voice [Macca voice ID].
Music: low-key cinematic, no upbeat pop. 
End with: [CTA verbatim].
```

### Pre-submit checklist (InVideo)

- [ ] Using script-to-video mode (not prompt-to-video)?
- [ ] Full script pasted (not summary)?
- [ ] Macca PVC voice selected (not InVideo default TTS)?
- [ ] Project asset bin pre-loaded with Midjourney stills + Storyblocks B-roll?
- [ ] Per-scene visual cues `[VISUAL: X]` in script?
- [ ] Magic Command planned for swapping mediocre stock picks after first preview?

---

## TOOL 4 — Submagic

### Research findings (Submagic, 2026)

**Top 5 rules for editorial-pace Submagic:**

1. **Use the "Ali" template, not Hormozi/Beast.** Ali Abdaal's preset is the only Submagic template purpose-built for editorial-explainer pace: word-by-word fade with sober colors, no rotation, no bounce, TT Fors font. Hormozi 1-5/Beast/Devin are TikTok-bro presets and will kill the consumer-protection tone.
2. **Pre-load the custom dictionary BEFORE first render** with AU vernacular: `drive-away`, `rego`, `EOFY`, `ute`, `dealer delivery`, `LCT`, `stamp duty`, `BAS`, `RWC`, `comprehensive`, `CTP`, plus dealer brand names. AI is "unreliable with strong regional accents" — pre-seeding niche terms is the only way to avoid render-then-edit cycles.
3. **Cap highlight colors at one (gold/yellow), not three.** Submagic supports 3 highlight colors; using all 3 reads as TikTok bro. Editorial = brand accent on the load-bearing word only (the dollar figure, the percentage, the dealer name).
4. **Burn-in captions, do NOT rely on YouTube auto-CC.** Documented 12-15% completion-rate lift (Opus 2026) and 15-25% watch-time lift on word-by-word styles. Auto-CC can be disabled by viewers; burn-in cannot. Always burn-in. Also upload a clean SRT to YouTube for accessibility/SEO.
5. **Manual-tweak emphasis on every video** — auto-emphasis over-fires. Workflow: let auto-pass run, then strip ~60-70% of highlights, keep only numbers, dealer names, and the one-word punchline per beat.

### Locked AU Dealer Math Submagic config

| Setting | Value | Why |
|---|---|---|
| Template | **Ali** (or Kelly fallback) | Only editorial-pace native template |
| Position | Center-third of screen | Standard reading position |
| Font size | 18-24pt | Mobile-legible, not frantic |
| Caption length | Max 5-7 words / line, 32-42 char | Opus 2026 standard |
| Hold time | 1.5-3s per caption (0.3s/word + 0.5s buffer) | Calm pace |
| Highlight colors | **1 only — outback orange #D17A3D** for dollar figures + dealer names | Editorial discipline |
| Animation | Word-by-word fade (Ali default). **Disable bounce/rotate** | Editorial vs TikTok |
| Auto-zoom | ON, but cap at 2-3 punches per 60s | Strip excess |
| B-roll suggestions | Vet for AU relevance (library is US-skewed) | Manual override |
| Export | 1080p 30fps (Starter cap) | Verify audio-video sync in preview before final |
| Burn-in | YES + upload separate clean SRT to YouTube | SEO + accessibility belt-and-braces |

### Custom dictionary (load BEFORE first render)

```
drive-away, rego, EOFY, ute, dealer delivery, LCT, stamp duty, BAS, RWC, comprehensive, CTP, ACCC, ASIC, Macca, Hilux, Prado, Land Cruiser, Camry, Corolla, Mercedes-Benz, Hyundai, Mazda, Holden, BYD, MG, Toyota
```

Path: Submagic editor → Fonts & Captions → Custom Dictionary → "Add custom word."

### Pre-submit checklist (Submagic)

- [ ] Template = Ali / Iman / Kelly / Karl (NOT Hormozi/Beast/Devin)?
- [ ] Custom dictionary loaded with AU vernacular + brand names?
- [ ] Highlight colors capped at 1 (outback orange)?
- [ ] Manual emphasis pass — stripped 60-70% of auto highlights?
- [ ] Audio-video sync verified in preview (NOT just trusted)?
- [ ] 1080p 30fps export confirmed?
- [ ] SRT downloaded for YouTube upload alongside burn-in?

---

## TOOL 5 — ElevenLabs (Macca voice — Paul, Default Library)

### Pivot from PVC plan (locked 2026-04-29)

Originally planned: Fiverr voice actor → 5-min recording → ElevenLabs PVC training. **Dropped because:**
- ElevenLabs PVC official minimum is 30 min source; 5 min produces below-IVC-grade clone
- $270 AUD avoidable cost
- Stock library Paul voice is already professionally tuned for the Macca brief

**Macca voice locked for lifetime of channel:** Paul (Australian Professional Presenter)
- **Voice ID:** `WLKp2jV6nrS8aMkPPDRO`
- **Type:** ElevenLabs Default Library, multilingual

### Research findings (ElevenLabs stock library voice, 2026)

**Top 5 rules:**

1. **Render Macca on Multilingual v2, NOT v3.** ElevenLabs explicitly states stock + PVC voices are "not fully optimized for Eleven v3" in current research-preview phase. Multilingual v2 = 2026 best for batch narration on stock voices.
2. **Stock-library settings: Stability 0.40 / Similarity 0.75 / Style 0.25 / Speaker Boost ON / Speed 0.95.** Stock voices need LOWER stability than PVCs — 0.40 produces "talking-to-a-mate" cadence; 0.55+ on stock voices reads robotic. Higher similarity (0.75) anchors the voice to its tuned profile.
3. **Punctuation > tags for explainer cadence.** Multilingual v2 doesn't accept v3 audio tags. Control delivery via: ellipses (`…`) for hesitation/reveal pauses, em-dashes (`—`) for sharp breaks, ALL-CAPS for dollar emphasis (`$8,500`), question marks for genuine intonation lift, SSML `<break time="1.0s"/>` for hard pauses (works on v2 only).
4. **Build pronunciation dictionary day one for AU vernacular + brand names.** Use **CMU Arpabet, not IPA**. Critical entries: `ute → Y UW1 T`, `EOFY → ee oh eff why`, `Mercedes-Benz → mer-SAY-deez benz`, `4WD → four wheel drive`, `rego`, `arvo`, `drive-away`, plus every car brand we'll voice.
5. **Chunk scripts ≤2,000 chars per generation.** Prevents voice drift over long renders. Splice in post.

### Locked Macca settings (Paul, stock library)

| Setting | Value | Why |
|---|---|---|
| Voice | **Paul - Australian Professional Presenter** (`WLKp2jV6nrS8aMkPPDRO`) | Locked Macca voice |
| Model | **Multilingual v2** | Optimised for batch narration on stock voices |
| Stability | **0.40** | Stock voices need lower stability than PVCs. 0.40 = talking-to-a-mate cadence. 0.55+ on stock = robotic |
| Similarity | **0.75** | Anchors voice to tuned profile |
| Style | **0.25** | Slight performative nudge softens "Professional Presenter" polish into explainer cadence |
| Speaker Boost | **ON** | Standard for podcast/explainer output |
| Speed | **0.95** | Slightly slower than 1.0 for editorial cadence |
| Chunk size | **≤2,000 chars per generation** | Prevents voice drift over long renders. Splice in post |

### Source-recording requirements

**RETIRED 2026-04-29.** Pivoted from PVC plan to ElevenLabs stock library voice (Paul). No source recording required.

If we ever revisit PVC for a future video, the original spec remains: ≥30 min duration, 24-bit 44.1/48kHz WAV, broadcast levels, XLR condenser mic, treated room, consistent mic distance.

### Punctuation conventions (Macca scripts going forward)

| Mark | Effect | When to use |
|---|---|---|
| `…` (ellipsis) | Pause + trailing uncertainty | Reveals: *"…and that's $4,200 over a fair price."* |
| `—` (em-dash) | Sharp break | Asides: *"the dealer — and this is the bit they hate — keeps the gap as profit."* |
| `-` (hyphen) | Brief micro-pause | Hyphenated words / micro-emphasis |
| `<break time="1.0s"/>` | Hard pause (Multilingual v2 ONLY) | Scene transitions |
| ALL-CAPS | Emphasis | Dollar figures: `$8,500 DRIVE-AWAY`, `THIRTY-FIVE HUNDRED` |
| `?` | Genuine intonation lift | Real questions only — don't fake-question statements |

### Pronunciation dictionary (load before first render)

CMU Arpabet entries:
- `ute → Y UW1 T`
- `EOFY → ee oh eff why`
- `arvo → AR-voh`
- `rego → REH-goh`
- `drive-away → drive away` (write as two words, no hyphen — usually renders better)
- `Mercedes-Benz → mer-SAY-deez benz`
- `Hyundai → HUN-day` (NOT "high-un-day")
- `Mazda → MAZ-duh`
- Plus every car model we'll reference

Path: ElevenLabs → Voice Lab → Macca PVC → Pronunciation Dictionary → Add Entry.

### Pre-submit checklist (ElevenLabs Paul / Macca render)

- [ ] Voice = Paul (`WLKp2jV6nrS8aMkPPDRO`)?
- [ ] Model = Multilingual v2 (NOT v3)?
- [ ] Settings: Stability 0.40 / Similarity 0.75 / Style 0.25 / Speaker Boost ON / Speed 0.95?
- [ ] Pronunciation dictionary pre-loaded with AU vernacular + brand names?
- [ ] Script chunked ≤2,000 chars per generation?
- [ ] Punctuation conventions applied (ellipses for reveals, em-dashes for asides, ALL-CAPS for dollar figures)?

---

## Universal pre-submit ritual

For ANY prompt going to ANY credit-spending tool:

1. **Pull the locked template** for that tool from this doc
2. **Fill in the variables** — don't write from scratch
3. **Run the tool's pre-submit checklist** (above for each tool)
4. **One re-read of the assembled prompt** — reads naturally? matches the template? no banned words?
5. **Submit ONCE** — expect first-shot success
6. **If first shot fails** — that's a research issue (template wrong for this case), not a tool issue. Update the doc, don't iterate-and-burn-credits

---

## Settings-precision rule (binding on Claude, locked 2026-04-29)

When Claude tells Adrian to do anything in a SaaS UI, Claude MUST already know:

- ✅ **Exact UI element name + position** (e.g. *"bottom-left of the generate panel, the toggle labelled 'Native Audio' with the green check"*)
- ✅ **Exact toggle states** (tick this / untick this — not "you might want to consider")
- ✅ **Exact credit/time cost** for the action (verified, not estimated)
- ✅ **Exact default behaviour** (what happens if Adrian doesn't change anything)
- ✅ **Exact failure modes** (what error messages appear, what triggers them)

If Claude doesn't know any of the above, Claude researches it BEFORE giving instructions, not after Adrian sits in front of the UI confused.

Adrian directive 2026-04-29: *"When you ask me to do something, I want you to know exactly what settings are available on each platform and tell me, untick this, tick this box, select this option. I don't wanna be going backwards and forwards."*

If a tool changes UI / pricing / behaviour mid-flight (like Kling did with watermark gating), Claude owns the miss + updates this doc.

## Variant-description rule (Midjourney + any 4-grid output, locked 2026-04-29)

When Claude reviews a Midjourney 4-grid (or any AI tool that returns multiple variants in a grid), Claude MUST describe each variant by **visual content**, not by file number or grid position number.

Adrian's UI shows a 2×2 grid of images without numbers. He cannot map "_0 / _1 / _2 / _3" file-suffix numbering to the visual grid he's looking at.

**Format for each variant when reviewing:**
- ✅ *"The variant with the orange sunset and power lines on the right side (upscale button U2 — top-right of grid)"*
- ✅ *"The atrium with two-storey glass facades and orange organic-pattern panels (U1 — top-left)"*
- ❌ *"Variant _2"* (means nothing visually to Adrian)
- ❌ *"The third one"* (which order? grid order varies)

**Position mapping for upscale buttons:**
- U1 = top-left of grid
- U2 = top-right
- U3 = bottom-left
- U4 = bottom-right

**Always include both: visual description + U-button label.** Adrian sees the grid → reads visual description → matches to U-button → clicks the right upscale.

Adrian directive 2026-04-29: *"I can't tell the order that these images are in. I can only look at the descriptions that you give me to differentiate between the different ones."*

---

## Channel-aesthetic --sref lock (Midjourney workflow, locked 2026-04-29)

Before re-generating V1 stills (or any future video), execute this once:

1. Pick 3 reference images representing channel aesthetic — Polymatter / Wendover Productions / Cleo Abram screenshots, or specific frames from each
2. Upload to a public URL (or use Midjourney URLs directly)
3. Run ONE Midjourney generation: `[generic test subject] --ar 16:9 --style raw --stylize 100 --sref <URL1> <URL2> <URL3> --sv 4 --v 7`
4. Pick the output that best matches our intended editorial aesthetic
5. **Note the returned `--sref <code>`** that Midjourney generates from your reference set
6. **Lock that code in this doc** under "Channel `--sref` code:" below
7. **Every future Midjourney prompt** uses `--sref <that-code> --sv 4`

**Channel `--sref` code (LOCKED here when generated):** `[TBD — generate next session]`

This guarantees palette + lineweight + texture consistency across V1 → V100 thumbnails, B-roll, scene illustrations.

---

## Doc maintenance

This doc updates whenever:
- A prompt produces unexpected output → root cause analysis added to "what failed" section for that tool
- New tool added to the SaaS stack → new section added
- Tool releases major version update → revalidate against current behaviour
- New successful pattern discovered from a future video → added to "what worked" section

Last updated: 2026-04-29 — V1 production lessons + all 5 research agents synthesised.

All 5 tools covered: Midjourney v7, Kling 3.0, InVideo AI, Submagic, ElevenLabs PVC.

Settings-precision rule + `--sref` channel-aesthetic-lock workflow added.
