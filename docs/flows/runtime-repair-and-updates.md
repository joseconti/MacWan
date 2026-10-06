# Flow — Runtime repair and updates (F6)

- Trigger: Settings → Engines; an app update; a worker that fails its `hello` handshake.
- Covers: AC-50, AC-51, AC-53.

## Steps
1. Engines lists `uv`, Python, each environment and its package versions from `runtime/state.json`,
   cross-checked with the worker's `probe`.
2. Repair deletes the broken environment and re-runs the install steps for it; models and the
   library are untouched (AC-50).
3. App update: Sparkle finds a new version → verifies the EdDSA signature → installs (AC-53).
4. After an app update the shipped lockfiles are compared with `runtime/state.json`; a difference
   runs the runtime update at next launch, before any job (AC-51).

## Branches and failure paths
- Handshake protocol mismatch → the worker is not used; the runtime update runs.
- Repair fails → cause + Retry; the app stays usable for browsing the library.
- Update signature invalid → rejected, reported, nothing installed.
- Runtime update interrupted → resumes at the first incomplete step (same mechanism as F1).
