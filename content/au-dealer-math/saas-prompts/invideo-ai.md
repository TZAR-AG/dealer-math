# InVideo AI — AUDM canonical prompt reference

> **🔴 ACTION ITEM: Downgrade Max → Plus before next billing cycle.**
> Max tier ($144 AUD/mo) cannot deliver the "auto-match B-roll → use in CapCut" workflow that justified its purchase — license restricts clip extraction. **Max-only feature actually needed: API access for n8n, which isn't built yet.** Plus ($25/mo, save ~$119/mo) covers AUDM scale. Re-upgrade only when (a) n8n pipeline is being built AND (b) AUDM has cleared 1K subs / first revenue OR (c) channel runs >12 videos/mo.

**Engine:** v6 / Agent One (proprietary stack). Built on Veo 3.1 for AI generation + iStock + Storyblocks-class library for stock matching.
**Tier (currently):** Max $144 AUD/mo (REVIEW — see action item above)
**Tier (recommended):** Plus $25 AUD/mo
**Use AUDM for:** **Final assembler** (recommended path) OR **shotlist research tool** (legal alternative). NOT a clip extractor.

---

## The license-blocker (critical context)

> *"You cannot download individual stock clips from InVideo for use in other tools... The license covers the finished video output, not the raw stock assets."* — InVideo Help Center

What this means for AUDM:
- Cannot rip MP4 clips out of InVideo's auto-assembled video for use in CapCut.
- The final assembled InVideo MP4 is licensed as an integrated whole (commercial use OK).
- Frame-by-frame screen recording + re-cutting in CapCut **violates iStock/Storyblocks licensing chain.**

Three legitimate paths:

| Path | What | Pros | Cons |
|---|---|---|---|
| **Final assembler** | Generate full video in InVideo, drop Paul VO via "upload audio", polish in their editor, export. Skip CapCut. | Single tool. License clean. | Less editorial control. AUDM aesthetic harder to lock vs CapCut. |
| **Shotlist research** | Generate auto-assembly. Screenshot the clip thumbnails it picks. Source equivalents from Storyblocks (paid sub) or Pexels (free). | Use InVideo's matching algorithm as creative director. | Paying $144/mo for inspiration is wasteful. |
| **Cancel + use Storyblocks Maker $30/mo** | Storyblocks lets you download licensed clips + use anywhere. | Workflow you originally wanted. | New tool to learn. |

---

## Prompt skeleton (Agent One scene-brief format)

InVideo AI reads prompts as **scene-based briefs**. The format that produces best B-roll auto-match:

```
Topic: [the subject in one literal sentence]
Audience: [who's watching — used to bias clip aesthetic]
Duration: [target seconds — controls scene count]
Style: cinematic documentary, [palette], handheld + slow push-in mix,
       no on-screen presenters, no talking heads, no text overlays,
       no captions burned in, faceless brand
Voice: skip — voiceover will be added externally
Music: skip — score added externally
Scenes: [n scenes, one literal sentence each describing what's
         visually happening, where, and the mood]
Footage instructions: real-world stock footage only. No AI-generated
                      avatars, no cartoon, no infographic overlays.
Geography: Australian context — RHD vehicles, AU number plates if
           visible, suburban dealership / coastal city / outback
           highway acceptable; reject US dealership exteriors,
           LHD interiors, European number plates.
```

**Three load-bearing tactics:**

1. **Scene-by-scene literal sentences beat one-sentence briefs.** A vague prompt produces generic stock; a 6-line scene list with specific verbs ("hands counting cash", "salesman pointing at screen", "drone over dealership lot at golden hour") locks the matcher.
2. **Negative prompts are mandatory.** InVideo will inject AI presenters, generic infographic overlays, and US-market footage by default. Phrase pattern that holds: `no AI avatars, no talking heads, no on-screen text, no infographic charts, no US dealerships`.
3. **Geography goes in the prompt every time.** AU stock library inside InVideo is thin (US/EU-skewed). Without explicit AU/RHD constraint, you'll get California Buick lots and Audi A6 dashboards with LHD steering.

---

## Five validated AUDM scene prompts

### Scene 1 — Hook
```
Topic: a salesman closing a car deal in an Australian dealership.
Style: cinematic documentary, charcoal/teal palette, handheld 24fps
       with shallow depth of field. No on-screen text. No avatars.
Scenes (5s each):
1. Close-up of a handshake across a desk in a glass-walled dealership.
2. Slow push on a buyer signing paperwork, pen visible, no face.
3. Wide of a suburban dealership lot at dusk, AU flagpoles if available.
Geography: Australian. Reject US showrooms.
```

### Scene 2 — Authority
```
Topic: a senior dealer principal walking a showroom floor at end of day.
Style: documentary, charcoal palette, slow tracking shots, contemplative.
Scenes: empty showroom lit warm, hands flipping a deal jacket,
overhead of a desk with calculator + manufacturer brochures,
neon "OPEN" sign flickering off.
No: presenters, charts, animated text.
```

