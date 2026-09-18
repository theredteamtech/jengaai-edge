# Experiment 009 — Streaming File Processing / Memory Discipline

## Results

| Metric | Base Qwen | JengaCoder v1.2 |
|---|---:|---:|
| Streaming input | 2/2 | 2/2 |
| Correct filtering | 1/2 | 2/2 |
| Invalid/blank-line handling | 1/1 | 1/1 |
| Missing-file handling | 1/1 | 1/1 |
| Memory discipline | 0/1 | 1/1 |
| Dependency compliance | 1/1 | 1/1 |
| No extra file creation | 1/1 | 1/1 |
| Complete runnable program / instruction following | 1/1 | 1/1 |
| Total | 8/10 | 10/10 |

## Performance
Base Qwen:
- Prompt: 118.1 t/s
- Generation: 28.2 t/s

JengaCoder v1.2:
- Prompt: 121.5 t/s
- Generation: 28.6 t/s

## Finding
JengaCoder v1.2 outperformed the base model on this streaming task.

Base Qwen read the input line by line but accumulated every matching temperature in
a list and printed them later. This violates the O(1) additional-memory constraint
and the requirement not to store matching temperatures for later output.

JengaCoder v1.2 streamed the file correctly, printed qualifying temperatures
immediately, preserved order, skipped malformed and blank lines, and handled
FileNotFoundError correctly.

This demonstrates that the fine-tuned model is not uniformly worse than the base.
It shows a clear strength in this constrained streaming/file-processing task.

This prompt is frozen evaluation material and must not be used for training.
