# Midjourney — AUDM canonical prompt reference

**Engine:** Midjourney v7 (default since 17 June 2025). V8 alpha exists but isn't stable — stay on v7.
**Tier:** Standard $46 AUD/mo per `saas-stack.md`.
**Use AUDM for:** photo-realistic close-ups (documents, products, cinematic detail), V2+ Macca mascot consistency via `--oref`.
**Use NB Pro instead for:** dealership scene establishment, multi-asset still life, faster iteration.

---

## ⚠ Upscale before download (LOCKED 2026-04-29)

**Default MJ web output is 1456×816** — below 1080p height. Without upscaling, Ken Burns zoom (105-108%) on a 1080p timeline pixellates visibly.

**SOP:** every AUDM generation → click **Upscale Subtle** (NOT Creative) → wait ~15-30 sec → Download upscaled. Subtle preserves documentary aesthetic; Creative adds texture/detail that drifts palette.

**Result:** 2912×1632 native, ~2× crisper at 1080p timeline display, headroom for zoom + crop.

**Cost:** ~1 credit per upscale on MJ Standard's quota — trivial.

---

## ⚠ MJ web vs Discord — different syntax (LOCKED 2026-04-29)

**Adrian uses MJ web (midjourney.com/imagine), NOT Discord.** MJ web does NOT accept inline flag syntax like `--ar 16:9` or `--style raw` or `--no [list]`. Those throw "flag not supported" errors.

**MJ web equivalents:**

| Discord flag | MJ web equivalent |
|---|---|
| `--ar 16:9` | Click "16:9" in Aspect Ratio panel |
| `--style raw` | Toggle "Style: Raw" in settings drawer |
| `--s 80` | Scale slider ~80 (Stylize equivalent) |
| `--v 7` | Version selector — set to v7 |
| `--chaos 0` | Variation Mode → Off (or 0) |
| `--no [list]` | **No dedicated UI field — bake negatives into the prompt body** (Adrian 2026-05-05: "mj dosent have an exclude bar"). Use natural-language avoid clauses or descriptive contrasts in the prompt itself. |
| `--sref [URL]` | Style Reference upload — drag URL or upload file |
| `--sw 200` | Style weight slider (if exposed) |

**SOP for AUDM in MJ web:**
1. Paste the prompt body — including any negative/avoid language baked in — into the prompt textarea
2. Right panel: Aspect Ratio → click `16:9`
3. Settings drawer: Style → Raw · Scale → 80 · Version → v7 · Variation Mode → Off
4. Style Reference: drop AUDM palette swatch URL/upload
5. Click Submit

**How to handle negatives without a dedicated field:**
- **Embed as descriptive contrast in the body:** "modern dark grey laminate office desk, NOT wooden, NOT rustic" beats listing `wood, rustic` in a separate `--no` field
- **Trailing avoid clause:** end the prompt with a short `Avoid: [comma-separated]` line in plain English — MJ respects this as natural-language guidance even though it isn't a formal flag
- **Positive anchor first, negative second:** every "don't render X" should pair with "DO render Y" in the same sentence — pure prohibition without a positive replacement leaves MJ free to drift

## ⚠ Document framing patterns — text must be INVISIBLE (LOCKED 2026-05-05)

Adrian 2026-05-05: *"we need to move a bit further away from being able to see text on documents, its either zoomed out a bit more or blurry"*. MJ v7 cannot render legible English under ~12 chars consistently. Even at "barely readable" framing, MJ drifts to gibberish that breaks the doc-forensics trust signal. So every doc-forensics prompt picks ONE of two safe patterns.

**Pattern 1 — Zoomed-out / wider framing:** top-down "desk overview" at 3+ ft / 1m+, document covers ~30-50% of frame. Text becomes texture, not content. Pen, mug, phone, lamp, calc share the frame as environment.
- ✅ "top-down wide on a charcoal melamine desk, contract paper covers 30% of frame, calculator + pen + smart key fob + coffee mug sharing the surface, environmental still, 35mm Summicron lens"
- ❌ "top-down close-up on a contract clause" — text becomes focal subject, MJ generates gibberish

