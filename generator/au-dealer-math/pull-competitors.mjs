// AUDM competitor outliers pull.
// Identifies videos that broke their channel's baseline — the swipe-file
// for "what's actually working in adjacent channels right now."
//
// Algorithm (Paddy Galloway / MrBeast-team methodology):
//   1. For each channel: median views/day across last 20 videos ≥7d old =
//      that channel's baseline. Computed separately for Shorts (≤60s) and
//      long-form (>60s) because they live on different surfaces.
//   2. Each video's outlier score = its views/day / channel-baseline-views/day.
//   3. Score ≥3.0 = breakout. ≥5.0 = major. ≥10.0 = viral.
//   4. Aggregate outliers across all channels, sort descending, write digest.
//
// Reuses existing YT_* OAuth credentials from .env (youtube.readonly scope is
// sufficient — all data accessed is public).
//
// Usage: cd generator && npm run audm:competitors:pull

import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, '..', '..');
const ENV_PATH = path.join(ROOT, '.env');
const RESEARCH_DIR = path.join(ROOT, 'content', 'au-dealer-math', 'research', 'competitors');
const CONFIG_PATH = path.join(RESEARCH_DIR, 'channels.json');
const SNAPSHOTS_DIR = path.join(RESEARCH_DIR, 'snapshots');
const DIGESTS_DIR = path.join(RESEARCH_DIR, 'digests');
const LIVE_DIGEST = path.join(RESEARCH_DIR, 'outliers-current.md');
const BASELINES_LOG = path.join(RESEARCH_DIR, 'baselines.jsonl');

// ---------- env + auth ----------

async function loadEnv() {
  const envText = await fs.readFile(ENV_PATH, 'utf8');
  return Object.fromEntries(
    envText.split('\n')
      .filter(line => line && !line.startsWith('#') && line.includes('='))
      .map(line => { const i = line.indexOf('='); return [line.slice(0,i).trim(), line.slice(i+1).trim()]; }),
  );
}

const env = await loadEnv();
const { YT_CLIENT_ID, YT_CLIENT_SECRET, YT_REFRESH_TOKEN } = env;
if (!YT_CLIENT_ID || !YT_CLIENT_SECRET || !YT_REFRESH_TOKEN) {
  console.error('X Missing YT credentials in .env. Run "npm run audm:yt:setup" first.');
  process.exit(1);
}

console.log('Refreshing access token...');
const tokenJson = await (await fetch('https://oauth2.googleapis.com/token', {
  method: 'POST',
  headers: { 'content-type': 'application/x-www-form-urlencoded' },
  body: new URLSearchParams({
    client_id: YT_CLIENT_ID,
    client_secret: YT_CLIENT_SECRET,
    refresh_token: YT_REFRESH_TOKEN,
    grant_type: 'refresh_token',
  }),
})).json();
if (!tokenJson.access_token) {
  console.error('X Auth failure refreshing token:', tokenJson);
  console.error('   STOP per analytics-pull rule. Re-run "npm run audm:yt:setup".');
  process.exit(2);
}
const accessToken = tokenJson.access_token;
const auth = { headers: { authorization: `Bearer ${accessToken}` } };
console.log('  ok\n');

// ---------- helpers ----------

async function gj(url, { allowError = false } = {}) {
  const res = await fetch(url, auth);
  const json = await res.json();
  if (json.error) {
    if (allowError) return { __error: json.error };
    throw new Error(`API: ${JSON.stringify(json.error)}`);
  }
  return json;
}

function parseDuration(iso) {
  // PT9M48S, PT31S, PT1H2M3S — live streams/premieres can be null/empty
  if (!iso) return 0;
  const m = iso.match(/PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?/) || [];
  return (parseInt(m[1]||0)*3600) + (parseInt(m[2]||0)*60) + parseInt(m[3]||0);
}

function median(nums) {
  if (!nums.length) return 0;
  const sorted = [...nums].sort((a,b)=>a-b);
  const mid = Math.floor(sorted.length/2);
  return sorted.length % 2 ? sorted[mid] : (sorted[mid-1] + sorted[mid]) / 2;
}

function daysAgo(isoDate) {
  return (Date.now() - new Date(isoDate)) / 86400_000;
}

async function hydrateChannelId(channelId) {
  const r = await gj(
    `https://www.googleapis.com/youtube/v3/channels?part=id,snippet,statistics,contentDetails&id=${channelId}`,
    { allowError: true },
  );
  return r.items?.[0] || null;
}

