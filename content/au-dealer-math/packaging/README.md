# AUDM Packaging System — Operating Manual

**What this is:** the world-class title + thumbnail engine for AU Dealer Math. Built 2026-05-06 as the response to V1 (1.7% CTR) + V2 (0.5% CTR) underperforming the locked psychology-stack title formula. Diagnosis: the title formula was solid; the thumbnail was redundant; the title-thumbnail pairing wasn't designed. This system fixes all three.

**Authority:** This system overrides ad-hoc thumbnail decisions for V3+ onwards. Before any thumbnail goes to production, it must pass the scorecard at ≥7/10 average and ≥6/10 in every category.

---

## The 10 files in this system

| File | Read when | Edit when |
|---|---|---|
| [README.md](README.md) | First time setting up · onboarding helpers | Workflow changes |
| [youtube_packaging_strategy.md](youtube_packaging_strategy.md) | Quarterly review · when CTR data invalidates assumptions | After every V12 milestone |
| [competitor_swipe_file.md](competitor_swipe_file.md) | Looking for thumbnail inspiration · running a competitor sweep | Monthly competitor refresh |
| [title_formulas.md](title_formulas.md) | Drafting any new title | When a new pattern proves at ≥4% CTR over 3+ videos |
| [thumbnail_brief_template.md](thumbnail_brief_template.md) | Briefing every new thumbnail | When a template wins at ≥5% CTR over 3+ videos |
| [title_thumbnail_pairing_framework.md](title_thumbnail_pairing_framework.md) | Picking the pairing mode for a new video | After 12 videos of pairing-mode CTR data |
| [packaging_scorecard.md](packaging_scorecard.md) | Before every upload (mandatory gate) | Quarterly (calibrate weights against actual CTR data) |
| [ctr_testing_framework.md](ctr_testing_framework.md) | Day 2 + Day 7 + Day 14 of every video lifecycle | When YouTube changes Test & Compare behavior |
| [video_packaging_database_template.csv](video_packaging_database_template.csv) | Logging every video at 48h, 7d, 14d, 30d | Continuously (each video = 4 rows) |
| [prompt_library.md](prompt_library.md) | Brainstorming · diagnosing · iterating | When a prompt produces consistently weak output |

---

## Weekly operating workflow

### Pre-upload (every video, mandatory)

1. **Pick the pairing mode** — Mode A / B / C / D ([title_thumbnail_pairing_framework.md](title_thumbnail_pairing_framework.md))
   - AUDM default = Mode A (title teases, thumb explains via document forensics)
   - ~50% Mode A · 25% Mode B · 15% Mode C · 10% Mode D target distribution

2. **Draft 3-5 title candidates** ([title_formulas.md](title_formulas.md))
   - Pull from the 100 templates · stack ≥4 of 5 psychology triggers · 50-62 chars · defamation-safe word substitutions

3. **Brief the thumbnail** ([thumbnail_brief_template.md](thumbnail_brief_template.md))
   - Pick from the 5 AUDM templates (Circled Clue · Number on Document · Split-Frame Transition · Stamped Overlay · Annotated Cheatsheet)
   - **Rule of non-redundancy:** thumbnail must answer a DIFFERENT question than the title raises

4. **Score the package** ([packaging_scorecard.md](packaging_scorecard.md))
   - 10 categories × 1-10 each
   - **Pass thresholds:** ≥7 average AND ≥6 in every category. If any category <6, rebuild that element before shipping.

5. **Mobile preview** — open ThumbnailTest free-tier preview (mobile mockup). If the visual story doesn't read at 200×112px, rebuild. Then upload, set unlisted, view on actual phone arm's-length.

6. **Log to database** ([video_packaging_database_template.csv](video_packaging_database_template.csv))
   - Pre-upload: title, hook pattern, thumbnail concept, scorecard total, pairing mode, predicted CTR

### Post-upload (every video, mandatory data pulls)

| Day | Action |
|---|---|
| Day 0 | Reply to first comments within 60 min · Pin cheatsheet comment · Verify thumbnail lock in Studio |
| Day 2 (48h) | `cd generator && npm run audm:yt:pull` — pull CTR + retention. Plot on 4-quadrant grid. Log to DB. |
| Day 7 | Re-pull. Note CTR delta. If CTR <2% AND impressions >500, run re-package decision per [ctr_testing_framework.md](ctr_testing_framework.md) |
| Day 14 | Final verdict (Win / Workhorse / Archive). Log lesson to DB. If retention curve populated, log biggest-drop-off timestamp. |
| Day 30 | Compounding learning: sort DB by CTR descending. Stare at top 3 + bottom 3. Patterns emerge. |

### Monthly (1× per month)

- **Competitor sweep** ([competitor_swipe_file.md](competitor_swipe_file.md)) — pull recent high-performers from the 8 tracked channels. Add new patterns to the swipe file.
- **Scorecard recalibration** — if a video scored 9/10 but flopped, OR a video scored 6/10 and crushed, revise the rubric weights.

### After every 12 videos

- **Pattern audit** — sort DB. Lock in winners. Retire losers. Update [title_formulas.md](title_formulas.md) with proven patterns.
- **Re-score the strategy report** — does the strategic frame still hold given the data?

---

## File locations

All files in: `c:/dev/Claude/content/au-dealer-math/packaging/`

Database ingestion: append rows to `video_packaging_database_template.csv` (or copy as `video_packaging_database.csv` for live data).

Per-video log: `c:/dev/Claude/content/au-dealer-math/scripts/v0X-renders/v0X-package-log.md` (one per video).

---

## When to break the rules

This system is rigid by design — that's its job at sub-1K subs. Break it only when:

1. **A specific pattern proves at ≥6% CTR across 3+ videos** — promote it to default, retire competing pattern.
2. **Adrian explicitly overrides** — his judgement on his own brand voice is final.
3. **YouTube changes the algorithm in a documented way** — re-score affected sections.

Otherwise: follow the system. The discipline is the edge.

---

**Last updated:** 2026-05-06 · **Re-score:** at V12 publish · **Owner:** Adrian (channel) + Claude (system maintenance)
