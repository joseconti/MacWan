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

---

## v1.1 — PRELIMINARY, reconciled with the sprint plan (2026-10-06)

The plan in `docs/sprints/` is now the itemization: one slice per unit of work, each with its hours.
This table is the sum of those slices and replaces the v1 table above as the working figure. It is
still **preliminary** — the firm estimate (v2) is written at the Phase 2 gate (S-011), once the
spikes have replaced the unknowns with measurements. Every figure is **AI working time plus José's
supervision time**, in one number per slice; contingency is not included.

| Sprint | Goal | Slices | Hours |
|---|---|---|---|
| 0 | Phase 1 discovery and base documentation | 1 | 2.5 |
| 1 | Spikes, Keel foundation and Phase 2 close | 13 | 22.25 |
| 2 | Foundations — project skeleton, runtime manager, worker protocol (no UI; runs while Design works) | 9 | 20 |
| 3 | Models — catalogue, downloads, conversion, Models screen, design system in code | 9 | 19.5 |
| 4 | First video — onboarding, MLX engine, T2V/I2V/TI2V, render queue | 9 | 21 |
| 5 | Library — recipes, export, quality presets, LoRA | 6 | 12 |
| 6 | MPS engine — FLF2V, VACE, V2V, T2I | 8 | 17 |
| 7 | Prompt Assistant, Settings, Diagnostics, updates | 7 | 14.5 |
| 8 | Character Animate / Replace (experimental, gated by S-005) | 4 | 10 |
| 9 | Hardening — accessibility, localization, security, documentation, release preparation | 8 | 21.5 |
| **Total** | | **74** | **160.25 h** |

<!-- keel:plan-total 160.25 -->

- Against v1 (103–171 h for AI plus supervision combined): inside the range. What v1 did not
  itemize and v1.1 does: the Keel tooling (S-007, S-014), the Phase 2 close and design brief
  (S-008…S-012), the Phase 4 handoff audit (S-022) and the end-user guide (S-071).
- Contingency proposed: +20 % (≈ 32 h), kept outside the plan so the plan can reach 100 %.
- Not in the total: `docs/sprints/deferred.md` — 8 items, ≈ 76 h (v1.x features and the product website).
- AI cost: not computed yet — the payment mode (subscription or API) is asked at the firm estimate
  (S-011). Actual usage is recorded in `docs/token-ledger.md`.
- Largest risks to the figure: unchanged from v1 — the outcomes of S-001 and S-002, and S-005's
  go/no-go for sprint 8 (10 h that a no-go removes).
