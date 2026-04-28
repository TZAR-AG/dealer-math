# AU Dealer Math Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Stand up a fully-automated faceless YouTube channel ("AU Dealer Math") from zero to first published video in 12 days, with a sustainable 3/wk publishing pipeline that targets $1K AUD/mo passive within ~10 weeks.

**Architecture:** Three-track build executed in parallel where possible — (1) **Brand assets** via Fiverr (mascot illustrator + AU voice actor), (2) **Production pipeline** via n8n orchestrating Claude API + ElevenLabs + Midjourney + Kling + InVideo AI + Submagic + YouTube Data API + Blotato, (3) **Funnel infrastructure** via Stan Store free product + Kit nurture sequence. After Day 12 setup, ship videos 3/wk for 30-day pilot with manual approval gates; transition to auto-publish once quality demonstrates.

**Tech stack:** n8n cloud, Claude API (Opus 4.7), ElevenLabs (Creator tier, custom voice clone), Midjourney (Standard, character refs), Kling 3.0 (motion clips), InVideo AI Max (assembly + bundled Veo 3.1), Submagic (Shorts), TubeBuddy Pro (scheduler), Storyblocks (B-roll), Canva Pro (thumbnails), Google Sheets (topic queue), Puppeteer HTML→PDF (lead magnet, reusing `generator/` pipeline), Stan Store (lead magnet delivery), Kit (email nurture), Blotato (Shorts cross-post).

**Reference spec:** [docs/superpowers/specs/2026-04-28-au-dealer-math-design.md](../specs/2026-04-28-au-dealer-math-design.md)

**Privacy lock:** Tecnica is NEVER referenced in any artifact, asset, script, or output. Generic public-data framing only.

---

## File Structure

### New files

| Path | Purpose |
|---|---|
| `~/.claude/skills/audealermath-script/SKILL.md` | New Claude skill that drafts AU Dealer Math scripts |
| `~/.claude/skills/audealermath-script/references/macca-voice.md` | Locked Macca voice rules + banned phrases |
| `~/.claude/skills/audealermath-script/references/title-formula.md` | Locked title templates for first 20 videos |
| `~/.claude/skills/audealermath-script/references/script-structure.md` | 6-section script template (hook → reframe → problem → threshold → unlocks → CTA) |
| `~/.claude/skills/audealermath-topic-gen/SKILL.md` | Weekly Sunday topic-research skill (10 candidates) |
| `content/au-dealer-math/macca-backstory.md` | Locked 200-word persona backstory |
| `content/au-dealer-math/mascot-brief.md` | Fiverr illustrator brief (Dealer + Buyer characters, 60 reference frames) |
| `content/au-dealer-math/voice-actor-brief.md` | Fiverr AU voice actor brief + audition line |
| `content/au-dealer-math/lead-magnet-7-lines.md` | "7 Lines on a Dealer Contract" PDF content draft |
| `content/au-dealer-math/kit-nurture-sequence.md` | 5-email nurture sequence draft |
| `content/au-dealer-math/script-template.md` | Locked 6-section script template + word count budgets |
| `content/au-dealer-math/topic-queue.md` | Google Sheet pointer + manual fallback queue |
| `generator/au-dealer-math/themes.js` | Single brand theme (charcoal/orange/cream) |
| `generator/au-dealer-math/base.css` | Shared CSS for lead magnet PDF |
| `generator/au-dealer-math/pages/01-cover.js` ... `08-cta.js` | 8-page lead magnet pages |
| `generator/au-dealer-math/pages/index.js` | Page aggregator |
| `generator/au-dealer-math/build-lead-magnet.js` | Puppeteer build script (HTML→PDF) |
| `generator/au-dealer-math/output/au-dealer-math-7-lines.pdf` | Built lead magnet PDF |
| `n8n/workflows/au-dealer-math-pipeline.json` | n8n export of main daily pipeline workflow |
| `n8n/workflows/au-dealer-math-topic-gen.json` | n8n export of Sunday topic-gen workflow |

### Modified files

None during build (greenfield channel + greenfield generator subdirectory).

---

## Pre-flight check

Before starting Task 1, verify these prerequisites are met:

- [ ] Adrian has decided on the mascot illustrator and voice actor (Fiverr accounts ready)
- [ ] Active payment method on Fiverr ($300 budget reserved)
- [ ] Active payment methods for SaaS subs ($300/mo recurring + ~$100 one-time signups)
- [ ] Google account ready for YouTube channel registration
- [ ] Spec reviewed and approved (this task happens implicitly — Adrian approved during brainstorming)

---

## Task 1: Lock the persona — Macca's backstory

**Goal:** Finalize the 200-word backstory file. Every script run must pass the "would Macca say this" check against this file.

**Files:**
- Create: `content/au-dealer-math/macca-backstory.md`

- [ ] **Step 1: Create the content directory**

```bash
mkdir -p content/au-dealer-math
```

- [ ] **Step 2: Write `content/au-dealer-math/macca-backstory.md`**

```markdown
# Macca — AU Dealer Math persona

## Backstory (200 words, locked)

Macca worked the Australian automotive industry for ten years, dealer-side. He saw how the trade-in lowball math actually works on the floor, how finance managers stack margin into novated lease agreements that customers don't read, how "drive-away pricing" gets reverse-engineered to hit the target margin without the buyer noticing. He's not on the floor anymore. Now he scores fifty-plus AU listings every morning — same data the dealers see — and posts the math.

He doesn't show his face. He doesn't name dealerships. He's not here to torch anyone's livelihood. He's here because every Australian who walks into a dealership has been pre-conditioned to believe the dealer holds the math, and that's a $5-15K asymmetry sitting on top of every transaction. Macca's pitch is simple: the math isn't actually complicated. The dealers just hope you don't run it.

If a viewer recognises something in their own deal, they can ask in the comments. Macca answers like a mate who's seen the inside, not a journalist who's writing a story. He's not selling cars. He's selling fluency.

## Sign-off line (every video)

> "I'm Macca. I do this every morning. AU Dealer Math."

## Voice consistency rule

Every script must pass the "would Macca actually say this" check before VO render. Banned: corporate jargon, hype, "transform your life", "smash the like button", "you won't believe", "secret hack". Required: AU vernacular ("ute", "drive-away", "rego", "mate"), specific dollar figures, calm confrontation.
```

- [ ] **Step 3: Commit**

```bash
git add content/au-dealer-math/macca-backstory.md
git commit -m "feat(audealermath): lock Macca persona backstory"
```

---

## Task 2: Write Fiverr mascot brief

**Goal:** Brief the illustrator to deliver 60 character reference frames for two recurring mascots ("The Dealer" and "The Buyer") within 5-7 days.

**Files:**
- Create: `content/au-dealer-math/mascot-brief.md`

- [ ] **Step 1: Write `content/au-dealer-math/mascot-brief.md`**

```markdown
# AU Dealer Math — Mascot Illustration Brief (Fiverr)

## What I need

Two recurring cartoon characters for a faceless YouTube channel about Australian car dealership economics. They appear together in dealership scenes, with one always selling and one always buying.

**Budget:** $200 USD. **Timeline:** 5-7 days.

## Character 1: "The Dealer"

- Mid-40s Australian male
- Polo shirt with logo erased (no real-brand affiliations)
- Polished shoes, lanyard, smart-casual
- **Always carrying a clipboard** — never put down
- Friendly outward face, calculating inward (default expression mildly conniving but warm)
- Body language: leaning slightly toward the buyer, gesturing with one hand

## Character 2: "The Buyer"

- 30s, gender-neutral
- Casual clothes (jeans + plain tee or button-up)
- Slightly tense shoulders (NOT hunched — just guarded)
- Holding either a phone (researching mode) or keys (resigned mode)
- Body language: arms slightly crossed in default pose

## Style requirements

- **Flat 2D vector aesthetic** (think Polymatter / Wendover / Cleo Abram, NOT Pixar/Disney 3D)
- **Limited color palette:** charcoal (#2B2B2B) + outback orange (#D17A3D) + cream (#F5EFE6) + secondary warm grey (#4A4340)
- **Proportions:** ~6.5-head, slightly stylised but NOT chibi or baby-face
- **NO Disney/Pixar/Marvel-echoing features** — no oversized eyes, no rounded baby cheeks, no anime-large pupils. Designed for trademarkability.
- Face details simplified — readable at thumbnail size

## Deliverables

For EACH character, I need:

1. **5 angles:** front, 3/4 left, 3/4 right, profile, back
2. **6 expressions:** neutral, smiling, confused, resigned, suspicious, alert

That's 60 reference frames total.

Plus:
3. PSD or AI source files (layered)
4. Transparent PNG exports of every frame
5. Brief style guide (1 page) — line weight, palette swatches, proportions sheet

## Audition

Please send a quick sketch of "The Dealer in 3/4 left, neutral expression" before we commit. I'll approve the style direction before you start the full set.

## What this is for

A YouTube channel that explains Australian car-buying math — finance margin, novated leases, on-road costs. The characters appear in dealership-floor cartoon scenes with voiceover narration. They're not meant to be realistic — they're symbolic stand-ins for "the dealer" and "the buyer" archetypes.
```

- [ ] **Step 2: Commit**

