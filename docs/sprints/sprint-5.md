---
schema: keel.sprint/1
sprint: 5
goal: Library — recipes, export, quality presets, LoRA
status: not-started
slices:
  - id: S-040
    title: Library store — render folders, recipe.json, thumbnails
    status: not-started
    hours: 1.5
    actual_hours: null
    actual_source: measured
    depends_on: [S-027, S-033]
    criteria: [AC-30]
  - id: S-041
    title: Library screen — grid, detail, player, Generate again, Use as input, delete
    status: not-started
    hours: 3
    actual_hours: null
    actual_source: measured
    depends_on: [S-040, S-028]
    criteria: [AC-30, AC-31, AC-80, AC-81]
  - id: S-042
    title: ExportService — H.264, HEVC, ProRes 422, PNG sequence, GIF, recipe metadata
    status: not-started
    hours: 2.5
    actual_hours: null
    actual_source: measured
    depends_on: [S-040]
    criteria: [AC-32]
  - id: S-043
    title: Quality presets — Draft (Lightning LoRA), Standard, High
    status: not-started
    hours: 1.5
    actual_hours: null
    actual_source: measured
    depends_on: [S-036]
    criteria: []
  - id: S-044
    title: LoRA loading — import, list, per-recipe scale and target
    status: not-started
    hours: 2
    actual_hours: null
    actual_source: measured
    depends_on: [S-031, S-036]
    criteria: [AC-10]
  - id: S-045
    title: End-to-end UI tests — create to library to export, accessibility audit
    status: not-started
    hours: 1.5
    actual_hours: null
    actual_source: measured
    depends_on: [S-041, S-042]
    criteria: [AC-80]
---

# Sprint 5 — Library — recipes, export, quality presets, LoRA

- Acceptance: every render reopens with its exact recipe and re-renders identically with the same
  seed (AC-30/AC-31); every export format produces a file that plays.
- Close-out: [filled at close]
