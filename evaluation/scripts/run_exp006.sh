#!/usr/bin/env bash
set -e

ROOT="$HOME/jengaai-edge"
PROMPT_FILE="$ROOT/evaluation/prompts/constraint_006.txt"
OUT_DIR="$ROOT/evaluation/results/exp006"

BASE="$HOME/models/jengaai/baselines/qwen2.5-coder-1.5b-instruct-local-q4_k_m.gguf"
JENGA="$ROOT/model/JengaCoder-v1.2-Q4_K_M.gguf"

LLAMA="$HOME/llama.cpp/build/bin/llama-cli"

mkdir -p "$OUT_DIR"

run_model () {
  NAME="$1"
  MODEL="$2"

  echo "========================================"
  echo "Running: $NAME"
  echo "========================================"

  "$LLAMA" \
    -m "$MODEL" \
    -t 4 \
    -c 4096 \
    -n 1024 \
    --offline \
    -p "$(cat "$PROMPT_FILE")" \
    --output "$OUT_DIR/$NAME.txt"

  echo
  echo "Saved response:"
  echo "$OUT_DIR/$NAME.txt"
  echo
}

run_model "base_qwen" "$BASE"
run_model "jengacoder_v1_2" "$JENGA"

echo "========================================"
echo "Experiment 006 completed"
echo "========================================"
