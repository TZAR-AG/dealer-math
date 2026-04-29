# Nano Banana Pro — AUDM canonical prompt reference

**Engine:** Google Gemini 3 Pro Image (via Artlist).
**Cost:** ~700 credits per 4K render (~$1.23 AUD); ~half for 2K.
**Aspect ratio:** set in Artlist UI dropdown (16:9 for AUDM B-roll). Prompt mention is redundant insurance.
**Use AUDM for:** AU dealership scenes, paper/document close-ups, product hero shots, anchor scene establishment.

---

## Prompt skeleton (Google's official 5-part order, AUDM-tuned)

```
[SUBJECT — physical description, materials, surface, what's in frame]
+ [ACTION/STATE — what is happening, even if static]
+ [LOCATION — specific AU dealership context, time of day, season]
+ [COMPOSITION — angle, framing, focal length, depth of field]
+ [STYLE — film stock, photographer/era anchors, color grade]
+ [CONSTRAINTS — palette hex codes with % weighting, faceless lock, text suppression]
```

**Six rules of thumb:**

1. **Front-load the physical subject.** "A black anodised aluminium calculator on slate" beats "Cinematic shot of a calculator." Stops the model latching onto the genre prior.
2. **Hex codes work** (Max Woolf empirical Dec 2025). Pair with named anchor: `"a palette of charcoal #2B2B2B (60%), cream #FAF7F2 (30%), and outback orange #C8612C accents (10%)"`.
3. **% weighting controls dominance.** Without it the three colors distribute evenly.
4. **Negation = positive framing, not "no".** Google explicitly says "empty street" beats "no cars". Negative prompt fields are deprecated in Imagen/Gemini 3.
5. **Repeat the most-load-bearing constraint twice in different words.** Faceless lock especially.
6. **16:9 in UI** + insurance mention in prompt: `"16:9 landscape, cinematic widescreen, no letterboxing"`.

---

## Brand-locked phrases (carry across every AUDM NB prompt)

**Palette block (paste at end of every prompt):**
```
limited palette: charcoal #2B2B2B (60% — dominant), cream #FAF7F2 (30% — surfaces, paper), outback orange #C8612C (10% — single accent only). No other colors. Desaturated overall, muted, documentary color grade.
```

**Faceless lock (triple-redundant):**
```
unpopulated scene, no figures, no people, no human silhouettes, no reflections of people in glass or chrome surfaces. Empty dealership.
```

**Text suppression (when needed):**
```
no text, no typography, no readable words, no letters, no logos, no brand names, no captions
```

**Light:**
```
low warm Australian afternoon sun raking from upper-left, long oblique shadows, ~16:00 light angle
```

**Style anchors that pull toward documentary cinema (NOT generic stock):**
- `Kodak Portra 400, 35mm` — default; warm tones, organic grain, lifted shadows
- `CineStill 800T` — tungsten balance, halation around lights — for dealership-at-dusk + showroom interiors
- `Fujifilm X-T4 with 23mm f/2` — neutral documentary realism
- `Leica M6, Tri-X 400` — B&W documentary fallback (use sparingly)

**Photographer/era anchors:**
- `Alec Soth American documentary photography` — quiet, observational, banal-as-cinematic (default)
- `Stephen Shore color documentary, 1970s vernacular` — flat noon-affect, banal sublime
- `Trent Parke Magnum Australia, harsh contrast, suburban realism` — AU-specific, hard light
- `Wim Wenders road photography, late afternoon, geometric` — wide cinematic framing

---

## Banned phrases (pull toward iStock / Pinterest / wellness)

These pull NB toward the aesthetic AUDM is positioned against. Avoid all:

