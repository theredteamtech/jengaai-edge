# Merge and quantization provenance

The recovered QLoRA adapter in `provenance/adapter/` was merged with the Qwen2.5-Coder-1.5B-Instruct base model. The merged model was converted to GGUF for llama.cpp and quantized to Q4_K_M.

## Published artifact

- Base-model revision: `2e1fd397ee46e1388853d2af2c993145b0f1098a`
- Adapter SHA256: `34455431fea5a115d30d943f901153f86311a86bd60f2881e89d69d7772f9278`
- Published model repository revision: `acd5bc24661d3258176068478be483cd587839e3`
- Published file: `JengaCoder-v1.2-Q4_K_M.gguf`
- Final GGUF SHA256: `e253182086f2bfd9e48ee3e4b683f151276fa1dfc6510faea8be0824dbe433bc`

## Reproduction recipe

- `merge_adapter.py` loads the pinned base-model revision, loads the recovered PEFT adapter, calls `merge_and_unload()`, and saves merged safetensors.
- `quantize_gguf.sh` converts that merged directory to F16 GGUF with llama.cpp and quantizes it to Q4_K_M.

The original shell-command transcript and exact historical llama.cpp commit were not retained. These scripts are therefore a transparent reproduction recipe based on the recovered adapter, pinned base revision and retained training configuration. They are not represented as the original historical transcript. The immutable published-model revision and final GGUF checksum identify the exact submitted artifact.
