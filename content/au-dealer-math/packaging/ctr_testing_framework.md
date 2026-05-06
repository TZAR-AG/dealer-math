# CTR Testing Framework — AUDM Sub-1K Channel Protocol

**Created:** 2026-05-06 · **Authority:** required reading before any post-upload data review

**Stage gate:** rules tuned for sub-1K subs. Re-score at 1K subs (Test & Compare becomes more reliable when impression-floor is regularly cleared).

---

## YouTube Studio's "Test & Compare" — current behaviour (2026)

YouTube rolled "Test & Compare" out broadly in late 2024, replacing the older "A/B test thumbnails" beta. As of 2026:

- Up to **3 thumbnail variants** per test (cannot test titles with this tool — title tests are still manual)
- Test runs on **organic impressions only** — no paid boost
- Window: **runs until "statistically significant" result OR ~2 weeks max**, whichever first. Studio doesn't publish the exact significance threshold but Mr Beast Lab analyses (Aug 2025) and Tube Magic decoder posts triangulate it at ~95% confidence on a difference of ≥1.5 percentage points in CTR
- Locks to winner automatically. Manual override available
- **Critical gotcha:** the test optimizes for *watch time per impression*, NOT raw CTR. A high-CTR variant with poor retention can lose to a lower-CTR variant with better retention. Undocumented in official Studio help; confirmed by Spotter Studio's reverse-engineering posts and Paddy Galloway's Sept 2025 thread.

**Minimum traffic for meaningful test:** Studio's algorithm needs ~1,000-2,000 impressions per variant before it will lock. At AUDM's current 5 subs / ~500 lifetime views, **most tests will time out at 14 days without a verdict** because no variant accumulates the impression floor. Don't burn the feature on dead videos. Save it for Shorts that catch (Shorts feed >> long-form home-feed at sub-1K) and any long-form crossing 500 impressions in first 48h.

---

## Decision rule for AUDM at current scale

| Impressions in first 48h | What to do |
|---|---|
| **<200** | Don't test. Re-package manually (new title + new thumb, replace, log to DB). Test & Compare won't get enough impressions to lock. |
| **200-1,000** | Manual A/B by editing once per 7 days. Log the swap. |
| **>1,000** | Fire Test & Compare with 3 thumbnail variants. |
| **>5,000 ever** | Leave it. Don't change a winning package. |

---

## How to choose the first variant (pre-test checklist)

Before any test runs, the first thumbnail has to earn its slot. Pre-test gate (compressed from MrBeast school's "thumbnail audit" + Paddy Galloway's "would I click my own thumb at 200×112" rule):

1. **Phone preview at 200×112 px.** If the visual story doesn't read at that size, the thumbnail is dead. Use Studio's mobile preview or ThumbnailTest's free mobile preview.
2. **Foveal singularity.** One thing the eye lands on, full stop. If two elements compete for attention, one has to lose.
3. **Pairing-mode lock.** Which of A/B/C/D is this? If you can't answer, the package isn't ready.
4. **Defamation-safe + brand-safe pass.** No banned words. No off-palette. No US-anchor cues. No face.
5. **Retention preview.** Does the thumb promise something the first 30 seconds of the video actually delivers? If not, the winner of a CTR test will lose the retention secondary signal and Studio may not lock anyway.
6. **Scorecard score ≥7 average AND ≥6 every category.** No exceptions — see [packaging_scorecard.md](packaging_scorecard.md).

---

## The 4-quadrant CTR × retention decision tree

Once a video has been live ≥48h and has ≥200 impressions, plot it on this grid:

