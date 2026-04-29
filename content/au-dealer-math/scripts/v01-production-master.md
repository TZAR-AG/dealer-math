# V1 Production Master — Engineered Prompt Sheet

**Purpose:** Show-stopper V1 production using the full paid SaaS stack (Nano Banana Pro · Midjourney · Kling 3.0 · InVideo AI Max · Storyblocks · ElevenLabs · CapCut · Submagic). Every prompt is engineered for AUDM's brand voice + Macca persona + the expanded V1 script.

**Scope:** Faceless — V1 has NO mascot. Macca-mascot composites enter from V2+ once Fiverr delivers the character ref sheet. Every visual prompt below preserves negative space / clean compositions where a mascot could be added later.

**VO foundation:** All 7 scenes re-rendered at ElevenLabs Paul speed **0.90**, total runtime **10:58**. Files in `voice/vo-scene-*.mp3`. Hits 2 mid-roll ad eligibility (≥10:00).

---

## 0. Layer architecture

V1's 10:58 runtime is built in 7 layers. **Kling is only ~10% of motion** — the rest comes from CapCut native effects + Storyblocks B-roll + animated overlays.

| Layer | Source | Share of runtime | Per-clip cost |
|---|---|---|---|
| 1. Anchor scene establishment | NB Pro + Midjourney stills | ~20% (~2 min) | NB ~$1.23, MJ ~$0.10 |
| 2. Motion punctuation | Kling 3.0 (image-to-video) | ~10% (~1 min) | ~$0.40-0.80/clip |
| 3. B-roll variety | InVideo AI auto-match + Storyblocks | ~30% (~3 min) | Subscription covers |
| 4. Animated emphasis | CapCut Text + Animation | ~10% (~1 min) | Free |
| 5. Continuity motion | CapCut Ken Burns (varied per still) | ~25% (~2.5 min) | Free |
| 6. Audio bed | Storyblocks instrumental | underlies all 10:58 | Subscription covers |
| 7. Captions | YouTube auto-CC (long-form) + Submagic (Shorts) | overlay | Subscription covers |

**Per-tool unique strengths (so we use each correctly):**

| Tool | Strong zone | Weak zone |
|---|---|---|
| **Nano Banana Pro** | Brand-consistent stylized AU dealership scenes; physical objects (papers, products); 16:9 native; fast iteration | Screens showing content; characters/people |
| **Midjourney Standard** | Photorealistic close-ups; documents with realistic paper grain; product hero shots; cinematic atmosphere | Brand-style consistency without seed images; faster iteration |
| **Kling 3.0** | Image-to-video motion (5-8s); subtle camera moves; preserve geometry | Complex motion; long sequences; characters |
| **InVideo AI Max** | Bulk auto-match B-roll to script; text-to-video for generic shots; full pipeline assembly | Brand-locked aesthetic (generic feel); fine control |
| **Storyblocks** | Generic AU street/dealership/finance B-roll; documentary-style cutaways | Brand-specific scenes; fine narrative control |

---

## 1. Brand-locked prompt phrases (carry across ALL prompts)

**Use in every NB/Midjourney prompt:**
- Palette: `charcoal #2B2B2B, cream #FAF7F2, outback orange #C8612C accent`
- Light: `warm late-afternoon Australian light from upper-left, long soft shadows`
- Style: `cinematic editorial photography, premium automotive industry documentary aesthetic`
- Style refs that anchor on-brand: `in the style of Mad Men set design, Carlos Cruz-Diez palette, late afternoon Sydney suburb`
- Always: `no text, no typography, no words, no letters, no logos, no brand names, no human figures` (faceless brand lock + V1 has no mascot yet)

**Phrases to AVOID:**
- "luxury car ad", "glamour shot", "promotional" — pulls toward generic stock photography
- "studio lighting", "white background" — wrong aesthetic for AUDM dealer-reveal niche
- "smiling salesperson", "happy customer" — faceless brand violation
- "modern minimal" — pulls toward Apple-style aesthetic; we want documentary-grit

---

## 2. Per-scene prompt sheet

For each scene: **VO duration · current visual asset · what's missing · prompts to fill the gap.**

