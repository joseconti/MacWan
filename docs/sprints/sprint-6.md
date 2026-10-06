---
schema: keel.sprint/1
sprint: 6
goal: MPS engine — FLF2V, VACE, V2V, T2I
status: not-started
slices:
  - id: S-046
    title: Worker MPS engine (diffusers) — load, generate, progress, cancel, GGUF and bf16 loading
    status: not-started
    hours: 3
    actual_hours: null
    actual_source: measured
    depends_on: [S-017, S-010]
    criteria: []
  - id: S-047
    title: MPSEngine (Swift) and capability routing between engines
    status: not-started
    hours: 1.5
    actual_hours: null
    actual_source: measured
    depends_on: [S-032, S-046]
    criteria: [AC-12]
  - id: S-048
    title: First + Last frame to Video task
    status: not-started
    hours: 2
    actual_hours: null
    actual_source: measured
    depends_on: [S-036, S-047]
    criteria: [AC-10, AC-11]
  - id: S-049
    title: VACE in the worker — reference images, mask, control video parameters
    status: not-started
    hours: 2
    actual_hours: null
    actual_source: measured
    depends_on: [S-046]
    criteria: []
  - id: S-050
    title: Edit & Control (VACE) screen, including mask and control inputs
    status: not-started
    hours: 3
    actual_hours: null
    actual_source: measured
    depends_on: [S-036, S-049]
    criteria: [AC-10, AC-11, AC-80]
  - id: S-051
    title: Video to Video task
    status: not-started
    hours: 2
    actual_hours: null
    actual_source: measured
    depends_on: [S-036, S-047]
    criteria: [AC-10, AC-11]
  - id: S-052
    title: Text to Image task
    status: not-started
    hours: 1.5
    actual_hours: null
    actual_source: measured
    depends_on: [S-036, S-047]
    criteria: [AC-10]
  - id: S-053
    title: Real-engine smoke suite (slow) and UI tests with accessibility audit for the new screens
    status: not-started
    hours: 2
    actual_hours: null
    actual_source: measured
    depends_on: [S-048, S-050, S-051, S-052]
    criteria: [AC-80]
---

# Sprint 6 — MPS engine — FLF2V, VACE, V2V, T2I

- Acceptance: each task renders on the Mac with the engine the capability table picks, and the UI
  never names the engine.
- Notes: scope follows S-002 — a pipeline that failed its spike is moved to `deferred.md`, never
  shipped broken.
- Close-out: [filled at close]
