# AU Dealer Math — Channel Trailer (v0, 45 sec)

Auto-plays for non-subscribers on the channel page. Sub-conversion lever distinct from V1 itself (V1 is too long to use as trailer).

## Spec
- **Duration:** 45 sec
- **Aspect:** 16:9 (1920×1080)
- **Voice:** Mac (ElevenLabs Paul, locked settings — same as V1)
- **Music:** same bed as V1, ducked -22 dB under VO
- **Visuals:** lifted from V1 footage (no new MJ/Kling generation needed)
- **Cover frame:** 0:00-0:01 — "I sold cars in Australia for 10 years."

## Script (paste into render pipeline as scene-trailer.mp3)

```
I sold cars in Australia for ten years.

I watched the same dealership tricks land the same customers, every week.

This channel runs the numbers behind those tricks.

Drive-away pricing. Novated leases. Trade-in lowballs. Finance manager margins. The seven lines on a contract you should never sign.

Everything I learned on the dealer side. Made for the buyer side.

I'm Mac. New explainers Mon, Wed, Fri.

Subscribe so you don't get burned at your next dealership visit.

A. U. Dealer Math.
```

Word count: ~85 words. At Mac's locked 0.95 speed = ~32-35 sec spoken + ~10 sec breathing room with music outro = ~45 sec total.

## Visual cuts (lifted from V1 baked assets)

Re-uses existing renders — no new bakes needed.

| Time | Visual | Source |
|---|---|---|
| 0:00-0:05 | M1 hook motion (kling-clip-1) | `motion/kling-clip-1-hook.mp4` |
| 0:05-0:13 | Three rooms three offices | `motion/baked/v2-mj/mj-v2-5A-three-offices-dolly-baked.mp4` |
| 0:13-0:20 | Cars comparison | `motion/baked/kb/still-3-cars-comparison-kb-8s.mp4` |
| 0:20-0:28 | Total cost reveal | `motion/baked/kb/still-v2-6B-total-cost-comparison-kb.mp4` |
| 0:28-0:35 | Confident customer | `motion/baked/kb/still-5-confident-customer-kb-12s.mp4` |
| 0:35-0:42 | Subscribe-prompt overlay frame: dealership-dusk + "Subscribe Mon/Wed/Fri" overlay | `motion/baked/kb/still-v2-7B-dealership-dusk-kb.mp4` |
| 0:42-0:45 | AUDM logo card | `brand/au-dealer-math/channel-logo-transparent.png` over charcoal |

## Build path (when Adrian wants to ship the trailer)

1. Render trailer VO:
   ```
   node generator/au-dealer-math/render-trailer-vo.js
   ```
   (Use same ElevenLabs settings as V1 scene VOs. New script file mirroring `render-scene-7-only.js` with the trailer text + seed=42424256.)

2. Build trailer timeline in DaVinci:
   - Reuse `build-v1-davinci.py` pattern
   - SCENES dict has one scene (trailer)
   - VISUAL_TRACK has the 7 cuts above
   - Music bed at -22dB, full duration
   - Export 1080p MP4 via `render-v1-davinci.py` pattern (same render config)

3. Upload to YouTube as Unlisted, set as channel trailer in Studio → Customisation → Layout → Video spotlight.

## Status

- [ ] VO rendered
- [ ] Timeline built
- [ ] Exported
- [ ] Set as channel trailer in Studio

Trailer is **post-V1-publish work** — V1 ships first, trailer follows within 7 days.
