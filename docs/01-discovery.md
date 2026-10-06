# Discovery — MacWan

> Phase 1. Status: **confirmed by José 2026-10-06** — every §9 default accepted (D-008).
> Research inputs: `docs/research/wan-video-ecosystem.md`, `docs/research/apple-silicon-runtime.md`,
> `docs/research/ai-assistant-cli.md`, `docs/00-competitive-landscape.md`.

## 1. The idea (José's words, summarised)

A native macOS app that gives a visual UI to everything in `github.com/Wan-Video`. The user installs
the app; on first launch the app installs everything it needs and keeps it updated; afterwards
everything is done visually. If the app needs to download models, it does. Development will be done
by Claude Code, so these docs must contain everything needed to build it without re-researching.

## 2. One-line purpose

**MacWan is the complete, zero-Terminal Wan video studio for Apple Silicon Macs: install the app,
pick a task, get a video — with the right model for your Mac chosen and installed for you.**

## 3. Project type and platform

- Type: **native desktop application** (not one of Keel's web/WordPress/MCP/library types —
  closest security profile: `web-app` + desktop specifics; see technical plan §7).
- Platform: **macOS 14 Sonoma or later, Apple Silicon (M1 or later) only.** Intel Macs and < 16 GB
  machines get the cloud engine only (if enabled) — local Wan is not viable there.
- UI: Swift 6 + SwiftUI. Inference: managed Python runtime with MLX and PyTorch-MPS engines.
- Distribution: **Developer ID–signed, notarized DMG with Sparkle auto-update**, not the Mac App
  Store (the sandbox forbids installing and running a Python runtime and downloaded executables).

## 4. Proposed v1 (the assistant proposes, José reacts)

**Onboarding & runtime**
1. First-launch wizard: hardware probe (chip, unified memory, free disk), tier assignment, licence
   notice (Apache-2.0 models, acceptable use), choice of starter model pack sized to the Mac.
2. Runtime manager: installs `uv` → standalone Python → locked venvs per engine → engine packages;
   verifies, repairs, updates; never touches system Python/Homebrew.
3. Model manager: catalogue of every supported Wan model with size, tier, task; download (HF, with
   ModelScope mirror fallback), resume, checksum, convert to MLX / quantize, delete originals,
   dedupe shared T5/VAE, show disk usage; update notices when upstream revisions change.

**Creation (each is a task screen with simple and advanced modes)**
4. Text → Video (Wan2.2 A14B / TI2V-5B / Wan2.1 1.3B by tier).
5. Image → Video (Wan2.2 A14B / TI2V-5B).
6. First + Last frame → Video (Wan2.1 FLF2V) — Pro tier.
7. Edit & Control / VACE (reference images, mask inpaint/outpaint, pose/depth guide) — Pro tier.
8. Video → Video restyle (Wan2.1 V2V).
9. Text → Image (single-frame Wan).
10. Character Animate / Replace (Wan2.2 Animate) — **experimental**, shown only on Pro/Studio tiers.

**Workflow**
11. Render queue with progress, ETA (from measured speed), cancel, re-run with same seed, background
    rendering with a notification on completion.
12. Library: every render with its full recipe (model, prompt, negative, seed, steps, size, LoRAs),
    thumbnails, playback, export (MP4/H.264, HEVC, ProRes, PNG sequence, GIF), "open recipe".
13. Quality presets: **Draft** (Lightning LoRA, 4–10 steps, 480P), **Standard**, **High**.
14. Optional Prompt Assistant (Off / Local MLX-LM / Claude CLI / Codex CLI / API key).
15. Settings: storage location (external SSD supported), engines, updates, privacy, diagnostics export.

