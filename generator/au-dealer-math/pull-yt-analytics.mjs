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

// ---------- Helper: query YouTube Analytics with normalized output ----------
async function ytaQuery(params) {
  const res = await fetch(
    'https://youtubeanalytics.googleapis.com/v2/reports?'
      + new URLSearchParams({ ids: `channel==${YT_CHANNEL_ID}`, ...params }),
    auth,
  );
  const j = await res.json();
  if (j.error) {
    return { ok: false, error: j.error.message, rows: [], cols: [] };
  }
  return {
    ok: true,
    cols: (j.columnHeaders || []).map(c => c.name),
    rows: j.rows || [],
  };
}

console.log('Fetching per-video analytics (last 30d)...');
const perVideoAnalytics = {};
for (const v of videos) {
  if (v.privacy !== 'public') continue;
  const startDate = v.publishedAt.slice(0, 10);
  const r = await ytaQuery({
    startDate, endDate: today,
    metrics: 'views,estimatedMinutesWatched,averageViewDuration,averageViewPercentage,subscribersGained,subscribersLost,likes,comments,shares',
    filters: `video==${v.id}`,
  });
  const row = r.rows[0] || [];
  perVideoAnalytics[v.id] = Object.fromEntries(r.cols.map((c, i) => [c.name, row[i] ?? 0]));
}
console.log(`  ok: ${Object.keys(perVideoAnalytics).length} videos with analytics\n`);

console.log('Fetching device-type breakdown (last 30d)...');
const deviceData = await ytaQuery({
  startDate: ago30, endDate: today,
  metrics: 'views,estimatedMinutesWatched,averageViewDuration',
  dimensions: 'deviceType', sort: '-views',
});
console.log(`  ok: ${deviceData.rows.length} device types\n`);

console.log('Fetching operating system breakdown (last 30d)...');
const osData = await ytaQuery({
  startDate: ago30, endDate: today,
  metrics: 'views,estimatedMinutesWatched',
  dimensions: 'operatingSystem', sort: '-views',
});
console.log(`  ok: ${osData.rows.length} OS\n`);

console.log('Fetching playback location breakdown (last 30d)...');
const playbackData = await ytaQuery({
  startDate: ago30, endDate: today,
  metrics: 'views,estimatedMinutesWatched',
  dimensions: 'insightPlaybackLocationType', sort: '-views',
});
console.log(`  ok: ${playbackData.rows.length} locations\n`);

console.log('Fetching subscribed-vs-not breakdown (last 30d)...');
const subStatusData = await ytaQuery({
  startDate: ago30, endDate: today,
  metrics: 'views,averageViewDuration,estimatedMinutesWatched',
  dimensions: 'subscribedStatus',
});
console.log(`  ok: ${subStatusData.rows.length} statuses\n`);

console.log('Fetching daily timeseries (last 30d)...');
const dailyData = await ytaQuery({
  startDate: ago30, endDate: today,
  metrics: 'views,estimatedMinutesWatched,subscribersGained,subscribersLost,likes,comments,shares',
  dimensions: 'day', sort: 'day',
});
console.log(`  ok: ${dailyData.rows.length} days\n`);

console.log('Fetching demographics (last 30d, may be empty <100 viewers)...');
const demoData = await ytaQuery({
  startDate: ago30, endDate: today,
  metrics: 'viewerPercentage',
  dimensions: 'ageGroup,gender', sort: '-viewerPercentage',
});
console.log(`  ok: ${demoData.rows.length} demo cells\n`);

console.log('Fetching country breakdown (last 30d, may be empty)...');
const countryData = await ytaQuery({
  startDate: ago30, endDate: today,
  metrics: 'views,estimatedMinutesWatched',
  dimensions: 'country', sort: '-views', maxResults: '15',
});
console.log(`  ok: ${countryData.rows.length} countries\n`);

console.log('Fetching sharing-service breakdown (last 30d)...');
const sharingData = await ytaQuery({
  startDate: ago30, endDate: today,
  metrics: 'shares',
  dimensions: 'sharingService', sort: '-shares',
});
console.log(`  ok: ${sharingData.rows.length} services\n`);

console.log('Fetching card metrics (last 30d, channel-level)...');
const cardData = await ytaQuery({
  startDate: ago30, endDate: today,
  metrics: 'cardImpressions,cardClicks,cardClickRate,cardTeaserImpressions,cardTeaserClicks',
});
console.log(`  ok\n`);

