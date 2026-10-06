"""S-001/S-003 spike: peak memory and embedding fidelity of each T5 loading mode.

  uv run python s001_t5.py <model-dir> <mode> <out.npz>     one mode, in its own process
Prints one JSON line. Compare the saved embeddings with s001_t5_compare.py.
"""
import json
import sys
import time
from pathlib import Path

import mlx.core as mx
import numpy as np
from transformers import AutoTokenizer

from mlx_video.models.wan_2.config import WanModelConfig
from mlx_video.models.wan_2.utils import encode_text
from t5_variants import load_t5

model_dir, mode, out = Path(sys.argv[1]), sys.argv[2], sys.argv[3]
raw = json.load(open(model_dir / "config.json"))
config = WanModelConfig(**{k: (tuple(v) if isinstance(v, list) else v) for k, v in raw.items()
                           if k in WanModelConfig.__dataclass_fields__})
tokenizer = AutoTokenizer.from_pretrained("google/umt5-xxl")
prompts = ["A red fox running through fresh snow, cinematic, golden hour",
           "Un gato naranja duerme sobre un teclado mientras llueve tras la ventana, plano detalle"]
mx.reset_peak_memory()
started = time.perf_counter()
encoder = load_t5(model_dir / "t5_encoder.safetensors", config, mode)
loaded = time.perf_counter()
embeddings = [encode_text(encoder, tokenizer, p, config.text_len) for p in prompts]
mx.eval(*embeddings)
done = time.perf_counter()
np.savez(out, *[np.array(e.astype(mx.float32)) for e in embeddings])
print(json.dumps({"t5_mode": mode, "load_s": round(loaded - started, 1), "encode_s": round(done - loaded, 1),
                  "mlx_peak_gb": round(mx.get_peak_memory() / 1024**3, 2),
                  "active_after_gb": round(mx.get_active_memory() / 1024**3, 2)}))
