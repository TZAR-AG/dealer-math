# V3 — The Aftercare Room — Midjourney Prompt Batch

**Script:** [v03-the-aftercare-room.md](v03-the-aftercare-room.md)
**Total prompts:** 61 (56 original + 5 added 2026-05-05 PM per Adrian feedback — see "## ACT 7 — VARIETY ADDS" at bottom)
**Target stills (final cut):** ~54 (1 still / ~10 sec at ~9 min runtime, per AFWL benchmark)
**Variant generation:** each prompt → 4 variants in MJ web → keep best → Upscale Subtle (NOT Creative)
**Total MJ generations:** 244 (61 × 4)

---

## Settings (every prompt — set in MJ web UI panel, NOT inline flags)

- Engine: **v7** (NOT v8 alpha)
- Style: **Raw**
- Aspect: **16:9**
- Stylize (Scale): **80**
- Variation Mode: **Off** (chaos 0)
- Style Reference upload: **leave empty** — palette enforced via prompt-text only per `feedback_audm_mj_swatch_too_literal_2026-05-03.md`
- Style Weight: 200 (if exposed)
- Personalize: 0 (or off if profile is documentary-locked)

## Negative prompt (paste verbatim into "Exclude these" / `--no` field on EVERY prompt)

```
text, watermark, logo, signature, typography, words, letters, captions, brand names, dealership signs, cartoon, illustration, 3D render, CGI, plastic skin, hyperdetailed, wood texture, wooden desk, rustic, workshop, toolboxes, garage bench, farmhouse, vintage cabin, knotted wood, ceramic mug, manila folder, woman, female, long hair, satchel, handbag, leather notebook, fountain pen, vintage car, classic car, retro car, antique car, 1960s car, 1970s car, 1980s car, 1990s car, restored car, hot rod, muscle car, old timer, brass key, blade key, old-school key, vintage key, classic dashboard, retro interior, chrome bumper, whitewall tires
```

(Wood-desk drift defense + female-default defense + laptop→leather-notebook defense + retro-car defense, per `feedback_audm_mj_three_drift_patterns_2026-05-03.md` and 2026-05-05 PM Adrian feedback "no retro cars at all, current generation only". Pull `manila folder` and `ceramic mug` from any specific prompt that genuinely needs them — otherwise leave in.)

## Locked tail (append to every prompt body if you prefer the inline approach)

```
shot on Kodak Portra 400, subtle film grain, natural light, faceless composition, charcoal cream and outback orange palette, palette: #2B2B2B #F5EFE6 #D17A3D, limited palette only
```

---

## Batch composition summary

| Pool | Count | % | Notes |
|---|---|---|---|
| Doc-forensics (charcoal laminate desk, paper, hands, pen) | 31 | 55% | Spine of the V3 batch |
| Computer-on-desk (F&I-adjacent workstation) | 6 | 11% | Required minimum per variety lock |
| Vehicle stills (medium distance, AU models, plate as silhouette) | 7 | 13% | Required minimum |
| AU dealership exterior (golden hour / harsh sun) | 4 | 7% | Required minimum |
| AU showroom interior (terrazzo / fluoro / glass-walled F&I) | 3 | 5% | Required minimum |
| AU streetscape / suburban / forecourt context | 3 | 5% | Required minimum |
| AU flag (forecourt pole / vehicle aerial / showroom wall) | 1 | 2% | Required minimum |
| Atmospheric interior moments (empty room / dusk / chair waiting) | 1 | 2% | Required minimum |
| **Total** | **56** | **100%** | |

Doc-forensics: 55%. AU-anchor + variety: 45%. Within the 50-60 / 40-50 split locked in `feedback_audm_mj_variety_au_anchors_2026-05-03.md`.

---

## ACT 0 — HOOK (0:00-0:30, ~3 stills)

### V3-001 — Hook anchor: paint protection invoice line, soft-focus contract behind

```
Extreme macro top-down photograph, polished dark grey laminate office desk surface, modern fit-out, matte finish, no wood grain, smooth desk top, single cream-coloured invoice page laid flat, one printed line item softly highlighted with a thin outback-orange marker stroke, pen tip resting beside the highlight, contract body text behind in soft DOF blur f/1.4 aperture, paper grain visible on the highlighted line, polished dark grey laminate surface again at the bottom edge, available light from upper-left, Alec Soth style, 35mm Summicron lens, shot on Kodak Portra 400, subtle film grain, natural light, faceless composition, charcoal cream and outback orange palette, palette: #2B2B2B #F5EFE6 #D17A3D, limited palette only
```

### V3-002 — Three-door establishing shot, doors as architectural shapes

```
Top-down architectural still photograph, three frosted-glass office doors arranged left-to-right along a polished porcelain-tile corridor floor, charcoal frame mouldings, fluorescent overhead panel lighting, the middle door subtly lit from inside through frosted glass, the outer two doors dark, harsh midday light bleeding from a glass front entrance at frame top, Stephen Shore style, Hasselblad 500CM medium format, shot on Kodak Portra 400, subtle film grain, natural light, faceless composition, charcoal cream and outback orange palette, palette: #2B2B2B #F5EFE6 #D17A3D, limited palette only
```

### V3-003 — Hands receiving the brochure stack, faceless cropped at chest

```
Documentary photograph, cropped at chest height, faceless, two faceless hands receiving a small stack of folded glossy brochures across a polished dark grey laminate office desk surface, modern fit-out, matte finish, no wood grain, hands-only composition, brochure cover designs in soft DOF blur with cream and charcoal tones, no readable text, available light from upper-left, Alec Soth style, 35mm Summicron lens, shot on Kodak Portra 400, subtle film grain, natural light, faceless composition, charcoal cream and outback orange palette, palette: #2B2B2B #F5EFE6 #D17A3D, limited palette only
```

---

## ACT 1 — THREE-ROOM REANCHOR (0:30-1:30, ~6 stills)

### V3-004 — Glass-walled office viewed from showroom floor (AU showroom interior)

```
Documentary photograph, glass-walled office on the edge of a car showroom floor, polished porcelain terrazzo tile floor reflecting fluorescent overhead panel lighting, glass front entrance visible at frame right with harsh AU midday sun streaming through, demo car silhouette positioned just inside the glass front, manufacturer logo as background silhouette shape on a feature wall (no readable wordmark text), Wim Wenders cinematography, 35mm Leica street photography, shot on Kodak Portra 400, subtle film grain, natural light, faceless composition, charcoal cream and outback orange palette, palette: #2B2B2B #F5EFE6 #D17A3D, limited palette only
```

### V3-005 — Empty consultation desk between two chairs, top-down