### Scene 1 — HOOK (0:00–0:24, 24 sec)

**Existing:** `kling-clip-1-hook.mp4` (5s) → `still-kling-clip-1-end.png` (19s on screen)
**Status:** ✅ ADEQUATE for V1. Hook scene is short. Add subtle Ken Burns to the still + 1 dollar-figure overlay at 0:02 ("$300/WEEK") and we're done.

**No new AI assets needed for Scene 1.** Skip to Scene 2.

---

### Scene 2 — AUTHORITY ANCHOR (0:24–1:06, 42 sec)

**Existing:** `still-1-dealership-floor.png` (the wide dealership floor with Macca silhouette walking)
**Visual gap:** 42 sec on a single still. Need 1 motion clip + 2 supporting visuals.

#### NEW asset 2A — Anchor still (Nano Banana Pro)

**Prompt:**
```
Top-down photograph of a worn manila training binder labeled with embossed
text on a charcoal-toned office desk, closed cover facing up, beside it a
ceramic coffee cup and a fountain pen, soft warm late-afternoon Australian
light from upper-left casting long shadow, premium automotive industry
documentary aesthetic, cinematic editorial photography, in the style of
Mad Men set design, palette of charcoal #2B2B2B and cream #FAF7F2 with
outback orange #C8612C accent on the binder spine. 16:9 landscape, shallow
depth of field. No text, no typography, no words, no letters, no logos,
no brand names, no human figures.
```
**Use as:** anchor visual at ~0:42 when Macca says "Started on the floor at a Japanese mass-market brand..." — implies the training history

#### NEW asset 2B — Kling motion clip from 2A

**Input:** asset 2A above (training binder still)
**Kling prompt (image-to-video):**
```
slow camera tilt down toward the closed manila training binder on the desk,
binder spine sharpening into focus as the lens approaches, pen and ceramic
coffee cup beside it in soft focus, warm desk lamp lighting from upper-left
unchanged, no figures, gentle subtle motion, cinematic stabilised, 5 seconds
```

#### NEW asset 2C — Storyblocks B-roll search terms

For 5-8 sec cutaway between still-1 and 2A:
- `australian car dealership floor wide`
- `dealership reception desk paperwork`
- `salesperson silhouette walking dealership`

---

### Scene 3 — THE QUESTION (1:06–3:02, 1:56)

**Existing:** `still-2-customer-confusion.png` (orange-toned salesperson + customer scene)
**Visual gap:** 1:56 on a single still. Need 4 supporting visuals + 2 motion clips.

#### NEW asset 3A — Anchor still: salesperson asking the budget question (Midjourney)

**Why Midjourney over NB:** photorealistic dialogue scene with composition control. Use Midjourney's `--style raw` for documentary feel.

**Prompt:**
```
cinematic close-up of an Australian car dealership desk seen from a low
side angle, salesperson hand reaching toward the customer hand across the
desk, only hands and forearms visible, papers and a calculator on the
desk surface, late afternoon warm orange light streaming from a window
behind the salesperson, charcoal palette with outback orange wash,
documentary photojournalism aesthetic, in the style of cinema vérité,
shallow depth of field, no faces visible, no logos --ar 16:9 --style raw
--stylize 250 --v 6.1
```

#### NEW asset 3B — Anchor still: "Road to a Sale" training binder open (Nano Banana Pro)

**Prompt:**
```
Top-down photograph of an open worn manila training binder on a charcoal
office desk, the visible page showing a numbered three-step diagram with
arrows pointing between steps, paper aged with subtle handling marks, a
red marker pen resting beside it, soft warm late-afternoon Australian
light from upper-left, premium automotive industry documentary aesthetic,
cinematic editorial photography, palette of charcoal #2B2B2B and cream
#FAF7F2 with outback orange #C8612C marker. 16:9 landscape, shallow depth
of field. No text, no typography, no words, no letters, no logos, no brand
names, no human figures.
```

**Note:** the diagram on the page should be visual blocks/arrows only — text overlays for "STEP 1 RAPPORT / STEP 2 NEEDS / STEP 3 BUDGET" added later in CapCut.

