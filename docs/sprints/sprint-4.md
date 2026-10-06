---
schema: keel.sprint/1
sprint: 4
goal: First video — onboarding, MLX engine, T2V/I2V/TI2V, render queue
status: not-started
slices:
  - id: S-031
    title: Worker MLX engine — load, generate, progress, preview frames, cancel, unload for T2V, I2V and TI2V
    status: not-started
    hours: 3
    actual_hours: null
    actual_source: measured
    depends_on: [S-017, S-010]
    criteria: []
  - id: S-032
    title: MLXEngine (Swift), capability table and the memory guard
    status: not-started
    hours: 2
    actual_hours: null
    actual_source: measured
    depends_on: [S-018, S-023, S-031]
    criteria: [AC-12]
  - id: S-033
    title: JobQueue — state machine, one render at a time, cancel, reorder, pause, sleep prevention, worker-crash recovery
    status: not-started
    hours: 2.5
    actual_hours: null
    actual_source: measured
    depends_on: [S-018, S-027]
    criteria: [AC-20, AC-21, AC-22]
  - id: S-034
    title: Onboarding wizard (F1) — hardware check, storage, starter pack, licence, resumable install checklist
    status: not-started
    hours: 3
    actual_hours: null
    actual_source: measured
    depends_on: [S-019, S-020, S-026, S-028]
    criteria: [AC-01, AC-02, AC-03, AC-04, AC-80, AC-81]
  - id: S-035
    title: Benchmark render and ETA calibration
    status: not-started
    hours: 1
    actual_hours: null
    actual_source: measured
    depends_on: [S-032, S-033]
    criteria: [AC-23]
  - id: S-036
    title: Create screen framework (inputs, preview, Advanced) and Text to Video
    status: not-started
    hours: 3
    actual_hours: null
    actual_source: measured
    depends_on: [S-016, S-028, S-032, S-033]
    criteria: [AC-10, AC-11, AC-80, AC-81]
  - id: S-037
    title: Image to Video and TI2V task screens
    status: not-started
    hours: 2
    actual_hours: null
    actual_source: measured
    depends_on: [S-036]
    criteria: [AC-10, AC-11]
  - id: S-038
    title: Queue screen, notifications and the menu-bar extra
    status: not-started
    hours: 2.5
    actual_hours: null
    actual_source: measured
    depends_on: [S-033, S-028]
    criteria: [AC-20, AC-22, AC-80]
  - id: S-039
    title: End-to-end UI tests — onboarding with the fake runtime, create to queue with the fake engine, accessibility audit per screen
    status: not-started
    hours: 2
    actual_hours: null
    actual_source: measured
    depends_on: [S-034, S-036, S-038]
    criteria: [AC-80]
---

# Sprint 4 — First video — onboarding, MLX engine, T2V/I2V/TI2V, render queue

- Acceptance: on a fresh macOS user, with zero Terminal use, the app reaches a playable first video
  (AC-01); cancelling frees memory within the limit of AC-20.
- Close-out: [filled at close]