**Pattern 2 — Shallow DOF blur:** macro/close-up with extreme shallow depth of field. IN-FOCUS subject is hand / pen tip / calculator buttons / smart key fob — text is in foreground or background blur.
- ✅ "extreme shallow depth of field, hand resting on calculator buttons, display soft-blurred glow in foreground, contract paper visible but text dissolved in DOF"
- ✅ "macro on pen tip touching paper, paper text blurred to texture in soft background blur, Hasselblad 500CM medium format aesthetic"
- ❌ "macro on contract showing 'INTEREST RATE' and signature line in sharp focus" — text in focus = MJ-text-failure

**Banned framings (never compose):**
- Tight macro where document text occupies >25% of frame in sharp focus
- Calculator display readable + in focus
- Hand pointing at / circling a specific word as focal subject
- "Reading distance" (~30cm) composition where viewer's eye lands on the text

**Mandatory `Avoid:` additions for any text-bearing surface** (paper, contract, brochure, calculator, sticker, screen, key tag):
```
legible text, readable text, sharp focus on document text, text as focal subject, reading-distance composition, text in focus, words on paper visible
```

### Plate handling — same logic, applied to number plates (LOCKED 2026-05-05)

Adrian 2026-05-05: *"same goes for any text like number plates, maybe prompts cars to have no number plates or just blank black number plate"*. Two safe prompt patterns for any vehicle prompt where a plate would be in frame. **Never request "AU plate" generically** — MJ butchers the characters every time.

**Pattern A — No plate at all:** explicitly prompt the car without a plate. Compose the angle so the absence reads naturally.
- Phrasing: `vehicle without front number plate, plate frame empty, no registration plate visible`
- Best angles: front three-quarter with plate area in shadow, profile, rear-on with plate cropped out of frame

**Pattern B — Blank black plate:** prompt the plate as a solid feature with NO characters. MJ renders a clean rectangle instead of gibberish letters.
- Phrasing: `blank matte black rectangular registration plate, no characters, no numbers, no letters, no text, solid plate face`
- Use this when plate-shape silhouette IS the AU-anchor signal (372×134mm rectangle vs US-square ratio carries the AU read; the absence of text means nothing to butcher)

**Mandatory `Avoid:` additions for any vehicle prompt with a plate in frame:**
```
visible plate text, plate characters, plate numbers, plate letters, AU plate text, state name on plate, registration text, gibberish text on plate
```

### Key fob handling — same logic, applied to button symbols (LOCKED 2026-05-05 PM)

Adrian 2026-05-05 PM: *"for keys, the symbols are all messed up, we need to prompts keys to look modern but have no symbols on them"*. Modern smart-proximity fob buttons normally carry tiny icons (lock-arrow, unlock-arrow, trunk, panic siren). MJ butchers those icons the same way it butchers text — they render as gibberish symbols that break the modern-fob trust signal. Fix: prompt the fob with **blank featureless buttons** and let the body shape carry the "smart key" read.

**Locked positive phrasing for any key visual:**
```
modern proximity smart key fob, rounded matte black plastic body with integrated chrome trim accent, four blank rectangular soft-touch buttons with NO symbols / NO icons / NO labels visible, smooth featureless button faces, small valet-blade slot, current Toyota or Ford Ranger key fob design language, recessed manufacturer logo silhouette only
```

**Mandatory `Avoid:` additions for any key visual:**
```
lock icon on button, unlock icon, trunk icon, panic icon, button symbols, button icons, gibberish symbols on key fob, manufacturer wordmark on key, brand name visible on fob, text on key fob, embossed labels on buttons, novelty keychain, oversized keyring with multiple keys
```

**The trio — documents + plates + fob buttons all obey the same doctrine.** Three small-text surfaces MJ can't render cleanly, three application patterns, one underlying rule: don't ask MJ to render small text or symbols. Compose for the absence (blank, blurred, or zoomed-out) and let shape/composition/atmosphere carry the meaning.

**Reference (full doctrine):** `.claude/rules/design-system-audm.md` §§ Document framing lock + Plate handling lock + Key style lock · memory `feedback_audm_mj_documents_text_invisible_2026-05-05.md` + `feedback_audm_mj_modernity_aftercare_keys_2026-05-05.md`.

