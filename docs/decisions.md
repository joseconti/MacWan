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

## D-013 — José's setup answers (2026-10-06)
- Date / phase: 2026-10-06 / Phase 2, sprint 1 (S-081)
- Decision: (1) **Test-first policy: `pure-logic`** — recipe validation, catalogue parsing, the JobQueue state machine, both protocol codecs and tier assignment get their test written and seen failing before the code; at every value a bug fix starts from a failing reproduction test and a test derived from an `AC-nn` is never edited to pass. (2) **Forge issues: after-sprint review plus issue capture on**, sweep interval 24 h; Keel comments and never closes an issue on its own reading. (3) **Notify: email to j.conti@joseconti.com** through the Gmail connector, for blocking stops only. (4) **Assistant config: full, for several tools** — which tools besides Claude Code is still to be named by José. (5) **Chaining: `start`, model `opus`** — takes effect once S-014 builds and smoke-tests the launcher; until then every close-out prints the prompt. (6) **Spikes: install `uv` and SwiftLint with Homebrew and download the small models first** (Wan2.1 1.3B, Wan2.2 TI2V-5B); A14B (≈ 126 GB) only after those work.
- Why: José's answers to the batched questions in the project thread.
- Alternatives rejected (and why): the other options offered for each question — José chose these.
- Supersedes: none (settles the questions left open in D-008)

## D-014 — Design system: MacWan founds its own, endorsed "By PackDesk"
- Date / phase: 2026-10-06 / Phase 1 step 9 (answered in sprint 1, S-081)
- Decision: no existing design system applies; MacWan founds one (canonical for the app and its later website). **The parent brand must be shown: "By PackDesk".** José called this very important. Where exactly the endorsement appears (app icon lock-up, About window, onboarding welcome, DMG background, website footer) and whether PackDesk has logo assets and brand rules to respect is asked in S-012, before the design brief is written.
- Why: José's answer.
- Alternatives rejected (and why): applying an existing identity — none exists for MacWan; a one-off design — the system will be reused by the website.
- Supersedes: none

## D-015 — No 16 GB Apple Silicon Mac is available: the Entry tier cannot be measured on real hardware
- Date / phase: 2026-10-06 / Phase 2, sprint 1 (S-081)
- Decision: recorded as a constraint, not yet as a product decision. José has no 16 GB Mac; the only test machine is an M5 with 32 GB. S-001 and S-003 will approximate 16 GB by capping the engines' memory limit on the 32 GB machine, and every Entry-tier figure obtained that way stays marked `VERIFY`. Consequence stated: D-008 sets 16 GB as the minimum supported Mac, and that minimum would ship without ever having run on a real 16 GB machine — a capped 32 GB Mac does not reproduce macOS memory pressure, swap or the GPU wired-memory limit of a 16 GB one.
- Why: José's answer.
- Alternatives (for José, at the Phase 2 gate S-011): keep 16 GB supported but labelled "not verified on real hardware" with a conservative memory guard; raise the minimum to 24 GB; or find an outside tester with a 16 GB Mac before release.
- Supersedes: none (qualifies D-008 item 1)

## D-016 — Spike environment pinned: mlx-video 87db56a, mlx 0.32.3, CPython 3.12
- Date / phase: 2026-10-06 / Phase 2, sprint 1 (S-001, in progress)
- Decision: the sprint 1 spikes run on `mlx-video` at commit `87db56a51758fefb748a359b90a5283bb8ba4837` with `mlx` 0.32.3, `torch` 2.14.1 and CPython 3.12, locked in `spikes/uv.lock`. The real entry points at that commit are `mlx_video.models.wan_2.convert` and `mlx_video.models.wan_2.generate`. Spike models are stored outside the repository, in `~/Library/Caches/MacWan-spikes/`. This is the spike pin, not yet the product pin: the worker's lockfiles are fixed at S-017 from whatever S-001…S-003 conclude.
- Why: upstream has no releases and its README names module paths that do not exist; measurements are only comparable on a fixed commit.
- Alternatives rejected (and why): tracking `main` — numbers would not be reproducible.
- Supersedes: none (implements D-004's "pin SHA")

## D-017 — A memory cap does not simulate a smaller Mac; the tier table is not valid as proposed
- Date / phase: 2026-10-06 / Phase 2, sprint 1 (S-001, in progress)
- Decision: recorded findings, with the product decision left to José at the Phase 2 gate (S-011). (1) `mx.set_memory_limit(10 GB)` did not constrain a render (23–25 GB used), so D-015's approach to Entry-tier figures is withdrawn; no Entry-tier number exists. (2) The measured peak is about 23 GB for loading and running the UMT5-XXL text encoder, on every model including the smallest; denoising TI2V-5B 4-bit needs 4.35 GB. The tier table proposed from transformer sizes is therefore unsupported: with the engine as it is, MacWan needs a 32 GB Mac. (3) Whether 16 GB or 24 GB is reachable depends on a T5-handling change (quantized T5, separate short-lived process, cached embeddings) that S-003 must now test. (4) 4-bit TI2V-5B is visibly broken at 10 steps while bf16 is clean.
- Why: measurements in `docs/research/benchmarks.md`.
- Alternatives: none chosen yet — after S-003, José decides between engineering the T5 path to keep a 16 GB minimum, or raising the minimum.
- Supersedes: the simulation approach in D-015 (its constraint — no 16 GB Mac — stands)

## D-018 — The 23 GB peak is avoidable: MacWan loads T5 itself and chooses the tiling
- Date / phase: 2026-10-06 / Phase 2, sprint 1 (S-001, in progress)
- Decision: corrects the conclusion of D-017 with further measurements (`docs/research/benchmarks.md`). The peak came from two upstream defaults — T5 upcast to float32 (23.7 GB) and an untiled VAE decode (up to 27 GB) — not from the models. With T5 kept in bf16 (11.1 GB, embeddings 0.9998 cosine to the reference) or 8-bit (8.1 GB, 0.998), and aggressive tiling (visually identical, 43–45 dB), Wan2.1 1.3B 4-bit renders in 8.6 GB and TI2V-5B in 9.4–15.6 GB. Consequences for the build: the worker loads the text encoder itself (bf16 by default; a pre-quantized 8-bit file for low-memory Macs; never 4-bit), the memory guard picks the tiling mode, and both are done by replacing `mlx-video` entry points in-process, not by forking it. Quantized TI2V-5B is only offered at 40 steps (clean) — at 10 steps only bf16 is clean.
- Why: measurements on the M5 / 32 GB.
- Alternatives rejected (and why): accepting upstream defaults — would make 32 GB the minimum Mac; 4-bit T5 — embeddings degrade (0.877 cosine).
- Still open (José, at S-011): the 16 GB minimum is now plausible for 1.3B and TI2V-5B 4-bit but cannot be verified without a 16 GB Mac (D-015); `mx.set_memory_limit` does not simulate one (D-017 item 1 stands).
- Supersedes: D-017 items 2 and 3 (the "needs a 32 GB Mac" reading). D-017 items 1 and 4 stand, item 4 refined: the artifacts are a low-step effect of quantization.
