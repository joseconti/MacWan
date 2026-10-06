# Functional specification — MacWan

> Phase 2 artifact, **DRAFT v0.2 (2026-10-06)**. Discovery is confirmed (D-008). This spec becomes
> binding at the Phase 2 gate (slice S-011), after the Sprint 1 spikes replace every `VERIFY` with a
> measurement. Items marked *proposed* are the assistant's defaults awaiting José's confirmation at
> that gate. Changes after the gate go through `docs/decisions.md`.

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
failed step shows the cause in plain language and a Retry. AC-04 an unsupported Mac (Intel, under
16 GB, macOS older than 14) is told why in plain language and is never offered a local task.

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
AC-12 a job whose variant's measured peak memory exceeds this Mac's budget is refused before it
starts, with the reason and a smaller variant suggested.

### F3 — Queue
List of jobs: state (queued, loading model, encoding prompt, denoising step n/N, decoding, saving,
done, failed, cancelled), ETA, cancel, reorder, pause queue. One job renders at a time (memory).
macOS notification on done/failed. App can be closed to the menu bar while rendering (menu-bar extra
shows progress). Sleep is prevented while a job runs (`ProcessInfo.beginActivity`).

**Acceptance:** AC-20 cancel stops within one denoising step (or a hard-kill after 10 s) and frees
memory. AC-21 a crash of the worker marks the job failed with the last log lines and restarts the
worker for the next job. AC-22 queued jobs survive quitting and relaunching the app, and a finished
or failed job raises a macOS notification. AC-23 after the benchmark render every job shows an ETA
derived from this Mac's measured seconds per step.

### F4 — Library
Grid of renders with thumbnail, task, model, duration, date; detail view with player, full recipe,
"Generate again", "Use as input" (e.g. last frame → I2V), export (MP4 H.264/HEVC, ProRes 422, PNG
sequence, GIF), reveal in Finder, delete. Recipes are also embedded as metadata in the MP4 (VERIFY
which container fields survive).

**Acceptance:** AC-30 every render stores its complete recipe, and opening it restores every
parameter exactly. AC-31 "Generate again" queues a job whose recipe is identical, seed included.
AC-32 every export format produces a file that plays, and exporting never modifies the original.

### F5 — Models
Catalogue grouped by task, each row: name, version, tasks, tier, size (download / on disk), state
(not installed, downloading %, converting, ready, update available, failed), actions (install,
pause/resume, verify, delete, change variant). Shows total disk used and free space. Shared
components (T5, VAEs) shown once with "used by N models".

**Acceptance:** AC-40 the disk figures shown match the filesystem within 1 %, with shared
components counted once. AC-41 a download can be paused and resumed, survives a relaunch, and never
re-downloads a file that already completed. AC-42 a file that fails its sha256 check is never used:
the item is marked failed with a Retry. AC-43 originals are deleted only after the converted variant
has verified. AC-44 deleting a model never removes a shared component another installed model uses.

### F6 — Runtime & updates
Settings → Engines: state of `uv`, Python, each venv and package versions; Repair; "Check for
updates". App updates via Sparkle; each app version ships its own lockfiles, so runtime packages are
updated by app updates (never silently mid-session). Model updates: compare the catalogue's pinned
HF revision with the remote; offer, never auto-download multi-GB updates.

**Acceptance:** AC-50 Engines shows the installed version of every runtime component, and Repair
rebuilds a broken environment without touching models or the library. AC-51 runtime packages never
change outside an app update. AC-52 a model update is offered with its size and never downloaded
automatically. AC-53 an app update is installed only when its EdDSA signature verifies.

### F7 — Prompt Assistant (optional)
"Enhance" button next to the prompt → shows the rewritten prompt as a diff the user accepts or
edits. Providers per `docs/research/ai-assistant-cli.md`. "Describe image" for I2V/Animate.

**Acceptance:** AC-60 the assistant is Off by default, and nothing replaces the user's prompt
without an explicit accept. AC-61 a provider that is missing, logged out or timing out produces a
plain-language message and never blocks generation. AC-62 API keys live only in the Keychain and
never appear in logs, diagnostics or recipes.

### F8 — Diagnostics
Export a zip with app/worker logs, hardware info, versions, last failed recipe — no media, no
prompts unless the user ticks the box.

**Acceptance:** AC-70 the exported zip contains no prompt and no media unless the box is ticked,
and no token or key in any case.

## 4. Non-functional requirements

