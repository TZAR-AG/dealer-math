# V1 LAUNCH — Sun 3 May 2026 19:00 AWST

**Set phone alarm for 19:05 AWST Sun 3 May 2026.**

When alarm fires:
1. Open Claude on laptop
2. Say: **"run V1 post-publish stack"**
3. I execute everything autonomously

That's it. The rest of this file is for me — Adrian doesn't need to run any of these manually unless Claude is unavailable.

---

## What I (Claude) will do when triggered

### Step 1 — Pin V1 comment
Read `content/au-dealer-math/v1-pinned-comment.md` for the locked Mac-voice comment text.
Drive Chrome DevTools MCP to youtube.com → V1 video → comment box → paste → Post → 3-dot menu → Pin.

### Step 2 — Retroactively link V1 to Shorts 2-5
V1 was private when Shorts uploaded so couldn't be picked in "Related video" field.
For each of Shorts 2, 3, 4, 5: YT Studio → edit Short → Video elements → Cards → Related video = "The Payment-Not-Price Pivot" → Save.
(Short 1 may have been done at upload, verify and skip if so.)

### Step 3 — Cheatsheet funnel smoke test
Open audealermath.com.au/cheatsheet in incognito → sign up with `hello+v1-launch-test@thestructuredself.com` → wait for incentive email → click confirm link → verify v2 PDF downloads → delete test subscriber from Kit.

### Step 4 — Capture post-publish analytics snapshot
`cd generator && npm run audm:yt:pull`
First V1 views / AVD / impressions take 30-60 min to populate. Snapshot now creates the baseline + a follow-up pull at 21:00 AWST gives the first hour metrics.

### Step 5 — Punch list back to Adrian
Surface a tight summary: each step success/fail, anything weird flagged.

---

## Channel reference
- Channel: AU Dealer Math (`UCQkgMP50xK86Y3X0Z74ikzw`)
- Channel URL: youtube.com/@audealermath
- V1 title: "The Payment-Not-Price Pivot"
- Cheatsheet: audealermath.com.au/cheatsheet
- Brand rule: `.claude/rules/design-system-audm.md`

## Don't
- Don't post extra comments
- Don't reply to existing comments without Adrian's approval
- Pin comment is the only public-facing write
