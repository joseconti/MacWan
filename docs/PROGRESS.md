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
- Design system: founding — MacWan's own, canonical for the app and its website; must carry the parent-brand endorsement "By PackDesk" (D-014); location fixed in S-012
- Keel portability: lock + embedded v6.5.0 (complete — both trees verified file-for-file against the v6.5.0 release tag)
- Assistant config: full (tools: claude + others José still has to name) (D-013) — rules and agents at the Phase 2 close (S-011), permissions, pre-commit gate and CI at S-014
- E2E: absent
- CI runs on: main (default) — push to main, version tags and PRs targeting main; to confirm when the package is generated (S-014)
- Models: n/a until agents exist
- Keel baseline: v6.5.0
- Website intent: yes, later (D-008)
- Client budget: no (D-008)
- User guide: n/a until Phase 6
- Docs theme: n/a until Phase 6
- Test-first policy: pure-logic (D-013)
- Push test scope: affected
- Sprints: on
- Durability: git remote origin https://github.com/joseconti/MacWan
- Autonomy: automatic (D-008; machine-local settings written, D-012) / issues: after-sprint / Issue sweep interval: 24h / Issue capture: on (D-013)
- Branches: integration branch `develop` (all work); `main` holds only the initial commit — nothing is ready for `main`
- Notify: email — j.conti@joseconti.com via the Gmail connector (D-013); send tool present this session, not yet test-fired
- Chaining: start (D-013) — not operative until S-014 builds `scripts/keel-continue` and `keel-chain-check --smoke` passes; until then the prompt is printed
- Chaining model: opus (D-013)
- Chain verified: not yet — written only by `scripts/keel-chain-check --smoke` (S-014)

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
- Phase: 2 — Functional spec  Step/sprint: sprint 1, slice **S-001** (mlx-video spike) in progress
- Done in S-001: `spikes/` environment pinned (D-016); Wan2.1 1.3B, Wan2.2 TI2V-5B and Wan2.2 T2V A14B downloaded, converted and rendered; the 23–29 GB memory peak explained and removed for the small models (D-018); A14B 4-bit works but peaks at 23–24 GB and takes 15–39 min per short clip on 32 GB. Results in docs/research/benchmarks.md. Models are in `~/Library/Caches/MacWan-spikes/` (≈ 275 GB).
- Next action: **wait for José to name a time window for heavy runs** — renders and conversions saturate his Mac and he stopped them on 2026-10-06 (L-002). The two 81-frame runs were killed before finishing and left no result. Work that does NOT load the machine can proceed meanwhile: S-003's tier table rebuilt from the peaks already measured (marking what is still unmeasured), S-006's prompt porting, and the documentation side of S-004. When a window is given: 81-frame clips, default step counts, I2V at 40 steps, A14B with one expert at a time (benchmarks.md "Still to do in S-001"). The original Hugging Face downloads (≈ 166 GB of ≈ 275 GB in `~/Library/Caches/MacWan-spikes/`) can be deleted once José agrees — asked, unanswered.
- Tooling: `scripts/keel-time`, `scripts/keel-plan`, `scripts/keel-verify` exist. The remaining Keel scripts and hooks are slice S-014 (Phase 5 scaffold); until then the close-out is done by hand.

## Open items
- Unresolved user questions (parked on José; none blocks S-001…S-006):
  1. Assistant config — which tools besides Claude Code (Codex, Cursor, Gemini CLI, Copilot, Windsurf)? Needed at S-011
  2. PackDesk — logo assets and brand rules, and where "By PackDesk" must appear. Needed at S-012
  3. Minimum Mac — 16 GB is now plausible (8.6 GB peak for Wan2.1 1.3B, D-018) but cannot be verified without a 16 GB Mac (D-015): ship it labelled unverified, raise the minimum to 24 GB, or find an outside tester. Needed at S-011
  4. When heavy spike runs may use the Mac (a time window), and whether to delete the original downloads (≈ 166 GB)
  5. MacWan's own licence (before Phase 7, D-008)
- Open Design Requests: none
- Unverified external steps/assets: every item marked VERIFY in docs/research/*.md and docs/threat-model.md (resolved by the sprint 1 spikes)
- Forge issues in progress: none
- PRs: #1 and #2 are merged into `develop`
- Ready for `main`: nothing

### Deferred items (consciously postponed work)
- v1.x and later features, and the product website: itemized in docs/sprints/deferred.md (S-073…S-080) — review trigger: after v1.0, or when José promotes one
- XCUITest takes the screen — mitigation to agree before S-039 (technical plan §12)

Last updated: 2026-10-06 — sprint 1: S-001 in progress; heavy runs stopped at José's request (L-002)
