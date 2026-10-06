"""S-001/S-003 spike: alternative ways to load the UMT5-XXL encoder with less memory.

mlx-video upcasts the 11.4 GB bf16 T5 weights to float32 (22.7 GB). These loaders keep the same
T5Encoder class and change only how the weights are held:

  float32   upstream behaviour (reference)
  bf16      weights kept as stored
  q8 / q4   Linear and Embedding layers quantized with mlx.nn.quantize after loading in bf16
"""
import mlx.core as mx
import mlx.nn as nn
from mlx_video.models.wan_2.text_encoder import T5Encoder

MODES = ("float32", "bf16", "q8", "q4")


def load_t5(model_path, config, mode):
    encoder = T5Encoder(
        vocab_size=config.t5_vocab_size, dim=config.t5_dim, dim_attn=config.t5_dim_attn,
        dim_ffn=config.t5_dim_ffn, num_heads=config.t5_num_heads, num_layers=config.t5_num_layers,
        num_buckets=config.t5_num_buckets, shared_pos=False,
    )
    weights = mx.load(str(model_path))
    if mode == "float32":
        weights = {k: v.astype(mx.float32) for k, v in weights.items()}
    encoder.load_weights(list(weights.items()))
    del weights
    if mode in ("q8", "q4"):
        nn.quantize(encoder, group_size=64, bits=int(mode[1]))
    mx.eval(encoder.parameters())
    mx.clear_cache()
    return encoder