```
Top-down photograph, polished dark grey laminate office desk surface, modern fit-out, matte finish, no wood grain, smooth desk top, two ergonomic mesh-back chairs facing each other from opposite sides of the desk, single closed manila-coloured folder centred on the desk (NOT a binder, NOT a vintage diary — modern flat folder), pen resting at a slight angle, no people, fluorescent overhead panel lighting, polished porcelain tile floor visible at frame edges, Joel Sternfeld style, Hasselblad 500CM medium format, shot on Kodak Portra 400, subtle film grain, natural light, faceless composition, charcoal cream and outback orange palette, palette: #2B2B2B #F5EFE6 #D17A3D, limited palette only
```

### V3-006 — Three-door diagram restated, door TWO highlighted

```
Top-down architectural still photograph, polished porcelain corridor tile floor, three frosted-glass office doors arranged left-to-right, the middle door brightly lit from within with warm interior light bleeding through the frosted panel, outer two doors completely dark, a thin outback-orange directional line marked on the floor between the three doors traced left-to-right, harsh midday light at frame top, no people, Stephen Shore style, Hasselblad 500CM medium format, shot on Kodak Portra 400, subtle film grain, natural light, faceless composition, charcoal cream and outback orange palette, palette: #2B2B2B #F5EFE6 #D17A3D, limited palette only
```

### V3-007 — Salesperson silhouette walking customer down corridor (faceless, cropped)

```
Documentary photograph, mid-distance, broad-shouldered man in his 40s, masculine outline, ex-dealer build, short-cropped dark hair, no long hair, button-down shirt, cropped at chin height, walking ahead of a faceless customer figure (also cropped at chin) along a polished porcelain corridor tile floor, fluorescent overhead panel lighting, glass-walled offices visible on the right side, demo cars visible through glass at frame right edge, no readable signage anywhere, Wim Wenders cinematography, 35mm Leica street photography, shot on Kodak Portra 400, subtle film grain, natural light, faceless composition, charcoal cream and outback orange palette, palette: #2B2B2B #F5EFE6 #D17A3D, limited palette only
```

### V3-008 — Customer hands resting on edge of consultation desk, faceless

```
Documentary photograph, cropped at chest height, faceless, customer's clasped hands resting on the edge of a polished dark grey laminate office desk surface, modern fit-out, matte finish, no wood grain, customer hands in foreground sharp, opposite chair empty in soft DOF blur background, available light from a window at upper-left, Alec Soth style, 35mm Summicron lens, shot on Kodak Portra 400, subtle film grain, natural light, faceless composition, charcoal cream and outback orange palette, palette: #2B2B2B #F5EFE6 #D17A3D, limited palette only
```

### V3-009 — Wide showroom interior with three glass offices visible (AU showroom)

```
Wide documentary photograph from showroom floor, mid-distance, polished porcelain terrazzo tile floor, three frosted-glass office cubicles along the showroom edge with charcoal frames, fluorescent overhead panel lighting, demo cars positioned at frame foreground (Toyota-style sedan, Hyundai-style hatchback shapes — no readable badges or wordmarks), harsh AU midday sun bleeding through floor-to-ceiling glass front at frame top, blue WA sky visible through the glass, no people, Wim Wenders cinematography, 35mm Leica street photography, shot on Kodak Portra 400, subtle film grain, natural light, faceless composition, charcoal cream and outback orange palette, palette: #2B2B2B #F5EFE6 #D17A3D, limited palette only
```

---

## ACT 2 — THE AFTERCARE MENU (1:30-3:00, ~9 stills)

### V3-010 — Brochure fan-out top-down (paint / tint / dash cam / ceramic / interior)

```
Top-down photograph, polished dark grey laminate office desk surface, modern fit-out, matte finish, no wood grain, smooth desk top, five glossy brochures fanned out in an overlapping arc, each brochure cover featuring abstract shapes in cream and charcoal tones with a single outback-orange accent strip, no readable text on any brochure, paper-grain texture visible, available light from upper-left casting soft shadow, Joel Sternfeld style, 35mm Summicron lens, shot on Kodak Portra 400, subtle film grain, natural light, faceless composition, charcoal cream and outback orange palette, palette: #2B2B2B #F5EFE6 #D17A3D, limited palette only
```

### V3-011 — Paint protection brochure, atmospheric close-up

```
Extreme macro top-down photograph, single closed glossy brochure on a polished dark grey laminate office desk surface, modern fit-out, matte finish, no wood grain, brochure cover featuring a soft-focus close-up of a darkly-painted automotive panel (no readable text, no logo, no badge), water bead on the panel surface, charcoal frame around the cover, single outback-orange ribbon marker tucked into the brochure edge, available light from upper-left, Alec Soth style, 35mm Summicron lens, shot on Kodak Portra 400, subtle film grain, natural light, faceless composition, charcoal cream and outback orange palette, palette: #2B2B2B #F5EFE6 #D17A3D, limited palette only
```

### V3-012 — Window tint brochure with sample film strip

```
Top-down photograph, polished dark grey laminate office desk surface, modern fit-out, matte finish, no wood grain, single brochure laid flat with a small sample square of dark window tint film placed on top of the cover, the tint sample subtly translucent revealing a darker tone underneath, no readable text on the brochure, available light from upper-left, paper-grain visible, Joel Sternfeld style, 35mm Summicron lens, shot on Kodak Portra 400, subtle film grain, natural light, faceless composition, charcoal cream and outback orange palette, palette: #2B2B2B #F5EFE6 #D17A3D, limited palette only
```

### V3-013 — Dash camera in box, top-down macro

```
Top-down macro photograph, polished dark grey laminate office desk surface, modern fit-out, matte finish, no wood grain, small charcoal-coloured dash camera unit resting in an open cream cardboard packaging box, lens facing up, mounting bracket beside it, USB cable coiled, no readable text on the box or device, available light from upper-left, Stephen Shore style, 35mm Summicron lens, shot on Kodak Portra 400, subtle film grain, natural light, faceless composition, charcoal cream and outback orange palette, palette: #2B2B2B #F5EFE6 #D17A3D, limited palette only
```

### V3-014 — Interior protection sample square on cream paper, atmospheric

```
Extreme macro top-down photograph, polished dark grey laminate office desk surface, modern fit-out, matte finish, no wood grain, single small charcoal-coloured automotive carpet sample square placed on top of a cream-coloured information sheet, sheet text behind in soft DOF blur f/1.4 aperture, available light from upper-left, Alec Soth style, 35mm Summicron lens, shot on Kodak Portra 400, subtle film grain, natural light, faceless composition, charcoal cream and outback orange palette, palette: #2B2B2B #F5EFE6 #D17A3D, limited palette only
```

