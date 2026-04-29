# ElevenLabs (Paul / Macca voice) — AUDM canonical prompt reference

> **🟢 PIPELINE UPGRADES (Starter-tier compatible, all shipped 2026-04-29):**
> 1. ✅ `previous_text`/`next_text`/`previous_request_ids` in `regenerate-vo.js` for scene-to-scene continuity
> 2. ✅ `apply_text_normalization: "on"` for guaranteed dollar/percentage handling
> 3. ✅ `seed` for reproducibility
> 4. 🚫 192kbps output — **Creator-tier only**; using default 128kbps on Starter
> 5. 🚫 Pronunciation dictionary upload — **Creator-tier only**; using phonetic respelling in script text instead (free, see § Phonetic respelling fallback)

**Engine:** Eleven Multilingual v2 (NOT v3 — v3 not optimised for library voices in 2026; audio tags `[pause]`/`[excited]` are v3-only and print as text in v2).
**Voice:** Paul - Australian Professional Presenter, Voice ID `WLKp2jV6nrS8aMkPPDRO`
**Tier:** **Starter** (verified 2026-04-29 — earlier "Creator $99" memory was wrong). Single ElevenLabs account on hello@thestructuredself.com, shared with SS work. Pronunciation Dictionaries are Creator-tier-locked → AUDM uses phonetic respelling in script text instead (free workaround, see § Phonetic respelling fallback below).
**Use AUDM for:** every long-form VO render. Render via API directly from `generator/au-dealer-math/regenerate-vo.js`.

---

## Locked voice settings (LOCKED 2026-04-29)

| Setting | Value | Rationale |
|---|---|---|
| Model | `eleven_multilingual_v2` | NOT v3 (library voice optimization) |
| Stability | **0.40** | Docs recommend 35-45% for documentary narration. Adds "imperfections that make it sound human" |
| Similarity | **0.75** | Docs say "0.75 for most cases"; >0.80 = artifacts |
| Style | **0.25** | Narrator-documentary band (10-50%). Lower-expressive = authority. Higher = emotional |
| Speaker Boost | ON | |
| Speed | **0.90** | Sweet spot. 0.85 = consonant-mush; 0.95 = auctioneer. 0.90 = natural narrator authority pace |
| Chunk size | ≤2000 chars (we send full scenes, ~400-700 chars each) | Sweet spot 250-800 chars per chunk; >1000 = tone drift; <250 = inconsistency |

**Optional A/B (after V1):** style 0.30 on hook + close, style 0.20 on body explanation scenes. Documentary narrators do this naturally; AI voices need it manually.

---

## Canonical API request body

This is the gold-standard request for every AUDM scene render. Update `regenerate-vo.js` to match:

```javascript
const body = {
  // CORE
  text: sceneText,                         // 250-800 chars ideal per chunk
  model_id: "eleven_multilingual_v2",
  language_code: "en",                     // forces English path, locks AU accent

  // VOICE SETTINGS (LOCKED)
  voice_settings: {
    stability: 0.40,
    similarity_boost: 0.75,
    style: 0.25,
    use_speaker_boost: true,
    speed: 0.90
  },

  // TEXT NORMALIZATION (NEW — set explicitly, don't rely on auto)
  apply_text_normalization: "on",          // forces $46,000 → "forty-six thousand dollars"

  // REPRODUCIBILITY (NEW)
  seed: 42424242,                          // lock per-scene; vary by +i for each scene

  // STITCHING (NEW — biggest single-shot quality lift)
  previous_text: prevSceneText || null,    // last 1-2 sentences of prior scene
  next_text: nextSceneText || null,        // first 1-2 sentences of next scene
  previous_request_ids: prevReqId ? [prevReqId] : [],

  // PRONUNCIATION DICT (NEW — see § Pronunciation dictionary below)
  pronunciation_dictionary_locators: [
    { pronunciation_dictionary_id: AUDM_DICT_ID, version_id: AUDM_DICT_VERSION }
  ]
};

// Query params:
// ?output_format=mp3_44100_128 (default — 192kbps is Creator-tier only)   (192kbps mp3, Creator-tier supported, free quality bump)
// Do NOT set optimize_streaming_latency — deprecated and we're not streaming
```

**Capture the response header `request-id` after each call** and pass it as `previous_request_ids` to the next call within the same render run. Single highest-leverage change to our pipeline. Request ID chain is valid for 2 hours.

---

## SSML / text cheat-sheet (Multilingual v2 specifics)

