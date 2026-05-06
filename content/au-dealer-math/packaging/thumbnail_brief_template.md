# Thumbnail Brief Template

**Use:** every new AUDM thumbnail. Fill out below before opening Photopea.

---

## Brief — V[N] · [Video working title]

### 1. Pairing mode lock (REQUIRED — pick before anything else)

- [ ] **A** — Title teases / Thumb explains (default · ~50% of uploads)
- [ ] **B** — Thumb teases / Title explains (counterintuitive · ~25%)
- [ ] **C** — Reinforce (search-intent · ~15%)
- [ ] **D** — Tension / Contrast (rare · ≤10%)

### 2. Locked title

```
[paste exact title shipped]
```

Char count: __ / 62 max
Psychology triggers stacked (per [reference_audm_title_formula](C:/Users/adria/.claude/projects/c--dev-Claude/memory/reference_audm_title_formula_2026-05-04.md)): __ / 5
- [ ] Loss aversion · [ ] Self-implication · [ ] Specificity · [ ] Identity activation · [ ] Curiosity gap with stakes

### 3. Template pick (one of 5)

- [ ] **A — Circled Clue** (forensic close-up + ONE orange hand-circle)
- [ ] **B — Number on Document** (single-figure reveal)
- [ ] **C — Split-Frame Transition** (PolyMatter-derived before/after)
- [ ] **D — Stamped Overlay** (rubber-stamp on contract)
- [ ] **E — Annotated Cheatsheet** (Wendover-derived pointer-tags)

### 4. The 9-question checklist (REQUIRED)

| # | Question | Answer |
|---|---|---|
| 1 | Core viewer DESIRE | |
| 2 | Core viewer FEAR | |
| 3 | Core curiosity gap | |
| 4 | Title role | tease / explain / reinforce / contradict |
| 5 | Thumbnail role | tease / explain / reinforce / contradict |
| 6 | Emotional trigger | loss aversion / status / identity / fear / greed / mystery |
| 7 | Visual trigger | circle / underline / split / number / stamp / pointer |
| 8 | Reason to click NOW | |
| 9 | Non-redundancy check | What's on the THUMB that's NOT in the TITLE? __ |

If question 9 is "nothing" — the thumbnail isn't ready. Rebuild.

### 5. Composition spec

**Focal element (the ONE thing the eye lands on):**
- [ ] document close-up · [ ] number · [ ] split-frame · [ ] stamp · [ ] cheatsheet fragment · [ ] hand+pen · [ ] other: __

**Supporting element (max ONE):**
- [ ] pen tip · [ ] calculator surface · [ ] pointer-tag · [ ] secondary text · [ ] none

**Text overlay:**
- Main: "______" (max 3-5 words, DM Sans Bold, ≥120pt at 1280×720)
- Secondary tag (optional): "______" (max 2 words, DM Sans Bold, ~60pt)
- Color: cream `#F5EFE6` on charcoal · OR · charcoal `#2B2B2B` on cream
- Position: left-third · right-third · top-third · bottom-third (NEVER bottom-380px on the 1080×1920 video itself per [feedback_ig_safe_zone_caption_position](C:/Users/adria/.claude/projects/c--dev-Claude/memory/feedback_ig_safe_zone_caption_position.md), but for thumbnails 1280×720 use any third)

### 6. Color discipline check

- [ ] Charcoal `#2B2B2B` background OR cream `#F5EFE6` document surface
- [ ] Outback orange `#D17A3D` ONE accent only (highlight / stamp / pointer / circle / number)
- [ ] Zero red, yellow, lime, neon
- [ ] Three-color discipline (charcoal + cream + orange — no fourth)

### 7. MJ prompt + composition (if generating)

```
[paste MJ v7 prompt — must include text-failure-pool exclusions per design-system-audm.md]
```

Prompt anchors used:
- [ ] Photographer style anchor: __
- [ ] Film stock: __ (default Kodak Portra 400)
- [ ] Camera body: __ (default Leica M6)
- [ ] Avoid clause: __

### 8. Anti-pattern check (NONE of these)

- [ ] No human face
- [ ] No yellow / red / lime accent
- [ ] No defamation language ("SCAM", "FRAUD", "LYING", "RIP-OFF", "EXPOSED")
- [ ] No title-duplicate text on thumbnail
- [ ] No all-caps screaming with exclamation marks
- [ ] No more than 6 words on the thumbnail
- [ ] No legible text on contract/document/plate (per text-failure-pool rule)

### 9. Mobile preview test (REQUIRED before locking)

