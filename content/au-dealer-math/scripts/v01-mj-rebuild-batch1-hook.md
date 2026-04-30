# V1 Rebuild — MJ Prompt Batch 1: Hook (0:00–0:20)

**Section target:** ~7 cuts at 3s avg (per locked cadence rules — hook is fastest section)
**KB zoom intensity:** 15-18% (per duration table — 3s clips need punch)
**Existing assets to reuse:** kling-clip-1-hook.mp4 (5s motion)
**New MJ stills needed:** 6
**Total runtime to fill:** 20.1s (actual VO duration)

## VO timeline (Whisper-locked)

| Time | Macca says |
|---|---|
| 0:00–0:03 | "If a car salesperson asks you, what's your weekly budget?" |
| 0:03–0:04 | "They've already won." |
| 0:04–0:06 | "The deal is over." |
| 0:06–0:07 | "You just don't know it yet." |
| 0:07–0:09 | "I sold cars in Australia for 10 years," |
| 0:09–0:14 | "and I asked that question to nearly every customer who walked through the door." |
| 0:14–0:16 | "In the next eight minutes," |
| 0:16–0:20 | "I'll show you what happens behind the desk after you answer." |

## Visual slot map

| Slot | Time | Duration | Asset | KB |
|---|---|---|---|---|
| H1 | 0:00–0:03 | 3.0s | **REUSE** kling-clip-1-hook.mp4 (motion) | n/a |
| H2 | 0:03–0:06 | 3.0s | **NEW** MJ — Hand pointing to weekly figure on contract | zoom-in 16% |
| H3 | 0:06–0:08 | 2.0s | **NEW** MJ — Empty showroom at dusk | zoom-out 18% |
| H4 | 0:08–0:11 | 3.0s | **NEW** MJ — Clock + papers on desk | zoom-in 16% |
| H5 | 0:11–0:14 | 3.0s | **NEW** MJ — Long dealership floor walk perspective | pan-right 15% |
| H6 | 0:14–0:16 | 2.0s | **NEW** MJ — Customer's back walking through door (silhouette) | zoom-in 18% |
| H7 | 0:16–0:20 | 4.0s | **NEW** MJ — Back-office corridor with three closed doors | zoom-in 14% |

## MJ web settings (configure once, persists for batch)

- **Aspect Ratio**: 16:9
- **Style**: Raw
- **Scale**: 80
- **Version**: v7
- **Variation Mode**: Off
- **Exclude / "things to avoid"** field:
  ```
  text, watermark, logo, signature, typography, words, letters, captions, brand names, dealership signs, cartoon, illustration, 3D render, CGI, plastic skin, hyperdetailed, people, faces, full figures, smiling, professional, commercial photography, studio lighting, octane render, unreal engine, 8K, cinematic, masterpiece
  ```

After each generation: **Upscale Subtle** before downloading.

---

## H2 — Hand pointing to weekly figure on contract (0:03–0:06)

**Subject anchor:** salesperson's hand pointing to a single column of weekly payment figures on a printed loan contract.

```
Documentary photograph, extreme close-up of a salesperson's hand holding a black ballpoint pen pointing to a single highlighted column on a printed loan contract, the column labeled "WEEKLY" clearly visible at the top, faceless composition cropped at wrist only, the contract paper has visible texture and a slight curl on the right edge, single overhead practical light raking from upper-left, deep oblique shadow falling right, shallow depth of field f/2 focused on the pen tip. Alec Soth quiet observational style, Kodak Portra 400 35mm film, organic grain, paper grain visible. Limited palette: charcoal #2B2B2B (60%), cream #FAF7F2 (30%), outback orange #C8612C (10% — only on a single highlighter mark on the column). Unpopulated, no figures, no faces, no full hands, only the wrist and pen visible. 16:9 widescreen.
```

**Save as:** `stills/auto-v2/hook-h2-weekly-column.png`

---

## H3 — Empty AU showroom at dusk (0:06–0:08)

**Subject anchor:** AU dealership at dusk, atmospheric, sense of "deal is over."

```
Documentary photograph, AU automotive dealership exterior at late dusk, two parked sedans visible through floor-to-ceiling showroom window glass, illuminated showroom floor inside, the outside dim and atmospheric, melancholic late-day mood, no figures inside the showroom, no figures outside on the lot. Wim Wenders road photography style, CineStill 800T tungsten balance, halation around showroom interior lights, subtle film grain. Limited palette: charcoal #2B2B2B (70%), cream #FAF7F2 (20% — interior glow), outback orange #C8612C (10% — single sodium streetlight on the right edge). Unpopulated, no figures, no people, no readable signage on the building. 16:9 widescreen.
```

**Save as:** `stills/auto-v2/hook-h3-showroom-dusk.png`

