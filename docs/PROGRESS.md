# PROGRESS — MacWan

> Living state. Read this FIRST in every session. Keep current and compact.

## Project card
- Name / one-line purpose: MacWan — the complete, zero-Terminal Wan video studio for Apple Silicon Macs (installs runtime + Wan models on first launch, every open Wan task visually)
- Project type: native desktop app (macOS, Apple Silicon) — confirmed (D-003, D-008)
- Stack & target platform(s): Swift 6/SwiftUI, macOS 14+, Apple Silicon only; Python worker (uv-managed) with MLX (mlx-video) + PyTorch-MPS (diffusers) engines — docs/03-technical-plan.md (DRAFT)
- License: undecided — José decides before Phase 7 (D-008); does not block development
- Docs language: English — confirmed by José (D-007); conversation with José in Spanish
- Security profile: web-app profile adapted to desktop (technical plan §7) — docs/threat-model.md (DRAFT; every control TO BUILD / MANUAL / VERIFY)
- Security audit: optional (D-010) — offered at S-068
- Accessibility: native macOS accessibility API in full (VoiceOver, keyboard, Reduce Motion, Increase Contrast) — docs/01-discovery.md §7
- i18n: English base, String Catalogs; locales EN, ES, CA (D-008)
- Installed base: fresh v1 (empty repository, no users)
- Design system: pending — asked (open items); decided in S-012 before the design brief
- Keel portability: lock + embedded v6.5.0 (complete — both trees verified file-for-file against the v6.5.0 release tag)
- Assistant config: pending — asked (open items)
- E2E: absent
- CI runs on: pending — asked with the assistant-config package
- Models: n/a until agents exist
- Keel baseline: v6.5.0
- Website intent: yes, later (D-008)
- Client budget: no (D-008)
- User guide: n/a until Phase 6
- Docs theme: n/a until Phase 6
- Test-first policy: pending — `pure-logic` proposed, asked (open items)
- Push test scope: affected
- Sprints: on
- Durability: git remote origin https://github.com/joseconti/MacWan
- Autonomy: automatic (D-008; machine-local settings written, D-012) / issues: asked, unanswered / Issue sweep interval: n/a until answered / Issue capture: asked, unanswered
- Branches: integration branch `develop` (all work); `main` holds only the initial commit — nothing is ready for `main`
- Notify: none chosen yet — asked (open items); until answered, silence means nothing was sent
- Chaining: pending — asked (open items); `off` is in effect until answered
- Chaining model: pending — asked with Chaining
- Chain verified: n/a

## Phase status
| Phase | Status | Key artifacts |
|-------|--------|---------------|
| 1 Discovery | done 2026-10-06 (D-008) | docs/00-competitive-landscape.md, docs/01-discovery.md, docs/estimate.md (v1 preliminary) |
| 2 Functional spec | in progress — 02/03 DRAFT v0.2, flows, threat model, change map, environment requirements written; gate (S-011) waits for the spikes and José's answers | docs/02-functional-spec.md, docs/03-technical-plan.md, docs/flows/, docs/threat-model.md, docs/estimate.md (v1.1 preliminary; firm at S-011) |
| 3 Design handoff | pending | docs/design/DESIGN-BRIEF.md |
| 4 Faithful build | pending | docs/BUILD-SPEC.md |
| 5 Development | pending — planned: sprints 2–9 | docs/sprints/ (index: docs/sprints/README.md), docs/05-test-points.md |
| 6 Documentation | pending | docs/architecture.md, docs/api/, docs/usage/, docs/reference/ |
| 7 Release | pending | docs/07-release.md |
| 8 Website | pending — depends on Phase 1 step 7 | docs/site/ or site repo |

## Current position
- Phase: 2 — Functional spec  Step/sprint: sprint 1, next slice **S-001** (mlx-video spike); S-007, S-008, S-009 done
- Next action: get José's OK to install `uv` and to download the spike models (tens of GB: Wan2.1 1.3B, Wan2.2 TI2V-5B; A14B ≈ 126 GB), then run `scripts/keel-time start --plan S-001,S-004,S-006` and work S-001 in `spikes/`, writing every measurement to `docs/research/benchmarks.md`. S-002, S-004 and S-006 do not depend on S-001 and can be worked while downloads run. This Mac is an M5 with 32 GB: Standard-tier figures are measurable here, Entry-tier (16 GB) ones are not.
- Tooling: `scripts/keel-time`, `scripts/keel-plan`, `scripts/keel-verify` exist. The remaining Keel scripts and hooks are slice S-014 (Phase 5 scaffold); until then the close-out is done by hand and `scripts/keel-verify` covers state and plan only.

## Open items
- Unresolved user questions (all parked on José; none blocks S-001…S-006):
  1. Test-first policy — `pure-logic` (recommended) / `pure-logic + acceptance` / `none`
  2. Design system — existing brand identity (where?) or MacWan founds one — needed for S-012
  3. Forge issues — review them at every sprint close (and at what interval, default 24 h)? Turn a problem José reports into a GitHub issue first (issue capture)?
  4. Notification channel when Keel stops
  5. Assistant config package (rules, agents, pre-commit gate, CI) and which tools; Gemini CLI in use?
  6. Chat chaining (`off` / `prefill` / `start` / `supervised`) and the chaining model
  7. OK to install `uv` and SwiftLint (Homebrew) and to download the spike models
  8. A 16 GB Apple Silicon Mac for Entry-tier measurements — available or not
  9. MacWan's own licence (before Phase 7, D-008)
- Open Design Requests: none
- Unverified external steps/assets: every item marked VERIFY in docs/research/*.md and docs/threat-model.md (resolved by the sprint 1 spikes)
- Forge issues in progress: none
- PRs: #1 and #2 are merged into `develop`
- Ready for `main`: nothing

### Deferred items (consciously postponed work)
- v1.x and later features, and the product website: itemized in docs/sprints/deferred.md (S-073…S-080) — review trigger: after v1.0, or when José promotes one
- XCUITest takes the screen — mitigation to agree before S-039 (technical plan §12)

Last updated: 2026-10-06 — sprint 1: Keel step 0a completed, Phase 2 documentation and the full sprint plan written (D-009…D-012)
