# Should MacWan lean on the Claude or ChatGPT CLI? — assessment

> Question from José: maybe the app does not need to download models and can use the Claude or
> ChatGPT CLI instead. This document answers it.

## 1. Short answer

**No for video generation, yes as an optional helper.** Claude Code (`claude`) and OpenAI Codex
(`codex`) are text/code agents. Neither generates video, and neither can run Wan. The video models
must run locally (downloaded weights) or on Alibaba's cloud. Where an LLM genuinely helps is the
*language* around the video:

| Job | Needs an LLM? | Wan's own answer | MacWan proposal |
|---|---|---|---|
| Generate video | No — needs Wan weights | local weights | MLX / MPS engines (local), Model Studio (cloud) |
| **Prompt extension** (short idea → rich cinematic prompt) | Yes | DashScope `qwen-plus` or local `Qwen2.5-*-Instruct` | Prompt Assistant (below) |
| **Image captioning** for I2V prompt extension and Animate-2 (fixed caption template) | Yes, vision | `qwen-vl-max` or local `Qwen2.5-VL-*` | Prompt Assistant with a vision-capable provider |
| Translate prompt EN↔ZH (Wan was trained mostly on Chinese captions; `--prompt_extend_target_lang zh` is the default) | Yes | Qwen | Prompt Assistant |
| Storyboarding a multi-shot sequence | Yes | — | later version |

## 2. The Prompt Assistant — a pluggable provider

One Swift protocol, several providers, chosen in Settings. All optional; the app works with none.

| Provider | How MacWan talks to it | Pros | Cons |
|---|---|---|---|
| **Off** | — | zero setup | weaker prompts |
| **Local (MLX-LM)** — default when the user enables the assistant | worker runs `mlx_lm` with e.g. `mlx-community/Qwen2.5-7B-Instruct-4bit` (≈ 4–5 GB) and `mlx-vlm` + `Qwen2.5-VL-7B-Instruct-4bit` for images (VERIFY exact repo ids) | offline, private, free, same model family Wan was tuned with | extra download, RAM while rendering |
| **Claude Code CLI** (if `claude` is on PATH and logged in) | `claude -p "<system+user prompt>" --output-format json` (non-interactive print mode) | uses the user's existing subscription; strong writing; image input supported | must be installed by the user; latency; output must be parsed defensively |
| **Codex CLI** (if `codex` is on PATH) | `codex exec "<prompt>"` non-interactive | same, for ChatGPT subscribers | same |
| **Anthropic API / OpenAI API / DashScope** | HTTPS with a key from the Keychain | no CLI needed | pay-per-use, key management |

Rules:
- Detect CLIs; never install them or log the user in on their behalf. Show "found / not found".
- Run CLIs with a minimal, fixed argument list and a timeout; treat their output as untrusted text
  (strip to the prompt field, length-limit, never execute it).
- Only the prompt text (and, if the user opts in, the input image) leaves the Mac; say so in the UI.
- The system prompts used for extension are versioned resources in the app, derived from Wan's
  `wan/utils/prompt_extend.py` system prompts (VERIFY and port them; keep EN and ZH variants).

## 3. Should Claude/Codex orchestrate MacWan itself (agent mode)?

Possible later: MacWan could expose a small local MCP server or CLI (`macwan generate …`) so an agent
can queue renders. Out of v1 — it adds a security surface (local API) for little user value now.
Recorded as a deferred idea in `docs/01-discovery.md`.

## 4. Decision proposed

Recorded as D-006 in `docs/decisions.md`: video generation never depends on Claude/ChatGPT; the
Prompt Assistant is optional with providers Off / Local MLX-LM / Claude CLI / Codex CLI / API keys;
default Off on first launch, suggested once after the first render.
