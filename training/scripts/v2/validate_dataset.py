#!/usr/bin/env python3
import argparse
import json
import re
import sys
from difflib import SequenceMatcher
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
DATA_DIR = ROOT / "training" / "data" / "v2"
EVAL_PROMPTS = ROOT / "evaluation" / "prompts"
SPLITS = ("train", "validation", "holdout")
REQUIRED_FIELDS = {"system", "instruction", "input", "output"}

def norm(text):
    return re.sub(r"\s+", " ", text.strip().lower())

def load_json(path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)

def load_eval_prompts():
    prompts = []
    if EVAL_PROMPTS.exists():
        for path in sorted(EVAL_PROMPTS.glob("constraint_*.txt")):
            text = path.read_text(encoding="utf-8").strip()
            if text:
                prompts.append((path.name, norm(text)))
    return prompts

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--strict-counts", action="store_true",
                        help="Require manifest target counts exactly.")
    parser.add_argument("--similarity", type=float, default=0.80,
                        help="Flag instruction similarity to frozen evaluation prompts.")
    args = parser.parse_args()

    errors = []
    warnings = []
    datasets = {}
    all_seen = {}

    manifest_path = DATA_DIR / "manifest.json"
    manifest = load_json(manifest_path) if manifest_path.exists() else None
    eval_prompts = load_eval_prompts()

    for split in SPLITS:
        path = DATA_DIR / f"{split}.json"
        try:
            records = load_json(path)
        except Exception as exc:
            errors.append(f"{split}: cannot load {path}: {exc}")
            continue

        if not isinstance(records, list):
            errors.append(f"{split}: top level must be a JSON list")
            continue

        datasets[split] = records
        local_seen = {}

        for idx, record in enumerate(records):
            label = f"{split}[{idx}]"
            if not isinstance(record, dict):
                errors.append(f"{label}: record must be an object")
                continue

            fields = set(record)
            missing = REQUIRED_FIELDS - fields
            if missing:
                errors.append(f"{label}: missing fields {sorted(missing)}")

            for field in REQUIRED_FIELDS & fields:
                if not isinstance(record[field], str):
                    errors.append(f"{label}: {field} must be a string")

            if any(field not in record or not isinstance(record.get(field), str)
                   for field in ("system", "instruction", "output")):
                continue

            if not record["system"].strip():
                errors.append(f"{label}: system is empty")
            if not record["instruction"].strip():
                errors.append(f"{label}: instruction is empty")
                continue
            if not record["output"].strip():
                errors.append(f"{label}: output is empty")

            key = norm(record["instruction"])

            if key in local_seen:
                errors.append(
                    f"{label}: duplicate instruction within {split}; "
                    f"first seen at {split}[{local_seen[key]}]"
                )
            else:
                local_seen[key] = idx

            if key in all_seen and all_seen[key][0] != split:
                prev_split, prev_idx = all_seen[key]
                errors.append(
                    f"{label}: split leakage; same instruction as "
                    f"{prev_split}[{prev_idx}]"
                )
            else:
                all_seen.setdefault(key, (split, idx))

            for prompt_name, frozen in eval_prompts:
                if key == frozen:
                    errors.append(
                        f"{label}: exact contamination from frozen {prompt_name}"
                    )
                    break
                ratio = SequenceMatcher(None, key, frozen).ratio()
                if ratio >= args.similarity:
                    warnings.append(
                        f"{label}: possible frozen-prompt paraphrase "
                        f"({prompt_name}, similarity={ratio:.3f})"
                    )
                    break

    print("JengaAI Edge v2 dataset validation")
    print("----------------------------------")
    for split in SPLITS:
        print(f"{split}: {len(datasets.get(split, []))} records")

    if manifest:
        targets = manifest.get("splits", {})
        if args.strict_counts:
            for split in SPLITS:
                expected = targets.get(split)
                if expected is not None and len(datasets.get(split, [])) != expected:
                    errors.append(
                        f"{split}: expected {expected} records, "
                        f"found {len(datasets.get(split, []))}"
                    )
        else:
            print("count mode: development (use --strict-counts for final targets)")
    else:
        warnings.append("manifest.json not found")

    print(f"frozen evaluation prompts loaded: {len(eval_prompts)}")
    print(f"errors: {len(errors)}")
    print(f"warnings: {len(warnings)}")

    if warnings:
        print("\nWARNINGS")
        for item in warnings:
            print(f"- {item}")

    if errors:
        print("\nERRORS")
        for item in errors:
            print(f"- {item}")
        sys.exit(1)

    print("\nPASS")

if __name__ == "__main__":
    main()