// Per-video deep-dive: traffic sources + retention curve + subscribed split + device split
console.log('Fetching per-video deep-dive data (traffic / retention / device)...');
const perVideoDeepDive = {};
for (const v of videos) {
  if (v.privacy !== 'public') continue;
  const startDate = v.publishedAt.slice(0, 10);
  const dive = {};

  dive.traffic = await ytaQuery({
    startDate, endDate: today, metrics: 'views,estimatedMinutesWatched',
    dimensions: 'insightTrafficSourceType', sort: '-views',
    filters: `video==${v.id}`,
  });

  dive.devices = await ytaQuery({
    startDate, endDate: today, metrics: 'views,estimatedMinutesWatched',
    dimensions: 'deviceType', sort: '-views',
    filters: `video==${v.id}`,
  });

  dive.subStatus = await ytaQuery({
    startDate, endDate: today, metrics: 'views,averageViewDuration',
    dimensions: 'subscribedStatus',
    filters: `video==${v.id}`,
  });

  dive.retention = await ytaQuery({
    startDate, endDate: today,
    metrics: 'audienceWatchRatio,relativeRetentionPerformance',
    dimensions: 'elapsedVideoTimeRatio',
    filters: `video==${v.id}`,
  });

  dive.daily = await ytaQuery({
    startDate, endDate: today,
    metrics: 'views,estimatedMinutesWatched,averageViewDuration,subscribersGained,likes,comments,shares',
    dimensions: 'day', sort: 'day',
    filters: `video==${v.id}`,
  });

  perVideoDeepDive[v.id] = dive;
}
console.log(`  ok: deep-dive for ${Object.keys(perVideoDeepDive).length} public videos\n`);

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

// YouTube Analytics API has a ~72h lag — videos newer than ~3 days return 0/null
// for views/watch-minutes/AVD/AVP. Data API (v.views, v.likes, v.comments) IS real-time.
// We display lagged metrics as "—" with a daysSincePublish indicator + footnote.
function laggedSecs(apiAvd, apiMinutes, dataApiViews, daysOld) {
  if (apiAvd > 0) return `${apiAvd}s`;
  if (apiMinutes > 0 && dataApiViews > 0) {
    return `${Math.round((apiMinutes * 60) / dataApiViews)}s`;
  }
  return daysOld < 3 ? '— †' : '0s';
}
function laggedPct(apiAvp, daysOld) {
  if (apiAvp > 0) return `${apiAvp.toFixed(1)}%`;
  return daysOld < 3 ? '— †' : '0%';
}
function laggedNum(val, daysOld) {
  if (val > 0) return String(val);
  return daysOld < 3 ? '— †' : '0';
}

const laggedVideos = videos.filter(v => {
  if (v.privacy !== 'public') return false;
  const a = perVideoAnalytics[v.id] || {};
  const daysOld = (Date.now() - new Date(v.publishedAt)) / 86400_000;
  return daysOld < 3 && (a.averageViewDuration || 0) === 0;
});

md += `## Videos\n\n`;
md += `| Title | Status | Published | Days | Views | AVD | AVD % | Subs+ | Likes | Comments |\n`;
md += `|---|---|---|---|---|---|---|---|---|---|\n`;
for (const v of videos) {
  const a = perVideoAnalytics[v.id] || {};
  const daysOld = (Date.now() - new Date(v.publishedAt)) / 86400_000;
  const daysStr = daysOld < 1 ? `${(daysOld * 24).toFixed(1)}h` : `${daysOld.toFixed(1)}d`;
  const isPublic = v.privacy === 'public';

  if (!isPublic) {
    // Private/unlisted — don't pretend we have analytics
    md += `| ${v.title} | ${v.privacy} | ${v.publishedAt.slice(0, 10)} | ${daysStr} `
      + `| ${v.views} | n/a | n/a | n/a | ${v.likes} | ${v.comments} |\n`;
    continue;
  }

  md += `| ${v.title} | ${v.privacy} | ${v.publishedAt.slice(0, 10)} | ${daysStr} `
    + `| ${v.views} | ${laggedSecs(a.averageViewDuration, a.estimatedMinutesWatched, v.views, daysOld)} `
    + `| ${laggedPct(a.averageViewPercentage, daysOld)} `
    + `| ${laggedNum(a.subscribersGained, daysOld)} | ${v.likes} | ${v.comments} |\n`;
}
md += `\n`;

