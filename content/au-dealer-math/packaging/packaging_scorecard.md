# Packaging Scorecard

**Created:** 2026-05-06 · **Authority:** mandatory pre-upload gate. Every video must score ≥7 average AND ≥6 in every category.

**Use:** fill out for every V[N] before upload. Save to `content/au-dealer-math/scripts/v0X-renders/v0X-package-log.md`. Strict scoring — do NOT inflate.

---

## V[N] Package Score — [video title]

**Pairing mode:** A / B / C / D
**Title:** "________________________"
**Thumbnail concept:** ________________

### 10-category scorecard (1-10 each)

#### 1. Clarity (can a stranger explain what the video is about in one breath?)
- 1-3: ambiguous, abstract, jargon-heavy
- 4-6: requires reading the title twice
- 7-9: instantly comprehensible, ~2 second read
- 10: zero ambiguity, every word load-bearing
- **Score: __ / 10**

#### 2. Curiosity (does the package raise a question the viewer NEEDS the answer to?)
- 1-3: no curiosity gap; viewer learns nothing from clicking
- 4-6: vague gap ("learn this"), low-stakes
- 7-9: specific question with implied stakes ("WHICH line?", "$X for what?")
- 10: viewer cannot stop thinking about the answer until they click
- **Score: __ / 10**

#### 3. Emotional strength (does the package activate one of: fear, identity, loss, status, curiosity?)
- 1-3: emotionally flat
- 4-6: mild interest
- 7-9: strong activation of ONE emotional driver
- 10: 2+ emotions stacked (e.g. fear + identity)
- **Score: __ / 10**

#### 4. Visual simplicity (foveal singularity — one element wins the eye)
- 1-3: 4+ elements competing
- 4-6: 3 elements, hierarchy unclear
- 7-9: 1 focal + 1 supporting + optional text, clean hierarchy
- 10: ONE element, full stop, every other pixel serves it
- **Score: __ / 10**

#### 5. Mobile readability (test at 200×112 px)
- 1-3: text unreadable at mobile size, focal element disappears
- 4-6: focal element survives but text is borderline
- 7-9: focal element + text clear at mobile size
- 10: package is MORE compelling at 200×112 than at full size (true mobile-first design)
- **Score: __ / 10**

#### 6. Specificity (concrete numbers, named entities, or specific objects)
- 1-3: vague ("save thousands", "common mistake")
- 4-6: somewhat specific ("save $5,000", "this question")
- 7-9: specific + non-round ("save $4,847", "the F&I office")
- 10: hyper-specific with proof anchor ("the $390 cost vs $2,400 markup")
- **Score: __ / 10**

#### 7. Credibility (does this read as an expert revealing real information, or as bait?)
- 1-3: feels like clickbait, "scammy" tone
- 4-6: borderline — could be either
- 7-9: clearly authoritative, calm-confident
- 10: package establishes expertise without saying it explicitly (showing > telling)
- **Score: __ / 10**

#### 8. Novelty (have we shipped this exact pattern before? have competitors?)
- 1-3: identical to last 3 AUDM videos OR identical to a competitor
- 4-6: similar to recent uploads, slight variation
- 7-9: new template within AUDM library, not in competitors' last 30 days
- 10: pattern interrupt — nothing else in feed looks like this
- **Score: __ / 10**

#### 9. Audience fit (does this match the AU 30-50yo professional buyer archetype?)
- 1-3: targets wrong demo (US viewer, hustle-culture vibe, generic finance)
- 4-6: AU-adjacent but not specific
- 7-9: clearly AU professional buyer, specific to the dealer-math niche
- 10: speaks directly to the buyer who's about to walk into a dealership
- **Score: __ / 10**

#### 10. Retention alignment (does the package promise something the first 30 seconds delivers?)
- 1-3: package promises X, video delivers Y — bait
- 4-6: package promises X, video delivers X eventually (~3 min)
- 7-9: package promises X, video delivers X in first 30s
- 10: cold-open is *more* engaging than the package promised — over-delivers
- **Score: __ / 10**

---

## Total — [X / 100]

**Average:** __ / 10

### Pass thresholds (mandatory before upload)

- [ ] Average ≥7/10
- [ ] Every category ≥6/10
- [ ] No category below 5 (auto-fail — rebuild that element)

### If pass: ship.
### If fail: rebuild the lowest-scoring element. Re-score. Repeat until pass.

---

## Worked examples — V1, V2, $46K Short scored

### V1 — "I Sold Cars for 10 Years — Never Answer This Question"

| Category | Score | Notes |
|---|---|---|
| Clarity | 8 | Title is clear; "never answer this question" raises it cleanly |
| Curiosity | 7 | Strong "what question?" gap — but thumbnail closes it by repeating the line |
| Emotional strength | 7 | Authority + curiosity + mild fear |
| **Visual simplicity** | **3** | 5-line text wall + tiny supporting hand-on-contract = no foveal singularity |
| **Mobile readability** | **4** | Text wall illegible at 200×112; focal element invisible |
| Specificity | 6 | "10 years" is specific; "this question" is vague-but-intentional |
| Credibility | 8 | First-person 10-year credential is strong |
| Novelty | 5 | Authority-claim pattern is well-trodden in niche |
| Audience fit | 8 | AU + dealer + first-person = on-target |
| Retention alignment | 7 | Cold-open delivers the question (eventually) |

