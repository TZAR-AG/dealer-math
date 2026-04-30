// One-shot: re-render scene 7 (signoff) only with updated text.
// Mirrors regenerate-vo.js settings exactly so the voice/seed match.
//
// Run: node generator/au-dealer-math/render-scene-7-only.js

const fs = require('node:fs');
const path = require('node:path');

const envPath = path.resolve(__dirname, '..', '..', '.env');
const envText = fs.readFileSync(envPath, 'utf8');
const env = Object.fromEntries(
  envText.split('\n').filter(l => l && !l.startsWith('#') && l.includes('=')).map(l => {
    const idx = l.indexOf('=');
    return [l.slice(0, idx).trim(), l.slice(idx + 1).trim().replace(/^["']|["']$/g, '')];
  })
);

const API_KEY = env.ELEVENLABS_API_KEY;
if (!API_KEY) { console.error('FATAL: ELEVENLABS_API_KEY not in .env'); process.exit(1); }

const VOICE_ID = 'WLKp2jV6nrS8aMkPPDRO';
const MODEL_ID = 'eleven_multilingual_v2';
const VOICE_SETTINGS = { stability: 0.55, similarity_boost: 0.75, style: 0.25, use_speaker_boost: true, speed: 0.95 };

// Parsed verbatim from v01-payment-not-price-pivot.md scene 7 blockquotes (post-update).
// 2026-04-30 third pass: split the closing into two sentences so "Dealer Math"
// is its own stressed final beat, not a tail-off. "I'm Mac." [period] then
// "Thanks for watching A. U. Dealer Math." [period] — letters spelled out
// individually via spaced periods (A. U.) which the model handles cleanly,
// and the channel name lands as the final emphasis.
const SCENE_7_TEXT = "Stay tuned for the next video. If you want the full cheatsheet — the seven lines on a dealer contract you should never sign — link in the description. Free. No catch. I'm Mac. Thanks for watching A. U. Dealer Math.";

const OUT_PATH = path.resolve(
  __dirname, '..', '..',
  'content', 'au-dealer-math', 'scripts', 'v01-renders', 'voice', 'vo-scene-7-signoff.mp3'
);

const PRONUNCIATION_DICT_ID = env.ELEVENLABS_AUDM_DICT_ID || null;
const PRONUNCIATION_DICT_VERSION = env.ELEVENLABS_AUDM_DICT_VERSION || null;

async function main() {
  console.log(`Re-rendering scene 7 with new sign-off line:`);
  console.log(`  "${SCENE_7_TEXT}"`);
  console.log(`Voice settings: speed ${VOICE_SETTINGS.speed} | stability ${VOICE_SETTINGS.stability} | similarity ${VOICE_SETTINGS.similarity_boost}`);
  console.log(`Seed: 42424248 (matches scene 7 in regenerate-vo.js: 42424242 + 6)`);
  console.log('---');

  const url = `https://api.elevenlabs.io/v1/text-to-speech/${VOICE_ID}`;
  const body = {
    text: SCENE_7_TEXT,
    model_id: MODEL_ID,
    language_code: 'en',
    voice_settings: VOICE_SETTINGS,
    apply_text_normalization: 'on',
    seed: 42424242 + 6, // scene index 6 = scene 7
    previous_text: null,
    next_text: null,
    previous_request_ids: [],
  };
  if (PRONUNCIATION_DICT_ID && PRONUNCIATION_DICT_VERSION) {
    body.pronunciation_dictionary_locators = [{
      pronunciation_dictionary_id: PRONUNCIATION_DICT_ID,
      version_id: PRONUNCIATION_DICT_VERSION,
    }];
    console.log(`Pronunciation dict: ${PRONUNCIATION_DICT_ID}`);
  } else {
    console.log('No pronunciation dict attached');
  }

  const res = await fetch(url, {
    method: 'POST',
    headers: { 'xi-api-key': API_KEY, 'Content-Type': 'application/json', 'Accept': 'audio/mpeg' },
    body: JSON.stringify(body),
  });

  if (!res.ok) {
    const err = await res.text();
    throw new Error(`ElevenLabs ${res.status}: ${err.slice(0, 500)}`);
  }

  const buffer = Buffer.from(await res.arrayBuffer());
  fs.writeFileSync(OUT_PATH, buffer);
  const approxSec = Math.round(buffer.length / 16000);
  console.log(`✓ Wrote ${(buffer.length / 1024).toFixed(0)}KB ≈ ~${approxSec}s to ${OUT_PATH}`);
  console.log('Run ffprobe next to get exact duration.');
}

main().catch(e => { console.error('FATAL:', e); process.exit(1); });
