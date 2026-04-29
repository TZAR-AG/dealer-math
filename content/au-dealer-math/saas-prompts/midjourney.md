# Midjourney — AUDM canonical prompt reference

**Engine:** Midjourney v7 (default since 17 June 2025). V8 alpha exists but isn't stable — stay on v7.
**Tier:** Standard $46 AUD/mo per `saas-stack.md`.
**Use AUDM for:** photo-realistic close-ups (documents, products, cinematic detail), V2+ Macca mascot consistency via `--oref`.
**Use NB Pro instead for:** dealership scene establishment, multi-asset still life, faster iteration.

---

## Locked parameter recipe (paste-ready tail)

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

1. Create a 1024×1024 PNG with three flat horizontal bars: `#2B2B2B` (top), `#FAF7F2` (middle), `#C8612C` (bottom). NO text.
2. Host on Imgur or any permanent CDN (NOT Discord — Discord URLs expire).
3. Lock the URL in `content/au-dealer-math/saas-prompts/_assets/palette-swatch-url.txt`.
4. Use that URL as `--sref` in every AUDM Midjourney prompt.

**File:** `content/au-dealer-math/saas-prompts/_assets/audm-palette-swatch.png` (TODO — build this once)

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
