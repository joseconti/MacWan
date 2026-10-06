"""S-001 spike: one mlx-video Wan render, measured.

Runs generate_video in-process and replaces the module-level tqdm of the denoising loop with a
timing iterator that also records MLX peak memory per phase — the same hook MacWan's worker can use for progress events and cancellation
without parsing any CLI output. Prints one JSON line.

  uv run python s001_generate.py <model-dir> <out.mp4> [--width W --height H --frames N --steps S]
                                 [--memory-limit-gb G] [--image PATH]
"""
import argparse
import json
import resource
import time

import mlx.core as mx
from mlx_video.models.wan_2 import generate as wan_generate

parser = argparse.ArgumentParser()
parser.add_argument("model_dir")
parser.add_argument("output")
parser.add_argument("--width", type=int, default=832)
parser.add_argument("--height", type=int, default=480)
parser.add_argument("--frames", type=int, default=17)
parser.add_argument("--steps", type=int, default=10)
parser.add_argument("--image")
parser.add_argument("--memory-limit-gb", type=float)
parser.add_argument("--prompt", default="A red fox running through fresh snow, cinematic, golden hour")
args = parser.parse_args()

if args.memory_limit_gb:
    mx.set_memory_limit(int(args.memory_limit_gb * 1024**3))

step_times = []
phase_peak = {}


def mark(phase):
    phase_peak[phase] = round(mx.get_peak_memory() / 1024**3, 2)
    mx.reset_peak_memory()


def timed(iterable, **_kwargs):
    mark("load_and_encode_gb")
    last = time.perf_counter()
    for item in iterable:
        yield item
        mx.eval()  # the loop evaluates lazily; the wall time between yields is what a user waits
        now = time.perf_counter()
        step_times.append(now - last)
        last = now
    mark("denoise_gb")


wan_generate.tqdm = timed
mx.reset_peak_memory()
started = time.perf_counter()
wan_generate.generate_video(
    model_dir=args.model_dir, prompt=args.prompt, image=args.image, width=args.width,
    height=args.height, num_frames=args.frames, steps=args.steps, seed=42,
    output_path=args.output, scheduler="unipc",
)
total = time.perf_counter() - started
mark("decode_and_save_gb")
steady = step_times[1:] or step_times
print(json.dumps({
    "model_dir": args.model_dir, "width": args.width, "height": args.height, "frames": args.frames,
    "steps": args.steps, "memory_limit_gb": args.memory_limit_gb,
    "total_s": round(total, 1), "first_step_s": round(step_times[0], 2) if step_times else None,
    "steady_s_per_step": round(sum(steady) / len(steady), 2) if steady else None,
    "mlx_peak_gb": max(phase_peak.values()), **phase_peak,
    "max_rss_gb": round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024**3, 2),
}))
