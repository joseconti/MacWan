# Wan-Video ecosystem — research reference

> Researched 2026-10-06 from the repositories' own READMEs, `requirements*.txt`, `pyproject.toml`
> and source (`generate.py`, `wan/configs/*`, `wan/modules/*`) on their `main` branches, plus the
> Hugging Face model pages. Anything marked **VERIFY** was not confirmed from a primary source and
> must be checked in the Phase 5 spikes before code depends on it.

## 1. What the organization is

`github.com/Wan-Video` is Alibaba Cloud's ("Tongyi Wanxiang") home for its open video generation
models. Weights live on Hugging Face under **`Wan-AI/`** and mirrored on ModelScope under
**`Wan-AI/`**. Everything open is **Apache-2.0** (code and weights). Generated content is owned by
the user, subject to the license's acceptable-use clause.

| Repo | What it is | Status | Relevance to MacWan |
|---|---|---|---|
| **Wan2.1** | First open generation (Feb 2025). T2V 1.3B/14B, I2V 14B (480P/720P), FLF2V 14B, VACE 1.3B/14B, T2I via the T2V model. Gradio demos. | Maintenance (last push Mar 2026) | **Include** — the only small model (1.3B) and the only FLF2V / VACE models. |
| **Wan2.2** | Current open generation (Jul 2025). MoE T2V/I2V "A14B", dense TI2V-5B, S2V-14B (speech-to-video), Animate-14B (character animation/replacement). | Active (Sep 2026) | **Include** — the core of the app. |
| **Wan-Animate-2** | Aug 2026 end-to-end character animation on a Wan2.2 base (Base + Distillation weights), text-driven viewpoint control. | New | **Include as "advanced / high-memory"** — tuned for 8×A800; diffusers support is still an open PR. |
| **Wan-Dancer** | Jul 2026 music-to-dance, minute-long 720p/30fps, built on Wan2.1 + DiffSynth-Studio. | New | **Out of v1** — CUDA 12.4, xfuser, tested on 8×A800 80 GB only. Revisit if a port appears. |
| **Wan-skills** | AI-agent skills (Claude-style `SKILL.md`) calling Alibaba's **cloud** API: `wan2.7-image-skill`, `wan-pptx-generator`. | Small | **Reference only** — shows the cloud API (DashScope / Model Studio) contract; feeds the optional cloud engine. |
| **diffusers** | A fork of `huggingface/diffusers`, last updated Feb 2025. | Stale fork | **Ignore** — use upstream `diffusers` from PyPI. |

### How they relate

```
                 Wan-AI weights on Hugging Face / ModelScope (Apache-2.0)
                                     │
  Wan2.1 (base gen 1) ──► Wan2.2 (base gen 2, MoE + 5B) ──► Wan-Animate-2 (2.2 base)
        │                                                     
        └──► Wan-Dancer (2.1 + DiffSynth)                     

  Wan 2.5 / 2.6 / 2.7 / 3.0  ──►  API-only on Alibaba Cloud Model Studio (no weights)
                                   └── Wan-skills wraps that API for agents
```

**Do they complement each other?** Yes. Each repo is a set of *tasks*; none supersedes another
completely. Wan2.2 is better than Wan2.1 at T2V/I2V, but Wan2.1 alone has the 1.3B model (runs on
modest Macs), First-Last-Frame-to-Video and VACE (all-in-one editing). Animate-2 supersedes Wan2.2
Animate in quality but needs far more memory. MacWan therefore exposes **tasks**, and picks the best
available model for each task (section 4).

### Open weights stopped at 2.2

Wan 2.5-Preview (Sep 2025), 2.6 (Dec 2025), 2.7 (Apr 2026) and 3.0 (Aug 2026) were released **only
as paid API** on Alibaba Cloud Model Studio. The newest downloadable base model is Wan2.2; the 2026
open releases (Animate-2, Dancer) are task models on the 2.2 / 2.1 base. MacWan's local engine is
therefore built on 2.1 + 2.2 (+ Animate-2), and newer models are reachable only through the optional
cloud engine (section 7).

## 2. Model catalogue (open weights)

Raw sizes are the Hugging Face repository totals of the **original** (non-diffusers) checkpoints.

