# AUDM V2 — DaVinci Resolve render script.
# Configures Deliver-page render settings, adds the timeline to the render
# queue, starts rendering, and polls until complete.
#
# Run AFTER build-v2-davinci.py has assembled the timeline. Inside DaVinci
# Resolve 20 Py3 Console, paste the standard one-line invocation pattern
# pointing at this file.
#
# 2026-04-30 fix: removed MarkIn/MarkOut=-1 keys (they made DaVinci render a
# single frame, producing 0.1MB output). Now relies on preset default of
# "Entire Timeline" range + explicit clear of any timeline in/out marks.

import time
from pathlib import Path

PROJECT_NAME = "AUDM_V2_FinanceManagersOffice"
TIMELINE_NAME = "V2_main"

OUT_DIR = Path(r"C:\dev\Claude\video\out")
OUT_NAME = "audm-v2-finance-managers-office"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Just use YouTube 1080p preset + override filename/location/range.
# MarkIn=0, MarkOut=end_frame is REQUIRED — preset default of 0/0 = 1-frame render.
# Empirically: explicit SetRenderSettings dict gets rejected on DaVinci 20
# (likely EncodingProfile / AudioCodec key names differ), so we go preset-only.

print("=" * 60)
print("AUDM V2 - DaVinci render (full timeline)")
print("=" * 60)

if 'resolve' not in dir():
    raise RuntimeError("'resolve' global not found. Run inside DaVinci Resolve Py3 Console.")

pm = resolve.GetProjectManager()
project = pm.GetCurrentProject() or pm.LoadProject(PROJECT_NAME)
if not project:
    raise RuntimeError(f"Could not load project {PROJECT_NAME}")
print(f"Project: {project.GetName()}")

# Find + activate the V2 timeline
timeline = project.GetCurrentTimeline()
if not timeline or timeline.GetName() != TIMELINE_NAME:
    for i in range(1, project.GetTimelineCount() + 1):
        tl = project.GetTimelineByIndex(i)
        if tl and tl.GetName() == TIMELINE_NAME:
            project.SetCurrentTimeline(tl)
            timeline = tl
            break
if not timeline:
    raise RuntimeError(f"Timeline '{TIMELINE_NAME}' not found. Run build script first.")

start_f = timeline.GetStartFrame()
end_f = timeline.GetEndFrame()
total_frames = end_f - start_f
print(f"Timeline: {timeline.GetName()}  (frames {start_f} -> {end_f}, {total_frames}f = {total_frames/24:.2f}s)")

if total_frames < 100:
    raise RuntimeError(f"Timeline has only {total_frames} frames — re-run build script first")

# Switch to Deliver page
resolve.OpenPage("deliver")

# Clear any stale render jobs from prior runs (including the broken 0.1MB one)
existing_jobs = project.GetRenderJobList() or []
for job in existing_jobs:
    jid = job.get("JobId") if isinstance(job, dict) else None
    if jid:
        project.DeleteRenderJob(jid)
if existing_jobs:
    print(f"Cleared {len(existing_jobs)} stale render job(s)")

# Wipe any prior broken output files at the same path so we know the
# new file is fresh (DaVinci will auto-suffix if it sees an existing name).
for ext in (".mp4", ".mov", ".mkv"):
    f = OUT_DIR / f"{OUT_NAME}{ext}"
    if f.exists():
        try:
            f.unlink()
            print(f"Removed prior output: {f.name}")
        except Exception as e:
            print(f"[warn] could not remove {f}: {e}")

# Clear timeline in/out marks (these would constrain the render range).
# DaVinci Resolve API uses MarkIn/MarkOut on the clip object, but for
# timeline render scope, the best signal is omitting MarkIn/MarkOut from
# the render-settings dict entirely. Done above.

# Load YouTube 1080p preset (encoder settings baked in: H.264 / 1080p / 24fps
# / MP4 / AAC). Then override filename + location + RENDER RANGE to the
# entire timeline. The preset defaults MarkIn=MarkOut=0 = 1-frame render.
if not project.LoadRenderPreset("YouTube - 1080p"):
    raise RuntimeError("Could not load YouTube - 1080p preset.")
print("Loaded preset: YouTube - 1080p")

override = {
    "TargetDir": str(OUT_DIR),
    "CustomName": OUT_NAME,
    "MarkIn": int(start_f),
    "MarkOut": int(end_f - 1),  # exclusive end; -1 to land on last real frame
}
if not project.SetRenderSettings(override):
    raise RuntimeError(f"Could not override settings: {override}")
print(f"Override applied: dir={OUT_DIR.name}, name={OUT_NAME}, "
      f"MarkIn={start_f}, MarkOut={end_f - 1}")

# Add timeline as render job
job_id = project.AddRenderJob()
if not job_id:
    raise RuntimeError("AddRenderJob returned empty — check render settings.")
print(f"Job added: {job_id}")

# Sanity-check: read the job back to verify range is the full timeline
jobs = project.GetRenderJobList() or []
my_job = next((j for j in jobs if j.get("JobId") == job_id), None)
if my_job:
    mi = my_job.get("MarkIn", "?")
    mo = my_job.get("MarkOut", "?")
    print(f"Job range: MarkIn={mi}, MarkOut={mo}  (expect full timeline)")

# Start rendering
print("\nStarting render...")
try:
    started = project.StartRendering([job_id])
except TypeError:
    started = project.StartRendering()
print(f"StartRendering: {'OK' if started else 'FAIL'}")

# Poll until done
poll_interval = 5
elapsed = 0
last_pct = -1
print(f"\nPolling every {poll_interval}s...")
while project.IsRenderingInProgress():
    status = project.GetRenderJobStatus(job_id) or {}
    pct = status.get("CompletionPercentage", 0)
    job_status = status.get("JobStatus", "Rendering")
    if pct != last_pct:
        print(f"  [{elapsed:>4d}s] {job_status} - {pct}%")
        last_pct = pct
    time.sleep(poll_interval)
    elapsed += poll_interval

# Final status
final = project.GetRenderJobStatus(job_id) or {}
fs = final.get('JobStatus', 'Unknown')
fpct = final.get('CompletionPercentage', 0)
print(f"\nFinal: {fs} - {fpct}%")

# Verify output
out_path = OUT_DIR / f"{OUT_NAME}.mp4"
if out_path.exists():
    sz_mb = out_path.stat().st_size / (1024 * 1024)
    if sz_mb < 50:
        print(f"\n[WARN] Output is only {sz_mb:.1f} MB — likely empty render.")
        print(f"       Check timeline in/out marks (press Alt+X in Edit page to clear), then re-run.")
    else:
        print(f"\n[OK] Output: {out_path}")
        print(f"     Size: {sz_mb:.1f} MB")
else:
    matches = [m for m in OUT_DIR.glob(f"{OUT_NAME}*")
               if m.suffix.lower() in (".mp4", ".mov", ".mkv")]
    if matches:
        latest = max(matches, key=lambda p: p.stat().st_mtime)
        sz_mb = latest.stat().st_size / (1024 * 1024)
        print(f"\n[OK] Output: {latest}  ({sz_mb:.1f} MB)")
    else:
        print(f"\n[FAIL] No output found at {out_path}")

print("\n" + "=" * 60)
print("RENDER COMPLETE")
print("=" * 60)
