# Experiment 005 — Offline HTTP Server / Dependency Discipline

## Results

| Metric | Base Qwen | JengaCoder v1.2 |
|---|---:|---:|
| Standard-library-only compliance | 2/2 | 2/2 |
| Correct /health behavior | 2/2 | 2/2 |
| Correct 404 behavior | 1/1 | 0/1 |
| Correct Content-Type | 1/1 | 1/1 |
| Port and execution correctness | 1/1 | 1/1 |
| No extra functionality | 1/1 | 1/1 |
| Complete runnable program | 1/1 | 1/1 |
| Instruction following | 1/1 | 1/1 |
| Total | 10/10 | 9/10 |

## Performance
Base Qwen:
- Prompt: 119.8 t/s
- Generation: 28.4 t/s

JengaCoder v1.2:
- Prompt: 114.6 t/s
- Generation: 28.6 t/s

## Finding
Both models correctly respected the offline and standard-library-only requirements.

JengaCoder v1.2 correctly implemented GET /health, returned the required JSON response,
used application/json, and listened on port 8000.

However, for non-/health paths it calls send_response(404) without calling end_headers().
This may result in an incomplete HTTP response.

This prompt is frozen evaluation material and must not be used for training.
