# AUDM Packaging — Prompt Library

**Created:** 2026-05-06 · **Use:** drop into Claude / ChatGPT for repeatable packaging tasks. Copy verbatim, fill in `[BRACKETS]`.

All prompts assume AUDM context (faceless, premium calm-authority, defamation-safe, AU-anchored, document-forensics aesthetic, charcoal+orange+cream palette). The first line of every prompt loads that context efficiently.

---

## 1. Competitor analysis prompt

```
You're acting as AUDM's YouTube packaging strategist. AUDM is a faceless AU-finance reveal channel with calm-authority positioning, charcoal+outback-orange+cream palette, defamation-safe rules (no scam/fraud/secret/trick).

Audit the channel: [CHANNEL URL]

Pull their 10 most-recent videos. For each, extract:
1. Title pattern (which of: authority anchor / curiosity gap / dollar reveal / inside-the-room / numbered list / why-entity / don't-yet / industry-state / buyer-prescription / comparison / time-bound / math-reframe / identity)
2. Thumbnail composition (focal element + supporting + text + color palette)
3. Pairing mode (A/B/C/D per `title_thumbnail_pairing_framework.md`)
4. Estimated CTR class (low / medium / high — based on view count vs channel baseline)

Then identify:
- The 3 strongest patterns AUDM should ethically steal (with adapted AUDM example for each)
- The 3 anti-patterns AUDM should NOT replicate (with reason)
- Any white-space niches the competitor isn't covering that AUDM could own

Output as a markdown table + bulleted recommendations. ~600 words max.
```

---

## 2. Title generation prompt

```
You're generating titles for AUDM's V[N] video. Constraints:
- 50-62 chars (max 65)
- Stack ≥4 of 5 psychology triggers: loss aversion, self-implication, specificity, identity activation, curiosity gap with stakes
- Banned words: scam, rip-off, fraud, secret, hidden, cheating, trick, lying, crooked, crook, liar
- No ALL CAPS, no exclamation marks, max 1 question mark
- Default OMIT "Australia" — channel name carries AU anchor
- AUDM voice = calm authority, dealer slang OK (F&I, drive-away, comparison rate)

Video topic: [TOPIC]
Video length: [LONG-FORM / SHORT]
Pairing mode pick: [A / B / C / D — see title_thumbnail_pairing_framework.md]
Hook category: [authority / curiosity gap / dollar / inside-room / list / why / don't-yet / state / prescription / vs / time / math / identity]
Specific dollar figure (if known): $[AMOUNT]
Specific named entity (if any): [Toyota / Hyundai / etc — Mac CV brands only]

Generate 7 title candidates. For each, list:
- Title (verbatim, char-counted)
- Triggers stacked (X/5)
- Char count
- Pairing-mode fit
- Risk (if any)
- Recommended thumbnail composition

Rank top 3 with one-line "why this wins." Final pick = the one Adrian should ship.
```

---

## 3. Thumbnail concept generation prompt

```
You're generating thumbnail concepts for AUDM V[N]. Constraints:
- Faceless (no human face, ever)
- Charcoal #2B2B2B + cream #F5EFE6 + outback orange #D17A3D (3-color discipline)
- DM Sans Bold for any text, max 3-5 words
- Mobile-first (test at 200×112px)
- ONE focal element + ONE supporting + optional text (max 3 layers)
- Document-forensics aesthetic (contracts, calculators, hands, pens, smart-keys, late-model AU utes)
- No defamation language (SCAM, FRAUD, LYING, RIP-OFF, EXPOSED)
- No legible text on documents/plates (per text-failure-pool rule)

Video title: "[LOCKED TITLE]"
Pairing mode: [A / B / C / D]
The "what's NOT in the title that should be on the thumb" question (Q9 of brief): [ANSWER]

Generate 5 thumbnail concept candidates. For each:
1. Template pick (A=Circled Clue / B=Number on Document / C=Split-Frame / D=Stamped Overlay / E=Annotated Cheatsheet)
2. Composition spec (focal + supporting + text + position)
3. MJ v7 prompt (with text-failure-pool exclusions baked in)
4. Predicted scorecard score per the 10 categories
5. Risk (any anti-pattern violations? mobile-readability issues?)

Rank top 3 by predicted CTR. Output the winning concept's full MJ prompt + Photopea composition spec ready to render.
```

---

## 4. Hook strengthening prompt