- NFR-01 Apple Silicon only; macOS 14+.
- NFR-02 No network except: model downloads (huggingface.co, modelscope), Sparkle feed, PyPI/GitHub
  for runtime install, and providers the user explicitly enables. No telemetry by default.
- NFR-03 UI never blocks: all engine work in the worker process; UI stays at 60 fps during renders.
- NFR-04 Every long operation is resumable or restartable without corrupting state.
- NFR-05 Accessibility per `docs/01-discovery.md` §7; localization-ready (String Catalogs).
- NFR-06 Secrets (API keys, HF token for gated mirrors) only in the Keychain.

- NFR-07 Every screen meets AC-80 and AC-81 (below).

**Cross-cutting acceptance:** AC-80 every screen and state passes the automated accessibility audit,
is fully operable from the keyboard with a visible focus, exposes name, role and value to VoiceOver,
announces long-operation progress, honours Reduce Motion and Increase Contrast, and never conveys
state by colour alone. AC-81 no user-facing string is hard-coded: every one comes from the String
Catalog, and English, Spanish and Catalan render without truncation.

## 5. Out of scope for v1

See `docs/01-discovery.md` §4 "Deferred" and `docs/sprints/deferred.md`.

## 6. Data model

| Entity | Stored in | Key fields | Rules |
|---|---|---|---|
| ModelDescriptor | `Resources/catalogue.json` (shipped, read-only) | id, family, tasks, source (HF repo + pinned revision, ModelScope), shared components, fps, frame rule, sizes, defaults, variants | schema-versioned; measured fields are `null` until measured, never invented |
| Variant | catalogue | id, engine, download_gb, disk_gb, peak_mem_gb, min_tier | one model has one or more |
| InstalledModel | SwiftData | model id, variant id, state, path, bytes on disk, installed revision, verified at | state ∈ not installed, downloading, converting, ready, update available, failed |
| SharedComponent | SwiftData | id (T5, VAE 2.1, VAE 2.2), path, bytes, used-by list | deleted only when used-by is empty (AC-44) |
| Recipe | `library/<render-id>/recipe.json` + SwiftData | task, model, variant, engine, every generation parameter, LoRAs, seed, app and engine versions | immutable once rendered; schema-versioned |
| Job | SwiftData | id, recipe, state, progress, ETA, timestamps, error code, last log lines | one job in a non-terminal render state at a time |
| Render | SwiftData + `library/<render-id>/` | id, recipe, video path, thumbnail, duration, created at | deleting removes the folder |
| RuntimeState | `runtime/state.json` | uv, Python and package versions per engine, install step reached | written after every completed step (AC-02) |
| Settings | UserDefaults | storage location, idle unload minutes, assistant provider, privacy switches, debug logging | secrets are never here (NFR-06) |

No account, no server-side data, no telemetry. Everything above lives on the user's Mac.

## 7. Integrations

| Service | Used for | Auth | Limits / failure handling |
|---|---|---|---|
| Hugging Face Hub | model downloads at a pinned revision | none (optional token in Keychain for gated mirrors) | resume by range; backoff on 429/5xx; fall back to ModelScope |
| ModelScope | mirror fallback | none | same resume and checksum rules |
| GitHub releases / PyPI | `uv`-driven install of Python and locked packages | none | only during runtime install or Repair; hashes from `uv.lock` |
| Sparkle appcast (host decided before Phase 7) | app updates | EdDSA signature | unsigned or invalid update is rejected (AC-53) |
| Claude Code CLI, Codex CLI (optional) | prompt enhance, caption, translate | the user's own CLI login | fixed arguments, timeout, output treated as data (AC-61) |
| Anthropic / OpenAI APIs (optional) | same | the user's API key in the Keychain | timeout; errors never block generation |

The allow-list of hosts is closed and lives in one place in code (`docs/threat-model.md`).

## 8. Permissions matrix

MacWan is a single-user desktop app: there are no roles. What gates a capability is the Mac and
what is installed.

| Capability | Entry (16 GB) | Standard (24–36 GB) | Pro (48–64 GB) | Studio (96 GB+) |
|---|---|---|---|---|
| T2V Wan2.1 1.3B (480P), TI2V-5B 4-bit short clips, T2I | yes | yes | yes | yes |
| TI2V-5B bf16 / 8-bit at 720P | no | yes | yes | yes |
| T2V, I2V A14B | no | 4-bit | 8-bit | yes |
| FLF2V, VACE 14B | no | no | yes (GGUF) | yes |
| V2V | per S-002 | per S-002 | yes | yes |
| Animate / Replace (experimental) | no | no | yes | yes |

