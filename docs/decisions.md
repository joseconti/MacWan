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
