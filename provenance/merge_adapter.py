#!/usr/bin/env python3
"""Reproduce the adapter merge for JengaCoder v1.2."""

import argparse
from pathlib import Path

import torch
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer

BASE_MODEL = "Qwen/Qwen2.5-Coder-1.5B-Instruct"
BASE_REVISION = "2e1fd397ee46e1388853d2af2c993145b0f1098a"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--adapter", default="provenance/adapter")
    parser.add_argument("--output", default="build/jengacoder-v1.2-merged")
    args = parser.parse_args()

    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=False)

    base = AutoModelForCausalLM.from_pretrained(
        BASE_MODEL,
        revision=BASE_REVISION,
        torch_dtype=torch.float16,
        low_cpu_mem_usage=True,
        trust_remote_code=False,
    )
    model = PeftModel.from_pretrained(base, args.adapter)
    merged = model.merge_and_unload()
    merged.save_pretrained(output, safe_serialization=True)

    tokenizer = AutoTokenizer.from_pretrained(
        BASE_MODEL,
        revision=BASE_REVISION,
        trust_remote_code=False,
    )
    tokenizer.save_pretrained(output)


if __name__ == "__main__":
    main()