**Deferred (v1.x, recorded so they are decisions, not omissions)**
- Speech → Video (Wan2.2 S2V) — no Mac-capable pipeline exists yet; needs a port or an upstream diffusers pipeline.
- Wan-Animate-2 — waiting for diffusers support (PR #14412) and RAM validation.
- Cloud engine (Alibaba Model Studio: Wan 2.5–3.0).
- LoRA training; Wan-Dancer (CUDA-only); multi-shot storyboard; agent/MCP control of the app.

## 5. Constraints and risks (honest)

| Risk | Severity | Mitigation |
|---|---|---|
| Wan is heavy; renders on Mac take minutes to tens of minutes | High (UX) | Draft preset, measured ETAs, queue + background + notifications |
| Disk: originals 34–126 GB per model | High | convert-then-delete, shared T5/VAE, external storage, clear pre-download sizing |
| Community engine (`mlx-video`) has no releases, one main maintainer | High | pin SHA; engine abstraction so the MPS/diffusers engine can replace it; contribute fixes upstream |
| MPS gaps (ops falling back to CPU, Animate preprocessing deps) | Medium | spikes before committing to a task; experimental flag |
| Upstream churn (diffusers, torch, mlx) | Medium | lockfiles shipped per app version; runtime updates only with app updates |
| Draw Things already covers T2V/I2V | Medium (market) | breadth of tasks + workflow (queue, library, recipes) |
| Notarization with a bundled Python toolchain | Medium | Python is installed at runtime into Application Support, not inside the bundle; only `uv` + worker sources are bundled and signed |

## 6. Internationalization and docs language

- Product base language **English**; built localization-ready from line one (String Catalogs,
  `.xcstrings`). Shipped locales v1: **English, Spanish, Catalan** (D-008).
- Prompts can be typed in any language; the assistant can translate to EN/ZH.
- `docs/` in **English** (Keel token-economy default, José's explicit request). Conversation in Spanish.

## 7. Accessibility (non-negotiable, from line one)

Full VoiceOver support for every control, including the timeline/player and the queue; Dynamic Type
-equivalent text scaling where macOS allows; keyboard-only operation; Reduce Motion respected (no
auto-playing previews when set); Increase Contrast; meaningful progress announcements
(`AccessibilityNotification.Announcement`) for long renders. Target: Apple accessibility API fully,
WCAG 2.2 AA principles applied to the native UI.

## 8. Website intent and budget

- Website (Keel Phase 8): **yes**, product site at a later date (D-008).
- Client budget: **no** — José's own product (D-008).

## 9. Questions put to José — all defaults accepted 2026-10-06 (D-008)

1. Minimum Mac: Apple Silicon + **16 GB**, macOS 14? *(default yes)*
2. Distribution: Developer ID DMG + Sparkle, not App Store? *(default yes)*
3. Licence of MacWan itself: GPL-3.0-or-later, proprietary, or freemium? *(default: decide before
   Phase 7; does not block development)*
4. Include the optional cloud engine in v1, or v1.x? *(default v1.x)*
5. Locales: EN + ES + CA? *(default yes)*
6. Product website later (Phase 8)? *(default yes)*
7. Keel session setup: automatic mode, forge-issue duty, issue capture, notification channel.

## 10. Environment & test drivers (step 5a preflight — 2026-10-06)

- This session can run commands where the repo lives: **yes** (Claude Code on José's Mac, in
  `/Users/joseconti/Documents/GitHub/MacWan`).
- Environment restrictions found: none — network, file deletion and local execution all work.
- `claude` on PATH: yes (`/Users/joseconti/.local/bin/claude`). Chaining itself is still unasked.
- Machines in play: one — José's Mac is the development machine, the repo host and the test runner.
- Present on the test machine: Apple M5, 32 GB unified memory, macOS 27.0.1, 605 GB free; Xcode 27.0
  (27A266a); XcodeGen; Python 3 (Homebrew); GitHub CLI.
- Missing or too old: `uv`, SwiftLint, gitleaks (optional). Nothing was installed at this step;
  install paths are in `docs/03-technical-plan.md` §13 and are asked before running.
- Impossible on this machine: Entry-tier (16 GB) measurements — it has 32 GB. Way around: a second
  16 GB Apple Silicon Mac, or the Entry rows stay `VERIFY` with a conservative memory guard.
- Screen-stealing verdict: Swift and Python unit tests and the worker protocol run headless;
  **XCUITest takes the screen.** Mitigation proposed: a dedicated macOS user session or scheduled
  batches José starts (technical plan §12) — to be agreed before the first UI test (S-039).
- Licence or privilege consequences: none — no container runtime, no elevated group. Xcode is
  already installed and licensed.
- Out-of-band notification channels that deliver: none chosen (José named no channel, D-008).
