# V3 Thumbnail Brief — The Aftercare Room

**Script:** [v03-the-aftercare-room.md](v03-the-aftercare-room.md)
**Title (locked):** *"The $1,800 Pitch in the Room Most Buyers Forget"*
**Output:** `content/au-dealer-math/scripts/v03-thumbnail.png` (1280×720, ~900KB)
**Builder:** `generator/au-dealer-math/build-thumbnail.py`
**Per-video text inputs (pre-locked in `reference_audm_thumbnail_spec_2026-05-01.md`):**
- Hero: **`DON'T BUY`**
- Stack: **`THE PAINT`** / **`PROTECTION`**

---

## Template selection

**Pick: Document Forensics**

Reasoning: V3's load-bearing visual is a contract / invoice with paint protection as a line item. Document Forensics is the highest-leverage template for this topic because the visual answer to the title's curiosity gap (*"the room most buyers forget"*) lives literally on the contract. The thumbnail's job is to render that one line item with an outback-orange accent stroke and let the headline carry the verdict.

Big-Number Reveal was considered (the $1,800 figure could anchor the visual) but rejected per the spec rule *"NO dollar reveal text — title carries the dollar shock; thumbnail carries the curiosity gap. Photo + question = scroll-stopper."* The dollar already lives in the title. The thumbnail must NOT duplicate it.

Comparison Split was considered (e.g. dealer plan vs independent detailer side-by-side) but rejected as too complex for thumbnail-feed legibility on mobile at small size.

---

## MJ photo backdrop — the prompt

Per `reference_audm_thumbnail_spec_2026-05-01.md` § "MJ photo backdrop":
- Subject right-weighted (right two-thirds of frame)
- Left third of frame in deep shadow as negative space (text overlay zone)
- Settings: 16:9 / Style Raw / Stylize 80 / Chaos 0 / v7 (palette swatch sref left empty per `feedback_audm_mj_swatch_too_literal_2026-05-03.md`)

**Prompt (paste into MJ web):**

```
Studio documentary photograph, polished dark grey laminate office desk surface, modern fit-out, matte finish, no wood grain, single cream-coloured invoice page positioned in the right two-thirds of the frame, one printed line item highlighted with a thick outback-orange marker stroke, line text behind in soft DOF blur f/1.4 aperture (atmospheric only, not legible), pen tip resting at the highlight, paper grain visible only on the highlighted line, the LEFT THIRD of the frame in deep shadow as negative space with the desk surface fading to near-black, dramatic single-source side-light from frame right, deep shadow falloff to frame left, Robert Frank documentary style, Hasselblad 500CM medium format, shot on Kodak Portra 400, subtle film grain, natural light, faceless composition, charcoal cream and outback orange palette, palette: #2B2B2B #F5EFE6 #D17A3D, limited palette only
```

**Negative prompt (paste into Exclude field):**
```
text, watermark, logo, signature, typography, words, letters, captions, brand names, dealership signs, cartoon, illustration, 3D render, CGI, plastic skin, hyperdetailed, wood texture, wooden desk, rustic, workshop, toolboxes, garage bench, farmhouse, vintage cabin, knotted wood, ceramic mug, manila folder, bright background, evenly-lit
```

**Generate 4 variants → pick the one where:**
- Left third truly recedes to deep shadow (not just dim — must feel like negative space)
- Highlighted invoice line sits in the right half, sharp and reading as paint-protection-style line item
- No legible text bleeding through MJ's gibberish (any visible text MUST be in DOF blur)
- Charcoal/cream/outback-orange palette holding — no drift to wood/warm-tone

**Upscale: Subtle** (NOT Creative). Save to `c:/dev/Claude/content/au-dealer-math/scripts/v03-thumbnail-mj.png`.

---

## PIL composite (run after MJ render lands)

Per `generator/au-dealer-math/build-thumbnail.py` (parametric, V2-V12 ready):

```bash
cd c:/dev/Claude/generator/au-dealer-math
python build-thumbnail.py \
  c:/dev/Claude/content/au-dealer-math/scripts/v03-thumbnail-mj.png \
  "DON'T BUY" \
  "THE PAINT" \
  "PROTECTION" \
  c:/dev/Claude/content/au-dealer-math/scripts/v03-thumbnail.png
```

Or via Python:

```python
from build_thumbnail import render
render(
  mj_image='c:/dev/Claude/content/au-dealer-math/scripts/v03-thumbnail-mj.png',
  hero_word="DON'T BUY",
  stack_words=['THE PAINT', 'PROTECTION'],
  output_path='c:/dev/Claude/content/au-dealer-math/scripts/v03-thumbnail.png'
)
```

**The builder applies (per locked V2-V12 spec):**
- Slot-based vertical layout — hero gets 1.3× share, stack words get equal shares
- Each word vertically centred in its slot, 92% slot fill
- Hero in **outback orange `#D17A3D`** (DM Sans Bold)
- Stack in **cream `#F5EFE6`** (DM Sans Bold)
- Left-side darkening gradient (the MJ negative-space zone)
- Subtle vignette
- Film grain pass

**Output:** 1280×720 PNG ready to upload to YouTube.

---

## Acceptance criteria (verify before YT upload)

- [ ] Hero word `DON'T BUY` clearly readable on mobile-feed thumbnail at small size (~120×68px)
- [ ] Stack words `THE PAINT` / `PROTECTION` cleanly stacked with no descender/ascender overlap (slot allocation should guarantee this — verify in the rendered output)
- [ ] Outback orange hero word is the strongest visual element after the photo subject
- [ ] No text in the right two-thirds (text only in the left negative-space zone)
- [ ] Photo subject (highlighted invoice line + pen tip) is sharp on the right, recognizable at small size
- [ ] No accidental text legibility from MJ in the photo (verify by squinting at the thumbnail)
- [ ] Charcoal / cream / outback orange palette holds — no drift to off-brand tones
- [ ] No AU pill (channel name carries geo-anchor)
- [ ] No dollar figure on thumbnail (title carries it)

---

## Integration with title

When the user sees this thumbnail in their YouTube feed alongside the title:

> Thumbnail (visual): faceless invoice with one line outback-orange-highlighted + pen tip + headline `DON'T BUY THE PAINT PROTECTION`
> Title (text below thumbnail): *The $1,800 Pitch in the Room Most Buyers Forget*

The two pieces work together:
- **Title = WHAT** ($1,800 pitch in a room you forgot existed) — the curiosity stake
- **Thumbnail = ANSWER** (don't buy the paint protection) — the verdict
- **Combined effect:** title creates the "what room? what pitch?" question, thumbnail tells you *the answer is "don't buy the paint protection"* — but the click is to learn *why*, *what makes it different from independent*, *what the actual margin is*

This is the strongest title+thumbnail combo of V1-V3 because the thumbnail commits to a clear verdict (the buyer-side action) rather than just teasing.

---

## Reference

- Spec: `reference_audm_thumbnail_spec_2026-05-01.md`
- Builder: `generator/au-dealer-math/build-thumbnail.py`
- Title formula: `reference_audm_title_formula_2026-05-04.md`
- MJ prompt rules: `content/au-dealer-math/saas-prompts/midjourney.md`