```
You're auditing this title-thumbnail pair for AUDM. The package failed/underperformed and needs a stronger hook.

Original title: "[CURRENT TITLE]"
Original thumbnail: [DESCRIBE — focal + text + colors]
Current CTR: [X.X%]
Current retention: [XX%]
Pairing mode: [A / B / C / D]

Diagnose the FIRST-FRAME failure mode:
1. Is the title-thumbnail pair non-redundant? (different questions answered)
2. Does the package raise a curiosity gap with clear stakes?
3. Does the thumbnail have foveal singularity (one element wins the eye)?
4. Is the thumbnail mobile-readable at 200×112?
5. Is the title triggers stack ≥4/5?
6. Is the cold-open delivering on the package's promise within 30s?

For the weakest 2 dimensions, propose 2 specific rebuilds. For each rebuild:
- New title (if changing) with char count + triggers stacked
- New thumbnail concept (composition + text)
- Predicted CTR lift (in percentage points)
- Whether to test sequentially (title only first, then thumb) or simultaneously
- Hard cap: 3 re-package attempts before archiving

Output as a tight diagnostic + action plan, ~400 words.
```

---

## 5. CTR diagnosis prompt

```
You're diagnosing AUDM V[N]. Pull data from `content/au-dealer-math/analytics/yt-YYYY-MM-DD.md` and the per-video log.

Video: [V[N] - title]
Hours since publish: [N hours]
CTR: [X.X%]
AVD: [Xs / X% retention]
Impressions: [N]
Top traffic source: [SHORTS / YT_OTHER_PAGE / SUBSCRIBER / etc]
Quadrant placement (per ctr_testing_framework.md): [Q1 / Q2 / Q3 / Q4]

Diagnose:
1. Is the CTR meaningful at this stage? (per signal-interpretation table — 1h sub-only / 24h browse-mix / 48h stable / 7d search-contributing / 14d locked)
2. What does the impression count tell us? (algo throttling? algo expanding?)
3. What does the traffic source tell us about cluster placement?
4. If retention curve has populated, where's the biggest drop-off? What does the timestamp tell us about the script's failure point?
5. Quadrant playbook applies — what's the recommended action?

Output:
- Diagnosis (1-2 sentences)
- Recommended action (specific — title edit / thumb rebuild / cold-open recut / archive / hold)
- Decision deadline (when this needs to be done by)
- What data to collect at next checkpoint
```

---

## 6. Packaging improvement prompt (post-failure)

```
V[N] failed: CTR [X%], retention [X%]. We've already attempted [N] re-packages with no movement.

Original package: title "[X]" + thumbnail "[X]"
Re-package 1: changed [X], new CTR [X%]
Re-package 2: changed [X], new CTR [X%]
Re-package 3: changed [X], new CTR [X%]

Honest verdict — is the package the problem, or is it:
1. Wrong topic for this audience cluster?
2. Wrong format (long-form when Short would win)?
3. Wrong pairing mode (Mode C reinforce when Mode A would have driven curiosity)?
4. Wrong audience fit (not AU professional buyer)?
5. Algo cluster mismatch (still in Semantic ID learning phase)?

If diagnosis is "the package":
- Propose 1 final rebuild with strongest possible Mode A or B execution
- Set decision deadline for next CTR pull (48h)

If diagnosis is "not the package":
- Recommend archive
- Write the lesson to per-video log
- Identify the upstream rule we should change for V[N+1] (topic selection, format choice, pairing-mode default, etc.)

Output: 200 words max. No fluff. The lesson is the value — what specifically should the next video do differently?
```

---

## 7. A/B test planning prompt

```
You're planning a Studio Test & Compare run for AUDM V[N].

Video: [V[N] - title]
Current 48h impressions: [N]
Eligibility (per ctr_testing_framework.md):
- <200 impressions in 48h → not eligible (manual re-package only)
- 200-1000 impressions → manual A/B (one swap per 7 days)
- >1000 impressions → fire Test & Compare

Pre-test gate (REQUIRED):
1. Mobile preview at 200×112 — passes?
2. Foveal singularity — one focal element wins?
3. Pairing mode locked (A/B/C/D)?
4. Defamation-safe + brand-safe pass?
5. Retention preview — does cold open deliver thumb's promise?
6. Scorecard ≥7 average?

If Test & Compare eligible:
- Generate 3 thumbnail variants that differ on ONE axis (composition OR text OR color emphasis — NOT all three)
- For each variant, list: composition + text + predicted scorecard score
- Predict the winner (which variant should win on watch-time-per-impression, NOT raw CTR — Studio's actual optimization target)

If manual A/B:
- Propose live variant + backup variant
- Set 7-day swap decision criteria

Output: variant table + decision matrix + when to check results.
```

