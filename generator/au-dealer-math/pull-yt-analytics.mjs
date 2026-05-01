// Daily AUDM YouTube analytics pull.
// Channel-level + per-video metrics. Output: content/au-dealer-math/analytics/.
//
// Usage: cd generator && npm run audm:yt:pull

import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, '..', '..');
const ENV_PATH = path.join(ROOT, '.env');
const OUT_DIR = path.join(ROOT, 'content', 'au-dealer-math', 'analytics');
const PER_VIDEO_DIR = path.join(OUT_DIR, 'videos');

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

const env = await loadEnv();
const { YT_CLIENT_ID, YT_CLIENT_SECRET, YT_REFRESH_TOKEN, YT_CHANNEL_ID } = env;
if (!YT_CLIENT_ID || !YT_CLIENT_SECRET || !YT_REFRESH_TOKEN || !YT_CHANNEL_ID) {
  console.error('X Missing YT credentials in .env. Run "npm run audm:yt:setup" first.');
  process.exit(1);
}

console.log('Refreshing access token...');
const tokenRes = await fetch('https://oauth2.googleapis.com/token', {
  method: 'POST',
  headers: { 'content-type': 'application/x-www-form-urlencoded' },
  body: new URLSearchParams({
    client_id: YT_CLIENT_ID,
    client_secret: YT_CLIENT_SECRET,
    refresh_token: YT_REFRESH_TOKEN,
    grant_type: 'refresh_token',
  }),
});
const tokenJson = await tokenRes.json();
if (!tokenJson.access_token) {
  console.error('X Auth failure refreshing token:', tokenJson);
  console.error('   STOP per analytics-pull rule. Re-run "npm run audm:yt:setup".');
  process.exit(2);
}
const accessToken = tokenJson.access_token;
const auth = { headers: { authorization: `Bearer ${accessToken}` } };
console.log('  ok\n');

const today = new Date().toISOString().slice(0, 10);
const ago30 = new Date(Date.now() - 30 * 86400_000).toISOString().slice(0, 10);
const ago7 = new Date(Date.now() - 7 * 86400_000).toISOString().slice(0, 10);

async function gj(url) {
  const res = await fetch(url, auth);
  const json = await res.json();
  if (json.error) throw new Error(`API: ${JSON.stringify(json.error)}`);
  return json;
}

console.log('Fetching channel stats (Data API)...');
const chanData = await gj(
  `https://www.googleapis.com/youtube/v3/channels?part=statistics,snippet,contentDetails&id=${YT_CHANNEL_ID}`,
);
const ch = chanData.items[0];
const subs = parseInt(ch.statistics.subscriberCount || '0', 10);
const totalViews = parseInt(ch.statistics.viewCount || '0', 10);
const videoCount = parseInt(ch.statistics.videoCount || '0', 10);
const uploadsPlaylist = ch.contentDetails.relatedPlaylists.uploads;
console.log(`  Subs: ${subs} · Views: ${totalViews} · Videos: ${videoCount}\n`);

console.log('Fetching upload list...');
const playlistData = await gj(
  `https://www.googleapis.com/youtube/v3/playlistItems?part=snippet,contentDetails&playlistId=${uploadsPlaylist}&maxResults=50`,
);
const videoIds = playlistData.items.map(i => i.contentDetails.videoId);
console.log(`  ok: ${videoIds.length} videos\n`);

console.log('Fetching per-video stats (Data API)...');
const videoStats = videoIds.length
  ? await gj(
      `https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails,status&id=${videoIds.join(',')}`,
    )
  : { items: [] };
const videos = videoStats.items.map(v => ({
  id: v.id,
  title: v.snippet.title,
  publishedAt: v.snippet.publishedAt,
  privacy: v.status.privacyStatus,
  duration: v.contentDetails.duration,
  views: parseInt(v.statistics.viewCount || '0', 10),
  likes: parseInt(v.statistics.likeCount || '0', 10),
  comments: parseInt(v.statistics.commentCount || '0', 10),
}));
videos.sort((a, b) => new Date(b.publishedAt) - new Date(a.publishedAt));
console.log(`  ok: ${videos.length} videos\n`);

