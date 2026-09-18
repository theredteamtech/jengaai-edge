# Experiment 004 — Exact Python Instruction Compliance

## Results

| Metric | Base Qwen | JengaCoder v1.2 |
|---|---:|---:|
| Correct numeric result | 2/2 | 2/2 |
| Exact output compliance | 2/2 | 2/2 |
| Exactly one loop | 1/1 | 1/1 |
| No forbidden constructs | 2/2 | 2/2 |
| Preserves original list | 1/1 | 1/1 |
| O(1) additional memory | 1/1 | 1/1 |
| Complete runnable program | 1/1 | 1/1 |
| Total | 10/10 | 10/10 |

## Performance
Base Qwen:
- Prompt: 115.6 t/s
- Generation: 30.2 t/s

JengaCoder v1.2:
- Prompt: 113.7 t/s
- Generation: 30.1 t/s

## Finding
Both models fully satisfied the explicit Python constraints.

This shows JengaCoder v1.2 can follow simple, local, non-interacting constraints very well.
The larger regressions observed in earlier experiments appear more strongly when several
requirements interact, especially in error handling and physical/embedded reasoning.

This prompt is frozen evaluation material and must not be used for training.
