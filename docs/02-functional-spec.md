# Functional specification — MacWan

> Phase 2 artifact, **DRAFT v0.1 (2026-10-06)** written ahead of the Phase 1 gate so development
> can start on the spikes. Becomes binding once José confirms `docs/01-discovery.md` §9. Changes
> after that go through `docs/decisions.md`.

## 1. Users

- **Creator** (primary): non-developer with an Apple Silicon Mac who wants local AI video. Never
  opens Terminal. Needs: clear model sizes, realistic waiting times, safe defaults.
- **Power user**: knows Wan/ComfyUI terms; wants seeds, steps, shift, CFG, LoRAs, schedulers,
  exact resolutions — behind an "Advanced" disclosure, never on the default path.

## 2. Glossary

Task (what the user wants: T2V, I2V…) · Model (a Wan checkpoint) · Variant (format + precision of a
model on disk: `mlx-bf16`, `mlx-q4`, `diffusers-bf16`, `gguf-q5`…) · Engine (MLX, MPS, Cloud) ·
Recipe (every parameter of a render) · Job (a recipe queued for rendering) · Tier (Entry, Standard,
Pro, Studio — from unified memory).

## 3. Flows

### F1 — First launch
1. Welcome → what MacWan does, that models are large and run locally.
2. Hardware check (automatic): chip, unified memory, macOS version, free space on the chosen volume.
   Unsupported → explain; offer cloud engine (when available) or quit.
3. Storage location: default `~/Library/Application Support/MacWan`, option to pick an external
   volume (models can exceed 100 GB).
4. Starter pack proposal by tier (e.g. Entry: TI2V-5B q4 + Wan2.1 1.3B; Standard: TI2V-5B + A14B
   T2V q4), with total download size and estimated disk after conversion. User may change it.
5. Licence acknowledgement (Apache-2.0, acceptable use summary + link).
6. Install: runtime then models, as a resumable checklist with per-item progress. The app is usable
   (browsing, settings) while installing; tasks unlock as their models become ready.
7. Benchmark render (tiny, ~10 s) to calibrate ETAs. Done → Home.

**Acceptance:** AC-01 a fresh Mac with no Python/Homebrew/Xcode reaches a playable first video with
zero Terminal use. AC-02 quitting mid-install and relaunching resumes where it stopped. AC-03 a
failed step shows the cause in plain language and a Retry.

### F2 — Create (every task screen)
Layout: left = inputs (prompt, images/videos/masks, quality preset), centre = preview/player,
right (collapsible) = Advanced (model, variant, resolution, frames/duration, steps, CFG, shift,
scheduler, seed, negative prompt, LoRAs). Primary button **Generate** → creates a Job in the queue.

Per-task inputs:
| Task | Required | Optional |
|---|---|---|
| Text → Video | prompt | negative, seed, size, duration |
| Image → Video | image, prompt (may be empty with assistant) | as above |
| First + Last → Video | first image, last image, prompt | as above |
| Edit & Control (VACE) | prompt + at least one of: reference images, source video, mask, control video | — |
| Video → Video | source video, prompt, strength | — |
| Text → Image | prompt | size |
| Animate / Replace | driving video, character image, mode | relighting LoRA (replace) |

Validation is done in the UI before queueing: frames `4n+1`, size from the model's supported list
(TI2V 1280×704/704×1280 only), TI2V dimensions divisible by 32, duration ↔ frames using the model's
fps (16 for 2.1/A14B, 24 for TI2V). A task whose model is not installed shows "Install <model>
(<size>)" instead of Generate.

**Acceptance:** AC-10 every parameter in Advanced maps 1:1 to an engine parameter recorded in the
recipe. AC-11 an invalid combination cannot be queued and the reason is shown next to the field.

### F3 — Queue
List of jobs: state (queued, loading model, encoding prompt, denoising step n/N, decoding, saving,
done, failed, cancelled), ETA, cancel, reorder, pause queue. One job renders at a time (memory).
macOS notification on done/failed. App can be closed to the menu bar while rendering (menu-bar extra
shows progress). Sleep is prevented while a job runs (`ProcessInfo.beginActivity`).

**Acceptance:** AC-20 cancel stops within one denoising step (or a hard-kill after 10 s) and frees
memory. AC-21 a crash of the worker marks the job failed with the last log lines and restarts the
worker for the next job.

### F4 — Library
Grid of renders with thumbnail, task, model, duration, date; detail view with player, full recipe,
"Generate again", "Use as input" (e.g. last frame → I2V), export (MP4 H.264/HEVC, ProRes 422, PNG
sequence, GIF), reveal in Finder, delete. Recipes are also embedded as metadata in the MP4 (VERIFY
which container fields survive).

### F5 — Models
Catalogue grouped by task, each row: name, version, tasks, tier, size (download / on disk), state
(not installed, downloading %, converting, ready, update available, failed), actions (install,
pause/resume, verify, delete, change variant). Shows total disk used and free space. Shared
components (T5, VAEs) shown once with "used by N models".

### F6 — Runtime & updates
Settings → Engines: state of `uv`, Python, each venv and package versions; Repair; "Check for
updates". App updates via Sparkle; each app version ships its own lockfiles, so runtime packages are
updated by app updates (never silently mid-session). Model updates: compare the catalogue's pinned
HF revision with the remote; offer, never auto-download multi-GB updates.

### F7 — Prompt Assistant (optional)
"Enhance" button next to the prompt → shows the rewritten prompt as a diff the user accepts or
edits. Providers per `docs/research/ai-assistant-cli.md`. "Describe image" for I2V/Animate.

### F8 — Diagnostics
Export a zip with app/worker logs, hardware info, versions, last failed recipe — no media, no
prompts unless the user ticks the box.

## 4. Non-functional requirements

- NFR-01 Apple Silicon only; macOS 14+.
- NFR-02 No network except: model downloads (huggingface.co, modelscope), Sparkle feed, PyPI/GitHub
  for runtime install, and providers the user explicitly enables. No telemetry by default.
- NFR-03 UI never blocks: all engine work in the worker process; UI stays at 60 fps during renders.
- NFR-04 Every long operation is resumable or restartable without corrupting state.
- NFR-05 Accessibility per `docs/01-discovery.md` §7; localization-ready (String Catalogs).
- NFR-06 Secrets (API keys, HF token for gated mirrors) only in the Keychain.

## 5. Out of scope for v1

See `docs/01-discovery.md` §4 "Deferred".
