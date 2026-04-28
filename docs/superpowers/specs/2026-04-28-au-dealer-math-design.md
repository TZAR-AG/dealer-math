# AU Dealer Math — Design Spec

**Status:** Approved 2026-04-28. Pending implementation plan (`writing-plans` next).

**Mission:** Faceless YouTube channel that publicly reveals how Australian car dealerships actually price cars + manipulate finance. Built on Adrian's 10-year AU automotive insider knowledge. Voice = "Macca" (pseudonym, AU voice actor cloned via ElevenLabs). Visual format = AI-illustrated cartoon stills + minor motion + stock B-roll insurance. Fully automated production pipeline orchestrated via n8n.

**Privacy lock:** Tecnica is Adrian's private valuation tool — NEVER referenced, shown, screen-captured, or named in any AU Dealer Math content, marketing, or operational artifact. Tecnica stays a closed competitive edge. Scripts use generic public-data framing ("the same data dealers see") without naming proprietary tools.

**Revenue target:** $1K AUD/mo passive at ~5-10K subs (~6-10 weeks). Year 1 ceiling: $20-40K AUD. Year 2 if 100K+ subs: $100-300K AUD.

**Daily commitment (Adrian):** 15-30 min during pilot phase, ~5 min/day after Phase 2 trust earned.

---

## 1. Persona — Macca

### Backstory (200 words, locked pre-pilot)

Macca worked the Australian automotive industry for ten years, dealer-side. He saw how the trade-in lowball math actually works on the floor, how finance managers stack margin into novated lease agreements that customers don't read, how "drive-away pricing" gets reverse-engineered to hit the target margin without the buyer noticing. He's not on the floor anymore. Now he scores fifty-plus AU listings every morning — same data the dealers see — and posts the math.

He doesn't show his face. He doesn't name dealerships. He's not here to torch anyone's livelihood. He's here because every Australian who walks into a dealership has been pre-conditioned to believe the dealer holds the math, and that's a $5-15K asymmetry sitting on top of every transaction. Macca's pitch is simple: the math isn't actually complicated. The dealers just hope you don't run it.

If a viewer recognises something in their own deal, they can ask in the comments. Macca answers like a mate who's seen the inside, not a journalist who's writing a story. He's not selling cars. He's selling fluency.

### Voice spec

- **Source:** Fiverr AU voice actor (~$80 one-time). Brief: AU male, 35-45 sound, calm-confident, slight blokey warmth, NOT corporate-radio-flat. Audition with the line: *"Most Aussies who walked into a dealership last weekend lost three grand before they sat down. Here's the math."*
- **Clone:** ElevenLabs Professional Voice Clone tier (Creator $99/mo). Settings: stability 0.55, similarity 0.4, style exaggeration 0.0.
- **Sign-off line (every video):** *"I'm Macca. I do this every morning. AU Dealer Math."*
- **Voice consistency rule:** every script passes the "would Macca actually say this" check before VO render. No corporate-jargon, no hype, no "transform your life", no "smash the like button".

---

## 2. Channel identity

| Field | Value |
|---|---|
| Channel name | **AU Dealer Math** |
| Tagline | *Run the numbers. Walk in fluent.* |
| YouTube handle | `@audealermath` (verify availability at registration) |
| Brand wrapper | Standalone — Capital Playbook stays parked |
| Primary geography | Australia |
| YT Studio category | **Education** (primary) + Howto & Style (secondary). Subtopics: Finance, Automotive. Locks 5-10× CPM swing per psychology research. |
| Cross-platform handles | IG `@audealermath` · TikTok `@audealermath` (claim Day 1, repurpose Shorts only initially) |

### Brand colors
- **Charcoal:** `#2B2B2B` (primary text, mascot outline)
- **Outback orange:** `#D17A3D` (accent, attention, dollar-figure reveals)
- **Cream:** `#F5EFE6` (background, paper-feel)
- **Charcoal soft:** `#4A4340` (secondary text)
- **Charcoal line:** `#E0E0E0` (rules, dividers)

Distinct from Capital Playbook (navy/gold/white) and Structured Self (sage/charcoal/cream) so the three faceless brands don't visually echo each other.

