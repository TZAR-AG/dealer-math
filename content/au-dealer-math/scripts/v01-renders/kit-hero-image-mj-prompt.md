# Kit landing page — hero image MJ prompt sheet

**Goal:** Generate a brand-on-brand background image for the AUDM 7-Lines cheatsheet landing page. Will sit as page background flanking the white form card (replacing the leopard-print Pierce default that we removed).

**Tool:** MidJourney v7 web (NOT Discord — different syntax)
**Locked formula:** [.claude/rules/design-system-audm.md](../../../.claude/rules/design-system-audm.md) + [saas-prompts/midjourney.md](../../saas-prompts/midjourney.md)

---

## Step 1 — open MJ web

Open https://midjourney.com/imagine in a fresh tab.

## Step 2 — set side panel options

Right panel / settings drawer:
- **Aspect Ratio:** `16:9` (landscape — fills the page bg)
- **Style:** `Raw` (mandatory — bypasses MJ beautification)
- **Scale (Stylize):** `80` (documentary realism — 250+ drifts to product ad)
- **Version:** `v7`
- **Variation Mode:** `Off` (or 0)
- **Style weight:** `200`

## Step 3 — upload palette reference

Style Reference field → **Upload file**:
`content/au-dealer-math/saas-prompts/_assets/audm-palette-swatch.png`

(For long-term reuse on V2-V12: also upload to Imgur once + save URL to `_assets/palette-swatch-url.txt`. Then drop the URL into the Style Reference field instead of re-uploading.)

## Step 4 — paste prompt body

```
Top-down close-up of an Australian car dealership purchase contract on a modern dark grey laminate office desk surface, cream printed paper page with realistic small printed legal clauses in tight columns, one specific clause near the upper third highlighted with a single thin horizontal orange marker stroke, a black ballpoint pen rests at the lower right edge slightly off-center and angled, soft natural light from upper left, subtle film grain, Alec Soth photography style, shot on Kodak Portra 400, Hasselblad 500CM medium format, available light only, quiet observational documentary realism
```

## Step 5 — paste exclude / negative prompt

In "Exclude these" / "Things to avoid" field:

```
text, watermark, logo, signature, typography, words, letters, captions, brand names, dealership signs, cartoon, illustration, 3D render, CGI, plastic skin, hyperdetailed, wood desk, rustic, workshop bench, manila folder, ceramic mug, warm wood tones, faces, persons, hands, glossy
```

## Step 6 — generate + pick winner

Submit. MJ generates 4 variants. Pick the one that passes:
- ✅ Faceless (no hands, no people)
- ✅ On-palette (charcoal desk, cream paper, single orange stroke — nothing else)
- ✅ Modern dark grey laminate desk (NOT wood / NOT rustic)
- ✅ Australian-coded (no US licence plates, no luxury-mag aesthetic)
- ✅ One single highlighted line (NOT decorated all over)

If all 4 fail any of these → re-roll (don't iterate the prompt blind — the formula's locked).

## Step 7 — Upscale Subtle (mandatory)

On the winner: click **Upscale Subtle** (NOT Creative). Wait ~15-30 sec. Download.

Result: ~2912×1632 PNG. Subtle preserves doc aesthetic; Creative drifts palette.

## Step 8 — save to repo

Save the upscaled PNG to:
`content/au-dealer-math/scripts/v01-renders/stills/v2/kit-hero-cheatsheet-bg.png`

Then ping me — I'll upload it to Kit as the page background and re-preview.

---

## Reference

- Design system: `.claude/rules/design-system-audm.md`
- Per-tool prompt canon: `content/au-dealer-math/saas-prompts/midjourney.md`
- Palette swatch source: `content/au-dealer-math/saas-prompts/_assets/audm-palette-swatch.png`
- Generator: `generator/au-dealer-math/generate-palette-swatch.py`
