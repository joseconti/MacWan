# Threat model — MacWan

> Phase 2 artifact (step 4c), DRAFT with the technical plan. Profile: Keel `web-app` adapted to a
> desktop app. Kept current through Phase 5 and re-verified at the Phase 7 gate. **Only `IN PLACE`
> may be read as true today.** No product code exists yet, so nothing is `IN PLACE`.

## 1. Assumptions

- Public by construction: the app bundle, the worker's Python sources, the protocol, the catalogue
  and the list of hosts. Nothing relies on any of them being secret.
- The app is not sandboxed (D-005): it has the user's full file access. The trust boundary is the
  user's own account, not a sandbox.
- The app downloads and executes third-party code (Python packages) and loads third-party weights.
  That supply chain is the main attack surface.
- Adversaries: a network attacker between the Mac and a download host; a compromised or malicious
  upstream package or model repository; a malicious file the user is persuaded to open (LoRA,
  image, video, mask); another local process of the same user. A local attacker with the user's
  privileges or root is out of scope.
- Assets worth protecting: the integrity of what runs on the Mac, API keys and tokens, the user's
  prompts and media, the user's disk.

## 2. Defended

| Threat | Control | State |
|---|---|---|
| Tampered model file in transit or at rest | sha256 from the catalogue's pinned revision verified before use (AC-42) | TO BUILD — S-024 |
| Model repository changes under a fixed name | Hugging Face revision pinned by commit in the catalogue | TO BUILD — S-023 |
| Malicious or changed Python package | `uv sync --frozen` from lockfiles with hashes, shipped inside the signed app | TO BUILD — S-017, S-020 |
| Arbitrary code execution through pickle weights | `.safetensors` only for models and LoRAs; pickle formats refused | TO BUILD — S-024, S-044 |
| Tampered `uv` binary | pinned version, checksum verified at build time, shipped inside the signed bundle | TO BUILD — S-021 |
| Malicious app update | Sparkle 2 EdDSA signature + notarization (AC-53) | TO BUILD — S-060, S-069 |
| Tampered app bundle | hardened runtime, Developer ID signature, notarization | MANUAL — José's certificate; pipeline S-069 |
| Command injection through prompts, paths or CLI arguments | `Process` with argument arrays, never a shell; assistant CLIs called with fixed arguments | TO BUILD — S-018, S-055 |
| Path traversal through protocol or catalogue paths | every path validated to stay inside MacWan's data root or a user-chosen file | TO BUILD — S-018, S-024 |
| Requests to unexpected hosts | one closed host allow-list, HTTPS only | TO BUILD — S-024 |
| Secret leakage | Keychain only (AC-62); log scrubber; diagnostics exclude prompts and media by default (AC-70) | TO BUILD — S-056, S-059 |
| Prompt-injection through assistant output | output shown as a diff and treated as text, never executed (AC-60) | TO BUILD — S-057 |
| Memory exhaustion freezing the Mac | memory guard before every job (AC-12) | TO BUILD — S-032 |
| Disk exhaustion | free-space check before download and conversion; clean stop on `DISK_FULL` | TO BUILD — S-026 |
| Library validation weakened for the worker | entitlement `disable-library-validation` only if S-004 proves it necessary | VERIFY — S-004 |
| Quarantine or Gatekeeper blocking downloaded binaries | behaviour measured on a clean user | VERIFY — S-004 |

## 3. Not defended — and what to do if it matters

| Not covered | Consequence | What it would take |
|---|---|---|
| No app sandbox | a compromised worker has the user's full file access | impossible with a runtime installed at first launch (D-005); a sandboxed helper would be a redesign |
| Compromise of an upstream package at the pinned version | malicious code runs as the user | vendoring and auditing every wheel; reproducible builds |
| Malicious model weights exploiting a parser bug in `safetensors`, MLX or PyTorch | code execution as the user | running inference in a VM or a restricted process |
| Content safety of generated video | the app does not filter what is generated; it shows the model licence's acceptable-use terms | a moderation model in the pipeline |
| Provenance of generated media | no watermark or C2PA signing | C2PA manifest at export |
| Local attacker with the user's account | can read the library, prompts and the Keychain items the user can read | FileVault and a locked session — the user's machine hygiene |
| Encryption at rest of the library and logs | relies on FileVault | an app-level encrypted store |
| Third-party LLM providers seeing prompts and images | when the user enables one, its provider receives what is sent | keep the assistant Off or use the local provider |
| Availability of Hugging Face and ModelScope | downloads fail when both are down | an own mirror |
| Media decoders (AVFoundation, ffmpeg) parsing hostile files | decoder bugs are the platform's | sandboxed decoding |

## 4. Security audit derivation

`Security audit: optional` — no money moves, no personal data is collected or sent anywhere by the
app, and no programmatic surface is reachable from outside (the worker speaks over stdio to its
parent only). Recomputed if scope changes: the deferred cloud engine (S-075) or agent/MCP control
(S-079) would flip it to `required`. Given the supply-chain surface, an audit is still offered at
S-068.