---

## H4 — Clock + contract on desk (0:08–0:11)

**Subject anchor:** time passing, "deal is over" closure imagery.

```
Documentary still life photograph, an analog clock face with brass numerals on a worn cream laminate desk, the minute hand visibly pointing to 4:45 position, a printed loan contract document partially under the clock with paper edges visible, a black ballpoint pen resting diagonally across the contract. Top-down 75-degree angle, shallow depth of field f/2.8 focused on the clock face, late afternoon practical window light raking from upper-left, deep oblique shadow falling right, paper grain visible. Stephen Shore American color documentary style, Kodak Portra 400 35mm film, organic grain, lifted shadows. Limited palette: charcoal #2B2B2B (55%), cream #FAF7F2 (35%), outback orange #C8612C (10% — single small brass accent on the clock's hour indicators). Unpopulated, no figures, no faces, no readable text on the contract. 16:9 widescreen.
```

**Save as:** `stills/auto-v2/hook-h4-clock-contract.png`

---

## H5 — Long dealership floor perspective (0:11–0:14)

**Subject anchor:** "10 years selling cars" — establishing authority.

```
Documentary photograph, deep one-point perspective view down a long AU automotive dealership showroom floor, polished concrete floor receding to vanishing point, four to six SUVs and sedans parked in geometric arrangement on each side, large floor-to-ceiling windows on both walls, manufacturer banners overhead but text intentionally illegible/blurred. Shot at 4pm — low warm Australian afternoon sun raking from upper-left, long oblique shadows across the floor. Single 24mm wide-angle lens, low eye-level, deep depth of field. Stephen Shore American color documentary style, Trent Parke Australian suburban realism, Kodak Portra 400 35mm film grain. Limited palette: charcoal #2B2B2B (60%), cream #FAF7F2 (30%), outback orange #C8612C (10% — only on a single rebate banner edge). Unpopulated, no figures, no people, no reflections of people in glass. 16:9 widescreen.
```

**Save as:** `stills/auto-v2/hook-h5-dealership-perspective.png`

---

## H6 — Customer's back through doorway (0:14–0:16)

**Subject anchor:** "every customer who walked through the door" — anonymous customer arrival.

```
Documentary photograph, low angle behind silhouette outline of an unidentified customer carrying a folder walking through the open glass door of a dealership, only the back of a shoulder and a folder visible, customer's head and face NOT visible, cropped at upper shoulder, glass door reflecting the Australian late-afternoon light, polished concrete floor visible inside. Shallow depth of field f/2 with focus on the door threshold. Trent Parke harsh Australian contrast, Kodak Portra 400 35mm film, organic grain. Limited palette: charcoal #2B2B2B (65%), cream #FAF7F2 (25%), outback orange #C8612C (10% — single dealership tab on the door edge). Faceless composition, no faces visible, no full figure, only a back-shoulder silhouette. 16:9 widescreen.
```

**Save as:** `stills/auto-v2/hook-h6-customer-doorway.png`

---

## H7 — Three closed doors corridor (0:16–0:20)

**Subject anchor:** "what happens behind the desk" — teaser for the three rooms reveal.

```
Documentary photograph, cinema-verité interior view of a long dealership back-office corridor with three closed doors evenly spaced down the right wall, polished cream linoleum floor, dim warm overhead practical light at the far end, single charcoal door handle on the nearest door catching a subtle highlight. One-point perspective receding to vanishing point. Shot at f/4 with shallow depth of field focused on the nearest door. Robert Frank documentary style, Kodak Portra 400 35mm film, organic grain, slight halation in highlights. Limited palette: charcoal #2B2B2B (65%), cream #FAF7F2 (25%), outback orange #C8612C (10% — single tab visible on the nearest door). Unpopulated, no figures, no faces, no readable signage on doors. 16:9 widescreen.
```

**Save as:** `stills/auto-v2/hook-h7-three-doors-corridor.png`

---

## Workflow

1. Open MJ web (midjourney.com/imagine)
2. Configure right-panel settings (one-time): Aspect 16:9, Style Raw, Scale 80, v7, Variation Off
3. Paste exclude block into "Things to avoid" field (one-time)
4. For each prompt H2-H7:
   - Paste prompt body in textarea
   - Submit
   - Wait ~60 sec for 4 variants
   - Pick the cleanest faceless variant matching brief
   - Click **Upscale Subtle**
   - Wait ~30 sec
   - Right-click → Save As → save to `c:\Users\adria\Downloads\` with target filename
5. Tell me when batch 1 is done; I'll move them to `stills/auto-v2/` and start ffmpeg-baking the KB MP4s

**Time estimate:** ~12-18 min for the 6 prompts (90 sec generate + 30 sec upscale + 30 sec save per prompt).
