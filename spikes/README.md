# spikes/ — throwaway sprint 1 experiments

Never app code. Each script answers one question from `docs/03-technical-plan.md` §9 and its
numbers go to `docs/research/benchmarks.md`. Models live outside the repository, in
`~/Library/Caches/MacWan-spikes/`.

- `pyproject.toml` / `uv.lock` — the pinned spike environment (`uv sync`).
- `s001_generate.py` — S-001: runs one `mlx-video` Wan render in-process, hooking the denoising
  loop for per-step timing, and prints one JSON line with seconds per step and MLX peak memory.
