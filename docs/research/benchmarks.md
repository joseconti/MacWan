# Benchmarks — measured on real hardware

> Results of the sprint 1 spikes. Every number here was produced by a command in `spikes/` and read
> from its output; nothing is estimated. Machine: **Apple M5, 32 GB unified memory, macOS 27.0.1**.
> Models live outside the repository in `~/Library/Caches/MacWan-spikes/`.

## S-001 — mlx-video (IN PROGRESS: Wan2.1 1.3B, Wan2.2 TI2V-5B and A14B measured, memory peaks explained; long clips pending)

Measured 2026-10-06. Environment (`spikes/pyproject.toml` + `spikes/uv.lock`): CPython 3.12,
`uv` 0.12.23, `mlx` 0.32.3, `torch` 2.14.1, `transformers` 5.19.0, `huggingface_hub` 1.33.0,
`mlx-video` at commit `87db56a51758fefb748a359b90a5283bb8ba4837` (pinned, D-016).

### Pinned facts

- **Real module paths: `mlx_video.models.wan_2.convert` and `mlx_video.models.wan_2.generate`.**
  Neither `mlx_video.wan2` nor `mlx_video.wan_2` (the two spellings in the upstream README) exists
  at this commit.
- Hugging Face revisions used: `Wan-AI/Wan2.1-T2V-1.3B` @ `37ec512624d61f7aa208f7ea8140a131f93afc9a`,
  `Wan-AI/Wan2.2-TI2V-5B` @ `921dbaf3f1674a56f47e83fb80a34bac8a8f203e`.
- Both models convert and generate on this Mac. First render: a recognisable, coherent clip from
  Wan2.1 1.3B (frame inspected by eye).

### Download and conversion

| Model | Download | Time (unauthenticated) | Variant | Convert time | Convert peak RSS | On disk | Transformer / T5 / VAE |
|---|---|---|---|---|---|---|---|
| Wan2.1 T2V 1.3B | 16 GB | 4 min 34 s | mlx-q4 | 245 s | 5.6 GB | 12 GB | 0.84 / 11.36 / 0.51 GB |
| | | | mlx-bf16 | 252 s (a download was running) | 5.3 GB | 14 GB | 2.84 / 11.36 / 0.51 GB |
| Wan2.2 TI2V-5B | 32 GB | 9 min 5 s | mlx-q4 | 184 s | 6.7 GB | 16.0 GB | 2.95 / 11.36 / 2.82 GB |
| | | | mlx-bf16 | 145 s | 6.9 GB | 22.5 GB | 10.00 / 11.36 / 2.82 GB |

### Generation (`spikes/s001_generate.py`, T2V, 17 frames, 10 steps, `unipc`, seed 42)

| Model / variant | Size | Total | First step | Steady s/step | MLX peak | Peak by phase: load+encode / denoise / decode+save | Result |
|---|---|---|---|---|---|---|---|
| 1.3B mlx-q4 | 832×480 | 207.8 s | 15.8 s | 10.18 | 27.09 GB | not split in this run | clean |
| 1.3B mlx-bf16 | 832×480 | 194.9 s | 11.4 s | 10.40 | 28.95 GB | not split in this run | clean |
| 1.3B mlx-q4, `set_memory_limit(10 GB)` | 832×480 | 209.3 s | 11.5 s | 10.75 | 24.77 GB | not split in this run | identical frames |
| 5B mlx-q4 | 1280×704 | 390.5 s | 11.2 s | 12.93 | 23.68 GB | not split in this run | **heavy artifacts** |
| 5B mlx-q4, `set_memory_limit(10 GB)` | 1280×704 | 299.4 s | 14.9 s | 13.90 | 23.12 GB | **23.12 / 4.35 / 15.39 GB** | identical frames |
| 5B mlx-bf16 | 1280×704 | 268.6 s | 11.4 s | 12.99 | 26.02 GB | **23.68 / 10.92 / 26.02 GB** | clean |

The 1.3B clips came out with 20 frames for 17 requested; the 5B clips with 17. Not explained yet (VERIFY).

### Where the memory goes — the text encoder and the VAE, not the video model