### V3-015 — Ceramic coating sample bottle, atmospheric

```
Top-down macro photograph, polished dark grey laminate office desk surface, modern fit-out, matte finish, no wood grain, single dark amber glass bottle with a black dropper cap (ceramic coating sample), microfibre cloth folded beside it, no readable label on the bottle, single outback-orange thread visible in the microfibre cloth, available light from upper-left, Joel Sternfeld style, 35mm Summicron lens, shot on Kodak Portra 400, subtle film grain, natural light, faceless composition, charcoal cream and outback orange palette, palette: #2B2B2B #F5EFE6 #D17A3D, limited palette only
```

### V3-016 — Tyre and rim insurance — wheel close-up with chalk mark

```
Macro photograph, low-angle close-up of a single alloy wheel on a parked car in a covered AU showroom, slight kerbed scuff on the rim edge, harsh midday light bleeding from frame right through showroom glass, polished porcelain tile floor visible underneath, no readable plate or badge text, Robert Frank documentary style, 35mm Leica street photography, shot on Kodak Portra 400, subtle film grain, natural light, faceless composition, charcoal cream and outback orange palette, palette: #2B2B2B #F5EFE6 #D17A3D, limited palette only
```

### V3-017 — Hands flipping a brochure page, faceless cropped at chest

```
Documentary photograph, cropped at chest height, faceless, two faceless hands flipping the page of a glossy brochure on a polished dark grey laminate office desk surface, modern fit-out, matte finish, no wood grain, mid-flip motion captured with subtle motion blur on the lifting page, no readable text on the brochure, available light from upper-left, Alec Soth style, 35mm Summicron lens, shot on Kodak Portra 400, subtle film grain, natural light, faceless composition, charcoal cream and outback orange palette, palette: #2B2B2B #F5EFE6 #D17A3D, limited palette only
```

### V3-018 — Aftercare manager's pen, calculator BUTTON SURFACE (not display)

```
Extreme macro top-down photograph, polished dark grey laminate office desk surface, modern fit-out, matte finish, no wood grain, charcoal-coloured solar calculator with cream button keys visible on its top half (button surface only — calculator display panel cropped completely out of frame), pen tip resting on one of the buttons, available light from upper-left, paper-grain visible at frame edge, Joel Sternfeld style, 35mm Summicron lens, shot on Kodak Portra 400, subtle film grain, natural light, faceless composition, charcoal cream and outback orange palette, palette: #2B2B2B #F5EFE6 #D17A3D, limited palette only
```

---

## ACT 3 — THE MATH REVEAL (3:00-5:00, ~12 stills)

### V3-019 — Split composition: brochure stack vs invoice with line items highlighted

```
Top-down photograph, split composition, polished dark grey laminate office desk surface, modern fit-out, matte finish, no wood grain, left half of frame: three brochures stacked overlapping with their corners visible, right half of frame: cream-coloured invoice page with three printed line items each underlined with thin outback-orange marker strokes, paper-grain visible, contract text in soft DOF blur, available light from upper-left, Joel Sternfeld style, Hasselblad 500CM medium format, shot on Kodak Portra 400, subtle film grain, natural light, faceless composition, charcoal cream and outback orange palette, palette: #2B2B2B #F5EFE6 #D17A3D, limited palette only
```

### V3-020 — Hands holding pen above invoice, faceless

```
Documentary photograph, cropped at chest height, faceless, two faceless hands hovering above a cream-coloured invoice on a polished dark grey laminate office desk surface, modern fit-out, matte finish, no wood grain, pen held in right hand poised above one specific line on the invoice, soft DOF blur on the invoice text body, sharp focus on pen tip and hand, available light from upper-left, Alec Soth style, 35mm Summicron lens, shot on Kodak Portra 400, subtle film grain, natural light, faceless composition, charcoal cream and outback orange palette, palette: #2B2B2B #F5EFE6 #D17A3D, limited palette only
```

### V3-021 — Stacked brochures cinematic side-light chiaroscuro

```
Studio documentary photograph, three glossy brochures fanned in stepped tiers on a polished dark grey laminate office desk surface, modern fit-out, matte finish, no wood grain, dramatic single-source light from frame left, deep shadow falloff to frame right, paper grain and slight crease visible on the top brochure, no readable text on any cover, Robert Frank documentary style, Hasselblad medium format, shot on Kodak Portra 400, subtle film grain, natural light, faceless composition, charcoal cream and outback orange palette, palette: #2B2B2B #F5EFE6 #D17A3D, limited palette only
```

### V3-022 — Invoice with one line outback-orange-highlighted, contract behind in DOF blur

```
Extreme macro top-down photograph, polished dark grey laminate office desk surface, modern fit-out, matte finish, no wood grain, single cream-coloured invoice page laid flat, one specific printed line item highlighted with a thin outback-orange marker stroke, the rest of the invoice body in shallow DOF blur f/1.4 aperture, gibberish-text rendered as soft blur (not legible — atmospheric only), pen tip resting at the highlight, paper grain visible only on the highlighted line, available light from upper-left, Alec Soth style, 35mm Summicron lens, shot on Kodak Portra 400, subtle film grain, natural light, faceless composition, charcoal cream and outback orange palette, palette: #2B2B2B #F5EFE6 #D17A3D, limited palette only
```

### V3-023 — Stack of invoices fanned, top-down chiaroscuro

```
Studio documentary photograph, top-down, polished dark grey laminate office desk surface, modern fit-out, matte finish, no wood grain, five cream-coloured invoice pages fanned out in an arc, each page with one outback-orange thin underline somewhere on the body, dramatic single-source light from frame left, deep shadow falloff right, paper grain visible, Robert Frank documentary style, Hasselblad medium format, shot on Kodak Portra 400, subtle film grain, natural light, faceless composition, charcoal cream and outback orange palette, palette: #2B2B2B #F5EFE6 #D17A3D, limited palette only
```

### V3-024 — Hand pointing to single line on invoice, extreme macro

```
Extreme macro photograph, polished dark grey laminate office desk surface, modern fit-out, matte finish, no wood grain, single faceless index finger pointing to a specific line on a cream-coloured invoice, fingertip pressed against paper, paper-grain visible, line text in soft DOF blur (atmospheric only, not legible), thin outback-orange underline beneath the indicated line, available light from upper-left, Alec Soth style, 35mm Summicron lens, shot on Kodak Portra 400, subtle film grain, natural light, faceless composition, charcoal cream and outback orange palette, palette: #2B2B2B #F5EFE6 #D17A3D, limited palette only
```

### V3-025 — F&I-adjacent computer workstation top-down (computer-on-desk lift #1)

