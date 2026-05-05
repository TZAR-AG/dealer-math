# AU Dealer Math — YouTube Best Practices Playbook

Channel-level YouTube checklist applied to V1 onwards. Built against AUDM 8-point upload checklist + 2026 algorithm research + AU-specific category requirements. NO third-party SaaS dependency (no TubeBuddy, no vidIQ) — channel runs on free YT Studio + research files in this repo.

Reference for every video upload.

---

## 8-point upload checklist (hit ALL on every upload)

| Item | V1 status | How |
|---|---|---|
| ✅ High Res Thumbnail | locked | 1280×720 PNG, < 2MB. `v01-thumbnail.png` |
| ✅ Comment Pinned | drafted | Post pinned comment within 30 sec of publish |
| ✅ Comment Hearted | day-of | Heart your own pinned comment (red ❤ icon) |
| ✅ Info Cards Added | configure | 2-4 cards, see § Cards below |
| ⚠ Liked on Facebook | day-of | Even if FB engagement is low, this signal counts |
| ✅ Chapters Added | drafted | Min 3 chapters, first at 0:00, gap ≥ 10 sec |
| ✅ End Screen Added | drafted | Subscribe + most-recent upload, last 15 sec |
| ✅ Captions Added | use auto | YouTube auto-CC fine — Adrian rejected burnt-in. Auto-CC = SEO signal + accessibility |

---

## Pre-publish checklist (run for every video)

### Title (≤ 70 chars, AU geo-anchor in first 50)
- Lock title BEFORE drafting thumbnail (thumbnail must support, not contradict, the title)
- Title is editable in Studio post-publish (no re-upload needed) — if 24h CTR <3%, swap to fallback title from `reference_audm_title_formula_2026-05-04.md` PHASE 6 candidates
- Locked V1: `I Sold Cars in Australia for 10 Years — Never Answer This One Question` (74 chars · CTR estimate 8-12%)

### Thumbnail
- 1280×720 (16:9), PNG
- < 2 MB file size
- Readable at mobile feed scale (~200×112 px)
- Max 3-4 words on screen
- Face / body / object on left, text on right (or vice versa) — never centred behind text
- Brand colour anchor: charcoal #2B2B2B + outback orange #D17A3D
- Self-check: legible at ~200×112 mobile-feed scale (open the PNG at 17% zoom — if you can't read the headline, it's broken)
- Contrast check: charcoal #2B2B2B + outback orange #D17A3D + cream #F5EFE6 only; no off-brand colour
- YT Studio's native thumbnail A/B test unlocks at 1K subs — defer split-testing until then; before that, swap manually if 24h CTR <3%