```bash
git add content/au-dealer-math/mascot-brief.md
git commit -m "feat(audealermath): Fiverr mascot illustrator brief"
```

- [ ] **Step 3: Adrian posts the brief on Fiverr** (manual)

Open fiverr.com → search "vector cartoon character illustrator" → filter to top-rated, $200 budget → message 3 candidates with the brief above → commission whichever responds first with a fitting portfolio + style match. Send the brief verbatim. Audition step is mandatory.

---

## Task 3: Write Fiverr voice actor brief

**Goal:** Get a 5-min recording from an AU male voice actor that ElevenLabs can clone via PVC.

**Files:**
- Create: `content/au-dealer-math/voice-actor-brief.md`

- [ ] **Step 1: Write `content/au-dealer-math/voice-actor-brief.md`**

```markdown
# AU Dealer Math — Voice Actor Brief (Fiverr)

## What I need

A 5-minute recording of an AU male voice that I'll use to clone via ElevenLabs Professional Voice Clone. Once cloned, the voice will narrate a faceless YouTube channel about Australian car-buying.

**Budget:** $80 USD. **Timeline:** 3 days.

## Voice profile

- **Australian male, 35-45 sound.** NOT corporate radio host. NOT bro-podcaster. Think: confident mate at the pub who happens to have analytical intelligence.
- **Warm baritone** — calm authority. Slight blokey edge but NOT laid-back. The viewer should feel the speaker has stakes.
- **Tone:** confrontational without aggression. "I've seen this and I'm telling you straight" — not "I'm angry about it."
- **Pace:** moderate. Pauses for emphasis on numbers. Slight tonal lift on revelations.

## Recording requirements

- **Studio-quality audio.** XLR mic + interface preferred. AT2020/SM7B/RE320 class. NO USB-only mics.
- **Quiet room** with treatment (closet recordings are fine if dry).
- **Single take per script section.** No edits. WAV or 320kbps MP3. 44.1kHz minimum.
- **Total length:** 5 minutes of clean speech. ~750-800 words. Read continuously, with natural pacing.

## Audition line (please send this first)

> "Most Aussies who walked into a dealership last weekend lost three grand before they sat down. Here's the math."

If your audition reads land, I'll send the full 750-word script for the 5-min recording.

## Audition criteria

- Authentic AU accent — NOT generic transatlantic, NOT British, NOT NZ
- Calm-confident delivery on the dollar figure
- No corporate-radio gloss
- "Three grand" should feel like everyday speech, not announcement

## Licensing

I need full commercial usage rights including the right to clone the voice via AI tools (ElevenLabs Professional Voice Clone). Confirm in your reply you understand and agree.

## What this voice will do

It'll narrate a faceless YouTube channel called "AU Dealer Math" — short-form (8-15 min) explainer videos about Australian car-buying tactics. The voice will be cloned and re-used across many episodes.
```

- [ ] **Step 2: Commit**

```bash
git add content/au-dealer-math/voice-actor-brief.md
git commit -m "feat(audealermath): Fiverr voice actor brief"
```

- [ ] **Step 3: Adrian posts the brief on Fiverr** (manual)

fiverr.com → "Australian voice actor male" → filter to verified pros, $80 budget → message 3 with the brief verbatim. Audition first. Hire the one whose audition line lands the calm-confrontation tone.

---

## Task 4: Sign up SaaS subscriptions

**Goal:** All recurring subscriptions active so the pipeline can be built.

**No code files — operational setup.**

- [ ] **Step 1: Sign up — n8n cloud**

Visit n8n.io/cloud → Starter plan ($20/mo) → email = `hello@thestructuredself.com` → save credentials in your password manager. Note the workspace URL.

- [ ] **Step 2: Sign up — InVideo AI Max**

invideo.io/ai → Max plan ($50/mo) → email = `hello@thestructuredself.com`. Verify the plan includes Veo 3.1 + Sora 2 / equivalent video model bundles. Save API key from Settings → API.

- [ ] **Step 3: Sign up — Midjourney Standard**

midjourney.com → Standard ($30/mo) → Discord-linked. Confirm fast hours included. Save Discord bot token from your account settings if you'll be triggering via API later (otherwise n8n will use Discord webhook).

- [ ] **Step 4: Sign up — Kling 3.0**

klingai.com → $10/mo Starter (660 credits ≈ 165 five-second clips). Save API key.

- [ ] **Step 5: Sign up — Submagic**

submagic.co → Starter $16/mo. Save API key.

- [ ] **Step 6: Sign up — TubeBuddy Pro**

tubebuddy.com → Pro $7.50/mo (after channel exists). Skip until Task 5 done.

- [ ] **Step 7: Sign up — Storyblocks**

storyblocks.com → All-Access $30/mo. Confirm unlimited downloads + commercial license.

- [ ] **Step 8: Verify ElevenLabs Creator tier active**

elevenlabs.io → confirm Creator tier ($99/mo) is active on your existing account (already used for Structured Self). If on Starter, upgrade. Note the API key.

- [ ] **Step 9: Lock all credentials in password manager**

Add a "AU Dealer Math" entry with all API keys, dashboard URLs, plan tiers, monthly cost. This is the source of truth for the SaaS budget.

- [ ] **Step 10: Commit a tracker**

```bash
mkdir -p content/au-dealer-math
cat > content/au-dealer-math/saas-stack.md << 'EOF'
# AU Dealer Math SaaS stack — recurring subscriptions

| Tool | Plan | Cost AUD/mo | API key location |
|---|---|---|---|
| n8n cloud | Starter | $30 | Password manager |
| InVideo AI | Max | $76 | Password manager |
| Midjourney | Standard | $46 | Discord-linked |
| Kling 3.0 | Starter | $15 | Password manager |
| Submagic | Starter | $24 | Password manager |
| TubeBuddy | Pro | $11 | Account settings |
| Storyblocks | All-Access | $46 | Account settings |
| ElevenLabs | Creator | $151 | Existing SS account |
| Claude API | (usage) | $15-30 | console.anthropic.com |
| **Total** | | **~$414/mo** | |

(USD-to-AUD at 0.65 exchange rate; revisit monthly.)
EOF
git add content/au-dealer-math/saas-stack.md
git commit -m "feat(audealermath): SaaS stack tracker"
```

---

## Task 5: Register YouTube channel + lock identity

**Goal:** AU Dealer Math channel live with correct branding, category locked to Education.

**No code files — operational setup.**

- [ ] **Step 1: Create new Google Brand Account**

studio.youtube.com → Settings → Channel → Account → Add new account → Brand Account "AU Dealer Math". This separates the channel from your personal Google identity.

- [ ] **Step 2: Set channel handle**

studio.youtube.com → Customisation → Basic info → Handle: `@audealermath` (verify availability — if taken, fall back to `@audealermathau` or `@aussiedealermath`)

- [ ] **Step 3: Set channel name + tagline**

- Name: `AU Dealer Math`
- Tagline: `Run the numbers. Walk in fluent.`

- [ ] **Step 4: Lock channel category**

studio.youtube.com → Settings → Channel → Advanced settings → Category: `Education`. This is the load-bearing CPM lock — Education category pulls $25-50 RPM in AU vs $5-10 for Entertainment/Animation.

- [ ] **Step 5: Set country to Australia**

studio.youtube.com → Settings → Channel → Country of residence: Australia. AU CPM premium ($36.21 vs US $32.75) requires this lock.

- [ ] **Step 6: Configure About section**

studio.youtube.com → Customisation → Basic info → Description:

```
AU Dealer Math is the channel that runs the numbers Australian car dealers don't want you to.

We break down dealer finance margins, novated lease math, trade-in lowball tactics, and on-road cost stitching — all from the perspective of someone who spent ten years on the dealer side.

Hosted by Macca. New explainers every Mon/Wed/Fri.

For the free PDF — "7 Lines on a Dealer Contract You Should Never Sign" — link below.
```

- [ ] **Step 7: Reserve cross-platform handles** (manual)

- IG: instagram.com → register `@audealermath` (or fallback)
- TikTok: tiktok.com → register `@audealermath` (or fallback)

These exist for Shorts cross-posting later. No content goes live yet.

- [ ] **Step 8: TubeBuddy Pro subscribe + connect**

tubebuddy.com → Pro $7.50/mo → connect to AU Dealer Math channel → enable A/B thumbnail tests + scheduled publish features.

- [ ] **Step 9: Commit a channel-config snapshot**

```bash
cat > content/au-dealer-math/channel-config.md << 'EOF'
# AU Dealer Math — YouTube channel config

| Setting | Value |
|---|---|
| Handle | `@audealermath` (verify after registration) |
| Country | Australia |
| Category | Education (LOCKED — do not change) |
| Tagline | Run the numbers. Walk in fluent. |
| Cadence | 3/wk (Mon/Wed/Fri 18:00 AWST publish) |
| TubeBuddy | Pro tier, connected |
| Cross-platform | IG @audealermath, TikTok @audealermath (Shorts only) |

## Critical: do NOT let YouTube auto-classify category as Entertainment/Animation. Verify at 1K subs and again at 10K subs.
EOF
git add content/au-dealer-math/channel-config.md
git commit -m "feat(audealermath): channel config snapshot"
```

---

## Task 6: Build the audealermath-script skill