| Goal | Use this | Don't use |
|---|---|---|
| 0.5-1s pause for impact (after dollar reveal) | `<break time="0.7s" />` | Audio tags `[pause]` (v3 only — prints as text in v2) |
| 1.5-2s "let it land" pause | `<break time="1.8s" />` | More than 2 breaks per chunk (instability) |
| Natural breath / cadence | Paragraph break (blank line in `text`) | Forced breaks for breathing |
| Soft hesitation | Ellipsis `...` (adds slight nervousness — use intentionally) | — |
| Short rhythmic pause | Em-dash `—` or comma | — |
| Emphasis on a word | ALL CAPS the word: "forty-six thousand dollars MORE" | `<emphasis>` (no v2 effect) |
| Phonetic respelling tricks | Hyphen-stress: "Mack-uh", "Mer-SAY-deez Benz" | `<phoneme>` (Flash/English v1 only — incompatible with v2) |
| Long-form consistency | `previous_text` / `next_text` API params | — |

**AUDM-specific tag placement (drop into scene scripts):**

- **Hook reveal:** `"forty-six thousand dollars <break time="0.6s" /> more out of your pocket."`
- **Authority anchor:** `"I'm Mack-uh. <break time="0.4s" /> Twenty years in dealerships."`
- **Trick reveal:** `"That's the loan-term trick. <break time="1.2s" /> Now here's how to flip it."`
- **CTA close:** `"Until next time <break time="0.5s" /> drive smart out there."`

**Stay under 3 break tags per scene** to dodge instability artifacts.

**Multilingual v2 already handles `$46,000` → "forty-six thousand dollars" correctly via `apply_text_normalization: "on"`** — no need to spell out numbers manually. Same for percentages: `9%` renders as "nine percent."

---

## Phonetic respelling fallback (Starter tier — current AUDM path)

**Pronunciation Dictionaries are gated behind Creator tier.** AUDM is on Starter, so we use **capital-letter-stress phonetic spelling in the raw script text** instead. ElevenLabs Multilingual v2 honors this directly — no API parameters needed.

| Word as-spoken | Phonetic respelling in script |
|---|---|
| Macca | `Mack-uh` |
| Mercedes | `Mer-SAY-deez` |
| Mercedes-Benz | `Mer-SAY-deez Benz` |
| Hyundai | `HUN-day` |
| Porsche | `POR-shuh` |
| Volkswagen | `VOLKS-vah-gen` |
| Peugeot | `POO-zho` |
| Renault | `REN-oh` |
| HiLux | `HIGH-lux` |
| ute (slang) | `yoot` |
| rego | `redge-oh` |
| servo | `serv-oh` |
| arvo | `ah-voh` |
| BMW (acronym) | `B M W` (with spaces) |
| MG | `M G` |
| BYD | `B Y D` |
| ATO | `A T O` |
| GFV | `G F V` |

**SOP:** before any new render, scan the script for any of the above words → swap to phonetic respelling. Script files keep the respellings (ugly to read but correct to render).

The `.pls` file at `_assets/audm-pronunciation.pls` stays in the repo for the day we upgrade to Creator tier — same content, just attached via API once Creator unlocks dict-write permission.

## Pronunciation dictionary (.pls upload, one-time — UPGRADE PATH ONLY)

⚠ **Requires Creator tier ($33 AUD/mo upgrade from Starter).** Currently NOT in use — AUDM uses phonetic respelling fallback instead. Below is the upgrade documentation for if/when AUDM justifies the tier bump.