| Task id (MacWan) | Model | HF repo | Resolutions | Frames / fps | Raw size | Notes |
|---|---|---|---|---|---|---|
| `t2v.small` | Wan2.1 T2V 1.3B | `Wan-AI/Wan2.1-T2V-1.3B` | 832×480 (720P unstable) | 81 / 16 | VERIFY (~17 GB incl. T5) | 8.19 GB VRAM on CUDA; best Mac entry point |
| `t2v.large.v21` | Wan2.1 T2V 14B | `Wan-AI/Wan2.1-T2V-14B` | 480P, 720P | 81 / 16 | VERIFY | superseded by 2.2 A14B |
| `i2v.v21` | Wan2.1 I2V 14B | `Wan-AI/Wan2.1-I2V-14B-480P` / `-720P` | 480P / 720P | 81 / 16 | VERIFY | superseded by 2.2 A14B |
| `flf2v` | Wan2.1 FLF2V 14B | `Wan-AI/Wan2.1-FLF2V-14B-720P` | 720P | 81 / 16 | VERIFY | first + last frame → video; **only source** |
| `vace.small` / `vace.large` | Wan2.1 VACE 1.3B / 14B | `Wan-AI/Wan2.1-VACE-1.3B` / `-14B` | 480P / 480P+720P | 81 / 16 | VERIFY | reference images, masks, inpaint/outpaint, pose/depth control |
| `t2v` | Wan2.2 T2V A14B (MoE) | `Wan-AI/Wan2.2-T2V-A14B` | 480P, 720P | 81 / 16 | **~126 GB** | two ~14B experts (high-noise, low-noise); only one active per step |
| `i2v` | Wan2.2 I2V A14B (MoE) | `Wan-AI/Wan2.2-I2V-A14B` | 480P, 720P | 81 / 16 | VERIFY (~126 GB) | aspect follows input image |
| `ti2v` | Wan2.2 TI2V 5B | `Wan-AI/Wan2.2-TI2V-5B` | **1280×704 / 704×1280 only** | **121 / 24** | **34.2 GB** | T2V and I2V in one model; Wan2.2-VAE 16×16×4; fastest 720P model |
| `s2v` | Wan2.2 S2V 14B | `Wan-AI/Wan2.2-S2V-14B` | 480P, 720P, 1024×704 … | audio-length / 16 | VERIFY | image + audio (+ pose video) → talking/singing video; optional CosyVoice TTS |
| `animate` | Wan2.2 Animate 14B | `Wan-AI/Wan2.2-Animate-14B` | 1280×720 | clips of 77 / 30 | VERIFY | animation or replacement mode; needs preprocessing (pose, face, mask; SAM2) |
| `animate2` | Wan-Animate-2 14B (Base / Distillation) | `Wan-AI/Wan2.2-Animate-2-14B` | 720P (480P on 2 GPUs) | 24 fps | VERIFY | consumes the driving video directly (no pose extractor); distilled = 10 steps, no CFG |
| *(out of v1)* | Wan-Dancer 14B | `Wan-AI/Wan-Dancer-14B` | 720P | 30 fps, >1 min | VERIFY | two-stage (global keyframes → local refine) |

Diffusers-format mirrors exist for most of them (`…-Diffusers` suffix): `Wan2.1-T2V-1.3B-Diffusers`,
`Wan2.1-T2V-14B-Diffusers`, `Wan2.1-I2V-14B-480P-Diffusers`, `Wan2.1-I2V-14B-720P-Diffusers`,
`Wan2.1-FLF2V-14B-720P-diffusers`, `Wan2.1-VACE-1.3B-diffusers`, `Wan2.1-VACE-14B-diffusers`,
`Wan2.2-T2V-A14B-Diffusers`, `Wan2.2-I2V-A14B-Diffusers`, `Wan2.2-TI2V-5B-Diffusers`,
`Wan2.2-Animate-14B-Diffusers`, and (Animate-2) `Wan2.2-Animate-2-14B-Diffusers` /
`Wan2.2-Animate-2-14B-Distilled-Diffusers`.

### Anatomy of a checkpoint (original format)

```
Wan2.2-TI2V-5B/                                 Wan2.2-T2V-A14B/ (and I2V-A14B)
├── models_t5_umt5-xxl-enc-bf16.pth  11.4 GB    ├── models_t5_umt5-xxl-enc-bf16.pth 11.4 GB
├── Wan2.2_VAE.pth                    2.8 GB    ├── Wan2.1_VAE.pth                  508 MB
├── diffusion_pytorch_model-0000N…   ~20 GB     ├── high_noise_model/   (≈14B params)
├── config.json                                  ├── low_noise_model/    (≈14B params)
└── google/ (umt5 tokenizer)                     └── google/
```

The **UMT5-XXL text encoder (5.68B params, 11.4 GB bf16) is identical in every model** — MacWan
must store it once and share it (dedupe by hash), not once per model.

### Quantized community weights (relevant for Mac memory)

- **GGUF** (QuantStack, used by ComfyUI-GGUF): `QuantStack/Wan2.2-TI2V-5B-GGUF` — Q4_K_M 3.43 GB,
  Q5_K_M 3.81 GB, Q8_0 5.4 GB. `QuantStack/Wan2.2-T2V-A14B-GGUF` — per expert Q4_K_M 9.65 GB,
  Q5_K_M 10.8 GB, Q8_0 15.4 GB.