## Locked parameter recipe — Discord (kept for reference)

```
--style raw --v 7 --ar 16:9 --s 80 --chaos 0 --sref [PALETTE_SWATCH_URL] --sw 200 --no text, watermark, logo, signature, typography, words, letters, captions, brand names, dealership signs, cartoon, illustration, 3D render, CGI, plastic skin, hyperdetailed
```

**Why each param:**
- `--style raw` — **mandatory.** Bypasses MJ beautification. Without it every shot drifts to "luxury car ad."
- `--v 7` — locked. Don't mix versions across a video set.
- `--ar 16:9` — landscape AUDM B-roll. Use `9:16` only for vertical Shorts cutdowns.
- `--s 80` — stylize 50-150 = documentary realism. 250+ = product ad. 400+ = full hallucination.
- `--chaos 0` — keep low for AUDM. Higher chaos breaks palette+composition consistency across the video's 8-12 image set.
- `--sref [PALETTE_SWATCH_URL]` — point to the AUDM palette swatch (build once, host permanently — see § Palette swatch below).
- `--sw 200` — style weight. 500+ is too dominant. 0 ignores. 180-250 is the sweet spot.
- `--no [block-list]` — negative prompt covers text bleed, watermarks, AI-style flags.

**Parameters to AVOID:**
- `--weird` — antithesis of doc realism
- `--cref` — **deprecated in v7.** Returns error or silently ignored. Use `--oref` for character ref.
- `--p 0` only if your personalization profile is wrong; otherwise complete the rating once with cinematic doc images and leave it on.

---

## Build the AUDM palette swatch (one-time, then reuse forever)

**Palette LOCKED per [.claude/rules/design-system-audm.md](../../../.claude/rules/design-system-audm.md):**
- `#2B2B2B` (top — Charcoal)
- `#F5EFE6` (middle — Cream)
- `#D17A3D` (bottom — Outback Orange)

**Build:** `python3 generator/au-dealer-math/generate-palette-swatch.py` — emits the 1024×1024 PNG with no text.

**File:** `content/au-dealer-math/saas-prompts/_assets/audm-palette-swatch.png` ✅ (built 2026-05-01)

**To use as MJ sref:**
1. Upload the swatch to Imgur (or any permanent CDN — NOT Discord, those URLs expire).
2. Lock the URL in `content/au-dealer-math/saas-prompts/_assets/palette-swatch-url.txt`.
3. In MJ web: drop the URL into the Style Reference field (or upload the PNG directly — MJ web hosts it).
4. Use that URL/upload as `--sref` (or web-equivalent) in every AUDM MidJourney prompt.

**Earlier palette (deprecated 2026-05-01):** `#FAF7F2` cream + `#C8612C` orange. Channel banner + logo + watermark all ship with the locked colors above, so the older swatch was out of sync. Don't use the old hexes.

---

## Style anchors that pull toward cinema verité (NOT luxury ad)

**Photographers (use 1, max 2 per prompt):**
- `Alec Soth photography style` — quiet, observational (closest to AUDM outback feel)
- `Joel Sternfeld` — banal documentary
- `Stephen Shore` — 1970s American color doc
- `Robert Frank` — grit
- `Wim Wenders cinematography` — German road-movie melancholy that maps to outback

**Lighting only (not full style anchors):**
- `Roger Deakins cinematography` (lighting reference only — full anchor is overused)
- `Emmanuel Lubezki natural light`

**Film stocks (always include one):**
- `shot on Kodak Portra 400` — default
- `Kodak Tri-X 400 black and white` — B&W documentary fallback
- `Fujifilm Pro 400H` — neutral
- `Cinestill 800T` — tungsten night/dusk

**Camera bodies (anchor realism):**
- `Leica M6`, `Hasselblad 500CM`, `35mm Leica street photography`
- DON'T say `DSLR` — pulls toward stock photography

**Lens/grain language:**
- `35mm Summicron lens`, `medium format`, `subtle film grain`, `natural light`, `available light only`

---

## Banned phrases (pull toward luxury ad / stock product)