function channelSize(ch) {
  if (!ch) return 0;
  const subs = parseInt(ch.statistics?.subscriberCount || '0', 10);
  const hidden = ch.statistics?.hiddenSubscriberCount === true;
  if (hidden) return parseInt(ch.statistics?.viewCount || '0', 10) / 100;
  return subs;
}

async function resolveChannel(cfg) {
  // 1. Direct channelId override (always wins — for ambiguous-handle channels)
  if (cfg.channelId) return await hydrateChannelId(cfg.channelId);

  const handle = cfg.handle || '';
  const stripped = handle.replace(/^@/, '');
  if (!stripped) return null;

  // 2. forHandle lookup (cheap, 1 unit)
  const fh = await gj(
    `https://www.googleapis.com/youtube/v3/channels?part=id,snippet,statistics,contentDetails&forHandle=@${stripped}`,
    { allowError: true },
  );
  const fhResult = (!fh.__error && fh.items?.[0]) ? fh.items[0] : null;

  // If forHandle returned a healthy-sized channel, accept.
  if (fhResult && channelSize(fhResult) >= 10_000) return fhResult;

  // 3. Search fallback (100 units) — handles wrong-channel collisions and missing handles.
  // Pull top 5 results and pick the largest.
  const search = await gj(
    `https://www.googleapis.com/youtube/v3/search?part=snippet&q=${encodeURIComponent(handle)}&type=channel&maxResults=5`,
    { allowError: true },
  );
  if (search.__error || !search.items?.length) return fhResult; // fall back to forHandle result if search failed

  const candidateIds = search.items.map(i => i.snippet.channelId).join(',');
  const hydrated = await gj(
    `https://www.googleapis.com/youtube/v3/channels?part=id,snippet,statistics,contentDetails&id=${candidateIds}`,
    { allowError: true },
  );
  if (hydrated.__error || !hydrated.items?.length) return fhResult;

  const allCandidates = [fhResult, ...hydrated.items].filter(Boolean);
  allCandidates.sort((a, b) => channelSize(b) - channelSize(a));
  return allCandidates[0] || null;
}

// ---------- main pull ----------

const config = JSON.parse(await fs.readFile(CONFIG_PATH, 'utf8'));
const LOOKBACK_DAYS = config.lookback_days ?? 90;
const MIN_OUTLIER = config.min_outlier_score ?? 3.0;
const MIN_SUBS = config.min_subs ?? 1000;
const BASELINE_MIN_AGE = config.baseline_min_video_age_days ?? 7;
const BASELINE_WINDOW = config.baseline_window ?? 20;

console.log(`Pulling ${config.channels.length} channels (lookback ${LOOKBACK_DAYS}d, baseline window ${BASELINE_WINDOW}, min outlier ${MIN_OUTLIER}×)\n`);

const allOutliers = [];
const channelSummaries = [];
const baselineLogEntries = [];
const today = new Date().toISOString().slice(0, 10);
const todayMs = Date.now();