- **MLX** conversion (mlx-video, see `apple-silicon-runtime.md`): 4-bit transformer ≈ 3.4× smaller —
  1.3B: 2.7 GB → 0.8 GB; 14B: ~28 GB → ~8 GB per transformer.
- **Distillation LoRAs**: `lightx2v/Wan2.2-Lightning` (4 steps, CFG 1) — the single biggest speed
  lever on slow hardware. LightX2V also publishes step-distilled and quantized Wan variants.

## 3. Installation & usage of the official repos (as documented)

### Wan2.1 / Wan2.2

```sh
git clone https://github.com/Wan-Video/Wan2.2.git && cd Wan2.2
pip install -r requirements.txt          # torch>=2.4, diffusers>=0.31, transformers 4.49–4.51.3,
                                         # accelerate, imageio[ffmpeg], flash_attn, numpy<2, dashscope
pip install -r requirements_s2v.txt      # S2V extras: openai-whisper, librosa, decord, CosyVoice deps…
pip install -r requirements_animate.txt  # Animate extras: decord, peft, onnxruntime, SAM2 (git)…
huggingface-cli download Wan-AI/Wan2.2-TI2V-5B --local-dir ./Wan2.2-TI2V-5B
# or: modelscope download Wan-AI/Wan2.2-TI2V-5B --local_dir ./Wan2.2-TI2V-5B
```

Python `>=3.10`. Wan2.1 additionally ships Gradio demos (`gradio/*.py`).

### `generate.py` (Wan2.2) — the canonical parameter surface

| Flag | Meaning | Default |
|---|---|---|
| `--task` | `t2v-A14B`, `i2v-A14B`, `ti2v-5B`, `s2v-14B`, `animate-14B` (Wan2.1: `t2v-1.3B`, `t2v-14B`, `i2v-14B`, `flf2v-14B`, `vace-1.3B`, `vace-14B`, `t2i-14B`) | `t2v-A14B` |
| `--size` | `W*H` from the per-task supported list (see below) | `1280*720` |
| `--frame_num` | frames, must be **4n+1** | model config (81; TI2V 121) |
| `--ckpt_dir` | checkpoint directory | required |
| `--prompt` / `--image` | text / input image (I2V, TI2V, S2V) | example prompt |
| `--base_seed` | seed (−1 = random) | −1 |
| `--sample_solver` | `unipc` or `dpm++` | `unipc` |
| `--sample_steps` | denoising steps | config (T2V/I2V 40, TI2V 50) |
| `--sample_shift` | flow-matching shift | config |
| `--sample_guide_scale` | CFG (Wan2.2 A14B: pair low/high) | config |
| `--offload_model`, `--convert_model_dtype`, `--t5_cpu` | memory reducers | off |
| `--use_prompt_extend`, `--prompt_extend_method {dashscope,local_qwen}`, `--prompt_extend_model`, `--prompt_extend_target_lang {zh,en}` | LLM prompt rewriting | off |
| S2V: `--audio`, `--enable_tts`, `--tts_prompt_audio`, `--tts_prompt_text`, `--tts_text`, `--pose_video`, `--num_clip`, `--infer_frames`, `--start_from_ref` | speech-to-video | — |
| Animate: `--src_root_path`, `--refert_num`, `--replace_flag`, `--use_relighting_lora` | animation / replacement | — |
| Multi-GPU: `--dit_fsdp`, `--t5_fsdp`, `--ulysses_size` (via `torchrun`) | CUDA only | — |

Supported sizes (`wan/configs/__init__.py`): T2V/I2V A14B `720*1280, 1280*720, 480*832, 832*480`;
TI2V-5B `704*1280, 1280*704`; S2V adds `1024*704, 704*1024, 704*1280, 1280*704`; Animate
`720*1280, 1280*720`. For I2V/TI2V/S2V the size is an **area** — the aspect follows the input image.

Default negative prompt is a long Chinese string (`wan_shared_cfg.sample_neg_prompt`); MacWan should
ship it as the default and let the user see/override it (an English translation shown alongside).

Official hardware notes: A14B single-GPU ≥ 80 GB VRAM; TI2V-5B ≥ 24 GB (RTX 4090) with
`--offload_model True --convert_model_dtype --t5_cpu`, "5 s of 720P in under 9 minutes";
Wan2.1 1.3B ≈ 8.19 GB, 5 s 480P in ~4 min on a 4090.

### Prompt extension (recommended by the Wan team)