if (laggedVideos.length > 0) {
  md += `> **† YouTube Analytics API data lag.** Videos under ~72h old return `
    + `\`0\`/null for views, watch-minutes, AVD, and AVP via the public API even though `
    + `Studio shows real numbers. This is a hard API constraint — Studio uses YouTube's `
    + `internal real-time aggregation that no public endpoint exposes. **For per-video AVD `
    + `on uploads <3d old, YouTube Studio (browser) is the source of truth.** Lifetime view `
    + `counts shown above ARE real-time (pulled from Data API, not Analytics API).\n\n`;
  md += `> **Currently lagged (${laggedVideos.length} video${laggedVideos.length === 1 ? '' : 's'}):** `
    + laggedVideos.map(v => `*${v.title.slice(0, 40)}*`).join(', ')
    + `. Data should populate ~${Math.ceil(3 - Math.max(...laggedVideos.map(v => (Date.now() - new Date(v.publishedAt)) / 86400_000)))}d from now.\n\n`;
}

// ============================================================
//  AUDIENCE BREAKDOWN — device / OS / playback / subscribed
// ============================================================
md += `## Audience breakdown (last 30d)\n\n`;

if (deviceData.rows.length > 0) {
  md += `### Device type\n\n`;
  md += `| Device | Views | Watch min | Avg watch (s) |\n|---|---|---|---|\n`;
  for (const r of deviceData.rows) {
    const [device, views, mins, avd] = r;
    md += `| ${device} | ${views} | ${mins} | ${avd || '—'} |\n`;
  }
  md += `\n`;
}

if (osData.rows.length > 0) {
  md += `### Operating system\n\n`;
  md += `| OS | Views | Watch min |\n|---|---|---|\n`;
  for (const r of osData.rows.slice(0, 10)) {
    md += `| ${r[0]} | ${r[1]} | ${r[2] || 0} |\n`;
  }
  md += `\n`;
}

if (playbackData.rows.length > 0) {
  md += `### Playback location\n\n`;
  md += `| Location | Views | Watch min |\n|---|---|---|\n`;
  for (const r of playbackData.rows) {
    md += `| ${r[0]} | ${r[1]} | ${r[2] || 0} |\n`;
  }
  md += `\n`;
}

if (subStatusData.rows.length > 0) {
  md += `### Subscribed vs not subscribed\n\n`;
  md += `| Status | Views | Avg watch (s) | Watch min |\n|---|---|---|---|\n`;
  for (const r of subStatusData.rows) {
    md += `| ${r[0]} | ${r[1]} | ${r[2] || 0} | ${r[3] || 0} |\n`;
  }
  md += `\n_If SUBSCRIBED viewers retain longer than UNSUBSCRIBED → channel-trust effect kicking in. Below 1K subs this row is usually thin._\n\n`;
}

if (countryData.rows.length > 0) {
  md += `### Country (top 15 by views)\n\n`;
  md += `| Country | Views | Watch min |\n|---|---|---|\n`;
  for (const r of countryData.rows) {
    md += `| ${r[0]} | ${r[1]} | ${r[2] || 0} |\n`;
  }
  md += `\n_AU should dominate. Spillover to US/UK is common and normal for AU finance content._\n\n`;
}

if (demoData.rows.length > 0) {
  md += `### Demographics (age × gender)\n\n`;
  md += `| Age | Gender | % of viewers |\n|---|---|---|\n`;
  for (const r of demoData.rows) {
    md += `| ${r[0]} | ${r[1]} | ${(r[2] || 0).toFixed(1)}% |\n`;
  }
  md += `\n`;
} else {
  md += `> _Demographics data is gated by YouTube — typically requires ~100+ unique viewers within a 30d window before populating. Check back when channel hits ~100 subs._\n\n`;
}

if (sharingData.rows.length > 0) {
  md += `### Sharing service\n\n`;
  md += `| Service | Shares |\n|---|---|\n`;
  for (const r of sharingData.rows) md += `| ${r[0]} | ${r[1]} |\n`;
  md += `\n`;
}

// ============================================================
//  DAILY TIMESERIES — last 30d
// ============================================================
if (dailyData.rows.length > 0) {
  md += `## Daily timeseries (last 30d)\n\n`;
  md += `| Day | Views | Watch min | Subs+ | Subs- | Likes | Comments | Shares |\n`;
  md += `|---|---|---|---|---|---|---|---|\n`;
  for (const r of dailyData.rows) {
    md += `| ${r[0]} | ${r[1]} | ${r[2]} | ${r[3]} | ${r[4]} | ${r[5]} | ${r[6]} | ${r[7]} |\n`;
  }
  md += `\n`;
}

