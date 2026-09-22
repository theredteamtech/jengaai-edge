#!/usr/bin/env bash
set -euo pipefail

# Usage:
#   LLAMA_CPP_DIR=/path/to/llama.cpp bash provenance/quantize_gguf.sh
#
# First merge:
#   python3 provenance/merge_adapter.py

: "${LLAMA_CPP_DIR:?Set LLAMA_CPP_DIR to the llama.cpp checkout}"

MERGED_DIR="build/jengacoder-v1.2-merged"
F16_GGUF="build/JengaCoder-v1.2-F16.gguf"
FINAL_GGUF="build/JengaCoder-v1.2-Q4_K_M.gguf"

python3 "${LLAMA_CPP_DIR}/convert_hf_to_gguf.py"     "${MERGED_DIR}"     --outfile "${F16_GGUF}"     --outtype f16

if [[ -x "${LLAMA_CPP_DIR}/build/bin/llama-quantize" ]]; then
    QUANTIZER="${LLAMA_CPP_DIR}/build/bin/llama-quantize"
else
    QUANTIZER="${LLAMA_CPP_DIR}/llama-quantize"
fi

"${QUANTIZER}" "${F16_GGUF}" "${FINAL_GGUF}" Q4_K_M
sha256sum "${FINAL_GGUF}"