---

## 8. Retention curve analysis prompt

```
V[N] retention curve has populated (>72h post-publish, >50 views). Pull from the analytics file.

Video: [V[N] - title]
Length: [MM:SS]
Retention curve (sample every 5%): [from yt-pull output]

Diagnose:
1. Where's the biggest drop-off? (% of audience lost between two adjacent samples)
2. Convert drop-off % to MM:SS timestamp on the actual video
3. What's happening in the script at that timestamp?
4. Is it a:
   - Hook failure (drop-off in first 30s)
   - Pacing failure (steady decline 1-3 min in)
   - Topic-shift failure (cliff at a specific topic transition)
   - End-of-video failure (sub-30% retention from start = total package mismatch)
5. What's the fix?
   - Hook failure → recut cold open via Studio Editor (insight-first, kill scene-setting)
   - Pacing failure → tighter cuts in 1-3 min range; reduce setup, get to point faster
   - Topic-shift failure → restructure script so transition is bridged with a "here's why this matters" line
   - End-of-video failure → fundamental package mismatch; archive

Output: timestamp-specific diagnosis + 1-3 sentence fix recommendation. ≤200 words.
```

---

## 9. Pairing mode picker prompt

```
You're picking the pairing mode for AUDM V[N] before any briefing happens.

Video topic: [TOPIC]
Video format: [LONG-FORM / SHORT]
Audience expected: [browse-discovery / search / mixed]
Search intent (if any): [keyword phrase]
Counterintuitive angle (if any): [paradox / contradiction / reframe]

Pick ONE mode (per title_thumbnail_pairing_framework.md):
- Mode A — Title teases / Thumb explains (default ~50%)
- Mode B — Thumb teases / Title explains (counterintuitive ~25%)
- Mode C — Reinforce (search-intent ~15%)
- Mode D — Tension/contrast (rare ≤10%)

For your pick, justify:
1. Why this mode fits the video's content type
2. What the title's role is (tease / explain / reinforce / contradict)
3. What the thumbnail's role is (tease / explain / reinforce / contradict)
4. The "non-redundancy check" — what's the SECOND curiosity gap the thumbnail will raise that the title doesn't?
5. What the "predict the partner" test produces (read title → can you predict thumbnail? if yes, the package is dead)

Output: mode pick + justification + non-redundancy check (≤150 words).
```

---

## 10. V[N] full package brief prompt

```
You're generating the complete V[N] package brief for AUDM. Inputs:
- Video topic: [TOPIC]
- Specific dollar figure (if known): $[AMOUNT]
- Specific named entity (if any): [Toyota / Hyundai / etc — Mac CV brands only]
- Video length: [LONG-FORM / SHORT]
- Search intent (if any): [keyword phrase]

Generate, in order:
1. Pairing mode lock (A/B/C/D) with justification
2. 3 title candidates ranked, top pick highlighted (50-62 chars, ≥4/5 triggers)
3. 3 thumbnail concepts ranked, top pick highlighted (Template A-E + composition spec + MJ v7 prompt)
4. Predicted scorecard score per the 10 categories
5. Predicted CTR + retention based on V1-V[N-1] baseline
6. Pre-publish QC checklist with checkbox status
7. Reason to publish at this specific time (cadence, news anchor, niche timing)

If the package fails the scorecard pre-check (any cat <6 or avg <7), surface the failure and propose the rebuild before locking. Don't ship a failing package.

Output: complete package brief, ready to drop into the per-video log file. ~800 words max.
```

---

## 11. Weekly competitor sweep prompt

```
You're running AUDM's weekly competitor sweep. For each of the 8 tracked channels, pull their 5 most-recent uploads and audit packaging.

Tracked channels:
1. AutoExpert AU / John Cadogan
2. CarEdge / Shefska brothers
3. Lucky Lopez
4. Aussie Finance With Luke
5. Car Dealership Guy
6. How Money Works
7. Wendover Productions / HAI
8. Spencer Cornelia

For each video:
- Title + estimated CTR class
- Thumbnail composition (focal + text + color)
- Pairing mode (A/B/C/D)
- New pattern? (yes/no — if yes, describe)

After all 40 videos audited:
- Identify any NEW patterns not yet in `competitor_swipe_file.md`
- Identify any patterns being abandoned (videos at the bottom of CTR ranges)
- Recommend what AUDM should test in the next 4 uploads based on emerging patterns

Output: append to `competitor_swipe_file.md` as a dated weekly section. ~800 words.
```

---

## 12. V[N] retrospective prompt (post-mortem after 14 days)