- [ ] Exported at 1280×720, opened in [ThumbnailTest mobile preview](https://thumbnailtest.com/preview)
- [ ] Visual story reads at 200×112 px
- [ ] Text legible at 200×112 px
- [ ] Foveal singularity holds (one element wins the eye)
- [ ] Phone-in-hand check at arm's length: still reads

### 10. Scorecard pass (REQUIRED before upload)

Go to [packaging_scorecard.md](packaging_scorecard.md). Score the package across all 10 categories. Pass thresholds:
- [ ] Average ≥7/10
- [ ] Every category ≥6/10

If any category <6: rebuild that element before shipping. No exceptions.

---

## Composition rules — fast reference

### Visual hierarchy (mandatory)

Three layers max, in this order:
1. **Focal element** (primary subject) — wins the eye in <0.5s
2. **Supporting element** (max ONE) — adds context after eye lands
3. **Text overlay** (3-5 words max) — final layer, doesn't compete

If you have 4+ elements, cut something.

### Mobile readability rules

- Test at **200×112 px** (the actual mobile feed thumbnail size)
- Main text ≥120pt at 1280×720 base resolution
- Subject occupies ≥30% of frame
- 3:1 minimum contrast ratio between text and background
- No information critical to comprehension below 50% of frame height (mobile UI may overlay)

### Text rules

- DM Sans Bold (or DM Sans Black for hero phrases) — never serif, never decorative
- Sentence case OR single-word ALL CAPS for emphasis (NOT both)
- 3-5 words MAX
- One color (cream OR charcoal — NOT mixed within same overlay)
- One size hierarchy (one hero size + one supporting size — NOT 3+ sizes)
- No exclamation marks, no question marks, no emojis

### Color/contrast rules

- 3-color discipline: charcoal + cream + outback orange. Period.
- Outback orange used ONCE per thumbnail as accent
- Charcoal as either dominant background OR text color (not both unless cream is the buffer)
- Cream as document surface OR text color
- Hard contrast (charcoal/cream pair) carries the visual; orange punctuates

### Background rules

- Document surface (cream paper) OR charcoal desk surface
- Avoid: photorealistic stock backgrounds, gradients with multiple colors, busy textures
- Allow: subtle paper grain, subtle film grain, soft DOF blur on supporting elements
- For MJ-generated backgrounds: lock to documentary realism per [content/au-dealer-math/saas-prompts/midjourney.md](content/au-dealer-math/saas-prompts/midjourney.md)

### Object/symbol rules

**Approved AUDM symbol library:**
- Contracts (cream paper on charcoal desk)
- Calculators (button surface only — display NOT in focus per text-failure rule)
- Pens (fountain pen, ballpoint — entering frame from edge)
- Hands (silhouette / partial — never full hand)
- Smart-key fobs (modern, BLANK buttons per design-system-audm.md update)
- Late-model utes (Hilux N80/N90, Land Cruiser 300, Ranger Next-Gen — see § Vehicle modernity lock)
- AU plate-shape silhouettes (no plate text)
- Tinted-window glass panels
- F&I office desk with computer monitor showing abstract data-viz
- Coffee stain / pen mark / drop of liquid (metaphor only — implied damage)
- Stop sign / yield sign / caution tape (metaphor props)
- Stamps ("DEALER COST", "MARKUP", "NOT NEGOTIABLE", "STAY SILENT")

**BANNED symbols:**
- Faces / facial features
- US plates / US banknotes / US dealership signage
- Vintage cars / pre-2020 model years
- Cartoon / illustration / 3D render
- Stock-photo handshakes / smiling people

---

## QC checklist (before upload)

Run through every item:

- [ ] Pairing mode locked (A / B / C / D)
- [ ] Title locked, char count ≤62, ≥4/5 psychology triggers
- [ ] Template picked (A / B / C / D / E)
- [ ] 9-question checklist filled
- [ ] Non-redundancy check passed (Q9 = something specific, not "nothing")
- [ ] Composition spec defined (focal + supporting + text)
- [ ] Color discipline holds (3-color, ONE orange accent)
- [ ] MJ prompt includes text-failure-pool exclusions (if MJ-generated)
- [ ] Anti-pattern check (NONE of the 7 violations)
- [ ] Mobile preview tested at 200×112 px
- [ ] Scorecard passed (≥7 avg, ≥6 every category)
- [ ] Phone-in-hand arm's-length check
- [ ] Thumbnail file saved to `content/au-dealer-math/scripts/v0X-renders/thumbnails/v0X-thumb-v1.png` (or v2, v3 for variants)
- [ ] Logged to [video_packaging_database_template.csv](video_packaging_database_template.csv)

---

## Common mistakes (avoid these)

1. **Title-duplicate text overlay** — V1 + V2 disease. Thumbnail text MUST add a second curiosity layer.
2. **Multi-line text walls** — V1 had 5 stacked lines. Mobile-feed-killer. Max 3-5 words.
3. **Tiny focal element** — V2's orange circle was microscopic. Focal element ≥30% of frame.
4. **Background-as-decoration** — V2's contract was too dim. Either it's the focal element (sharp + lit) or it's not in the thumbnail.
5. **Drift between modes** — starting with Mode A intent, ending with Mode C execution. Lock the mode at brief stage.
6. **Stock-aesthetic temptation** — handshakes, dealer-floor stock photos, smiling salespeople. Off-brand. Use MJ-generated documentary realism.
7. **Skipping mobile preview** — desktop-Photopea looks great, mobile-feed dies. Test before upload.

---

## Filed-with

- [packaging_scorecard.md](packaging_scorecard.md) — scoring gate
- [title_thumbnail_pairing_framework.md](title_thumbnail_pairing_framework.md) — pairing mode picker
- [competitor_swipe_file.md](competitor_swipe_file.md) — visual references + 5 templates
- [.claude/rules/design-system-audm.md](.claude/rules/design-system-audm.md) — visual constraints
- [content/au-dealer-math/saas-prompts/midjourney.md](content/au-dealer-math/saas-prompts/midjourney.md) — MJ v7 prompt invariants
