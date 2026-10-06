---
schema: keel.sprint/1
sprint: 3
goal: Models — catalogue, downloads, conversion, Models screen, design system in code
status: not-started
slices:
  - id: S-022
    title: Phase 4 — design handoff completeness audit with evidence, Design Requests if needed, docs/BUILD-SPEC.md
    status: not-started
    hours: 2.5
    actual_hours: null
    actual_source: measured
    depends_on: [S-012]
    criteria: []
  - id: S-023
    title: Catalogue — schema, loader, validation, Resources/catalogue.json with the measured values
    status: not-started
    hours: 2
    actual_hours: null
    actual_source: measured
    depends_on: [S-010, S-015]
    criteria: []
  - id: S-024
    title: Worker download — Hugging Face resume, pinned revision, sha256 verification, ModelScope fallback, host allow-list
    status: not-started
    hours: 2.5
    actual_hours: null
    actual_source: measured
    depends_on: [S-017]
    criteria: [AC-41, AC-42]
  - id: S-025
    title: Worker convert and quantize — MLX conversion, delete originals, shared T5/VAE dedupe
    status: not-started
    hours: 2.5
    actual_hours: null
    actual_source: measured
    depends_on: [S-024]
    criteria: [AC-43]
  - id: S-026
    title: ModelManager — install state machine, disk accounting, verify, delete, change variant
    status: not-started
    hours: 2.5
    actual_hours: null
    actual_source: measured
    depends_on: [S-023, S-024, S-025]
    criteria: [AC-40, AC-44]
  - id: S-027
    title: Persistence — SwiftData store for installed models, jobs and renders
    status: not-started
    hours: 1.5
    actual_hours: null
    actual_source: measured
    depends_on: [S-015]
    criteria: []
  - id: S-028
    title: Design tokens, shared components and the app shell with navigation, from the handoff
    status: not-started
    hours: 2.5
    actual_hours: null
    actual_source: measured
    depends_on: [S-022]
    criteria: []
  - id: S-029
    title: Models screen
    status: not-started
    hours: 2.5
    actual_hours: null
    actual_source: measured
    depends_on: [S-026, S-028]
    criteria: [AC-40, AC-41, AC-80, AC-81]
  - id: S-030
    title: Model update notices — pinned revision against remote, offered and never automatic
    status: not-started
    hours: 1
    actual_hours: null
    actual_source: measured
    depends_on: [S-026]
    criteria: [AC-52]
---

# Sprint 3 — Models — catalogue, downloads, conversion, Models screen, design system in code

- Acceptance: a model can be installed, paused, resumed, verified, converted, switched to another
  variant and deleted from the Models screen, with disk figures that match the filesystem.
- Notes: S-022 is the Phase 4 gate and depends on Design having returned the handoff
  (`EXTERNAL-APPROVAL`); S-023…S-027 do not, and are worked first if the handoff is late.
- Close-out: [filled at close]