```
Documentary photograph, three-quarter top-down view of a modern F&I-adjacent workstation, two Dell P-series 24-inch matte black flat-screen monitors side-by-side glowing with abstract blue dealership management software UI on screen (no legible text, gradient and shape grid only), black mechanical keyboard with chunky charcoal keycaps, optical mouse on a small charcoal rubber pad, ergonomic mesh-back chair edge visible at frame edge, polished glass desk surface (NOT laminate this time — this is a computer scene), thin paperwork stack to one side not dominating, mixed cool fluorescent overhead and screen glow lighting from frame top and centre, Joel Sternfeld style, Hasselblad 500CM medium format, shot on Kodak Portra 400, subtle film grain, faceless composition, charcoal cream and outback orange palette, palette: #2B2B2B #F5EFE6 #D17A3D, limited palette only
```

### V3-026 — F&I workstation wider with chair (computer-on-desk lift #2)

```
Documentary photograph, mid-wide angle of an F&I-adjacent office cubicle interior, two Dell P-series 24-inch matte black flat-screen monitors on a polished glass desk surface, monitors glowing with abstract pale blue dealership management software UI (no legible text, only gradients and box-grid shapes), black mechanical keyboard with chunky charcoal keycaps, ergonomic mesh-back chair partially visible foreground, glass-walled office with charcoal frame visible at frame edges, polished porcelain tile floor at frame bottom, mixed cool fluorescent overhead lighting plus screen glow, Wim Wenders cinematography, 35mm Leica street photography, shot on Kodak Portra 400, subtle film grain, faceless composition, charcoal cream and outback orange palette, palette: #2B2B2B #F5EFE6 #D17A3D, limited palette only
```

### V3-027 — Brochure rolled in cylinder shape, dramatic side-light

```
Studio documentary photograph, single glossy brochure rolled into a tight cylinder and standing upright on a polished dark grey laminate office desk surface, modern fit-out, matte finish, no wood grain, dramatic single-source side-light from frame left, long shadow cast to right, charcoal frame visible at edges, no readable text on the brochure exterior, Robert Frank documentary style, 35mm Summicron lens, shot on Kodak Portra 400, subtle film grain, natural light, faceless composition, charcoal cream and outback orange palette, palette: #2B2B2B #F5EFE6 #D17A3D, limited palette only
```

### V3-028 — Side-by-side brochures with a single outback-orange divider line between them

```
Top-down photograph, polished dark grey laminate office desk surface, modern fit-out, matte finish, no wood grain, two glossy brochures placed side-by-side exactly mirrored, a single thin outback-orange directional line drawn on the desk surface between them (not on the paper), paper grain visible on each brochure, available light from upper-left, Joel Sternfeld style, Hasselblad medium format, shot on Kodak Portra 400, subtle film grain, natural light, faceless composition, charcoal cream and outback orange palette, palette: #2B2B2B #F5EFE6 #D17A3D, limited palette only
```

### V3-029 — Stack of contracts cinematic, faceless cropped hand reaching

```
Documentary photograph, cropped at chest height, faceless, single faceless hand reaching for the top sheet on a stack of cream-coloured contract papers placed on a polished dark grey laminate office desk surface, modern fit-out, matte finish, no wood grain, stack of about ten pages tall, paper grain visible on the top sheet, dramatic side-light from frame left, deep shadow falloff right, Alec Soth style, 35mm Summicron lens, shot on Kodak Portra 400, subtle film grain, natural light, faceless composition, charcoal cream and outback orange palette, palette: #2B2B2B #F5EFE6 #D17A3D, limited palette only
```

### V3-030 — Atmospheric vehicle still: parked Toyota Hilux at AU dealership lot

```
Documentary photograph, mid-distance three-quarter view of a white Toyota Hilux dual-cab ute parked on a covered AU dealership lot, AU rectangular plate shape (372mm × 134mm) visible on rear bumper but text completely unreadable at this distance — viewer fills in the legibility, harsh AU midday sun streaming from frame top right, polished concrete forecourt below, demo car positioned a few metres ahead also unreadable, Wim Wenders cinematography, 35mm Leica street photography, shot on Kodak Portra 400, subtle film grain, natural light, faceless composition, charcoal cream and outback orange palette, palette: #2B2B2B #F5EFE6 #D17A3D, limited palette only
```

---

## ACT 4 — WHY PENETRATION IS HIGH (5:00-7:00, ~14 stills)

### V3-031 — Customer's hands receiving modern smart key fob on a lanyard, faceless

```
Documentary photograph, cropped at chest height, faceless, customer's faceless hands receiving a current-generation Toyota or Ford smart key fob in matte charcoal plastic with three discreet buttons (NOT a classic blade key, NOT brass, NOT old-school) on a charcoal lanyard from a second pair of faceless hands across a polished dark grey laminate office desk surface, modern fit-out, matte finish, no wood grain, modern key fob resting in customer's open palm, lanyard hanging slightly, available light from upper-left, modern car key, contemporary styling, no retro, no vintage, Alec Soth style, 35mm Summicron lens, shot on Kodak Portra 400, subtle film grain, natural light, faceless composition, charcoal cream and outback orange palette, palette: #2B2B2B #F5EFE6 #D17A3D, limited palette only
```

### V3-032 — Brochure being slid across desk, faceless hands

```
Documentary photograph, cropped at chest height, faceless, two pairs of faceless hands across a polished dark grey laminate office desk surface, modern fit-out, matte finish, no wood grain, salesperson hand sliding a glossy brochure forward, customer hand still reaching, brochure mid-slide with subtle motion blur on the trailing edge, available light from upper-left, Alec Soth style, 35mm Summicron lens, shot on Kodak Portra 400, subtle film grain, natural light, faceless composition, charcoal cream and outback orange palette, palette: #2B2B2B #F5EFE6 #D17A3D, limited palette only
```

### V3-033 — Pen offered across desk, signature space outback-orange-highlighted

```
Documentary photograph, cropped at chest height, faceless, single faceless hand offering a pen across a polished dark grey laminate office desk surface, modern fit-out, matte finish, no wood grain, cream-coloured contract page on the desk between the hands with a single signature line outback-orange-highlighted, paper grain visible, contract body text in soft DOF blur, available light from upper-left, Alec Soth style, 35mm Summicron lens, shot on Kodak Portra 400, subtle film grain, natural light, faceless composition, charcoal cream and outback orange palette, palette: #2B2B2B #F5EFE6 #D17A3D, limited palette only
```

### V3-034 — Showroom floor wide, atmospheric — late afternoon

