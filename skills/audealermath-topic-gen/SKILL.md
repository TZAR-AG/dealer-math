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
