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
| 6 | [`00-competitive-landscape.md`](00-competitive-landscape.md) | Draw Things, ComfyUI, mlx-video… and why MacWan must cover every task |
| 7 | [`01-discovery.md`](01-discovery.md) | purpose, proposed v1, risks, i18n, accessibility, open questions |
| 8 | [`02-functional-spec.md`](02-functional-spec.md) | flows, screens, acceptance criteria (DRAFT) |
| 9 | [`03-technical-plan.md`](03-technical-plan.md) | stack, architecture, code map, worker protocol, catalogue schema, spikes (DRAFT) |
| 10 | [`estimate.md`](estimate.md) · [`sprints/`](sprints/) | AI-time estimate and the sprint plan |

**Next action for a developer:** Sprint 1 spikes (`sprints/sprint-1.md`) on an Apple Silicon Mac.
Anything marked **VERIFY** in the research docs is unconfirmed and must be proven before code relies on it.