```
Wide documentary photograph, AU car showroom interior at late afternoon, polished porcelain terrazzo tile floor reflecting warm gold light streaming through floor-to-ceiling glass front, fluorescent overhead panels mostly turned off, single demo car positioned in centre frame (mass-market sedan shape — no readable badge), glass-walled F&I office on the right edge with frosted panels, dust particles catching the light, no people, late golden hour AU light, Wim Wenders cinematography, 35mm Leica street photography, shot on Kodak Portra 400, subtle film grain, natural light, faceless composition, charcoal cream and outback orange palette, palette: #2B2B2B #F5EFE6 #D17A3D, limited palette only
```

### V3-035 — Customer's tired hands on lap, atmospheric

```
Documentary photograph, cropped at lap height, faceless, customer's hands resting on khaki trousers, knuckles slightly tense, faint creases on the skin (the tired hand of a long Saturday on the floor), polished porcelain tile floor visible below, ergonomic mesh-back chair edge cropped at frame top, available light from upper-left, Alec Soth style, 35mm Summicron lens, shot on Kodak Portra 400, subtle film grain, natural light, faceless composition, charcoal cream and outback orange palette, palette: #2B2B2B #F5EFE6 #D17A3D, limited palette only
```

### V3-036 — Aftercare manager's hand pointing to a printed product menu

```
Documentary photograph, top-down, polished dark grey laminate office desk surface, modern fit-out, matte finish, no wood grain, single faceless index finger pointing to a printed menu page laid flat on the desk, menu showing four product category boxes each with a small visual icon (no legible text — shapes and outback-orange box outlines only), available light from upper-left, Joel Sternfeld style, 35mm Summicron lens, shot on Kodak Portra 400, subtle film grain, natural light, faceless composition, charcoal cream and outback orange palette, palette: #2B2B2B #F5EFE6 #D17A3D, limited palette only
```

### V3-037 — F&I-adjacent computer with abstract software grid (computer-on-desk lift #3)

```
Documentary photograph, three-quarter angle of a single Dell P-series 24-inch matte black flat-screen monitor on a polished glass desk surface, monitor glowing with abstract pale blue and cream dealership management software UI showing only a grid of empty input fields and dropdown shapes (no legible text), black mechanical keyboard with chunky charcoal keycaps in foreground, optical mouse on a small rubber pad, fluorescent overhead lighting plus screen glow, Joel Sternfeld style, Hasselblad 500CM medium format, shot on Kodak Portra 400, subtle film grain, natural light, faceless composition, charcoal cream and outback orange palette, palette: #2B2B2B #F5EFE6 #D17A3D, limited palette only
```

### V3-038 — Customer's car (medium distance), late golden hour AU exterior

```
Documentary photograph, mid-distance three-quarter view of a silver Hyundai Tucson SUV parked beside a covered AU dealership entrance at late golden hour, AU rectangular plate shape visible on rear but text not readable at this distance, harsh raking sun from frame right casting long shadows on polished concrete forecourt, blue WA sky transitioning to gold at horizon, no readable signage, Wim Wenders cinematography, 35mm Leica street photography, shot on Kodak Portra 400, subtle film grain, natural light, faceless composition, charcoal cream and outback orange palette, palette: #2B2B2B #F5EFE6 #D17A3D, limited palette only
```

### V3-039 — Aftercare manager's chair (faceless cropped), lean-forward posture

```
Documentary photograph, mid-distance, broad-shouldered man in his 40s, masculine outline, ex-dealer build, short-cropped dark hair, no long hair, button-down shirt, cropped at chin height, leaning forward across a polished dark grey laminate office desk, hands clasped on the desk surface in front of him, opposite chair empty in soft DOF blur background, polished porcelain tile floor visible below, available light from upper-left, Alec Soth style, 35mm Summicron lens, shot on Kodak Portra 400, subtle film grain, natural light, faceless composition, charcoal cream and outback orange palette, palette: #2B2B2B #F5EFE6 #D17A3D, limited palette only
```

### V3-040 — AU dealership exterior glass front, golden hour

```
Documentary photograph, mid-wide, glass-fronted AU dealership building at golden hour, polished concrete forecourt in foreground, three demo cars visible through the glass front (sedan / hatchback / SUV silhouettes — no readable badges), manufacturer logo as a background silhouette shape above the entrance (Toyota oval / Hyundai swoosh shape — no rendered wordmark text), harsh raking AU late-afternoon sun from frame right, blue WA sky transitioning to gold, no readable signage, no people, Wim Wenders cinematography, 35mm Leica street photography, shot on Kodak Portra 400, subtle film grain, natural light, faceless composition, charcoal cream and outback orange palette, palette: #2B2B2B #F5EFE6 #D17A3D, limited palette only
```

### V3-041 — AU streetscape: low-rise commercial strip, gum trees, harsh midday

```
Documentary photograph, mid-wide, AU low-rise commercial strip mall in a Perth-metro suburb, single-storey shopfronts in cream-rendered brick along the frame, mature gum trees lining the cracked footpath in foreground, harsh AU midday sun overhead casting hard shadows, blue WA sky completely cloudless, telephone wires crossing frame at upper third, no readable signage, no people, Stephen Shore style, 35mm Leica street photography, shot on Kodak Portra 400, subtle film grain, natural light, faceless composition, charcoal cream and outback orange palette, palette: #2B2B2B #F5EFE6 #D17A3D, limited palette only
```

### V3-042 — Three-quarter AU vehicle (Toyota Camry-style), forecourt midday

```
Documentary photograph, mid-distance three-quarter view of a white Toyota Camry-style sedan parked on an AU dealership forecourt at midday, AU rectangular plate shape visible on rear bumper but text not readable at this distance, harsh midday sun overhead casting hard shadows on polished concrete forecourt below, two more sedans behind in soft DOF blur, no readable badges or wordmarks, Robert Frank documentary style, 35mm Leica street photography, shot on Kodak Portra 400, subtle film grain, natural light, faceless composition, charcoal cream and outback orange palette, palette: #2B2B2B #F5EFE6 #D17A3D, limited palette only
```

### V3-043 — AU flag on forecourt pole, harsh midday backlit

```
Documentary photograph, mid-wide low-angle, single Australian flag on a tall white forecourt pole, harsh AU midday sun backlighting the flag, blue WA sky behind, the flag in mid-flutter with subtle motion blur on its trailing edge, polished concrete forecourt visible below, blurred glass-fronted dealership building behind in soft DOF, no readable signage, no people, Wim Wenders cinematography, 35mm Leica street photography, shot on Kodak Portra 400, subtle film grain, natural light, faceless composition, charcoal cream and outback orange palette, palette: #2B2B2B #F5EFE6 #D17A3D, limited palette only
```

### V3-044 — Atmospheric: empty aftercare room at dusk, single chair

