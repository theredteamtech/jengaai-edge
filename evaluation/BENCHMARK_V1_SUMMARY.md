# JengaAI ConstraintBench v1 — Diagnostic Summary

## Models
- Base: Qwen2.5-Coder-1.5B-Instruct, locally converted and Q4_K_M quantized
- Fine-tuned: JengaCoder v1.2 Q4_K_M
- Both: 1.54B parameters, 934.69 MiB
- Runtime: same llama.cpp build and CPU configuration

## Scores

| Experiment | Base Qwen | JengaCoder v1.2 |
|---|---:|---:|
| 001 — HC-SR04 constraint following | 4/10 | 1/10 |
| 002 — Offline Python error handling | 10/10 | 7/10 |
| 003 — C++ resource constraints | 9/10 | 8/10 |
| 004 — Exact Python instruction compliance | 10/10 | 10/10 |
| 005 — Offline HTTP dependency discipline | 10/10 | 9/10 |
| 006 — Arduino INPUT_PULLUP | 7/10 | 3/10 |
| 007 — Potentiometer/PWM | 8/10 | 7/10 |
| 008 — Incompatible constraint recognition | 6/10 | 0/10 |
| 009 — Streaming/memory discipline | 8/10 | 10/10 |
| 010 — ESP32 voltage safety | 5/10 | 4/10 |
| TOTAL | 77/100 | 59/100 |

## Hardware Subset
Experiments: 001, 006, 007, 010

Base Qwen: 24/40
JengaCoder v1.2: 15/40

## Non-Hardware Subset
Experiments: 002, 003, 004, 005, 008, 009

Base Qwen: 53/60
JengaCoder v1.2: 44/60

## Main Findings

### 1. Physical grounding is JengaCoder v1.2's largest weakness
The model often understands the desired programming behavior but fails to map it
correctly to real electrical connections and board-specific behavior.

Observed failures included:
- invented Servo/lid behavior
- invented or misidentified LED types
- incorrect resistor placement
- reversed INPUT_PULLUP logic
- wrong board-specific APIs
- unsafe voltage-interface reasoning
- repeated incorrect HC-SR04 distance formula

### 2. Global constraint consistency is weak
JengaCoder may attempt to produce familiar code even when requirements are
mutually incompatible.

Experiment 008 was the strongest example: the model claimed the impossible
requirements were satisfiable and then directly violated them using vector
and std::sort.

### 3. Control-flow/postcondition reasoning needs improvement
The model can write syntactically reasonable exception handling while failing
to reason about execution after an exception.

### 4. Basic coding capability remains strong
JengaCoder performed well on straightforward Python/C++ tasks and exact local
constraints.

### 5. Streaming/memory discipline can outperform the base model
In Experiment 009, JengaCoder correctly streamed results with O(1) additional
memory while the base model accumulated matches in a list.

### 6. Runtime performance is not the main regression
Across paired experiments, generation speed remained broadly similar between
the clean base model and JengaCoder v1.2.

## Gate 2 Training Priorities

1. Component inventory locking
2. Electrical topology correctness
3. Board-specific API correctness
4. Voltage compatibility and safe refusal
5. Incompatible-constraint detection
6. Postcondition/control-flow reasoning
7. Contrastive hardware examples
8. Preservation examples for existing strengths

## Evaluation Policy
All ten ConstraintBench v1 prompts are frozen evaluation material.

They must NOT be placed in the training dataset, paraphrased into training
examples, or used as target answers during corrective fine-tuning.

New training examples must test the same underlying competencies using distinct
problems and scenarios.

## Caveat
This is a small 10-prompt diagnostic benchmark, not a statistically comprehensive
measure of general model quality. Its purpose is to identify failure modes and
guide the next controlled training experiment.
