"""Burn sentence-block captions into an AUDM V[N] master MP4.

Usage:
    python render-vN-captions.py <N>

    <N>  Video number (integer, e.g. 2 for V2, 1 for smoke-test on V1)

Resolves paths automatically from N:
    IN_MP4           video/out/audm-v{N:02d}-*.mp4        (latest non-captioned master)
    TRANSCRIPTIONS   content/au-dealer-math/scripts/v{N:02d}-renders/vo-transcriptions.json
    OUT_MP4          video/out/audm-v{N:02d}-{stem}-captioned.mp4

Caption spec (LOCKED — do not change for V2-V12):
    font      DM Sans Regular, fontsize 38
    colour    cream #F5EFE6 + black stroke borderw=4
    box       NONE (document-forensics aesthetic)
    y         (h*0.82)-text_h/2  (baseline sits at 82% of frame height)
    x         (w-text_w)/2  (horizontally centred)
    2-liners  two separate drawtext filters, symmetric around y=82%

Sentence-chunking rules:
    - Split on terminal punctuation: . ? !  (punctuation is the LAST char of the
      word token, e.g. "budget?")
    - Hard empty-sentence guard: a "sentence" with no words is discarded
    - Soft line-length cap: ~35 chars per line
    - Sentences > 70 chars get split at the nearest comma to the midpoint, or at
      the midpoint word if no comma is present
    - Use timeline_start / timeline_end for all timings

Pipeline position:
    DaVinci export  ->  THIS SCRIPT  ->  swap-vN-music.py  ->  upload
"""

import json
import re
import subprocess
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

REPO = Path(r"C:\dev\Claude")
VIDEO_OUT = REPO / "video" / "out"
CONTENT = REPO / "content" / "au-dealer-math" / "scripts"

FFMPEG = (
    r"C:\Users\adria\AppData\Local\Microsoft\WinGet\Packages"
    r"\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe"
    r"\ffmpeg-8.1-full_build\bin\ffmpeg.exe"
)
FFPROBE = (
    r"C:\Users\adria\AppData\Local\Microsoft\WinGet\Packages"
    r"\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe"
    r"\ffmpeg-8.1-full_build\bin\ffprobe.exe"
)

FONTS_DIR = REPO / "fonts"
DMSANS_REGULAR = FONTS_DIR / "DM_Sans" / "DMSans-Regular.ttf"

FONTSIZE = 38
FONTCOLOR = "#F5EFE6"
BORDERCOLOR = "#000000"
BORDERW = 4
# Y at which the centre of a 1-line caption block sits (82% of frame height)
Y_CENTER_EXPR = "h*0.82"
# Approximate pixels-per-character at fontsize 38 on a 1920-wide frame:
# DM Sans is fairly compact; ~20px/char is a reasonable estimate.
CHARS_PER_LINE = 35
CHARS_SOFT_SPLIT = 70  # sentences longer than this get a 2-line split

# ---------------------------------------------------------------------------
# Path resolution
# ---------------------------------------------------------------------------

def resolve_paths(n: int):
    """Return (in_mp4, transcriptions_json, out_mp4) for video number N."""
    pad = f"{n:02d}"

    # Find the latest non-captioned, non-final master in video/out/
    # Try zero-padded form (v02, v03 ...) first; fall back to bare digit (v1, v2)
    # for backwards compat with V1 which shipped before the naming convention locked.
    candidates = sorted(VIDEO_OUT.glob(f"audm-v{pad}-*.mp4"))
    if not candidates:
        candidates = sorted(VIDEO_OUT.glob(f"audm-v{n}-*.mp4"))
    candidates = [
        p for p in candidates
        if not p.stem.endswith("-captioned")
        and not p.stem.endswith("-final")
    ]
    if not candidates:
        raise FileNotFoundError(
            f"No master MP4 found matching video/out/audm-v{pad}-*.mp4 "
            f"or audm-v{n}-*.mp4\n"
            f"(excluding -captioned and -final variants)"
        )
    in_mp4 = candidates[-1]  # latest by name sort

    transcriptions = CONTENT / f"v{pad}-renders" / "vo-transcriptions.json"
    if not transcriptions.exists():
        raise FileNotFoundError(
            f"Transcriptions not found: {transcriptions}\n"
            f"Generate vo-transcriptions.json for V{n} before running captions."
        )

    out_mp4 = VIDEO_OUT / f"{in_mp4.stem}-captioned.mp4"
    return in_mp4, transcriptions, out_mp4


