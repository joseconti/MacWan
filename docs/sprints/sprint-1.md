---
schema: keel.sprint/1
sprint: 1
goal: Spikes, Keel foundation and Phase 2 close
status: in-progress
slices:
  - id: S-001
    title: mlx-video spike — convert + generate Wan2.1 1.3B, Wan2.2 TI2V-5B (q4/bf16), A14B (q4); pin SHA and real module paths; measure peak memory, s/step, disk
    status: in-progress
    hours: 3
    actual_hours: 1.85
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
  - id: S-007
    title: Keel step 0a — keel-time, keel-plan, keel-verify, sessions log, token ledger, conformance sweep, machine-local settings
    status: done
    hours: 1.5
    actual_hours: 0.10
    actual_source: estimated
    depends_on: []
    criteria: []
  - id: S-008
    title: Phase 2 documentation — flows, AC ids, data model, integrations, design split, threat model, code-map markers, change map, environment preflight and requirements
    status: done
    hours: 2
    actual_hours: 0.10
    actual_source: estimated
    depends_on: []
    criteria: []
  - id: S-009
    title: Sprint plan — slices for sprints 2–9, deferred backlog, estimate v1.1 reconciled with the plan
    status: done
    hours: 1
    actual_hours: 0.07
    actual_source: estimated
    depends_on: []
    criteria: []
  - id: S-010
    title: Consolidate spike results — docs/research/benchmarks.md, frozen tier table, catalogue values, decisions; update 02/03 to match
    status: not-started
    hours: 1.5
    actual_hours: null
    actual_source: measured
    depends_on: [S-001, S-002, S-003, S-004, S-005, S-006]
    criteria: []
  - id: S-011
    title: Phase 2 gate — adversarial spec review, open questions closed, firm estimate v2
    status: not-started
    hours: 1.5
    actual_hours: null
    actual_source: measured
    depends_on: [S-010]
    criteria: []
  - id: S-012
    title: Phase 3 — design-system decision and DESIGN-BRIEF.md with the ready-to-paste Design prompt
    status: not-started
    hours: 2
    actual_hours: null
    actual_source: measured
    depends_on: [S-011]
    criteria: []
  - id: S-081
    title: Record José's setup answers — test-first policy, design system (By PackDesk), issues duty, notification channel, assistant config, chaining, spike downloads, no 16 GB Mac
    status: done
    hours: 0.25
    actual_hours: 0.01
    actual_source: measured
    depends_on: []
    criteria: []
---

# Sprint 1 — Spikes, Keel foundation and Phase 2 close

- Acceptance: every spike in `docs/03-technical-plan.md` §9 has a written result in
  `docs/research/benchmarks.md`; catalogue values that were `null` are measured; decisions that
  change the plan are recorded in `docs/decisions.md`; the Phase 2 definition of done passes item by
  item; the design brief is handed to José with its ready-to-paste prompt.
- Notes: spikes S-001…S-006 need Apple Silicon hardware and multi-GB model downloads (`HARDWARE`);
  they run on José's Mac (M5, 32 GB — see `docs/01-discovery.md` "Environment & test drivers").
  The 16 GB measurements of S-001/S-003 need a second machine or are recorded as `VERIFY`.
  Spikes live in `spikes/` (throwaway scripts, not app code). S-007…S-009 are documentation and
  tooling and do not depend on the spikes. Their `actual_hours` are `estimated`: `scripts/keel-time` was written inside S-007, so the clock
  only started at 19:00 for a session whose first command ran at 18:51 and ended at 19:07 CEST
  (0.27 h in all, split across the three slices by judgment).
- Close-out: [filled at close]