#### NEW asset 3C — Anchor still: the conversation moving onto rails (Midjourney)

**Prompt:**
```
abstract cinematic visualization of a conversation moving onto a track,
two parallel rails curving away into late-afternoon orange haze, warm
charcoal foreground with cream signage posts beside the rails, premium
automotive industry documentary aesthetic, dramatic Australian dusk
lighting, shallow depth of field, in the style of Caspar David Friedrich
landscape painting --ar 16:9 --style raw --v 6.1
```

#### NEW asset 3D — Kling motion clip from 3A

**Input:** asset 3A (hands-across-desk still)
**Kling prompt:**
```
extreme subtle camera dolly forward and slight push-in toward the hands
across the desk, late afternoon orange light shifting almost imperceptibly,
papers and calculator unchanged in position, photojournalistic stabilised
motion, 5 seconds
```

#### NEW asset 3E — Kling motion clip from 3B

**Input:** asset 3B (open training binder)
**Kling prompt:**
```
slow vertical camera lift away from the open training binder, the diagram
on the page receding gradually as the camera rises, marker pen and desk
surface fading into soft focus, warm light unchanged, cinematic stabilised
motion, 5 seconds
```

#### Storyblocks B-roll for Scene 3:
- `dealer training program manual`
- `salesperson conversation customer`
- `paperwork desk close-up`

---

### Scene 4 — THE LOAN-TERM TRICK (3:02–5:46, 2:44) ⭐ BIGGEST CONVERSION SCENE

**Existing:** `still-3-cars-comparison.png` + `kling-clip-3-cars-parallax.mp4` (5s) + `still-kling-clip-3-end.png`
**Visual gap:** 2:44 with one motion clip. Need 4 NEW visuals + 2 motion clips. This is the centerpiece reveal — invest the most here.

#### NEW asset 4A — Anchor still: $300/wk × 4yr vs 7yr split-screen math (Nano Banana Pro)

**Prompt:**
```
Cinematic split-screen photograph: left half a stack of 4 layered cream
papers on a charcoal desk, right half a much taller stack of 7 layered
cream papers on the same desk, the 7-paper stack visibly bigger and
heavier, dramatic warm late-afternoon Australian light from upper-left
casting long shadows, depth contrast between the two stacks emphasised,
premium automotive industry documentary aesthetic, cinematic editorial
photography. 16:9 landscape, shallow depth of field. Palette of charcoal
#2B2B2B and cream #FAF7F2 with outback orange #C8612C accent. No text,
no typography, no words, no letters, no logos, no brand names, no human
figures.
```

**CapCut overlay:** "$300/WK × 4 YRS = $62,400" left + "$300/WK × 7 YRS = $109,200" right + "$46,800 MORE →" between them, all in `#FFD700` Anton font 200pt

#### NEW asset 4B — Anchor still: dealership commission diagram visualization (Midjourney)

**Prompt:**
```
overhead view of a charcoal desk with a single document at the centre
showing a stylized branching tree diagram drawn in outback orange ink,
multiple branches splitting from the central trunk, warm late-afternoon
Australian light from upper-left, documentary photojournalism aesthetic,
charcoal palette with cream paper and outback orange ink, in the style
of cinema vérité, shallow depth of field --ar 16:9 --style raw
--stylize 250 --v 6.1
```

#### NEW asset 4C — Anchor still: the MORE EXPENSIVE car (Nano Banana Pro)

**Prompt:**
```
Cinematic photograph of a single premium Australian sedan parked on a
charcoal showroom floor under a warm overhead spotlight, polished dark
paint reflecting the spotlight, charcoal walls, parquet floor, soft
fall-off into shadow at the edges of the frame, premium automotive
industry documentary aesthetic, cinematic editorial photography,
in the style of Mad Men set design. 16:9 landscape, shallow depth of
field. Palette of charcoal #2B2B2B and cream #FAF7F2 with outback
orange #C8612C accent in the spotlight glow. No text, no typography,
no words, no letters, no logos, no brand names, no human figures,
no badges visible on the car.
```

