# Token Ledger — MacWan

> Actual token usage. One row per working session, appended at session end.
> Method is always stated: measured (environment counter, API usage, provider dashboard)
> or estimated (volume-based). An honest estimate beats an empty cell.

## Sessions
| Date | Phase/sprint | Model(s) | Input tokens | Output tokens | Method | Notes |
|------|--------------|----------|--------------|---------------|--------|-------|
| 2026-10-06 | Phase 1 / sprint 0 (S-000) | not recorded | — | — | not recorded | two cloud sessions (PRs #1 and #2) ran before this ledger existed; their usage was not captured and is not reconstructed |
| 2026-10-06 | Phase 2 / sprint 1 (S-007, S-008, S-009) | claude-opus-5-5 | ≈ 160,000 | ≈ 55,000 | estimated (volume-based) | input counts unique context once; cached re-reads across tool calls are not included |
| 2026-10-06 | Phase 2 / sprint 1 (S-081, S-001 in progress) | claude-opus-5-5 | ≈ 60,000 | ≈ 25,000 | estimated (volume-based) | same conversation as the previous row; only the context added after it is counted |
| 2026-10-06 | Phase 2 / sprint 1 (S-001 in progress) | claude-opus-5-5 | ≈ 70,000 | ≈ 30,000 | estimated (volume-based) | same conversation; only the context added after the previous row |

Running total: ≈ 290,000 / ≈ 110,000 (estimated; sprint 0 not recorded) — updated with each row.

## Final reconciliation (at release — Phase 7)
- Total tokens by model: pending
- Cost at verified prices (source + date): pending
- Estimate vs actual: pending
- Lesson for future estimates: pending