**Goal:** A new Claude skill that drafts 1,500-word AU Dealer Math scripts from a topic input, using Macca's voice rules + locked structure + locked title formula.

**Files:**
- Create: `~/.claude/skills/audealermath-script/SKILL.md`
- Create: `~/.claude/skills/audealermath-script/references/macca-voice.md`
- Create: `~/.claude/skills/audealermath-script/references/title-formula.md`
- Create: `~/.claude/skills/audealermath-script/references/script-structure.md`

- [ ] **Step 1: Create skill directory**

```bash
mkdir -p ~/.claude/skills/audealermath-script/references
```

- [ ] **Step 2: Write `~/.claude/skills/audealermath-script/SKILL.md`**

```markdown
---
name: audealermath-script
description: Generate AU Dealer Math YouTube video scripts. Use when Adrian asks to draft a video, propose a script for a topic, or write today's pilot episode. Output is a 1,500-word, 8-15 minute script following Macca's locked voice + 6-section structure + AU Dealer Math title formula. Includes title options, description, thumbnail concepts.
---

# AU Dealer Math Script Generator

## Overview

Generate production-ready video scripts for the AU Dealer Math YouTube channel. Every script follows Macca's confrontational-but-calm voice + the locked 6-section structure + the AU Dealer Math title formula.

## Privacy lock

NEVER reference Tecnica. NEVER show or imply screen-rec of any proprietary tool. Use generic "the same data dealers see" framing only. If the topic seems to require Tecnica-specific framing, route around it.

## Before writing

1. Read `references/macca-voice.md` — load the voice rules + banned phrases
2. Read `references/title-formula.md` — load the locked title templates
3. Read `references/script-structure.md` — load the 6-section template + word budgets
4. Confirm the topic with Adrian (or use the Sunday topic queue)
5. Use WebSearch + Reddit MCP (r/AusFinance, r/CarsAustralia) to ground specific numbers + current AU context. Every claim needs a real number.

## Script production process

### Step 1: Research
- Search for current AU data on the topic (rates, prices, ATO rulings, dealer markups)
- Find Australian-specific data (AUD figures, ATO schemes, AU dealer practices)
- Identify common buyer misconceptions to call out

### Step 2: Generate 3 title options

Use the locked formulas from `references/title-formula.md`. Primary template = "What Your Aussie Dealer Won't Tell You About [X]". Secondary = "Inside the Aussie Dealership: [X]" or "$X is What Your [Car] is Really Worth in [City] Right Now". All under 60 chars.

### Step 3: Write the script

Follow the 6-section structure in `references/script-structure.md`. Word budget: 1,400-1,700 words total. Each section's word budget is specified there.

### Step 4: Generate metadata

After the script, include:
- 3 title options
- YouTube description with chapters (timestamps), 7-Lines PDF lead-magnet CTA, hashtags
- 10-15 tags
- 3 thumbnail concepts (real photo + slab-caps text + outback-orange underline word)

### Step 5: Save

Save to `content/au-dealer-math/scripts/video-XX-topic-slug.md`

## Quality checklist

- [ ] Hook in first 25 sec uses vivid-scene + named-victim opener
- [ ] Every dollar figure backed by a real, current AU source (cite in script comments)
- [ ] Macca's sign-off line included verbatim at end
- [ ] Lead-magnet CTA inserted at 9:30 mark
- [ ] No Tecnica references anywhere
- [ ] No banned phrases (see macca-voice.md)
- [ ] AU vernacular present (ute / drive-away / rego / mate / EOFY / etc.)
- [ ] 4 numbered unlocks (Luke playbook), not 3 or 5
- [ ] Total word count 1,400-1,700

## Output format

Return the script in this exact structure so n8n can parse it:

```yaml
---
title_options:
  - "Title option 1 (under 60 chars)"
  - "Title option 2"
  - "Title option 3"
description: |
  YouTube description with chapters, CTA, hashtags
tags:
  - tag1
  - tag2
  ...
thumbnail_concepts:
  - "Concept 1: photo + slab-caps text + underlined word"
  - "Concept 2: ..."
  - "Concept 3: ..."
---

[SECTION 1: HOOK]
...verbatim Macca script...

[SECTION 2: REFRAME]
...

[etc.]
```
```

- [ ] **Step 3: Write `~/.claude/skills/audealermath-script/references/macca-voice.md`**

```markdown
# Macca's voice rules

## Backstory anchor

See `content/au-dealer-math/macca-backstory.md` for the full 200-word persona. Every script must read as something Macca would say.

## Voice tone

- Calm-confrontational. Direct. Specific.
- Confidence comes from numbers, not claims.
- "I've seen this from the inside" framing — but never names specific dealerships.
- Slight blokey warmth — AU vernacular, mate-energy.
- Numbers carry weight. Voice intensity shifts on every dollar reveal.

## Required AU vernacular (use naturally, don't force)

- "ute" (utility vehicle)
- "drive-away" / "drive-away pricing"
- "rego" (registration)
- "EOFY" (end of financial year)
- "mate"
- "trade" (as noun: "your trade")
- "lot" (the dealer's car yard)
- "stamp" / "stamps" (stamp duty)
- "Bunnings" (cultural reference, sparingly)
- "ATO" (always spelled out: Australian Taxation Office)

## Banned phrases (never use)

- "transform your life"
- "smash the like button"
- "you won't believe"
- "secret hack"
- "hack" (as verb in any context)
- "doctors hate this"
- "literally"
- "game-changer"
- "dealership X is the worst" (no specific names)
- "trust me, I'm an expert"
- Caps-lock for emphasis ever
- Exclamation marks (zero — period)

## Voice intensity shifts

The Fiverr-cloned AU voice has natural variability. Direct intensity shifts at:
- Every dollar-figure reveal (slight lift)
- Threshold moment ("this is where everything changes" — pause, then drop tone)
- Lead-magnet CTA (warmer, mate-energy)
- Sign-off ("I'm Macca..." — calm declarative)

## What Macca doesn't do

- Doesn't sell. He explains. The product is fluency.
- Doesn't moralise about dealers. Acknowledges they're running a business.
- Doesn't promise outcomes. Promises clarity.
- Doesn't claim to be a journalist or a regulator. Claims to have been on the floor.

## Lead-magnet CTA (insert at 9:30 mark every video)

> "There's a free PDF in the description — the 7 lines on a dealer contract you should never sign. Grab that, and run the math next time."

## Sign-off (every video, last 10 sec)

> "I'm Macca. I do this every morning. AU Dealer Math."
```

- [ ] **Step 4: Write `~/.claude/skills/audealermath-script/references/title-formula.md`**

```markdown
# AU Dealer Math title formulas (locked for first 20 videos)

## Why locked

Templated CTR compounds because viewers' brains stop processing format and only process the variable. Easy Actually proved 1M subs from one phrase formula. Don't deviate during pilot.

## Primary template (use 14 of first 20)

**"What Your Aussie Dealer Won't Tell You About [X]"**

Variables to slot:
- Drive-away pricing
- Novated leases
- Trade-in math
- Finance margin
- On-road costs
- EOFY runout
- Demo cars
- Fleet returns
- GST + LCT math
- Toyota dealer profit
- Ute markup
- EV FBT exemption
- Manufacturer rebates
- Stock-take incentives
- Salary sacrifice
- Loan-protection insurance

## Secondary template (use 6 of first 20)

**"Inside the Aussie Dealership: [X]"** (insider walk-through)
**"$[X] is What Your [Car] is Really Worth in [City] Right Now"** (number-reveal — Luke threshold playbook)

## Title rules

- Under 60 characters
- "Aussie" or "AU" in title for SEO + algo classification
- Concrete dollar figure if possible
- ALL caps for ONE word maximum (the punch word) — entire title NOT all-caps
- No exclamation marks
- No question marks (works for AFWL, dilutes for analytical brand)

## After 20 videos

A/B test: pick top-3 by retention + CTR, lock those, test 5 new patterns. Repeat every 20 videos.
```

- [ ] **Step 5: Write `~/.claude/skills/audealermath-script/references/script-structure.md`**

