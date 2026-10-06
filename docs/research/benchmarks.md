# Benchmarks — measured on real hardware

> Results of the sprint 1 spikes. Every number here was produced by a command in `spikes/` and read
> from its output; nothing is estimated. Machine: **Apple M5, 32 GB unified memory, macOS 27.0.1**.
> Models live outside the repository in `~/Library/Caches/MacWan-spikes/`.

## S-001 — mlx-video (IN PROGRESS: Wan2.1 1.3B and Wan2.2 TI2V-5B done; A14B, I2V mode and 8-bit pending)

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

### What the numbers mean for MacWan

1. **The memory peak is the text encoder, not the video model.** Loading and running UMT5-XXL costs
   about 23 GB at peak, whatever the model; denoising TI2V-5B in 4-bit needs 4.35 GB. The proposed
   tier table (built on transformer size) is therefore wrong as written: today even the smallest
   model peaks at 25–29 GB. A 16 GB or 24 GB Mac is only reachable by changing how T5 is handled —
   a quantized T5, encoding in a short-lived separate process, or caching embeddings. That is a new
   question for S-003 and it decides the minimum Mac.
2. **VAE decode is the second peak:** 15–26 GB for 17 frames at 1280×704 with `--tiling auto`. The
   other tiling modes are not measured yet.
3. **`mx.set_memory_limit` does not cap memory** (10 GB asked, 23–25 GB used). The plan of D-015 —
   approximating a 16 GB Mac by capping the engine — does not work as recorded (D-017).
4. **4-bit TI2V-5B is not usable at 10 steps** — strong colour and block artifacts where bf16 is
   clean with the same seed. 4-bit 1.3B is fine. Whether 8-bit or more steps fix it is not measured.
5. **4-bit buys disk, not speed:** seconds per step are the same as bf16 on this machine.
6. **About half of a short render is not denoising:** roughly 100 s (1.3B) to 140 s (5B) go to
   loading, T5 encoding, decoding and saving. A warm worker that keeps models loaded matters.
7. **Speed on an M5:** ≈ 10 s/step at 832×480 and ≈ 13 s/step at 1280×704, for 17 frames. Clips of
   81–121 frames and 40-step renders are not measured; do not extrapolate linearly.
8. **Generation calls the network:** `generate.py` runs `AutoTokenizer.from_pretrained("google/umt5-xxl")`
   and reaches the Hugging Face Hub on every run. MacWan must load the tokenizer from the files the
   model repository already ships and run offline (NFR-02).
9. **No progress or cancel API:** `generate_video` is one monolithic function with a `tqdm` loop.
   Replacing the module-level `tqdm` in-process (what the spike script does) gives per-step events
   and a place to raise for cancellation without parsing output. Phase events and previews need the
   worker to own the orchestration.
10. **T5 is written again into every converted model directory** (11.36 GB each — 45 GB across the
    four variants here). The shared-component dedupe in the plan is necessary, not optional.
11. **Upstream T5 and VAE weights are pickle (`.pth`), not safetensors.** The converter loads them
    with `torch.load(..., weights_only=True)`. The threat model is corrected accordingly.
12. **Dual-expert models load both experts at once** (read in `generate.py`; not yet measured). With
    the T5 peak above, A14B on 32 GB is doubtful and is the next thing to measure.

### Still to do in S-001

A14B q4 (≈ 126 GB download — next, D-013), I2V mode of TI2V-5B, 8-bit variants, 40-step quality,
longer clips (81 and 121 frames), tiling modes, and a T5-handling experiment for point 1.
