# Competitive landscape — MacWan

> Phase 1 step 0. Scanned 2026-10-06. Facts are from the products' pages and docs listed in
> Sources; anything not confirmed is marked VERIFY.

## Who already lets a Mac user run Wan

| Product | Type | Wan coverage | Setup cost for a non-developer | Gaps MacWan can fill |
|---|---|---|---|---|
| **Draw Things** | Native iOS/macOS app (App Store), free, Metal-optimised | Wan 2.1 and 2.2 (T2V, I2V, 5B) — wiki page "Wan 2.2"; 24 GB+ recommended for video | Low (App Store) | General image app first, video second; no S2V / Animate / VACE task flows (VERIFY); no queue/project workflow around Wan; closed source |
| **ComfyUI Desktop** | Node-graph app (Electron + Python) | Every Wan task via native nodes, Kijai's WanVideoWrapper, GGUF | High — graphs, custom nodes, model folders, fp8 files that crash on MPS (issue #9255) | MacWan hides graphs behind task screens and picks Mac-safe weights automatically |
| **mlx-video** (CLI) | Python package | Wan2.1/2.2 T2V, I2V, TI2V; LoRA; 4-bit | High — Terminal, Python, manual download + conversion | MacWan uses it as an engine and puts a UI, downloads and conversion on top |
| **mlx-gen**, **mlx-video-gen**, **mlx-video-rs** | CLI / scripts | Wan2.2 5B / 14B subsets | High | same as above |
| **Pinokio** (Wan2GP and others) | One-click script launcher, browser UI | Wan via Gradio apps; Wan2GP is CUDA-centric (VERIFY Mac support) | Medium | Not native, browser UI, CUDA assumptions |
| **wan.video / Model Studio** | Alibaba cloud (web + API) | Wan 2.5–3.0 (API-only models) and older | Low, paid | No privacy/offline; MacWan can integrate it as an optional engine |
| **Generic cloud apps** (Magic Hour, getimg, RunComfy…) | SaaS | Wan 2.2 hosted | Low, paid | Not local |

## Confrontation — what each competitor does that MacWan's v1 must answer

| Functionality | Who has it | Demand evidence | MacWan v1 | Cost (AI time) |
|---|---|---|---|---|
| T2V / I2V with Wan2.2 locally | Draw Things, ComfyUI, mlx-video | Core of every Wan Mac guide and video | **Yes** | in core estimate |
| Automatic Mac-safe weights (no fp8 crash) | none automatic | ComfyUI #9255 and many forum threads | **Yes** — capability table picks MLX/GGUF | in core |
| First-run installer that needs no Terminal | Draw Things (no Python) | the user's own requirement | **Yes** | high (runtime manager) |
| Fast preview (Lightning 4-step LoRA) | ComfyUI, mlx-video | widely used in community workflows | **Yes** ("Draft" quality preset) | low |
| FLF2V, VACE | ComfyUI | ComfyUI official workflows | **Yes, Pro tier** | medium |
| Character Animate / Replace | ComfyUI (Kijai), HF Space | Wan2.2-Animate launch traction | **Experimental**, gated by RAM | high |
| Speech-to-Video | ComfyUI, HF Space | S2V launch | **Deferred to v1.x** (no Mac-capable pipeline yet) | high, uncertain |
| Node graphs / custom pipelines | ComfyUI | power users | **No** — not MacWan's audience | — |
| Cloud fallback for newest Wan | wan.video | open weights stopped at 2.2 | **Optional engine, v1.x** | medium |
| LoRA library | ComfyUI, mlx-video | large LoRA ecosystem | **Basic** (load a .safetensors LoRA) | low |

## Honest assessment

Draw Things is the real competitor: native, free, fast, already supports Wan 2.2. MacWan only has a
reason to exist if it is **the most complete Wan app on the Mac** — every open Wan task, not only
T2V/I2V — with a zero-Terminal installer, hardware-aware model choice and a render queue. If v1
shipped only T2V/I2V it would be a worse Draw Things. The proposed v1 (`docs/01-discovery.md`)
therefore includes FLF2V and VACE and treats Animate as experimental.

## Sources

- https://wiki.drawthings.ai/wiki/Wan_2.2 · https://www.heyuan110.com/posts/ai/2026-02-15-draw-things-ultimate-guide/
- https://docs.comfy.org/tutorials/video/wan/wan2_2 · https://github.com/Comfy-Org/ComfyUI/issues/9255
- https://github.com/Blaizzy/mlx-video · https://github.com/lpalbou/mlx-gen · https://github.com/garvitkhurana/mlx-video-gen · https://github.com/bhubbard/mlx-video-rs
- https://howaiworks.ai/blog/alibaba-wan-open-weights-stopped-at-2-2
