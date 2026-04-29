# AU Dealer Math — Video 1 Kling Motion Clip Prompt Sheet

## Approach

Kling AI 3.0 supports image-to-video. Workflow:
1. Use Midjourney still as the input image
2. Add motion prompt describing the camera movement / element animation
3. Generate 5-second clip
4. Drop into edit timeline as a "hero motion shot"

For V1, we need 3 hero motion clips at key retention re-hook moments. Each is 3-5 seconds.

**Universal Kling 3.0 settings:**
- Aspect ratio: 16:9
- Duration: 5 seconds
- Motion strength: medium (camera-led, not scene-driven)
- Style: photorealistic-leaning

---

## Clip 1 — Scene 1 (0:09) — "10 YEARS" hook motion

**Purpose:** the "I sold cars in Australia for ten years" moment. Visual hook re-anchor at 0:09 to keep 30s hold-through ≥70%.

**Input image:** Generate a Midjourney still of a stylised Australian car-lot silhouette at golden hour. Palette charcoal/cream/outback orange.

**Midjourney precursor prompt:**
```
stylised silhouette of an Australian car dealership exterior at golden 
hour dusk, low camera angle looking up at the building edge, rows of 
cars in foreground silhouette, dramatic warm orange and charcoal sky, 
minimalist editorial photography aesthetic, no figures, 16:9 cinematic 
--ar 16:9 --style raw --v 6.1
```

**Kling motion prompt:**
```
slow horizontal camera dolly from left to right along the row of car 
silhouettes, cinematic stabilised motion, subtle warm light shift, 
no people, 5 seconds
```

**Acceptance criteria:**
- ✅ Smooth horizontal dolly (no stutter)
- ✅ Light shift feels natural (sunrise/sunset transitioning)
- ✅ No appearing figures or distortion
- ❌ Reject if cars deform during the dolly (Kling sometimes warps geometry)

---

## Clip 2 — Scene 2 (0:15) — Wordmark animated reveal

**Purpose:** brand wordmark reveal. NOT generated via Kling — built in After Effects (typography animation).

**Spec:**
- Black charcoal background
- "AU DEALER MATH" wordmark fades in letter-by-letter, 0.4 sec stagger
- Outback orange underline draws in left-to-right
- Subtitle "What dealers don't tell you" fades in below at 0.8 sec
- Total animation length: 3 sec
- Hold final state: 1 sec

**Built in:** After Effects via Adrian's editor or InVideo AI. Kling is overkill for typographic motion.

---

## Clip 3 — Scene 4 (3:45) — Two cars side-by-side parallax

**Purpose:** the "$40K car vs $55K car" hero comparison moment. Visual punch at the centerpiece reveal.

**Input image:** Midjourney Still 3 (the two-cars side-by-side comparison).

**Kling motion prompt:**
```
gentle parallax camera dolly slowly pulling backward from the two 
cars, both cars holding still while the background slides slightly, 
subtle depth-of-field shift, cinematic stabilised, no figures, 5 seconds
```

**Acceptance criteria:**
- ✅ Cars stay still (don't morph or move)
- ✅ Background has subtle parallax (not static)
- ✅ Camera pull-back feels intentional, not jarring
- ❌ Reject if cars distort or shift between frames

---

## Production order

1. Adrian generates Midjourney stills (per `v01-midjourney-prompts.md`) — Day 4-5
2. Pick best stills, drop into Kling — Day 5
3. Generate motion clips with prompts above
4. After Effects: build the wordmark reveal (Clip 2) + any additional typographic motion needed
5. All motion clips delivered to editor for assembly

---

## Estimated time + cost

| Step | Time | Kling credits |
|---|---|---|
| Generate 2 Kling clips (clip 1 + clip 3) | 20 min | ~10 credits |
| Refinement passes if needed | 15 min | ~5 credits |
| After Effects wordmark animation (Clip 2) | 30 min | n/a |
| **Total** | **~65 min** | **~15 credits** |

Kling 3.0 Starter ($10/mo) = 660 credits/mo. ~15 credits is comfortable.

---

## Why we're not using Kling for everything

For V1 specifically, the bulk of the visual layer is:
- Typography (After Effects / InVideo AI / Submagic)
- Static stills (Midjourney)
- Stock B-roll (Storyblocks)

Kling is reserved for 2-3 hero moments where motion compounds the message. Over-using AI motion video on V1 risks the YouTube Jan 2026 AI-deboost wave (mass-templated motion = deboost trigger). Three motion clips inside an otherwise typography-and-stills video reads as editorial choice, not AI mass output.

---

## Adrian's manual flow once Midjourney + Kling are confirmed live

1. Generate Midjourney stills (per `v01-midjourney-prompts.md`)
2. Pick best stills for clips 1 + 3
3. Open Kling AI (https://klingai.com/)
4. Upload still as input
5. Paste motion prompt verbatim from this file
6. Generate 5-sec clip
7. Drop output into `content/au-dealer-math/scripts/v01-renders/motion/`
8. Ping me to QC before edit assembly
