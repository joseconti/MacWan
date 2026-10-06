---
schema: keel.sprint/1
sprint: 9
goal: Hardening — accessibility, localization, security, documentation, release preparation
status: not-started
slices:
  - id: S-065
    title: Accessibility — automated audit of every screen and state, driven keyboard pass, fixes
    status: not-started
    hours: 3
    actual_hours: null
    actual_source: measured
    depends_on: [S-039, S-045, S-053]
    criteria: [AC-80]
  - id: S-066
    title: Guided VoiceOver pass with José, one instruction at a time, and fixes
    status: not-started
    hours: 2.5
    actual_hours: null
    actual_source: measured
    depends_on: [S-065]
    criteria: [AC-80]
  - id: S-067
    title: Spanish and Catalan localization, long-string layout check
    status: not-started
    hours: 2.5
    actual_hours: null
    actual_source: measured
    depends_on: [S-058]
    criteria: [AC-81]
  - id: S-068
    title: Security hardening, threat-model re-verification, security audit offer
    status: not-started
    hours: 3
    actual_hours: null
    actual_source: measured
    depends_on: [S-058, S-060]
    criteria: []
  - id: S-069
    title: Sign and notarize pipeline (scripts/notarize.sh) and install test on a clean macOS user
    status: not-started
    hours: 2.5
    actual_hours: null
    actual_source: measured
    depends_on: [S-060]
    criteria: [AC-01, AC-53]
  - id: S-070
    title: Phase 6 documentation — architecture, api, usage, reference, security, accessibility, README
    status: not-started
    hours: 3
    actual_hours: null
    actual_source: measured
    depends_on: [S-065]
    criteria: []
  - id: S-071
    title: End-user guide (guide/) on keel-docs-theme, in the shipped locales
    status: not-started
    hours: 3
    actual_hours: null
    actual_source: measured
    depends_on: [S-067, S-070]
    criteria: []
  - id: S-072
    title: Phase 7 gate — full suite on the candidate, keel-verify, release record, licence decision, version
    status: not-started
    hours: 2
    actual_hours: null
    actual_source: measured
    depends_on: [S-066, S-068, S-069, S-070, S-071]
    criteria: []
---

# Sprint 9 — Hardening — accessibility, localization, security, documentation, release preparation

- Acceptance: the Phase 6 and Phase 7 definitions of done pass item by item; the release candidate
  is on `develop` and signalled as ready for `main`. The merge, the tag and the release are José's.
- Notes: S-066 is `ASSISTIVE-TECH`; S-069 needs José's Developer ID and notary credentials
  (`CREDENTIAL`); MacWan's own licence must be decided before S-072 (D-008).
- Close-out: [filled at close]