```
You're running the 14-day retrospective on AUDM V[N]. The video has been live long enough for final verdict.

Video: [V[N] - title]
Pairing mode: [A / B / C / D]
Final 14d CTR: [X.X%]
Final 14d retention: [XX%]
Quadrant verdict: [Q1 / Q2 / Q3 / Q4]

Compare against:
- Predicted scorecard score: [X/100]
- Predicted CTR: [X.X%]
- Channel baseline (last 5 videos avg): [X.X%]

Diagnose:
1. Did the scorecard predict accurately? If not, which categories misjudged?
2. Did the pairing mode work for this content type?
3. What's the 1-sentence lesson for V[N+1]?

Promote / retire patterns:
- Any pattern proven (≥6% CTR over 3+ videos) → promote to default in `title_formulas.md`
- Any pattern at <2% CTR → retire to "deprecated" section
- Any thumbnail template proven (≥5% CTR over 3+ videos) → promote in `competitor_swipe_file.md`

Output: complete retrospective, ready to update the package log + the source-of-truth files. Actionable changes only.
```

---

## 13. Cold-open recut prompt (when retention is the failure)

```
V[N] has Q2 (high CTR, low retention) — the package promised something the cold open didn't deliver.

Title: "[X]"
Thumbnail concept: [X]
First 60s of script: [PASTE]
Biggest retention drop-off: [X%] at [MM:SS]

Diagnose:
1. What does the package promise? (What's the curiosity gap raised?)
2. When does the cold open deliver on that promise? (What second?)
3. Is there preamble before the delivery? (scene-setting / handshake / coffee — kill these)

Generate 3 cold-open rewrites that:
- Open within 5 seconds on the strongest insight in the script
- Deliver on the package's promise within 15 seconds
- Use Mac voice (calm authority, dealer slang, first-person specificity)
- Don't use scene-setting or "today I'm going to explain" preamble
- Hit ~30 words / ~10 seconds at Mac's 2.86 wps rate

For each rewrite, predict:
- Retention curve at 30s mark (target ≥60% per yt-analytics-baselines)
- Whether Studio's secondary signal (watch-time-per-impression) will lift

Output the winning rewrite + the recut instruction (Studio Editor timestamp range to trim) ready to execute.
```

---

## 14. Scorecard recalibration prompt

```
You're recalibrating the AUDM scorecard against actual data. After [N] videos shipped, pull the database and regress predicted score against actual CTR.

For each of the 10 categories:
1. What's the average score the scorecard gave?
2. What's the correlation with actual CTR?
3. Is the category over-weighted or under-weighted relative to the data?

Identify:
- The 2 categories that most strongly predicted CTR (keep weight)
- The 2 categories that LEAST predicted CTR (consider de-weighting)
- Any new dimension not captured by the current 10 categories that the data suggests matters

Output:
- Updated weight recommendations
- Proposed scorecard v2 (if any category changes)
- Anti-inflation check: is the average score drifting up over time? (Score-inflation drift = scorecard losing its strict gate function)
- Recommended re-score schedule (next checkpoint)

Update `packaging_scorecard.md` with the changes.
```

---

## How to use these prompts

1. **Drop into Claude or ChatGPT.** Fill in `[BRACKETS]`. The first line loads AUDM context.
2. **Save outputs to per-video log.** Don't let outputs evaporate — the database compounds.
3. **Re-run when patterns shift.** The prompts are templates, not relics. Update them when new findings invalidate assumptions.
4. **Combine prompts.** A typical V[N] flow: Prompt 9 (mode picker) → Prompt 10 (full brief) → Prompt 5 (CTR diagnosis at 48h) → Prompt 8 (retention curve at Day 3) → Prompt 12 (retrospective at 14d).

---

## Filed-with

- [README.md](README.md) — operating manual
- [youtube_packaging_strategy.md](youtube_packaging_strategy.md) — strategic core
- [title_thumbnail_pairing_framework.md](title_thumbnail_pairing_framework.md) — pairing modes
- [thumbnail_brief_template.md](thumbnail_brief_template.md) — thumbnail spec
- [packaging_scorecard.md](packaging_scorecard.md) — scoring gate
- [ctr_testing_framework.md](ctr_testing_framework.md) — testing protocol
- [competitor_swipe_file.md](competitor_swipe_file.md) — visual references
- [title_formulas.md](title_formulas.md) — 100 templates
- [video_packaging_database_template.csv](video_packaging_database_template.csv) — DB schema

> Re-score quarterly. Add new prompts when a recurring task surfaces ≥3 times.
