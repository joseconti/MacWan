# Lessons Learned — MacWan

> Append-only; never trim. Symptom → cause → fix.

## L-001 — Documentation and tooling slices were estimated in hours and took minutes
- Date / phase: 2026-10-06 / Phase 2, sprint 1 (S-007, S-008, S-009)
- Symptom: three slices estimated at 4.5 h in total were finished in about 0.27 h of wall-clock time (−94 %).
- Cause: the estimates were written as if a slice were a human work block. Pure writing work by the AI, with no build, no download, no hardware run and no question to José, is bounded by generation time, not by hours.
- Fix / rule: when re-estimating at the Phase 2 gate (S-011), size documentation-only and pure-code slices from this measurement, and keep hour-scale figures only for slices dominated by things the AI waits on — model downloads, renders, Xcode builds and UI test runs, notarization, and José's supervision. Do not apply this session's ratio to those: a spike that downloads 34 GB is not 15 times faster than planned.
- Also: start `scripts/keel-time` before the first command of a session, so actuals are measured and not backfilled.