### Typography
- **Display / titles:** DM Sans Bold (already licensed in Adrian's stack)
- **Body / charts:** Inter Regular
- **Numerical reveals:** Fraunces (variable, italic) — for dollar figures + emphasis

---

## 3. Mascot — design brief (Fiverr, ~$200)

### Specification

- **Two recurring characters:** "The Dealer" + "The Buyer". Both ~6.5-head proportion (slightly stylised, not chibi, not realistic).
- **The Dealer:** Mid-40s AU male, polo shirt with logo erased, polished shoes, lanyard, smart-casual. Friendly outward, calculating inward. Distinguishing feature: clipboard always carried, never put down.
- **The Buyer:** 30s gender-neutral, casual clothes, slightly tense shoulders. Holding either a phone (researching) or keys (resigned). Expression palette: hopeful → confused → resigned.
- **Style:** Flat 2D vector aesthetic. Limited color palette matched to brand (charcoal + outback orange + cream). NO Disney/Pixar/Marvel-echoing proportions (oversized eyes, rounded baby-face features → off-limits per IP risk research).
- **Character refs needed:** 5 angles (front, 3/4 left, 3/4 right, profile, back) × 6 expressions (neutral, smiling, confused, resigned, suspicious, alert) per character. = 60 reference frames total.
- **Deliverables from Fiverr:** PSD/AI source files + transparent PNG character library + style guide. ~$200 budget. ~5-7 day turnaround.
- **Lock procedure:** before pilot starts, generate Midjourney `--sref` references from the Fiverr files so AI-generated dealership scenes maintain character consistency across videos.

### Trademark
- File for AU trademark on character design + AU Dealer Math wordmark before video 5 publishes (~$330 AUD via IP Australia). Protects brand in case content goes viral and copycats emerge.

---

## 4. Visual format spec

### Per-video composition (8-15 min long-form)

| Layer | % of runtime | Source | Notes |
|---|---|---|---|
| AI-illustrated stills (Macca + Dealer + Buyer + dealership scenes) | ~70% | Midjourney with locked character refs | Held 60-90 sec each with Ken Burns zoom. ~30-50 stills/video. Curatable consistency = beats AI motion drift. |
| AI motion clips (hook moments, transitions) | ~10% | Kling 3.0 | 5-15 sec each. Cold open + 1-2 transitions + close. NOT for character action — Kling for environmental motion (dealership lot, money, rain on cars). |
| Real B-roll insurance | ~10% | Storyblocks + public Carsales/Drive listing screenshots + AU dealership stock footage | **Mandatory layer** — pure AI animation = -25-35% retention vs hybrid. Real footage dodges YT AI-moderator + lifts retention. NO Tecnica footage anywhere. |
| Sketch charts (data reveals) | ~10% | Procreate iPad sketch aesthetic | Hand-drawn style à la HMW. Adrian sketches once, library grows over time. |

### Pattern interrupt cadence (locked from psychology research)
- **0-60 sec:** pattern interrupt every 3-5 sec (camera move, character entry, motion clip, color flash, text reveal)
- **60 sec onward:** widen to every 5-8 sec
- **Comedy beat:** ~1 per 30-45 sec (visual gag, ironic line, dealer-buyer micro-interaction)

### B-roll cycling rule
- First 3 minutes: image change every 3-5 sec
- After 3 minutes: image change every 5-8 sec
- Never hold one still > 90 sec without zoom/pan motion

---

## 5. Title formula (locked for first 20 videos)

Templated CTR compounds because the brain stops processing format and only processes the variable (Easy Actually's playbook — 1.1M subs from one phrase).

**Primary template (use 14 of first 20):**
- *"What Your Aussie Dealer Won't Tell You About [X]"*
- Variables: drive-away pricing, novated leases, trade-in math, finance margin, on-road costs, EOFY runout, demo cars, fleet returns, GST + LCT math, Toyota dealer profit, ute markup, EV FBT exemption, etc.

**Secondary templates (use 6 of first 20 to test):**
- *"Inside the Aussie Dealership: [X]"* (insider-walkthrough framing)
- *"$X is What Your [Car] is Really Worth in [City] Right Now"* (number-reveal framing — Luke's threshold playbook)

**Avoid:**
- Cadogan-style snark ("FAKE / BUSTED / EXPOSED" caps)
- AI-template signals ("You Won't Believe", "Doctors Hate This")
- Hype words ("transform", "secret", "hack")

**A/B test rule:** after 20 videos, pick top-3 winners by retention + CTR, lock those, test 5 new patterns. Repeat every 20 videos.

---

## 6. Script structure (8-15 min long-form, locked template)

| Section | Time | Content | Animation density |
|---|---|---|---|
| Hook | 0:00-0:25 | Vivid scene + named-victim opener: *"Somewhere in Australia today, someone earning $70K is at a dealership about to sign on a $55K car. They'll stretch the loan over 7 years, pay close to $15K in interest. Here's the math they didn't show."* | Pattern interrupt every 3 sec — Macca character enter, Dealer character enter, dollar-figure reveal, Kling motion of dealership lot |
| Reframe | 0:25-1:00 | "But here's what nobody tells you..." | Continued 3-5 sec interrupts |
| Problem deep-dive | 1:00-3:30 | The behavioural + economic mechanism. Numbers shown step-by-step. ~600 words. | 4-5 sec image cycle, sketch chart at 2:00 mark |
| Threshold / turning point | 3:30-5:00 | The pivot moment: "$X is the line where everything changes" | Slow zoom on number reveal, voice intensity shift |
| Practical unlocks | 5:00-9:00 | Numbered list — exactly 4 items consistently (Luke playbook). Each item = ~30-40 sec. | 5-8 sec image cycle, sketch chart per item |
| Recap + CTA | 9:00-10:30 | One-line recap of all 4 unlocks + Macca sign-off + lead magnet pitch ("link in description for the 7-lines PDF") | Slow zoom on Macca character, end-card builds |

**Voice intensity rule:** intensity must shift on every dollar-figure reveal + threshold moment. Monotone narration is the #1 killer of retention >5 min.

**Lead-magnet CTA bake (locked from video 1):** every script has the Macca line *"There's a free PDF in the description — the 7 lines on a dealer contract you should never sign. Grab that, and run the math next time."* Inserted at 9:30 mark.

---

## 7. Production pipeline — n8n workflow

### 7a. Weekly topic generation (Sunday cron)

Every Sunday at 18:00 AWST, n8n fires a topic-research workflow:

1. Claude API scrapes inputs:
   - **AU automotive news** (last 7 days) via WebSearch — Drive.com.au, CarsGuide, Carsales news, Toyota AU + Ford AU + Mazda AU corporate announcements, ATO publications on FBT/novated leases
   - **Reddit signals** via Reddit MCP — top posts past week from r/AusFinance, r/CarsAustralia, r/AusEcon, r/PersonalFinanceAU
   - **Topic queue history** — what's been published already (anti-repeat dedupe)
   - **AU-specific calendar markers** — EOFY proximity, RBA meetings, fuel-excise changes, holiday driving seasons
2. Claude API generates **10 topic candidates** with: title hypothesis (in locked formula), 1-line angle, current-relevance hook, suggested mascot scene, estimated AU search volume hint
3. n8n drops the 10 candidates into Adrian's Google Sheet (column A = title, B = angle, C = relevance, D = pick? checkbox)
4. **Adrian: ~15 min Sunday** — ticks 5 of the 10 boxes
5. n8n moves the 5 picked into the daily topic queue, ordered Mon/Wed/Fri (or Mon-Sat if daily cadence post-pilot)

Output: rolling 7-day topic queue, refreshed every Sunday. Always one week of runway.

### Phase 1 (manual approval, first 12 videos)

```
06:00 AWST cron fires
    ↓
1. Pull today's topic from Google Sheet (topic queue auto-generated weekly — see § 7a)
    ↓
2. Claude API → 1500-word script + title + description + 5 thumbnail concepts
    ↓
3. PAUSE — n8n notifies Adrian (Telegram/email) with script
    ↓
4. ADRIAN CHECKPOINT #1 (5 min) — rewrites hook, injects 1 original POV line, approves
    ↓
5. Midjourney API → 30-50 illustrated stills using locked character refs
    ↓
6. ElevenLabs API → Macca voiceover MP3 (clone voice ID, locked settings 0.55/0.4)
    ↓
7. Kling 3.0 → 3-5 hook-moment motion clips
    ↓
8. Storyblocks API → 5-10% real B-roll inserts (dealer lots, auctions, money close-ups, AU street scenes, public Carsales/Drive listing screenshots)
    ↓
9. InVideo AI Max → assembles all assets → rendered MP4 (~10-15 min unattended)
    ↓
10. Thumbnail generation → existing youtube-thumbnail skill outputs 3 variants
    ↓
11. PAUSE — n8n notifies Adrian
    ↓
12. ADRIAN CHECKPOINT #2 (10 min) — watches MP4 at 2× speed, picks 1 of 3 thumbnails, approves
    ↓
13. YouTube Data API → uploads as private, schedules for 18:00 AWST publish
    ↓
14. Submagic API → auto-generates 3 Shorts from long-form
    ↓
15. Blotato → cross-posts Shorts to TikTok + IG Reels at staggered times
    ↓
16. n8n logs to Google Sheet: video URL, render time, total cost, status
```

**Total Adrian time:** 15-30 min per video. **Render time:** 30-45 min unattended. **Total elapsed:** 60-75 min cron-to-publish.

### Phase 2 (auto-publish + spot-check, post-pilot)

After pilot demonstrates quality (defined in Section 11 — kill metrics), checkpoints #1 + #2 collapse into a single "automated quality gate":
- Script length 1400-1700 words ✓
- Voice render no errors ✓
- 30-50 stills generated ✓
- Real B-roll inserted ✓
- Thumbnail meets template spec ✓

If all pass → auto-publish. Adrian spot-checks 1-2 videos/week. Daily time drops to ~5 min.

---

## 8. Thumbnail template (locked Canva spec)

Steal HMW's signature: white slab-caps text + red underline on real photography.

| Element | Spec |
|---|---|
| Background | Real photo (car, dealership floor, money close-up, public Carsales listing screenshot) — 70% of frame |
| Mascot overlay (Macca character) | Bottom-right corner, 30% of frame, cutout from character library |
| Text | 3-6 word punch. White slab-caps (Inter Black at 110pt). |
| Underline | Outback orange `#D17A3D` squiggle hand-drawn under the most provocative word |
| Numbers | If dollar figure in title, render in Fraunces italic + outback orange, oversized |

**Templated 100% in Canva.** Adrian/n8n picks photo + types title text → Canva generates 3 variants → Adrian picks one at checkpoint #2.

---

## 9. Lead magnet — Day 1 hook

### *"7 Lines on a Dealer Contract You Should Never Sign"*

- **Format:** 8-page PDF, designed in same generator pipeline as Structured Self planner (Puppeteer HTML→PDF)
- **Content:** 7 specific contract clauses with dealer interpretation vs buyer-protection rewrite. Plain English. Each line gets 1 page.
- **Capture method:** Stan Store free product (zero-friction email capture, instant delivery)
- **CTA placement:** every video description + every Macca sign-off + pinned comment
- **Email follow-up sequence (Kit, 5 emails):**
  1. Day 0: Delivery + intro to Macca
  2. Day 3: "How dealers actually quote drive-away" (story)
  3. Day 5: "The novated lease trap" (math)
  4. Day 7: "What I'd do if I had to buy a car this weekend" (positioning)
  5. Day 10: First soft pitch — when $29-49 product launches (placeholder)

**Why Day 1:** every research agent flagged that AdSense-only is fragile post-2026. Email list = the moat that survives any algo shift. Easy Actually's mistake (1M subs, no list) is the anti-pattern.

---

## 10. Cadence + pilot plan

### 30-day pilot
- **Cadence:** 3 videos/week (Mon, Wed, Fri publish at 18:00 AWST — catches AU evening commute)
- **Total videos:** 12
- **Format mix:** 8 dealer-reveal (primary template) + 2 inside-the-dealership (secondary) + 2 number-reveal (secondary)
- **Approval:** manual every video (Phase 1)

### Pilot metrics (kill / scale triggers)

**Scale to daily cadence if ANY of these by Day 30:**
- Video 3 hits ≥10K views organically
- Average retention across 12 videos ≥40%
- Email list captures ≥100 subs from PDF lead magnet
- ≥1 video crosses 50K views

**Pivot positioning if NONE of the above:**
- Reduce to 2/wk for next 30 days
- Test secondary template families (Inside, Number-Reveal) at higher mix
- Deeper customer-voice research via Reddit MCP (r/AusFinance, r/CarsAustralia)
- Reconsider whether AU automotive cartoon is the right niche or pivot to AU Personal Finance Cartoon

**Kill the channel if:**
- After 60 days + 24 videos, no video has crossed 5K views
- Channel category is being misclassified by YT Studio (locked to Entertainment instead of Education) and CPM is sub-$5
- Demonetization warning issued by YouTube
- Adrian's manual edit time per video exceeds 45 min (rig is broken)

---

## 11. Monetization staircase (research-locked)

| Sub band | Action | Estimated monthly rev (AUD) | Timing trigger |
|---|---|---|---|
| 0-1K | YPP not yet eligible. Free PDF + Kit list build only | $0 | n/a |
| 1K-10K | YPP application + AdSense activated. Lead magnet from Day 1. | $50-1K | YPP requires 1K subs + 4K watch-hours |
| 10K-50K | Soft-launch $29-49 product (generic AU car-buying spreadsheet — not Tecnica-derived) | $1-5K | 10K-sub trigger |
| 50K-100K | Webinar funnel for $297-497 mid-tier course | $5-15K | 50K-sub trigger |
| **100K-250K** | **Flagship $497-997 "AU Car Buying System" course** | **$15-50K** | 100K-sub trigger (don't wait for 1M like Magnates Media — finance/auto buyers convert 5-10× harder than business-bio entertainment buyers) |
| 250K+ | Coaching tier $2-5K + novated lease affiliate stack (Driva $80-200/lead, Stratton Finance) + dealer-network referral arrangements | $50-200K+ | 250K-sub trigger |

**$1K/mo target hit at ~5-10K subs (~6-10 weeks from launch at 3/wk cadence).**

---

## 12. Cross-mission compounding

| Mission | How AU Dealer Math feeds it | How it feeds AU Dealer Math |
|---|---|---|
| **Tecnica** | **NEVER REFERENCED.** Tecnica stays Adrian's private competitive edge. No screen-captures, no name mentions, no implicit references. | Tecnica may inform Adrian's *thinking* about which topics matter (privately), but no Tecnica artifact appears in scripts, B-roll, or marketing. |
| **Capital Playbook** (parked) | n/a | n/a — kept separate. CP brand could be revived later as a finance-only sister channel. |
| **Structured Self** | n/a — kept separate. Different audience, different voice, different visual identity. | n/a |
| **Yard WA / Jacob** | Channel gives Adrian editorial cover (Macca is a content character, separate from Adrian's scout work). | Generic AU dealer-side patterns inform topic ideas, but NO specific deals, names, or proprietary data ever appears. |

---

## 13. Risk mitigation runbook

| Risk | Severity | Mitigation |
|---|---|---|
| YouTube July 2025 demonetization wave (16 channels deleted Jan 2026, 4.7B views, $10M/yr) | **HIGH** | Mandatory 5-min hook edit + 10-min QC + original POV insert per video. Manual approval Phase 1 → spot-check Phase 2. |
| AI character drift across daily videos | **HIGH** | Midjourney `--sref` + locked reference images. Generate all character shots in single session per video. Mascot evolves intentionally every 20-30 episodes (Skibidi expansion playbook), never through drift. |
| Disney/Pixar IP cease-and-desist | **MEDIUM** | Mascots designed from scratch via Fiverr (~$200), proportions/colors deliberately NOT echoing Disney/Pixar/Marvel. AU trademark filed before video 5 publishes ($330). |
| AU CPM only fires if YT Studio category = Education/Howto | **MEDIUM** | Lock category at registration. Verify category classification at 1K subs and again at 10K. Manual override if YT auto-classifies as Entertainment. |
| Cadogan overlap (439K incumbent) | **LOW** | Differentiation = FORMAT (cartoon storytelling vs his rant-cam) + DEPTH (specific deal math + AU public-data analysis vs his opinion-led journalism). Test 4 videos against retention threshold before committing beyond 30 days. |
| Adrian voice forensic ID | **LOW** (mitigated to negligible) | Voice = Fiverr AU actor clone, not Adrian's voice. No Adrian audio anywhere in pipeline. |
| AdSense-only fragility post-2026 | **HIGH** | Email + lead magnet from Day 1. Product launches at 10K (not 100K). Affiliate stack from 50K. Diversification day 1. |
| Audience fatigue from same-pipeline content | **MEDIUM** | Mascot evolves every 20-30 episodes. Title formula refreshes every 20 videos via A/B winner-rotation. Real B-roll layer keeps each video visually unique. |
| API auth-token rot (n8n + ElevenLabs + Midjourney + InVideo + YouTube) | **MEDIUM** | Mirror Adrian's existing `analytics-pull.md` token-discipline. Monthly health-check via `npm run tokens:check` extension. Auto-refresh where supported. |
| Yard WA / Jacob professional friction if dealer figures out it's Adrian | **MEDIUM** | No real-world dealer names in content. No Adrian voice. No identifying personal details. Pseudonym Macca + Fiverr voice = forensic separation. |

---

## 14. Implementation prerequisites (before Day 1)

| Task | Owner | Timeline | Cost |
|---|---|---|---|
| YouTube channel registration `@audealermath` + brand banner | Adrian | Day 1 | $0 |
| Fiverr mascot illustrator brief + commission | Adrian | Day 1-7 | ~$200 |
| Fiverr AU voice actor brief + 5-min recording | Adrian | Day 1-3 | ~$80 |
| ElevenLabs Creator subscription + Macca voice clone | Adrian | Day 3-5 (after voice sample) | $99/mo |
| Midjourney Standard subscription + character ref locks | Adrian | Day 8-10 (after Fiverr deliverables) | $30/mo |
| InVideo AI Max + Kling 3.0 + Submagic + TubeBuddy + n8n cloud subscriptions | Adrian | Day 1 | ~$103/mo |
| Storyblocks subscription | Adrian | Day 1 | $30/mo |
| Lead magnet PDF design + Stan Store free product setup | Adrian + Claude pipeline | Day 8-12 | $0 |
| Kit nurture sequence (5 emails) drafted | Adrian + Claude | Day 8-12 | $0 (existing Kit account) |
| n8n workflow built + tested end-to-end | Adrian + Claude | Day 5-10 | $0 (after subs active) |
| AU trademark application (mascot + wordmark) | Adrian | Day 5 publishes onward | ~$330 |
| First weekly topic-gen run (Claude proposes 10, Adrian picks 5) | Adrian + n8n | Day 10-12 | $0 |

**Total spend math:**
- **Pre-Day-1 one-time:** ~$330 (Fiverr mascot $200 + Fiverr voice $80 + channel banner/intro $50)
- **At video 5:** +$330 (AU trademark filing, IP Australia, single class)
- **Recurring monthly:** ~$280-300 (ElevenLabs $99 + Midjourney $30 + InVideo $50 + Kling $10 + Submagic $16 + TubeBuddy $7.50 + n8n $20 + Storyblocks $30 + Claude API $10-20)
- **Year 1 total:** ~$660 one-time + ~$3,360 recurring = ~$4,020 AUD
- **Break-even:** $1K/mo target (month 3-4) covers monthly burn; full Year 1 cost recouped by month 4-5 at target trajectory

---

## 15. Success criteria (Year 1)

- **Floor:** $1K AUD/mo recurring revenue achieved by month 3-4. Channel sustained at 3-5 videos/week.
- **Target:** $15K AUD/mo recurring revenue by month 12. 50-100K subs. Mid-tier course launched.
- **Stretch:** $30-50K AUD/mo recurring revenue by month 12. 100K+ subs. Flagship course shipped.
- **Kill threshold:** if $1K/mo not hit by month 6 OR Adrian's daily commitment exceeds 90 min sustained for 30+ days, pivot positioning under same channel OR sunset.

---

## 16. References

### Research agents (this session)
- Top AI/cartoon faceless channels — found Neural Viz solo template ($100/mo, 237K subs)
- AI video SaaS landscape — confirmed InVideo + ElevenLabs + Midjourney + Kling stack
- Cartoon viewer psychology — pure AI -25-35% retention vs hybrid (locks B-roll insurance layer)
- AU YouTube gap analysis — AU Automotive Cartoon = 9.5/10 white-space
- Channel teardowns: Sleepless Historian, Easy Actually, Boring History Secrets, PolyMatter

### Adrian's existing assets leveraged
- ElevenLabs Creator subscription (existing for Structured Self — separate Macca voice slot)
- 10 years AU dealer-side industry knowledge (script substrate only — Tecnica itself is private and never surfaces in content)
- 10 years AU automotive industry experience (script content moat)
- Six already-built Capital Playbook skills (`youtube-script`, `youtube-seo`, `youtube-thumbnail`, `content-calendar`, `pdf-product`) — adaptable to AU Dealer Math context
- Existing Stan Store + Kit + Zapier stack (lead magnet delivery + email nurture)

### Critical 2026 policy alerts
- Sora 2 shutting April 26 2026 (TWO DAYS from this spec date) — do not build on it
- Veo 3.1 (Jan 2026) is now default, $19.99/mo Google AI Pro
- Mandatory Disclosure Policy: must check "Altered or Synthetic Content" at upload — failure = permanent YPP ineligibility
- April 2025 + Jan 2026 enforcement waves wiped 16 channels (4.7B views, $10M/yr) for templated-no-narrative content

---

**Approved 2026-04-28. Next: writing-plans skill → implementation plan.**
