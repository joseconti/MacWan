---
schema: keel.sprint/1
sprint: 2
goal: Foundations — project skeleton, runtime manager, worker protocol (no UI; runs while Design works)
status: not-started
slices:
  - id: S-013
    title: Scaffold — XcodeGen project.yml, SwiftPM packages, app target shell, SwiftLint/swift-format/ruff configs, .gitattributes, scripts/build.sh
    status: not-started
    hours: 2.5
    actual_hours: null
    actual_source: measured
    depends_on: [S-011]
    criteria: []
  - id: S-014
    title: Keel scaffold tooling — keel-doctor, keel-affected-tests, pre-push and post-commit hooks, keel-close, keel-handoff-verify, keel-stop-hook, keel-session-pid, docs/playground.md, docs/05-test-points.md, docs/api/INDEX.md
    status: not-started
    hours: 3
    actual_hours: null
    actual_source: measured
    depends_on: [S-013]
    criteria: []
  - id: S-015
    title: MacWanCore — Recipe, Job, Task, ModelDescriptor, Variant, Tier, error types, logger with debug switch
    status: not-started
    hours: 2
    actual_hours: null
    actual_source: measured
    depends_on: [S-013]
    criteria: []
  - id: S-016
    title: Recipe validation — 4n+1 frames, supported sizes, size divisor, fps to duration (test-first)
    status: not-started
    hours: 1.5
    actual_hours: null
    actual_source: measured
    depends_on: [S-015]
    criteria: [AC-10, AC-11]
  - id: S-017
    title: Worker package — protocol v1 (hello handshake, commands, events, closed error codes), fake engine, pytest suite
    status: not-started
    hours: 2.5
    actual_hours: null
    actual_source: measured
    depends_on: [S-013]
    criteria: []
  - id: S-018
    title: Swift protocol codec and EngineHost — spawn, handshake, monitor, crash restart, golden JSON tests
    status: not-started
    hours: 2.5
    actual_hours: null
    actual_source: measured
    depends_on: [S-015, S-017]
    criteria: [AC-21]
  - id: S-019
    title: HardwareProbe and tier assignment
    status: not-started
    hours: 1.5
    actual_hours: null
    actual_source: measured
    depends_on: [S-015]
    criteria: [AC-04]
  - id: S-020
    title: RuntimeManager — uv, standalone Python, per-engine venvs, state.json, repair, resume (tested with a fake uv)
    status: not-started
    hours: 3
    actual_hours: null
    actual_source: measured
    depends_on: [S-015]
    criteria: [AC-02, AC-03, AC-50, AC-51]
  - id: S-021
    title: Bundle uv (scripts/fetch-uv, Contents/Helpers) and real runtime install smoke on Apple Silicon
    status: not-started
    hours: 1.5
    actual_hours: null
    actual_source: measured
    depends_on: [S-020]
    criteria: [AC-01]
---

# Sprint 2 — Foundations — project skeleton, runtime manager, worker protocol (no UI; runs while Design works)

- Acceptance: `scripts/build.sh` builds the app shell; the Swift and Python suites pass; the app
  installs a real runtime into Application Support and the worker answers `probe` over the protocol.
- Notes: nothing here needs the design handoff, so it runs in parallel with Design's work on the
  brief from S-012. Assumptions from the spikes are re-validated at the sprint kickoff.
- Close-out: [filled at close]
