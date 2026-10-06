# Flow — Prompt Assistant (F7, optional)

- Trigger: Enhance next to a prompt, or Describe image on an image input.
- Covers: AC-60, AC-61, AC-62.

## Steps
1. Assistant is Off → the button explains the feature and opens its settings (suggested once after
   the first render, never forced).
2. User picks a provider: Local MLX-LM, Claude Code CLI, Codex CLI, or an API key.
3. Enhance sends the prompt (and the image for captioning) to the provider with the ported Wan
   system prompt.
4. System shows the result as a diff → the user accepts, edits or discards (AC-60).

## Branches and failure paths
- CLI not installed or not logged in → plain-language message with what to do (AC-61).
- Timeout or provider error → message; the original prompt is untouched; generation is unaffected.
- Local model not installed → offered through the Models flow with its size.
- API key missing or rejected → asks for it; stored only in the Keychain (AC-62).