`professional`, `corporate`, `business`, `high quality`, `4K masterpiece`, `happy`, `smiling`, `team`, `diverse group`, `beautiful`, `stunning`, `amazing`, `epic`, `cinematic` (too generic — replace with named cinematographer), `cozy`, `warm and inviting`, `welcoming`, `studio lighting`, `white background`, `commercial photography`, `octane render`, `unreal engine`, `hyperdetailed`, `8K`, `Wes Anderson` (pulls pastel symmetry), `Roger Deakins` (overused stylistically), `shot on iPhone` (flattens look)

Also avoid implicit human cues even when banned: `car salesman`, `customer`, `buyer`, `salesperson` — even with negation, increases figure-hallucination risk in glass/chrome reflections.

---

## Five validated AUDM prompt examples

### 1. AU dealership floor wide shot

```
A wide empty AU automotive dealership showroom interior, polished concrete floor, 
two SUVs and one ute parked in geometric arrangement, large floor-to-ceiling 
windows on the left wall, manufacturer banners overhead but text illegible/blurred. 
Shot at 4pm — low warm Australian afternoon sun raking from upper-left, long 
oblique shadows across the floor, dust motes visible in light shafts. Single 
overhead fluorescent panel cool-bleed mixing with warm window light. 24mm 
wide-angle, low eye-level, deep depth of field, single-point perspective receding 
to back wall. Kodak Portra 400 35mm film aesthetic, organic grain, lifted shadows. 
In the style of Stephen Shore American color documentary and Trent Parke Australian 
suburban realism. Limited palette: charcoal #2B2B2B (60%), cream #FAF7F2 (30%), 
outback orange #C8612C (10% — only on a single rebate banner edge). Unpopulated, 
no figures, no people, no reflections of people in glass. 16:9 cinematic widescreen.
```

### 2. Open training binder on a desk (Road to a Sale)

```
An open three-ring training binder lying flat on a worn cream laminate desk, 
visible spiral binding, dog-eared printed pages with faint typewriter-style 
content (text intentionally blurred/illegible), a charcoal ballpoint pen resting 
diagonally across the right page, a chipped ceramic mug at upper-right edge. 
Top-down 90-degree angle, slight 5-degree tilt, shallow depth of field f/2.8 
focused on the binding. Late afternoon window light raking from upper-left, 
single high oblique shadow from the pen. Documentary close-up, in the style of 
Alec Soth quiet observational photography. Kodak Portra 400 35mm, organic grain, 
muted tones. Limited palette: charcoal #2B2B2B, cream #FAF7F2, with a single 
outback orange #C8612C plastic tab on the binder edge. No legible text, no 
typography, no logos, no figures. 16:9 landscape.
```

### 3. Stack of loan papers (4yr vs 7yr split)

```
A stack of approximately twelve printed A4 loan contract papers slightly fanned 
on a charcoal slate desk surface, top sheet partially curled, a black metal 
calculator partially visible at the upper-right edge, a single outback orange 
#C8612C paper clip on the top sheet. Printed content on papers blurred/illegible 
— rows of grey horizontal lines suggesting text, faint table grids, no readable 
words. Three-quarter overhead angle 60 degrees, shallow depth of field, 50mm lens. 
Low warm late-afternoon sun raking from upper-left, paper edges glowing slightly, 
deep shadow falling to lower-right. Documentary still life, CineStill 800T 
aesthetic, halation in highlights. Limited palette: charcoal #2B2B2B (60%), 
cream #FAF7F2 (30%), outback orange #C8612C (10%). Unpopulated, no figures, no 
hands, no faces, no readable text. 16:9 widescreen.
```

### 4. Black product bottle on slate (paint protection hero)

```
A matte black anodised aluminium product bottle standing upright on a charcoal 
slate surface, single small outback orange #C8612C debossed mark on the lower 
front, condensation beading on the upper third. Centered composition, 35mm 
medium shot, eye-level slightly above the cap, shallow depth of field f/2 with 
sharp focus on the bottle face. Single high warm key light from upper-left, 
soft falloff to the right, no fill — strong chiaroscuro. Cream #FAF7F2 fabric 
backdrop, slightly out of focus. Editorial product documentary in the style of 
Wim Wenders still photography, Kodak Portra 400 35mm grain. Limited palette: 
charcoal #2B2B2B (70%), cream #FAF7F2 (25%), outback orange #C8612C (5% — 
single small mark only). Unpopulated, no figures, no reflections of people. 
16:9 landscape.
```