Use **alias substitution** (not phoneme — v2 doesn't support phonemes). Upload as `.pls` XML once, attach `pronunciation_dictionary_id` + `version_id` to every TTS call.

**File: `content/au-dealer-math/saas-prompts/_assets/audm-pronunciation.pls`**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<lexicon version="1.0"
  xmlns="http://www.w3.org/2005/01/pronunciation-lexicon"
  alphabet="ipa" xml:lang="en-AU">

  <!-- Brand / persona -->
  <lexeme><grapheme>Macca</grapheme><alias>Mack-uh</alias></lexeme>

  <!-- AU vernacular -->
  <lexeme><grapheme>ute</grapheme><alias>yoot</alias></lexeme>
  <lexeme><grapheme>rego</grapheme><alias>redge-oh</alias></lexeme>
  <lexeme><grapheme>servo</grapheme><alias>serv-oh</alias></lexeme>
  <lexeme><grapheme>arvo</grapheme><alias>ah-voh</alias></lexeme>

  <!-- Car brands -->
  <lexeme><grapheme>Mercedes</grapheme><alias>Mer-SAY-deez</alias></lexeme>
  <lexeme><grapheme>Mercedes-Benz</grapheme><alias>Mer-SAY-deez Benz</alias></lexeme>
  <lexeme><grapheme>Hyundai</grapheme><alias>HUN-day</alias></lexeme>
  <lexeme><grapheme>Porsche</grapheme><alias>POR-shuh</alias></lexeme>
  <lexeme><grapheme>Volkswagen</grapheme><alias>VOLKS-vah-gen</alias></lexeme>
  <lexeme><grapheme>Peugeot</grapheme><alias>POO-zho</alias></lexeme>
  <lexeme><grapheme>Renault</grapheme><alias>REN-oh</alias></lexeme>
  <lexeme><grapheme>BMW</grapheme><alias>B M W</alias></lexeme>
  <lexeme><grapheme>MG</grapheme><alias>M G</alias></lexeme>
  <lexeme><grapheme>BYD</grapheme><alias>B Y D</alias></lexeme>

  <!-- Models -->
  <lexeme><grapheme>HiLux</grapheme><alias>HIGH-lux</alias></lexeme>
  <lexeme><grapheme>D-Max</grapheme><alias>Dee-Max</alias></lexeme>
  <lexeme><grapheme>MU-X</grapheme><alias>M U X</alias></lexeme>
  <lexeme><grapheme>BT-50</grapheme><alias>B T fifty</alias></lexeme>

  <!-- Acronyms -->
  <lexeme><grapheme>p.a.</grapheme><alias>per annum</alias></lexeme>
  <lexeme><grapheme>APR</grapheme><alias>A P R</alias></lexeme>
  <lexeme><grapheme>RRP</grapheme><alias>R R P</alias></lexeme>
  <lexeme><grapheme>WOVR</grapheme><alias>W O V R</alias></lexeme>
  <lexeme><grapheme>EOFY</grapheme><alias>ee oh eff why</alias></lexeme>
  <lexeme><grapheme>ATO</grapheme><alias>A T O</alias></lexeme>
</lexicon>
```

**Upload path:** ElevenLabs dashboard → Voices → Pronunciation Dictionaries → New → upload `audm-pronunciation.pls`. Capture the `pronunciation_dictionary_id` + `version_id` returned. Add to `.env`:

```
ELEVENLABS_AUDM_DICT_ID=...
ELEVENLABS_AUDM_DICT_VERSION=...
```

**Test entries on V1 render** — if Paul nails "Mercedes" natively, drop the entry to avoid over-correction. Multilingual v2's text normalizer handles `$46,000` and `2.9%` — do NOT add entries for raw dollar/percent figures.

---

## Chunk strategy

**Verdict: keep one-scene-per-call AND add stitching params.** Don't split scenes further.

- Scene typical size: 400-700 chars → already in the 250-800 sweet spot
- What was missing: each scene was sent as isolated request with no context → tone drift between scenes
- **Stitching solves drift better than smaller chunks would**

The updated `regenerate-vo.js` loop:

```javascript
let prevText = null;
let prevReqId = null;

for (let i = 0; i < scenes.length; i++) {
  const scene = scenes[i];
  const nextText = scenes[i + 1]?.text?.slice(0, 200) || null;
  const prevSnippet = prevText?.slice(-200) || null;

  const body = {
    text: scene.text,
    model_id: MODEL_ID,
    voice_settings: VOICE_SETTINGS,
    apply_text_normalization: "on",
    seed: 42424242 + i,
    previous_text: prevSnippet,
    next_text: nextText,
    previous_request_ids: prevReqId ? [prevReqId] : []
  };

  const res = await fetch(url, { method: 'POST', /* ... */ body: JSON.stringify(body) });
  const reqId = res.headers.get('request-id');
  // ... save buffer ...
  prevText = scene.text;
  prevReqId = reqId;     // valid 2 hours
}
```

---

## Speed parameter empirical curve

Measured behavior (V1 expanded script, 2480 words):

| Speed | Effective wpm | V1 runtime | Mid-roll status |
|---|---|---|---|
| 0.95 (original lock) | ~326 | 4:57 | ⚠ under 8:00 (no mid-roll) |
| 0.92 | ~282 | ~9:09 | ✓ 1 mid-roll |
| 0.90 ⭐ | ~226 | 10:58 | ✓✓ 2 mid-rolls |
| 0.88 | ~258 | ~7:46 | ⚠ under 8:00 |
| 0.85 | ~204 | 12:10 | ✓✓ but felt dragged |

**Range hard limit: 0.7-1.2** (API rejects outside). Quality degrades audibly below ~0.85 (consonant mushiness).

**Sweet spot for AUDM authority pace: 0.90.** Locked.

---

## Implementation priority

1. **Add `previous_text`/`next_text`/`previous_request_ids` to `regenerate-vo.js`** — biggest single-shot quality lift, ~30 min code change. Should be done BEFORE next render run.
2. **Upload AUDM pronunciation dictionary** (one-time .pls upload, attach locator to every render).
3. **Set `apply_text_normalization: "on"` and `seed`** (3 lines of code).
4. **Bump `output_format` to `mp3_44100_128 (default — 192kbps is Creator-tier only)`** (one query param).
5. **Optional later:** scene-level style modulation (0.30 hook / 0.20 body) for V2+.

---

## Failure modes + mitigations

| Symptom | Cause | Fix |
|---|---|---|
| Voice tone shifts between scenes | No request stitching | Add `previous_text`/`next_text`/`previous_request_ids` |
| `$46,000` rendered as "dollar four six zero zero zero" | `apply_text_normalization` set to default (auto) which can be unreliable | Set explicitly: `apply_text_normalization: "on"` |
| "Macca" pronounced wrong (Mack-AH or hard-c) | Pronunciation dict not attached | Upload `.pls`, attach locator |
| Voice quality mushy on long scenes | Speed too low (<0.85) OR chunk too long (>1000 chars) | Stay at 0.90; keep scenes 400-700 chars |
| Audio tags `[pause]`/`[excited]` print as text | v3-only feature, we're on v2 | Use `<break>` and ALL CAPS instead |
| `<phoneme>` tag has no effect | Multilingual v2 doesn't support phonemes | Use pronunciation dictionary alias substitution instead |

---

## Validated patterns log

- 2026-04-29: V1 expanded script rendered at speed 0.90 = 10:58 total. Adrian A/B-tested 0.85/0.88/0.90/0.92 — 0.90 selected as sweet spot. **NOT YET using stitching params** (next render run will).
- 2026-04-29: Macca voice locked. Source: research-validated against ElevenLabs official docs + community 2026 patterns.
- *(append validated patterns after each render batch)*

---

## Sources

- [ElevenLabs — Best practices for TTS](https://elevenlabs.io/docs/overview/capabilities/text-to-speech/best-practices)
- [ElevenLabs — Create speech API reference](https://elevenlabs.io/docs/api-reference/text-to-speech/convert)
- [ElevenLabs — How can I add pauses?](https://help.elevenlabs.io/hc/en-us/articles/13416374683665-How-can-I-add-pauses)
- [ElevenLabs — Pauses and SSML phoneme tags with the API](https://help.elevenlabs.io/hc/en-us/articles/24352686926609-Do-pauses-and-SSML-phoneme-tags-work-with-the-API)
- [ElevenLabs — Force a certain pronunciation](https://help.elevenlabs.io/hc/en-us/articles/16712320194577-How-can-I-force-a-certain-pronunciation-of-a-word-or-name)
- [ElevenLabs — Speed control](https://elevenlabs.io/docs/agents-platform/customization/voice/speed-control)
- [ElevenLabs — Pronunciation dictionaries](https://elevenlabs.io/docs/eleven-agents/customization/voice/pronunciation-dictionary)
- [ElevenLabs — Request stitching for TTS API](https://elevenlabs.io/blog/request-stitching-for-text-to-speech-api)
- [ElevenLabs — Latency optimization (deprecated `optimize_streaming_latency`)](https://elevenlabs.io/docs/eleven-api/concepts/latency)
- [ElevenLabs — Text normalization](https://github.com/elevenlabs/elevenlabs-docs/blob/main/fern/docs/pages/best-practices/prompting/normalization.mdx)
- [ElevenLabs — Documentary narrator voices](https://elevenlabs.io/voice-library/documentary-narrator-voices)
- [ElevenLabs — IVC vs PVC](https://help.elevenlabs.io/hc/en-us/articles/13313681788305-What-is-the-difference-between-Instant-Voice-Cloning-IVC-and-Professional-Voice-Cloning-PVC)
- [Webfuse — ElevenLabs Cheat Sheet 2026](https://www.webfuse.com/elevenlabs-cheat-sheet)