#### NEW asset 4D — Anchor still: GFV trade-up treadmill visualization (Midjourney)

**Prompt:**
```
cinematic visualization of three identical luxury sedans receding into
warm orange haze, all three positioned on a charcoal turntable platform,
the closest sedan crisp and sharp, the middle and far sedans progressively
softer in focus suggesting model-cycle replacement, premium automotive
industry documentary aesthetic, late-afternoon Australian dusk lighting,
shallow depth of field, in the style of Andrei Tarkovsky --ar 16:9
--style raw --stylize 300 --v 6.1
```

#### NEW asset 4E — Kling motion from 4A

**Input:** asset 4A (split-stack math)
**Kling prompt:**
```
slow camera dolly from left to right across the two paper stacks, the
4-paper stack first then the 7-paper stack, the size contrast becoming
more apparent as the camera moves, warm light unchanged, cinematic
stabilised motion, 5 seconds
```

#### NEW asset 4F — Kling motion from 4D

**Input:** asset 4D (luxury sedan treadmill)
**Kling prompt:**
```
gentle parallax camera dolly slowly pulling backward from the three
identical luxury sedans, all sedans holding still while the warm haze
behind them shifts subtly, depth-of-field deepening as the camera
recedes, cinematic stabilised motion, 5 seconds
```

#### Storyblocks B-roll for Scene 4:
- `loan calculator close-up hands`
- `signing finance contract pen`
- `australian luxury car dealership showroom`
- `manufacturer logo plate stylized`

---

### Scene 5 — WHY THE DEALER PLAYS (5:46–8:35, 2:49) ⭐ MOST VIRAL POTENTIAL

**Existing:** `still-4-three-rooms.png` (the three doors / aftercare/finance scene)
**Visual gap:** 2:49 with one still. Need 5 NEW visuals + 3 motion clips. The dealer-reveal climax — invest heavily.

#### NEW asset 5A — Anchor still: aftercare manager office (Nano Banana Pro)

**Prompt:**
```
Cinematic photograph of a clean reception desk in an automotive aftercare
office, on the desk a single black bottle with sleek minimal labelling
beside a folded microfiber cloth and a silver tin container, warm
late-afternoon Australian light from a single window upper-left, charcoal
walls fading to shadow at edges, premium automotive industry documentary
aesthetic, cinematic editorial photography, in the style of Mad Men
set design. 16:9 landscape, shallow depth of field. Palette of charcoal
#2B2B2B and cream #FAF7F2 with outback orange #C8612C glow from desk
lamp. No text, no typography, no words, no letters, no logos, no brand
names, no human figures.
```

#### NEW asset 5B — Anchor still: paint protection bottle hero (Midjourney)

**Why Midjourney:** product hero shot needs photorealistic precision.

**Prompt:**
```
extreme close-up product hero photograph of a sleek matte black automotive
detailing bottle with no labels, single dramatic spotlight from upper-left
catching the bottle edge, charcoal background fading to deep black at
edges, surface beneath is a polished slate counter showing subtle reflection,
shallow depth of field with bottle sharp and background gentle bokeh,
premium product photography aesthetic, in the style of Apple product
photography meets Caravaggio chiaroscuro --ar 16:9 --style raw
--stylize 350 --v 6.1
```

#### NEW asset 5C — Anchor still: finance manager office desk (Nano Banana Pro)

**Prompt:**
```
Cinematic photograph of an automotive finance manager's office desk
overhead view, at the centre a single loan contract on cream paper with
a fountain pen resting on it, beside the contract a simple calculator
and a coffee cup, warm late-afternoon Australian light from upper-left,
charcoal desk surface, premium automotive industry documentary aesthetic,
cinematic editorial photography, in the style of Mad Men set design.
16:9 landscape, shallow depth of field. Palette of charcoal #2B2B2B
and cream #FAF7F2 with outback orange #C8612C accent. No text, no
typography, no words, no letters, no logos, no brand names, no human
figures.
```

**CapCut overlay:** when VO says "the bank approves at one rate; the contract gets written at a higher one" — overlay text "BANK 7.0% → CONTRACT 9.0%" in `#FFD700`.