**Total: 63/100 · Average: 6.3/10 · FAIL** (below 7-avg threshold + 2 categories below 6)

**Diagnosis:** the title is fine; the THUMBNAIL fails on visual simplicity + mobile readability. Predicted by scorecard, confirmed by 1.7% CTR.

**Fix:** rebuild thumbnail per [competitor_swipe_file.md](competitor_swipe_file.md) V1 alternatives. Predicted score after fix: 8.5/10 average.

### V2 — "Why Every Australian Buyer Loses $4,800 in This One Room"

| Category | Score | Notes |
|---|---|---|
| Clarity | 8 | Title is clear |
| **Curiosity** | **5** | Title carries the curiosity but thumbnail repeats $4,800 verbatim, closing the gap |
| Emotional strength | 8 | Loss aversion + identity + specific number |
| **Visual simplicity** | **4** | 3 separate text blocks ($4,800 / LOST / ONE ROOM) compete for foveal attention |
| **Mobile readability** | **5** | Text fragments survive but document is too dim, focal element microscopic |
| Specificity | 9 | Non-round $4,800 + "every Australian buyer" + "this one room" |
| Credibility | 7 | Calm authority frame |
| Novelty | 6 | Specific-dollar reveal is on-brand but the execution is text-poster |
| Audience fit | 9 | Direct hit on AU professional buyer |
| Retention alignment | 5 | Title promises an answer in 60s; video delivers in 3+ min preamble |

**Total: 66/100 · Average: 6.6/10 · FAIL** (below 7-avg threshold + 3 categories below 6)

**Diagnosis:** the LOCKED 5/5 psychology-stack title got compromised by thumbnail redundancy AND retention-alignment gap. Predicted by scorecard, confirmed by 0.5% CTR + 26% retention.

**Fix:** rebuild thumbnail (Template C split-frame) + recut V2 cold-open via Studio Editor (start on the strongest insight line, not the coffee-handshake preamble). Predicted score after fix: 8.8/10 average.

### $46K Short — "Why your weekly payment costs $46K more"

| Category | Score | Notes |
|---|---|---|
| Clarity | 9 | Instant comprehension |
| Curiosity | 9 | "$46K more" = strong loss-aversion gap |
| Emotional strength | 9 | Loss + specific shocking number |
| Visual simplicity | 8 | First-frame foveal singularity holds (Short, not LF, but principle applies) |
| Mobile readability | 9 | Native 9:16 mobile-first |
| Specificity | 9 | Non-round $46K, "weekly payment" is anchor term |
| Credibility | 8 | Mac voice |
| Novelty | 8 | Counterintuitive — weekly payments costing MORE than monthly = pattern interrupt |
| Audience fit | 9 | AU dealer-math hot topic |
| Retention alignment | 8 | Sub-30s payoff |

**Total: 86/100 · Average: 8.6/10 · PASS**

**Result:** 470 views in 48h, 53.5% retention. Scorecard correctly predicted breakout.

---

## Calibration history

Track the scorecard's predictive accuracy over time. After every 5 videos, regress score against actual CTR + retention.

| Video | Predicted score | Actual CTR | Actual retention | Verdict (Q1/Q2/Q3/Q4) | Scorecard accuracy |
|---|---|---|---|---|---|
| V1 | 6.3 | 1.7% | 42% | Q3 (low CTR, decent retention) | ✅ predicted weak |
| V2 | 6.6 | 0.5% | 26% | Q4 (both low) | ✅ predicted weak |
| $46K Short | 8.6 | (Shorts CTR not exposed) | 53.5% | Q1 (gold) | ✅ predicted strong |

If scorecard fails to predict CTR ≥3 times: re-weight the categories. Likely culprits: visual simplicity weight too high vs specificity, or curiosity score is being inflated.

---

## Anti-inflation rules

To prevent score-inflation drift:

1. **No 9 or 10 unless you can name a specific reason.** "Feels strong" is not a reason. "Specific non-round number with named-entity proof anchor" is.
2. **Default to 5-7 range.** Most packages are average. Reserve 8+ for genuinely strong, 9-10 for elite.
3. **Score categories independently.** Don't anchor category 5 on category 4's score.
4. **Compare against competitors.** If your thumbnail wouldn't out-CTR a Cadogan thumbnail in the same feed, score it conservatively.
5. **Re-score after publish.** When CTR data comes in, ask: did I overscore curiosity? underscore retention-alignment?

---

## When the scorecard fails

The scorecard is a heuristic, not gospel. Override when:

1. **Specific data invalidates the score.** A scored-9 video flopped at 1% CTR. Re-weight the categories.
2. **Adrian explicitly disagrees on calibration.** His judgement on his own brand is final.
3. **A new pattern is mid-test.** Test & Compare hasn't locked yet — wait for the data, don't override the scorecard prematurely.

Otherwise: follow the scorecard. The discipline IS the edge.

---

## Filed-with

- [thumbnail_brief_template.md](thumbnail_brief_template.md) — pre-scoring brief
- [title_thumbnail_pairing_framework.md](title_thumbnail_pairing_framework.md) — pairing mode picker
- [ctr_testing_framework.md](ctr_testing_framework.md) — post-upload protocol
- [video_packaging_database_template.csv](video_packaging_database_template.csv) — DB schema