# ---------------------------------------------------------------------------
# Transcription loading
# ---------------------------------------------------------------------------

def load_words(transcriptions: Path):
    """Return a flat list of word dicts from all scenes, sorted by timeline_start."""
    with transcriptions.open(encoding="utf-8") as f:
        data = json.load(f)

    words = []
    for scene in data["scenes"]:
        for w in scene["words"]:
            words.append({
                "word": w["word"],
                "start": float(w["timeline_start"]),
                "end": float(w["timeline_end"]),
            })
    words.sort(key=lambda w: w["start"])
    return words


# ---------------------------------------------------------------------------
# Sentence chunking
# ---------------------------------------------------------------------------

def is_sentence_end(word_token: str) -> bool:
    """True if this word token ends a sentence (last char is . ? !)"""
    stripped = word_token.rstrip()
    return bool(stripped) and stripped[-1] in ".?!"


def split_long_sentence(words):
    """
    Recursively split a sentence-block whose joined text exceeds CHARS_SOFT_SPLIT
    into N sub-blocks, each fitting comfortably in 2 caption lines (~70 chars).

    Strategy:
    1. If text fits in CHARS_SOFT_SPLIT, return as-is.
    2. Find midpoint char position; locate nearest comma.
    3. Split there (or at midpoint word if no comma in range).
    4. Recurse into each half — guarantees no sub-block exceeds the threshold,
       so wrap_to_lines never has to drop words to stay within 2 lines.
    """
    text = " ".join(w["word"] for w in words)
    if len(text) <= CHARS_SOFT_SPLIT or len(words) <= 1:
        return [words]

    mid_char = len(text) // 2

    # Build cumulative char positions for each word
    positions = []
    pos = 0
    for w in words:
        positions.append(pos)
        pos += len(w["word"]) + 1  # +1 for the space

    # Find nearest comma to midpoint
    best_idx = None
    best_dist = len(text)
    for i, w in enumerate(words):
        if "," in w["word"]:
            dist = abs(positions[i] - mid_char)
            if dist < best_dist:
                best_dist = dist
                best_idx = i

    if best_idx is not None and 0 < best_idx < len(words) - 1:
        split_at = best_idx + 1  # include the comma word in the first chunk
    else:
        # Midpoint by word index
        split_at = max(1, min(len(words) - 1, len(words) // 2))

    first = words[:split_at]
    second = words[split_at:]
    if not first or not second:
        return [words]  # degenerate — can't split, leave as-is
    # RECURSE: keep splitting until every sub-block fits in 2 lines
    return split_long_sentence(first) + split_long_sentence(second)


def chunk_into_sentences(words):
    """
    Group word dicts into sentence-block lists.
    Returns a list of dicts: {words, text, start_t, end_t, lines}.

    'lines' is a list of strings (1 or 2 lines) ready for drawtext.
    """
    sentences = []
    current = []

    for w in words:
        current.append(w)
        if is_sentence_end(w["word"]):
            sentences.append(current)
            current = []

    # Handle trailing words with no terminal punctuation
    if current:
        sentences.append(current)

    # Expand any over-long sentences into 2 sub-blocks
    expanded = []
    for sent in sentences:
        if not sent:
            continue
        sub_blocks = split_long_sentence(sent)
        expanded.extend(sub_blocks)

    # Build final block dicts with line wrapping
    blocks = []
    for words_block in expanded:
        if not words_block:
            continue
        text = " ".join(w["word"] for w in words_block)
        start_t = words_block[0]["start"]
        end_t = words_block[-1]["end"]
        lines = wrap_to_lines(text, CHARS_PER_LINE)
        blocks.append({
            "words": words_block,
            "text": text,
            "start_t": start_t,
            "end_t": end_t,
            "lines": lines,
        })

    return blocks


def wrap_to_lines(text: str, max_chars: int) -> list:
    """
    Wrap text into 1 or 2 lines, each ideally <= max_chars.
    If a single word exceeds max_chars, it stays on its own line.

    Safety net: every word in `text` MUST appear in the output. If wrapping
    produces 3+ lines, lines 2..N are folded into line 2 (which may exceed
    max_chars but never drops words). Upstream caller (split_long_sentence)
    is responsible for keeping sentences short enough that this rarely fires.

    Returns a list of 1 or 2 line strings.
    """
    words = text.split()
    if not words:
        return []

    lines = []
    current_line = []
    current_len = 0

    for w in words:
        needed = len(w) if not current_line else current_len + 1 + len(w)
        if needed <= max_chars or not current_line:
            current_line.append(w)
            current_len = needed
        else:
            lines.append(" ".join(current_line))
            current_line = [w]
            current_len = len(w)

    if current_line:
        lines.append(" ".join(current_line))

    # Safety net: fold any 3rd+ line into line 2 — never drop words.
    if len(lines) > 2:
        lines = [lines[0], " ".join(lines[1:])]

    return lines


# ---------------------------------------------------------------------------
# ffmpeg escape helpers
# ---------------------------------------------------------------------------

def escape_drawtext(text: str) -> str:
    """
    Escape a caption string for use inside a single-quoted ffmpeg drawtext
    text='...' value (in a filter_complex_script file).

    The result is wrapped in single quotes in the filter string: text='<result>'

    Problem: ASCII apostrophes ( ' U+0027 ) inside single-quoted text would
    terminate the ffmpeg single-quote string early (e.g. "what's" → broken).
    Macca VO has many contractions: what's, they've, don't, it's, etc.

    Solution: replace ASCII apostrophe with the Unicode right single quotation
    mark ( ' U+2019 ).  DM Sans renders this identically to a straight apostrophe
    in video captions.  The font supports the glyph.  This character is NOT
    special to ffmpeg's option parser.

    Additional escapes (applied after apostrophe replacement):
      - Colon  :  →  \\:   (ffmpeg option separator — must be escaped)
      - Percent %  →  \\%   (ffmpeg printf format — must be escaped)
      - Backslash \\  →  \\\\  (escape char — must be escaped first if present)

    NOTE: Backslash is escaped first to avoid double-escaping downstream chars.
    """
    t = text
    # 1. Escape backslashes first (avoids double-escaping)
    t = t.replace("\\", "\\\\")
    # 2. Replace ASCII apostrophe with Unicode curly apostrophe (safe in single-quotes)
    t = t.replace("'", "’")   # ' → '
    # 3. Colon → escaped colon
    t = t.replace(":", "\\:")
    # 4. Percent → escaped percent
    t = t.replace("%", "\\%")
    return t


def font_path_arg(font: Path) -> str:
    """Convert Windows font path to ffmpeg-safe format (forward slashes, escaped colon)."""
    return str(font).replace("\\", "/").replace(":", r"\:")


# ---------------------------------------------------------------------------
# Filter chain builder
# ---------------------------------------------------------------------------

def build_filter_chain(blocks: list, font_arg: str) -> str:
    """
    Build a single ffmpeg -filter_complex string that chains all sentence-block
    drawtext filters.

    Each block is a timed caption: enabled only during [start_t, end_t].
    1-line blocks use one drawtext centred at y=(h*0.82)-text_h/2.
    2-line blocks use two drawtext filters with y-offsets symmetric around y=82%.

    The chain is built as:
        [0:v] filter_1 [v1]; [v1] filter_2 [v2]; ... [v{N-1}] filter_N [vout]

    If there are no blocks, returns an empty string (caller skips filter).
    """
    if not blocks:
        return ""

    filters = []
    in_label = "0:v"
    out_label = None

    total = len(blocks)
    for i, blk in enumerate(blocks):
        start_t = blk["start_t"]
        end_t = blk["end_t"]
        enable = f"enable='between(t,{start_t:.4f},{end_t:.4f})'"
        lines = blk["lines"]
        out_label = f"v{i}"

        if len(lines) == 1:
            txt = escape_drawtext(lines[0])
            filt = (
                f"[{in_label}]drawtext="
                f"fontfile='{font_arg}'"
                f":text='{txt}'"
                f":fontsize={FONTSIZE}"
                f":fontcolor={FONTCOLOR}"
                f":bordercolor={BORDERCOLOR}:borderw={BORDERW}"
                f":box=0"
                f":x=(w-text_w)/2"
                f":y=({Y_CENTER_EXPR})-text_h/2"
                f":{enable}"
                f"[{out_label}]"
            )
            filters.append(filt)

        else:
            # Two drawtext filters — line 0 above centre, line 1 below.
            # With fontsize=38, a typical line is ~44px high (38 + leading).
            # We offset each line by half a line height (~22px) from centre.
            # Using arithmetic expressions so it scales to any frame height:
            #   line_h ≈ fontsize * 1.15   (rough leading factor)
            #   line0_y = (h*0.82) - line_h
            #   line1_y = (h*0.82)
            LINE_H_EXPR = f"{FONTSIZE}*1.15"
            txt0 = escape_drawtext(lines[0])
            txt1 = escape_drawtext(lines[1])
            mid_label = f"v{i}a"

            filt0 = (
                f"[{in_label}]drawtext="
                f"fontfile='{font_arg}'"
                f":text='{txt0}'"
                f":fontsize={FONTSIZE}"
                f":fontcolor={FONTCOLOR}"
                f":bordercolor={BORDERCOLOR}:borderw={BORDERW}"
                f":box=0"
                f":x=(w-text_w)/2"
                f":y=({Y_CENTER_EXPR})-{LINE_H_EXPR}"
                f":{enable}"
                f"[{mid_label}]"
            )
            filt1 = (
                f"[{mid_label}]drawtext="
                f"fontfile='{font_arg}'"
                f":text='{txt1}'"
                f":fontsize={FONTSIZE}"
                f":fontcolor={FONTCOLOR}"
                f":bordercolor={BORDERCOLOR}:borderw={BORDERW}"
                f":box=0"
                f":x=(w-text_w)/2"
                f":y=({Y_CENTER_EXPR})"
                f":{enable}"
                f"[{out_label}]"
            )
            filters.append(filt0)
            filters.append(filt1)

        in_label = out_label

    # Rename final output label to 'vout' for clean map reference
    # (Replace the last [vN] label in the last filter with [vout])
    filters[-1] = re.sub(r"\[v\d+a?\]$", "[vout]", filters[-1])

    return ";".join(filters)


# ---------------------------------------------------------------------------
# Render
# ---------------------------------------------------------------------------

def render(in_mp4: Path, out_mp4: Path, filter_chain: str) -> bool:
    """Run ffmpeg. Returns True on success.

    With 200+ caption blocks the filter_complex string easily exceeds Windows'
    32767-char command-line limit.  Write the filter to a temp .txt file and
    pass it via -filter_complex_script instead.
    """
    import tempfile, os

    if filter_chain:
        # Write filter chain to a temp file to avoid Windows MAX_PATH on args
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", delete=False, encoding="utf-8"
        ) as tf:
            tf.write(filter_chain)
            filter_script = tf.name

        try:
            cmd = [
                FFMPEG, "-y", "-loglevel", "error",
                "-i", str(in_mp4),
                "-filter_complex_script", filter_script,
                "-map", "[vout]",
                "-map", "0:a",
                "-c:v", "libx264", "-preset", "medium", "-crf", "20",
                "-pix_fmt", "yuv420p", "-r", "24",
                "-c:a", "copy",
                str(out_mp4),
            ]
            print(f"Running ffmpeg...")
            r = subprocess.run(cmd, capture_output=True, text=True)
        finally:
            try:
                os.unlink(filter_script)
            except OSError:
                pass
    else:
        # No captions (empty transcription) — passthrough
        cmd = [
            FFMPEG, "-y", "-loglevel", "error",
            "-i", str(in_mp4),
            "-c:v", "libx264", "-preset", "medium", "-crf", "20",
            "-pix_fmt", "yuv420p", "-r", "24",
            "-c:a", "copy",
            str(out_mp4),
        ]
        print(f"Running ffmpeg (passthrough - no caption blocks)...")
        r = subprocess.run(cmd, capture_output=True, text=True)

    if r.returncode != 0:
        print(f"[FAIL] ffmpeg exited {r.returncode}")
        print(r.stderr.strip())
        return False
    return True


# ---------------------------------------------------------------------------
# Smoke-test helpers
# ---------------------------------------------------------------------------

def extract_frame(mp4: Path, t: float, label: str) -> Path:
    """Extract a single frame at time t for visual verification."""
    out_png = mp4.parent / f"_verify-captions-{label}.png"
    cmd = [
        FFMPEG, "-y", "-loglevel", "error",
        "-ss", f"{t:.3f}",
        "-i", str(mp4),
        "-frames:v", "1",
        str(out_png),
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode == 0:
        print(f"  Frame at t={t}s -> {out_png.name}")
    else:
        print(f"  Frame extract failed at t={t}: {r.stderr.strip()[:200]}")
    return out_png


def get_duration(mp4: Path) -> float:
    """Return duration in seconds via ffprobe."""
    cmd = [
        FFPROBE, "-v", "error",
        "-select_streams", "v:0",
        "-show_entries", "format=duration",
        "-of", "csv=p=0",
        str(mp4),
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    try:
        return float(r.stdout.strip())
    except ValueError:
        return -1.0


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python render-vN-captions.py <N>")
        print("  e.g. python render-vN-captions.py 2")
        sys.exit(1)

    try:
        n = int(sys.argv[1])
    except ValueError:
        print(f"Error: <N> must be an integer, got: {sys.argv[1]!r}")
        sys.exit(1)

    print("=" * 70)
    print(f"AUDM V{n} - Sentence-block caption renderer")
    print("=" * 70)

    # 1. Resolve paths
    try:
        in_mp4, transcriptions, out_mp4 = resolve_paths(n)
    except FileNotFoundError as e:
        print(f"[ERROR] {e}")
        sys.exit(1)

    print(f"  IN   : {in_mp4.name}")
    print(f"  JSON : {transcriptions}")
    print(f"  OUT  : {out_mp4.name}")
    print()

    # 2. Load words
    words = load_words(transcriptions)
    print(f"  Loaded {len(words)} words from transcriptions")

    # 3. Chunk into sentences
    blocks = chunk_into_sentences(words)
    print(f"  Chunked into {len(blocks)} caption blocks")
    print()

    # 4. Preview first 5 blocks
    print("  First 5 blocks:")
    for blk in blocks[:5]:
        lines_preview = " / ".join(blk["lines"])
        print(f"    [{blk['start_t']:.2f}s-{blk['end_t']:.2f}s] {lines_preview!r}")
    print()

    # 5. Validate font
    if not DMSANS_REGULAR.exists():
        print(f"[ERROR] Font not found: {DMSANS_REGULAR}")
        sys.exit(1)
    font_arg = font_path_arg(DMSANS_REGULAR)

    # 6. Build filter chain
    filter_chain = build_filter_chain(blocks, font_arg)
    if not filter_chain:
        print("[WARN] No caption blocks produced - output will be a passthrough copy.")

    # 7. Render
    print(f"  Rendering captioned output...")
    ok = render(in_mp4, out_mp4, filter_chain)
    if not ok:
        sys.exit(1)

    sz_mb = out_mp4.stat().st_size / (1024 * 1024)
    print(f"  [OK] {out_mp4.name} ({sz_mb:.1f} MB)")
    print()

    # 8. Verify duration
    src_dur = get_duration(in_mp4)
    out_dur = get_duration(out_mp4)
    dur_diff = abs(out_dur - src_dur)
    print(f"  Duration check: source={src_dur:.2f}s  output={out_dur:.2f}s  diff={dur_diff:.3f}s")
    if dur_diff > 1.0:
        print(f"  [WARN] Duration mismatch > 1s - check output carefully.")
    else:
        print(f"  [OK] Duration within tolerance.")
    print()

    # 9. Extract verification frames
    print("  Extracting verification frames...")
    extract_frame(out_mp4, 2.5, "t2.5s")
    extract_frame(out_mp4, 10.0, "t10s")
    print()

    print("=" * 70)
    print(f"Done. Captioned output: {out_mp4}")
    print()
    print("Next steps:")
    print("  1. Open _verify-captions-t2.5s.png  - check caption visible at lower-third")
    print("  2. Open _verify-captions-t10s.png   - check lower-third caption present")
    print("  3. If visual OK, proceed to swap-vN-music.py")
    print("=" * 70)