console.log('Fetching channel-level analytics (Analytics API, last 30d)...');
const chanAnalyticsRes = await fetch(
  'https://youtubeanalytics.googleapis.com/v2/reports?'
    + new URLSearchParams({
      ids: `channel==${YT_CHANNEL_ID}`,
      startDate: ago30,
      endDate: today,
      metrics: 'views,estimatedMinutesWatched,averageViewDuration,subscribersGained,subscribersLost,likes,comments,shares',
      dimensions: '',
    }),
  auth,
);
const chanAnalyticsJson = await chanAnalyticsRes.json();
const chanRow = chanAnalyticsJson.rows?.[0] || [];
const chanCols = chanAnalyticsJson.columnHeaders || [];
const chanMetrics = Object.fromEntries(chanCols.map((c, i) => [c.name, chanRow[i] ?? 0]));
console.log('  ok\n');

console.log('Fetching channel-level traffic sources (last 30d)...');
const trafficRes = await fetch(
  'https://youtubeanalytics.googleapis.com/v2/reports?'
    + new URLSearchParams({
      ids: `channel==${YT_CHANNEL_ID}`,
      startDate: ago30,
      endDate: today,
      metrics: 'views',
      dimensions: 'insightTrafficSourceType',
      sort: '-views',
    }),
  auth,
);
const trafficJson = await trafficRes.json();
const trafficRows = trafficJson.rows || [];
console.log(`  ok: ${trafficRows.length} sources\n`);

console.log('Fetching per-video analytics (last 30d)...');
const perVideoAnalytics = {};
for (const v of videos) {
  if (v.privacy !== 'public') continue;
  const startDate = v.publishedAt.slice(0, 10);
  const vRes = await fetch(
    'https://youtubeanalytics.googleapis.com/v2/reports?'
      + new URLSearchParams({
        ids: `channel==${YT_CHANNEL_ID}`,
        startDate,
        endDate: today,
        metrics: 'views,estimatedMinutesWatched,averageViewDuration,averageViewPercentage,subscribersGained,likes,dislikes,comments,shares',
        filters: `video==${v.id}`,
      }),
    auth,
  );
  const vJson = await vRes.json();
  const row = vJson.rows?.[0] || [];
  const cols = vJson.columnHeaders || [];
  perVideoAnalytics[v.id] = Object.fromEntries(cols.map((c, i) => [c.name, row[i] ?? 0]));
}
console.log(`  ok: ${Object.keys(perVideoAnalytics).length} videos with analytics\n`);

await fs.mkdir(OUT_DIR, { recursive: true });
await fs.mkdir(PER_VIDEO_DIR, { recursive: true });

const channelSnapshot = {
  pulled_at: new Date().toISOString(),
  channelId: YT_CHANNEL_ID,
  subs,
  totalViews,
  videoCount,
  views30d: chanMetrics.views || 0,
  watchMinutes30d: chanMetrics.estimatedMinutesWatched || 0,
  avd30d: chanMetrics.averageViewDuration || 0,
  subsGained30d: chanMetrics.subscribersGained || 0,
  subsLost30d: chanMetrics.subscribersLost || 0,
  likes30d: chanMetrics.likes || 0,
  comments30d: chanMetrics.comments || 0,
  shares30d: chanMetrics.shares || 0,
  publicVideoCount: videos.filter(v => v.privacy === 'public').length,
};
await fs.appendFile(path.join(OUT_DIR, 'channel-snapshots.jsonl'), JSON.stringify(channelSnapshot) + '\n');

