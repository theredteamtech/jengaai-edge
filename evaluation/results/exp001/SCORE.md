# Experiment 001 — Constraint Following

## Prompt
Arduino Uno + HC-SR04 + one LED + one 220 ohm resistor only.
LED must turn on at <= 25 cm.

## Results

| Metric | Base Qwen | JengaCoder v1.2 |
|---|---:|---:|
| Component compliance | 1/2 | 0/2 |
| Wiring correctness | 1/2 | 0.5/2 |
| Distance calculation | 0/2 | 0/2 |
| Code correctness | 0.5/2 | 0.5/2 |
| Threshold behavior | 1/1 | 0/1 |
| Testing procedure | 0.5/1 | 0/1 |
| Total | 4/10 | 1/10 |

## Performance
Base Qwen:
- Prompt: 65.5 t/s
- Generation: 18.4 t/s

JengaCoder v1.2:
- Prompt: 66.8 t/s
- Generation: 18.2 t/s

## Finding
JengaCoder v1.2 showed a strong constraint-following regression on this prompt.
It invented Servo/lid behavior and multiple LED colors, omitted the required resistor,
and used an incorrect HC-SR04 distance formula.

This prompt is frozen evaluation material and must not be used for training.
