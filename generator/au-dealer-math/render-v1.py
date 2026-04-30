# Render AUDM V1 to 1080p MP4 from the assembled DaVinci timeline.
# RUN INSIDE DaVinci Resolve 20 Py3 Console after build-v1-davinci.py has
# successfully built the timeline AND you've QC'd it on the Edit page.
#
# In the Py3 console, paste this single-line invocation (with raw-string path):
#   __import__("builtins").__dict__["compile"](open(r"C:\dev\Claude\generator\au-dealer-math\render-v1.py").read(), "render-v1.py", "exec")
# Or simpler — open the file, copy contents, paste directly into the Py3 console.
#
# Output: video/out/audm-v1-payment-not-price-pivot.mp4
# Then upload that file to Submagic for captions.

from pathlib import Path

REPO = Path(r"C:\dev\Claude")
OUT_DIR = REPO / "video" / "out"
OUT_DIR.mkdir(parents=True, exist_ok=True)

PROJECT_NAME = "AUDM_V1_PaymentNotPrice"
RENDER_NAME = "audm-v1-payment-not-price-pivot"

print("=" * 60)
print("AUDM V1 - render to 1080p MP4")
print("=" * 60)

if 'resolve' not in dir():
    raise RuntimeError("'resolve' global not found. Run inside DaVinci Resolve Py3 Console.")

pm = resolve.GetProjectManager()
project = pm.GetCurrentProject()
if not project or project.GetName() != PROJECT_NAME:
    project = pm.LoadProject(PROJECT_NAME)
if not project:
    raise RuntimeError(f"Could not load project {PROJECT_NAME}")
print(f"Project: {project.GetName()}")

timeline = project.GetCurrentTimeline()
if not timeline:
    raise RuntimeError("No active timeline")
print(f"Timeline: {timeline.GetName()}")

# Switch to Deliver page (some render presets only resolve there)
resolve.OpenPage("deliver")

# Configure render settings - H.264 1080p 24fps for YouTube
# Submagic accepts standard MP4. No need for ProRes master format.
render_settings = {
    "TargetDir": str(OUT_DIR),
    "CustomName": RENDER_NAME,
    "FormatWidth": 1920,
    "FormatHeight": 1080,
    "FrameRate": "24",
    "VideoFormat": "mp4",
    "VideoCodec": "H.264",
    "AudioCodec": "aac",
    "AudioBitDepth": "16",
    "AudioSampleRate": "48000",
    "ExportVideo": True,
    "ExportAudio": True,
    "MarkIn": timeline.GetStartFrame(),
    "MarkOut": timeline.GetEndFrame(),
}

# Try to load the YouTube preset; not all installs have it. Fall back to direct settings.
loaded_preset = project.LoadRenderPreset("YouTube 1080p")
if not loaded_preset:
    loaded_preset = project.LoadRenderPreset("H.264 Master")
print(f"Render preset loaded: {bool(loaded_preset)}")

ok = project.SetRenderSettings(render_settings)
print(f"Render settings applied: {ok}")

job_id = project.AddRenderJob()
print(f"Render job queued: {job_id}")

print("\nStarting render - this will take 5-15 min for a ~10-min video.")
print("Watch progress in the Deliver page (bottom-right).")
print(f"Output target: {OUT_DIR / (RENDER_NAME + '.mp4')}")
print()

started = project.StartRendering([job_id])
print(f"Rendering started: {started}")
print()
print("When complete:")
print("  1. Verify the MP4 exists at the target path")
print("  2. Upload to Submagic for captions")
print("  3. Download captioned MP4 + upload to YouTube")