### Description (optimise first 150 chars for "above the fold")
- Hook line in first 100 chars (mobile shows ~125 before "show more")
- Lead magnet link by char 200 max
- Keyword-load top paragraph naturally (don't keyword-stuff)
- Chapters (timestamps + readable titles)
- Synthetic voice disclosure (legal + community trust)
- Hashtags max 3 at end (`#AUDealerMath #CarBuyingAustralia #DealerFinance`)
- Locked template at [v01-youtube-metadata.md](scripts/v01-youtube-metadata.md)

### Tags (research-locked 2026-05-05 — see [research/yt-tags-2026-05-05.md](research/yt-tags-2026-05-05.md))
- **Locked target:** 20 tags · 480-498 YT-counted chars (multi-word tags wrap in quotes, +2 each)
- **Slot 1:** exact match brand `au dealer math`
- **Slots 2-3:** primary topic anchors (the 1-2 nouns the video is about)
- **Slots 4-7:** title-derived long-tail + 3 autocomplete-confirmed long-tails for the topic
- **Slots 8-20 (channel-wide constants — copy-paste on every video):** `car buying australia, dealer finance, car dealer tricks, car salesman tricks, australian car dealer, ex car salesperson, how to negotiate a car deal australia, car loan australia, finance manager dealership, how to buy a car australia, new car buying tips, dealership tricks, drive away price`
- **Char-budget verifier:** before publish, run `len(', '.join(f'"{t}"' if ' ' in t else t for t in tags))` — must be 480-498
- V1 + V2 final tag strings + V3-V25 topic-pack templates: see [research/yt-tags-2026-05-05.md](research/yt-tags-2026-05-05.md) § TL;DR + § Reusable formula
- Re-score after V12 publish using real Studio impression data
- Tag rankings only meaningful after 30+ days of data

### Chapters (min 4 for a 9+ min video)
- First chapter at 0:00 mandatory
- Min 10 sec gap between chapters
- Chapter title = curiosity hook, not section name
- ❌ "Introduction" ✅ "The question that ends the deal"
- Locked V1: 7 chapters at 0:00, 0:20, 0:53, 2:27, 4:40, 7:17, 9:36

### Cards (configure during upload)
- 2-4 cards per video
- Card 1 — Subscribe prompt at ~25% point (where viewers are committed)
- Card 2 — Lead magnet link at hook moment (~2:50, when "$46,800 more" lands)
- Card 3 (optional) — Related video / playlist (no playlist on V1, skip)
- Card 4 (optional) — Poll for engagement signal (avoid for V1, keep clean)

### End screen (last 15-20 sec)
- 2 elements minimum: Subscribe button + Most-recent upload
- Optional 3rd: Best-performing video (skip on V1, no other videos yet)
- 15 sec hold-time better than 20 sec for retention
- Locked design at [v01-youtube-metadata.md](scripts/v01-youtube-metadata.md) § End screen

---

## Channel-level setup (one-time, before V1)

### Profile picture (logo)
- 800×800 minimum, square crop
- Visible at 16×16 (small avatar size)
- High contrast against feed background
- Brand colour anchor

### Banner
- 2048×1152 PNG
- Safe zone: centre 1235×338 (mobile crops outer edges)
- DO NOT put critical text outside safe zone
- Brief locked at [v01-channel-banner-v1.md](scripts/v01-channel-banner-v1.md)

### About section / Description
- Channel description (paste from [channel-config.md](channel-config.md)):
```
AU Dealer Math is the channel that runs the numbers Australian car dealers don't want you to.

We break down dealer finance margins, novated lease math, trade-in lowball tactics, and on-road cost stitching — all from the perspective of someone who spent ten years on the dealer side.

Hosted by Macca. New explainers every Mon/Wed/Fri.

For the free PDF — "7 Lines on a Dealer Contract You Should Never Sign" — link below.
```

### Channel keywords (paste at Settings → Channel → Basic info)
```
au dealer math, australian car dealer, car buying australia, dealer finance, dealer tricks, car negotiation australia, novated lease australia, weekly car payment, drive away price, finance manager dealer, car loan trap, dealer secrets australia, ex car salesperson, automotive education australia, car buying tips
```

### Country + Category (CRITICAL — affects CPM)
- Country = **Australia** (NOT auto-detect)
- Default category = **Education** (NOT Entertainment / Animation)
- AU CPM premium $36.21 vs US $32.75 — both must hold
- YouTube auto-classifies new channels as Entertainment by default. Manual override during upload + at Settings → Channel.

### Custom URL
- Set to `@audealermath` (locked)

### Links section (Studio → Customisation → Links)
- Lead magnet: `audealermath.com.au/cheatsheet` (or Stan/Kit fallback URL until domain live)
- Email contact: `hello@audealermath.com.au`
- IG handle: `@audealermath`
- TikTok: `@audealermath` (when claimed)

### Featured video
- V1 is the featured video for non-subscribers (default)
- For returning subscribers, set "Featured for returning subscribers" = latest video (rotates automatically)

### Sections (homepage layout)
- Disable all sections for V1 launch (channel looks cleaner with just the featured video + uploads)
- Re-enable Sections after V3 publishes (gives YouTube enough videos to populate "Recent uploads")

---

## Free / manual replacements for SaaS-only workflows

We do NOT use TubeBuddy / vidIQ / any paid YT-tooling SaaS (per `feedback_no_new_saas_until_revenue.md`). Equivalents:

1. **Tag research** → `content/au-dealer-math/research/yt-tags-2026-05-05.md` (research-locked formula + per-video sets, refreshed at V12 publish via re-run of `generator/scrapling/yt-tag-pull.py`).
2. **Best-practice audit** → this doc + `reference_audm_title_formula_2026-05-04.md` + the per-video pre-build checklists in script files.
3. **Thumbnail check** → manual self-review at 17% zoom (mobile-feed scale) + the brand-palette lock in `.claude/rules/design-system-audm.md`.
4. **Thumbnail A/B test** → wait for YT Studio's native A/B (unlocks at 1K subs); pre-1K, swap manually if 24h CTR <3%.
5. **Card templates** → V3 onwards copy card config from V1/V2 (Subscribe at 25%, lead-magnet at hook moment).
6. **Tag rankings** → YT Studio Analytics > Reach > "Search results" surfaces real query data after 30 days. Source-of-truth for V12+ tag re-scoring.
7. **Bulk tag updates** → manual via Studio (or via `generator/au-dealer-math/upload-yt.mjs` if we add a `videos.update` path later — currently not built).

---

## Day-of-publish actions (in this order, within 60 min of going live)

1. **Verify it went live** at scheduled time (check YouTube Studio + the live channel URL)
2. **Drop pinned comment** within 30 sec — see template at [v01-youtube-metadata.md](scripts/v01-youtube-metadata.md) § Pinned comment
3. **Heart your own pinned comment** (red ❤ icon — algo signal)
4. **Cross-post on Facebook** — share video link to your personal feed (1 click). Even minimal engagement counts as cross-platform signal.
5. **LinkedIn share** — short personal-narrative caption + link
6. **Reddit value comments** — 30-60 min after publish, drop value-led comments in r/AusFinance + r/CarsAustralia threads (NOT link drops; only mention the channel if asked)
7. **TikTok + IG Reel cut** — 60-sec hook+fix native upload, "full on YouTube, search AU Dealer Math" caption
8. **Studio → Analytics → Realtime** — monitor first 60 min retention curve

---

## First-week monitoring (Day 0 → Day 7)

| Metric | Target | Action if missed |
|---|---|---|
| First 60-min CTR | 4-7% | Below 3% → swap thumbnail manually in Studio (replaces uploaded thumbnail; CTR test resets) |
| Avg view duration | ≥ 50% (~4:50 of 9:47) | Below 35% → check retention graph for cliff, note for V2 hook |
| Comment count Day 1 | ≥ 5 | Below 3 → reply to every existing comment to prompt more |
| Lead magnet clicks Day 7 | ≥ 2% of views | Below 1% → tighten card timing or rewrite description CTA |
| Subscriber lift | ≥ 0.5% conversion (≥ 1 sub per 200 views) | Below 0.3% → end-screen subscribe placement weak |

Reply to **every** comment within 2 hours for first 48 hours. Algo lift documented at 15-20% reach.

---

## 🔬 RESEARCH-BACKED ADDITIONS (2026-04-30)

Three findings from 2026 channel-growth research that materially change the playbook:

### YouTube Studio native A/B test — use on EVERY video from V1

YouTube Studio includes a free A/B test feature supporting 3 variants per video (thumbnail OR title). Documented **2.3× average CTR uplift** when used vs single-variant uploads (Thumbify 2026). 40%+ CTR lifts plausible at small N.

**Workflow:** every video upload includes 3 thumbnails — usually one each from templates A / B / C in the locked thumbnail engine. YouTube auto-rotates them across impressions, picks the winner after ~10K impressions or 1-2 weeks. No additional cost.

This single feature is worth more than chasing a "better" thumbnail tool.

### Lead magnet host = Kit landing page (NOT Stan, NOT custom Vercel)

Per 2026 research:
- Industry-mean lead magnet conversion = ~18%
- Kit's native landing-page → tag → sequence flow has the lowest friction for free PDFs in education niche (Embeddable 2026)
- Stan optimises for mobile transactions = wrong shape for free downloads
- Custom Vercel = solving a problem you don't have (no CRM tie-in)
- Kit cost: included in SS subscription — $0 incremental for AUDM

**Setup workflow:**
1. Kit dashboard → Landing Pages → New → "AU Dealer Math — 7 Lines on a Dealer Contract"
2. Upload PDF as the deliverable
3. Tag rule: incoming email gets tagged `audm-cheatsheet`
4. Sequence trigger: tag fires the AUDM nurture sequence (5 emails over 14 days)
5. Public URL: `audealermath.kit.com/cheatsheet` — drop into V1 description + pinned comment + cards
6. Add UTM: `?utm_source=youtube&utm_medium=v1&utm_campaign=launch`

### Thumbnail engine — 3 locked templates (Document Forensics added)

The 3 templates baked into `generator/au-dealer-math/thumbnail-engine.py`:

- **Template A — Big-Number Reveal:** dollar figure + 1-line headline over MJ backdrop. V1's choice.
- **Template B — Comparison Split:** two-panel "what dealer says vs what's true" with chevron divider. Best for direct-myth-bust videos.
- **Template C — Document Forensics:** zoomed contract/document close-up + red highlight on a clause + dollar callout. **Most on-brand for AUDM** (per 2026 niche research). Best CTR pattern for AU finance education.

Per video: render all 3 variants, upload all 3 to YouTube Studio A/B test, let the winner emerge.

### AU finance niche thumbnail rule

Per 2026 niche research: AU finance YouTube **explicitly avoids US-style screaming-face / all-caps clickbait thumbnails**. AU audience prefers calmer, authoritative styling — comparable to MoneySmart AU / Glen James / Aussie Finance With Luke patterns.

For AUDM: max 4-6 words on screen, 2-3 brand colours, dollar figures in yellow accent (NOT red), document/contract close-ups over face shots. Document Forensics template fits this rule best.

---

## 🚀 HIGH-IMPACT GROWTH LEVERS (don't skip these)

These are the things that separate a channel that hits 10K subs in 6 months from one that stalls at 500. Most creators skip them.

### 1. Shorts strategy — the #1 discovery lever for new channels (DO THIS WITH V1)

YouTube Shorts feed gets 70 BILLION daily views. New channels get 10-100× more impressions on Shorts vs long-form. Cut V1 into vertical clips today:

- **Short 1: The hook** (0:00–0:30 of V1) — "If a salesperson asks your weekly budget, they've already won."
- **Short 2: The $46K reveal** (2:50–3:20) — visual punch on the loan-term math
- **Short 3: The two-sentence fix** (7:17–7:50) — what to actually say at the dealership
- **Short 4: The three rooms** (4:40–5:20) — what dealerships hide structurally
- **Short 5: The aftercare margin** (6:00–6:30) — the $1,000-2,500 gross reveal

Each Short:
- 9:16 vertical, 1080×1920
- 30-50 sec ideal
- Caption baked in (Shorts watched 80% sound-off)
- End frame: "Full breakdown on the channel — search AU Dealer Math"
- Title format: `The question Aussie car dealers don't want you to answer #shorts`
- Same description footer + 3 hashtags only
- Schedule one per day Day 0 → Day 4 to maintain channel activity

**Tools:** CapCut (fastest for vertical reframe + auto-caption) or DaVinci (manual but consistent). Each Short = 30-60 min production.

### 2. Branding watermark (subscribe button on every video)

YouTube Studio → Customisation → Branding → **Video watermark**. Upload a small (150×150) AUDM logo PNG. Appears bottom-right of every video for the last 90% of runtime. Hovering it shows a subscribe button.

- Causes a 5-10% subscriber-rate lift across the channel
- One-time setup, applies to V1 onwards retroactively
- Use a transparent-background PNG so it overlays cleanly

### 3. Channel trailer (auto-plays for non-subscribers)

A 30-60 sec "what this channel is about" video that auto-plays on the channel page for visitors who haven't subscribed yet. Massive sub-conversion lever.

V1 itself is too long to use as a trailer. Build a dedicated 45-sec trailer:
- 0-5s: Hook ("I sold cars in Australia for 10 years.")
- 5-30s: 3 quick "you'll learn" beats
- 30-45s: "New explainers Mon/Wed/Fri. Subscribe so you don't get burned at your next dealership visit."

Studio → Customisation → Layout → "Video spotlight" → set trailer.

### 4. Playlist setup (even with 1 video)

Create the playlist **"AU Dealer Math — Start Here"** with V1 as the only video for now. Then:
- V2-V12 auto-add to it
- Anyone watching V1 sees "next in playlist" = auto-plays V2 when published
- Session time on channel goes up (algo loves this)
- The playlist URL is shareable on Reddit/IG/etc

Studio → Content → Playlists → Create playlist.

### 5. Verbal subscribe prompts (V2+ requirement)

Bake INTO V2 script:
- ~30% mark: *"If you've never had this kind of breakdown before, hit subscribe — there's another one in 2 days that pulls apart..."*
- ~70% mark: *"And before we get to the fix, if this is saving you tens of thousands at your next dealership visit, that's what subscribing is for."*

Do NOT shoehorn into V1 (already rendered). Add to V2 script template + every script onwards.

### 6. Open-loop hook (V2+ requirement)

Bake INTO every script's first 15 sec. After the pattern interrupt, drop a forward-loop:

> *"By the end of this video, you'll know exactly which question to refuse to answer at any Australian dealership — and the two-sentence response that flips the negotiation. But first..."*

The viewer's brain needs the loop closed. They'll watch through to the end. Documented +15-25% avg view duration in finance-explainer niches.

### 7. Lead magnet UTM tracking (set up before V1 publish)

Don't use bare `audealermath.com.au/cheatsheet`. Use:
```
https://audealermath.com.au/cheatsheet?utm_source=youtube&utm_medium=v1_description&utm_campaign=launch
```

If using Stan/Kit fallback, attach UTM params there too. Lets you measure:
- % of viewers clicking lead magnet
- Which placement (description vs pinned comment vs card) drives most clicks
- Conversion rate by source

### 8. Engagement velocity in first 60 minutes (make-or-break)

YouTube tests every new video on subs + small cohort first. If first-60-min signals are strong, distribution expands 10-100×.

Within first 30 min of publish:
- **Notify your network** — text family/friends with the YT link, ask them to watch + comment with a make/model question (organic-feeling). Do NOT ask for likes/subs (fake engagement detection).
- **Reply to every comment within 5 minutes** for first hour. Algo lift documented at 15-20% reach.
- **Pin the engagement-bait comment** asking for make/model in replies — every reply = signal
- **Drop value comments on competitor channels** in same niche (Aussie Finance with Luke, Cars Guide AU, CarSales videos) — value-led, NOT link drops. People click the commenter's profile.

### 9. Active commenting on adjacent channels (long-tail discovery)

Comment value-led on:
- Aussie Finance with Luke (similar AU finance audience)
- CarsGuide YouTube
- CarExpert Australia
- Drive.com.au videos
- CarSales videos

Rules:
- Add value (specific insight, math, perspective) — never plug
- Use channel handle if asked
- Don't spam — 1-2 quality comments per week per channel
- Visible to thousands; commenter profile click-through is real

### 10. Community tab (unlocks at 500 subs)

Until then, skip. After 500 subs:
- Poll: "Which dealer trick should we break down next?" with 4 options
- Behind-scenes shot
- Quote card from a customer comment
- Posts every 3-4 days = stays in subs' feed

Highest-engagement format: polls. Drives next-video planning + sub-conversion via "loyalty rewards."

---

## What NOT to do

- ❌ Auto-share via Zapier (kills authenticity signal vs manual share)
- ❌ Buy views / engagement (instant deboost on detection)
- ❌ Use clickbait title that doesn't match content (CTR-then-bounce hurts more than low CTR)
- ❌ Post any specific dealer brand allegations (defamation rule, see [scripts/](scripts/))
- ❌ Tag-stuff > 15 tags (signal noise hurts > help)
- ❌ Add captions burnt-in to V1 — auto-CC only ([feedback_audm_caption_tool memory](C:/Users/adria/.claude/projects/c--dev-Claude/memory/reference_audm_caption_tool.md))
- ❌ Schedule outside Sun 7-9pm AEST (V1 specifically; pilot gets best algo seeding) or Mon/Wed/Fri 6pm AWST (V2+)
- ❌ Enable kids content / Made-for-kids — would block targeted-ads, dropping CPM by 60%

---

## Reference

- 8-point upload checklist: § "8-point upload checklist" in this doc (no TubeBuddy / vidIQ — see "Free / manual replacements" section)
- 2026 algorithm research: agents 2026-04-29
- AU CPM benchmarks: Australian YT CPM data 2026
- V1 metadata: [v01-youtube-metadata.md](scripts/v01-youtube-metadata.md)
- Channel config: [channel-config.md](channel-config.md)
- Caption decision: memory `reference_audm_caption_tool.md` — auto-CC only, no Submagic