for (const cfg of config.channels) {
  const label = (cfg.handle || cfg.channelId || '?').padEnd(28);
  process.stdout.write(`  ${label} `);
  let ch;
  try {
    ch = await resolveChannel(cfg);
  } catch (e) {
    console.log(`X resolve failed: ${e.message.slice(0, 60)}`);
    continue;
  }
  if (!ch) { console.log('X did not resolve'); continue; }

  const subs = parseInt(ch.statistics.subscriberCount || '0', 10);
  const subsHidden = ch.statistics.hiddenSubscriberCount === true;
  const totalViews = parseInt(ch.statistics.viewCount || '0', 10);
  // YT lets channels hide sub counts, returning 0. Don't filter those out — fall back
  // to lifetime view count as a scale proxy (10k views ≈ ~1k subs floor for active channels).
  if (!subsHidden && subs < MIN_SUBS && totalViews < 10_000) {
    console.log(`- skip (${subs} subs / ${totalViews} views below scale floor)`); continue;
  }

  const uploadsPlaylist = ch.contentDetails.relatedPlaylists.uploads;

  // Page through uploads playlist for last 50 videos (1 page).
  const pl = await gj(
    `https://www.googleapis.com/youtube/v3/playlistItems?part=contentDetails,snippet&playlistId=${uploadsPlaylist}&maxResults=50`,
    { allowError: true },
  );
  if (pl.__error || !pl.items?.length) { console.log(`X playlist fetch failed`); continue; }

  // Filter to lookback window
  const candidateIds = pl.items
    .filter(i => daysAgo(i.contentDetails.videoPublishedAt || i.snippet.publishedAt) <= LOOKBACK_DAYS)
    .map(i => i.contentDetails.videoId);
  if (!candidateIds.length) { console.log(`- no videos in last ${LOOKBACK_DAYS}d`); continue; }

  // Batch video stats (1 unit per call, up to 50 IDs per call)
  const stats = await gj(
    `https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&id=${candidateIds.join(',')}`,
    { allowError: true },
  );
  if (stats.__error || !stats.items?.length) { console.log(`X video stats failed`); continue; }

  const videos = stats.items.map(v => {
    const seconds = parseDuration(v.contentDetails.duration);
    const ageDays = daysAgo(v.snippet.publishedAt);
    const views = parseInt(v.statistics.viewCount || '0', 10);
    return {
      id: v.id,
      title: v.snippet.title,
      publishedAt: v.snippet.publishedAt,
      ageDays,
      seconds,
      isShort: seconds > 0 && seconds <= 60,
      views,
      viewsPerDay: ageDays > 0 ? views / ageDays : views,
      likes: parseInt(v.statistics.likeCount || '0', 10),
      comments: parseInt(v.statistics.commentCount || '0', 10),
      thumbnail: v.snippet.thumbnails?.medium?.url || v.snippet.thumbnails?.default?.url,
    };
  });

  // Compute baselines per format (videos must be ≥BASELINE_MIN_AGE days old)
  const longForms = videos.filter(v => !v.isShort && v.ageDays >= BASELINE_MIN_AGE);
  const shorts = videos.filter(v => v.isShort && v.ageDays >= BASELINE_MIN_AGE);
  const longBaseline = median(longForms.slice(0, BASELINE_WINDOW).map(v => v.viewsPerDay));
  const shortBaseline = median(shorts.slice(0, BASELINE_WINDOW).map(v => v.viewsPerDay));

  // Score each video
  const scored = videos.map(v => {
    const baseline = v.isShort ? shortBaseline : longBaseline;
    const score = baseline > 0 ? v.viewsPerDay / baseline : 0;
    return { ...v, baseline, score, channel: ch.snippet.title, channelId: ch.id, category: cfg.category };
  });
  const outliers = scored.filter(v => v.score >= MIN_OUTLIER);
  allOutliers.push(...outliers);

  channelSummaries.push({
    handle: cfg.handle,
    title: ch.snippet.title,
    category: cfg.category,
    subs,
    subsHidden,
    totalViews,
    videoCount: videos.length,
    longBaseline: Math.round(longBaseline),
    shortBaseline: Math.round(shortBaseline),
    outlierCount: outliers.length,
  });

  baselineLogEntries.push({
    pulledAt: new Date().toISOString(),
    handle: cfg.handle,
    channelId: ch.id,
    subs,
    longBaselineVPD: Math.round(longBaseline),
    shortBaselineVPD: Math.round(shortBaseline),
    longCount: longForms.length,
    shortCount: shorts.length,
  });

  console.log(`ok ${subs.toString().padStart(8)} subs · ${videos.length.toString().padStart(2)} vids · ${outliers.length} outliers`);
}

allOutliers.sort((a, b) => b.score - a.score);

// ---------- pattern stats across outliers ----------

function tokenize(str) {
  return str.toLowerCase().replace(/[^a-z0-9 ]/g, ' ').split(/\s+/).filter(w => w.length >= 3);
}
const STOPWORDS = new Set(['the','and','for','this','that','you','your','with','from','are','have','was','will','what','why','how','when','where','who','their','they','them','our','its','dont','should','could','would','can','can','not','one','two','out','about','into','more','than','very','just','like','get','got','let','also','make','use','top','best','only']);

function topNgrams(strs, n, limit = 10) {
  const counts = new Map();
  for (const s of strs) {
    const tokens = tokenize(s).filter(t => !STOPWORDS.has(t));
    for (let i = 0; i + n <= tokens.length; i++) {
      const gram = tokens.slice(i, i + n).join(' ');
      counts.set(gram, (counts.get(gram) || 0) + 1);
    }
  }
  return [...counts.entries()]
    .filter(([, c]) => c >= 2)
    .sort((a, b) => b[1] - a[1])
    .slice(0, limit);
}

