// Regenerate AU Dealer Math V1 voiceover via ElevenLabs API.
// Reads the V1 script, splits into 7 scenes, renders each at locked Macca
// voice (Paul) settings, saves to v01-renders/voice/.
//
// Run from repo root: node generator/au-dealer-math/regenerate-vo.js
//
// Env required: ELEVENLABS_API_KEY (loaded from .env)

const fs = require('node:fs');
const path = require('node:path');
const { setTimeout: sleep } = require('node:timers/promises');

// Manual .env loader (avoid dotenv dep in commonjs subpkg)
const envPath = path.resolve(__dirname, '..', '..', '.env');
const envText = fs.readFileSync(envPath, 'utf8');
const env = Object.fromEntries(
  envText
    .split('\n')
    .filter(l => l && !l.startsWith('#') && l.includes('='))
    .map(l => {
      const idx = l.indexOf('=');
      return [l.slice(0, idx).trim(), l.slice(idx + 1).trim().replace(/^["']|["']$/g, '')];
    })
);

const API_KEY = env.ELEVENLABS_API_KEY;
if (!API_KEY) {
  console.error('FATAL: ELEVENLABS_API_KEY not in .env');
  process.exit(1);
}

const VOICE_ID = 'WLKp2jV6nrS8aMkPPDRO'; // Paul — locked Macca voice
const MODEL_ID = 'eleven_multilingual_v2';
const VOICE_SETTINGS = {
  stability: 0.55, // Bumped from 0.40 (2026-04-30) — reduces stutter/glitch artifacts on long scenes
  similarity_boost: 0.75,
  style: 0.25,
  use_speaker_boost: true,
  speed: 0.95, // Bumped from 0.90 (2026-04-30) — Adrian wanted slightly faster pacing
};

const SCRIPT_PATH = path.resolve(
  __dirname, '..', '..',
  'content', 'au-dealer-math', 'scripts', 'v01-payment-not-price-pivot.md'
);
const OUT_DIR = path.resolve(
  __dirname, '..', '..',
  'content', 'au-dealer-math', 'scripts', 'v01-renders', 'voice'
);

// Map script scene headers to output filenames matching CapCut convention
const SCENE_FILES = {
  'HOOK': 'vo-scene-1-hook.mp3',
  'AUTHORITY ANCHOR': 'vo-scene-2-authority.mp3',
  'THE QUESTION': 'vo-scene-3-question.mp3',
  'THE LOAN-TERM': 'vo-scene-4-loan-trick.mp3',
  'WHY THE DEALER': 'vo-scene-5-why-dealer.mp3',
  'THE FIX': 'vo-scene-6-fix.mp3',
  'CTA': 'vo-scene-7-signoff.mp3',
};

function parseScenes(markdown) {
  // Match scene headers like "## [0:00–0:15] HOOK — Mistake Callout"
  const lines = markdown.split('\n');
  const scenes = [];
  let current = null;

  for (const line of lines) {
    const headerMatch = line.match(/^## \[(\d+:\d+).+?\]\s+(.+)$/);
    if (headerMatch) {
      if (current) scenes.push(current);
      current = { title: headerMatch[2].trim(), lines: [] };
      continue;
    }
    // Stop at "## Production notes" / "## Voice rules QC pass" etc — non-scene sections
    if (/^## (Production|Voice rules|Spec)/.test(line)) {
      if (current) scenes.push(current);
      current = null;
      continue;
    }
    if (current && line.startsWith('>')) {
      // Strip the leading "> " and trim
      current.lines.push(line.replace(/^>\s?/, ''));
    }
  }
  if (current) scenes.push(current);

  return scenes.map(s => ({
    title: s.title,
    text: cleanText(s.lines.join('\n')),
  }));
}

function cleanText(raw) {
  return raw
    .replace(/\*\*(.+?)\*\*/g, '$1')        // bold markdown
    .replace(/\*(.+?)\*/g, '$1')             // italic markdown
    .replace(/`(.+?)`/g, '$1')               // inline code
    .replace(/^\s*\n+/gm, '')                // strip empty lines from blockquote breaks
    .replace(/\n+/g, ' ')                    // collapse multi-line into one paragraph for ElevenLabs
    .replace(/\s+/g, ' ')                    // collapse whitespace
    .trim();
}

function findFilenameForTitle(title) {
  for (const [key, fname] of Object.entries(SCENE_FILES)) {
    if (title.toUpperCase().includes(key)) return fname;
  }
  return null;
}

function approxDurationSec(byteSize) {
  // ElevenLabs default MP3 = 128kbps → 16,000 bytes/sec
  return Math.round(byteSize / 16000);
}

function fmtTime(sec) {
  const m = Math.floor(sec / 60);
  const s = sec % 60;
  return `${m}:${String(s).padStart(2, '0')}`;
}

// Optional pronunciation dictionary attachment
const PRONUNCIATION_DICT_ID = env.ELEVENLABS_AUDM_DICT_ID || null;
const PRONUNCIATION_DICT_VERSION = env.ELEVENLABS_AUDM_DICT_VERSION || null;

async function renderScene(text, outPath, ctx) {
  // ctx: { sceneIndex, prevText, nextText, prevReqId }
  // Output format: default 128kbps mp3 on Starter tier (192kbps is Creator-only — verified 2026-04-29)
  const url = `https://api.elevenlabs.io/v1/text-to-speech/${VOICE_ID}`;
  const body = {
    text,
    model_id: MODEL_ID,
    language_code: 'en',
    voice_settings: VOICE_SETTINGS,
    apply_text_normalization: 'on',  // forces $46,000 → "forty-six thousand dollars"
    seed: 42424242 + (ctx?.sceneIndex || 0),  // deterministic per-scene reproducibility
    // Stitching DISABLED 2026-04-30: previous_text/next_text caused audible
    // artifacts at scene boundaries — trailing silence at end (model expecting
    // continuation) and truncated first word at start (model assuming prior
    // context). Each scene now renders standalone with full open/close.
    previous_text: null,
    next_text: null,
    previous_request_ids: [],
  };
  if (PRONUNCIATION_DICT_ID && PRONUNCIATION_DICT_VERSION) {
    body.pronunciation_dictionary_locators = [{
      pronunciation_dictionary_id: PRONUNCIATION_DICT_ID,
      version_id: PRONUNCIATION_DICT_VERSION,
    }];
  }

  const res = await fetch(url, {
    method: 'POST',
    headers: {
      'xi-api-key': API_KEY,
      'Content-Type': 'application/json',
      'Accept': 'audio/mpeg',
    },
    body: JSON.stringify(body),
  });

  if (!res.ok) {
    const err = await res.text();
    throw new Error(`ElevenLabs ${res.status}: ${err.slice(0, 300)}`);
  }

  const reqId = res.headers.get('request-id') || null;
  const buffer = Buffer.from(await res.arrayBuffer());
  fs.writeFileSync(outPath, buffer);
  return { bytes: buffer.length, reqId };
}

async function main() {
  if (!fs.existsSync(OUT_DIR)) fs.mkdirSync(OUT_DIR, { recursive: true });

  const md = fs.readFileSync(SCRIPT_PATH, 'utf8');
  const scenes = parseScenes(md);
  console.log(`Parsed ${scenes.length} scenes from script.`);
  console.log(`Voice settings: speed ${VOICE_SETTINGS.speed} | stability ${VOICE_SETTINGS.stability} | similarity ${VOICE_SETTINGS.similarity_boost}`);
  console.log('---');

  let totalSec = 0;
  let totalChars = 0;
  let prevText = null;
  let prevReqId = null;

  if (PRONUNCIATION_DICT_ID) {
    console.log(`Pronunciation dict attached: ${PRONUNCIATION_DICT_ID}`);
  } else {
    console.log('No pronunciation dict (set ELEVENLABS_AUDM_DICT_ID + _VERSION in .env)');
  }
  console.log('Stitching: previous_text + next_text + previous_request_ids ON');
  console.log('Output format: default mp3_44100_128 (128kbps — Starter tier; 192kbps requires Creator)');
  console.log('Text normalization: ON · seed: 42424242+i');
  console.log('---');

  for (let i = 0; i < scenes.length; i++) {
    const scene = scenes[i];
    const fname = findFilenameForTitle(scene.title);
    if (!fname) {
      console.log(`  [skip] No filename mapping for "${scene.title}"`);
      continue;
    }
    const charCount = scene.text.length;
    totalChars += charCount;
    const outPath = path.join(OUT_DIR, fname);
    process.stdout.write(`[${i + 1}/${scenes.length}] ${fname} (${charCount} chars)... `);
    try {
      // Stitching context: last ~200 chars of previous + first ~200 chars of next
      const nextScene = scenes[i + 1];
      const ctx = {
        sceneIndex: i,
        prevText: prevText ? prevText.slice(-200) : null,
        nextText: nextScene ? nextScene.text.slice(0, 200) : null,
        prevReqId,
      };
      const { bytes, reqId } = await renderScene(scene.text, outPath, ctx);
      const sec = approxDurationSec(bytes);
      totalSec += sec;
      prevText = scene.text;
      prevReqId = reqId;  // valid 2 hours
      console.log(`✓ ${(bytes / 1024).toFixed(0)}KB ≈ ${fmtTime(sec)}${reqId ? ` · req=${reqId.slice(0, 8)}` : ''}`);
      // Brief pause to be polite to API
      await sleep(500);
    } catch (e) {
      console.log(`✗ FAILED: ${e.message}`);
      process.exit(1);
    }
  }

  console.log('---');
  console.log(`Total chars rendered: ${totalChars.toLocaleString()}`);
  console.log(`Approx total runtime: ${fmtTime(totalSec)}`);
  console.log(`Output: ${OUT_DIR}`);
}

main().catch(e => {
  console.error('FATAL:', e);
  process.exit(1);
});
