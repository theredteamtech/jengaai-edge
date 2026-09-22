# Base-model revision

- Source: `Qwen/Qwen2.5-Coder-1.5B-Instruct`
- Hugging Face revision: `2e1fd397ee46e1388853d2af2c993145b0f1098a`
- Weight file: `model.safetensors`
- Weight file size: `3,087,467,144` bytes
- Weight file SHA256: `c1b9b30e907950516ba3c646bdf570d8084c25a6410a0cdca80cf04b11bc13a8`

The historical training script loaded the repository's `main` revision without an explicit pin. The revision above was independently recorded as the upstream `main` revision before the Gate 1 submission and remained the upstream revision when Gate 2 provenance was prepared. The file checksum and size were retrieved from the Hugging Face LFS metadata for that exact revision.

This limitation is disclosed because the runtime-resolved revision was not written into the original training log.
