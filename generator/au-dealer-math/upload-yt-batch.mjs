// AUDM YouTube batch uploader.
//
// Reads a JSON spec file with an "uploads" array and uploads each entry
// serially using the same logic as upload-yt.mjs. Halts on first failure
// (no auto-retry — surface the error so Adrian can decide).
//
// Usage:
//   npm run yt-upload:batch -- --spec=path/to/batch.json [--dry-run]
//
// Spec format:
//   {
//     "uploads": [
//       {
//         "file": "video/out/shorts/audm-v2-short-1.mp4",
//         "title": "What dealers do in the F&I office",
//         "description_file": "content/au-dealer-math/scripts/v02-shorts-metadata.md#short-1-description",
//         "tags": ["AUDealerMath", "DealerFinance", "shorts"],
//         "category_id": 22,
//         "schedule": "2026-05-05T18:00:00+08:00",
//         "privacy": "private",
//         "made_for_kids": false,
//         "thumbnail": "path/to/thumb.png",
//         "comment_file": "content/au-dealer-math/scripts/v02-shorts-metadata.md#short-1-pinned-comment"
//       },
//       ...
//     ]
//   }

import fs from 'node:fs/promises';
import path from 'node:path';
import { spawn } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, '..', '..');
const UPLOAD_SCRIPT = path.join(__dirname, 'upload-yt.mjs');
const LOG_DIR = path.join(ROOT, 'content', 'au-dealer-math', 'uploads');

function parseArgs(argv) {
  const out = {};
  for (const arg of argv.slice(2)) {
    if (!arg.startsWith('--')) continue;
    const eq = arg.indexOf('=');
    if (eq === -1) out[arg.slice(2)] = true;
    else out[arg.slice(2, eq)] = arg.slice(eq + 1);
  }
  return out;
}

const args = parseArgs(process.argv);
if (!args.spec) {
  console.error('X --spec=<path-to-json> is required.');
  process.exit(1);
}

const specPath = path.isAbsolute(args.spec) ? args.spec : path.join(ROOT, args.spec);
const specRaw = await fs.readFile(specPath, 'utf8');
const spec = JSON.parse(specRaw);

if (!Array.isArray(spec.uploads) || !spec.uploads.length) {
  console.error('X spec.uploads must be a non-empty array.');
  process.exit(1);
}

// ============================================================================
// Pre-flight quota estimate
// ============================================================================

let estimatedQuota = 0;
for (const u of spec.uploads) {
  estimatedQuota += 1600;
  if (u.thumbnail) estimatedQuota += 50;
  if (u.comment_file) estimatedQuota += 50;
}

console.log(`=== Batch upload plan ===`);
console.log(`  Spec:               ${args.spec}`);
console.log(`  Uploads:            ${spec.uploads.length}`);
console.log(`  Estimated quota:    ~${estimatedQuota} units / 10,000 daily`);
console.log(`  Quota utilization:  ${(estimatedQuota / 100).toFixed(1)}%`);
if (estimatedQuota > 10000) {
  console.error(`\nX Estimated quota exceeds 10,000 daily limit. Split the batch.`);
  process.exit(1);
}
if (estimatedQuota > 8000) {
  console.warn(`\n! WARNING: Estimated quota >8,000 units (>80% of daily limit).`);
  console.warn(`  If anything else uses YT API today, this batch may fail mid-run.`);
}
console.log('');

// ============================================================================
// Sequential upload via child_process
// ============================================================================

function buildArgs(u) {
  const a = [
    UPLOAD_SCRIPT,
    `--file=${u.file}`,
    `--title=${u.title}`,
    `--description-file=${u.description_file}`,
  ];
  if (u.tags) {
    const tagsStr = Array.isArray(u.tags) ? u.tags.join(',') : u.tags;
    a.push(`--tags=${tagsStr}`);
  }
  if (u.category_id != null) a.push(`--category-id=${u.category_id}`);
  if (u.schedule) a.push(`--schedule=${u.schedule}`);
  if (u.privacy) a.push(`--privacy=${u.privacy}`);
  if (u.made_for_kids === true) a.push('--made-for-kids');
  if (u.thumbnail) a.push(`--thumbnail=${u.thumbnail}`);
  if (u.comment_file) a.push(`--comment-file=${u.comment_file}`);
  if (args['dry-run']) a.push('--dry-run');
  return a;
}

function runOne(u, idx) {
  return new Promise((resolve, reject) => {
    const cliArgs = buildArgs(u);
    console.log(`\n--- [${idx + 1}/${spec.uploads.length}] ${u.title} ---`);
    const child = spawn(process.execPath, cliArgs, {
      cwd: ROOT,
      stdio: 'inherit',
    });
    child.on('exit', code => {
      if (code === 0) resolve();
      else reject(new Error(`Upload ${idx + 1} exited with code ${code}`));
    });
    child.on('error', reject);
  });
}

const results = [];
let halted = false;
for (let i = 0; i < spec.uploads.length; i++) {
  if (halted) break;
  const u = spec.uploads[i];
  const startedAt = new Date().toISOString();
  try {
    await runOne(u, i);
    results.push({
      index: i,
      title: u.title,
      file: u.file,
      schedule: u.schedule || null,
      status: args['dry-run'] ? 'dry-run-ok' : 'uploaded',
      startedAt,
      finishedAt: new Date().toISOString(),
    });
  } catch (err) {
    results.push({
      index: i,
      title: u.title,
      file: u.file,
      status: 'FAILED',
      error: err.message,
      startedAt,
      finishedAt: new Date().toISOString(),
    });
    console.error(`\nX Halting batch at upload ${i + 1}: ${err.message}`);
    console.error(`   No auto-retry. Investigate, fix, re-run with a trimmed spec.`);
    halted = true;
  }
}

// Save log
await fs.mkdir(LOG_DIR, { recursive: true });
const isoSafe = new Date().toISOString().replace(/[:.]/g, '-');
const logPath = path.join(LOG_DIR, `upload-log-${isoSafe}.json`);
await fs.writeFile(logPath, JSON.stringify({
  spec_path: args.spec,
  dry_run: !!args['dry-run'],
  total: spec.uploads.length,
  completed: results.filter(r => r.status === 'uploaded' || r.status === 'dry-run-ok').length,
  failed: results.filter(r => r.status === 'FAILED').length,
  results,
}, null, 2));

console.log(`\n=== Batch ${halted ? 'HALTED' : 'complete'} ===`);
console.log(`  Log: ${logPath}`);
console.log(`  Completed: ${results.filter(r => r.status === 'uploaded' || r.status === 'dry-run-ok').length}/${spec.uploads.length}`);
if (halted) {
  console.log(`  Failed at: upload ${results.findIndex(r => r.status === 'FAILED') + 1}`);
  process.exit(3);
}