#### NEW asset 5D — Anchor still: the holdback hidden layer (Midjourney) ⭐ FLAGSHIP REVEAL

**Why this matters:** the holdback explanation is the channel's flagship dealer-reveal. Visual must land.

**Prompt:**
```
cinematic three-tier paper stack visualization on a dramatic charcoal
desk, the top paper crisp and well-lit showing a contract layout, the
middle paper partially in shadow, the bottom paper almost completely
obscured in deep shadow with only the corner edge visible, dramatic
single-source warm orange light from upper-left, very deep chiaroscuro
contrast revealing what's hidden vs what's visible, premium automotive
industry documentary aesthetic, in the style of Caravaggio chiaroscuro
meets cinema vérité, shallow depth of field --ar 16:9 --style raw
--stylize 400 --v 6.1
```

#### NEW asset 5E — Anchor still: volume rebate dollar visualization (Nano Banana Pro)

**Prompt:**
```
Cinematic photograph of stacked Australian banknotes on a charcoal desk,
the stack neatly arranged but voluminous, soft warm late-afternoon
Australian light from upper-left casting long soft shadows behind the
stack, charcoal background fading to deep shadow at edges, premium
automotive industry documentary aesthetic, cinematic editorial
photography. 16:9 landscape, shallow depth of field. Palette of
charcoal #2B2B2B and cream #FAF7F2 with outback orange #C8612C accent
from light glow. No text, no typography, no words, no letters, no
logos, no brand names, no human figures.
```

**CapCut overlay:** "$30,000 BACK ON $350,000 BUY" in `#FFD700` over the cash stack.

#### NEW asset 5F — Kling motion from 5A

**Input:** 5A (aftercare desk)
**Kling prompt:**
```
slow camera dolly forward through the threshold of the aftercare office,
revealing the desk with the bottle, cloth and tin progressively closer,
warm light from upper-left unchanged, cinematic stabilised motion,
no figures, 5 seconds
```

#### NEW asset 5G — Kling motion from 5C

**Input:** 5C (finance manager desk)
**Kling prompt:**
```
top-down zoom-in onto the loan contract page, camera descending slowly,
the calculator and pen beside it staying in frame, paper grain sharpening
as the lens approaches, warm desk lamp light unchanged, cinematic
stabilised motion, 5 seconds
```

#### NEW asset 5H — Kling motion from 5D ⭐ KEY VIRAL MOMENT

**Input:** 5D (three-tier holdback stack)
**Kling prompt:**
```
slow lateral camera slide from right to left across the three-tier
paper stack, dramatic warm orange light shifting subtly to reveal more
of the bottom hidden paper as the camera moves, top paper staying
clearly lit, middle paper transitioning between shadow and light,
cinematic stabilised motion, 5 seconds
```

#### Storyblocks B-roll for Scene 5:
- `australian banknotes stack close-up`
- `paint protection product close-up`
- `loan contract paperwork`
- `calculator hands finance`
- `manufacturer rebate paperwork`

---

### Scene 6 — THE FIX (8:35–11:06, 2:31)

**Existing:** `still-5-confident-customer.png`
**Visual gap:** 2:31 with one still. Need 3 NEW visuals + 1 motion clip.

#### NEW asset 6A — Anchor still: bank pre-approval letter (Nano Banana Pro)

**Prompt:**
```
Cinematic top-down photograph of a formal bank pre-approval letter on
cream paper resting on a leather portfolio, a fountain pen beside it,
the letter has a subtle institutional letterhead at top with elegant
horizontal lines (no readable text), warm late-afternoon Australian
light from upper-left, charcoal portfolio leather visible around the
edges, premium banking documentary aesthetic, cinematic editorial
photography. 16:9 landscape, shallow depth of field. Palette of
charcoal #2B2B2B and cream #FAF7F2 with outback orange #C8612C accent.
No text, no typography, no words, no letters, no logos, no brand names,
no human figures.
```

#### NEW asset 6B — Anchor still: total cost comparison side-by-side (Midjourney)

