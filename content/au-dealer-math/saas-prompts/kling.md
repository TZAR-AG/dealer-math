# Kling 3.0 — AUDM canonical prompt reference

**Engine:** Kling 3.0 (Feb 2026 release). Standard mode for default; Pro mode burns extra credits for hero shots.
**Tier:** Starter $11.17 AUD/mo per `saas-stack.md` (paid tier — supports watermark-free downloads).
**Use AUDM for:** image-to-video motion punctuation. 5-8 sec clips between long-hold stills. ~10% of total runtime, NOT carpet motion.
**ALWAYS use Image-to-Video** (I2V) — feed NB Pro / Midjourney stills as input.

---

## Prompt skeleton (5-part order, mandatory)

**Word count target: 20–50 words.** Above 50 starts hallucinating; above 300 triggers full breakdown.

```
Camera: [ONE move, with speed adjective]
Anchor: preserve [subject] shape, scale, and any visible label text
Action: [single subtle physical beat, anchored to an object]
Mood: [documentary lighting cue + texture cue]
Duration: 5s, hold final frame
```

**Three load-bearing rules:**

1. **One camera move per clip — never two.** "Slow push-in then pan right" = #2 most expensive mistake. Split into two clips instead.
2. **Speed adjective is mandatory:** `slow`, `gentle`, `subtle`, `micro`, `smooth`. Without it Kling improvises and warps.
3. **Continuity guardrail line every prompt:** *"preserve silhouette, maintain label text, keep proportions, maintain scale."* Single highest-leverage anti-warping line.

---

## Watermark removal — the actual fix

Earlier today we got watermarked Kling output despite Starter tier. Per research, root cause:

**Kling does NOT auto-strip the watermark.** After generation, the **Download** button opens a dialog with a checkbox labelled *"No watermark"* (sometimes "Remove watermark"). Multiple sources flag this as *"the #1 missed feature causing paid subscribers to think they're still getting watermarks."*

**The toggle does NOT persist between sessions** — tick it every render.

**SOP:** generate → preview → click Download → **TICK "No watermark"** → confirm → save.

If the toggle is missing entirely on a clip, the clip was generated under a free-tier session (browser logged out). Re-generate inside an authenticated paid session.

---

## Motion verbs — work vs fail

### Work cleanly (use these)

- Slow dolly in / slow dolly push / **macro dolly-in**
- Slow camera pan (left/right) — specify direction
- Slow tilt up / slow tilt down
- Static tripod shot with subtle parallax
- Slow pull-back reveal
- Slow push-in
- Tracking shot (lateral follow)
- Crane up / crane reveal
- Rack focus from foreground to background
- Steadicam float

### Fail / cause warping

- "Dynamic," "rapid," "energetic" camera moves on documentary stills (pushes Kling into action latent space; it starts hallucinating subjects)
- Two moves in one clip ("dolly-in and pan")
- "Camera moves" / "camera goes" / "scene transitions" — too vague, it improvises
- "Zoom" without "slow" qualifier — produces sudden zooms
- Aggressive verbs ("crashes through," "rushes," "snaps to")
- POV / handheld / FPV drone language on still-life inputs (will fabricate motion-blur and hallucinated scenery)

---

## Negative prompt block (paste in negative prompt field every render)

```
warped text, morphing letters, melting edges, distorted documents, hallucinated figures, sudden zoom, motion blur trail, plastic over-smooth, low quality artifacts, flickering
```

**Don't write "no warping" — Kling's negative field auto-treats input as "avoid this."** Just write the symptom: "warping" not "no warping". Same for figures: "extra people" not "no extra people."

Going past 15 negative terms produces lifeless output. Stay ~10.

---

## Five validated AUDM motion prompts (drop-in ready)

**Format:** Body prompt below + paste the negative prompt block in the Kling negative field.

### 1. Open training binder (Scene 3 — Road to a Sale reveal)

```
Slow dolly push into the open binder centre spread. Preserve page layout, 
keep text crisp on the page, maintain paper grain. Subtle highlight glow 
rolls across the page from left as a shaft of late-afternoon office light 
shifts. Documentary 35mm look, soft directional warm key, faint dust motes. 
5s, hold final frame.
```

### 2. Split-screen loan paper stacks (Scene 4 — 4yr vs 7yr math)

```
Static framing with micro parallax — left stack of loan papers shifts subtly 
forward, right stack of cash documents holds. Preserve all text and label 
positions, maintain scale and silhouette. Cool overhead daylight on left, 
warm desk-lamp pool on right. Documentary realism, faint paper-fibre texture. 
5s.
```

### 3. Three-tier holdback chiaroscuro (Scene 5 — FLAGSHIP REVEAL)

```
Slow tilt up across three stacked envelopes labelled VFACT, KICKBACK, BONUS. 
Preserve label text, keep proportions and stack alignment. Single hard 
side-key from left, deep shadow falling right, dust in the beam. Macro 
dolly-in finishes on the top envelope. Documentary 35mm grain. 5s.
```

### 4. Luxury sedan turntable with model-cycle replacement (Scene 4 — GFV)

