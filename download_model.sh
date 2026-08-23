#!/usr/bin/env bash
set -euo pipefail

MODEL_DIR="model"
MODEL_FILE="JengaCoder-v1.2-Q4_K_M.gguf"
MODEL_PATH="${MODEL_DIR}/${MODEL_FILE}"
PART_PATH="${MODEL_PATH}.part"
MODEL_URL="https://huggingface.co/theredteamtech/JengaCoder-v1.2/resolve/main/JengaCoder-v1.2-Q4_K_M.gguf"

EXPECTED_SHA256="e253182086f2bfd9e48ee3e4b683f151276fa1dfc6510faea8be0824dbe433bc"

mkdir -p "${MODEL_DIR}"

if [ -f "${MODEL_PATH}" ]; then
    echo "Model already exists: ${MODEL_PATH}"
else
    echo "Downloading JengaCoder v1.2..."
    curl -L --fail --progress-bar \
        "${MODEL_URL}" \
        -o "${MODEL_PATH}"
fi

echo "Verifying SHA-256..."

ACTUAL_SHA256=$(sha256sum "${MODEL_PATH}" | awk '{print $1}')

if [ "${ACTUAL_SHA256}" != "${EXPECTED_SHA256}" ]; then
    echo "ERROR: SHA-256 mismatch"
    echo "Expected: ${EXPECTED_SHA256}"
    echo "Actual:   ${ACTUAL_SHA256}"
    exit 1
fi

echo "JengaCoder v1.2 downloaded and verified successfully."
