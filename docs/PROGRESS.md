# PROGRESS — MacWan

> Living state. Read this FIRST in every session. Keep current and compact.

## Project card
- Name / one-line purpose: MacWan — the complete, zero-Terminal Wan video studio for Apple Silicon Macs (installs runtime + Wan models on first launch, every open Wan task visually)
- Project type: native desktop app (macOS, Apple Silicon) — confirmed (D-003, D-008)
- Stack & target platform(s): Swift 6/SwiftUI, macOS 14+, Apple Silicon only; Python worker (uv-managed) with MLX (mlx-video) + PyTorch-MPS (diffusers) engines — docs/03-technical-plan.md (DRAFT)
- License: undecided — José decides before Phase 7 (D-008); does not block development
- Docs language: English — confirmed by José (D-007); conversation with José in Spanish
- Security profile: web-app profile adapted to desktop (technical plan §7) — threat model pending Phase 2
- Security audit: pending — derived at Phase 2 §4c
- Accessibility: native macOS accessibility API in full (VoiceOver, keyboard, Reduce Motion, Increase Contrast) — docs/01-discovery.md §7
- i18n: English base, String Catalogs; locales EN, ES, CA (D-008)
- Installed base: fresh v1 (empty repository, no users)
- Design system: pending — Phase 1 step 9
- Keel portability: lock + embedded v6.5.0 (complete — both trees verified file-for-file against the v6.5.0 release tag)
- Assistant config: pending — offered in the Phase 1 step 0a batch
- E2E: absent
- CI runs on: pending — asked with the assistant-config package
- Models: n/a until agents exist
- Keel baseline: v6.5.0
- Website intent: yes, later (D-008)
- Client budget: no (D-008)
- User guide: n/a until Phase 6
- Docs theme: n/a until Phase 6
- Test-first policy: pending — Phase 2 step 4e
- Push test scope: affected
- Sprints: on
- Durability: git remote origin https://github.com/joseconti/MacWan
- Autonomy: automatic (D-008) / issues: not yet asked / Issue sweep interval: n/a / Issue capture: not yet asked
- Branches: integration branch `develop`; `main` holds only the initial commit
- Notify: none chosen yet — José did not name a channel; the project thread is the only channel
- Chaining: pending — Phase 1 step 0a
- Chaining model: pending
- Chain verified: n/a

## Phase status
| Phase | Status | Key artifacts |
|-------|--------|---------------|
| 1 Discovery | done 2026-10-06 (D-008) | docs/00-competitive-landscape.md, docs/01-discovery.md, docs/estimate.md (v1 preliminary) |
| 2 Functional spec | in progress — 02/03 DRAFT v0.1; firmed after Sprint 1 spikes | docs/02-functional-spec.md, docs/03-technical-plan.md, docs/flows/, docs/estimate.md (firm), docs/budget.md |
| 3 Design handoff | pending | docs/design/DESIGN-BRIEF.md |
| 4 Faithful build | pending | docs/BUILD-SPEC.md |
| 5 Development | pending | docs/sprints/, docs/05-test-points.md |
| 6 Documentation | pending | docs/architecture.md, docs/api/, docs/usage/, docs/reference/ |
| 7 Release | pending | docs/07-release.md |
| 8 Website | pending — depends on Phase 1 step 7 | docs/site/ or site repo |

## Current position
- Phase: 2 — Functional spec  Step/sprint: Sprint 1 (spikes) next
- Next action: run Sprint 1 spikes (docs/sprints/sprint-1.md) on José's Apple Silicon Mac via a Remote Control session in /Users/joseconti/Documents/GitHub/MacWan; feed measurements into docs/research/benchmarks.md and catalogue values; then firm 02/03 and estimate v2 at the Phase 2 gate.
- Keel step 0a still pending: scripts/keel-time, scripts/keel-verify, docs/sessions.md, docs/keel-conformance.md, assistant-config offer, chaining — sprint actuals are `estimated` until keel-time exists; docs/.keel/plan.json not generated yet.

## Open items
- Unresolved user questions: forge-issue duty and issue capture (Keel setup Q2/Q2b); notification channel (Q3); MacWan licence (before Phase 7)
- Open Design Requests: none
- Unverified external steps/assets: every item marked VERIFY in docs/research/*.md (resolved by Sprint 1 spikes)
- Forge issues in progress: none
- PRs: #1 Keel integration (draft); #2 base docs (draft, stacked on #1)

### Deferred items (consciously postponed work)
- v1.x: Speech-to-Video (S2V), Wan-Animate-2, cloud engine (Model Studio, Wan 2.5–3.0), LoRA training, agent/MCP control — docs/01-discovery.md §4
- Excluded while CUDA-only: Wan-Dancer

Last updated: 2026-10-06 — Phase 1 closed (D-008)
