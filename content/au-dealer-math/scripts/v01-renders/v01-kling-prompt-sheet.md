# V1 Kling motion-clip sheet — final

10 Kling 3.0 image-to-video clips. Each uses a v2/ still as input + a motion prompt. 5 sec each. Built to canonical patterns from `saas-prompts/kling.md`.

**Output:** save MP4s to `content/au-dealer-math/scripts/v01-renders/motion/v2/` with the filename listed.

---

## Universal SOP per clip

1. Open [klingai.com](https://klingai.com) → Generate → Image-to-Video → Kling 3.0 (Standard mode)
2. Upload input still from `content/au-dealer-math/scripts/v01-renders/stills/v2/` (path listed per clip)
3. Paste motion prompt (20-50 words, ONE camera move only)
4. Paste universal negative prompt (below)
5. Settings: 5 sec · 16:9 · motion strength medium · photorealistic-leaning style
6. Generate (5-15 min render time on Starter tier)
7. Preview → if warping / figures appear / sudden zoom → re-roll once
8. **Download → TICK "No watermark" → save to motion/v2/** with the filename listed

## Universal negative prompt (paste in Negative field every render)

```
warped text, morphing letters, melting edges, distorted documents, hallucinated figures, sudden zoom, motion blur trail, plastic over-smooth, low quality artifacts, flickering
```

---

## 1 — Slot 2A — Training binder tilt-down

**Input still:** `still-v2-2A-training-binder.png`
**Save as:** `motion/v2/kling-v2-2A-binder-tilt-down.mp4`

```
Slow camera tilt down toward the closed manila training binder on the office desk, binder spine sharpening as the camera approaches, pen and matte black coffee cup beside it staying in soft focus. Preserve binder shape and silhouette, maintain proportions, keep paper grain. Warm desk lamp light from upper-left unchanged. Documentary realism. 5 seconds, hold final frame.
```

---

## 2 — Slot 3B — Open Road-to-a-Sale binder dolly-in

**Input still:** `still-v2-3B-road-to-a-sale.png`
**Save as:** `motion/v2/kling-v2-3B-binder-dolly.mp4`

```
Slow dolly push-in toward the open binder centre spread, the schematic flowchart diagram on the page sharpening into focus as the camera moves forward. Preserve page layout, keep diagram linework crisp, maintain paper grain. Subtle warm light shaft rolling across the page from upper-left. Documentary 35mm look, soft directional warm key. 5 seconds, hold final frame.
```

---

## 3 — Slot 3D — Three-rooms slow pull-back (uses existing still)

**Input still:** `still-4-three-rooms.png` (from existing v01-renders/stills/, not v2/)
**Save as:** `motion/v2/kling-v2-3D-three-rooms-pull.mp4`

```
Slow camera pull-back from the three doors, revealing more of the corridor interior as the camera recedes. Preserve door layout, keep proportions, maintain warm interior lighting. Subtle parallax on the corridor walls. Documentary observational tone, soft warm key from upper-left. 5 seconds, hold final frame.
```

---

## 4 — Slot 4A — Split-stacks lateral camera slide

**Input still:** `still-v2-4A-split-stacks.png`
**Save as:** `motion/v2/kling-v2-4A-stacks-pan.mp4`

```
Slow horizontal camera slide from left to right across the two paper stacks, the height contrast becoming more obvious as the camera passes from the shorter stack to the taller stack. Preserve stack shapes, maintain paper grain, keep proportions. Warm light from upper-left unchanged. Cinematic stabilised motion. 5 seconds, hold final frame.
```

---

## 5 — Slot 4D — Luxury sedan turntable rotation

**Input still:** `still-v2-4D-luxury-treadmill.png`
**Save as:** `motion/v2/kling-v2-4D-luxury-treadmill.mp4`

```
Slow horizontal pan around the stationary luxury sedan, faint parallax on the showroom backdrop. Preserve vehicle silhouette, paint colour, badge and grille shape, maintain proportions. Studio key light from upper-right unchanged, cool rim light, polished concrete floor reflection underneath. Cinematic automotive documentary tone. 5 seconds, no zoom, hold final frame.
```

---

## 6 — Slot 5A — Three glass offices slow dolly forward

**Input still:** `still-v2-5A-three-glass-offices.png`
**Save as:** `motion/v2/kling-v2-5A-three-offices-dolly.mp4`

```
Slow dolly forward toward the three glass-fronted offices, the office signage strip and interior details sharpening as the camera approaches. Preserve office layout, glass reflections stable, keep proportions and signage strip aligned. Warm interior lighting from upper-left unchanged, polished concrete floor reflection. Cinematic stabilised motion. 5 seconds, hold final frame.
```

---

## 7 — Slot 5C — Finance manager desk top-down zoom-in

**Input still:** `still-v2-5C-finance-desk.png`
**Save as:** `motion/v2/kling-v2-5C-finance-zoom.mp4`

```
Slow top-down zoom-in onto the loan contract page on the finance manager desk, the calculator and pen beside it staying in frame, paper grain and contract details sharpening as the lens descends. Preserve desk layout, maintain proportions, keep paper grain. Warm desk lamp light from upper-left unchanged. Documentary realism. 5 seconds, hold final frame.
```

---

## 8 — Slot 5D — Three-tier holdback chiaroscuro slide ⭐ FLAGSHIP

**Input still:** `still-v2-5D-holdback-three-tier.png`
**Save as:** `motion/v2/kling-v2-5D-holdback-chiaroscuro.mp4`

```
Slow lateral camera slide from right to left across the three-tier paper stack, dramatic warm orange light shifting subtly to reveal more of the bottom hidden paper edge as the camera moves. Preserve top paper crisp lighting, middle paper transitioning between shadow and light, bottom paper barely visible. Maintain stack alignment and proportions. Cinematic chiaroscuro stabilised motion. 5 seconds, hold final frame.
```

---

## 9 — Slot 6A — Bank pre-approval letter slow camera tilt

**Input still:** `still-v2-6A-bank-letter.png`
**Save as:** `motion/v2/kling-v2-6A-bank-letter-tilt.mp4`

```
Slow camera tilt up from the bottom signature line of the bank pre-approval letter to the institutional letterhead at the top, document staying flat on the leather portfolio, fountain pen and signet remaining in frame. Preserve paper grain, leather grain, letterhead layout. Maintain proportions and warm directional light from upper-left. Premium banking documentary aesthetic. 5 seconds, hold final frame.
```

---

## 10 — Slot 6C — Dealership window slow pull-back reveal

**Input still:** `still-v2-6C-window-banner.png`
**Save as:** `motion/v2/kling-v2-6C-window-banner-pull.mp4`

```
Slow camera pull-back from the finance banner inside the dealership glass facade, gradually revealing more of the showroom interior with the cars parked inside coming into view. Preserve banner layout and percentage symbol, keep glass reflections stable, maintain awning shape and showroom proportions. Late-afternoon golden hour warm light, soft anamorphic flare. Documentary observational tone. 5 seconds, hold final frame.
```

---

## Per-clip QC checklist

After each Kling render preview, before downloading:

- [ ] No warped text or morphing letters in any visible signage/papers
- [ ] No hallucinated figures (people in reflections, shadows that look like people)
- [ ] No sudden zoom or aggressive motion (smooth slow movement only)
- [ ] No melting edges or geometry distortion
- [ ] Subject identity preserved (the still's main subject doesn't drift)
- [ ] Palette stays charcoal/cream/orange (no shift mid-clip)
- [ ] **Watermark toggle is OFF before download** — TICK "No watermark" checkbox

Re-roll if any check fails. If 3 rolls all fail on the same prompt, ping me and we'll adjust the prompt.

---

## Cost + time budget

- 10 Kling clips × ~$0.10-0.40 per clip = **~$2-4 AUD** in Kling Starter credits (well under monthly quota)
- Render time: 5-15 min per clip — submit them in parallel via Kling's queue if possible
- Total wall-clock: ~30 min if running in parallel, ~2 hr if sequential

---

## What comes after Kling

Once all 10 motion clips are saved to `motion/v2/`:

1. **Storyblocks B-roll** (13 clips) — search/download per the [v01-motion-plan.md](v01-motion-plan.md) per-scene B-roll list. Save to `motion/v2-broll/`.
2. **Storyblocks cash for 5E** — search "australian banknotes stack close-up", save to `motion/v2-broll/storyblocks-5E-cash-stack.mp4` (you can keep the MJ 5E render as backup).
3. **Storyblocks music bed** — search "calm confrontation instrumental cinematic" or "documentary tension piano", 11+ min track, save to `motion/v2-broll/music-bed.mp3`.
4. **CapCut assembly** — open the existing project, replace VO clips with new stitched 0.90 renders, layer in the new stills + Kling clips + Storyblocks B-roll per [`v01-motion-plan.md`](v01-motion-plan.md), apply Ken Burns variations, add dollar-figure text overlays, mix music bed at -38 LUFS.
5. **Export** 1080p MP4 to `final/v1-payment-not-price-pivot.mp4`.
6. **Submagic** — generate 3 Shorts cutdowns from the long-form (Magic Clips add-on).
7. **YouTube** upload with TubeBuddy SEO + auto-CC enables automatically.
8. **Blotato** cross-post the 3 Shorts to TikTok + IG Reels.

---

## Reference

- Built from canonical patterns in `saas-prompts/kling.md`
- All prompts use the 5-part order: Camera → Anchor → Action → Mood → Duration
- One camera move per clip, speed adjective mandatory
- Continuity guardrail line in every prompt
- Tight 30-50 word body
