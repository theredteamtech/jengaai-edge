# Base-versus-fine-tuned output examples
These examples use frozen prompts that were run against the unmodified Qwen2.5-Coder-1.5B-Instruct base model and JengaCoder v1.2. The text below is copied programmatically from the committed evaluation artifacts without rewriting either model's response.

## Experiment 001: Hardware constraint-following regression

### Identical prompt
```text
You have an Arduino Uno, one HC-SR04 ultrasonic sensor, one LED, one 220 ohm resistor, and jumper wires only. Build a proximity warning system where the LED turns on when an object is 25 cm or closer. Give pin-by-pin wiring, complete Arduino code, and a short test procedure. Do not use or mention any component that is not listed.
```

### Unmodified base-model output
```text
User:
You have an Arduino Uno, one HC-SR04 ultrasonic sensor, one LED, one 220 ohm resistor, and jumper wires only. Build a proximity warning system where the LED turns on when an object is 25 cm or closer. Give pin-by-pin wiring, complete Arduino code, and a short test procedure. Do not use or mention any component that is not listed.

Assistant:
### Step 1: Wiring

1. **Connect the HC-SR04 Sensor:**
   - Connect the VCC pin of the HC-SR04 to the 5V pin of the Arduino.
   - Connect the GND pin of the HC-SR04 to the GND pin of the Arduino.
   - Connect the Trig pin of the HC-SR04 to digital pin 9 of the Arduino.
   - Connect the Echo pin of the HC-SR04 to digital pin 10 of the Arduino.

2. **Connect the LED:**
   - Connect the positive terminal of the LED to digital pin 2 of the Arduino.
   - Connect the negative terminal of the LED to the GND pin of the Arduino.

3. **Connect the Resistor:**
   - Connect the positive terminal of the resistor to the positive terminal of the LED.
   - Connect the negative terminal of the resistor to the GND pin of the Arduino.

### Step 2: Arduino Code

```cpp
const int trigPin = 9;
const int echoPin = 10;
const int ledPin = 2;
const int thresholdDistance = 25; // in cm

void setup() {
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  pinMode(ledPin, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  long duration = pulseIn(echoPin, HIGH);
  float distance = duration * 0.0343; // convert microseconds to centimeters

  Serial.print("Distance: ");
  Serial.print(distance);
  Serial.println(" cm");

  if (distance <= thresholdDistance) {
    digitalWrite(ledPin, HIGH);
  } else {
    digitalWrite(ledPin, LOW);
  }

  delay(100);
}
```

### Step 3: Test Procedure

1. **Power Up the Arduino:**
   - Connect the Arduino to your computer using a USB cable.
   - Open the Arduino IDE and upload the code to the Arduino Uno.

2. **Observe the LED:**
   - Place an object within 25 cm of the HC-SR04 sensor.
   - Observe the LED. It should turn on when the object is within 25 cm of the sensor.

3. **Move the Object:**
   - Move the object away from the HC-SR04 sensor.
   - Observe the LED. It should turn off when the object is more than 25 cm away from the sensor.

This setup provides a simple proximity warning system using an Arduino Uno, an HC-SR04 ultrasonic sensor, and an LED. The LED turns on when an object is within 25 cm of the sensor, providing a basic form of obstacle detection.
```

### JengaCoder v1.2 output
```text
User:
You have an Arduino Uno, one HC-SR04 ultrasonic sensor, one LED, one 220 ohm resistor, and jumper wires only. Build a proximity warning system where the LED turns on when an object is 25 cm or closer. Give pin-by-pin wiring, complete Arduino code, and a short test procedure. Do not use or mention any component that is not listed.

Assistant:
### Pin-by-pin Wiring

1. **HC-SR04 VCC -> Arduino 5V**
2. **HC-SR04 GND -> Arduino GND**
3. **HC-SR04 TRIG -> Arduino 9**
4. **HC-SR04 ECHO -> Arduino A0**
5. **LED red/VCC -> Arduino 5V**
6. **LED red/GND -> Arduino GND**
7. **LED green/VCC -> Arduino 5V**
8. **LED green/GND -> Arduino GND**
9. **LED blue/VCC -> Arduino 5V**
10. **LED blue/GND -> Arduino GND**

### Arduino Code

```cpp
#include <Servo.h>

const int TRIG_PIN = 9;
const int ECHO_PIN = A0;

const int LED_RED_PIN = 6;
const int LED_GREEN_PIN = 5;
const int LED_BLUE_PIN = 3;

const float THRESHOLD_CM = 25.0f;
const float THRESHOLD_CM_RED = 10.0f;
const float THRESHOLD_CM_GREEN = 20.0f;

const int LED_ON = HIGH;
const int LED_OFF = LOW;

Servo lid;

bool lidOpen = false;
bool redLEDOn = false;
bool greenLEDOn = false;
bool blueLEDOn = false;

float readDistanceCm() {
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);

  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);

  digitalWrite(TRIG_PIN, LOW);

  unsigned long duration =
      pulseIn(ECHO_PIN, HIGH, 30000UL);

  if (duration == 0) {
    return -1.0f;
  }

  return duration * 0.0343f / 2.0f / 1000.0f;
}