let md = `# AUDM YouTube Analytics — ${today}\n\n`;
md += `_Channel: ${ch.snippet.title} (${YT_CHANNEL_ID})_\n\n`;
md += `## Channel summary\n\n`;
md += `| Metric | Value |\n|---|---|\n`;
md += `| Subscribers (lifetime) | **${subs}** |\n`;
md += `| Total views (lifetime) | ${totalViews} |\n`;
md += `| Videos published | ${videoCount} |\n`;
md += `| Views (last 30d) | ${chanMetrics.views || 0} |\n`;
md += `| Watch time minutes (last 30d) | ${chanMetrics.estimatedMinutesWatched || 0} |\n`;
md += `| Avg view duration (last 30d) | ${chanMetrics.averageViewDuration || 0}s |\n`;
md += `| Subs gained (last 30d) | ${chanMetrics.subscribersGained || 0} |\n`;
md += `| Subs lost (last 30d) | ${chanMetrics.subscribersLost || 0} |\n`;
md += `| Likes (last 30d) | ${chanMetrics.likes || 0} |\n`;
md += `| Comments (last 30d) | ${chanMetrics.comments || 0} |\n`;
md += `| Shares (last 30d) | ${chanMetrics.shares || 0} |\n\n`;

md += `## Traffic sources (last 30d)\n\n`;
md += `| Source | Views |\n|---|---|\n`;
for (const [type, views] of trafficRows) {
  md += `| ${type} | ${views} |\n`;
}
md += `\n`;

md += `## Videos\n\n`;
md += `| Title | Status | Published | Views | AVD | AVD % | Subs+ | Likes | Comments |\n`;
md += `|---|---|---|---|---|---|---|---|---|\n`;
for (const v of videos) {
  const a = perVideoAnalytics[v.id] || {};
  md += `| ${v.title} | ${v.privacy} | ${v.publishedAt.slice(0, 10)} `
    + `| ${v.views} | ${a.averageViewDuration || 0}s | ${(a.averageViewPercentage || 0).toFixed?.(1) || a.averageViewPercentage || 0}% `
    + `| ${a.subscribersGained || 0} | ${v.likes} | ${v.comments} |\n`;
}
md += `\n`;

md += `## Quick health check (per analytics baselines)\n\n`;
md += `Targets per \`content/au-dealer-math/research/yt-analytics-baselines-2026-05-01.md\`:\n`;
md += `- Avg view duration ≥ **45%** (current: ${(chanMetrics.averageViewDuration || 0)}s — need video runtime to compute %)\n`;
md += `- CTR ≥ **4%** (Analytics API does not expose CTR at channel level — see YT Studio)\n`;
md += `- Return-viewer rate ≥ **10%** (requires audience tab)\n`;
md += `\n_Pulled at ${new Date().toISOString()}_\n`;

const outFile = path.join(OUT_DIR, `yt-${today}.md`);
await fs.writeFile(outFile, md);
console.log(`Wrote ${outFile}`);

for (const v of videos) {
  if (v.privacy !== 'public') continue;
  const a = perVideoAnalytics[v.id] || {};
  const slug = v.title.replace(/[^a-z0-9]+/gi, '-').slice(0, 60).toLowerCase().replace(/^-|-$/g, '');
  const file = path.join(PER_VIDEO_DIR, `${slug}-${v.id}.jsonl`);
  const snapshot = {
    pulledAt: new Date().toISOString(),
    daysSincePublish: Math.floor((Date.now() - new Date(v.publishedAt)) / 86400_000),
    views: v.views,
    likes: v.likes,
    comments: v.comments,
    avd_sec: a.averageViewDuration || 0,
    avd_pct: a.averageViewPercentage || 0,
    subsGained: a.subscribersGained || 0,
    watchMinutes: a.estimatedMinutesWatched || 0,
  };
  await fs.appendFile(file, JSON.stringify(snapshot) + '\n');
}
console.log(`Per-video snapshots appended.`);

console.log(`\n=== AUDM YouTube pull complete ===`);
console.log(`  Subs: ${subs} · 30d views: ${chanMetrics.views || 0} · Public videos: ${videos.filter(v => v.privacy === 'public').length}`);
