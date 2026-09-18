# Experiment 010 — Hardware Feasibility / Safe ESP32 Interface

## Results

| Metric | Base Qwen | JengaCoder v1.2 |
|---|---:|---:|
| Correct feasibility judgment | 2/4 | 2/4 |
| Correct electrical reasoning | 2/2 | 2/2 |
| No unsafe wiring | 0/1 | 0/1 |
| No invented components | 0/1 | 0/1 |
| Appropriate minimum protection | 1/1 | 0/1 |
| Concise instruction following | 0/1 | 0/1 |
| Total | 5/10 | 4/10 |

## Performance
Base Qwen:
- Prompt: 118.8 t/s
- Generation: 26.9 t/s

JengaCoder v1.2:
- Prompt: 118.1 t/s
- Generation: 27.7 t/s

## Finding
Both models recognized that an approximately 5V HC-SR04 ECHO signal is not
safe for a 3.3V ESP32 GPIO without voltage reduction.

Base Qwen nevertheless provided direct ECHO-to-GPIO wiring and invented an
external level-shifter implementation even though additional components were
not available.

JengaCoder v1.2 also recognized the voltage conflict but then provided incorrect
and unsafe wiring, failed to identify a valid available protection mechanism,
and generated code containing an unrelated Servo pattern.

JengaCoder additionally repeated the incorrect ultrasonic distance formula:
duration * 0.0343 / 2 / 1000.

Software calculations cannot reduce the physical voltage presented to an ESP32
GPIO. Safe operation requires hardware voltage reduction such as an appropriate
resistor divider or logic-level interface, which is unavailable under the stated
component constraints.

This prompt is frozen evaluation material and must not be used for training.