### 5. Manufacturer rebate cash stack

```
A loose stack of approximately twenty AU $100 banknotes (face design intentionally 
blurred/illegible to avoid currency reproduction), partially fanned on a worn 
cream manila folder labelled with an unreadable scrawl, a single outback orange 
#C8612C rubber band lying beside the stack, a black ballpoint pen at the lower-left 
edge. Three-quarter overhead angle 70 degrees, shallow depth of field f/2.8 focused 
on the topmost note edge, 50mm lens. Low warm late-afternoon sun raking from 
upper-left, hard oblique shadows, slight halation around bright surfaces. Documentary 
still life in the style of Stephen Shore American color photography and Alec Soth 
quiet observation. CineStill 800T aesthetic, organic grain, muted tones, dealer-desk 
realism. Limited palette: charcoal #2B2B2B (50%), cream #FAF7F2 (40%), outback 
orange #C8612C (10%). Unpopulated, no figures, no hands, no faces, no readable 
text on banknotes or folder. 16:9 widescreen.
```

---

## Failure modes + mitigations

| Symptom | Cause | Fix |
|---|---|---|
| Renders look like generic stock photo | Too many "professional/corporate/cinematic" generic words | Replace with named photographer + film stock anchors |
| Figures bleed into glass/chrome reflections | Faceless lock missing reflection clause | Add `"no reflections of people in glass or chrome surfaces"` |
| Palette comes out evenly distributed (mint/beige drift) | No % weighting on palette | Add 60/30/10 weighting + "single accent only" |
| Hallucinated text on documents/signage | Negation not phrased correctly | Use positive framing: `"text intentionally blurred/illegible, rows of grey horizontal lines"` |
| Pulls toward editorial wellness aesthetic | Cuyana/Aesop/Intelligent Change anchors active | Drop those — use Alec Soth/Stephen Shore/Trent Parke instead |
| iPad/screen content scribbled abstractly | NB cannot render legible screens | Render screen OFF + Canva-composite real content on top |
| Subject melts/distorts | Style anchors fighting subject (book-on-cream prior with non-book subject) | Front-load subject FIRST, push style to end |

---

## Edit feature warning

NB's edit feature costs **another 700 credits per edit** (full re-generation, not true inpaint). Never use for small fixes. Use Canva or Photopea for region-specific touch-ups.

---

## Validated patterns log

- 2026-04-29: 6 V1 stills (still-1 through still-5 + still-kling-clip-1-input) generated successfully on AUDM aesthetic. 2912x1632 native (above 1080p). Aspect handled in Artlist UI.
- *(append validated patterns after each render batch)*

---

## Sources

- [Google Cloud — Ultimate prompting guide for Nano Banana](https://cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-nano-banana)
- [Google Blog — Nano Banana Pro prompting tips](https://blog.google/products-and-platforms/products/gemini/prompting-tips-nano-banana-pro/)
- [Atlabs — Ultimate Nano Banana Pro Prompting Guide 2026](https://www.atlabs.ai/blog/the-ultimate-nano-banana-pro-prompting-guide-mastering-gemini-3-pro-image)
- [Max Woolf — Nano Banana Pro empirical review (Dec 2025)](https://minimaxir.com/2025/12/nano-banana-pro/)
- [Artlist — How to use Nano Banana Pro](https://artlist.io/blog/nano-banana-prompts/)
- [Chase Jarvis — Adding film grain with Nano Banana Pro](https://chasejarvis.com/blog/how-to-add-film-grain-with-nano-banana-pro-3-methods/)
