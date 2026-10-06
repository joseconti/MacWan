---
schema: keel.sprint/1
sprint: 8
goal: Character Animate / Replace (experimental, gated by S-005)
status: not-started
slices:
  - id: S-061
    title: Animate preprocessing on the Mac — pose, face and mask extraction in the worker
    status: not-started
    hours: 3
    actual_hours: null
    actual_source: measured
    depends_on: [S-005, S-046]
    criteria: []
  - id: S-062
    title: Worker Animate and Replace generation
    status: not-started
    hours: 3
    actual_hours: null
    actual_source: measured
    depends_on: [S-061]
    criteria: []
  - id: S-063
    title: Animate task screen — tier-gated, marked experimental
    status: not-started
    hours: 2.5
    actual_hours: null
    actual_source: measured
    depends_on: [S-036, S-062]
    criteria: [AC-10, AC-11, AC-80]
  - id: S-064
    title: Smoke test, UI test and accessibility audit for Animate
    status: not-started
    hours: 1.5
    actual_hours: null
    actual_source: measured
    depends_on: [S-063]
    criteria: [AC-80]
---

# Sprint 8 — Character Animate / Replace (experimental, gated by S-005)

- Acceptance: on a Pro or Studio tier Mac a driving video plus a character image produces an
  animated clip; on lower tiers the task is not offered.
- Notes: a no-go from S-005 moves this whole sprint to `deferred.md` with its D-entry.
- Close-out: [filled at close]