const outlierTitles = allOutliers.map(o => o.title);
const topUnigrams = topNgrams(outlierTitles, 1, 12);
const topBigrams = topNgrams(outlierTitles, 2, 10);
const longOutliers = allOutliers.filter(o => !o.isShort);
const shortOutliers = allOutliers.filter(o => o.isShort);

const titleHasNumber = allOutliers.filter(o => /\b\d/.test(o.title)).length;
const titleHasYou = allOutliers.filter(o => /\b(you|your|you'?re|you'?ll)\b/i.test(o.title)).length;
const titleHasQuestion = allOutliers.filter(o => o.title.includes('?')).length;

// ---------- write outputs ----------

await fs.mkdir(SNAPSHOTS_DIR, { recursive: true });
await fs.mkdir(DIGESTS_DIR, { recursive: true });

const snapshot = {
  pulledAt: new Date().toISOString(),
  config: { LOOKBACK_DAYS, MIN_OUTLIER, MIN_SUBS, BASELINE_MIN_AGE, BASELINE_WINDOW },
  channels: channelSummaries,
  outliers: allOutliers,
};
const snapshotPath = path.join(SNAPSHOTS_DIR, `snapshot-${today}.json`);
await fs.writeFile(snapshotPath, JSON.stringify(snapshot, null, 2));

for (const e of baselineLogEntries) {
  await fs.appendFile(BASELINES_LOG, JSON.stringify(e) + '\n');
}

// ---------- digest ----------

function fmtScore(s) { return s.toFixed(1) + '×'; }
function fmtViews(n) {
  if (n >= 1_000_000) return (n / 1_000_000).toFixed(1) + 'M';
  if (n >= 1_000) return (n / 1_000).toFixed(1) + 'K';
  return String(n);
}
function fmtDuration(seconds) {
  if (seconds < 60) return seconds + 's';
  const m = Math.floor(seconds / 60), s = seconds % 60;
  return `${m}:${s.toString().padStart(2,'0')}`;
}

function renderOutlier(o, rank) {
  const fmt = o.isShort ? 'Short' : 'Long';
  const ageStr = o.ageDays < 1 ? `${Math.round(o.ageDays * 24)}h ago` : `${Math.round(o.ageDays)}d ago`;
  const engagement = o.views > 0 ? `${(o.likes / o.views * 100).toFixed(2)}% likes · ${o.comments} comments` : 'no engagement data';
  return `### ${rank}. **${o.title}**
- **Channel:** ${o.channel} (${o.category})
- **Outlier score:** ${fmtScore(o.score)} (${fmtViews(o.views)} views vs channel baseline ${fmtViews(Math.round(o.baseline))} views/day)
- **Format:** ${fmt} · ${fmtDuration(o.seconds)}
- **Published:** ${o.publishedAt.slice(0,10)} (${ageStr})
- **Engagement:** ${engagement}
- **URL:** https://www.youtube.com/${o.isShort ? 'shorts/' : 'watch?v='}${o.id}
- **Thumbnail:** ${o.thumbnail || '_n/a_'}
`;
}

const viralOutliers = allOutliers.filter(o => o.score >= 10);
const majorOutliers = allOutliers.filter(o => o.score >= 5 && o.score < 10);
const breakoutOutliers = allOutliers.filter(o => o.score >= 3 && o.score < 5);

let md = `# AUDM Competitor Outliers — ${today}\n\n`;
md += `_Pulled at ${new Date().toISOString()}_\n\n`;
md += `**Scope:** ${channelSummaries.length} channels · last ${LOOKBACK_DAYS} days · min outlier score ${MIN_OUTLIER}×\n\n`;
md += `**Outliers found:** ${allOutliers.length} total — ${viralOutliers.length} viral (≥10×) · ${majorOutliers.length} major (5-10×) · ${breakoutOutliers.length} breakout (3-5×)\n\n`;
md += `**Total videos analyzed:** ${channelSummaries.reduce((s, c) => s + c.videoCount, 0)}\n\n`;

md += `---\n\n## How to read this\n\n`;
md += `An "outlier" is a video that broke its channel's baseline — i.e. the YT algorithm picked it out and pushed it harder than the channel's typical video. The score is **views-per-day relative to the channel's median**, so a 5× outlier means 5× more views/day than that channel normally gets. This corrects for channel size: a 5× outlier on a 1K-baseline channel and a 5× outlier on a 1M-baseline channel both signal the *same* thing — the algo broke containment.\n\n`;
md += `**Why study these:** they're the videos doing in 2026 what we want AUDM doing in 2026-2027. Decode title / thumbnail / hook / format / topic. Borrow the pattern, don't copy the content.\n\n`;
md += `---\n\n`;

