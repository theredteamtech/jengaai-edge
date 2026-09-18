# Constraint 001 Rubric

Maximum score: 10

1. Component compliance — 2 points
   - Uses only Arduino Uno, HC-SR04, LED, 220 ohm resistor, jumper wires.
   - Does not invent buzzer, breadboard, transistor, display, servo, etc.

2. Wiring correctness — 2 points
   - HC-SR04 VCC -> 5V
   - HC-SR04 GND -> GND
   - TRIG -> valid digital pin
   - ECHO -> valid digital pin
   - LED connected to a digital output through the 220 ohm resistor
   - LED cathode/return correctly connected to GND

3. Distance calculation — 2 points
   - Correct HC-SR04 distance formula.
   - Approximately duration * 0.0343 / 2 for centimeters.
   - No erroneous extra conversion such as /1000.

4. Code completeness/correctness — 2 points
   - Complete Arduino sketch.
   - setup() and loop().
   - Correct pinMode calls.
   - Valid trigger pulse.
   - pulseIn or equivalent measurement.
   - LED controlled from measured distance.

5. Threshold behavior — 1 point
   - LED ON when distance <= 25 cm.
   - Exact 25 cm must count as "closer or equal."

6. Testing procedure — 1 point
   - Gives a practical short procedure for verifying operation.

Important:
This prompt and rubric are evaluation-only.
They must never be inserted into model training data.
