# Running Wan on Apple Silicon — research reference

> Researched 2026-10-06. Conclusions marked **VERIFY** are reasoned from source code or secondary
> sources and must be proven in the Phase 5 spikes (`docs/03-technical-plan.md` §9) before the
> architecture is frozen.

## 1. Bottom line

**The official Wan repos do not run on a Mac as published.** They are CUDA-only by construction.
MacWan must run the models through Mac-capable runtimes instead, and use the official repos as the
reference for parameters, defaults and behaviour:

1. **MLX** (Apple's array framework, Metal-native) via the community package **`mlx-video`** —
   primary engine for Wan2.1 / Wan2.2 T2V, I2V, TI2V. Supports 4-bit/8-bit quantization and LoRA
   (Lightning 4-step). Fastest path and smallest memory.
2. **PyTorch on MPS** via upstream **`diffusers`** — secondary engine for the tasks MLX does not
   cover (FLF2V, VACE, V2V, Animate). Diffusers already special-cases MPS in the Wan transformer.
3. **Cloud** (Alibaba Model Studio API) — optional, for Wan 2.5–3.0 and for Macs too small for a task.

## 2. Why the official code fails on Mac (source evidence)

| Blocker | Where | Effect on MPS |
|---|---|---|
| `flash_attn` is a hard requirement | `requirements.txt`, `pyproject.toml` | FlashAttention is CUDA-only; `pip install` fails on macOS. |
| `flash_attention()` asserts `q.device.type == 'cuda'` and the DiT calls it **directly** | `wan/modules/attention.py`, `wan/modules/model.py` (lines ~145, ~175) | The SDPA fallback exists only in `attention()`, which the model does not use. |
| RoPE computed in **float64 / complex128** (`torch.polar`, `view_as_complex(...float64)`) | `wan/modules/model.py` `rope_params`, `rope_apply` | MPS has no float64/complex128 support. |
| `torch.cuda.set_device`, `torch.cuda.synchronize`, `torch.cuda.empty_cache`, `torch.amp.autocast('cuda')`, `device = torch.device(f"cuda:{id}")` | `generate.py`, `wan/text2video.py`, `wan/textimage2video.py` … | Hard-coded CUDA device everywhere. |
| fp8 (`Float8_e4m3fn`) checkpoints (ComfyUI's `*_fp8_scaled`) | ComfyUI repackaged weights | MPS has no fp8 — ComfyUI issue #9255; workaround is GGUF. |
| `decord`, `xfuser`, `yunchang`, CUDA wheels | Animate, Dancer, Animate-2 requirements | No (or poor) macOS arm64 wheels — VERIFY per package. |

A patched fork of the official code is possible (`osama-ata/Wan2.2-mlx` and others exist), but
maintaining a fork of research code is the most expensive option; MacWan avoids it.

Diffusers, by contrast, already does `freqs_dtype = torch.float32 if torch.backends.mps.is_available() else torch.float64`
in `transformer_wan.py` and uses PyTorch SDPA — the MPS-specific fixes are upstream.

## 3. Engine A — MLX via `mlx-video` (primary)

- Repo: `github.com/Blaizzy/mlx-video` (MIT). Models: Wan2.1 (1.3B, 14B), Wan2.2 (T2V-A14B dual,
  I2V-A14B dual, TI2V-5B), plus LTX-2. No tagged releases — **pin a commit SHA**.
- Requirements: macOS on Apple Silicon, Python ≥ 3.11, `mlx` ≥ 0.22 (PyPI latest 0.32.3 on
  2026-10-06), PyTorch only for weight conversion.
- Install: `uv pip install git+https://github.com/Blaizzy/mlx-video.git@<sha>`

Workflow (download original weights → convert → generate):

```bash
huggingface-cli download Wan-AI/Wan2.2-TI2V-5B --local-dir ./Wan2.2-TI2V-5B
python -m mlx_video.wan2.convert --checkpoint-dir ./Wan2.2-TI2V-5B --output-dir ./Wan2.2-TI2V-5B-MLX-Q4 \
       --quantize --bits 4 --group-size 64          # --dtype bfloat16 default; --model-version auto
python -m mlx_video.wan2.generate --model-dir ./Wan2.2-TI2V-5B-MLX-Q4 \
       --image ./in.png --prompt "…" --width 1280 --height 704 --num-frames 41 \
       --steps 40 --guide-scale 5.0 --seed 42 --output-path out.mp4
```

- The converter writes `config.json`, `t5_encoder.safetensors`, `vae.safetensors`,
  (`vae_encoder.safetensors` for I2V), `model.safetensors` (2.1) or `high_noise_model.safetensors` +
  `low_noise_model.safetensors` (2.2). Quantization targets attention + FFN (~95 % of weights).
  `--quantize-only` re-quantizes an existing MLX dir.
- Generate flags: `--model-dir --prompt --image --negative-prompt --width --height --num-frames (4n+1)
  --steps --guide-scale (float or "high,low") --shift --seed --output-path --scheduler {euler,dpm++,unipc}
  --trim-first-frames --tiling {auto,none,spatial,temporal} --lora-high <path> <scale> --lora-low <path> <scale>`.
- Defaults per model: Wan2.1 50 steps/shift 5/CFG 5; Wan2.2 T2V 40/12/"3.0,4.0"; I2V 40/5/"3.5,3.5";
  TI2V 40/5/5. Upstream notes **10 steps with `unipc` is often enough** for fast previews.
- Sizes: 4-bit 1.3B ≈ 0.8 GB, 4-bit 14B ≈ 8 GB per transformer.
- **VERIFY:** the README uses both `mlx_video.wan2.*` and `mlx_video.wan_2.*` module paths — the
  spike must pin the real entry points at the chosen SHA. MacWan must not shell out to the CLI; it
  imports the package from its own worker (§6) so progress and cancellation are observable.
- Gap: no FLF2V, VACE, V2V, S2V, Animate in MLX today.

## 4. Engine B — PyTorch MPS via `diffusers` (secondary)

- Upstream pipelines (checked `src/diffusers/pipelines/__init__.py`, `main`, 2026-10-06):
  `WanPipeline`, `WanImageToVideoPipeline` (incl. FLF2V via `last_image`), `WanVACEPipeline`,
  `WanVideoToVideoPipeline`, `WanAnimatePipeline`. **No S2V pipeline and no `WanAnimate2Pipeline`
  upstream yet** (Animate-2 is diffusers PR #14412).
- Versions on PyPI (2026-10-06): `diffusers` 0.41.0, `torch` 2.14.1 — pin exact versions in the lockfile.
- Recommended dtypes: transformer and text encoder bf16, **VAE float32**.
- Memory tools: `pipe.enable_model_cpu_offload()`, group offloading, `from_single_file()`,
  GGUF loading (`GGUFQuantizationConfig`) — on Apple Silicon "CPU" and "GPU" share unified memory, so
  offload saves less than on CUDA; the real lever is quantized weights (GGUF Q4–Q8). VERIFY which
  offload modes actually reduce peak RSS on MPS.
- Set `PYTORCH_ENABLE_MPS_FALLBACK=1` so the rare unsupported op falls back to CPU instead of
  crashing; log every fallback (they are slow) so the spike can find them.
- Wan2.2-Animate preprocessing (pose/face detectors, SAM2) is the largest unknown on MPS — VERIFY.

## 5. Memory model and hardware tiers

Apple Silicon has **unified memory**: model weights, activations and the OS share one pool. macOS
lets the GPU wire only part of it (default ≈ 65–75 %, VERIFY per machine via
`recommendedMaxWorkingSetSize`). Peak = transformer(s) resident + T5 (11.4 GB bf16, can be
unloaded after encoding) + VAE decode (large at 720P; tiling reduces it) + activations.

Proposed tiers (to be **measured** in spike S-003 and then written into the app's capability table):

| Unified memory | Tier | Comfortable local tasks (proposal) |
|---|---|---|
| < 16 GB / Intel Mac | unsupported | cloud engine only |
| 16 GB | **Entry** | Wan2.1 T2V 1.3B (480P), TI2V-5B 4-bit at short lengths |
| 24–36 GB | **Standard** | TI2V-5B bf16/8-bit 720P; A14B T2V/I2V 4-bit (experts loaded one at a time) |
| 48–64 GB | **Pro** | A14B 8-bit, FLF2V / VACE 14B (GGUF), Animate 14B experimental |
| ≥ 96 GB | **Studio** | everything local incl. Animate-2 experimental, longer clips, 720P without tiling |

Wan2.2 MoE detail: only one expert is active per step (switch at the SNR boundary), so a careful
runtime loads high-noise → runs early steps → frees it → loads low-noise. mlx-video handles the dual
pipeline; whether it frees the first expert is a spike question.

Disk: originals are huge (A14B ≈ 126 GB, TI2V-5B 34 GB). MacWan downloads the original, converts,
then deletes the original by default (keeping only the converted, optionally quantized, copy), and
shares the T5 encoder and VAEs across models. Require free space ≥ (download + converted) before
starting; show it in the download sheet.

Speed: no trustworthy published Mac benchmarks for Wan exist (searched). MacWan measures its own
on first run (a tiny benchmark render) and shows time estimates from those measurements.

## 6. Recommended process model

```
MacWan.app (Swift/SwiftUI, sandbox OFF, Developer ID + notarized)
  └─ spawns ──► ~/Library/Application Support/MacWan/runtime/venv-<engine>/bin/python -m macwan_worker
                    stdin  ← JSON-lines commands  (generate, cancel, convert, probe, shutdown)
                    stdout → JSON-lines events    (progress step/total, phase, log, preview frame path, result, error)
```

- One long-lived worker per engine keeps weights warm between renders; idle timeout unloads them.
- `macwan_worker` is MacWan's own small Python package (shipped in the app bundle, versioned with
  the app) that imports `mlx_video` / `diffusers` — never parse CLI stdout.
- Cancellation: a `cancel` command checked between denoising steps; hard-kill after a grace period.
- Python runtime: a bundled **`uv`** binary installs a standalone CPython (python-build-standalone)
  and creates locked venvs from `uv.lock` files shipped in the app — reproducible, no Homebrew, no
  system Python, no Xcode CLT. `ffmpeg` comes from `imageio-ffmpeg` wheels (VERIFY licence: LGPL
  build) or a bundled static arm64 build.

## 7. Engine C — cloud (optional)

Alibaba Cloud Model Studio ("DashScope") hosts Wan 2.5 → 3.0. Wan 2.7 I2V example:
`POST https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis`
with `Authorization: Bearer $DASHSCOPE_API_KEY` and `X-DashScope-Async: enable`, model
`wan2.7-i2v-2026-04-25`, body `prompt` (≤ 5000 chars), `resolution` `720P|1080P`, `duration` 2–15 s,
`prompt_extend`, `media[]` (first_frame, last_frame, driving_audio, first_clip); then poll
`GET /tasks/{task_id}` (~15 s interval, task valid 24 h); result `video_url` valid 24 h. Paid,
per-second pricing (see Model Studio pricing page). The key lives in the macOS Keychain, never in
files or logs. Endpoint shapes and model ids change per release — VERIFY at implementation time.

## 8. Existing Mac-native alternatives (for positioning — see `docs/00-competitive-landscape.md`)

Draw Things (App Store, supports Wan 2.1/2.2 incl. 5B), ComfyUI Desktop (works with GGUF Wan on
Mac), `mlx-video` CLI, `mlx-gen`, `mlx-video-rs` (Rust MLX port), Pinokio one-click installers.

## 9. Sources

- Wan2.2 `wan/modules/attention.py`, `wan/modules/model.py`, `generate.py`, `wan/textimage2video.py` (main)
- https://github.com/Blaizzy/mlx-video and `mlx_video/models/wan_2/README.md`
- diffusers `src/diffusers/models/transformers/transformer_wan.py` (line ~375, MPS float32 RoPE)
- https://github.com/Comfy-Org/ComfyUI/issues/9255 (fp8 unsupported on MPS → GGUF)
- https://www.alibabacloud.com/help/en/model-studio/image-to-video-general-api-reference
- PyPI JSON for `mlx`, `diffusers`, `torch`, `mlx-lm` (versions on 2026-10-06)
