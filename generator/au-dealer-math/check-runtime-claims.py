"""check-runtime-claims.py — Pre-render runtime-claim verifier for AU Dealer Math V[N] scripts.

Usage:
    python check-runtime-claims.py N [--script-only]

    N            : Video number (2 for V2, 1 for V1)
    --script-only: Force word-count estimation even if master-vo.mp3 exists

Exits:
    0 = all claims pass OR no claims found
    1 = at least one claim outside ±15s tolerance (block render)
    2 = error (script not found, ambiguous file match, bad args)

Why this exists:
    V1 shipped with Mac saying "In the next eight minutes, I'll show you..."
    but master-vo.mp3 is 587.18s (9:47). 107s over. Caught post-render.
    V2-V12 must catch this BEFORE render begins.

Calibration (V1, locked 2026-05-03):
    Spoken word count (blockquote lines only, markdown stripped): 1681
    Actual master-vo.mp3 duration:                                587.18s
    Calibrated rate:                                              2.8628 wps
    Source word count method: extract lines starting with '>',
      strip '>' prefix, strip markdown (*...*), split on whitespace.
"""

import re
import subprocess
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
REPO = Path(r"C:\dev\Claude")
SCRIPTS_DIR = REPO / "content" / "au-dealer-math" / "scripts"

FFPROBE = (
    r"C:\Users\adria\AppData\Local\Microsoft\WinGet\Packages"
    r"\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe"
    r"\ffmpeg-8.1-full_build\bin\ffprobe.exe"
)

# ---------------------------------------------------------------------------
# Calibration constant (V1 — recompute when more videos are available)
# 1681 blockquote words / 587.18s actual VO = 2.8628 wps
# ---------------------------------------------------------------------------
WORDS_PER_SECOND = 1681 / 587.18   # ≈ 2.8628

# Tolerance: ±15 seconds
TOLERANCE_S = 15.0

# Keywords that, when appearing ANYWHERE in the stem's suffix-part, mark a
# production/metadata file rather than the canonical script.
EXCLUDE_KEYWORDS = {
    "banner", "kling", "midjourney", "mj-rebuild", "production-master",
    "shorts-metadata", "storyboard", "thumbnail", "youtube-metadata",
    "channel-trailer", "voice-actor", "metadata",
}

# ---------------------------------------------------------------------------
# Number-word lookup (0-30)
# ---------------------------------------------------------------------------
WORD_TO_INT = {
    "zero": 0, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
    "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
    "eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14,
    "fifteen": 15, "sixteen": 16, "seventeen": 17, "eighteen": 18,
    "nineteen": 19, "twenty": 20, "twenty-one": 21, "twenty-two": 22,
    "twenty-three": 23, "twenty-four": 24, "twenty-five": 25,
    "twenty-six": 26, "twenty-seven": 27, "twenty-eight": 28,
    "twenty-nine": 29, "thirty": 30,
    # Space-separated forms (normalised → hyphenated before lookup)
    "twenty one": 21, "twenty two": 22, "twenty three": 23,
    "twenty four": 24, "twenty five": 25, "twenty six": 26,
    "twenty seven": 27, "twenty eight": 28, "twenty nine": 29,
}

# Regex: match "NUMBER minutes" or "NUMBER-minute" or "NUMBER seconds"
# NUMBER is either a digit (1-30) or a word/hyphenated-word form
_DIGIT_PAT = r"(?:[1-9]|[12]\d|30)"
_WORD_PAT  = (
    r"(?:zero|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|"
    r"thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|thirty|"
    r"twenty[- ](?:one|two|three|four|five|six|seven|eight|nine)|twenty)"
)
_NUM_PAT = rf"({_DIGIT_PAT}|{_WORD_PAT})"