Rewrites a short prompt into a detailed one. Two built-in methods: **DashScope** (`qwen-plus` for
text, `qwen-vl-max` for images; env `DASH_API_KEY`, intl `DASH_API_URL=https://dashscope-intl.aliyuncs.com/api/v1`)
or **local Qwen** (`Qwen2.5-14B/7B/3B-Instruct`, `Qwen2.5-VL-7B/3B-Instruct`). Wan-Animate-2 requires
an image caption in a fixed Chinese template produced by an LLM/VLM. → see `ai-assistant-cli.md`.

### Animate (2.2) preprocessing

`wan/modules/animate/preprocess/preprocess_data.py` turns (driving video, reference image) into
`src_pose.mp4`, `src_face.mp4` (+ `src_bg.mp4`, `src_mask.mp4` for replacement) using the
`process_checkpoint` shipped in the model repo (pose/face detectors, optional FLUX for retargeting,
SAM2 for masks). This is the heaviest and most CUDA-coupled part of the ecosystem.

### Wan-Animate-2

`git clone --recursive`, Python 3.11, torch 2.7 (cu126), `flash-attn`, `pip install -e .`, weights
`Wan-AI/Wan2.2-Animate-2-14B` to `./ckpts/`. Inference `infer/wan_animate_2_demo.py --prompt … --refer-img-file … --refer-video-file … --config wan_animate_2.yaml`
(distilled: `wan_animate_2_distillation.yaml --sample_guide_scale 1.0 --step 10`). Gradio demos
included. Diffusers `WanAnimate2Pipeline` is in diffusers PR #14412 — **not in upstream `main` as of
2026-10-06** (checked `src/diffusers/pipelines/__init__.py`).

### Wan-Dancer

Ubuntu 22.04, Python 3.10, torch 2.6 cu124, `flash_attn==2.6.3`, `xfuser==0.4.0`, `yunchang`,
shell scripts `gen_video_global.sh` → `gen_video_local.sh`, five dance genres via Chinese prompt
files. Excluded from v1 (see section 1).

## 4. Task → engine → model map for MacWan

| User-facing task | Primary model | Fallback for small Macs | Engine on Mac (see runtime doc) |
|---|---|---|---|
| Text → Video | Wan2.2 T2V A14B | Wan2.2 TI2V-5B, then Wan2.1 1.3B | MLX |
| Image → Video | Wan2.2 I2V A14B | Wan2.2 TI2V-5B | MLX |
| First + Last frame → Video | Wan2.1 FLF2V 14B | — | PyTorch-MPS (diffusers `WanImageToVideoPipeline`) |
| Edit / Control (VACE) | Wan2.1 VACE 14B | VACE 1.3B | PyTorch-MPS (diffusers `WanVACEPipeline`) |
| Video → Video (restyle) | Wan2.1 T2V + V2V | — | PyTorch-MPS (diffusers `WanVideoToVideoPipeline`) |
| Text → Image | Wan2.1 T2V 14B, 1 frame | — | MLX (frames=1) — VERIFY |
| Character Animate / Replace | Wan2.2 Animate 14B | — | PyTorch-MPS (diffusers `WanAnimatePipeline`) + preprocessing |
| Character Animate v2 | Wan-Animate-2 (Distilled) | — | PyTorch-MPS — **experimental**, gated on diffusers support + RAM |
| Speech → Video | Wan2.2 S2V 14B | — | **VERIFY** — no diffusers pipeline upstream; needs a port of `wan/speech2video.py` to MPS |
| Wan 2.5 → 3.0 (any task) | cloud | — | Cloud (Model Studio API), optional |

## 5. Sources

- https://github.com/Wan-Video (org page) · Wan2.1, Wan2.2, Wan-Animate-2, Wan-Dancer, Wan-skills READMEs (raw.githubusercontent.com, `main`)
- Wan2.2 source: `generate.py`, `wan/configs/__init__.py`, `wan/configs/wan_ti2v_5B.py`, `wan/configs/shared_config.py`, `wan/modules/attention.py`, `wan/modules/model.py`
- https://huggingface.co/Wan-AI/Wan2.2-TI2V-5B/tree/main · https://huggingface.co/Wan-AI/Wan2.2-T2V-A14B/tree/main
- https://huggingface.co/QuantStack/Wan2.2-TI2V-5B-GGUF · https://huggingface.co/QuantStack/Wan2.2-T2V-A14B-GGUF
- https://huggingface.co/docs/diffusers/main/en/api/pipelines/wan · diffusers `src/diffusers/pipelines/__init__.py`
- https://howaiworks.ai/blog/alibaba-wan-open-weights-stopped-at-2-2 (open vs API-only timeline)
- https://docs.comfy.org/tutorials/video/wan/wan2_2