`professional`, `commercial photography`, `advertisement`, `studio lighting`, `4K UHD`, `octane render`, `Unreal Engine`, `hyperdetailed`, `8K`, `cinematic` (paradoxically — too generic; replace with named cinematographer), `epic`, `masterpiece`, `beautiful lighting`, `dramatic`

---

## Office desk standard (LOCKED 2026-04-29)

**AUDM dealership desks are office desks, NEVER wood/rustic/workshop.** First V1 batch had 50% drift to wood-desk / workshop-bench because "charcoal office desk" alone didn't lock the surface — MJ pulls hard toward "manila binder + worn wood desk + ceramic mug" rustic priors.

**Locked phrasing for ANY desk-involving prompt:** `modern dark grey laminate office desk` (preferred) or `charcoal melamine executive desk surface` (alternative).

**Add to negative prompt for ALL desk shots:**
```
--no wood texture, wooden desk, rustic, workshop, toolboxes, garage bench, farmhouse, vintage cabin, knotted wood, ceramic mug
```

Need positive (modern laminate) AND negative (wood / workshop / rustic mug props) to cancel both directional priors.

## Diagram language (LOCKED 2026-04-29)

**MJ takes "branching tree diagram" literally as a botanical tree.** Locked phrasing for ANY flowchart/schematic prompt:

- ✅ Use: `"stylized flowchart with arrows splitting from a central node"`, `"schematic flow diagram with three connected boxes"`, `"hand-drawn process diagram with arrows"`
- ❌ Avoid: `"branching tree diagram"`, `"tree of nodes"`, `"network diagram"` — all pull toward botanical/organic tree

**Add to negative prompt for diagram shots:** `--no botanical tree, plant, branches, leaves, organic tree`

---

## Five validated AUDM prompt examples

(All append the locked tail from above. Paste the body below + the tail.)

### 1. Hands across desk (no faces — Scene 3 budget question)

```
Documentary photograph, two pairs of hands across a dealership negotiation desk, 
salesperson hand holding pen pointing to contract, customer hands clasped 
uncertain, shallow depth of field, natural window light, Alec Soth style, 
Kodak Portra 400, 35mm Leica, faceless composition cropped at chest, charcoal 
cream and burnt orange palette, palette: #2B2B2B #FAF7F2 #C8612C, limited 
palette only [LOCKED-TAIL]
```

### 2. Open training binder with diagram (Scene 3 — Road to a Sale)

```
Cinema verité photograph, open vinyl-bound dealer training binder on a worn 
desk, a simple hand-drawn finance flow diagram visible on the page with clean 
linework, single overhead practical light, Stephen Shore style, Hasselblad 
500CM medium format, slight film grain, paper grain visible, charcoal cream 
and burnt orange tones, palette: #2B2B2B #FAF7F2 #C8612C, limited palette 
only [LOCKED-TAIL]
```

### 3. Split-screen 4yr vs 7yr loan stacks (Scene 4 hero)

```
Studio still life documentary photograph, two stacks of contract paper side 
by side on slate surface, left stack shorter labeled with a tab marker, right 
stack noticeably taller with same tab marker, dramatic chiaroscuro single 
light source, Joel Sternfeld style, Kodak Portra 400, sharp realistic paper 
grain, charcoal cream and burnt orange accents, palette: #2B2B2B #FAF7F2 
#C8612C, limited palette only [LOCKED-TAIL]
```

### 4. Luxury sedan with replacement-cycle implication (Scene 4 GFV reveal)

```
Documentary photograph, late-model dark sedan parked alone at dusk in front 
of dealership pre-delivery shed, identical car visible in background through 
open shed door, Wim Wenders cinematography, Cinestill 800T, melancholy outback 
Australian dusk light, charcoal sky cream wall and one orange sodium streetlight, 
palette: #2B2B2B #FAF7F2 #C8612C, limited palette only [LOCKED-TAIL]
```

### 5. Three-tier document chiaroscuro reveal (Scene 5 holdback — FLAGSHIP REVEAL)

```
Studio documentary photograph, three documents fanned in stepped tiers on 
dark slate, dramatic single-source light from left, deep shadow falloff right, 
paper grain and slight crease visible, Robert Frank documentary style, 
Hasselblad medium format, charcoal cream and burnt orange accent on a single 
tab, palette: #2B2B2B #FAF7F2 #C8612C, limited palette only [LOCKED-TAIL]
```

