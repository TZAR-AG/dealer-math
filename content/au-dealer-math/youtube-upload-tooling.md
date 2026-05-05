# YouTube Upload Tooling — AUDM

CLI for uploading AUDM mains + Shorts to YouTube via the YouTube Data API v3,
replacing the manual YT Studio click-flow. Saves ~3-4 min per upload across
V3-V25 (24 mains + ~120 Shorts ≈ 7-9 hours).

## Files

- `generator/au-dealer-math/yt-upload-setup.mjs` — one-time OAuth flow
- `generator/au-dealer-math/upload-yt.mjs` — single-video CLI
- `generator/au-dealer-math/upload-yt-batch.mjs` — multi-video JSON-spec runner
- `generator/dashboard/pullers/.yt-upload-access-cache.json` — auto-managed access-token cache
- `.env` keys added: `YT_UPLOAD_REFRESH_TOKEN` (separate from existing read-only `YT_REFRESH_TOKEN`)

## One-time setup

The upload tool needs broader OAuth scopes than the analytics pull
(`youtube.upload` + `youtube.force-ssl`). It does NOT touch the
existing analytics token — both refresh tokens live in `.env`
side-by-side.

```bash
cd generator
npm run yt-upload:setup
```

Flow:
1. Script prints an OAuth URL.
2. Open the URL in your browser, sign in to the AUDM YouTube account, click
   Allow on the consent screen (you'll see "manage your YouTube videos" —
   that's the upload scope).
3. Browser redirects to `http://127.0.0.1:47824/callback` — local server
   catches the code automatically.
4. Refresh token is exchanged + written to `.env` as `YT_UPLOAD_REFRESH_TOKEN`.

Refresh-token lifespan: ~6 months. If a future upload errors with
`AUTH_FAILED` (HTTP 400 from `oauth2.googleapis.com/token`), re-run
`npm run yt-upload:setup`.

## Single-video upload

```bash
cd generator
npm run yt-upload -- \
  --file=video/out/shorts/audm-v2-short-1.mp4 \
  --title="What dealers do in the F&I office" \
  --description-file=content/au-dealer-math/scripts/v02-shorts-metadata.md#short-1-description \
  --tags=AUDealerMath,DealerFinance,shorts \
  --category-id=22 \
  --schedule=2026-05-05T18:00:00+08:00 \
  --thumbnail=content/au-dealer-math/scripts/v02-renders/thumbnails/short-1.png \
  --comment-file=content/au-dealer-math/scripts/v02-shorts-metadata.md#short-1-pinned-comment
```

### Flags

| Flag | Required | Notes |
|---|---|---|
| `--file` | yes | MP4 path (absolute or relative to repo root) |
| `--title` | yes | ≤100 chars; `<` and `>` rejected |
| `--description-file` | yes | path or `path#anchor` (see below); body ≤5000 chars |
| `--tags` | no | comma-separated; total ≤500 chars |
| `--category-id` | no | default `22` (People & Blogs); `27` = Education for AUDM mains |
| `--schedule` | no | ISO8601 (e.g. `2026-05-05T18:00:00+08:00`); forces privacy=private + publishAt |
| `--privacy` | no | `private` \| `unlisted` \| `public`; default `private`; ignored if `--schedule` set |
| `--made-for-kids` | no | flag; default `false` (AUDM is general audience) |
| `--thumbnail` | no | `.png` or `.jpg`; ≤2MB; calls `thumbnails.set` after upload |
| `--comment-file` | no | path or `path#anchor`; posts via `commentThreads.insert` after upload |
| `--dry-run` | no | validate inputs + print payload; no API calls |

### `path#anchor` extraction

Both `--description-file` and `--comment-file` accept either a plain file
path (whole file body becomes the description/comment) or a `path#anchor`
form to extract a specific block from a multi-section markdown file.

Two anchor patterns:

1. **`short-N-description` / `short-N-pinned-comment`** — designed for the
   AUDM shorts-metadata files at `content/au-dealer-math/scripts/v0X-shorts-metadata.md`.
   Walks to the `### Short N — ...` heading and pulls the body of the first
   `**Description (...):**` or `**Pinned comment (...):**` block under it.

2. **Generic heading slug** — e.g. `#my-section-name` matches a heading
   (`# My Section Name`, `## My Section Name`, `### My Section Name`) by
   slugified title and returns the body until the next heading at the same
   or higher level.

### Output (success)

```
=== Uploaded ===
  Title:    What dealers do in the F&I office
  Video ID: abc123XYZ
  URL:      https://youtu.be/abc123XYZ
  Studio:   https://studio.youtube.com/video/abc123XYZ/edit
  Schedule: 2026-05-05T10:00:00.000Z  (status: private until publishAt)
  Thumbnail: set
  Comment:  posted (commentId=Ugkx...)
            MANUAL PIN required: https://studio.youtube.com/video/abc123XYZ/comments
  Quota used: ~1700 units
```

The `MANUAL PIN required` line is the load-bearing reminder — see Limitations.

## Batch upload

For posting a full week of Shorts in one shot, use a JSON spec:

```bash
cd generator
npm run yt-upload:batch -- --spec=content/au-dealer-math/uploads/v02-shorts-batch.json
```

### Spec format

```json
{
  "uploads": [
    {
      "file": "video/out/shorts/audm-v2-short-1.mp4",
      "title": "What dealers do in the F&I office",
      "description_file": "content/au-dealer-math/scripts/v02-shorts-metadata.md#short-1-description",
      "tags": ["AUDealerMath", "DealerFinance", "shorts"],
      "category_id": 22,
      "schedule": "2026-05-05T18:00:00+08:00",
      "made_for_kids": false,
      "thumbnail": "content/au-dealer-math/scripts/v02-renders/thumbnails/short-1.png",
      "comment_file": "content/au-dealer-math/scripts/v02-shorts-metadata.md#short-1-pinned-comment"
    },
    {
      "file": "video/out/shorts/audm-v2-short-2.mp4",
      "title": "Why a 2 percent markup costs you $3,000",
      "description_file": "content/au-dealer-math/scripts/v02-shorts-metadata.md#short-2-description",
      "tags": ["AUDealerMath", "CarFinanceAustralia", "shorts"],
      "schedule": "2026-05-06T21:00:00+08:00",
      "comment_file": "content/au-dealer-math/scripts/v02-shorts-metadata.md#short-2-pinned-comment"
    }
  ]
}
```

Each entry uses the same fields as the single CLI (snake_case JSON keys map to
kebab-case CLI flags: `category_id` → `--category-id`, etc).

Behaviour:
- Pre-flight quota estimate; warns >8,000 units; fails fast >10,000
- Uploads serially (no parallelism — quota and YT processing both prefer
  sequential)
- Halts on first failure (no auto-retry — surface the error so Adrian can
  decide whether to fix + restart with a trimmed spec)
- Writes `content/au-dealer-math/uploads/upload-log-{ISO}.json` with full
  result history

## Quota guidelines

Default daily quota is **10,000 units**. Per-call costs:

| Endpoint | Cost |
|---|---|
| `videos.insert` | 1,600 |
| `thumbnails.set` | 50 |
| `commentThreads.insert` | 50 |

Practical ceiling per day:
- ~6 mains/Shorts WITH thumbnail + pinned comment (1,700 each = 10,200, just over)
- ~6 mains/Shorts WITHOUT thumbnail (1,650 each = 9,900)
- ~5 if doing both safely under 8,500 (leaves headroom for analytics calls)

The batch helper estimates quota upfront and refuses to start if the run
exceeds 10,000. AUDM cadence is 1 main/day + 1 Short/day = ~3,400 units, so
quota is comfortable for the daily cadence.

If quota becomes a constraint at scale, request a quota increase via the
Google Cloud Console (typically takes 1-2 weeks; gets you to 1M units/day for
established channels).

## Limitations

What this tool **cannot** do (manual Studio steps required):

- ❌ **Pin a comment.** YouTube exposes no API endpoint to pin a comment, even
  for the channel owner. The tool posts the comment via the API, then prints
  the deep link — manually click "pin" in Studio (~5 sec). This is a known YT
  API gap, not a tool limitation.
- ❌ **Add Shorts "Related Video" card.** Studio UI only. Per current AUDM
  research, Shorts shouldn't link out anyway (kills feed-loop retention).
- ❌ **Add YT-Studio end-screen elements** (cards, end-screens with
  subscribe/related-video panels). Studio UI only.
- ❌ **Toggle "Allow embedding"** (defaults to allowed) or **"Notify subscribers"**
  (defaults to ON for public uploads). The API doesn't expose these knobs;
  defaults apply. For the AUDM cadence the defaults are correct.
- ❌ **Edit playlist membership.** Out of scope for V1; can be added later via
  `playlistItems.insert` (50 quota each) if it becomes a recurring need.

## Re-score conditions

- **Switch to a service account?** No — service accounts can't own
  YouTube channels. Installed-app OAuth is the correct + only path for
  channel-owned uploads.
- **Quota increase?** Request when AUDM hits 1K subs OR when daily upload
  cadence exceeds 5 videos/day for 7+ consecutive days.
- **Add playlist auto-add?** Add when AUDM has ≥3 active playlists Adrian
  consistently adds new uploads to (currently zero playlists set up).

## Reference

- Built: 2026-05-05 to eliminate manual YT Studio upload click-flow for V3-V25
- Auth pattern mirrors: `generator/au-dealer-math/yt-setup.mjs` +
  `generator/au-dealer-math/pull-yt-analytics.mjs`
- Hard-stop on AUTH_FAILED per `.claude/rules/analytics-pull.md`
- Existing analytics token (`YT_REFRESH_TOKEN`) is preserved untouched —
  upload uses a separate `YT_UPLOAD_REFRESH_TOKEN`
