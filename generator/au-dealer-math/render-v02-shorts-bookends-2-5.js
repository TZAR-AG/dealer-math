// Render V2 Shorts 2-5 bookend VOs via ElevenLabs API.
// Uses LOCKED Mac voice settings (Paul WLKp2jV6nrS8aMkPPDRO, v2/0.40/0.75/0.25/Speed 0.90).
// DO NOT MODIFY VOICE SETTINGS — see feedback_macca_voice_locked_forever_no_silent_edits_2026-05-03.md
//
// Run from repo root: node generator/au-dealer-math/render-v02-shorts-bookends-2-5.js

const fs = require('node:fs');
const path = require('node:path');
const { setTimeout: sleep } = require('node:timers/promises');

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

const VOICE_ID = 'WLKp2jV6nrS8aMkPPDRO';
const MODEL_ID = 'eleven_multilingual_v2';
// =====================================================================
// MAC VOICE — LOCKED FOREVER. DO NOT MODIFY. NO EXCEPTIONS.
// =====================================================================
const VOICE_SETTINGS = {
  stability: 0.40,
  similarity_boost: 0.75,
  style: 0.25,
  use_speaker_boost: true,
  speed: 0.90,
};

const OUT_DIR = path.resolve(
  __dirname, '..', '..',
  'content', 'au-dealer-math', 'scripts', 'v02-renders', 'voice-shorts'
);

// Each Short = open + close pair, loop seam baked in (close phrase chains
// naturally back to open).
const BOOKENDS = [
  // Short 2 — Rate Range ($3,000) — S5 "Why [process] costs $[X]"
  { name: 'short2-open',  text: 'How much does a two percent rate markup actually cost you?' },
  { name: 'short2-close', text: "Two percent. Three thousand dollars. That's how it adds up." },

  // Short 3 — Same Bank Different Outcomes — S2 "Never [verb] [thing] at a [place]"
  { name: 'short3-open',  text: 'Same bank. Same approval. Why do two buyers walk out with different rates?' },
  { name: 'short3-close', text: 'Same bank. Same approval. Different outcomes.' },

  // Short 4 — Aftercare Margin ($3,000) — S1 "[$Specific] [Verb] [object/process]"
  { name: 'short4-open',  text: "There's a room before the F and I office most buyers don't notice." },
  { name: 'short4-close', text: "Three thousand dollars. One room. Most buyers don't even notice it." },

  // Short 5 — Three Rooms / Three Negotiations — S3 "[N] [items] before you [action]"
  { name: 'short5-open',  text: 'How many people do you actually negotiate with at a dealership?' },
  { name: 'short5-close', text: 'You thought you negotiated with one. You negotiated with three.' },
];

async function renderBookend(text, outPath, idx) {
  const url = `https://api.elevenlabs.io/v1/text-to-speech/${VOICE_ID}/with-timestamps`;
  const body = {
    text,
    model_id: MODEL_ID,
    language_code: 'en',
    voice_settings: VOICE_SETTINGS,
    apply_text_normalization: 'on',
    seed: 42424242 + 2000 + idx,
    previous_text: null,
    next_text: null,
  };
  const res = await fetch(url, {
    method: 'POST',
    headers: {
      'xi-api-key': API_KEY,
      'Content-Type': 'application/json',
      'Accept': 'application/json',
    },
    body: JSON.stringify(body),
  });
  if (!res.ok) {
    const err = await res.text();
    throw new Error(`ElevenLabs ${res.status}: ${err.slice(0, 300)}`);
  }
  const json = await res.json();
  const audio = Buffer.from(json.audio_base64, 'base64');
  fs.writeFileSync(outPath, audio);

  const align = json.normalized_alignment || json.alignment;
  const wordTimings = [];
  if (align && align.characters && align.character_start_times_seconds && align.character_end_times_seconds) {
    const chars = align.characters;
    const starts = align.character_start_times_seconds;
    const ends = align.character_end_times_seconds;
    let curWord = '';
    let curStart = null;
    for (let i = 0; i < chars.length; i++) {
      const c = chars[i];
      if (c.match(/\s/)) {
        if (curWord) {
          wordTimings.push({ word: curWord, timeline_start: curStart, timeline_end: ends[i-1] });
          curWord = '';
          curStart = null;
        }
      } else {
        if (!curWord) curStart = starts[i];
        curWord += c;
      }
    }
    if (curWord) {
      wordTimings.push({
        word: curWord,
        timeline_start: curStart,
        timeline_end: ends[chars.length - 1],
      });
    }
  }
  const timingsPath = outPath.replace(/\.mp3$/, '.timings.json');
  fs.writeFileSync(timingsPath, JSON.stringify({ text, words: wordTimings }, null, 2));
  return { bytes: audio.length, words: wordTimings.length };
}

async function main() {
  if (!fs.existsSync(OUT_DIR)) fs.mkdirSync(OUT_DIR, { recursive: true });

  console.log('=== V2 Shorts 2-5 — bookend VOs ===');
  console.log(`Voice: Paul (Mac LOCKED) speed=${VOICE_SETTINGS.speed} stab=${VOICE_SETTINGS.stability}`);
  console.log('---');

  for (let i = 0; i < BOOKENDS.length; i++) {
    const { name, text } = BOOKENDS[i];
    const outPath = path.join(OUT_DIR, `${name}.mp3`);
    process.stdout.write(`[${i+1}/${BOOKENDS.length}] ${name}: "${text}"... `);
    try {
      const { bytes, words } = await renderBookend(text, outPath, i);
      console.log(`OK ${(bytes/1024).toFixed(0)}KB · ${words} words`);
      await sleep(300);
    } catch (e) {
      console.log(`FAILED: ${e.message}`);
      process.exit(1);
    }
  }
  console.log('---');
  console.log('Output dir:', OUT_DIR);
}

main().catch(e => { console.error('FATAL:', e); process.exit(1); });
