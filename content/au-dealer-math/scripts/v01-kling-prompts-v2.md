# V1 Kling Motion Clip Prompts — v2 (expanded script, 12-min runtime)

10 motion clips covering the long-hold scenes in the expanded V1. Replaces v1-kling-prompts.md (which only covered 2 hero shots).

**Universal Kling 3.0 settings:**
- Aspect ratio: 16:9
- Duration: 5 seconds
- Motion strength: medium (camera-led, photorealistic-leaning)
- ⚠ **NO WATERMARK** — toggle ON before download (Starter tier supports this; the watermarked clips earlier today were a download-time mistake)

**Priority order (most visual-gap impact first):**

---

## Clip 1 — Scene 5 (5:46–5:51) — Aftercare manager office reveal

**Why:** Scene 5 holds for 3:06 with no motion. Highest visual-gap priority. Hook to "There isn't one office behind the salesperson. There are two."

**Input image:** existing `still-4-three-rooms.png`

**Kling motion prompt:**
```
slow camera dolly forward through the threshold of the dealership back office,
revealing a clean reception desk with paint protection product samples on the counter,
warm interior lighting with soft shadows, photorealistic stylised AU dealership aesthetic,
charcoal and outback orange palette, no figures, 5 seconds
```

**Acceptance:** clean dolly forward, no warping of geometry, palette stays on-brand

---

## Clip 2 — Scene 5 (6:30–6:35) — Paint protection product close-up

**Why:** anchor visual for "$2,000 retail / $500 cost / 75% margin" reveal.

**Input image:** generate new Nano Banana still — automotive paint protection bottle on a clean black slate counter, soft directional lighting, AU dealership aesthetic, no logos visible

**Kling motion prompt:**
```
extreme slow rotation around a paint protection product bottle on a slate counter,
camera circling 30 degrees to reveal the label, dramatic spotlight from above,
shallow depth of field, charcoal background fading to soft warm orange,
no figures, 5 seconds
```

---

## Clip 3 — Scene 5 (7:00–7:05) — Finance manager paperwork zoom

**Why:** anchor visual for "the bank approves at one rate; contract gets written at a higher one" rate-markup reveal.

**Input image:** generate new Nano Banana still — overhead view of a loan contract on a desk, pen resting on it, calculator beside it, percentage figures legible but stylised

**Kling motion prompt:**
```
top-down zoom-in onto a loan contract page, camera descending slowly,
the percentage figure on the page sharpening as the lens approaches,
calculator partially visible, AU dealership executive desk aesthetic,
warm desk lamp lighting, no figures, 5 seconds
```

---

## Clip 4 — Scene 5 (7:30–7:35) — Holdback hidden layer visualization

**Why:** anchor visual for "a layer the salesperson on the floor can't see" reveal — the holdback. Most viral-potential beat in the script.

**Input image:** generate new Nano Banana still — three-tier paper stack on a desk, top layer clearly visible (sale contract), middle obscured, bottom partially hidden (manufacturer holdback statement)

**Kling motion prompt:**
```
slow lateral camera slide right to left across three stacked documents on a desk,
the top layer crisp, middle and bottom layers progressively shrouded in shadow,
revealing a partially-obscured manufacturer payment statement at the bottom,
charcoal palette with directional warm light, no figures, 5 seconds
```

---

## Clip 5 — Scene 4 (3:35–3:40) — $300/wk × 7yr loan math reveal

**Why:** the centerpiece $46,800-difference reveal needs visual punch beyond text overlay.

**Input image:** generate new Nano Banana still — a loan calculator screen showing two columns: "4 YEARS / $62,400" and "7 YEARS / $109,200" with the difference highlighted

**Kling motion prompt:**
```
slow camera push-in toward a loan calculator display, the two columns of numbers
sharpening as the lens approaches, soft glow appearing around the larger total,
AU dealership desk environment partially visible in soft bokeh, warm overhead
lighting, no figures, 5 seconds
```

---

## Clip 6 — Scene 4 (4:30–4:35) — GFV trade-up treadmill (luxury)

**Why:** anchor visual for the Guaranteed Future Value reveal — "the customer never owns the car."