`mlx-video` upcasts the 11.4 GB bf16 UMT5-XXL weights to float32 at load. `spikes/s001_t5.py` loads
the same encoder four ways (`spikes/t5_variants.py`), each in its own process, and compares the
embeddings of two prompts (one English, one Spanish) with the float32 reference:

| T5 loading | Peak | Load + encode | Cosine vs float32 | Relative error |
|---|---|---|---|---|
| float32 (upstream) | 23.68 GB | 25.1 s | 1 | 0 |
| bf16 (weights as stored) | 11.12 GB | 3.0 s | 0.9998 / 0.9996 | 1.9 % / 2.7 % |
| 8-bit (quantized after a bf16 load) | 8.14 GB (5.63 GB once quantized) | 2.3 s | 0.9982 / 0.9986 | 6.0 % / 5.3 % |
| 4-bit | 5.68 GB (2.98 GB once quantized) | 2.0 s | 0.877 / 0.875 | 51 % — degraded |

Full renders with the lighter loaders and VAE tiling (17 frames, `unipc`, seed 42, per-phase peaks):

| Model / variant | T5 | Tiling | Steps | Total | s/step | Load+encode / denoise / decode+save | **Peak** | Result (frame inspected) |
|---|---|---|---|---|---|---|---|---|
| 1.3B mlx-q4, 832×480 | 8-bit | auto | 10 | 137.1 s | 8.65 | 8.14 / 2.06 / 27.09 GB | 27.09 GB | clean (differs from the float32 render: 12.5 dB) |
| 1.3B mlx-q4, 832×480 | bf16 | auto | 10 | 367.8 s | 10.94 | 11.13 / 2.06 / 27.09 GB | 27.09 GB | clean (25.8 dB vs float32 — same shot) |
| **1.3B mlx-q4, 832×480** | **8-bit** | **aggressive** | 10 | 258.3 s | 10.32 | 8.14 / 2.06 / 8.62 GB | **8.62 GB** | **clean** |
| 5B mlx-bf16, 1280×704 | bf16 | auto | 10 | 260.1 s | 14.46 | 11.12 / 10.91 / 26.02 GB | 26.02 GB | clean (33.0 dB vs float32) |
| 5B mlx-bf16, 1280×704 | bf16 | aggressive | 10 | 365.3 s | 14.20 | 11.12 / 10.96 / 15.56 GB | 15.56 GB | clean (44.8 dB vs untiled) |
| 5B mlx-q8, 1280×704 | bf16 | aggressive | 10 | 431.4 s | 16.59 | 11.12 / 6.63 / 11.71 GB | 11.71 GB | **artifacts** |
| 5B mlx-q4, 1280×704 | bf16 | aggressive | **40** | 991.3 s | 14.97 | 11.12 / 4.39 / 9.42 GB | 11.12 GB | **clean** |
| 5B mlx-q8, 1280×704, **I2V** | bf16 | aggressive | 10 | 482.2 s | 18.77 | 11.13 / 8.38 / 11.72 GB | 11.72 GB | runs; last frame washed out |

TI2V-5B 8-bit: converted in 156 s, 18.3 GB on disk. Aggressive tiling changes the picture by less
than the eye can see (43.5–44.8 dB against the untiled decode) and costs 100–120 s of decode time
on these clips. Totals vary with what else the machine was doing; s/step is the steadier figure.

### Wan2.2 T2V A14B (dual expert), 4-bit

Download: 118 GB on disk in 27 min 36 s (revision `c8c270b13ee05bfa474194ac9fb07a5868a97cea`).
Conversion to 4-bit: 714 s, peak RSS 9.6 GB, 26.7 GB on disk (two experts of 8.38 GB + T5 11.36 GB
+ VAE 0.51 GB). Renders with T5 bf16, aggressive tiling, 17 frames requested (20 delivered), 10 steps:

| Size | Total | First step | Steady s/step | Load+encode / denoise / decode+save | Peak | Result |
|---|---|---|---|---|---|---|
| 832×480 | 917.4 s (15 min) | 107.6 s | 82.4 | 17.22 / 20.36 / 23.46 GB | 23.46 GB | clean |
| 1280×720 | 2341.2 s (39 min) | 256.1 s | 217.5 | 17.23 / 24.47 / 23.64 GB | 24.47 GB | clean, the best picture of the three models |

