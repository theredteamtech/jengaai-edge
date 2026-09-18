# Experiment 002 — Offline Python / Standard Library Constraint Following

## Results

| Metric | Base Qwen | JengaCoder v1.2 |
|---|---:|---:|
| Constraint compliance | 2/2 | 2/2 |
| Correct JSON loading | 2/2 | 2/2 |
| Correct filtering logic | 2/2 | 2/2 |
| Missing-file handling | 1/1 | 0/1 |
| Malformed-JSON handling | 1/1 | 0/1 |
| Program completeness | 1/1 | 0/1 |
| Instruction following | 1/1 | 1/1 |
| Total | 10/10 | 7/10 |

## Performance
Base Qwen:
- Prompt: 127.7 t/s
- Generation: 28.5 t/s

JengaCoder v1.2:
- Prompt: 117.5 t/s
- Generation: 30.1 t/s

## Finding
JengaCoder v1.2 respected the offline and standard-library-only constraints and produced the correct filtering logic.

However, its exception handling is incomplete. If students.json is missing or malformed,
the program prints an error message but continues execution. The variable "students"
is never assigned, so the later loop raises NameError.

This indicates a correctness and constraint-reasoning regression outside hardware tasks as well.

This prompt is frozen evaluation material and must not be used for training.