```markdown
# AU Dealer Math script structure (locked template)

## 6 sections, 1,400-1,700 words total

### 1. Hook (0:00-0:25 — 80-100 words)

Vivid-scene + named-victim opener. Generic template:

> "Somewhere in Australia today, [a specific person profile] is at a [specific dealership type] about to sign on a [specific car at specific price]. They'll [specific consequence with dollar figure]. Here's the math they didn't show."

Pattern interrupt every 3 sec — Macca character entry, dealer character entry, dollar reveal, motion clip.

### 2. Reframe (0:25-1:00 — 100-130 words)

"But here's what nobody tells you..." — set up the structural problem behind the surface trick. Not personal. Not moral. Mechanical.

Continued 3-5 sec interrupts.

### 3. Problem deep-dive (1:00-3:30 — 380-450 words)

The behavioural + economic mechanism. Numbers shown step-by-step. This is where Adrian's checkpoint #1 dealer-knowledge insert lands — the specific insider detail only he'd know.

4-5 sec image cycle. Sketch chart at 2:00 mark.

### 4. Threshold / turning point (3:30-5:00 — 200-260 words)

The pivot moment: "$X is the line where everything changes". Voice intensity shift. Slow zoom on number reveal.

### 5. Practical unlocks (5:00-9:00 — 500-600 words)

**Exactly 4 numbered unlocks. Not 3, not 5. Luke playbook.**

Each unlock = ~30-40 sec of voice = ~100-150 words.

Format per unlock:
- Number + name (e.g. "1. Run drive-away decomp")
- 1-sentence what
- 2-3 sentences how
- Closing data point

5-8 sec image cycle. Sketch chart per unlock.

### 6. Recap + CTA (9:00-10:30 — 140-180 words)

One-line recap of all 4 unlocks + Macca sign-off + lead magnet pitch (insert at 9:30 mark).

CTA verbatim:

> "There's a free PDF in the description — the 7 lines on a dealer contract you should never sign. Grab that, and run the math next time."

Sign-off verbatim:

> "I'm Macca. I do this every morning. AU Dealer Math."

Slow zoom on Macca character. End-card builds.

## Pattern interrupt cadence rules

- 0-60 sec: pattern interrupt every 3-5 sec
- 60+ sec: widen to every 5-8 sec
- Never hold one still > 90 sec without zoom/pan motion
- Comedy beat: ~1 per 30-45 sec (visual gag, ironic micro-interaction between Dealer + Buyer characters)

## Word count enforcement

Every script must total 1,400-1,700 words. Below 1,400 = video too short for AU finance niche sweet spot. Above 1,700 = retention drops past 8-min cliff.
```

- [ ] **Step 6: Test the skill manually**

In a Claude Code session, invoke the skill:

```
/audealermath-script topic: "novated lease vs cash on a $40K Hilux"
```

Expected: ~1,500-word script + 3 titles + description + tags + 3 thumbnail concepts. Verify Macca voice + structure compliance.

If output drifts, refine the references and retest. Iterate until 3 consecutive runs hit spec.

- [ ] **Step 7: Commit**

```bash
git add ~/.claude/skills/audealermath-script/
git commit -m "feat(audealermath): script-generation skill with Macca voice + locked formulas"
```

---

## Task 7: Build the audealermath-topic-gen skill

**Goal:** A weekly Sunday skill that produces 10 topic candidates from AU news + Reddit + market signals, for Adrian to pick 5 from.

**Files:**
- Create: `~/.claude/skills/audealermath-topic-gen/SKILL.md`

- [ ] **Step 1: Create skill directory**

```bash
mkdir -p ~/.claude/skills/audealermath-topic-gen
```

- [ ] **Step 2: Write `~/.claude/skills/audealermath-topic-gen/SKILL.md`**

```markdown
---
name: audealermath-topic-gen
description: Generate 10 AU Dealer Math video topic candidates for the upcoming week. Use when Adrian asks for next week's topics, runs Sunday topic-gen, or needs new content ideas. Sources: AU automotive news (last 7 days), Reddit r/AusFinance + r/CarsAustralia signals, AU calendar markers (EOFY proximity, RBA meetings, fuel-excise changes), and topic queue history (anti-repeat dedupe).
---

# AU Dealer Math — Weekly Topic Generation

## Overview

Every Sunday at 18:00 AWST, generate 10 candidate topics for the upcoming week's AU Dealer Math videos. Adrian picks 5.

## Inputs to research

1. **AU automotive news, last 7 days** via WebSearch:
   - Drive.com.au homepage
   - CarsGuide news
   - Carsales news
   - Toyota AU + Ford AU + Mazda AU corporate announcements
   - ATO publications on FBT / novated leases / car expense rules
   - RBA cash rate decisions (affect car finance rates)

2. **Reddit signals** via Reddit MCP (`mcp__reddit__get_subreddit_hot_posts`):
   - r/AusFinance hot posts past week
   - r/CarsAustralia hot posts past week
   - r/AusEcon hot posts past week
   - r/PersonalFinanceAU hot posts past week
   - Look for: dealership complaints, novated lease confusion, trade-in stories, dealer-tactic exposés

3. **Topic queue history** — read `content/au-dealer-math/topic-queue.md` and skip anything already published or queued

4. **AU calendar markers**:
   - EOFY proximity (June 30 = peak ute deals — dealer runout)
   - RBA meetings (first Tuesday of month)
   - Fuel-excise changes (Feb / Aug indexation)
   - Holiday driving seasons (summer Dec-Feb, Easter)

## Output format

Append to `content/au-dealer-math/topic-queue.md`:

```markdown
## Week of YYYY-MM-DD (proposed)

| # | Title (locked formula) | Angle (1 line) | Current relevance | Mascot scene | Adrian pick? |
|---|---|---|---|---|---|
| 1 | What Your Aussie Dealer Won't Tell You About Drive-Away Pricing | Decomposing on-road costs into actual dealer markup vs real fees | Evergreen, always relevant | Dealer holds clipboard, points at line items | [ ] |
| 2 | ... | ... | ... | ... | [ ] |
| ... 10 total | | | | | |
```

After writing, prompt Adrian: *"10 topic candidates for next week dropped in `content/au-dealer-math/topic-queue.md`. Tick 5 boxes (manually edit the file), and reply 'topics locked' when done."*

## Selection rules Adrian uses

- Mix at least 3 evergreen + 2 timely (news-pegged)
- 4 of 5 use Primary title template, 1 of 5 uses Secondary
- No two consecutive videos on the same micro-topic (dedupe across last 4 weeks)
- If a Reddit thread is gaining traction, pick a topic that addresses it directly

## After Adrian picks

Re-read `content/au-dealer-math/topic-queue.md`, find the 5 ticked rows, move them to a new section:

```markdown
## Week of YYYY-MM-DD (locked)

Mon: [Title 1]
Wed: [Title 2]
Fri: [Title 3]
+ 2 standby for daily-cadence ramp

(Next Sunday topic-gen fires automatically)
```
```

- [ ] **Step 3: Commit**

```bash
git add ~/.claude/skills/audealermath-topic-gen/
git commit -m "feat(audealermath): Sunday topic-gen skill"
```

---

## Task 8: Lock voice clone in ElevenLabs (post-Fiverr delivery)

**Goal:** Once Fiverr voice actor delivers 5-min recording, create Professional Voice Clone in ElevenLabs. Lock voice ID + settings.

**Trigger:** Fiverr voice deliverable received.

- [ ] **Step 1: Verify recording quality**

Listen to the 5-min recording. Confirm:
- AU accent authentic (not transatlantic)
- No mouth noises / breaths excessive
- Single take, no edits
- Studio quality — XLR-class mic
- 44.1kHz minimum

If any fail, request rework from Fiverr (within revision window).

- [ ] **Step 2: Upload to ElevenLabs Voice Lab (PVC)**

elevenlabs.io → Voice Lab → Add Voice → Professional Voice Clone → Upload the WAV/MP3 → Name: "Macca PVC". Wait for processing (~3-6 hours).

- [ ] **Step 3: Test the cloned voice**

Open VoiceLab → Macca PVC → Generate test phrase: *"Most Aussies who walked into a dealership last weekend lost three grand before they sat down. Here's the math."* Compare to original audition. Should be 95%+ match.

- [ ] **Step 4: Lock settings**

Settings:
- Stability: 0.55
- Similarity: 0.4
- Style exaggeration: 0.0
- Speaker boost: enabled

Save these as the default for "Macca PVC" voice.

- [ ] **Step 5: Document the voice ID**

Append to `content/au-dealer-math/saas-stack.md`:

```markdown
## Voice IDs

- **Macca (PVC)**: `<paste voice ID from URL or Settings panel>`
- Settings: stability 0.55, similarity 0.4, style 0.0, speaker boost on
```

- [ ] **Step 6: Commit**

```bash
git add content/au-dealer-math/saas-stack.md
git commit -m "feat(audealermath): Macca PVC voice locked in ElevenLabs"
```

---

## Task 9: Lock mascot character refs in Midjourney (post-Fiverr delivery)

**Goal:** Once Fiverr illustrator delivers 60 reference frames, generate Midjourney `--sref` references so AI-generated dealership scenes maintain character consistency.

**Trigger:** Fiverr mascot deliverable received.

- [ ] **Step 1: QC the deliverables**

Open the PSD/AI source. Verify:
- 60 frames total (5 angles × 6 expressions × 2 characters)
- Brand palette respected (charcoal + outback orange + cream)
- No Disney/Pixar-echo proportions
- Line weight + style consistent across all frames

If any fail, request rework.

- [ ] **Step 2: Export reference PNGs**

In the source file, export each character at 1024×1024 transparent PNG. Save to:

```
content/au-dealer-math/mascot-refs/
  dealer-front-neutral.png
  dealer-front-smiling.png
  ... (30 dealer frames)
  buyer-front-neutral.png
  ... (30 buyer frames)
```

- [ ] **Step 3: Upload to Midjourney for `--sref` codes**

In the Midjourney Discord channel, drag the front-neutral PNGs (dealer + buyer) into the chat. Right-click → Copy Image URL. Run:

```
/imagine prompt: dealer character standing in showroom, holding clipboard, neutral expression --sref <dealer-image-url> --cw 100 --ar 16:9
```

This trains MJ on the character. Save the Job ID.

- [ ] **Step 4: Generate 5 test scenes**

For each character, generate 5 dealership scenes. Verify character drift is < 10% — face proportions, palette, clothing should hold.