**Prompt:**
```
overhead view of two parallel loan documents on a charcoal desk,
identical layout but one slightly taller stack than the other, warm
late-afternoon Australian light from upper-left casting equal shadows
behind both, sharp focus on both papers, documentary photojournalism
aesthetic, charcoal and cream palette, in the style of cinema vérité,
shallow depth of field --ar 16:9 --style raw --stylize 250 --v 6.1
```

**CapCut overlay:** "BANK $58,000" left + "DEALER $63,500" right, both in `#FFD700`.

#### NEW asset 6C — Anchor still: dealership window with rate banner (Nano Banana Pro)

**Prompt:**
```
Cinematic photograph of a dealership window display from outside the
glass, late-afternoon Australian street reflection partially visible
in the window, inside the window a large promotional banner in
cream-on-charcoal palette with a stylized percentage symbol design,
warm late-afternoon orange light streaming through, premium automotive
industry documentary aesthetic, cinematic editorial photography. 16:9
landscape, shallow depth of field. Palette of charcoal #2B2B2B and
cream #FAF7F2 with outback orange #C8612C banner accent. No text,
no typography, no words, no letters, no logos, no brand names, no
human figures.
```

**CapCut overlay:** "FROM 1.99%" in `#FFD700` Anton 240pt at the centre of the banner.

#### NEW asset 6D — Kling motion from 6C

**Input:** 6C (dealership window)
**Kling prompt:**
```
slow horizontal camera dolly past the dealership window from right to
left, the window banner sharpening as the lens passes, glass reflection
of late-afternoon street life subtly visible, warm orange light shifting
subtly, cinematic stabilised motion, no figures, 5 seconds
```

#### Storyblocks B-roll for Scene 6:
- `australian bank loan letter`
- `signing pen close-up`
- `dealership window finance banner`

---

### Scene 7 — CTA + SIGN-OFF (11:06–11:32, 26 sec)

**Existing:** continues `still-5-confident-customer.png`
**Visual gap:** end card + lead magnet visualization.

#### NEW asset 7A — Anchor still: lead magnet PDF visualization (Nano Banana Pro)

**Prompt:**
```
Cinematic photograph of a closed black laptop on a charcoal desk with
a folded printed cheatsheet beside it, warm late-afternoon Australian
light from upper-left, paper has visible folds suggesting a downloadable
guide, premium automotive industry documentary aesthetic, cinematic
editorial photography. 16:9 landscape, shallow depth of field. Palette
of charcoal #2B2B2B and cream #FAF7F2 with outback orange #C8612C
accent on the cheatsheet edge. No text, no typography, no words, no
letters, no logos, no brand names, no human figures.
```

**CapCut overlay:** add channel wordmark "AU DEALER MATH" + subscribe CTA + lead-magnet URL.

#### Storyblocks B-roll for Scene 7:
- `australian street signage suburb`
- `dealership exterior late afternoon`

---

## 3. InVideo AI Max — text-to-video / B-roll auto-match prompts

InVideo AI does best with **scene-segment summaries** rather than the full script. Feed it each scene's distilled "what's on screen" description. It auto-matches stock footage from its library.

**How to use:** open ai.invideo.io workspace, paste each prompt below into "Generate from text" or "Brand templates" → AI assembles a 30-60 sec scene from its stock library + AI voiceover. We **discard** the AI VO and keep the **B-roll selections** to drop into our CapCut timeline.

### InVideo prompts per scene

**Scene 1 InVideo prompt:**
```
Make a 25-second cinematic video showing Australian car dealerships at
late afternoon. Wide exterior shots of dealership lots with rows of cars,
warm orange sunset light, no people in close-up. 16:9. Charcoal and
warm orange tones. No text on screen.
```

**Scene 2 InVideo prompt:**
```
Make a 45-second cinematic video showing the inside of an Australian car
dealership salesfloor. Top-down dolly shots, salespeople walking past
rows of new cars from a high angle, no faces visible, warm orange interior
lighting, charcoal floors. 16:9. Documentary aesthetic. No text on screen.
```

**Scene 3 InVideo prompt:**
```
Make a 2-minute cinematic video showing salesperson and customer hands
across a dealership desk, papers being shuffled, calculators, training
binders, conversation gestures. No faces visible. Warm late-afternoon
Australian dealership interior. 16:9. Documentary photojournalism style.
No text on screen.
```