CLAIM_RE = re.compile(
    rf"(?:"
    rf"(?:over\s+the\s+next|in\s+the\s+next|the\s+next|next|in)\s+{_NUM_PAT}[\s-]minute"
    rf"|the\s+{_NUM_PAT}[\s-]minute"
    rf"|{_NUM_PAT}[\s-]minute"
    rf"|{_NUM_PAT}\s+second"
    rf")",
    re.IGNORECASE,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def parse_number(s: str) -> int:
    """Convert digit-string or word-form to int. Returns -1 on failure.

    Space-separated compounds ("twenty one") are normalised to their
    hyphenated form ("twenty-one") before the dict lookup so WORD_TO_INT
    only needs to carry the canonical hyphenated keys.
    """
    s = s.strip().lower()
    if s.isdigit():
        return int(s)
    # Normalise space-separated compound numbers → hyphenated form
    normalised = s.replace(" ", "-")
    return WORD_TO_INT.get(normalised, WORD_TO_INT.get(s, -1))


def find_script(n: int) -> Path:
    """Find the canonical script file for video N.

    Returns the single matching Path or raises SystemExit(2) on ambiguity/miss.
    """
    prefix = f"v{n:02d}-"
    candidates = []
    for p in SCRIPTS_DIR.glob(f"{prefix}*.md"):
        # Must be directly under SCRIPTS_DIR (not inside a renders/ subdir)
        if p.parent != SCRIPTS_DIR:
            continue
        # Strip the prefix to get the suffix portion
        suffix_part = p.stem[len(prefix):]  # e.g. "payment-not-price-pivot"
        # Exclude if any production keyword appears in the suffix part
        excluded = any(kw in suffix_part for kw in EXCLUDE_KEYWORDS)
        if not excluded:
            candidates.append(p)

    if len(candidates) == 0:
        print(f"Error: no canonical script found for V{n:02d} in {SCRIPTS_DIR}")
        print(f"  Looked for: {prefix}*.md (excluding production notes)")
        sys.exit(2)
    if len(candidates) > 1:
        print(f"Error: ambiguous script match for V{n:02d} — found multiple candidates:")
        for c in candidates:
            print(f"  {c}")
        print("Please rename or remove the extras.")
        sys.exit(2)
    return candidates[0]


def count_spoken_words(text: str) -> int:
    """Count words in spoken (blockquote) lines only.

    Spoken lines start with '>' in Markdown. This matches what
    regenerate-vo.js feeds to ElevenLabs.
    """
    spoken_parts = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith(">"):
            spoken = stripped.lstrip(">").strip()
            if spoken:
                # Strip markdown emphasis markers
                spoken = re.sub(r"\*+", "", spoken)
                # Collapse non-ASCII (smart-quotes, em-dashes become spaces)
                spoken = re.sub(r"[^\x00-\x7F]+", " ", spoken)
                spoken_parts.append(spoken)
    return len(" ".join(spoken_parts).split())


def extract_claims(text: str):
    """Scan SPOKEN (blockquote) lines of the script for runtime claims.

    Only blockquote lines (starting with '>') are scanned — these are the
    lines Mac actually speaks, and therefore the only place a runtime claim
    would appear. Production-note lines, section headings, and italic stage
    directions are excluded.

    Returns list of (line_number, line_text, claimed_seconds) tuples.
    Line numbers are 1-based (matching the source file).
    """
    results = []
    lines = text.splitlines()
    for i, line in enumerate(lines, start=1):
        stripped = line.strip()
        if not stripped.startswith(">"):
            continue  # Skip non-spoken lines

        for m in CLAIM_RE.finditer(stripped):
            # The regex has up to 3 capture groups; find the first non-None
            num_str = next((g for g in m.groups() if g is not None), None)
            if num_str is None:
                continue
            n = parse_number(num_str)
            if n <= 0:
                continue

            full_match = m.group(0).lower()
            # Determine unit: seconds if "second" in match, else minutes
            if "second" in full_match:
                claimed_s = float(n)
            else:
                claimed_s = float(n) * 60.0

            results.append((i, stripped, claimed_s))

    return results


def get_vo_duration_ffprobe(mp3_path: Path) -> float:
    """Return duration of an MP3 via ffprobe (seconds, float)."""
    cmd = [
        FFPROBE, "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(mp3_path),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: ffprobe failed: {result.stderr.strip()}")
        sys.exit(2)
    return float(result.stdout.strip())


def fmt_duration(s: float) -> str:
    """Format seconds as M:SS string."""
    mins = int(s) // 60
    secs = s - mins * 60
    return f"{mins}:{secs:05.2f}"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help"):
        print(__doc__)
        sys.exit(0)

    try:
        n = int(args[0])
    except ValueError:
        print(f"Error: V-number must be an integer, got: {args[0]!r}")
        sys.exit(2)

    force_script_only = "--script-only" in args

    script_path = find_script(n)
    script_text = script_path.read_text(encoding="utf-8", errors="replace")

    # Determine VO duration
    vo_path = SCRIPTS_DIR / f"v{n:02d}-renders" / "voice" / "master-vo.mp3"
    use_ffprobe = (not force_script_only) and vo_path.exists()

    if use_ffprobe:
        mode = "post-render (master-vo.mp3 exists)"
        actual_s = get_vo_duration_ffprobe(vo_path)
        duration_label = f"Actual VO duration: {actual_s:.2f}s ({fmt_duration(actual_s)})"
    else:
        mode_note = "master-vo.mp3 not found" if not vo_path.exists() else "--script-only flag"
        mode = f"script-only ({mode_note})"
        word_count = count_spoken_words(script_text)
        actual_s = word_count / WORDS_PER_SECOND
        duration_label = (
            f"Estimated VO duration: {actual_s:.0f}s ({actual_s / 60:.2f} min) "
            f"from {word_count} words at {WORDS_PER_SECOND:.2f} wps"
        )

    # Print header
    print(f"Script: {script_path}")
    print(f"Mode:   {mode}")
    print(f"{duration_label}")
    print()

    # Scan for claims
    claims = extract_claims(script_text)

    if not claims:
        print("No runtime claims found in script.")
        print("Recommendation: keep script generic (\"for the rest of this video\",")
        print("  \"from here on\") — can't be wrong.")
        sys.exit(0)

    print(f"Found {len(claims)} runtime claim{'s' if len(claims) != 1 else ''}:")
    fails = 0
    passes = 0
    for (lineno, line_text, claimed_s) in claims:
        diff = actual_s - claimed_s
        status_ok = abs(diff) <= TOLERANCE_S
        status_str = "[OK]  Within ±15s tolerance" if status_ok else "[FAIL] Outside ±15s tolerance"
        if status_ok:
            passes += 1
        else:
            fails += 1

        # Truncate line for display
        display = line_text if len(line_text) <= 80 else line_text[:77] + "..."
        claimed_min = claimed_s / 60.0
        print(f"  Line {lineno}: \"{display}\"")
        print(f"    Claimed:   {claimed_min:.0f} minute{'s' if claimed_min != 1 else ''} ({claimed_s:.1f}s)")
        print(f"    {'Actual' if use_ffprobe else 'Estimated'}:  {actual_s:.2f}s")
        print(f"    Diff:      {diff:+.2f}s")
        print(f"    Status:    {status_str}")
        print()

    print(f"Result: {fails} fail / {passes} pass")
    sys.exit(0 if fails == 0 else 1)


if __name__ == "__main__":
    main()
