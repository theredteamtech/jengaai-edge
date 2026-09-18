# Experiment 006 — Arduino Button / INPUT_PULLUP

## Results

| Metric | Base Qwen | JengaCoder v1.2 |
|---|---:|---:|
| Exact component compliance | 0/1 | 0/1 |
| Push-button wiring | 2/2 | 0/2 |
| LED wiring | 0/2 | 0/2 |
| Correct INPUT_PULLUP configuration | 1/1 | 1/1 |
| Correct active-low logic | 1/1 | 0/1 |
| Exact pin compliance | 1/1 | 1/1 |
| Complete Arduino sketch | 1/1 | 1/1 |
| Test procedure | 1/1 | 0/1 |
| Total | 7/10 | 3/10 |

## Performance
Base Qwen:
- Prompt: 122.4 t/s
- Generation: 28.3 t/s

JengaCoder v1.2:
- Prompt: 115.1 t/s
- Generation: 27.5 t/s

## Finding
Both models had physical wiring problems.

Base Qwen correctly understood INPUT_PULLUP and active-low button logic, but failed
to place the 220 ohm resistor correctly in series with the LED.

JengaCoder v1.2 showed a larger hardware reasoning failure. It misplaced the resistor
around the button, omitted proper LED wiring, reversed the INPUT_PULLUP behavior,
and introduced an unlisted multimeter in the test procedure.

This provides additional evidence that JengaCoder v1.2's strongest regression area
is physical/embedded-system reasoning rather than basic coding.

This prompt is frozen evaluation material and must not be used for training.