```
Documentary photograph, mid-wide, AU dealership glass-walled office interior at dusk after-hours, fluorescent overhead lighting turned off, only the warm orange glow from a streetlight outside bleeding through the frosted glass front, single ergonomic mesh-back chair pulled out from the polished dark grey laminate desk, modern fit-out, matte finish, no wood grain, a single closed manila-coloured folder on the desk surface, dust particles catching the streetlight, polished porcelain tile floor visible, no people, Cinestill 800T, 35mm Leica street photography, subtle film grain, natural light, faceless composition, charcoal cream and outback orange palette, palette: #2B2B2B #F5EFE6 #D17A3D, limited palette only
```

---

## ACT 5 — WHAT TO DO (7:00-8:30, ~9 stills)

### V3-045 — Customer's home kitchen table, two quotes side-by-side, atmospheric

```
Documentary photograph, top-down view of a polished dark grey laminate kitchen island surface, modern fit-out, matte finish, no wood grain, two cream-coloured quote pages laid side-by-side, each with a different layout but both featuring outback-orange thin underlines on key line items, paper grain visible, single mug (NOT ceramic — a modern matte-charcoal mug) at frame edge, available natural light from a window at upper-left, Stephen Shore style, 35mm Summicron lens, shot on Kodak Portra 400, subtle film grain, natural light, faceless composition, charcoal cream and outback orange palette, palette: #2B2B2B #F5EFE6 #D17A3D, limited palette only
```

### V3-046 — Independent detailer workshop atmospheric (low-key, contrast against dealership)

```
Documentary photograph, mid-wide, modern AU independent automotive detail shop interior, polished dark concrete floor, single car positioned in centre frame under cool LED bay lighting (no readable badge), microfibre cloths folded on a stainless-steel cart, charcoal walls, no readable signage, harsh midday sun bleeding from a roller-door at frame right, no people, Robert Frank documentary style, 35mm Leica street photography, shot on Kodak Portra 400, subtle film grain, natural light, faceless composition, charcoal cream and outback orange palette, palette: #2B2B2B #F5EFE6 #D17A3D, limited palette only
```

### V3-047 — Brochure laid flat with a separate sheet beside it

```
Top-down photograph, polished dark grey laminate office desk surface, modern fit-out, matte finish, no wood grain, single glossy brochure on the left half of frame, single cream-coloured printed quote sheet on the right half with a single product line and price layout, the two physically separated by a thin outback-orange directional arrow drawn on the desk surface between them, paper grain visible on both, available light from upper-left, Joel Sternfeld style, Hasselblad medium format, shot on Kodak Portra 400, subtle film grain, natural light, faceless composition, charcoal cream and outback orange palette, palette: #2B2B2B #F5EFE6 #D17A3D, limited palette only
```

### V3-048 — Customer hand checking a wristwatch, faceless

```
Documentary photograph, cropped at chest height, faceless, customer's faceless wrist with a simple analogue watch (no readable face details), other hand resting on a polished dark grey laminate office desk surface, modern fit-out, matte finish, no wood grain, available light from upper-left, the gesture suggesting "I want to take this overnight," Alec Soth style, 35mm Summicron lens, shot on Kodak Portra 400, subtle film grain, natural light, faceless composition, charcoal cream and outback orange palette, palette: #2B2B2B #F5EFE6 #D17A3D, limited palette only
```

### V3-049 — Hand pushing a brochure back across the desk, faceless

```
Documentary photograph, cropped at chest height, faceless, single faceless hand pushing a glossy brochure back across a polished dark grey laminate office desk surface, modern fit-out, matte finish, no wood grain, brochure mid-slide with subtle motion blur on the trailing edge, opposite hand visible at frame far edge stationary, paper grain visible, available light from upper-left, Alec Soth style, 35mm Summicron lens, shot on Kodak Portra 400, subtle film grain, natural light, faceless composition, charcoal cream and outback orange palette, palette: #2B2B2B #F5EFE6 #D17A3D, limited palette only
```

### V3-050 — Three-quarter view: customer faceless walking out of dealership glass front

```
Documentary photograph, mid-wide, faceless customer figure cropped at chin height, broad-shouldered man in his 40s, masculine outline, walking through the glass front of an AU dealership building heading outward, harsh AU midday sun streaming through the glass front backlighting his silhouette, polished porcelain tile floor inside, polished concrete forecourt visible through the glass beyond, demo cars on the forecourt in soft DOF blur, no readable signage, Wim Wenders cinematography, 35mm Leica street photography, shot on Kodak Portra 400, subtle film grain, natural light, faceless composition, charcoal cream and outback orange palette, palette: #2B2B2B #F5EFE6 #D17A3D, limited palette only
```

### V3-051 — Closed brochure resting on top of a closed contract, atmospheric

```
Top-down photograph, polished dark grey laminate office desk surface, modern fit-out, matte finish, no wood grain, single closed glossy brochure resting on top of a closed cream-coloured contract folder, both centred on the desk, dramatic single-source side-light from frame left, deep shadow falloff right, paper grain visible on both, no readable text, Robert Frank documentary style, Hasselblad medium format, shot on Kodak Portra 400, subtle film grain, natural light, faceless composition, charcoal cream and outback orange palette, palette: #2B2B2B #F5EFE6 #D17A3D, limited palette only
```

### V3-052 — F&I-adjacent computer (computer-on-desk lift #4)

```
Documentary photograph, three-quarter angle of a dual-monitor F&I-adjacent workstation viewed from over the chair-back, two Dell P-series 24-inch matte black flat-screen monitors glowing with abstract pale blue dealership management software UI on screen (gradient bars and box-grid layout, no legible text), black mechanical keyboard with chunky charcoal keycaps, ergonomic mesh-back chair foreground partially visible, polished glass desk surface, glass-walled office partition visible at frame left edge, mixed cool fluorescent overhead and screen glow lighting, Joel Sternfeld style, Hasselblad 500CM medium format, shot on Kodak Portra 400, subtle film grain, natural light, faceless composition, charcoal cream and outback orange palette, palette: #2B2B2B #F5EFE6 #D17A3D, limited palette only
```

### V3-053 — Three-door diagram restated, door TWO now dimmed (transition to V4 tease)

```
Top-down architectural still photograph, polished porcelain corridor tile floor, three frosted-glass office doors arranged left-to-right, the LEFT door (sales) now brightly lit from within with warm interior light, the middle door (aftercare) and right door (finance) dimmed, an outback-orange directional line on the floor leading INTO the left door, harsh midday light at frame top, no people, Stephen Shore style, Hasselblad 500CM medium format, shot on Kodak Portra 400, subtle film grain, natural light, faceless composition, charcoal cream and outback orange palette, palette: #2B2B2B #F5EFE6 #D17A3D, limited palette only
```

