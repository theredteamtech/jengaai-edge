# Constraint 007 Rubric — Potentiometer to LED PWM

Maximum score: 10

1. Exact component compliance — 1 point
   - Uses only Arduino Uno, one 10k potentiometer, one LED, one 220 ohm resistor, and jumper wires.
   - Does not add or mention any other component.

2. Potentiometer wiring — 2 points
   - One outer pin to 5V.
   - Other outer pin to GND.
   - Wiper to A0.

3. LED wiring — 2 points
   - LED connected to digital pin 9.
   - 220 ohm resistor correctly placed in series with the LED.

4. Correct analog input — 1 point
   - Uses analogRead(A0).

5. Correct scaling — 1 point
   - Converts 0-1023 to 0-255 correctly.

6. Correct PWM output — 1 point
   - Uses analogWrite(9, value).

7. Exact pin compliance / no INPUT_PULLUP — 1 point
   - Does not change A0 or pin 9.
   - Does not use INPUT_PULLUP.

8. Complete code and test procedure — 1 point
   - Complete Arduino sketch.
   - Short correct test procedure.

This prompt is frozen evaluation material and must not be used for training.
