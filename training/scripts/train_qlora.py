import json
import os
from pathlib import Path

import torch
from datasets import Dataset
from peft import LoraConfig
from transformers import AutoTokenizer, BitsAndBytesConfig
from trl import SFTConfig, SFTTrainer


# ============================================================
# Configuration
# ============================================================

BASE_MODEL = "Qwen/Qwen2.5-Coder-1.5B-Instruct"

ROOT = Path(__file__).resolve().parents[2]

TRAIN_FILE = (
    ROOT
    / "training"
    / "data"
    / "jengacoder_train_v1.json"
)

VAL_FILE = (
    ROOT
    / "training"
    / "data"
    / "jengacoder_validation_v1.json"
)

OUTPUT_DIR = (
    ROOT
    / "training"
    / "output"
    / "jengacoder-v1"
)

ADAPTER_DIR = (
    ROOT
    / "training"
    / "output"
    / "jengacoder-v1-adapter"
)

SEED = 42


# ============================================================
# GPU Check
# ============================================================

if not torch.cuda.is_available():
    raise RuntimeError(
        "CUDA GPU not detected. "
        "Run this training script on an NVIDIA GPU environment."
    )

gpu_name = torch.cuda.get_device_name(0)

supports_bf16 = torch.cuda.is_bf16_supported()

compute_dtype = (
    torch.bfloat16
    if supports_bf16
    else torch.float16
)

print("=" * 70)
print("JengaCoder QLoRA Training")
print("=" * 70)

print(f"GPU:            {gpu_name}")
print(f"CUDA:           {torch.version.cuda}")
print(f"Compute dtype:  {compute_dtype}")
print(f"Base model:     {BASE_MODEL}")
print()


# ============================================================
# Load Dataset
# ============================================================

def load_json(path):
    with path.open(
        "r",
        encoding="utf-8",
    ) as file:
        return json.load(file)


train_raw = load_json(TRAIN_FILE)
val_raw = load_json(VAL_FILE)


def convert_example(item):
    user_content = item["instruction"].strip()

    if item.get("input", "").strip():
        user_content += (
            "\n\nInput:\n"
            + item["input"].strip()
        )

    return {
        "prompt": [
            {
                "role": "system",
                "content": item["system"].strip(),
            },
            {
                "role": "user",
                "content": user_content,
            },
        ],
        "completion": [
            {
                "role": "assistant",
                "content": item["output"].strip(),
            }
        ],
    }


train_examples = [
    convert_example(item)
    for item in train_raw
]

val_examples = [
    convert_example(item)
    for item in val_raw
]


train_dataset = Dataset.from_list(
    train_examples
)

val_dataset = Dataset.from_list(
    val_examples
)


print(
    f"Training examples:   {len(train_dataset)}"
)

print(
    f"Validation examples: {len(val_dataset)}"
)

print()


# ============================================================
# Tokenizer
# ============================================================

tokenizer = AutoTokenizer.from_pretrained(
    BASE_MODEL,
    trust_remote_code=False,
)

if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

tokenizer.padding_side = "right"


# ============================================================
# QLoRA 4-bit Configuration
# ============================================================

quantization_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_use_double_quant=True,
    bnb_4bit_compute_dtype=compute_dtype,
)


# ============================================================
# LoRA Configuration
# ============================================================

peft_config = LoraConfig(
    r=16,
    lora_alpha=32,
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM",

    target_modules=[
        "q_proj",
        "k_proj",
        "v_proj",
        "o_proj",
        "gate_proj",
        "up_proj",
        "down_proj",
    ],
)


# ============================================================
# Training Configuration
# ============================================================

training_args = SFTConfig(
    output_dir=str(OUTPUT_DIR),

    num_train_epochs=2,

    per_device_train_batch_size=1,
    per_device_eval_batch_size=1,

    gradient_accumulation_steps=8,

    learning_rate=1e-4,

    warmup_ratio=0.05,

    weight_decay=0.01,

    logging_steps=5,
    logging_first_step=True,

    eval_strategy="epoch",
    save_strategy="epoch",

    save_total_limit=2,

    max_length=2048,

    completion_only_loss=True,

    eos_token="<|im_end|>",

    gradient_checkpointing=True,

    gradient_checkpointing_kwargs={
        "use_reentrant": False
    },

    fp16=not supports_bf16,
    bf16=supports_bf16,

    seed=SEED,
    data_seed=SEED,

    report_to="none",

    model_init_kwargs={
        "dtype": compute_dtype,
    },
)


# ============================================================
# Trainer
# ============================================================

trainer = SFTTrainer(
    model=BASE_MODEL,

    args=training_args,

    train_dataset=train_dataset,

    eval_dataset=val_dataset,

    processing_class=tokenizer,

    peft_config=peft_config,

    quantization_config=quantization_config,
)


print()
print("=" * 70)
print("Starting JengaCoder training")
print("=" * 70)
print()


train_result = trainer.train()


# ============================================================
# Save Adapter
# ============================================================

ADAPTER_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

trainer.model.save_pretrained(
    ADAPTER_DIR
)

tokenizer.save_pretrained(
    ADAPTER_DIR
)


print()
print("=" * 70)
print("TRAINING COMPLETE")
print("=" * 70)

print(
    f"Adapter saved to: {ADAPTER_DIR}"
)

print(
    f"Final training loss: "
    f"{train_result.training_loss}"
)

print()
print(
    "JengaCoder v1 adapter created successfully."
)