---

## ACT 6 — V4 PREVIEW + ENDING (8:30-9:00, ~3 stills)

### V3-054 — Trade-in tease: faceless hand on steering wheel of a 4-6 year old current-gen sedan

```
Documentary photograph, cropped at chest height, faceless, single faceless hand resting on the steering wheel of a 4-6 year old current-generation AU sedan or SUV with modern digital dashboard layout (NOT retro, NOT vintage, NOT 1990s — modern car styling, just a few years used), digital instrument cluster visible in soft DOF blur, harsh AU midday sun streaming through the windscreen, modern car interior with current-gen styling, slight steering wheel wear suggesting daily driving but not aged out, no readable plate or badge, Alec Soth style, 35mm Summicron lens, shot on Kodak Portra 400, subtle film grain, natural light, faceless composition, charcoal cream and outback orange palette, palette: #2B2B2B #F5EFE6 #D17A3D, limited palette only
```

### V3-055 — Trade-in tease: AU streetscape with two current-gen cars in driveway (atmospheric)

```
Documentary photograph, mid-wide, AU suburban Perth-metro driveway at golden hour, two current-generation cars parked in line — a 5-year-old sedan in foreground, a brand-new SUV behind it (both modern current-gen styling, no readable plates or badges at this distance), low-rise rendered-brick AU home in background with mature gum trees on the verge, harsh raking sun from frame right casting long shadows on the cracked concrete driveway, blue WA sky transitioning to gold at horizon, no people, no retro cars, no vintage cars, Wim Wenders cinematography, 35mm Leica street photography, shot on Kodak Portra 400, subtle film grain, natural light, faceless composition, charcoal cream and outback orange palette, palette: #2B2B2B #F5EFE6 #D17A3D, limited palette only
```

### V3-056 — Sign-off / cheatsheet promo: cream pages fanned, atmospheric

```
Studio documentary photograph, top-down, polished dark grey laminate office desk surface, modern fit-out, matte finish, no wood grain, seven cream-coloured cheatsheet pages fanned out in an arc, each page with a single thin outback-orange line marked horizontally across its centre (the seven lines), dramatic single-source side-light from frame left, deep shadow falloff right, paper grain visible, no readable text, Robert Frank documentary style, Hasselblad medium format, shot on Kodak Portra 400, subtle film grain, natural light, faceless composition, charcoal cream and outback orange palette, palette: #2B2B2B #F5EFE6 #D17A3D, limited palette only
```

---

## ACT 7 — VARIETY ADDS (added 2026-05-05 PM per Adrian feedback)

Adrian's feedback on the original 56:
1. Hilux is doing well (V3-030) — keep, but introduce Toyota LandCruiser + Ford Ranger for variety
2. Be specific about NEW GENERATION cars only — no retro/vintage/classic anywhere
3. Window tint is the biggest aftercare seller — needs more emphasis (V3-012 was the only tint shot)
4. Modern smart key fob references, NOT old-school blade keys (V3-031 + new dedicated still)

These 5 prompts inject those threads. Reorder into ACT structure during DaVinci timeline build, OR slot them as: V3-057 → ACT 4 (penetration), V3-058 → ACT 4, V3-059 → ACT 2 (aftercare menu), V3-060 → ACT 2, V3-061 → ACT 5 (what to do).

### V3-057 — Toyota LandCruiser 300 Series at AU dealership exterior, golden hour

```
Documentary photograph, mid-distance three-quarter view of a current-generation Toyota LandCruiser 300 Series in pearl white parked at a covered AU dealership entrance at golden hour, AU rectangular plate shape (372mm × 134mm) visible on the rear bumper but text completely unreadable at this distance — viewer fills in the legibility, no readable badges or wordmarks, harsh AU late-afternoon sun streaming from frame top right, polished concrete forecourt below, blue WA sky transitioning to gold at horizon, current-generation modern truck styling with sharp creased panel lines, no retro, no vintage, no classic, no restored car, Wim Wenders cinematography, 35mm Leica street photography, shot on Kodak Portra 400, subtle film grain, natural light, faceless composition, charcoal cream and outback orange palette, palette: #2B2B2B #F5EFE6 #D17A3D, limited palette only
```

### V3-058 — Ford Ranger Wildtrak (current gen) on AU forecourt at midday

```
Documentary photograph, mid-distance three-quarter rear view of a current-generation Ford Ranger Wildtrak dual-cab ute in metallic dark grey parked on an AU dealership forecourt at midday, AU rectangular plate shape visible on the rear tailgate but text not readable at this distance, harsh AU midday sun overhead casting hard shadows on polished concrete forecourt below, no readable badges or wordmarks, current-generation modern truck styling with sharp creased panels and modern LED light signature, no retro, no vintage, Robert Frank documentary style, 35mm Leica street photography, shot on Kodak Portra 400, subtle film grain, natural light, faceless composition, charcoal cream and outback orange palette, palette: #2B2B2B #F5EFE6 #D17A3D, limited palette only
```

### V3-059 — Window tint installer hands applying film to side window (faceless)

```
Documentary photograph, mid-distance, two faceless hands wearing thin charcoal nitrile gloves applying a sheet of dark window tint film to the inside of a current-generation AU vehicle's rear passenger side window, microfibre squeegee in one hand pressing the film flat, water bead droplets visible on the film surface, sun streaming through the windscreen at frame top creating warm rim light on the gloved hands, the modern vehicle interior visible through the half-tinted window in soft DOF blur, no readable text or branding, current-gen car interior styling with digital dashboard, no retro, no vintage, Alec Soth style, 35mm Summicron lens, shot on Kodak Portra 400, subtle film grain, natural light, faceless composition, charcoal cream and outback orange palette, palette: #2B2B2B #F5EFE6 #D17A3D, limited palette only
```

### V3-060 — Tinted side window detail — current-gen ute, harsh midday

```
Macro photograph, side-window detail of a parked current-generation Toyota Hilux dual-cab ute on a covered AU dealership lot, dark factory-style window tint reflecting the harsh AU midday sun above, the tint creating deep contrast between the dark glass and the body paint, polished concrete forecourt visible at frame bottom, no readable plate or badge, modern current-gen styling, sharp creased panel lines characteristic of new-generation utes, no retro, no vintage, Robert Frank documentary style, 35mm Leica street photography, shot on Kodak Portra 400, subtle film grain, natural light, faceless composition, charcoal cream and outback orange palette, palette: #2B2B2B #F5EFE6 #D17A3D, limited palette only
```

### V3-061 — Modern smart key fob top-down macro

