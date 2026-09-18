#!/usr/bin/env bash
set -euo pipefail

LLAMA="$HOME/llama.cpp/build/bin/llama-cli"

BASE="$HOME/models/jengaai/baselines/qwen2.5-coder-1.5b-instruct-local-q4_k_m.gguf"
JENGA="$HOME/jengaai-edge/model/JengaCoder-v1.2-Q4_K_M.gguf"

PROMPT_FILE="$HOME/jengaai-edge/evaluation/prompts/constraint_001.txt"

OUTDIR="$HOME/jengaai-edge/evaluation/results/exp001"
LOGDIR="$HOME/jengaai-edge/evaluation/logs/exp001"

mkdir -p "$OUTDIR" "$LOGDIR"

PROMPT="$(cat "$PROMPT_FILE")"

run_model () {
    NAME="$1"
    MODEL="$2"

    echo
    echo "========================================"
    echo "Running: $NAME"
    echo "========================================"

    rm -f "$OUTDIR/${NAME}.txt"
    rm -f "$LOGDIR/${NAME}.log"

    "$LLAMA" \
        -m "$MODEL" \
        -t 4 \
        -c 4096 \
        -n 1024 \
        --temp 0 \
        --seed 42 \
        -cnv \
        -st \
        -p "$PROMPT" \
        --output "$OUTDIR/${NAME}.txt" \
        2> "$LOGDIR/${NAME}.log"

    echo
    echo "Saved response:"
    echo "$OUTDIR/${NAME}.txt"

    echo "Size:"
    wc -c "$OUTDIR/${NAME}.txt"
}

run_model "base_qwen" "$BASE"
run_model "jengacoder_v1_2" "$JENGA"

echo
echo "========================================"
echo "Experiment 001 completed"
echo "========================================"