If drift > 10%: train with more reference angles via `--sref` chaining. Repeat until consistent.

- [ ] **Step 5: Document the prompt template**

Create `content/au-dealer-math/mascot-prompt-template.md`:

```markdown
# Midjourney prompt template for AU Dealer Math characters

## Character refs

Dealer reference URL: <paste MJ permalink>
Buyer reference URL: <paste MJ permalink>

## Locked prompt template

For dealership scenes:

```
/imagine prompt: [scene description] in 2D vector flat aesthetic, charcoal #2B2B2B + outback orange #D17A3D + cream #F5EFE6 palette, AU dealership setting, [character] from [angle], [expression] expression --sref <character-ref-url> --cw 100 --ar 16:9 --style raw
```

For close-ups:

```
/imagine prompt: close-up of [character] [expression] in 2D vector flat aesthetic, charcoal #2B2B2B + outback orange #D17A3D + cream #F5EFE6 palette --sref <character-ref-url> --cw 100 --ar 16:9 --style raw
```

## Generation rules

- Always `--cw 100` (max character weight) for character consistency
- Always `--ar 16:9` (YouTube format)
- `--style raw` to disable MJ's default styling that drifts toward photorealism
- Generate all character shots in single MJ session per video to maintain visual consistency
```

- [ ] **Step 6: Commit**

```bash
git add content/au-dealer-math/mascot-refs/ content/au-dealer-math/mascot-prompt-template.md
git commit -m "feat(audealermath): Midjourney mascot refs + prompt template locked"
```

---

## Task 10: Build lead magnet PDF — "7 Lines on a Dealer Contract"

**Goal:** 8-page PDF, designed via existing `generator/` Puppeteer pipeline. Reuses the Structured Self build approach but in AU Dealer Math brand colors.

**Files:**
- Create: `generator/au-dealer-math/themes.js`
- Create: `generator/au-dealer-math/base.css`
- Create: `generator/au-dealer-math/build-lead-magnet.js`
- Create: `generator/au-dealer-math/pages/01-cover.js` ... `08-cta.js`
- Create: `generator/au-dealer-math/pages/index.js`
- Create: `content/au-dealer-math/lead-magnet-7-lines.md`

- [ ] **Step 1: Draft the lead magnet content**

Create `content/au-dealer-math/lead-magnet-7-lines.md` with 7 specific contract clauses:

```markdown
# 7 Lines on a Dealer Contract You Should Never Sign

## Page 1 — Cover

**7 Lines on a Dealer Contract You Should Never Sign**

A free guide from AU Dealer Math.

---

## Page 2 — Intro from Macca

I spent ten years on the dealer side of Australian car sales. There are seven specific clauses in a typical purchase contract that make me wince — and I'm telling you because once you've seen them, you can't un-see them.

This isn't a takedown of dealers. They're running a business. But every Australian who signs one of these contracts has the math stacked against them — usually in ways the seller hopes they won't notice.

Read this once. Carry the knowledge into the next negotiation.

— Macca

---

## Page 3 — Line 1: "Drive-away price includes all standard on-road costs"

What it means: stamp duty + rego + LCT (Luxury Car Tax) + PPSR + dealer delivery.
What's hidden: dealer delivery is a markup, not a fee. ~$1,500-3,000 per car. Negotiable.
The fix: ask for the "ex-on-road" price and reverse-engineer the dealer delivery component.

---

## Page 4 — Line 2: "Trade-in value: as inspected"

What it means: the figure you signed for is the figure they pay.
What's hidden: dealers reassess "as inspected" and reduce on settlement if you're locked in.
The fix: get the trade figure agreed in writing BEFORE signing the new-car contract.

---

## Page 5 — Line 3: "Finance through dealer panel rate"

What it means: dealer arranges finance through their broker network.
What's hidden: dealer earns 1-3% origination commission baked into the rate.
The fix: get pre-approved at your bank/credit union first. Make dealer match or beat.

---

## Page 6 — Line 4: "Loan protection insurance optional but recommended"

What it means: GAP insurance, mechanical extended warranty, etc.
What's hidden: 50-80% commission to dealer. Often duplicates existing coverage.
The fix: decline at the table. Reassess separately if you need any of it.

---

## Page 7 — Line 5: "Vehicle ready for collection within 14 business days"

What it means: lock-in period for the dealer to source/prep.
What's hidden: if market pricing drops in those 14 days, you're locked at the higher price.
The fix: add a clause: "If retail price drops on equivalent stock, contract repriced to lower."

---

## Page 8 — Line 6: "Pre-delivery inspection: completed"

What it means: dealer attests vehicle inspected before handover.
What's hidden: ~30% of PDIs are tick-box, not actual inspections.
The fix: independent pre-delivery inspection. ~$200 from a local mechanic.

---

## Page 9 — Line 7: "Acknowledgement: I have read and understood all terms"

What it means: legal lock-in.
What's hidden: this signature waives most consumer-protection redress later.
The fix: cross out anything you didn't fully understand. Initial each crossed line. Negotiate before signing.

---

## Page 10 — CTA

Want more like this?

→ Subscribe to AU Dealer Math on YouTube: youtube.com/@audealermath

Mon / Wed / Fri at 6pm AWST. Macca runs the math the dealers don't want you to.
```

- [ ] **Step 2: Create the generator subdirectory**

```bash
mkdir -p generator/au-dealer-math/pages generator/au-dealer-math/output
```

- [ ] **Step 3: Write `generator/au-dealer-math/themes.js`**

Reference: see `generator/themes.js` (existing SS pipeline) for structure.

```javascript
// AU Dealer Math single brand theme
const themes = {
  'au-dealer-math': {
    name: 'AU Dealer Math',
    bg: '#F5EFE6',          // cream
    heading: '#2B2B2B',      // charcoal
    body: '#4A4340',         // charcoal-soft
    accent: '#D17A3D',       // outback orange
    secondary: '#4A4340',
    grid: '#E0E0E0'
  }
}

function themeToCssVars(theme) {
  return `
    --bg: ${theme.bg};
    --heading: ${theme.heading};
    --body: ${theme.body};
    --accent: ${theme.accent};
    --secondary: ${theme.secondary};
    --grid: ${theme.grid};
  `
}

module.exports = { themes, themeToCssVars }
```

- [ ] **Step 4: Write `generator/au-dealer-math/base.css`**

```css
@page {
  size: A4;
  margin: 0;
}

body {
  font-family: 'Inter', sans-serif;
  background: var(--bg);
  color: var(--body);
  margin: 0;
  padding: 0;
  -webkit-print-color-adjust: exact;
  print-color-adjust: exact;
}

.page {
  width: 210mm;
  height: 297mm;
  padding: 24mm 20mm;
  page-break-after: always;
  display: flex;
  flex-direction: column;
}

h1 {
  font-family: 'DM Sans', sans-serif;
  font-weight: 700;
  font-size: 36pt;
  color: var(--heading);
  line-height: 1.1;
  margin: 0 0 12pt 0;
}

h2 {
  font-family: 'DM Sans', sans-serif;
  font-weight: 700;
  font-size: 18pt;
  color: var(--heading);
  margin: 0 0 8pt 0;
}

h3 {
  font-family: 'DM Sans', sans-serif;
  font-weight: 700;
  font-size: 14pt;
  color: var(--accent);
  margin: 0 0 6pt 0;
}

p {
  font-size: 11pt;
  line-height: 1.6;
  margin: 0 0 8pt 0;
}

.eyebrow {
  font-family: 'DM Sans', sans-serif;
  font-weight: 700;
  font-size: 9pt;
  letter-spacing: 0.25em;
  text-transform: uppercase;
  color: var(--accent);
  margin: 0 0 16pt 0;
}

.line-number {
  font-family: 'Fraunces', serif;
  font-style: italic;
  font-size: 60pt;
  color: var(--accent);
  line-height: 1;
  margin: 0 0 12pt 0;
}

.label-block {
  border-left: 3pt solid var(--accent);
  padding-left: 12pt;
  margin: 12pt 0;
}

.label-block h3 {
  margin-bottom: 4pt;
}

.label-block p {
  font-size: 10pt;
  margin: 0;
}
```

- [ ] **Step 5: Write `generator/au-dealer-math/pages/01-cover.js`**

```javascript
function render(theme) {
  return `
    <div class="page" style="justify-content: center; align-items: flex-start;">
      <p class="eyebrow">A FREE GUIDE FROM AU DEALER MATH</p>
      <h1>7 Lines on a Dealer Contract You Should Never Sign</h1>
      <p style="margin-top: 20mm; font-size: 14pt;">Run the numbers. Walk in fluent.</p>
    </div>
  `
}

module.exports = { render }
```

- [ ] **Step 6: Write `generator/au-dealer-math/pages/02-intro.js`**

```javascript
function render(theme) {
  return `
    <div class="page">
      <p class="eyebrow">FROM MACCA</p>
      <h2>Why these seven lines matter</h2>
      <p>I spent ten years on the dealer side of Australian car sales. There are seven specific clauses in a typical purchase contract that make me wince — and I'm telling you because once you've seen them, you can't un-see them.</p>
      <p>This isn't a takedown of dealers. They're running a business. But every Australian who signs one of these contracts has the math stacked against them — usually in ways the seller hopes they won't notice.</p>
      <p>Read this once. Carry the knowledge into the next negotiation.</p>
      <p style="margin-top: 20mm;">— Macca</p>
    </div>
  `
}

module.exports = { render }
```