**Scene 4 InVideo prompt:**
```
Make a 2-and-a-half-minute cinematic video showing loan paperwork
being signed, calculators displaying numbers, contracts being prepared,
luxury cars being delivered, financial documents being shuffled. No
faces visible, only hands and papers. Warm Australian dealership
interior lighting, charcoal and orange tones. 16:9. Documentary style.
No text on screen.
```

**Scene 5 InVideo prompt:**
```
Make a 3-minute cinematic video showing finance manager offices,
aftercare detailing products on display, bank approval paperwork,
manufacturer rebate documents, money stacks, dealership back-office
workflows. No faces visible, only hands and documents. Warm Australian
late-afternoon lighting, charcoal and orange tones. 16:9. Documentary
photojournalism style. No text on screen.
```

**Scene 6 InVideo prompt:**
```
Make a 2-and-a-half-minute cinematic video showing a confident customer
walking into a dealership with paperwork in hand, bank pre-approval
letters, dealer financing documents being compared side by side, dealership
window displays with promotional banners. No faces in close-up, only
hands and documents and silhouettes. Warm Australian afternoon lighting,
charcoal and orange tones. 16:9. Documentary aesthetic. No text on screen.
```

**Scene 7 InVideo prompt:**
```
Make a 30-second cinematic video showing an Australian dealership
exterior at golden hour, late-afternoon street view, signage stylized,
ending with a closed laptop and folded paper guide on a desk. No faces.
Warm orange light, charcoal and cream palette. 16:9. Documentary style.
No text on screen.
```

**What we want from InVideo:** the **B-roll selections it makes**, not the assembled video. Discard their AI VO, capture the source clip URLs from their stock library (Submagic-class library), download the matched clips, drop into CapCut as the "B-roll variety" layer (Layer 3 in the architecture).

---

## 4. Production order (what to do first, second, third)

**Phase A — Asset generation (parallel, ~2-3 hr unattended-render time):**

1. **Nano Banana Pro:** generate 12 stills (assets 2A, 3B, 4A, 4C, 5A, 5C, 5E, 6A, 6C, 7A, plus extras). ~$15 in credits. Save to `content/au-dealer-math/scripts/v01-renders/stills/v2/`.
2. **Midjourney:** generate 6 stills (assets 3A, 3C, 4B, 4D, 5B, 5D, 6B). ~$0.60 in credits. Save to same v2 folder.
3. **InVideo AI:** open workspace, paste 7 scene prompts, capture B-roll clip selections per scene. Download the auto-matched stock clips (NOT the assembled InVideo video). Save to `motion/v2-broll/`.
4. **Storyblocks:** search the per-scene B-roll terms above, download 3-5 clips per scene. Save to `motion/v2-broll/`.

**Phase B — Motion punctuation (sequential after Phase A, ~3-4 hr render time):**

5. **Kling 3.0:** submit 10-12 image-to-video jobs (assets 2B, 3D, 3E, 4E, 4F, 5F, 5G, 5H, 6D plus 1-2 extras using Phase A stills as inputs). Toggle **NO WATERMARK** before download. Save to `motion/v2/`.

