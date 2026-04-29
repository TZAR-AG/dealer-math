# AU Dealer Math — Video 1 Midjourney Prompt Sheet

## Visual style template (applies to ALL prompts)

> *charcoal #2B2B2B and cream #F5EFE6 palette with outback orange #D17A3D accents, Polymatter and Wendover Productions vector flat illustration aesthetic, Cleo Abram inspired minimalism, no faces or recognisable features, Australian setting, 16:9 cinematic composition, soft lighting, contemporary editorial illustration*

**Universal parameters:** `--ar 16:9 --style raw` (UI Version dropdown set to 7 Standard — don't add `--v` to prompts, let UI handle versioning)

**Negative-prompt syntax rule (locked 2026-04-29):** combine all suppression terms into ONE `--no` parameter with comma-separated list. Multiple `--no` parameters accumulate negative weights and trigger Midjourney's "sum of all prompt weights must be positive" error.
- ✅ `--no logo, badge, brand, grille` (one `--no` parameter)
- ❌ four separate `--no` parameters strung together (fails)

**Aspect ratio rule:** all stills are 16:9 to match YouTube frame natively. Don't deviate — square crops waste vertical real estate when burnt into a landscape edit.

**Iteration plan:** generate 4 variants per prompt, pick best. If first batch doesn't land, refine the descriptor (less is often more — too many descriptors fight each other).

---

## Still 1 — Scene 2 (0:20) — Top-down dealership floor

**Purpose:** establishes Macca's "I worked here" world. Calm, observational, slightly elevated angle.

**Prompt (refined 2026-04-29 against real premium AU showroom reference — Taylor BMW Sydney):**
```
top-down isometric architectural illustration of a premium Australian car dealership showroom interior, vast polished concrete floor reflecting overhead lights, double-height ceiling with floor-to-ceiling glazed facades letting natural daylight cascade through, laser-cut aluminium feature wall accents with geometric patterns, rows of new cars displayed on the level showroom floor (NO plinths NO raised platforms), small consultation desks and a cafe corner visible in the background as customer oasis space, clean gallery-like minimalist atmosphere, no people visible, charcoal and cream palette with outback orange accent lights, Polymatter and Wendover Productions vector flat illustration aesthetic, minimalist editorial style, 16:9 cinematic --ar 16:9 --style raw --no logo, badge, brand, grille
```

**Acceptance criteria:**
- ✅ No human figures
- ✅ Clear charcoal + cream palette dominance
- ✅ At least 6 cars visible in rows
- ✅ Polished/clean dealership feel (NOT outdoor lot, NOT rural yard)
- ❌ Reject if it looks like a parking garage or warehouse
- ❌ Reject if any logos or brand names appear on cars

---

## Still 2 — Scene 3 (2:00) — Customer at desk with confusion

**Purpose:** illustrates the moment the customer is asked the trap question. Customer is the silhouette focal point, salesperson is a peripheral counterpart.

**Prompt:**
```
flat 2D illustration of an Australian car dealership desk scene from 
behind the customer's shoulder, customer silhouette holding car keys 
looking at a contract with question marks floating around their head, 
salesperson silhouette across the desk gesturing with a brochure, 
charcoal cream and outback orange palette, vector flat aesthetic in 
the style of Polymatter Wendover Cleo Abram, no facial features visible, 
modern editorial illustration, 16:9 cinematic composition, soft natural 
desk lighting --ar 16:9 --style raw
```

**Acceptance criteria:**
- ✅ Customer in foreground silhouette
- ✅ Salesperson in mid-ground, NO face
- ✅ Question marks visible (small, not cartoonish)
- ✅ Desk between them with contract / brochure on it
- ❌ Reject if either figure shows facial detail
- ❌ Reject if it looks comic-book / Marvel-style

---

## Still 3 — Scene 4 (3:45) — Two cars side-by-side comparison

**Purpose:** visualises the "$40K car at 4yr vs $55K car at 7yr, same weekly payment" moment. Two cars with price tags.

**Prompt:**
```
flat 2D editorial illustration showing two cars side by side on neutral 
charcoal background, left car a compact sedan with a small price tag, 
right car a larger luxury SUV with a larger price tag, both with 
identical "$300/week" labels above them, vector flat aesthetic with 
clean line work, charcoal cream and outback orange palette, 
Polymatter Wendover Productions style, minimalist editorial 
illustration, no logos or brand markings on cars, 16:9 cinematic 
--ar 16:9 --style raw
```

**Acceptance criteria:**
- ✅ Two clearly differentiated vehicles (compact vs SUV)
- ✅ NO visible brand logos or grille details that could imply a real brand
- ✅ Generic vehicle silhouettes / line drawings work better than detailed renders
- ✅ Clean charcoal background — no environmental clutter
- ❌ Reject if either car looks specifically like a real model (Toyota Camry / Mercedes GLE etc.)

**Important:** Midjourney sometimes adds brand logos. Inspect carefully. If logos appear, regenerate with `--no logo, --no badge, --no brand`.

---

## Still 4 — Scene 5 (4:30) — Three-room dealership cutaway

**Purpose:** the "Three-Room Trap" reveal. Shows the customer's path through Sales → Aftercare → Finance.

**Prompt (refined 2026-04-29 — three glass-fronted offices side-by-side, BMW Sydney showroom reference):**
```
front-elevation isometric illustration of three glass-fronted offices side by side inside a premium Australian car dealership showroom, each office with floor-to-ceiling glass walls and a small signage strip above its entrance, leftmost office SALES with a desk and silhouette figure inside, middle office AFTERCARE with a counter and shelving plus silhouette figure, rightmost office FINANCE with a desk computer and silhouette figure, polished concrete showroom floor in the foreground, double-height ceiling with daylight cascading from above, laser-cut aluminium accent panels between offices, all human figures pure silhouettes with NO faces or features, charcoal cream and outback orange palette with outback orange highlights on the entrance signage, vector flat illustration Polymatter Wendover Productions style, minimalist editorial premium showroom feel, 16:9 cinematic --ar 16:9 --style raw --no logo, badge, brand
```

**Acceptance criteria:**
- ✅ Three distinct rooms visible
- ✅ Labels readable: SALES / AFTERCARE / FINANCE
- ✅ Hallway or connection between them clear
- ✅ Silhouettes only, no faces
- ❌ Reject if it looks like a floor plan rather than illustration
- ❌ Reject if the rooms blend together (each must read distinctly)

**Note:** Midjourney text rendering is unreliable. If labels render as gibberish, generate the scene WITHOUT labels and add them in After Effects post-production.

---

## Still 5 — Scene 6 (6:45) — Confident customer silhouette

**Purpose:** the visual payoff moment. Customer has the script, salesperson is on the back foot.

**Prompt:**
```
flat 2D illustration of a confident customer silhouette standing 
calmly at a car dealership desk, hands relaxed at sides, posture 
upright and confident, salesperson silhouette across the desk leaning 
forward in a slightly defensive posture, charcoal cream and outback 
orange palette, vector flat aesthetic in the style of Polymatter and 
Wendover Productions, no facial features visible, modern editorial 
illustration, soft natural lighting from above the desk, 16:9 cinematic 
--ar 16:9 --style raw
```

**Acceptance criteria:**
- ✅ Customer body language reads as confident (upright, hands relaxed)
- ✅ Salesperson body language reads as slightly defensive (lean-forward, hands on desk)
- ✅ Composition mirrors Still 2 but with reversed power dynamic
- ❌ Reject if customer looks aggressive or salesperson looks defeated (overplay = less believable)

---

## Still 6 — Scene 7 (7:40) — Lead magnet PDF cover float

**Purpose:** end-card visual showing the lead-magnet PDF cover floating above a dark background, drawing the eye to the description link.

**Prompt:**
```
floating 3D-style stylised PDF cover above a charcoal background, 
the cover features the title "7 LINES ON A DEALER CONTRACT YOU 
SHOULD NEVER SIGN" in bold cream typography, AU Dealer Math wordmark 
small at top, outback orange accent stripe, soft drop shadow beneath, 
minimalist editorial product photography aesthetic, charcoal cream 
and outback orange palette, 16:9 cinematic, premium feel 
--ar 16:9 --style raw
```

**Note:** Midjourney text on a generated PDF cover usually reads as gibberish. Better path: generate a blank stylised PDF cover floating in space, then composite the actual title text in After Effects. Use this prompt to get the float aesthetic, then layer real text on top.

**Alternative approach:** skip Midjourney entirely for this still. Render the lead-magnet PDF (already done — it's at `generator/au-dealer-math/output/au-dealer-math-7-lines.pdf`). Take a screenshot of page 1 (the cover). Use that screenshot in After Effects with a soft drop shadow + slight rotation. Faster + factually accurate (the viewer sees the actual cover they'll receive).

---

## Production tips (Midjourney specific 2026)

1. **Run all 6 prompts in one Midjourney session** to maintain visual consistency. Generation drift across sessions is real.
2. **Use `--seed` if you find a v6.1 setup that lands** — locks the aesthetic across batches.
3. **Avoid text in the prompts** — Midjourney text rendering is unreliable in v6.1. Generate text-free imagery, layer typography in post.
4. **Test with `--style raw`** if the default style drifts toward illustration-cliché. Raw mode keeps it editorial and clean.
5. **Reject anything with brand-recognisable elements.** YouTube algorithmic enforcement scans for trademark infringement; even subtle car-brand cues can trigger it.
6. **Batch download all 4 variants** of each prompt (don't pick one immediately). Sometimes a v3 of variant 2 beats v1 of all four.

---

## Estimated time + cost

| Step | Time | Midjourney credits |
|---|---|---|
| Initial generation (6 prompts × 4 variants) | 30 min | ~24 generations |
| Variant selection + 1-2 refinement passes | 30 min | ~12 generations |
| Final pick + export to PSD/PNG | 15 min | 0 |
| **Total** | **~75 min** | **~36 generations** |

Midjourney Standard ($30/mo) = 200 hours fast generation. 36 generations costs ~$2-3 in credits. Comfortable.

---

## Adrian's manual flow once Midjourney is confirmed live

1. Open Discord → Midjourney bot or web UI (https://www.midjourney.com/explore)
2. Copy each prompt verbatim from this file
3. Run them in batch (don't wait between)
4. As variants come back, drop the best 2-3 from each into a folder: `content/au-dealer-math/scripts/v01-renders/`
5. Ping me — I'll QC against the storyboard acceptance criteria before we move to Kling motion + edit
