# Experiment 007 — Potentiometer to LED PWM

## Results

| Metric | Base Qwen | JengaCoder v1.2 |
|---|---:|---:|
| Exact component compliance | 0/1 | 1/1 |
| Potentiometer wiring | 2/2 | 2/2 |
| LED wiring | 1/2 | 0/2 |
| Correct analog input | 1/1 | 1/1 |
| Correct scaling | 1/1 | 1/1 |
| Correct PWM output | 1/1 | 1/1 |
| Exact pins / no INPUT_PULLUP | 1/1 | 1/1 |
| Complete code and test procedure | 1/1 | 0/1 |
| Total | 8/10 | 7/10 |

## Performance
Base Qwen:
- Prompt: 118.0 t/s
- Generation: 28.7 t/s

JengaCoder v1.2:
- Prompt: 112.5 t/s
- Generation: 28.5 t/s

## Finding
Both models understood the analogRead-to-PWM programming concept.

Base Qwen used the required pins and correct scaling, but its LED wiring was incomplete
and its test procedure introduced unlisted items such as a breadboard.

JengaCoder v1.2 correctly read A0, scaled the reading, and used analogWrite on pin 9,
but its physical LED description was incorrect. It described a normal LED using
VCC, GND, and data-style connections and omitted the required 220 ohm series resistor.

JengaCoder also used analogWriteRange(255), which is not part of the standard
Arduino Uno AVR API. The Uno already uses a 0-255 PWM range for analogWrite().

This adds evidence that JengaCoder v1.2 generally understands embedded programming
logic better than it understands the physical/electrical implementation.

This prompt is frozen evaluation material and must not be used for training.
