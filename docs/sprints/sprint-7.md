---
schema: keel.sprint/1
sprint: 7
goal: Prompt Assistant, Settings, Diagnostics, updates
status: not-started
slices:
  - id: S-054
    title: PromptAssistant core, ported Wan system prompts, local MLX-LM provider
    status: not-started
    hours: 2.5
    actual_hours: null
    actual_source: measured
    depends_on: [S-017, S-010]
    criteria: [AC-60]
  - id: S-055
    title: Claude Code CLI and Codex CLI providers — fixed arguments, timeouts, output as data
    status: not-started
    hours: 1.5
    actual_hours: null
    actual_source: measured
    depends_on: [S-054]
    criteria: [AC-61]
  - id: S-056
    title: API-key providers and SecretsStore (Keychain)
    status: not-started
    hours: 2
    actual_hours: null
    actual_source: measured
    depends_on: [S-054]
    criteria: [AC-62]
  - id: S-057
    title: Enhance UI (diff accept or edit) and Describe image
    status: not-started
    hours: 2
    actual_hours: null
    actual_source: measured
    depends_on: [S-036, S-054]
    criteria: [AC-60, AC-80]
  - id: S-058
    title: Settings — storage (external volume), engines and Repair, privacy, updates
    status: not-started
    hours: 3
    actual_hours: null
    actual_source: measured
    depends_on: [S-020, S-026, S-028]
    criteria: [AC-50, AC-51, AC-80, AC-81]
  - id: S-059
    title: Diagnostics export — scrubbed zip
    status: not-started
    hours: 1.5
    actual_hours: null
    actual_source: measured
    depends_on: [S-015]
    criteria: [AC-70]
  - id: S-060
    title: Sparkle 2 integration and scripts/appcast.sh
    status: not-started
    hours: 2
    actual_hours: null
    actual_source: measured
    depends_on: [S-013]
    criteria: [AC-53]
---

# Sprint 7 — Prompt Assistant, Settings, Diagnostics, updates

- Acceptance: the assistant is Off by default and every provider can be enabled and used without
  affecting generation; the diagnostics zip contains no prompt or media unless ticked.
- Close-out: [filled at close]
