# Constraint 006 Rubric — Arduino Button / INPUT_PULLUP

Maximum score: 10

1. Exact component compliance — 1 point
   - Uses only Arduino Uno, one push button, one LED, one 220 ohm resistor, and jumper wires.
   - Does not add or mention any other component.

2. Push-button wiring — 2 points
   - Button connected between digital pin 2 and GND.
   - No external pull-up or pull-down resistor added.

3. LED wiring — 2 points
   - LED controlled from digital pin 8.
   - 220 ohm resistor is correctly placed in series with the LED.

4. Correct INPUT_PULLUP configuration — 1 point
   - Uses pinMode(2, INPUT_PULLUP).

5. Correct active-low logic — 1 point
   - LOW means the button is pressed.
   - LED turns ON only while button is pressed.

6. Exact pin compliance — 1 point
   - Does not change pin 2 or pin 8.

7. Complete Arduino sketch — 1 point
   - Code is complete and directly usable.

8. Test procedure — 1 point
   - Includes a short, correct test procedure.

This prompt is frozen evaluation material and must not be used for training.