- [ ] **Step 7: Write `generator/au-dealer-math/pages/03-line-1.js` through `09-line-7.js`**

Pattern (one per line):

```javascript
// 03-line-1.js
function render(theme) {
  return `
    <div class="page">
      <p class="eyebrow">LINE ONE OF SEVEN</p>
      <p class="line-number">01</p>
      <h2>"Drive-away price includes all standard on-road costs"</h2>

      <div class="label-block">
        <h3>What it means</h3>
        <p>Stamp duty + rego + LCT + PPSR + dealer delivery.</p>
      </div>

      <div class="label-block">
        <h3>What's hidden</h3>
        <p>Dealer delivery is a markup, not a fee. ~$1,500-3,000 per car. Negotiable.</p>
      </div>

      <div class="label-block">
        <h3>The fix</h3>
        <p>Ask for the "ex-on-road" price and reverse-engineer the dealer delivery component.</p>
      </div>
    </div>
  `
}

module.exports = { render }
```

Repeat for lines 2-7 with the content from `content/au-dealer-math/lead-magnet-7-lines.md`.

- [ ] **Step 8: Write `generator/au-dealer-math/pages/10-cta.js`**

```javascript
function render(theme) {
  return `
    <div class="page" style="justify-content: center; align-items: center; text-align: center;">
      <p class="eyebrow">WANT MORE LIKE THIS?</p>
      <h1 style="font-size: 28pt;">Subscribe to AU Dealer Math</h1>
      <p style="font-size: 14pt; margin-top: 12pt;">youtube.com/@audealermath</p>
      <p style="margin-top: 30mm;">Mon / Wed / Fri at 6pm AWST.</p>
      <p>Macca runs the math the dealers don't want you to.</p>
    </div>
  `
}

module.exports = { render }
```

- [ ] **Step 9: Write `generator/au-dealer-math/pages/index.js`**

```javascript
const cover = require('./01-cover')
const intro = require('./02-intro')
const line1 = require('./03-line-1')
const line2 = require('./04-line-2')
const line3 = require('./05-line-3')
const line4 = require('./06-line-4')
const line5 = require('./07-line-5')
const line6 = require('./08-line-6')
const line7 = require('./09-line-7')
const cta = require('./10-cta')

function renderAllPages(theme) {
  return [
    cover.render(theme),
    intro.render(theme),
    line1.render(theme),
    line2.render(theme),
    line3.render(theme),
    line4.render(theme),
    line5.render(theme),
    line6.render(theme),
    line7.render(theme),
    cta.render(theme)
  ].join('\n')
}

module.exports = { renderAllPages }
```

- [ ] **Step 10: Write `generator/au-dealer-math/build-lead-magnet.js`**

Reference: see `generator/build-lead-magnet.js` (existing SS) for the Puppeteer pattern.

```javascript
const puppeteer = require('puppeteer')
const fs = require('fs')
const path = require('path')
const { themes, themeToCssVars } = require('./themes')
const { renderAllPages } = require('./pages/index')

async function build() {
  const theme = themes['au-dealer-math']
  const css = fs.readFileSync(path.join(__dirname, 'base.css'), 'utf-8')

  const html = `
    <!DOCTYPE html>
    <html>
      <head>
        <meta charset="UTF-8">
        <link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;700&family=Inter:wght@300;400;500;700&family=Fraunces:opsz,wght@9..144,400;9..144,700&display=swap" rel="stylesheet">
        <style>
          :root {
            ${themeToCssVars(theme)}
          }
          ${css}
        </style>
      </head>
      <body>
        ${renderAllPages(theme)}
      </body>
    </html>
  `

  const browser = await puppeteer.launch({ headless: 'new' })
  const page = await browser.newPage()
  await page.setContent(html, { waitUntil: 'networkidle0' })
  await page.evaluateHandle('document.fonts.ready')

  const outDir = path.join(__dirname, 'output')
  if (!fs.existsSync(outDir)) fs.mkdirSync(outDir, { recursive: true })

  const outPath = path.join(outDir, 'au-dealer-math-7-lines.pdf')
  await page.pdf({
    path: outPath,
    format: 'A4',
    printBackground: true,
    margin: { top: 0, right: 0, bottom: 0, left: 0 }
  })

  await browser.close()
  console.log(`PDF built: ${outPath}`)
}

build().catch(err => {
  console.error(err)
  process.exit(1)
})
```

- [ ] **Step 11: Build the PDF**

```bash
cd generator/au-dealer-math
node build-lead-magnet.js
```

Expected: `output/au-dealer-math-7-lines.pdf` exists, 10 pages, brand colors render correctly.

- [ ] **Step 12: Visually QC the PDF**

Open the PDF. Verify:
- Cover renders with cream background + charcoal title + outback orange eyebrow
- All 7 lines have proper "What it means / What's hidden / The fix" structure
- CTA page links to `youtube.com/@audealermath`
- No font-loading issues (DM Sans + Inter + Fraunces all visible)

If issues: fix in pages, re-run build, re-QC.

- [ ] **Step 13: Commit**

```bash
git add generator/au-dealer-math/ content/au-dealer-math/lead-magnet-7-lines.md
git commit -m "feat(audealermath): lead magnet PDF — 7 Lines on a Dealer Contract"
```

---

## Task 11: Set up Stan Store free product (lead magnet delivery)

**Goal:** Free Stan Store product that captures email + delivers the PDF immediately.

- [ ] **Step 1: Open Stan Store admin**

stan.store/admin → log in with Adrian's existing account → Products → New Product.

- [ ] **Step 2: Configure the free product**

- Title: `7 Lines on a Dealer Contract You Should Never Sign`
- Price: `Free`
- Type: `Digital download`
- Description (paste verbatim):

```
Spent 10 years on the AU dealer side. Here are the 7 specific clauses in a typical purchase contract that make me wince — and how to handle them.

Free PDF, instant download. From Macca at AU Dealer Math.
```

- Image: upload the cover-page render of the PDF (export page 1 as PNG via Preview)
- File upload: `generator/au-dealer-math/output/au-dealer-math-7-lines.pdf`

- [ ] **Step 3: Set the slug**

URL: `stan.store/audealermath/p/7-lines-dealer-contract` (verify availability — Stan can silently redirect bad slugs per the `feedback_verify_stan_product_url_2026-04-27.md` rule).

- [ ] **Step 4: Click-verify the public URL**

Open the URL in incognito browser. Confirm:
- Page loads to the actual product page (NOT storefront fallback)
- Cover image renders
- "Add to cart for free" button works
- Email capture screen appears after click

If it redirects to storefront, the slug failed. Try `7-lines` or `dealer-contract-pdf` instead.

- [ ] **Step 5: Configure email capture**

Stan dashboard → Product → Notifications → enable "Send to Kit" → connect Kit account (already authorised for SS — should work) → tag: `AUDM_LeadMagnet_7Lines`.

- [ ] **Step 6: Test end-to-end**

In incognito browser, complete the free purchase with a test email (use a `+test@` alias). Verify within 5 min:
- Email arrives with PDF attached or download link
- Kit list shows new subscriber tagged `AUDM_LeadMagnet_7Lines`

- [ ] **Step 7: Document the URL**

```bash
cat >> content/au-dealer-math/saas-stack.md << 'EOF'

## Lead magnet delivery

- **Stan Store URL:** stan.store/audealermath/p/7-lines-dealer-contract
- **Kit tag:** `AUDM_LeadMagnet_7Lines`
- **PDF source:** `generator/au-dealer-math/output/au-dealer-math-7-lines.pdf`
- **Re-upload:** if PDF content changes, re-upload to Stan + email past subscribers
EOF
git add content/au-dealer-math/saas-stack.md
git commit -m "feat(audealermath): Stan Store lead magnet live"
```

---

## Task 12: Build Kit nurture sequence (5 emails)

**Goal:** 5-email automation that fires when `AUDM_LeadMagnet_7Lines` tag is applied.

**Files:**
- Create: `content/au-dealer-math/kit-nurture-sequence.md`

- [ ] **Step 1: Draft `content/au-dealer-math/kit-nurture-sequence.md`**

