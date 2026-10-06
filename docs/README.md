# MacWan docs — start here

MacWan is a native macOS (Apple Silicon) app that installs, updates and runs every open model from
[github.com/Wan-Video](https://github.com/Wan-Video) behind a visual UI. The project follows the
Keel workflow (see `CLAUDE.md` / `AGENTS.md`); live state is in `PROGRESS.md`.

Read in this order:

| # | Document | What you get |
|---|---|---|
| 1 | [`PROGRESS.md`](PROGRESS.md) | where the project is, next action, open questions |
| 2 | [`decisions.md`](decisions.md) | decisions already taken — never re-open them |
| 3 | [`research/wan-video-ecosystem.md`](research/wan-video-ecosystem.md) | what each Wan repo is, how they relate, every model, sizes, CLI flags, defaults |
| 4 | [`research/apple-silicon-runtime.md`](research/apple-silicon-runtime.md) | why the official code fails on Mac, MLX vs PyTorch-MPS, memory tiers, process model, cloud API |
| 5 | [`research/ai-assistant-cli.md`](research/ai-assistant-cli.md) | where Claude/ChatGPT CLIs help (prompts) and where they cannot (video) |
| 5b | [`research/benchmarks.md`](research/benchmarks.md) | what was actually measured on the Mac — read before trusting any size, speed or memory figure elsewhere |
| 6 | [`00-competitive-landscape.md`](00-competitive-landscape.md) | Draw Things, ComfyUI, mlx-video… and why MacWan must cover every task |
| 7 | [`01-discovery.md`](01-discovery.md) | purpose, proposed v1, risks, i18n, accessibility, open questions |
| 8 | [`02-functional-spec.md`](02-functional-spec.md) · [`flows/`](flows/) | requirements, acceptance criteria (`AC-nn`), data model, design split, the five flows (DRAFT) |
| 9 | [`03-technical-plan.md`](03-technical-plan.md) | stack, architecture, marked code map, change map, worker protocol, catalogue schema, testing, environment requirements, spikes (DRAFT) |
| 10 | [`threat-model.md`](threat-model.md) | assumptions, controls with their delivery state, what is deliberately not defended |
| 11 | [`estimate.md`](estimate.md) · [`sprints/README.md`](sprints/README.md) | AI-time estimate and the sprint plan (73 slices, sprints 0–9) · [`sprints/deferred.md`](sprints/deferred.md) |
| 12 | [`sessions.md`](sessions.md) · [`token-ledger.md`](token-ledger.md) · [`keel-conformance.md`](keel-conformance.md) | measured session time, token usage, the Keel conformance sweep |

Project scripts: `scripts/keel-time` (session clock), `scripts/keel-plan` (regenerates the plan and
answers "what is left": `scripts/keel-plan --left`), `scripts/keel-verify` (state and plan linter).

**Next action for a developer:** the sprint 1 spikes, starting with S-001 (`sprints/sprint-1.md`), on an Apple Silicon Mac.
Anything marked **VERIFY** in the research docs is unconfirmed and must be proven before code relies on it.