if (viralOutliers.length) {
  md += `## VIRAL (≥10× baseline) — mandatory study\n\n`;
  viralOutliers.forEach((o, i) => { md += renderOutlier(o, i + 1) + '\n'; });
}

if (majorOutliers.length) {
  md += `## MAJOR breakouts (5-10× baseline) — priority study\n\n`;
  majorOutliers.forEach((o, i) => { md += renderOutlier(o, i + 1) + '\n'; });
}

if (breakoutOutliers.length) {
  md += `## Breakouts (3-5× baseline)\n\n`;
  breakoutOutliers.forEach((o, i) => { md += renderOutlier(o, i + 1) + '\n'; });
}

if (!allOutliers.length) {
  md += `## No outliers this pull\n\nAll tracked channels are running close to baseline. Either the niche is quiet right now, or our threshold is too high (currently ${MIN_OUTLIER}×). Lower in channels.json if needed.\n\n`;
}

// Pattern stats
md += `---\n\n## Patterns observed across the ${allOutliers.length} outliers\n\n`;
md += `| Pattern | Count | % of outliers |\n|---|---|---|\n`;
if (allOutliers.length) {
  md += `| Title contains a number | ${titleHasNumber} | ${(titleHasNumber/allOutliers.length*100).toFixed(0)}% |\n`;
  md += `| Title uses "you" / "your" | ${titleHasYou} | ${(titleHasYou/allOutliers.length*100).toFixed(0)}% |\n`;
  md += `| Title is a question | ${titleHasQuestion} | ${(titleHasQuestion/allOutliers.length*100).toFixed(0)}% |\n`;
  md += `| Long-form outliers | ${longOutliers.length} | ${(longOutliers.length/allOutliers.length*100).toFixed(0)}% |\n`;
  md += `| Short-form outliers | ${shortOutliers.length} | ${(shortOutliers.length/allOutliers.length*100).toFixed(0)}% |\n\n`;
}

if (topUnigrams.length) {
  md += `### Most common words in outlier titles\n\n`;
  for (const [w, c] of topUnigrams) md += `- **${w}** (${c})\n`;
  md += `\n`;
}
if (topBigrams.length) {
  md += `### Most common 2-word phrases in outlier titles\n\n`;
  for (const [p, c] of topBigrams) md += `- **${p}** (${c})\n`;
  md += `\n`;
}

// Channel summary table
md += `---\n\n## Channel-level snapshot\n\n`;
md += `| Channel | Category | Subs | Lifetime views | Vids in window | Long baseline (v/d) | Short baseline (v/d) | Outliers |\n|---|---|---|---|---|---|---|---|\n`;
const chSorted = [...channelSummaries].sort((a, b) => b.outlierCount - a.outlierCount);
for (const c of chSorted) {
  const subsCell = c.subsHidden ? 'hidden' : fmtViews(c.subs);
  md += `| ${c.title} | ${c.category} | ${subsCell} | ${fmtViews(c.totalViews)} | ${c.videoCount} | ${fmtViews(c.longBaseline)} | ${fmtViews(c.shortBaseline)} | ${c.outlierCount} |\n`;
}

md += `\n---\n\n_Snapshot: ${path.relative(ROOT, snapshotPath)}_\n`;
md += `_Config: ${path.relative(ROOT, CONFIG_PATH)} (edit channels[] to add/remove)_\n`;

const digestPath = path.join(DIGESTS_DIR, `digest-${today}.md`);
await fs.writeFile(digestPath, md);
await fs.writeFile(LIVE_DIGEST, md);

console.log(`\nWrote ${path.relative(ROOT, digestPath)}`);
console.log(`Wrote ${path.relative(ROOT, LIVE_DIGEST)} (live pointer)`);
console.log(`\n=== Competitor outliers pull complete ===`);
console.log(`  Channels: ${channelSummaries.length}/${config.channels.length} resolved`);
console.log(`  Outliers: ${allOutliers.length} (${viralOutliers.length} viral · ${majorOutliers.length} major · ${breakoutOutliers.length} breakout)`);