**Phase C — Assembly (CapCut, ~2-3 hr Adrian's time):**

6. Replace all timeline VO clips with new 0.90 renders (~5 min)
7. Re-stretch visuals to new 10:58 scene boundaries (~10 min)
8. Layer in: anchor stills (Phase A NB+MJ) → motion clips (Kling) → B-roll cutaways (InVideo+Storyblocks) per scene
9. Apply varied Ken Burns to all stills (different zoom/pan per still — uniform Ken Burns dies)
10. Add 7-10 dollar-figure text overlays in `#FFD700` Anton 200-240pt
11. Add Storyblocks "calm-confrontation" instrumental music bed at -23 LUFS, fade to silence at sign-off
12. QC pass: scrub through 11 min, check no Kling watermarks, check overlay accuracy, check audio balance

**Phase D — Post-production (~1.5 hr):**

13. Export 1080p MP4 → `final/v1-payment-not-price-pivot.mp4`
14. Submagic: generate 3 Shorts cutdowns from the long-form (kinetic captions only on Shorts)
15. YouTube upload (auto-CC enables) + TubeBuddy SEO optimization
16. Blotato: cross-post the 3 Shorts to TikTok + IG Reels at staggered times

**Total time-to-ship from a fresh start: ~10-12 hr Adrian-hand work + 6-8 hr unattended render time.**

---

## 5. Macca mascot integration (V2+)

**V1 has no mascot.** All visual prompts above preserve negative space where Macca's mascot can composite later.

**When Fiverr mascot delivers (Day 7-10 per AUDM launch plan):**
1. Receive PNG ref sheet of Macca with multiple poses + 3-quarter angles
2. In V2 onwards, use **Midjourney character reference** feature (`--cref` parameter pointing to the Fiverr ref sheet) to generate scene compositions WITH Macca silhouette/pose embedded
3. Alternative: composite Macca PNG onto V1-style scenes in CapCut Layer 4 (animated emphasis layer) — quicker, less consistent
4. Lock the Macca pose library in `brand/audm/macca-poses/` after Fiverr delivery for reuse across V2-V100

**For V1 specifically:** the absence of a face actually reinforces "I sold cars for ten years" — Macca speaks but doesn't appear, leaving the viewer to imagine the dealer-floor experience. Ship V1 faceless, add mascot from V2.

---

## 6. Cost estimate (one-time V1 production)

| Item | Cost AUD |
|---|---|
| Nano Banana Pro: 12 stills × ~$1.23 | ~$15 |
| Midjourney: 6 stills × ~$0.10 | ~$1 |
| Kling 3.0: 12 motion clips (Starter tier credits, included) | $0 marginal |
| InVideo AI: 7 scene auto-matches (Max tier, included) | $0 marginal |
| Storyblocks: 15-20 B-roll clips (All-Access, included) | $0 marginal |
| ElevenLabs: VO already rendered | $0 |
| Submagic: 3 Shorts cutdowns (Starter, included) | $0 marginal |
| **Total marginal V1 production cost** | **~$16 AUD** |

The recurring SaaS subscriptions cover the bulk. Marginal cost per video drops to credits + render time.

---

## 7. Quality gates (DO NOT SHIP if any fail)

- [ ] All Kling clips are watermark-free (verify by scrubbing each clip in CapCut)
- [ ] No human faces in any V1 visuals (faceless brand lock)
- [ ] No specific dealership brand logos visible in any visual
- [ ] No on-screen text contradicts the script (every dollar figure overlay matches what Macca says)
- [ ] Audio mix is at -23 LUFS for VO clarity, music bed sits below at -38 LUFS
- [ ] Total runtime is between 10:00 and 12:00 (mid-roll eligibility window)
- [ ] All 7 scene boundaries align: visual cuts at scene transitions match the VO scene-end timestamps within 0.5 sec
- [ ] No Kling motion clip stretches a still beyond its 5-8 sec native duration
- [ ] Ken Burns animations are VARIED (not uniform across stills — that reads as filler)
- [ ] Final QC watch-through caught no obvious AI artifacts (warped geometry, melting edges, hallucinated text)

---

## Reference

- **Created:** 2026-04-29 evening, after V1 ship deferred
- **Replaces:** `v01-kling-prompts.md` (3-clip plan), `v01-kling-prompts-v2.md` (10-clip plan that didn't account for full SaaS stack)
- **Source content:** `dealer-knowledge-bank.md` Q1-Q8
- **Voice:** ElevenLabs Paul `WLKp2jV6nrS8aMkPPDRO`, speed 0.90, runtime 10:58
- **Brand-naming policy:** category-only attribution per `macca-backstory.md § Brand-naming policy` (Mercedes named only for agency-model topic — not used in V1)
- **Mascot integration:** queued for V2+ once Fiverr delivers Macca character ref sheet (Day 7-10 per AUDM launch plan)
- **Update cadence:** revise after V1 ships with what worked / what didn't, propagate learnings to V2 production