void setup() {
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);

  pinMode(LED_RED_PIN, OUTPUT);
  pinMode(LED_GREEN_PIN, OUTPUT);
  pinMode(LED_BLUE_PIN, OUTPUT);

  lid.attach(2);
  lid.write(0);
}

void loop() {
  float distance = readDistanceCm();

  bool objectPresent = distance > 0 && distance <= THRESHOLD_CM;

  bool lidOpenNew = objectPresent && !lidOpen;

  bool redLEDOnNew = objectPresent && distance <= THRESHOLD_CM_RED;

  bool greenLEDOnNew = objectPresent && distance <= THRESHOLD_CM_GREEN;

  bool blueLEDOnNew = !objectPresent;

  if (lidOpenNew) {
    lid.write(90);
  } else if (lidOpen) {
    lid.write(0);
  }

  if (redLEDOnNew) {
    digitalWrite(LED_RED_PIN, LED_ON);
  } else {
    digitalWrite(LED_RED_PIN, LED_OFF);
  }

  if (greenLEDOnNew) {
    digitalWrite(LED_GREEN_PIN, LED_ON);
  } else {
    digitalWrite(LED_GREEN_PIN, LED_OFF);
  }

  if (blueLEDOnNew) {
    digitalWrite(LED_BLUE_PIN, LED_ON);
  } else {
    digitalWrite(LED_BLUE_PIN, LED_OFF);
  }

  delay(50);
}
```

### Test Procedure

1. Connect the HC-SR04 sensor to the Arduino.
2. Upload the code to the Arduino.
3. Observe the LED behavior. The red LED should turn on when the object is 10 cm or closer, the green LED should turn on when the object is 20 cm or closer, and the blue LED should turn off when the object is 25 cm or further away.
4. Adjust the thresholds and colors as needed.
```

### Scoring record
```text
# Experiment 001 — Constraint Following

## Prompt
Arduino Uno + HC-SR04 + one LED + one 220 ohm resistor only.
LED must turn on at <= 25 cm.

## Results

| Metric | Base Qwen | JengaCoder v1.2 |
|---|---:|---:|
| Component compliance | 1/2 | 0/2 |
| Wiring correctness | 1/2 | 0.5/2 |
| Distance calculation | 0/2 | 0/2 |
| Code correctness | 0.5/2 | 0.5/2 |
| Threshold behavior | 1/1 | 0/1 |
| Testing procedure | 0.5/1 | 0/1 |
| Total | 4/10 | 1/10 |

## Performance
Base Qwen:
- Prompt: 65.5 t/s
- Generation: 18.4 t/s

JengaCoder v1.2:
- Prompt: 66.8 t/s
- Generation: 18.2 t/s

## Finding
JengaCoder v1.2 showed a strong constraint-following regression on this prompt.
It invented Servo/lid behavior and multiple LED colors, omitted the required resistor,
and used an incorrect HC-SR04 distance formula.

This prompt is frozen evaluation material and must not be used for training.
```

## Experiment 009: Streaming and memory-discipline improvement

### Identical prompt
```text
Write a complete Python 3.10 program that processes a potentially very large text file named temperatures.txt.

Each valid line contains one signed integer temperature, for example:

25
-3
41

Requirements:
1. Read the file line by line. Do not load the whole file into memory.
2. Print only temperatures greater than or equal to 30.
3. Preserve the original order.
4. Ignore blank lines.
5. If a non-blank line is not a valid integer, skip that line without terminating the program.
6. If temperatures.txt does not exist, print exactly:
FILE NOT FOUND
7. Use only the Python standard library.
8. Do not create another file.
9. Do not use read(), readlines(), list(), comprehensions, pandas, numpy, or any third-party package.
10. Use O(1) additional memory apart from Python's normal per-line input buffering.
11. Do not store the matching temperatures for later printing.
12. Give only the complete Python program followed by a short explanation.

The program must work correctly even if temperatures.txt is much larger than available RAM.
```

