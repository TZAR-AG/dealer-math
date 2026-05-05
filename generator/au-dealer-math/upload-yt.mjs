// AUDM YouTube upload CLI — single-video uploader.
//
// Uses the youtube.upload + youtube.force-ssl scopes obtained via
// `npm run yt-upload:setup` (separate refresh token from analytics).
//
// Usage:
//   npm run yt-upload -- \
//     --file=video/out/shorts/audm-v2-short-1.mp4 \
//     --title="What dealers do in the F&I office" \
//     --description-file=content/au-dealer-math/scripts/v02-shorts-metadata.md#short-1-description \
//     --tags=AUDealerMath,DealerFinance,shorts \
//     --category-id=22 \
//     --schedule=2026-05-05T18:00:00+08:00 \
//     --thumbnail=path/to/thumb.png \
//     --comment-file=content/au-dealer-math/scripts/v02-shorts-metadata.md#short-1-pinned-comment \
//     --dry-run
//
// Quota: videos.insert=1600 + thumbnails.set=50 + commentThreads.insert=50.

import fs from 'node:fs/promises';
import { createReadStream, statSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { Readable } from 'node:stream';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, '..', '..');
const ENV_PATH = path.join(ROOT, '.env');
const ACCESS_CACHE = path.join(ROOT, 'generator', 'dashboard', 'pullers', '.yt-upload-access-cache.json');

// ============================================================================
// Arg parsing
// ============================================================================

function parseArgs(argv) {
  const out = {};
  for (const arg of argv.slice(2)) {
    if (!arg.startsWith('--')) continue;
    const eq = arg.indexOf('=');
    if (eq === -1) {
      out[arg.slice(2)] = true;
    } else {
      out[arg.slice(2, eq)] = arg.slice(eq + 1);
    }
  }
  return out;
}

const args = parseArgs(process.argv);

function usage(msg) {
  if (msg) console.error(`X ${msg}\n`);
  console.error('Required flags:');
  console.error('  --file=<path>                MP4 to upload');
  console.error('  --title=<string>             ≤100 chars');
  console.error('  --description-file=<path>    .md/.txt path; supports #anchor for block extraction');
  console.error('Optional flags:');
  console.error('  --tags=a,b,c                 comma-separated, ≤500 chars total');
  console.error('  --category-id=22             default 22 (People & Blogs); 27=Education');
  console.error('  --schedule=<ISO8601>         e.g. 2026-05-05T18:00:00+08:00');
  console.error('                               implies privacyStatus=private + publishAt');
  console.error('  --privacy=<private|unlisted|public>  default private');
  console.error('  --made-for-kids              flag; default false');
  console.error('  --thumbnail=<path>           optional .png/.jpg');
  console.error('  --comment-file=<path>        post pinned comment (path or path#anchor)');
  console.error('  --dry-run                    validate + print payload, do NOT upload');
  process.exit(1);
}

if (!args.file) usage('--file is required');
if (!args.title) usage('--title is required');
if (!args['description-file']) usage('--description-file is required');

// ============================================================================
// Env + token refresh
// ============================================================================

async function loadEnv() {
  const envText = await fs.readFile(ENV_PATH, 'utf8');
  return Object.fromEntries(
    envText.split('\n')
      .filter(line => line && !line.startsWith('#') && line.includes('='))
      .map(line => {
        const eq = line.indexOf('=');
        return [line.slice(0, eq).trim(), line.slice(eq + 1).trim()];
      }),
  );
}

async function readAccessCache() {
  try {
    const raw = await fs.readFile(ACCESS_CACHE, 'utf8');
    return JSON.parse(raw);
  } catch {
    return null;
  }
}

async function writeAccessCache(token, expiresInSec) {
  const data = {
    access_token: token,
    expires_at: Date.now() + (expiresInSec - 60) * 1000, // 60s safety buffer
  };
  await fs.mkdir(path.dirname(ACCESS_CACHE), { recursive: true });
  await fs.writeFile(ACCESS_CACHE, JSON.stringify(data, null, 2));
}

