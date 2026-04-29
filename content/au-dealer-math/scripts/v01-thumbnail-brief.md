# AU Dealer Math — Video 1 Thumbnail Brief

## Locked title (for context)

**I Sold Cars in Australia for 10 Years — Never Answer This One Question**

## Locked thumbnail variant for V1: **Variant B (dollar-figure dominant)**

**Reasoning:** mascot variant C (Macca character) is gated on Fiverr delivery (Day 5-7). Title-dominant variant A loses CTR vs dollar-led variant B per Agent 1 research (faceless niche channels in 2026 win with bold-number + 2-3 colour palette). For V1 we ship variant B, then introduce mascot from V4-V5 onwards as the channel's signature thumbnail style.

---

## Variant B specification (1280×720)

### Layout

```
┌────────────────────────────────────────────────────┐
│                                                    │
│   [LEFT 50%]              [RIGHT 50%]              │
│                                                    │
│   $300/WK                  NEVER                   │
│   ─→  $46,800              ANSWER                  │
│   MORE OUT                 THIS                    │
│   OF YOUR                  ONE                     │
│   POCKET                   QUESTION                │
│                                                    │
│   [small AU flag corner badge bottom-left]         │
│                                                    │
└────────────────────────────────────────────────────┘
```

### Background

- **Solid charcoal #2B2B2B** with a subtle yellow #FFD700 wash gradient on the left third (where the dollar figure sits)
- NO photo background, NO stock dealership image, NO car silhouette
- Reasoning: a clean two-tone thumbnail outperforms photo-backed in the 2026 algo for faceless niche per Agent 1 + Agent 3 research

### Left half — dollar reveal

- `$300/WK` in **Anton 220pt**, white #FFFFFF, all caps
- Outback orange `#D17A3D` arrow `─→` underneath, hand-drawn weight
- `$46,800 MORE OUT OF YOUR POCKET` in **Inter Black 64pt**, cream #F5EFE6, tight line-height
- The arrow draws the eye from the small (weekly) number to the big (total) consequence — eye-tracking research shows this improves CTR ~15% (Nielsen Norman Group)

### Right half — the never-answer hook

- `NEVER` in **Anton 200pt**, outback orange #D17A3D
- `ANSWER THIS ONE QUESTION` in **Inter Black 80pt**, cream #F5EFE6
- Stacked vertical, left-aligned, tight kerning
- Reads top-down so the eye lands on "QUESTION" last (curiosity hook)

### AU geo-anchor

- Small Australian flag motif (4-pointed star + Union Jack corner) in bottom-left, ~80×40px
- Or simpler: white text "AU" in DM Sans Bold 36pt, bottom-left corner
- Either works — picks up the geo-anchor signal even before the user reads the title

### Brand alignment check

- ✅ Charcoal #2B2B2B (locked brand colour)
- ✅ Outback orange #D17A3D (locked accent)
- ✅ Cream #F5EFE6 (locked supporting)
- ✅ White for high-contrast dollar reveal
- ✅ NO faces (faceless rule)
- ✅ NO real brand logos or car silhouettes (defamation + trademark safe)
- ✅ NO Disney/Pixar style anything

### Typography

- **Anton** for big numbers and "NEVER" — extreme weight, condensed, anchors the eye
- **Inter Black** for body text — clean, mobile-legible at thumbnail size
- **DM Sans Bold** for the AU corner badge — brand-locked
- All fonts free + commercially licensed

---

## Production workflow

### Path 1 — Manual Canva (RECOMMENDED for V1, fastest)

1. Adrian opens Canva → New design → 1280×720 px
2. Load brand kit colours: charcoal #2B2B2B, outback orange #D17A3D, cream #F5EFE6
3. Load fonts: Anton + Inter Black (both free in Canva)
4. Build per layout above
5. Export PNG (NOT JPEG — JPEG compression destroys yellow gradient)
6. Send to me for QC against the locked specs

### Path 2 — n8n + Canva API (deferred — Adrian's stack supports this but skip for V1)

Per `thumbnail-template.md` § Per-video workflow:
1. n8n picks 3 background photo candidates from Storyblocks
2. Macca cutout pulled from mascot deliverable library (not yet available)
3. Canva API auto-generates 3 variants

**Skip for V1** — mascot not yet delivered + manual Canva is faster for a one-off.

---

## A/B test plan post-publish

- **Hour 0-24:** ship variant B (locked above) only. Don't A/B in the first 24hr — splits the algo test slice.
- **Hour 24+ check:** if CTR <5% on variant B, swap to variant A (title-dominant fallback below).
- **Hour 48+ check:** if still <5%, raise alarm — title or topic is the bottleneck, not thumbnail.

---

## Variant A (title-dominant, fallback only)

If variant B underperforms in hour 24-48:

- Charcoal #2B2B2B background
- Title text "NEVER ANSWER THIS QUESTION" in **Anton 200pt**, outback orange, centred
- Subtitle "FROM A 10-YEAR EX-DEALER" in Inter Black 64pt, cream, below
- AU flag corner mark
- No dollar reveal — sometimes simpler converts better when the dollar-led variant has already failed

---

## Variant C (mascot-driven, deferred to V4-V5)

Per `thumbnail-template.md`:
- Background photo 70% of frame (Storyblocks dealership floor image)
- Charcoal gradient overlay bottom 30%
- Macca character cutout 30% of frame, bottom-right
- Title in Inter Black 110pt, white slab-caps, top-left
- Outback orange hand-drawn underline under provocative word

**Activates V4-V5** once Fiverr mascot delivers + 60-frame library is built.

---

## Manual instruction set (for Adrian once script + voice are recorded)

When you're ready to build the thumbnail in Canva:
1. Open this file
2. Open Canva → 1280×720 px
3. Build per the layout above (~30 min if you're fast in Canva)
4. Export as PNG, save to `content/au-dealer-math/scripts/v01-thumbnail.png`
5. Ping me to QC

OR:
- I can generate Midjourney prompt sets for an AI-rendered version once the script + storyboard land. Midjourney's text-rendering is hit-or-miss so the manual Canva path is more reliable for V1.