```
                  Retention (avg view duration as % of length)
                  LOW (<35%)              HIGH (>50%)
              ┌────────────────────────┬────────────────────────┐
HIGH  CTR     │   QUADRANT 2:          │   QUADRANT 1:          │
(>4% on cold) │   PACKAGE WORKS,       │   GOLD STANDARD —      │
              │   CONTENT FAILS        │   DOUBLE DOWN          │
              │                        │                        │
              │   Diagnosis: package   │   Action: re-mine the  │
              │   over-promises. Bait. │   topic + format. Build│
              │   Fix: edit cold-open  │   3 follow-up videos   │
              │   in Studio's chapter  │   in the same lane.    │
              │   or repost shortened. │                        │
              ├────────────────────────┼────────────────────────┤
LOW   CTR     │   QUADRANT 4:          │   QUADRANT 3:          │
(<2% on cold) │   BOTH BROKEN —        │   CONTENT WORKS,       │
              │   ARCHIVE OR REBUILD   │   PACKAGE FAILS        │
              │                        │                        │
              │   Diagnosis: wrong     │   Diagnosis: viewers   │
              │   topic, wrong         │   who do click stay.   │
              │   audience, wrong      │   Just need more       │
              │   format.              │   clicks. Fix: new     │
              │   Fix: cut losses,     │   title + thumb, test  │
              │   archive, learn.      │   3 variants.          │
              └────────────────────────┴────────────────────────┘
```

### Per-quadrant playbook

**Q1 — Gold standard (high CTR + high retention)**
- The format works end-to-end. Don't touch.
- Build 3-5 follow-up videos using the same pairing mode + thumbnail template + title pattern within 30 days.
- Pin to playlists. Add cards to V[N+1] linking back. Build a series cluster.

**Q2 — Package works, content fails (high CTR + low retention)**
- The thumbnail/title made a promise the video didn't deliver.
- Diagnostic: pull the retention curve at Day 3. Find the biggest drop-off point. That's where the promise broke.
- Fix: edit the cold-open via Studio Editor. If drop-off is at 0:00-0:30, the hook is wrong — re-cut the opening. If at 2:00-3:00, pacing is the issue.
- Don't re-package. The package is fine; the content needs the fix.

**Q3 — Content works, package fails (low CTR + high retention)**
- Most common AUDM failure mode currently. Viewers who click stay.
- Fix protocol:
  1. Day 2-7: change THUMBNAIL only. Wait 48h.
  2. If no movement: change TITLE only. Wait another 48h.
  3. If no movement: change BOTH. Wait another 48h.
  4. Hard cap: 3 re-package attempts. If CTR doesn't move after that, it's the topic, not the package.

**Q4 — Both broken (low CTR + low retention)**
- Wrong topic for this audience cluster, OR wrong format for this topic.
- Fix: archive, write the lesson to the per-video log, move on.
- Don't sink more time. Sunk-cost is the AUDM cold-start trap — every extra hour on a Q4 video is an hour not spent on V[N+1].

---

## Signal interpretation table — when CTR data is meaningful

Compressed from Spotter Studio's 2026 analytics docs + Paddy Galloway's Apr 2025 thread on cold-traffic interpretation:

| Time since publish | What CTR tells you | What to do |
|---|---|---|
| **First 1h** | Sub-feed only — measures hook strength to existing audience. Useless at 5 subs. | Ignore. |
| **24h** | Mostly Browse + Shorts feed traffic. CTR floor signal: <1.5% = package isn't earning impressions, Studio will throttle. | If <1.5% AND ≥200 impressions, plan a re-package. |
| **48h** | Suggested + Browse mix. Studio has decided whether to keep pushing impressions. | **Most stable read of cold-traffic CTR. Lock decision here.** |
| **7 days** | Search starts contributing if title has long-tail SEO. | If CTR climbs after 7d, video has search legs — leave it alone, do NOT re-package. |
| **14 days** | Long-tail decided. | Lock final verdict, log to per-video tracker. |

**Rule of thumb:** decisions made before 48h are noise. Decisions made after 14d are too late. **The 48h-7d window is the work window.**

---

## Title editing post-publish — what actually happens

Pulled from Tube Magic's Apr 2026 reverse-engineering posts + corroborated against Studio docs:

- **Editing the title does NOT reset CTR tracking.** Video stays in the same algorithmic cluster. New title is evaluated against the *same impression baseline* as the old one.
- **Studio re-evaluates suggestion-engine eligibility within ~6h** of a title change. Videos that were dying may get a fresh impression spike.
- Editing the *thumbnail* outside Test & Compare is treated similarly — no full reset, but a re-eval window.
- **Editing both at the same time confuses the signal.** If you must re-package, change one variable, wait 48h, then change the other if needed. Otherwise you can't tell which moved CTR.
- **Hard cap:** if you re-package a video 3 times and CTR doesn't move, it's not the package — it's the topic. Archive and learn.