### Unmodified base-model output
```text
User:
Write a complete Python 3.10 program that processes a potentially very large text file named temperatures.txt.

Each valid line contains one signed integer temperature, for example:

25
-3
41

Requirements:
1. Read the file line by line. Do not load the whole file into memory.
2. Print only temperatures greater than or equal to 30.
3. Preserve the original order.
4. Ignore blank lines.
5. If a non-blank line is not a valid integer, skip that line without terminating the program.
6. If temperatures.txt does not exist, print exactly:
FILE NOT FOUND
7. Use only the Python standard library.
8. Do not create another file.
9. Do not use read(), readlines(), list(), comprehensions, pandas, numpy, or any third-party package.
10. Use O(1) additional memory apart from Python's normal per-line input buffering.
11. Do not store the matching temperatures for later printing.
12. Give only the complete Python program followed by a short explanation.

The program must work correctly even if temperatures.txt is much larger than available RAM.

Assistant:
```python
# Import necessary libraries
import os

def read_temperatures(filename):
    """
    Reads temperatures from a file and returns a list of valid temperatures.
    """
    valid_temperatures = []
    try:
        with open(filename, 'r') as file:
            for line in file:
                # Skip empty lines
                if line.strip():
                    try:
                        # Attempt to convert the line to an integer
                        temp = int(line.strip())
                        # Check if the temperature is valid
                        if temp >= 30:
                            valid_temperatures.append(temp)
                    except ValueError:
                        # Skip non-integer lines
                        pass
    except FileNotFoundError:
        print("FILE NOT FOUND")
        return None
    return valid_temperatures

def main():
    # Define the file path
    file_path = "temperatures.txt"

    # Check if the file exists
    if not os.path.exists(file_path):
        print("FILE NOT FOUND")
        return

    # Read temperatures
    temperatures = read_temperatures(file_path)

    if temperatures is not None:
        # Print valid temperatures
        print("Valid temperatures:", temperatures)

if __name__ == "__main__":
    main()
```

### Explanation:

1. **read_temperatures function**:
    - This function reads the file line by line, ignoring blank lines and converting valid integer lines to temperatures.
    - It uses a try-except block to handle non-integer lines gracefully.

2. **main function**:
    - This function checks if the file "temperatures.txt" exists.
    - If the file exists, it reads the temperatures using `read_temperatures`.
    - If the file does not exist, it prints "FILE NOT FOUND".
    - If the temperatures are read successfully, it prints the valid temperatures.

This program adheres to the given requirements and handles large files efficiently without loading them into memory.
```

### JengaCoder v1.2 output
```text
User:
Write a complete Python 3.10 program that processes a potentially very large text file named temperatures.txt.

Each valid line contains one signed integer temperature, for example:

25
-3
41

Requirements:
1. Read the file line by line. Do not load the whole file into memory.
2. Print only temperatures greater than or equal to 30.
3. Preserve the original order.
4. Ignore blank lines.
5. If a non-blank line is not a valid integer, skip that line without terminating the program.
6. If temperatures.txt does not exist, print exactly:
FILE NOT FOUND
7. Use only the Python standard library.
8. Do not create another file.
9. Do not use read(), readlines(), list(), comprehensions, pandas, numpy, or any third-party package.
10. Use O(1) additional memory apart from Python's normal per-line input buffering.
11. Do not store the matching temperatures for later printing.
12. Give only the complete Python program followed by a short explanation.

The program must work correctly even if temperatures.txt is much larger than available RAM.

Assistant:
```python
def main():
    try:
        with open("temperatures.txt", "r") as file:
            for line in file:
                try:
                    temp = int(line)
                    if temp >= 30:
                        print(temp)
                except ValueError:
                    continue
    except FileNotFoundError:
        print("FILE NOT FOUND")

if __name__ == "__main__":
    main()
```

Explanation:
- `with open(..., "r") as file:` ensures that `file` is closed after reading.
- `for line in file:` reads the file line by line without loading it all into memory.
- `try: int(line)` attempts to convert the line to an integer. If this fails, `ValueError` is raised.
- `continue` skips to the next iteration if the conversion fails.
- If the file does not exist, `FileNotFoundError` is caught and an appropriate message is printed.
```

### Scoring record
```text
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
```