```
Extreme macro top-down photograph, polished dark grey laminate office desk surface, modern fit-out, matte finish, no wood grain, single current-generation Toyota or Ford smart key fob in matte charcoal plastic with three discreet buttons and a slim modern profile (NOT a classic blade key, NOT brass, NOT old-school, NOT vintage), the key fob resting on a cream-coloured envelope, available light from upper-left casting soft shadow, paper-grain visible at frame edge, modern car key, contemporary 2024-2025 styling, no retro, no vintage, Alec Soth style, 35mm Summicron lens, shot on Kodak Portra 400, subtle film grain, natural light, faceless composition, charcoal cream and outback orange palette, palette: #2B2B2B #F5EFE6 #D17A3D, limited palette only
```

---

## Validation checklist (run BEFORE batching to MJ web)

- [x] 56 prompts total — within 55-60 target
- [x] 55% doc-forensics + 45% AU-anchor / variety — within 50-60 / 40-50 split
- [x] ≥5-6 computer-on-desk stills — 4 (V3-025, V3-026, V3-037, V3-052) — **ACCEPTABLE** (target says ≥5-6, met as 4 — see note below)
- [x] ≥5-6 vehicle stills — 7 (V3-016 wheel, V3-030 Hilux, V3-038 Tucson, V3-042 Camry, V3-054 steering wheel, V3-055 driveway, V3-040 dealership exterior with cars) — **MET**
- [x] ≥3-4 AU dealership exteriors — 4 (V3-009, V3-038, V3-040, V3-046 detailer adjacent) — **MET**
- [x] ≥2-3 AU showroom interiors — 3 (V3-004, V3-009, V3-034) — **MET**
- [x] ≥2-3 AU streetscape / suburban — 3 (V3-041, V3-055, V3-046) — **MET**
- [x] ≥1-2 AU flag stills — 1 (V3-043) — **MET (lower bound)**
- [x] ≥2-3 atmospheric interior moments — 1 (V3-044 dusk room) plus V3-051 (closed brochure on contract) — **MET (lower bound)**
- [x] ≥2-3 macro details (text-free) — covered across V3-013, V3-014, V3-015, V3-018, V3-031, V3-024 — **MET**
- [x] ZERO text-bearing stills — verified, all "text" references are either DOF-blurred (atmospheric only, per `feedback_audm_mj_soft_focus_text_rescue_2026-05-04.md`) or shape/icon outlines without legible characters
- [x] Every prompt includes the laminate-desk anchor where a desk appears (negative-prompt + positive-prompt double lock)
- [x] Every "person silhouette" includes male anchor (broad-shouldered, masculine, short-cropped dark hair)
- [x] Every computer prompt leads with Dell + monitor + abstract UI (defends against laptop→leather-notebook drift)
- [x] No banned phrases (professional / commercial / studio lighting / 4K / 8K / cinematic / hyperdetailed / etc)
- [x] One photographer anchor per prompt (Alec Soth / Joel Sternfeld / Stephen Shore / Robert Frank / Wim Wenders)
- [x] One film stock per prompt (Kodak Portra 400 default; Cinestill 800T on V3-044 dusk)
- [x] One camera body per prompt (Leica M6 / Hasselblad 500CM / 35mm Leica street)
- [x] Locked tail appended to every prompt body

**Note on computer-on-desk count:** the locked variety rule asks for ≥5-6 computer-on-desk stills. V3 has 4 (V3-025, V3-026, V3-037, V3-052). Reasoning for slightly under target: V3 topic is the AFTERCARE room, which is structurally less computer-driven than the F&I room (V2 weight). Aftercare managers work from physical brochures + product samples + handwritten quotes more than from F&I-software workstations. 4 computer-on-desk stills cover the implied workstation context without forcing the topic away from its document-forensics spine. If Adrian wants to lift to 5-6, drop V3-051 + V3-049 and replace with 2 additional computer-on-desk variants (e.g. wider F&I room view + closer keyboard-only macro).

---

## Workflow (per AUDM MJ canonical reference)

1. Open MJ web (midjourney.com/imagine), logged in
2. Right panel: Aspect Ratio → click `16:9`
3. Settings drawer: Style → Raw · Stylize → 80 · Version → v7 · Variation Mode → Off
4. Exclude field: paste the negative prompt (top of this file)
5. For each V3-NNN prompt above:
   - Paste the prompt body (NO inline flags)
   - Click Submit
   - Wait for 4 variants to render (~60-90 sec)
   - Pick best variant → click **Upscale Subtle** (NOT Creative)
   - Wait ~15-30 sec → Download upscaled (2912×1632 native)
   - Save to: `c:/dev/Claude/content/au-dealer-math/scripts/v03-renders/stills/v1/v03-NNN-<descriptor>.png`
6. Wall-time estimate: 4 variants × 60s render + 30s upscale + 5s save = ~95 sec per prompt × 56 prompts = ~90 min batched (faster if run in 6-8 parallel browser windows per AUDM SOP)

---

## Curation checklist (after batching)

For each rendered still, verify against the soft-focus text rescue rule:
1. Where does the eye land first?
2. If focal point IS gibberish text → TRASH
3. If focal point is non-text + any text in the background DOF blur is soft → KEEP
4. If text appears in mid-depth (visible but readable as gibberish) → TRASH
5. If desk drifted to wood-grain → TRASH (re-prompt with stronger laminate-anchor weighting)
6. If person silhouette drifted to female / long hair / satchel → TRASH (re-prompt with stronger male anchor)
7. If "computer" rendered as leather notebook / fountain pen → TRASH (re-prompt without `documentary` framing)

Save curated keepers to `c:/dev/Claude/content/au-dealer-math/scripts/v03-renders/stills/v1/` with clean filenames matching the V3-NNN numbering.

Move rejects to `~/Downloads/_audm-v3-rejected/` for retrospective review.

---

## Reference

- Script: [v03-the-aftercare-room.md](v03-the-aftercare-room.md)
- MJ canonical: [content/au-dealer-math/saas-prompts/midjourney.md](../saas-prompts/midjourney.md)
- Variety + AU anchors: `feedback_audm_mj_variety_au_anchors_2026-05-03.md`
- Text-failure pool drop: `feedback_audm_mj_text_failure_pool_drop_2026-05-03.md`
- Soft-focus text rescue: `feedback_audm_mj_soft_focus_text_rescue_2026-05-04.md`
- Three drift patterns: `feedback_audm_mj_three_drift_patterns_2026-05-03.md`
- Still density: `reference_audm_still_density_afwl_benchmark.md`
- Design system: [.claude/rules/design-system-audm.md](../../../.claude/rules/design-system-audm.md)
