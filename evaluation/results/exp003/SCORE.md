# Experiment 003 — C++ Resource Constraints

## Results

| Metric | Base Qwen | JengaCoder v1.2 |
|---|---:|---:|
| Correct result logic | 2/2 | 1/2 |
| Single traversal | 2/2 | 2/2 |
| O(1) additional memory | 2/2 | 2/2 |
| No forbidden memory behavior | 1/1 | 1/1 |
| Correct C++17 program | 1/1 | 1/1 |
| 100 signed 16-bit sample values | 0/1 | 0/1 |
| Explanation | 1/1 | 1/1 |
| Total | 9/10 | 8/10 |

## Finding
Both models respected most resource constraints.

Base Qwen produced the correct one-pass maximum/count algorithm, but did not explicitly provide 100 signed 16-bit sample values and used int rather than int16_t.

JengaCoder v1.2 also respected the memory and traversal constraints, but initialized the maximum occurrence counter to 0 while starting traversal from index 1. This can produce an incorrect count when the first element remains the maximum.

Neither model explicitly initialized all 100 sample values.

This prompt is frozen evaluation material and must not be used for training.