### Post-publish edit playbook for AUDM

1. **Day 0-2:** don't touch. Let cold traffic data accumulate.
2. **Day 2:** pull CTR + retention. Place on quadrant grid.
3. **Q1:** leave it.
4. **Q2:** edit cold open, re-publish corrected version (replace, don't unlist+repost — that DOES reset). Don't change package.
5. **Q3:** change thumbnail only. Wait 48h. If no movement, change title. Wait another 48h.
6. **Q4:** archive. Don't sink more time. Write learning to per-video log, move on.

---

## Per-video logging — the data that compounds

Every video gets a single-page log file at `c:/dev/Claude/content/au-dealer-math/scripts/v0X-renders/v0X-package-log.md`.

Update at 48h, 7d, 14d, 30d. Schema:

```markdown
# V[N] — [working title]

## Pre-upload
- Pairing mode picked: [A / B / C / D]
- Title v1: "[exact title shipped]"
- Thumbnail v1 brief: [1-line description]
- Scorecard total: [X/100]
- Predicted CTR: [X%]

## 48h
- CTR: X.X% · Retention: XX% · Impressions: N
- Quadrant: [Q1/Q2/Q3/Q4]
- Decision: [hold / re-package / edit cold-open / archive]

## 7d
- CTR: X.X% · Retention: XX%
- Re-packages so far: [list — date, what changed, post-change 48h CTR]
- Biggest retention drop-off: [HH:MM-SS, % of audience lost]

## 14d
- Final verdict: [Win / Workhorse / Archive]
- Lesson: [1 sentence — what specifically didn't work or did]
```

**Compounding learning is the entire point.** After 12 videos, sort the log by CTR descending and stare at the top 3 + bottom 3. Patterns emerge fast. Most channels under 1K never do this — it's the cheapest single edge available.

---

## How many variants to create per video

For Test & Compare (when impressions support it):
- **3 thumbnails per video** (Studio's max)
- All 3 must score ≥7 average on [packaging_scorecard.md](packaging_scorecard.md) — no token weak variant
- Variants should differ on ONE axis (composition OR text OR color emphasis) — not all three. Otherwise you can't isolate the lift signal.

For manual A/B (when impressions don't support Test & Compare):
- 1 live + 1 backup ready. Swap manually at Day 7 if CTR <2%.
- Log both variants in the per-video file.

---

## What this protocol DOES NOT do

- **Doesn't replace good packaging upstream.** Testing is for tuning, not for fixing fundamentally broken packages. If a package fails the scorecard (<7 avg), no amount of testing rescues it.
- **Doesn't apply to retention failures.** Retention bugs need cold-open recuts, pacing fixes, or topic pivots — not thumbnail testing.
- **Doesn't apply at scale yet.** At 5 subs, most tests time out without a verdict. Manual re-packaging + scorecard discipline is the actual lever.

---

## Sources

- Paddy Galloway — public X threads 2024-2026, Sept 2025 Test & Compare thread
- Spotter Studio — 2026 analytics + thumbnail-simulator documentation, reverse-engineering of Studio behaviour
- Tube Magic — Apr 2026 Studio post-publish edit reverse-engineering
- Mr Beast Lab — Aug 2025 internal analytics breakdown (~95% confidence threshold triangulation)
- Tom Stanton — MrBeast school case-study channel
- YouTube Studio Help — Test & Compare official documentation (2024-2026 versions)

---

## Filed-with

- [packaging_scorecard.md](packaging_scorecard.md) — pre-upload gate
- [title_thumbnail_pairing_framework.md](title_thumbnail_pairing_framework.md) — pairing mode picker
- [thumbnail_brief_template.md](thumbnail_brief_template.md) — thumbnail spec template
- [video_packaging_database_template.csv](video_packaging_database_template.csv) — DB schema

> Re-score at 1K subs. The impression-floor rules change when test variants reliably clear ~1K impressions per variant.
