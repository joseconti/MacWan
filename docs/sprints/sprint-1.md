---
schema: keel.sprint/1
sprint: 1
goal: Spikes — prove the Mac runtimes before freezing the architecture
status: not-started
slices:
  - id: S-001
    title: mlx-video spike — convert + generate Wan2.1 1.3B, Wan2.2 TI2V-5B (q4/bf16), A14B (q4); pin SHA and real module paths; measure peak memory, s/step, disk
    status: not-started
    hours: 3
    actual_hours: null
    actual_source: measured
    depends_on: []
    criteria: []
  - id: S-002
    title: diffusers on MPS spike — FLF2V, VACE, V2V, Animate pipelines; list CPU fallbacks; GGUF loading
    status: not-started
    hours: 3
    actual_hours: null
    actual_source: measured
    depends_on: []
    criteria: []
  - id: S-003
    title: Memory tiers — measure every variant, freeze the tier table
    status: not-started
    hours: 1.5
    actual_hours: null
    actual_source: measured
    depends_on: [S-001, S-002]
    criteria: []
  - id: S-004
    title: Notarized app installs uv + standalone Python + venv on a clean macOS user
    status: not-started
    hours: 2
    actual_hours: null
    actual_source: measured
    depends_on: []
    criteria: [AC-01]
  - id: S-005
    title: Wan2.2 Animate preprocessing on Mac — go/no-go
    status: not-started
    hours: 2
    actual_hours: null
    actual_source: measured
    depends_on: [S-002]
    criteria: []
  - id: S-006
    title: Prompt extension — port Wan system prompts; local Qwen 4-bit vs claude -p
    status: not-started
    hours: 1
    actual_hours: null
    actual_source: measured
    depends_on: []
    criteria: []
---

# Sprint 1 — Spikes

- Acceptance: every spike in `docs/03-technical-plan.md` §9 has a written result in
  `docs/research/benchmarks.md`; `Resources/catalogue.json` values that were `null` are measured;
  decisions that change the plan are recorded in `docs/decisions.md`.
- Notes: runs on José's Mac(s) — needs Apple Silicon hardware (`HARDWARE`). Spikes live in
  `spikes/` (throwaway scripts, not app code).