The table is *proposed* (from `docs/research/apple-silicon-runtime.md` §5); S-003 freezes it from measurements.
**Warning (D-017, D-018):** the first measurements replace the reasoning behind it. Upstream defaults
peak at 23–29 GB on every model; with MacWan loading T5 itself and tiling the decode, Wan2.1 1.3B
needs 8.6 GB and TI2V-5B 9.4–15.6 GB (`docs/research/benchmarks.md`). S-003 rewrites this table
from those figures; nothing below 32 GB has been run on real hardware (D-015). A task whose model is not installed
shows "Install" instead of "Generate"; a task above the Mac's tier is shown as unavailable with the
reason, never hidden without explanation.

## 9. Flows index

- [`flows/first-launch.md`](flows/first-launch.md) — F1
- [`flows/create-and-render.md`](flows/create-and-render.md) — F2, F3
- [`flows/model-install.md`](flows/model-install.md) — F5
- [`flows/runtime-repair-and-updates.md`](flows/runtime-repair-and-updates.md) — F6
- [`flows/prompt-assistant.md`](flows/prompt-assistant.md) — F7

F4 (Library) and F8 (Diagnostics) are single-step and need no flow file.

## 10. Technical plan

See `docs/03-technical-plan.md` and `docs/threat-model.md`.

## 11. Design split

**Needs design**

| # | Screen | Template reuse |
|---|---|---|
| 1 | Main window shell — sidebar (Create tasks, Queue, Library, Models, Settings), toolbar | the frame for 3–8 |
| 2 | Onboarding wizard — welcome, hardware check, storage, starter pack, licence, install checklist, benchmark | ONE step template, seven contents |
| 3 | Create task screen — inputs, preview/player, Advanced inspector | ONE template for all seven tasks; only the input block differs |
| 4 | Mask and control input (VACE) | extension of 3 |
| 5 | Queue | list template shared with 7 |
| 6 | Library — grid and detail (player, recipe, actions, export sheet) | — |
| 7 | Models — catalogue list with states and disk summary | list template shared with 5 |
| 8 | Settings — Storage, Engines, Assistant, Privacy, Updates, Diagnostics | ONE form template, six tabs |
| 9 | Prompt-enhance diff sheet | — |
| 10 | Menu-bar extra (progress, pause, open) | — |
| 11 | States for every screen: empty, loading, error, unsupported tier, model not installed | one pattern, reused |
| 12 | App icon, menu-bar icon, document/notification imagery, and the "By PackDesk" parent-brand endorsement (D-014) | SVG + PNG |

**No design:** worker, protocol, engines, runtime manager, model manager, catalogue, queue logic,
persistence, export, build and release scripts.

**External manual setup (José):** Apple Developer ID certificate and notary credentials; Sparkle
EdDSA key pair; the appcast host. All `CREDENTIAL`; walked one step at a time in Phase 4.

**Foreseen external assets:** sample videos and images for the onboarding and the empty states
(must be renders made with MacWan itself or licence-clear material).

**Rich references held by the user:** none recorded.

**Per-screen accessibility requirements:** every screen carries AC-80 in full. In addition: the
player exposes play, pause, scrub and frame step to the keyboard and VoiceOver; the queue and the
install checklist announce state changes; previews never auto-play under Reduce Motion; the mask
editor has a non-pointer alternative (import a mask file); drag-to-reorder has a menu equivalent;
targets are at least 24×24 pt.

**Target window sizes (*proposed*):** minimum 1100×700 pt, designed at 1440×900 pt, verified at
1100×700, 1440×900 and 1920×1200; below 1280 pt wide the Advanced inspector becomes an overlay.
Light and dark appearance, both with Increase Contrast.

## 12. Estimate

See `docs/estimate.md` and the sprint plan in `docs/sprints/` (index: `docs/sprints/README.md`).

## 13. Open questions for the user

Answered on 2026-10-06 (D-013, D-014): test-first policy, design system, issues duty, notification
channel, chaining. Still open — see `docs/PROGRESS.md` open items:

1. Which assistant tools besides Claude Code get the config package.
2. PackDesk assets and where "By PackDesk" appears (the design system is MacWan's own, D-014).
3. The Entry tier without a real 16 GB Mac (D-015), and the other *proposed* items above (tier
   table, window sizes) — confirmed at the Phase 2 gate.
