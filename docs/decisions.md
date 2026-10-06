# Decisions — MacWan

> Append-only. A session NEVER re-opens a decision recorded here on its own initiative;
> only the user reverses a decision (append the reversal as a new entry).

## D-001 — The project is run with Keel from day one, embedded in the repository
- Date / phase: 2026-10-06 / Phase 1 step 0a
- Decision: MacWan follows the Keel workflow from the start. Keel v6.5.0 (latest release tag of github.com/joseconti/keel-skill at this date) is embedded in both discovery trees, `.claude/skills/keel/` and `.agents/skills/keel/`, and the portability lock is present in `CLAUDE.md` and `AGENTS.md`.
- Why: José asked explicitly to have Keel inside the repository, at its latest version, so any session or assistant opening the repo is bound to it.
- Alternatives rejected (and why): lock only, without the embedded copy — rejected because José asked for Keel inside the repo.
- Supersedes: none

## D-002 — Branch layout for an empty repository
- Date / phase: 2026-10-06 / Phase 1 step 0a
- Decision: `main` receives a minimal initial commit (README + .gitignore); `develop` is created from it as the integration branch; Keel work lands on `develop` through work branches.
- Why: Keel's git flow — `develop` integrates, `main` is the person's.
- Alternatives rejected (and why): committing Keel directly to `main` — contradicts the git flow.
- Supersedes: none

## D-003 — Product: a native macOS app covering every open Wan task
- Date / phase: 2026-10-06 / Phase 1
- Decision: MacWan is a native Swift/SwiftUI app for Apple Silicon (macOS 14+) that installs its own runtime and the Wan models on first launch, keeps them updated, and exposes every open Wan task visually (Wan2.1 + Wan2.2 + Wan-Animate-2; Wan-Dancer excluded while CUDA-only).
- Why: José's request; competitive scan shows only breadth of tasks + zero-Terminal setup differentiates MacWan from Draw Things.
- Alternatives rejected (and why): wrapping the official Gradio demos in a web view — CUDA-only code, not native, poor UX.
- Supersedes: none

## D-004 — Inference engines: MLX primary, PyTorch-MPS (diffusers) secondary, official repos as reference only
- Date / phase: 2026-10-06 / Phase 1 (proposal; to be confirmed by spikes S-001/S-002)
- Decision: run Wan through `mlx-video` (MLX) for T2V/I2V/TI2V and upstream `diffusers` on MPS for FLF2V/VACE/V2V/Animate, both driven by MacWan's own Python worker over a JSON-lines protocol. The official Wan repos are not executed (CUDA-only: flash_attn assert, float64 RoPE, torch.cuda calls); they are the reference for parameters and defaults.
- Why: evidence in docs/research/apple-silicon-runtime.md §2.
- Alternatives rejected (and why): maintaining a patched fork of Wan2.1/2.2 — highest maintenance cost; ComfyUI as a backend — heavy, graph-centric, fp8 pitfalls.
- Supersedes: none