// ============================================================
//  CARD METRICS — channel level
// ============================================================
if (cardData.ok && cardData.rows.length > 0) {
  const [cardImpr, cardClicks, cardCtr, teaserImpr, teaserClicks] = cardData.rows[0];
  md += `## Card metrics (last 30d, channel-level)\n\n`;
  md += `| Metric | Value |\n|---|---|\n`;
  md += `| Card impressions | ${cardImpr} |\n`;
  md += `| Card clicks | ${cardClicks} |\n`;
  md += `| Card click rate | ${((cardCtr || 0) * 100).toFixed(2)}% |\n`;
  md += `| Teaser impressions | ${teaserImpr} |\n`;
  md += `| Teaser clicks | ${teaserClicks} |\n\n`;
  if ((cardImpr || 0) === 0) md += `> _No cards added yet. Adding 2-3 cards per long-form (linking to next video) typically lifts session-time by 15-30%. Channel-level Studio → Editor → Cards._\n\n`;
}

// ============================================================
//  PER-VIDEO DEEP DIVE — traffic sources / retention curve drop-off / device split
// ============================================================
md += `## Per-video deep dive\n\n`;
md += `_Public videos only. Retention curves populate ~72h after publish. Per-video markdown files written to \`content/au-dealer-math/analytics/videos/*.md\`._\n\n`;

const publicVideos = videos.filter(v => v.privacy === 'public');
for (const v of publicVideos) {
  const dive = perVideoDeepDive[v.id] || {};
  const a = perVideoAnalytics[v.id] || {};
  const daysOld = (Date.now() - new Date(v.publishedAt)) / 86400_000;

  md += `### ${v.title}\n\n`;
  md += `- Published: ${v.publishedAt.slice(0, 10)} (${daysOld < 1 ? `${(daysOld * 24).toFixed(1)}h` : `${daysOld.toFixed(1)}d`} old)\n`;
  md += `- Views (lifetime, real-time): **${v.views}** · Likes: ${v.likes} · Comments: ${v.comments}\n`;
  md += `- AVD: ${laggedSecs(a.averageViewDuration, a.estimatedMinutesWatched, v.views, daysOld)} (${laggedPct(a.averageViewPercentage, daysOld)}) · Subs+: ${laggedNum(a.subscribersGained, daysOld)}\n`;
  md += `- URL: https://youtube.com/watch?v=${v.id}\n\n`;

  if ((dive.traffic?.rows || []).length > 0) {
    md += `**Traffic sources:**\n\n`;
    md += `| Source | Views | Watch min |\n|---|---|---|\n`;
    for (const r of dive.traffic.rows) md += `| ${r[0]} | ${r[1]} | ${r[2] || 0} |\n`;
    md += `\n`;
  }

  if ((dive.devices?.rows || []).length > 0) {
    md += `**Device split:**\n\n`;
    md += `| Device | Views | Watch min |\n|---|---|---|\n`;
    for (const r of dive.devices.rows) md += `| ${r[0]} | ${r[1]} | ${r[2] || 0} |\n`;
    md += `\n`;
  }

  if ((dive.subStatus?.rows || []).length > 0) {
    md += `**Subscribed split:**\n\n`;
    md += `| Status | Views | Avg watch (s) |\n|---|---|---|\n`;
    for (const r of dive.subStatus.rows) md += `| ${r[0]} | ${r[1]} | ${r[2] || 0} |\n`;
    md += `\n`;
  }

  // Retention curve — the gold metric for "where did viewers drop off"
  if ((dive.retention?.rows || []).length > 0) {
    md += `**Retention curve** (audienceWatchRatio per 1% chunk of video):\n\n`;
    md += `| Elapsed % | Watch ratio | Relative perf |\n|---|---|---|\n`;
    // Show every 5% bucket for readability + flag drops
    const rows = dive.retention.rows;
    const samples = rows.filter((_, i) => i % 5 === 0 || i === rows.length - 1);
    for (const r of samples) {
      const pct = (r[0] * 100).toFixed(0);
      const watch = (r[1] * 100).toFixed(1);
      const rel = (r[2] || 0).toFixed(2);
      md += `| ${pct}% | ${watch}% | ${rel}× |\n`;
    }

    // Flag the biggest drop-off point
    let biggestDrop = { from: 0, to: 0, drop: 0 };
    for (let i = 1; i < rows.length; i++) {
      const drop = rows[i - 1][1] - rows[i][1];
      if (drop > biggestDrop.drop) {
        biggestDrop = { from: rows[i - 1][0], to: rows[i][0], drop };
      }
    }
    if (biggestDrop.drop > 0) {
      md += `\n**🔴 Biggest drop-off:** ${(biggestDrop.from * 100).toFixed(0)}% → ${(biggestDrop.to * 100).toFixed(0)}% of video (lost ${(biggestDrop.drop * 100).toFixed(1)}% of audience).\n`;
      const videoDurSec = parseDuration(v.duration);
      if (videoDurSec > 0) {
        const fromSec = Math.round(biggestDrop.from * videoDurSec);
        const toSec = Math.round(biggestDrop.to * videoDurSec);
        md += `→ Approximate timestamp: **${fmtMMSS(fromSec)} → ${fmtMMSS(toSec)}** of a ${fmtMMSS(videoDurSec)} video.\n`;
      }
    }
    md += `\n`;
  } else if (daysOld < 3) {
    md += `> _Retention curve not yet available — populates ~72h after publish (currently ${daysOld.toFixed(1)}d). Check back soon._\n\n`;
  } else {
    md += `> _No retention data returned. Likely too few views for YouTube to compute (typically needs ~50+ views)._\n\n`;
  }

  if ((dive.daily?.rows || []).length > 0) {
    md += `**Daily breakdown since publish:**\n\n`;
    md += `| Day | Views | Watch min | AVD | Subs+ | Likes | Comments | Shares |\n|---|---|---|---|---|---|---|---|\n`;
    for (const r of dive.daily.rows) {
      md += `| ${r[0]} | ${r[1]} | ${r[2]} | ${r[3] || 0}s | ${r[4]} | ${r[5]} | ${r[6]} | ${r[7]} |\n`;
    }
    md += `\n`;
  }

  md += `---\n\n`;
}