**Input image:** generate new Nano Banana still — a luxury sedan rolling slowly on a turntable in a showroom, three identical sedans in shadow behind it suggesting model-cycle replacement, German/European dealership aesthetic

**Kling motion prompt:**
```
slow rotating turntable shot of a luxury sedan in a charcoal showroom,
identical sedans visible in soft focus behind it suggesting succession,
warm overhead spotlight, parquet floor, no figures, 5 seconds
```

---

## Clip 7 — Scene 3 (1:30–1:35) — Road to a Sale training playbook

**Why:** anchor visual for "the first document they handed me was called Road to a Sale."

**Input image:** generate new Nano Banana still — a closed worn manila training binder labeled "ROAD TO A SALE" lying on an office desk, beside a pen and a coffee cup, dated 2010s aesthetic

**Kling motion prompt:**
```
slow camera tilt down toward a closed worn manila binder on an office desk,
binder label "ROAD TO A SALE" sharpening into focus, pen and ceramic coffee
cup beside it in soft focus, warm desk lamp lighting from upper-left,
no figures, 5 seconds
```

---

## Clip 8 — Scene 6 (8:55–9:00) — Bank pre-approval letter

**Why:** anchor visual for "bring real bank pre-approval. Not an estimate."

**Input image:** generate new Nano Banana still — a formal bank pre-approval letter on a leather portfolio, AU bank letterhead style, signed in pen at the bottom

**Kling motion prompt:**
```
slow camera tilt up from the bottom signature line of a bank pre-approval letter
to the bank letterhead at the top, document resting on a leather portfolio,
soft directional lighting, premium AU consumer banking aesthetic, no figures, 5 seconds
```

---

## Clip 9 — Scene 6 (9:30–9:35) — Total cost comparison papers

**Why:** anchor visual for "total cost over the full term, all fees included, both papers side by side."

**Input image:** generate new Nano Banana still — two loan documents side-by-side on a desk, one labeled "BANK" the other "DEALER", both with total-cost figures clearly different

**Kling motion prompt:**
```
slow lateral camera slide left across two side-by-side loan documents on a desk,
the BANK paper on the left and DEALER paper on the right, both papers in equal
focus, total-cost figures legible but stylised, executive desk aesthetic,
no figures, 5 seconds
```

---

## Clip 10 — Scene 6 (10:30–10:35) — Manufacturer rate campaign banner

**Why:** anchor visual for "1.99% / 4.9% / manufacturer fixed-rate campaign window."

**Input image:** generate new Nano Banana still — a dealership window display showing a "FINANCE FROM 1.99%" promotional banner, Australian dealership at street level

**Kling motion prompt:**
```
slow horizontal camera dolly past a dealership window display, "FINANCE FROM 1.99%"
banner sharpening as the lens passes, glass reflection of street life subtly visible,
late-afternoon warm light, AU dealership exterior aesthetic, no figures, 5 seconds
```

---

## Generation order

1. **Drop existing inputs first** (clips 1, 5 use existing stills) — these can submit immediately
2. **Generate 8 new Nano Banana stills** for clips 2-4, 6-10 (~5-15 min each)
3. **Submit Kling jobs** as inputs become ready — Kling render time 5-15 min per clip on Starter tier
4. **Download with NO WATERMARK toggled** — verify before download

Total render budget: ~2-4 hr running in parallel. Adrian's manual time: ~5 min per Kling submission × 10 = ~50 min if doing manually, or fully driven via dev tools after login.

---

## Storyblocks B-roll backup list

For any scenes where Kling renders fail or look off-brand, Storyblocks search terms:
- "Australian dealership exterior" → scene 1/5 backups
- "loan paperwork close-up" → scenes 4/5/6 backups
- "calculator finance close-up" → scene 4 backup
- "money stack Australian currency" → scene 5 holdback backup
- "AU street signage suburb" → scene 7 sign-off backup

Drop these as 5-10 sec cutaways between Kling clips for additional visual variety.

---

## Reference

- Created: 2026-04-29 evening, V1 ship deferred for visual depth fix
- Replaces: `v01-kling-prompts.md` (original 3-clip plan obsoleted by script expansion)
- Related: `V1-HANDOFF.md` § Punch list, `dealer-knowledge-bank.md` (source content)
