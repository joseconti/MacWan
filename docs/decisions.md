# Decisions — MacWan

> Append-only. A session NEVER re-opens a decision recorded here on its own initiative;
> only the user reverses a decision (append the reversal as a new entry).

## D-001 — The project is run with Keel from day one, embedded in the repository
- Date / phase: 2026-10-06 / Phase 1 step 0a
- Decision: MacWan follows the Keel workflow from the start. Keel v6.5.0 (latest release tag of github.com/joseconti/keel-skill at this date) is embedded in both discovery trees, `.claude/skills/keel/` and `.agents/skills/keel/`, and the portability lock is present in `CLAUDE.md` and `AGENTS.md`.
- Why: José asked explicitly to have Keel inside the repository, at its latest version, so any session or assistant opening the repo is bound to it.
- Alternatives rejected (and why): lock only, without the embedded copy — rejected because José asked for Keel inside the repo.
- Supersedes: none

## D-002 — Branch layout for an empty repository
- Date / phase: 2026-10-06 / Phase 1 step 0a
- Decision: `main` receives a minimal initial commit (README + .gitignore); `develop` is created from it as the integration branch; Keel work lands on `develop` through work branches.
- Why: Keel's git flow — `develop` integrates, `main` is the person's.
- Alternatives rejected (and why): committing Keel directly to `main` — contradicts the git flow.
- Supersedes: none