async function getAccessToken(env) {
  const { YT_CLIENT_ID, YT_CLIENT_SECRET, YT_UPLOAD_REFRESH_TOKEN } = env;
  if (!YT_CLIENT_ID || !YT_CLIENT_SECRET || !YT_UPLOAD_REFRESH_TOKEN) {
    console.error('X Missing upload credentials in .env.');
    console.error('   Run "npm run yt-upload:setup" first.');
    console.error('   Required keys: YT_CLIENT_ID, YT_CLIENT_SECRET, YT_UPLOAD_REFRESH_TOKEN');
    process.exit(1);
  }

  const cached = await readAccessCache();
  if (cached && cached.access_token && cached.expires_at > Date.now()) {
    return cached.access_token;
  }

  const tokenRes = await fetch('https://oauth2.googleapis.com/token', {
    method: 'POST',
    headers: { 'content-type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({
      client_id: YT_CLIENT_ID,
      client_secret: YT_CLIENT_SECRET,
      refresh_token: YT_UPLOAD_REFRESH_TOKEN,
      grant_type: 'refresh_token',
    }),
  });
  const tokenJson = await tokenRes.json();
  if (!tokenJson.access_token) {
    console.error('X AUTH_FAILED refreshing upload token:', tokenJson);
    console.error('   STOP per analytics-pull rule. Re-run "npm run yt-upload:setup".');
    console.error('   Likely cause: refresh_token expired (~6mo lifespan) or revoked.');
    process.exit(2);
  }
  await writeAccessCache(tokenJson.access_token, tokenJson.expires_in || 3600);
  return tokenJson.access_token;
}

// ============================================================================
// Description-file / comment-file path#anchor parsing
// ============================================================================
//
// Supports:
//   path/to/file.md                  -> entire file body
//   path/to/file.md#anchor           -> extract one block from the file
//
// Anchor format: kebab-case slug. Two patterns supported:
//   (A) "short-N-description"  | "short-N-pinned-comment"
//       -> walks to "### Short N" heading, then extracts the contents of the
//          first `**Description (...):**` or `**Pinned comment (...):**` block
//          following it (up to the next bold-label or heading).
//   (B) Any other slug
//       -> looks for a heading whose slugified title matches the anchor
//          (## or ### or #), returns the body until the next heading at the
//          same-or-higher level.

function slugify(s) {
  return s
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-|-$/g, '');
}