// ============================================================
//  WHAT THE API CAN NOT TELL US
// ============================================================
md += `## What this puller CANNOT see (Studio-only / API limits)\n\n`;
md += `1. **Thumbnail impressions + impression CTR.** Confirmed via probe: the API rejects \`impressions\` as "Unknown identifier". This is the #1 click metric. Studio shows it; no public endpoint exposes it. Cross-check fresh uploads in YT Studio for CTR.\n`;
md += `2. **Search terms / specific traffic source detail.** \`insightTrafficSourceDetail\` filtered queries return "query not supported." YouTube does not expose individual search queries via the public API (only Search Console exposes that, and YouTube isn't there).\n`;
md += `3. **Real-time data on uploads <72h old.** Hard ~72h API lag — even \`views\` returns 0 from Analytics API for fresh uploads. We fall back to Data API \`viewCount\` for lifetime views (real-time), but AVD/retention/watch-minutes lag 3 days.\n`;
md += `4. **Sub-source attribution.** \`subscribersGained dimensions=insightTrafficSourceType\` rejected as "query not supported." Studio's Subscribers tab shows this; API doesn't.\n`;
md += `5. **Demographics under threshold.** Age/gender data hidden until ~100+ unique viewers in a window (privacy floor).\n\n`;

md += `## Quick health check (per analytics baselines)\n\n`;
md += `Targets per \`content/au-dealer-math/research/yt-analytics-baselines-2026-05-01.md\`:\n`;
md += `- Avg view duration ≥ **45%** (current channel avg: ${(chanMetrics.averageViewDuration || 0)}s)\n`;
md += `- CTR ≥ **4%** _(Studio-only metric — see "What this puller CANNOT see" above)_\n`;
md += `- Return-viewer rate ≥ **10%** _(Studio-only — Audience tab)_\n`;
md += `\n_Pulled at ${new Date().toISOString()}_\n`;

// ============================================================
//  HELPERS for retention drop-off timestamp
// ============================================================
function parseDuration(iso) {
  // ISO 8601 duration like PT1M30S or PT12M5S or PT45S
  const m = (iso || '').match(/^PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?$/);
  if (!m) return 0;
  const h = parseInt(m[1] || '0', 10);
  const min = parseInt(m[2] || '0', 10);
  const s = parseInt(m[3] || '0', 10);
  return h * 3600 + min * 60 + s;
}
function fmtMMSS(sec) {
  const m = Math.floor(sec / 60);
  const s = sec % 60;
  return `${m}:${String(s).padStart(2, '0')}`;
}

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