Both experts are resident for the whole render (measured: 17–24 GB even in 4-bit). On this 32 GB
Mac the result is correct but **six to sixteen times slower per step than TI2V-5B** at the same
size, which points at memory pressure rather than raw compute; it is not a usable experience here.
Loading one expert at a time is the obvious experiment and is not done yet.

### What the numbers mean for MacWan

1. **The two memory peaks are the text encoder and the VAE decode, and both are avoidable.** The
   upstream defaults peak at 23–29 GB on every model. With T5 held in bf16 or 8-bit and tiled
   decoding, Wan2.1 1.3B renders in **8.6 GB** and TI2V-5B in **9.4–15.6 GB**. The denoising itself
   is small: 2.1 GB (1.3B 4-bit), 4.4 GB (5B 4-bit), 6.6–8.4 GB (5B 8-bit), 10.9 GB (5B bf16).
2. **MacWan must own the T5 loading and the tiling choice** — neither is an `mlx-video` option worth
   relying on. Recommended defaults from these runs: T5 in bf16 (8-bit, shipped pre-quantized, when
   memory is tight), tiling chosen by the memory guard. 4-bit T5 is out.
3. **A 16 GB Mac is plausible for Wan2.1 1.3B and TI2V-5B 4-bit, but unverified:** these peaks were
   measured on a 32 GB machine, and `mx.set_memory_limit` does not cap usage (10 GB asked, 23–25 GB
   used), so a smaller Mac cannot be simulated here (D-015, D-017, D-018).
4. **Quantized TI2V-5B needs steps.** At 10 steps bf16 is clean and both 4-bit and 8-bit are full of
   artifacts; 4-bit at 40 steps is clean. The Draft preset cannot be "quantized 5B at 10 steps".
5. **Quantizing buys memory and disk, not speed:** seconds per step are equal or worse than bf16.
6. **Speed on an M5 (17 frames):** ≈ 10 s/step at 832×480, ≈ 13–15 s/step at 1280×704. A clean
   40-step 17-frame 720p clip took 16.5 min. Clips of 81–121 frames are not measured; do not
   extrapolate linearly.
7. **A large part of a short render is not denoising** — loading, encoding, decoding and saving.
   T5 in bf16 encodes in 3 s instead of 25 s; a warm worker removes most of the rest.
8. **Generation calls the network:** `generate.py` runs `AutoTokenizer.from_pretrained("google/umt5-xxl")`
   and reaches the Hugging Face Hub on every run. MacWan must load the tokenizer from the files the
   model repository already ships and run offline (NFR-02).
9. **No progress or cancel API:** `generate_video` is one monolithic function with a `tqdm` loop.
   Replacing module-level names in-process (what the spike scripts do for `tqdm` and
   `load_t5_encoder`) gives per-step events, a place to raise for cancellation, and the T5 change,
   without forking the package. Phase events and previews need the worker to own the orchestration.
10. **T5 is written again into every converted model directory** (11.36 GB each — 68 GB across the
    six variants here). The shared-component dedupe in the plan is necessary, not optional.
11. **Upstream T5 and VAE weights are pickle (`.pth`), not safetensors.** The converter loads them
    with `torch.load(..., weights_only=True)`. The threat model is corrected accordingly.
12. **I2V works** on TI2V-5B through the same entry point; its quality at low steps with a quantized
    model is poor and needs the same 40-step check.
13. **A14B is not a 32 GB model as the engine stands.** It renders correctly in 4-bit but holds
    both experts in memory (23–24 GB peak) and takes 15–39 minutes for a 17-frame, 10-step clip.
    Offering it on the Standard tier, as the proposed table did, is not supported by the data;
    it belongs to 48 GB and above unless expert swapping brings it down.

### Still to do in S-001

Longer clips (81 frames running; 121 pending), 1.3B and 5B at their default step counts, I2V at
40 steps, a pre-quantized 8-bit T5 file loaded directly, and A14B with one expert loaded at a time.
