# AU Dealer Math SaaS stack

## Per-task SaaS map (LOCKED 2026-04-30, post V1 ship)

What tool is used for what task across the V1-V12 production pipeline. **NB Pro NOT on this list — V1 shipped without it; V2-V12 don't need it.**

| Production task | Tool / approach | Cost incremental | Notes |
|---|---|---|---|
| Script writing | Claude / manual | $0 | Adrian-driven; reference content/au-dealer-math/scripts/ |
| Voiceover generation | **ElevenLabs** (Paul voice, locked settings) | $0 (in stack) | regenerate-vo.js · stitching DISABLED · seed=42424242+i |
| VO master concat | **ffmpeg `acrossfade`** (local) | $0 | build-master-vo.py · 200ms tri crossfades · ONE master VO file |
| AI image generation (stills + thumbnail backgrounds) | **MidJourney v7** | $0 (in stack) | engineered prompts at saas-prompts/midjourney.md |
| AI video generation (motion clips of stills) | **Kling 3.0** | $0 (in stack) | 5s motion clips of selected MJ stills |
| Stock B-roll / motion (when AI insufficient) | **Storyblocks All-Access** | $0 (in stack) | $100/mo · download under license |
| Music bed | **Storyblocks All-Access** | $0 (in stack) | Pre-ducked + looped via ffmpeg crossfade |
| Ken Burns animation on stills | **ffmpeg `zoompan`** (local) | $0 | 4× lanczos pre-scale anti-shake · bake-stills.py templates |
| Video editing / timeline assembly | **DaVinci Resolve 20 Free** | $0 | Py3 console scripting · build-v0X-davinci.py |
| Video export | **DaVinci Deliver** (scripted) | $0 | render-v1-davinci.py · YouTube 1080p preset · MarkIn/Out override |
| Captions (long-form) | **YouTube auto-CC** | $0 | Adrian rejected Submagic for AUDM long-form |
| Captions (Shorts) | YouTube auto-CC OR **Submagic** (already in stack for SS) | $0 | Submagic already paid for SS — reuse for AUDM Shorts if kinetic captions desired |
| Channel banner PNG | **Python + PIL** (generate-channel-banner.py) | $0 | 2560×1440 · brand colors locked · DM Sans Bold |
| Channel logo / watermark | **Python + PIL** (generate-channel-logo.py) | $0 | AUDM monogram · 800×800 master + 150×150 watermark |
| Thumbnail base imagery | **MidJourney v7** | $0 (in stack) | 16:9 · style raw · 4 variants per video |
| Thumbnail composite + text | **Python + PIL** (thumbnail-engine.py) | $0 | 3 locked templates: Big-Number / Comparison / Document Forensics |
| Thumbnail A/B testing | **YouTube Studio native** | $0 | Free, supports 3 variants/video · 2.3× CTR uplift documented (Thumbify 2026) |
| Shorts cuts | **ffmpeg** (render-v1-shorts.py) | $0 | Centre-crop 16:9 → blur-pad 9:16 + burnt-in caption + CTA overlay |
| Lead magnet PDF generation | **Node + Puppeteer** (generator/au-dealer-math/build-lead-magnet.js) | $0 | HTML→PDF · 7-lines cheatsheet |
| **Lead magnet hosting** | **Kit landing page** | $0 (in SS stack) | NOT Stan, NOT Vercel — Kit's tag+sequence is optimal for free PDF in education niche (Embeddable 2026) |
| Email nurture sequence | **Kit** (in SS stack) | $0 | content/au-dealer-math/kit-nurture-sequence.md |
| Cross-platform scheduling | **Blotato** (in SS stack) for IG/TikTok cross-post; **YouTube Studio** native for YT | $0 | Native uploads only — no auto-cross-share |
| YouTube SEO optimization | **TubeBuddy Pro** | $0 (in stack) | Tag Explorer · Best Practices audit · A/B test |
| YouTube analytics | **YouTube Studio** + **TubeBuddy Channelytics** | $0 | Realtime + retention curves · most-replayed graph |
| YouTube comment management | **YouTube Studio** native | $0 | Reply within 2 hrs first 48 hrs (15-20% reach lift documented) |
| Pronunciation dictionary | **In-script phonetic respelling** (NOT ElevenLabs PD — Pro tier only) | $0 | Phonetic respelling in script text instead of API attachment |

## NB Pro decision (LOCKED 2026-04-30)

Nano Banana Pro is **NOT in the AUDM stack**. Adrian was out of credits when V1 shipped — V1 shipped fine without it via MJ + Python+PIL. Per 2026 research (NightCafe, SpectrumAI):

- NB Pro's strength = single-shot photorealism + text-in-image consistency
- AUDM's need = LOCKED brand typography + repeatable layout = OPPOSITE
- "Language-driven Photoshop" framing argues AGAINST NB Pro for branded series production
- For one-off SS hero images later, MAY revisit upgrade. Not for AUDM V1-V12.