```markdown
# AU Dealer Math — Kit nurture sequence (5 emails)

Trigger: Kit tag `AUDM_LeadMagnet_7Lines` applied.

## Email 1 — Day 0 (immediate)

**Subject:** Your 7-Lines PDF is here

**Body:**

The PDF is attached. Or grab it again here: [Stan Store URL]

I'm Macca. I do this every morning — running the math on Australian car deals so buyers walk in fluent.

If you found one of those seven lines in a contract you've already signed, reply and tell me which one. I read every reply.

YouTube link if you want more like this: youtube.com/@audealermath

— Macca

---

## Email 2 — Day 3

**Subject:** How dealers actually quote drive-away

**Body:**

When a dealer quotes you "$X drive-away", what they're actually doing is reverse-engineering the figure to hit a target margin. The breakdown they show you (stamp + rego + LCT + delivery) makes it look like fixed costs. It isn't.

Here's the math:

[insert specific worked example — $58K Hilux dealer breakdown]

The line that's a markup, not a fee: dealer delivery. Always.

If you want me to walk through this on video: youtube.com/@audealermath — newest episode covers it.

— Macca

---

## Email 3 — Day 5

**Subject:** The novated lease trap most accountants don't explain

**Body:**

Novated leases get pitched as "tax-effective". The math is more complicated than that.

Here's what actually happens:

[insert: salary sacrifice math + FBT + residual value + fuel/rego bundling]

Whether a novated lease beats cash for YOU depends on three numbers that nobody at the dealership will work out for you. They're not hidden — they're just not surfaced.

Three numbers you need:
1. Your top marginal tax rate (not your average — top marginal)
2. The car's residual value at end of lease (set by ATO)
3. Total cost-of-ownership over the lease term, including the residual buyout

Run those, then come back to the lease pitch. The math either works or it doesn't.

— Macca

---

## Email 4 — Day 7

**Subject:** What I'd do if I had to buy a car this weekend

**Body:**

Hypothetical: I'm buying a used Hilux this weekend. ~$40K budget. Here's the order I'd actually run:

1. **Walk the lots without committing** — three dealerships, no test drives, just price-list collection. Calibrate the market.
2. **Run the same model through public listing sites** — same year, same trim, private + dealer side-by-side. The gap is the dealer markup ceiling.
3. **Decline finance + extras at the desk.** Decline GAP, decline extended warranty, decline tinted-glass package. All separately reviewable later.
4. **Negotiate ex-on-road first**, then itemise the on-road components. Stamp duty is fixed by state; dealer delivery is the negotiable line.
5. **Pre-delivery: independent inspection.** $200 from a local mechanic. Saves thousands.

That's the whole playbook.

If you want this for your specific situation, reply with model + budget + state and I'll draft the math next week.

— Macca

---

## Email 5 — Day 10

**Subject:** A small thing coming soon

**Body:**

Heads up — I'm putting together something more comprehensive. Tentatively a $29-49 product: a worksheet that runs the math on any specific car you're considering. Inputs: model + year + state + dealer offer. Outputs: realistic walk-away figure, where the dealer's margin actually sits, what the on-road costs SHOULD be.

If you'd want first access when it ships, reply "in" and I'll add you to the early-bird list.

For now: keep watching. Mon / Wed / Fri at 6pm AWST.

— Macca
```

- [ ] **Step 2: Build the sequence in Kit**

app.kit.com → Sequences → New sequence → "AU Dealer Math 7-Lines Nurture"

For each email:
- Paste subject + body from `content/au-dealer-math/kit-nurture-sequence.md`
- Set delivery delay (Day 0 / 3 / 5 / 7 / 10)
- Email 1 attaches PDF (or links to Stan Store URL)
- Save each before moving to next

- [ ] **Step 3: Build the automation**

app.kit.com → Automations → New automation → "AUDM Lead Magnet → Nurture"
- Trigger: tag `AUDM_LeadMagnet_7Lines` applied
- Action: subscribe to "AU Dealer Math 7-Lines Nurture" sequence
- Save + activate

- [ ] **Step 4: Test end-to-end**

Apply tag manually to a test subscriber → verify Email 1 fires within 5 min → wait 3 days → verify Email 2 fires.

- [ ] **Step 5: Commit**

```bash
git add content/au-dealer-math/kit-nurture-sequence.md
git commit -m "feat(audealermath): Kit nurture sequence drafted + automation live"
```

---

## Task 13: Build Canva thumbnail template

**Goal:** Locked Canva template that produces consistent thumbnails in 60-90 sec per video.

- [ ] **Step 1: Create new Canva template**

canva.com → Create design → Custom size → 1280×720 (YouTube thumbnail) → Save as "AUDM Thumbnail Template v1"

- [ ] **Step 2: Lock template structure**

Layers (bottom → top):
1. **Background photo** (placeholder rectangle, 70% of frame) — to be swapped per video
2. **Charcoal gradient overlay** at bottom (40% opacity, 30% of frame height) — readability for text
3. **Title text** — Inter Black 110pt, white, slab-caps, 3-6 word punch — center-bottom
4. **Underline** — outback orange (`#D17A3D`) hand-drawn squiggle under the most provocative word
5. **Mascot cutout** (Macca in 30% of frame, bottom-right corner) — to be swapped per video
6. **Dollar figure overlay** (optional) — Fraunces italic 80pt, outback orange — top-left

- [ ] **Step 3: Add brand kit to Canva**

Settings → Brand Kit → Colors:
- Charcoal `#2B2B2B`
- Outback orange `#D17A3D`
- Cream `#F5EFE6`
- Charcoal soft `#4A4340`

Fonts:
- DM Sans Bold (display)
- Inter Black (titles)
- Fraunces (numbers)

- [ ] **Step 4: Save 3 variants for A/B testing**

Duplicate template into 3 variants:
- A: title-text dominant (no dollar figure)
- B: dollar-figure dominant (smaller title)
- C: mascot-emotion focus (resigned/alert expression in foreground)

- [ ] **Step 5: Document the template**

```bash
cat > content/au-dealer-math/thumbnail-template.md << 'EOF'
# AU Dealer Math thumbnail template

## Canva templates (locked)

- A — title-dominant: [Canva URL]
- B — dollar-figure dominant: [Canva URL]
- C — mascot-emotion: [Canva URL]

## Template specs

- Size: 1280×720
- Background photo: 70% of frame
- Charcoal gradient overlay: bottom 30%, 40% opacity
- Title: Inter Black 110pt, white slab-caps, 3-6 words
- Underline: outback orange hand-drawn under provocative word
- Mascot: 30% of frame, bottom-right corner
- Dollar figure (optional): Fraunces italic 80pt, outback orange, top-left

## Per-video workflow

1. n8n picks 3 background photo candidates from Storyblocks (cars, dealership, money)
2. n8n picks Macca cutout based on script tone (neutral / alert / resigned)
3. Canva API generates 3 thumbnail variants (A + B + C)
4. Adrian picks 1 at Checkpoint #2
EOF
git add content/au-dealer-math/thumbnail-template.md
git commit -m "feat(audealermath): Canva thumbnail template locked"
```

---

## Task 14: Build n8n main pipeline workflow

**Goal:** End-to-end n8n workflow that runs the 16-step daily pipeline (Phase 1 — manual approval at checkpoints).

**Files:**
- Create: `n8n/workflows/au-dealer-math-pipeline.json` (export from n8n UI after build)

- [ ] **Step 1: Create n8n directory in repo**

```bash
mkdir -p n8n/workflows
```

- [ ] **Step 2: Build workflow nodes in n8n cloud**

Open the n8n cloud workspace → New workflow → "AU Dealer Math Pipeline"

Add nodes in order:

1. **Cron Trigger** — daily 06:00 AWST
2. **Google Sheets** — read today's topic from `topic-queue` sheet
3. **HTTP Request → Claude API** — POST to `api.anthropic.com/v1/messages` with the audealermath-script skill content as system prompt + topic as user message. Output: 1500-word script.
4. **Send Telegram Message (or email)** — Adrian gets the script + "approve to continue?" link. Workflow pauses.
5. **Webhook listener** — wait for Adrian's approval webhook
6. **HTTP Request → Midjourney** — call MJ via Discord webhook for 30-50 stills using locked character refs
7. **HTTP Request → ElevenLabs** — POST to `api.elevenlabs.io/v1/text-to-speech/<MaccaPVC voice ID>` with script body. Save MP3.
8. **HTTP Request → Kling 3.0** — generate 3-5 hook-moment motion clips
9. **HTTP Request → Storyblocks API** — fetch 5-10 real B-roll clips matching script themes
10. **HTTP Request → InVideo AI** — POST script + voice MP3 + image URLs + B-roll URLs to InVideo for assembly. Wait for render (~10-15 min). Returns rendered MP4 URL.
11. **HTTP Request → Canva API** — generate 3 thumbnail variants from template
12. **Send Telegram Message** — Adrian gets the rendered MP4 + 3 thumbnails. Workflow pauses.
13. **Webhook listener** — wait for Adrian's thumbnail pick
14. **HTTP Request → YouTube Data API** — upload MP4 as private, schedule for 18:00 AWST publish
15. **HTTP Request → Submagic API** — generate 3 Shorts from long-form
16. **HTTP Request → Blotato** — schedule Shorts to TikTok + IG Reels (staggered times across next 24h)
17. **Google Sheets append** — log video URL, render time, total cost, status

- [ ] **Step 3: Wire credentials**

For each HTTP node, add credentials from Task 4's password manager:
- Anthropic API key
- ElevenLabs API key
- Midjourney Discord webhook
- Kling API key
- Storyblocks API key
- InVideo API key
- Canva API key
- YouTube OAuth (Google Brand Account from Task 5)
- Submagic API key
- Blotato API key
- Telegram bot token (or email SMTP)

- [ ] **Step 4: Test workflow end-to-end manually**

Trigger workflow manually with a sample topic ("test: drive-away pricing decomposition"). Walk through both checkpoints. Verify:
- Script generates within 60 sec
- Voice render within 5 min
- Visuals generate within 10 min (MJ + Kling combined)
- Assembly within 15 min
- Thumbnail generates within 2 min
- YouTube upload + schedule succeeds

