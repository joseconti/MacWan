# Estimate — MacWan

> **v1 — PRELIMINARY (Phase 1 close draft, 2026-10-06).** Wide ranges on purpose. Every figure is
> **AI working time plus José's supervision time** — never human-team time. Firm estimate at the
> Phase 2 gate, after the spikes (Sprint 1) replace unknowns with measurements.

| Sprint | Scope | AI hours | Supervision (José) |
|---|---|---|---|
| 1 | Spikes S-001…S-006 (MLX, MPS, tiers, notarized runtime, Animate prep, prompt assistant) | 8–14 | 3–6 (runs on his Macs) |
| 2 | Xcode skeleton (XcodeGen, packages), RuntimeManager, worker + protocol v1, fake engine | 10–16 | 1–2 |
| 3 | Catalogue, ModelManager (download/resume/checksum/convert/quantize/dedupe/delete), Models screen | 10–16 | 2–3 |
| 4 | Onboarding wizard, MLX engine, T2V / I2V / TI2V screens, JobQueue, notifications, menu-bar extra | 12–18 | 2–4 |
| 5 | Library, recipes, export (H.264/HEVC/ProRes/PNG/GIF), presets incl. Lightning Draft, LoRA loading | 8–12 | 1–2 |
| 6 | MPS engine; FLF2V, VACE, V2V, T2I tasks | 12–20 | 2–4 |
| 7 | Prompt Assistant (local MLX-LM, Claude CLI, Codex CLI, API), Settings, Diagnostics, Sparkle | 8–12 | 1–2 |
| 8 | Animate / Replace (experimental, gated by S-005) | 8–16 | 2–3 |
| 9 | Accessibility pass, ES/CA localization, hardening, threat model, notarization pipeline, docs, release prep | 10–16 | 3–5 |
| **Total** | | **86–140 h** | **17–31 h** |

Contingency not included (+20 % proposed). Biggest uncertainty: S-001/S-002 outcomes — if
`mlx-video` cannot be used, the MPS engine becomes primary and Sprint 4 grows by ~8–12 h.

**Hard constraint:** building, running and UI-testing a macOS app needs a Mac. Cloud sessions can
write code and run the Python worker's pure-logic tests, but every build/test point runs on José's
Mac (Remote Control session in `/Users/joseconti/Documents/GitHub/MacWan`). Supervision hours above
assume that.