## Recurring monthly subscriptions — LOCKED 2026-04-29

**All 7 tools confirmed monthly recurring (no annual prepays).** Adrian verified 2026-04-29.

| # | Tool | Plan | AUD/mo | Status |
|---|---|---|---|---|
| 1 | n8n cloud | Starter | **$42.25** | ✅ LIVE — monthly recurring |
| 2 | InVideo AI | **Max → DOWNGRADING to Plus** | ~~$144.88~~ → **~$25** | 🟡 Adrian emailed for refund 2026-04-29 (research: clip extraction license-blocked) |
| 3 | Midjourney | Standard | **$46.01** | ✅ LIVE — monthly recurring |
| 4 | Kling 3.0 | Starter | **$11.17** | ✅ LIVE — monthly recurring |
| 5 | Submagic | **Starter + Magic Clips** | **$58.00** | ✅ LIVE — Magic Clips add-on added 2026-04-29 (research: bare Starter 2-min cap kills Shorts workflow) |
| 6 | TubeBuddy | Pro | **$20.91** | ✅ LIVE — monthly recurring |
| 7 | Storyblocks | All-Access | **$100.00** | ✅ LIVE — monthly recurring |
| 8 | ElevenLabs | **Starter** (corrected 2026-04-29) | $0 incremental | ✅ LIVE on hello@thestructuredself.com (single ElevenLabs account, shared with SS). Memory previously incorrectly said "Creator" — verified Starter via dashboard chat agent 2026-04-29. Pronunciation Dictionaries gated behind Creator tier. AUDM uses phonetic respelling in script text instead. Upgrade to Creator (~$33 AUD/mo Adrian-side) only if multi-pronunciation-dict workflow becomes essential. |
| 9 | Claude API | Usage-based | ~$15-30 AUD/mo | ✅ LIVE on existing console.anthropic.com |
| | **Total monthly recurring (post downgrades)** | | **~$329 AUD/mo** | (incl Claude API estimate; saves ~$89 vs original $418) |
| | **Confirmed fixed (excl Claude usage)** | | **~$303.34 AUD/mo** | (after InVideo Max→Plus + Submagic +Magic Clips) |

**Note on AUD vs published USD pricing:** several tools charge AU customers more than published USD retail. Likely combination of GST/regional pricing/conversion markup. The figures above are what AUDM pays — use these for P&L, not USD retail estimates.

## One-time costs

| Item | USD | AUD | Timing |
|---|---|---|---|
| Fiverr mascot illustrator | $200 | $307 | Day 1 |
| Fiverr AU voice actor | $80 | $123 | Day 1 |
| Channel banner / intro animation | $50 | $77 | Day 1 |
| AU trademark filing (mascot + wordmark, single class) | $215 | $330 | At Video 5 publish |
| **Total upfront pre-Day-1** | **$330** | **$507** | |
| **Total at Video 5** | **+$215** | **+$330** | |
| **Year 1 one-time total** | **$545** | **$837** | |

## Year 1 cost projection

- One-time: $837 AUD
- Recurring × 12: $5,000-5,184 AUD
- **Year 1 total:** ~$5,800-6,000 AUD
- **Break-even at $1K AUD/mo target:** month 6 (cumulative breakeven), month 3-4 (operating breakeven)

## Voice IDs (LOCKED 2026-04-29)

**Pivot:** dropped Fiverr voice + PVC plan in favour of ElevenLabs Voice Library stock voice. Saves $270 AUD upfront, eliminates 3-5 day source-recording delay, professional library quality.

- **Macca voice (LOCKED FOR LIFETIME OF CHANNEL):** Paul — Australian Professional Presenter
- **Voice ID:** `WLKp2jV6nrS8aMkPPDRO`
- **Type:** ElevenLabs default library voice (multilingual)
- **Descriptor:** "Australian, Male, Professional Presenter, Multilingual"
- **Settings (research-locked for stock library voice — different from PVC):**
  - Model: **Eleven Multilingual v2** (NOT v3 — v3 not optimised for library voices yet)
  - Stability: **0.40** (lower = less performative, more "talking-to-a-mate" cadence; raise to 0.55 if first render reads too loose)
  - Similarity: **0.75**
  - Style: **0.25**
  - Speaker Boost: **ON**
  - Speed: **0.95** (slightly slower than 1.0 for explainer cadence)

**Same-voice-forever rule:** Paul = Macca for V1 → V100. NO voice transitions. Channel brand consistency = same outcome as a custom clone, $0 cost.

## Lead magnet delivery

- _populated after Task 11 (Stan Store setup)_

## API key audit cadence

Monthly health-check (mirror `analytics-pull.md` § Token refresh flows) — first Monday of each month.