## D-005 — Distribution outside the Mac App Store
- Date / phase: 2026-10-06 / Phase 1 (default, pending José's confirmation — discovery §9 Q2)
- Decision: Developer ID–signed, notarized DMG with Sparkle 2 updates; app sandbox off.
- Why: the App Store sandbox forbids installing a Python runtime and running downloaded executables, which the "app installs everything on first launch" requirement needs.
- Alternatives rejected (and why): App Store — incompatible with the runtime manager.
- Supersedes: none

## D-006 — Claude / ChatGPT CLIs are optional prompt helpers, never the video engine
- Date / phase: 2026-10-06 / Phase 1
- Decision: video generation never depends on an LLM CLI. An optional Prompt Assistant offers providers Off / Local MLX-LM (Qwen) / Claude Code CLI / Codex CLI / API keys for prompt extension, image captioning and translation. Default Off; suggested after the first render.
- Why: Claude and Codex cannot generate video or run Wan; Wan itself recommends LLM prompt extension (docs/research/ai-assistant-cli.md).
- Alternatives rejected (and why): requiring a CLI — adds an account dependency without enabling video.
- Supersedes: none

## D-007 — Documentation in English
- Date / phase: 2026-10-06 / Phase 1 §6
- Decision: all docs/ and product base language in English; conversation with José in Spanish.
- Why: José's explicit request; Keel token-economy default.
- Alternatives rejected (and why): Spanish docs — José asked for English.
- Supersedes: none

## D-008 — Phase 1 answers: all recommended defaults accepted
- Date / phase: 2026-10-06 / Phase 1 close
- Decision: José answered "todo correcto" to docs/01-discovery.md §9, accepting every default: (1) minimum Mac Apple Silicon with 16 GB, macOS 14; (2) Developer ID notarized DMG + Sparkle, outside the App Store (confirms D-005); (3) MacWan's own licence decided later, before Phase 7; (4) cloud engine in v1.x, not v1; (5) locales EN, ES, CA; (6) product website later (Phase 8 = yes); (7) Keel automatic mode on. No notification channel was named; client budget: no.
- Why: José's explicit confirmation in the project thread.
- Alternatives rejected (and why): see docs/01-discovery.md §9 options.
- Supersedes: none (confirms D-005)

## D-009 — Sprint plan v1: 73 slices in sprints 0–9; design runs in parallel with the foundations
- Date / phase: 2026-10-06 / Phase 2 (sprint 1, S-009)
- Decision: every unit of work to v1.0 is a slice in `docs/sprints/` (160 h of AI working time plus supervision, contingency excluded). Sprint 1 also carries the Keel foundation, the Phase 2 close and the Phase 3 design brief (S-007…S-012). Sprint 2 builds only what needs no design (skeleton, runtime, worker, protocol) so it runs while Design works on the brief; the Phase 4 handoff audit (S-022) opens sprint 3. v1.x features and the product website live in `docs/sprints/deferred.md` (S-073…S-080), outside the total. The plan is preliminary until the Phase 2 gate (S-011): spike outcomes may move, resize or drop slices, each change recorded here.
- Why: Keel requires every piece of work to be in the plan with its hours before it starts; José asked for the sprints explicitly.
- Alternatives rejected (and why): planning only the next sprint — leaves "what is left and how long" unanswerable; waiting for Design before any code — idles sprint 2 work that does not depend on design.
- Supersedes: none (extends the nine-row table of estimate v1)

## D-010 — Security audit: optional (derived, not asked)
- Date / phase: 2026-10-06 / Phase 2 step 4c
- Decision: the card's `Security audit:` line is `optional`. Derived from `docs/threat-model.md` §4: no money moves, the app collects and transmits no personal data, and no programmatic surface is reachable from outside (the worker speaks over stdio to its parent). An audit is still offered at S-068 because of the supply-chain surface.
- Why: Keel derives this line from the threat model; it is recomputed whenever the threat model changes — the deferred cloud engine (S-075) or agent/MCP control (S-079) would flip it to `required`.
- Alternatives rejected (and why): `required` — none of the three criteria holds today.
- Supersedes: none

## D-011 — Keel project scripts are Python 3, standard library only
- Date / phase: 2026-10-06 / Phase 1 step 0a (completed in sprint 1, S-007)
- Decision: `scripts/keel-time`, `scripts/keel-plan` and `scripts/keel-verify` (sharing `scripts/_keel_plan.py`) are written in Python 3 with no third-party package. `scripts/keel-plan` is the single generator of `docs/.keel/plan.json` and `docs/sprints/README.md`.
- Why: the scripts parse YAML frontmatter and do decimal arithmetic on hours, which plain shell does badly; Python 3 is present on every development Mac with Xcode. One shared module means the plan is computed by one implementation.
- Alternatives rejected (and why): POSIX shell with awk — fragile for the frontmatter and the projection maths; a YAML library — a dependency for a closed, tiny schema.
- Supersedes: none

## D-012 — Machine-local automatic mode written for this checkout
- Date / phase: 2026-10-06 / session-start setup
- Decision: `.claude/settings.local.json` (gitignored) was created on José's Mac with `permissions.defaultMode: auto`, Keel's forge allow-list, its minimal deny block and an absolute `env.PATH`, implementing the automatic mode recorded in D-008. No committed permission file was written.
- Why: D-008 recorded automatic mode; the file is per machine, so a fresh checkout has none.
- Alternatives rejected (and why): per-session `--permission-mode auto` — has to be repeated every session.
- Supersedes: none