function extractShortBlock(text, shortNum, blockType) {
  // blockType: 'description' | 'pinned-comment'
  const lines = text.split('\n');

  // Find the "### Short N" heading
  const headingRe = new RegExp(`^###\\s+Short\\s+${shortNum}\\b`, 'i');
  let i = lines.findIndex(l => headingRe.test(l));
  if (i === -1) return null;

  // Find the **Block label** within this section (until next ### or higher heading)
  const labelRe = blockType === 'description'
    ? /^\*\*Description\b[^*]*\*\*[:\s]*$/i
    : /^\*\*Pinned comment\b[^*]*\*\*[:\s]*$/i;

  i++;
  while (i < lines.length) {
    if (/^#{1,3}\s/.test(lines[i])) break; // hit next heading first
    if (labelRe.test(lines[i])) {
      // Collect block: skip blank lines, then collect until next blank-blank or
      // next bold-label or next heading or `---`
      i++;
      while (i < lines.length && !lines[i].trim()) i++;
      const out = [];
      while (i < lines.length) {
        const l = lines[i];
        if (/^#{1,3}\s/.test(l)) break;
        if (/^---\s*$/.test(l)) break;
        // Stop at next bold-label field (e.g. "**File:** ...", "**Pre-build checklist:**")
        // ONLY if we've already collected at least one non-blank line.
        if (/^\*\*[A-Z][^*]*\*\*/.test(l) && out.some(x => x.trim())) break;
        out.push(l);
        i++;
      }
      // Trim trailing blanks
      while (out.length && !out[out.length - 1].trim()) out.pop();
      return out.join('\n');
    }
    i++;
  }
  return null;
}

function extractByHeadingSlug(text, anchor) {
  const lines = text.split('\n');
  for (let i = 0; i < lines.length; i++) {
    const m = lines[i].match(/^(#{1,6})\s+(.+?)\s*$/);
    if (!m) continue;
    if (slugify(m[2]) !== anchor) continue;
    const level = m[1].length;
    const stopRe = new RegExp(`^#{1,${level}}\\s`);
    const out = [];
    for (let j = i + 1; j < lines.length; j++) {
      if (stopRe.test(lines[j])) break;
      out.push(lines[j]);
    }
    while (out.length && !out[0].trim()) out.shift();
    while (out.length && !out[out.length - 1].trim()) out.pop();
    return out.join('\n');
  }
  return null;
}

async function readContentRef(ref) {
  // ref = path OR path#anchor
  const hashIdx = ref.indexOf('#');
  const filePath = hashIdx === -1 ? ref : ref.slice(0, hashIdx);
  const anchor = hashIdx === -1 ? null : ref.slice(hashIdx + 1);

  const absPath = path.isAbsolute(filePath) ? filePath : path.join(ROOT, filePath);
  const text = await fs.readFile(absPath, 'utf8');

  if (!anchor) return text.trim();

  // Try the "short-N-description" / "short-N-pinned-comment" pattern first
  const shortMatch = anchor.match(/^short-(\d+)-(description|pinned-comment)$/i);
  if (shortMatch) {
    const block = extractShortBlock(text, parseInt(shortMatch[1], 10), shortMatch[2].toLowerCase());
    if (block !== null) return block.trim();
    throw new Error(
      `Could not find Short ${shortMatch[1]} ${shortMatch[2]} block in ${filePath}. `
      + `Looked for "### Short ${shortMatch[1]}" heading + "**${shortMatch[2] === 'description' ? 'Description' : 'Pinned comment'} (...):**" label.`,
    );
  }

  // Fallback: heading-slug match
  const block = extractByHeadingSlug(text, anchor);
  if (block !== null) return block.trim();

  throw new Error(`Could not resolve anchor "#${anchor}" in ${filePath}.`);
}

// ============================================================================
// Validation
// ============================================================================

function validateInputs() {
  const errors = [];

  // File
  const filePath = path.isAbsolute(args.file) ? args.file : path.join(ROOT, args.file);
  let fileStat;
  try {
    fileStat = statSync(filePath);
  } catch {
    errors.push(`--file not found: ${args.file}`);
  }
  if (fileStat && !fileStat.isFile()) {
    errors.push(`--file is not a regular file: ${args.file}`);
  }

  // Title
  if (args.title.length > 100) {
    errors.push(`--title is ${args.title.length} chars; YT limit is 100.`);
  }
  if (args.title.includes('<') || args.title.includes('>')) {
    errors.push(`--title contains < or >; YT rejects these.`);
  }

  // Tags
  let tagList = [];
  if (args.tags) {
    tagList = args.tags.split(',').map(s => s.trim()).filter(Boolean);
    const totalLen = tagList.reduce((n, t) => n + t.length + 2, 0); // +2 for quote-comma overhead
    if (totalLen > 500) {
      errors.push(`--tags total length ~${totalLen} chars; YT limit is 500.`);
    }
  }

  // Category
  const categoryId = args['category-id'] ? String(args['category-id']) : '22';
  if (!/^\d+$/.test(categoryId)) errors.push(`--category-id must be numeric.`);

  // Schedule
  let publishAt = null;
  if (args.schedule) {
    const d = new Date(args.schedule);
    if (isNaN(d.getTime())) {
      errors.push(`--schedule is not a valid ISO8601 datetime: ${args.schedule}`);
    } else if (d.getTime() < Date.now()) {
      errors.push(`--schedule is in the past: ${args.schedule}`);
    } else {
      publishAt = d.toISOString();
    }
  }

  // Privacy
  let privacy = (args.privacy || 'private').toLowerCase();
  if (!['private', 'unlisted', 'public'].includes(privacy)) {
    errors.push(`--privacy must be private | unlisted | public.`);
  }
  if (publishAt) privacy = 'private'; // schedule forces private+publishAt

  // Thumbnail
  if (args.thumbnail) {
    const thumbPath = path.isAbsolute(args.thumbnail) ? args.thumbnail : path.join(ROOT, args.thumbnail);
    try {
      const ts = statSync(thumbPath);
      if (!ts.isFile()) errors.push(`--thumbnail not a file: ${args.thumbnail}`);
      if (ts.size > 2 * 1024 * 1024) {
        errors.push(`--thumbnail is ${(ts.size / 1024 / 1024).toFixed(2)}MB; YT limit is 2MB.`);
      }
    } catch {
      errors.push(`--thumbnail not found: ${args.thumbnail}`);
    }
  }

  return {
    errors,
    filePath,
    fileSize: fileStat ? fileStat.size : 0,
    tagList,
    categoryId,
    publishAt,
    privacy,
    madeForKids: !!args['made-for-kids'],
  };
}

// ============================================================================
// Upload (resumable)
// ============================================================================

async function uploadVideo({ accessToken, filePath, fileSize, metadata }) {
  // Step 1 — initiate resumable session
  console.log('Initiating resumable upload session...');
  const initRes = await fetch(
    'https://www.googleapis.com/upload/youtube/v3/videos?uploadType=resumable&part=snippet,status',
    {
      method: 'POST',
      headers: {
        authorization: `Bearer ${accessToken}`,
        'content-type': 'application/json; charset=UTF-8',
        'x-upload-content-type': 'video/*',
        'x-upload-content-length': String(fileSize),
      },
      body: JSON.stringify(metadata),
    },
  );
  if (!initRes.ok) {
    const errText = await initRes.text();
    throw new Error(`Resumable init failed (${initRes.status}): ${errText}`);
  }
  const uploadUrl = initRes.headers.get('location');
  if (!uploadUrl) throw new Error('No Location header in resumable init response.');
  console.log('  ok: session opened\n');

  // Step 2 — single PUT with the full body (simplest reliable path for files we
  // expect to be ≤200MB Shorts/mains; resumable session protects against the
  // network blip case via session URL).
  console.log(`Uploading ${(fileSize / 1024 / 1024).toFixed(2)}MB...`);
  const fileStream = createReadStream(filePath);
  const putRes = await fetch(uploadUrl, {
    method: 'PUT',
    headers: {
      'content-type': 'video/*',
      'content-length': String(fileSize),
    },
    body: Readable.toWeb(fileStream),
    duplex: 'half',
  });
  if (!putRes.ok) {
    const errText = await putRes.text();
    throw new Error(`Upload PUT failed (${putRes.status}): ${errText}`);
  }
  const result = await putRes.json();
  console.log('  ok: upload complete\n');
  return result;
}

async function setThumbnail({ accessToken, videoId, thumbPath }) {
  console.log('Setting thumbnail...');
  const stat = statSync(thumbPath);
  const stream = createReadStream(thumbPath);
  const ext = path.extname(thumbPath).toLowerCase();
  const contentType = ext === '.png' ? 'image/png'
    : (ext === '.jpg' || ext === '.jpeg') ? 'image/jpeg'
    : 'application/octet-stream';
  const res = await fetch(
    `https://www.googleapis.com/upload/youtube/v3/thumbnails/set?videoId=${videoId}`,
    {
      method: 'POST',
      headers: {
        authorization: `Bearer ${accessToken}`,
        'content-type': contentType,
        'content-length': String(stat.size),
      },
      body: Readable.toWeb(stream),
      duplex: 'half',
    },
  );
  if (!res.ok) {
    const errText = await res.text();
    throw new Error(`Thumbnail set failed (${res.status}): ${errText}`);
  }
  console.log('  ok\n');
}

async function postComment({ accessToken, videoId, commentText }) {
  console.log('Posting pinned comment...');
  const res = await fetch(
    'https://www.googleapis.com/youtube/v3/commentThreads?part=snippet',
    {
      method: 'POST',
      headers: {
        authorization: `Bearer ${accessToken}`,
        'content-type': 'application/json',
      },
      body: JSON.stringify({
        snippet: {
          videoId,
          topLevelComment: {
            snippet: { textOriginal: commentText },
          },
        },
      }),
    },
  );
  if (!res.ok) {
    const errText = await res.text();
    throw new Error(`Comment insert failed (${res.status}): ${errText}`);
  }
  const json = await res.json();
  console.log(`  ok: commentId=${json.id}\n`);
  return json.id;
}

// ============================================================================
// Main
// ============================================================================

async function main() {
  const v = validateInputs();
  if (v.errors.length) {
    console.error('X Validation failed:');
    for (const e of v.errors) console.error('  - ' + e);
    process.exit(1);
  }

  // Resolve description (path or path#anchor)
  let description;
  try {
    description = await readContentRef(args['description-file']);
  } catch (err) {
    console.error('X --description-file: ' + err.message);
    process.exit(1);
  }
  if (description.length > 5000) {
    console.error(`X description is ${description.length} chars; YT limit is 5000.`);
    process.exit(1);
  }

  // Resolve comment (optional)
  let commentText = null;
  if (args['comment-file']) {
    try {
      commentText = await readContentRef(args['comment-file']);
    } catch (err) {
      console.error('X --comment-file: ' + err.message);
      process.exit(1);
    }
    if (commentText.length > 10000) {
      console.error(`X comment is ${commentText.length} chars; YT limit is 10000.`);
      process.exit(1);
    }
  }

  // Build the video resource
  const snippet = {
    title: args.title,
    description,
    categoryId: v.categoryId,
  };
  if (v.tagList.length) snippet.tags = v.tagList;

  const status = {
    privacyStatus: v.privacy,
    selfDeclaredMadeForKids: v.madeForKids,
  };
  if (v.publishAt) status.publishAt = v.publishAt;

  const metadata = { snippet, status };

  // Quota math
  const quotaUnits = 1600
    + (args.thumbnail ? 50 : 0)
    + (commentText ? 50 : 0);

  // Print plan
  console.log('=== Upload plan ===');
  console.log(`  File:        ${args.file}  (${(v.fileSize / 1024 / 1024).toFixed(2)}MB)`);
  console.log(`  Title:       ${args.title}  (${args.title.length}/100)`);
  console.log(`  Description: ${description.length}/5000 chars`);
  console.log(`  Tags:        ${v.tagList.length ? v.tagList.join(', ') : '(none)'}`);
  console.log(`  Category:    ${v.categoryId}`);
  console.log(`  Privacy:     ${v.privacy}${v.publishAt ? ` (publishAt=${v.publishAt})` : ''}`);
  console.log(`  Made-for-kids: ${v.madeForKids}`);
  console.log(`  Thumbnail:   ${args.thumbnail || '(none)'}`);
  console.log(`  Comment:     ${commentText ? `${commentText.length} chars` : '(none)'}`);
  console.log(`  Quota cost:  ~${quotaUnits} units`);
  console.log(`  Daily quota: 10,000 units (default) — this run uses ${(quotaUnits / 100).toFixed(1)}%`);
  console.log('');

  if (args['dry-run']) {
    console.log('=== DRY RUN — no API calls made ===');
    console.log('Resolved metadata payload:');
    console.log(JSON.stringify(metadata, null, 2));
    if (commentText) {
      console.log('\nResolved comment text:');
      console.log('---');
      console.log(commentText);
      console.log('---');
    }
    console.log('\nValidation: PASSED. Re-run without --dry-run to upload.');
    return;
  }

  // Real upload
  const env = await loadEnv();
  const accessToken = await getAccessToken(env);

  let result;
  try {
    result = await uploadVideo({
      accessToken,
      filePath: v.filePath,
      fileSize: v.fileSize,
      metadata,
    });
  } catch (err) {
    console.error('X Upload failed: ' + err.message);
    console.error('   No partial-state corruption — resumable session aborts cleanly.');
    process.exit(3);
  }

  const videoId = result.id;
  const url = `https://youtu.be/${videoId}`;
  const studio = `https://studio.youtube.com/video/${videoId}/edit`;

  let thumbnailDone = false;
  if (args.thumbnail) {
    const thumbPath = path.isAbsolute(args.thumbnail) ? args.thumbnail : path.join(ROOT, args.thumbnail);
    try {
      await setThumbnail({ accessToken, videoId, thumbPath });
      thumbnailDone = true;
    } catch (err) {
      console.error('! Thumbnail failed (video uploaded OK): ' + err.message);
    }
  }

  let commentId = null;
  if (commentText) {
    try {
      commentId = await postComment({ accessToken, videoId, commentText });
    } catch (err) {
      console.error('! Comment post failed (video uploaded OK): ' + err.message);
    }
  }

  // Success report
  console.log('=== Uploaded ===');
  console.log(`  Title:    ${args.title}`);
  console.log(`  Video ID: ${videoId}`);
  console.log(`  URL:      ${url}`);
  console.log(`  Studio:   ${studio}`);
  if (v.publishAt) {
    console.log(`  Schedule: ${v.publishAt}  (status: private until publishAt)`);
  } else {
    console.log(`  Privacy:  ${v.privacy}`);
  }
  if (args.thumbnail) {
    console.log(`  Thumbnail: ${thumbnailDone ? 'set' : 'FAILED — set manually in Studio'}`);
  }
  if (commentText) {
    if (commentId) {
      console.log(`  Comment:  posted (commentId=${commentId})`);
      console.log(`            MANUAL PIN required: ${studio.replace('/edit', '/comments')}`);
    } else {
      console.log(`  Comment:  FAILED — paste manually in Studio`);
    }
  }
  console.log(`  Quota used: ~${quotaUnits} units`);
}

await main();