### Scene 3 — Question
```
Topic: a confused buyer reading fine print on a finance contract.
Style: tight close-ups, charcoal/amber, handheld micro-shake.
Scenes: finger tracing a contract line, eyes squinting at small text,
calculator displaying a number, salesman mid-frame out of focus.
No on-screen text overlays.
```

### Scene 4 — Loan trick
```
Topic: showing money flowing from buyer to finance company to dealer.
Style: documentary, charcoal/teal, no infographics, no animated arrows.
Scenes: cash counted by hand, EFTPOS terminal beeping, finance
manager's office door closing, computer screen showing loan
application form (Australian, not US).
No: charts, graphs, presenter avatars.
```

### Scene 7 — Sign-off
```
Topic: a quiet dealership at closing time, Australian suburban.
Style: cinematic, charcoal palette, slow exterior dolly.
Scenes: sodium streetlights coming on, last car driving off the lot,
dealership sign powering down. Mood: contemplative, end-of-day.
```

---

## Tier features (for the downgrade decision)

### Plus ($25/mo) — recommended for current AUDM scale

- 50 min/mo generation (covers ~8-10 full V1-class videos)
- 80 iStock credits/mo
- 1080p export, watermark-free
- Brand kit
- Standard rendering speed
- **No API access** (matters when n8n is built — not now)

### Max ($144/mo) — review/downgrade

- 200 min/wk generation (~16x more than Plus)
- 320 iStock credits/mo
- 4K export + priority rendering + unlimited storage
- 5 brand kits
- **API access** (Max-only — for n8n)
- Agent One memory across episodes
- Justifies the price ONLY when: n8n is live AND running 15+ videos/mo OR multiple missions through one account

**Honest math at AUDM scale (V1→V12 over May, ~12 videos):** ~60 min generation total. Plus's 50/mo is tight but workable. Max is overkill until automation lands.

---

## Failure modes + mitigations

| Symptom | Cause | Fix |
|---|---|---|
| InVideo injects AI presenter despite faceless requirement | No explicit negative prompt | Add `no AI avatars, no talking heads, no presenters` to every scene brief |
| US dealership / LHD vehicles in output | No geography constraint | Add `Australian context, RHD vehicles, AU number plates, reject US dealership exteriors, LHD interiors` to every prompt |
| Generic stock clips (businessman shaking hands) | Brief too vague | Switch to scene-by-scene literal sentences with specific verbs |
| Want B-roll only but get full video assembly | InVideo always outputs assembled video | Either (a) accept and use as final assembler, or (b) screenshot thumbnails as shotlist + source from Storyblocks |
| Manual replacement of 30-50% of B-roll | Stock library doesn't have AU automotive niche depth | Pre-acceptance — for niche topics InVideo's library is thin. Plan manual replacement budget OR move to Storyblocks Maker. |

---

## Decision tree for V1 onward

```
Is n8n pipeline built?
├── No → Downgrade to Plus $25/mo
│   ├── Use as final assembler (drop Paul VO via upload, polish in InVideo editor, export)
│   │   └── Recommended for V1 ship
│   └── OR cancel + Storyblocks Maker $30/mo for clip licensing flexibility
│
└── Yes → Keep Max $144/mo
    └── Use API for n8n auto-pipeline
```

**Today's recommendation: downgrade to Plus + use as final assembler for V1.**

---

## Validated patterns log

- 2026-04-29: research surfaced license blocker. Adrian to decide on tier downgrade.
- *(append validated patterns after each render batch)*

---

## Sources

- [InVideo AI Help — Can I download AI-generated media](https://help.invideo.io/en/articles/9974526-can-i-download-and-use-the-ai-generated-media)
- [InVideo Plus vs Max plan differences (official)](https://help-ai.invideo.io/en/articles/9380456-what-is-the-difference-between-the-plus-and-max-plans)
- [InVideo plans & credits breakdown](https://help.invideo.io/en/articles/11528140-what-plans-does-invideo-offer-and-what-s-included-in-each)
- [Flowith — InVideo AI FAQ stock footage commercial use](https://flowith.io/blog/invideo-ai-faq-stock-footage-voiceover-export-quality-commercial/)
- [InVideo Pricing 2026 Free vs Plus vs Max](https://flowith.io/blog/invideo-pricing-2026-free-vs-plus-vs-max/)
- [Digen — InVideo Agent One Review 2026](https://resource.digen.ai/invideo-ai-video-agent-review-2026/)
- [unite.ai — InVideo Review with AI Agent](https://www.unite.ai/invideo-review/)
- [Motiontheagency — Honest InVideo AI Review](https://www.motiontheagency.com/blog/honest-review-of-invideo-ai-generated-video)
- [InVideo Veo 3.1 Prompting Guide (official)](https://invideo.io/blog/google-veo-prompt-guide/)
