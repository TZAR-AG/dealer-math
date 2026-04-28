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
4. Confirm the topic with Adrian (or use the Sunday topic queue at `content/au-dealer-math/topic-queue.md`)
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