If any node fails: fix, re-test, repeat.

- [ ] **Step 5: Export workflow JSON**

n8n UI → Workflow → Export → save to `n8n/workflows/au-dealer-math-pipeline.json`

- [ ] **Step 6: Commit**

```bash
git add n8n/workflows/au-dealer-math-pipeline.json
git commit -m "feat(audealermath): n8n daily pipeline workflow"
```

---

## Task 15: Build n8n weekly topic-gen workflow

**Goal:** Sunday cron that produces 10 topic candidates for Adrian to pick from.

**Files:**
- Create: `n8n/workflows/au-dealer-math-topic-gen.json` (export from n8n UI)

- [ ] **Step 1: Build workflow in n8n**

New workflow → "AU Dealer Math Topic Gen"

Nodes:

1. **Cron Trigger** — Sundays 18:00 AWST
2. **HTTP Request → WebSearch (or SearchAPI)** — query "AU automotive news last 7 days" + "ATO car ruling 2026" + "RBA cash rate" — return top 20 results
3. **HTTP Request → Reddit MCP API** — pull r/AusFinance + r/CarsAustralia + r/AusEcon + r/PersonalFinanceAU hot posts past 7 days
4. **Google Sheets read** — load `topic-queue` sheet to dedupe
5. **HTTP Request → Claude API** — system prompt = audealermath-topic-gen skill content. User message = combined news + Reddit + dedupe inputs. Output: 10 topic candidates in markdown table format.
6. **Google Sheets append** — write 10 topics to `topic-queue` sheet, week-of-YYYY-MM-DD section
7. **Send Telegram Message** — Adrian gets: "10 topic candidates dropped. Tick 5 boxes in [sheet URL] by Tuesday 09:00 AWST."

- [ ] **Step 2: Test workflow end-to-end manually**

Trigger manually. Verify:
- Web search returns AU-relevant results
- Reddit MCP returns hot posts
- Claude generates 10 topics in correct format
- Google Sheets row appended
- Telegram message arrives

- [ ] **Step 3: Export + commit**

n8n UI → Workflow → Export → save as `n8n/workflows/au-dealer-math-topic-gen.json`

```bash
git add n8n/workflows/au-dealer-math-topic-gen.json
git commit -m "feat(audealermath): n8n Sunday topic-gen workflow"
```

---

## Task 16: First weekly topic-gen run (manual)

**Goal:** Adrian runs the topic-gen workflow once before the pilot kicks off.

- [ ] **Step 1: Manually trigger topic-gen workflow**

n8n cloud → AU Dealer Math Topic Gen → Run now.

- [ ] **Step 2: Adrian picks 5 topics**

Open Google Sheet → review the 10 candidates → tick 5 checkboxes. ~15 min.

- [ ] **Step 3: Confirm queue**

Verify the daily pipeline workflow can pull the picked topics in order. Run the daily pipeline manually with topic 1.

If something's broken: fix, retest.

---

## Task 17: Ship pilot videos 1-12 (3/wk for 30 days)

**Goal:** First 12 videos shipped with manual approval at every checkpoint, with metrics tracked.

For EACH of the 12 videos (Mon/Wed/Fri publish at 18:00 AWST):

- [ ] **Step 1: 06:00 AWST — Daily pipeline auto-fires**

n8n cron triggers. Adrian receives Telegram with script draft.

- [ ] **Step 2: Checkpoint #1 — Adrian dealer-knowledge POV insert (~5 min)**

Read draft. Add 1 specific insider detail only Adrian would know:
- Real margin number on this car at this dealership tier
- Specific finance manager script that gets used
- Hidden contract line item from real-world experience
- Dealer tactic currently running in WA market

Approve to continue.

- [ ] **Step 3: Pipeline runs (~30-45 min unattended)**

Voice → visuals → assembly → thumbnail.

- [ ] **Step 4: Checkpoint #2 — Adrian QC pass (~10 min)**

Watch rendered MP4 at 2× speed. Pick 1 of 3 thumbnails. Approve.

- [ ] **Step 5: Pipeline uploads + schedules**

YouTube Data API uploads as private, schedules for 18:00 AWST publish. Submagic generates Shorts. Blotato cross-posts.

- [ ] **Step 6: Track metrics in Google Sheet**

After publish, log to `pilot-metrics` sheet:
- Video #
- Title
- Publish date
- 24h views
- 3-day views
- 7-day views
- Avg view duration
- CTR
- Subs gained
- Email signups (cross-ref Stan Store)

- [ ] **Step 7: Repeat for next video**

12 total videos. Mon/Wed/Fri × 4 weeks = 12.

---

## Task 18: Day 30 pilot review — kill/scale decision

**Goal:** Decide whether to ramp to daily, hold at 3/wk, pivot, or kill based on pilot metrics.

- [ ] **Step 1: Aggregate pilot metrics**

Pull all 12 videos' data from `pilot-metrics` sheet. Calculate:
- Average 7-day views per video
- Average retention (% viewed)
- Average CTR
- Total subs gained
- Total email signups
- Best video + worst video (titles + view counts)

- [ ] **Step 2: Apply decision rules from spec § 10**

**Scale to daily IF ANY:**
- Video 3 hit ≥10K views organically
- Average retention across 12 videos ≥40%
- Email list captures ≥100 subs
- ≥1 video crossed 50K views

**Pivot positioning IF NONE of the above:**
- Reduce to 2/wk for next 30 days
- Test secondary template families at higher mix
- Deeper customer-voice research via Reddit MCP
- Reconsider niche (unlikely — research strongly backed AU automotive cartoon)

**Kill the channel IF:**
- After 60 days + 24 videos, no video has crossed 5K views
- YT auto-classified as Entertainment (CPM sub-$5)
- Demonetization warning issued
- Adrian's manual edit time per video exceeds 45 min consistently

- [ ] **Step 3: Document decision**

Append to `content/au-dealer-math/pilot-review-2026-MM-DD.md`:

```markdown
# AU Dealer Math — Pilot Review (Day 30)

**Reviewed:** YYYY-MM-DD
**Decision:** [SCALE TO DAILY / HOLD 3-WK / PIVOT / KILL]

## Aggregate metrics
- Avg 7-day views: N
- Avg retention: X%
- Avg CTR: X%
- Total subs: N (vs pilot start: 0)
- Total email signups: N
- Best video: [title, view count]
- Worst video: [title, view count]

## Decision rationale
[2-3 sentences: which trigger fired and why]

## Next 30 days
- Cadence: [daily / 3-wk / 2-wk / killed]
- Approval mode: [Phase 1 manual / Phase 2 auto-publish + spot-check]
- Topic-formula: [keep primary / test secondary]
```

- [ ] **Step 4: Commit**

```bash
git add content/au-dealer-math/pilot-review-*.md
git commit -m "docs(audealermath): Day 30 pilot review"
```

- [ ] **Step 5: If SCALE → transition to Phase 2**

If decision = scale to daily:
- Update n8n cron to fire daily (Mon-Sat)
- Modify checkpoint #1 + #2 nodes to conditional auto-pass when quality-check rules met (script word count + voice render OK + 30+ stills + B-roll inserted + thumbnail meets template)
- Adrian spot-checks 1-2/week instead of daily
- Daily Adrian time drops from 15-30 min → 5 min

- [ ] **Step 6: AU trademark filing**

If decision = scale OR hold (anything except kill):
- File AU trademark for AU Dealer Math wordmark + mascot via IP Australia ($330)
- ipaustralia.gov.au → Online Services → File a trademark application
- Class 41 (educational/entertainment services) at minimum

---

## Self-review checklist

- [ ] All file paths in tasks are absolute or relative to repo root
- [ ] Every code step shows complete code, not "similar to above"
- [ ] No "TBD", "TODO", "implement later" placeholders
- [ ] Tasks are bite-sized (each step 2-5 min)
- [ ] Frequent commits at task boundaries
- [ ] Spec § coverage:
  - Persona (§1) → Task 1
  - Channel identity (§2) → Task 5
  - Mascot (§3) → Tasks 2, 9
  - Visual format (§4) → Tasks 6, 13, 14
  - Title formula (§5) → Task 6
  - Script structure (§6) → Task 6
  - Pipeline (§7) → Tasks 14, 15
  - Thumbnail (§8) → Task 13
  - Lead magnet (§9) → Tasks 10, 11, 12
  - Cadence + pilot (§10) → Tasks 17, 18
  - Monetization (§11) → Task 18 (post-pilot trigger)
  - Risk mitigation (§13) → embedded throughout (e.g. Task 5 category lock, Task 9 character refs, Task 6 banned phrases)
  - Prerequisites (§14) → Tasks 1-13

## References

- Spec: [docs/superpowers/specs/2026-04-28-au-dealer-math-design.md](../specs/2026-04-28-au-dealer-math-design.md)
- Existing generator pipeline (reference for lead magnet build): [generator/build-lead-magnet.js](../../../generator/build-lead-magnet.js)
- Existing youtube-script skill (reference for new audealermath-script skill): `~/.claude/skills/youtube-script/SKILL.md`
- Existing Stan Store URL verification rule: `feedback_verify_stan_product_url_2026-04-27.md`
- Existing token-discipline rule: `.claude/rules/analytics-pull.md` § Token refresh flows