---

## V2+ Macca mascot integration via `--oref`

**Setup (one-time after Fiverr delivery):**
1. Receive Macca character ref sheet from Fiverr (multiple poses, neutral background)
2. Pick the **single best front-facing reference** image
3. Host on permanent CDN (NOT Discord)
4. Lock the URL in `brand/audm/macca-poses/macca-oref-url.txt`

**Per-prompt usage from V2 onwards:**

```
[scene description WITHOUT describing Macca's face/clothes — only what he's doing and where]
[locked AUDM tail]
--oref [MACCA-REF-URL] --ow 100
```

**`--ow` (omni weight) tuning:**
- `--ow 100` — default; balanced fidelity + scene flexibility
- `--ow 200-400` — bump if Macca starts drifting between shots
- `--ow 50-80` — drop if scenes feel too static (more pose variety)
- `--ow 800+` — avoid; overfits, breaks composition

**Cost note:** `--oref` doubles GPU cost per render. Budget for it. A 12-shot Macca-heavy video = ~24 GPU-shots equivalent.

**Known limitation:** `--oref` locks face/hair tightly but is loose on outfit colors. Reinforce Macca's outfit palette in text every prompt.

---

## Failure modes + mitigations

| Symptom | Cause | Fix |
|---|---|---|
| Output looks like luxury car ad / stock | `--style raw` missing or generic words ("professional/cinematic") in prompt | Add `--style raw`, replace generic words with named photographer + film stock |
| Palette comes out wrong / drifts mid-batch | No `--sref` palette swatch OR swatch URL changed | Lock the swatch URL once, use everywhere |
| Composition breaks across 8-12 image set | `--chaos > 10` or `--p` profile too strong | Drop chaos to 0, optionally `--p 0` for neutral baseline |
| Macca drifts between V2 shots | `--ow 100` too low for character lock | Bump to 200-300 |
| Hallucinated text on documents | Negative prompt missing relevant terms | Add to `--no`: `text, watermark, logo, signature, typography, words, letters, captions` |
| Outfit colors drift on Macca shots | `--oref` doesn't lock outfit | Reinforce in prompt body: "Macca wearing his locked navy work shirt and grey trousers" |

---

## Validated patterns log

- *(append validated patterns after each render batch)*
- 2026-04-29: not yet used for AUDM. Existing AUDM stills are NB Pro, not Midjourney. First MJ batch: V1 expanded production (12 NB + 6 MJ planned per `v01-production-master.md`).

---

## Sources

- [Midjourney Version docs](https://docs.midjourney.com/hc/en-us/articles/32199405667853-Version)
- [Midjourney Parameter List docs](https://docs.midjourney.com/hc/en-us/articles/32859204029709-Parameter-List)
- [Midjourney Style Reference --sref docs](https://docs.midjourney.com/hc/en-us/articles/32180011136653-Style-Reference)
- [Midjourney Omni Reference --oref docs](https://docs.midjourney.com/hc/en-us/articles/36285124473997-Omni-Reference)
- [Midjourney --no parameter docs](https://docs.midjourney.com/hc/en-us/articles/32173351982093-No)
- [V7 is now the default model](https://updates.midjourney.com/v7-is-now-the-default-model/)
- [Midjourney V7 in 2026: What Changed for Builders](https://dev.to/evan-dong/midjourney-v7-in-2026-what-actually-changed-for-builders-1lga)
- [Midjourney Cinematic Realism 2026 Blueprint](https://promptsera.com/midjourney-prompts-cinematic-realism/)
- [V7 cref vs oref incompatibility](https://flowith.io/blog/midjourney-v7-consistent-characters-masterclass/)
- [How to get specific colors in Midjourney V7](https://www.cometapi.com/how-to-get-specific-colors-in-midjourney-v7/)
- [Style Reference for photographers (Midlibrary)](https://midlibrary.io/midguide/midjourney-style-reference-sref-for-photographers)
- [Alec Soth Midjourney style (Midlibrary)](https://midlibrary.io/styles/alec-soth)