```
Slow horizontal pan around stationary sedan, faint parallax on the dealership 
backdrop. Preserve vehicle silhouette, paint colour, badge and grille shape. 
Studio key from upper right, cool rim light, polished concrete reflection 
underneath. Cinematic automotive documentary tone. 5s, no zoom.
```

### 5. Dealership window with finance banner (Scene 6 — fix close)

```
Slow pull-back reveal from finance banner text out to full glass facade. 
Preserve banner layout and lettering, keep glass reflections stable, 
maintain awning shape. Late-afternoon golden hour, warm window glow, soft 
anamorphic flare. Documentary observational tone. 5s, hold final frame.
```

---

## Failure modes + mitigations

| Failure mode | Mitigation |
|---|---|
| Documents/paper text morphs to gibberish | Add positive guardrail "preserve text, maintain label" + "warped text, morphing letters" to negative. **If still bad: composite real text in CapCut over the clip.** Kling cannot render legible text reliably — accept it and post-comp. |
| Calculator displays / signage text scrambles | Same — generate without trying to enforce numerals, comp digits/text in post |
| Subject identity drifts mid-clip | I2V always (we already do this); keep the input still uncluttered, centred, well-lit; reduce motion intensity language ("slow," "subtle," "micro"); add "preserve silhouette" |
| Hallucinated figures appear | Drop POV/handheld/FPV/crowd language; add "static framing" or "tripod shot"; negative-prompt "extra people, hallucinated figures" |
| Sudden zooms / dramatic motion you didn't ask for | Add "slow" qualifier to every move; cap at one move per clip; add "no sudden zoom" to negatives |
| Palette shifts off-brand mid-clip | Lock with "maintain palette, consistent lighting"; specify 2-3 brand colours in lighting cue ("warm tungsten + cool window blue") |
| Cramming kills the clip in 5s | Two-to-three beats max in 5s. Dialogue cap: 8-12 words. One camera move only. |

---

## Standard vs Pro vs 3.0 Omni — when to use each

- **Kling 3.0 Standard (V3):** AUDM default. Best for prompt-first I2V on still inputs. Up to 15s, 1080p on Standard plan, multi-shot capable. Use for every motion-punctuation clip we ship.
- **Kling 3.0 Pro (Professional Mode):** same V3 model, more sampling budget per gen. Worth the extra credits when a hero clip is failing standard mode at 3+ rerolls. Don't default — burn credits.
- **Kling 3.0 Omni (O3):** built on the O1 architecture, supports **video reference input**. Skip until we want a recurring "Macca's animated chart" or recurring character lock across episodes. Overkill for current AUDM workflow.

---

## SOP for AUDM Kling motion clip

1. Centre, crop, brighten, declutter the input still BEFORE upload (Kling reads cluttered inputs poorly)
2. Upload to klingai.com Image-to-Video page, select Kling 3.0 Standard
3. Paste 20-50 word prompt with 5-part order
4. Paste 10-term negative prompt block in negative field
5. Set: 5 sec duration, 16:9 aspect, motion strength medium, photorealistic-leaning style
6. Generate (5-15 min render time on Starter tier)
7. Preview — if warping/figures: re-roll with revised continuity guardrail
8. **Download → TICK "No watermark" → save to `motion/v2/`**
9. Verify clip is watermark-free by scrubbing in CapCut before timeline drop

---

## Validated patterns log

- 2026-04-29: 2 V1 motion clips generated (kling-clip-1-hook + kling-clip-3-cars-parallax). First batch had watermarks — root cause identified as missing "No watermark" toggle on download. Re-rendered correctly.
- *(append validated patterns after each render batch)*

---

## Sources

- [Kling 3.0 Prompting Guide — fal.ai](https://blog.fal.ai/kling-3-0-prompting-guide/)
- [Kling 3.0 Prompt Guide: Best Practices & Examples (2026) — klingaio.com](https://klingaio.com/blogs/kling-3-prompt-guide)
- [Kling 3.0 Reference Guide (2026) — magichour.ai](https://magichour.ai/blog/kling-30-reference-guide)
- [Mastering Kling 3.0: 10 Advanced AI Video Prompts — atlascloud.ai](https://www.atlascloud.ai/blog/guides/mastering-kling-3.0-10-advanced-ai-video-prompts-for-realistic-human-motion)
- [Hidden Secrets of Kling AI Prompting Playbook — InVideo](https://invideo.io/blog/hidden-secrets-of-kling-ai/)
- [12 Common Kling AI Prompt Mistakes & Fixes (2026) — videoai.me](https://videoai.me/blog/kling-ai-prompt-mistakes)
- [Kling AI Best Negative Prompts — Pollo AI](https://pollo.ai/hub/kling-ai-best-negative-prompts)
- [Kling AI Remove Watermark: All Effective Methods (2026) — gstory.ai](https://www.gstory.ai/blog/kling-ai-remove-watermark/)
- [Kling 3.0 vs Kling 3.0 Omni — PiAPI](https://piapi.ai/blogs/kling-3-0-vs-kling-3-0-omni-video-quality)
