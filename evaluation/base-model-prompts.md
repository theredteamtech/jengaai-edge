# JengaAI Base Model Evaluation Prompts

## TEST 1 — Python Debugging

The following Python function is supposed to return the average of valid numeric values, while ignoring None values. It contains bugs.

```python
def average(values):
    total = 0
    for value in values:
        total += value
    return total / len(values)

Correct the function so that:

None values are ignored.
An empty list returns 0.
A list containing only None values returns 0.
Do not use external libraries.
Give the corrected code and briefly explain the bugs.

## TEST 2 — FastAPI Backend

Create a small FastAPI application for recording student attendance.

Requirements:
1. POST /attendance accepts student_name and status.
2. status must only be "present" or "absent".
3. Store records in memory only.
4. GET /attendance returns all records.
5. GET /attendance/{student_name} returns that student's records.
6. Return HTTP 404 if the student does not exist.
7. Give complete runnable Python code.
8. Do not use a database or external service.


## TEST 3 — HTML + JavaScript

Create a single-file HTML application for calculating a student's average mark.

Requirements:
1. Inputs for Mathematics, English and Science.
2. Every mark must be between 0 and 100.
3. A Calculate button.
4. Display the average to two decimal places.
5. Display "Invalid mark" if any value is missing or outside 0–100.
6. Use only HTML, CSS and vanilla JavaScript.
7. Everything must be contained in one HTML file.
8. Give complete working code.


## TEST 4 — Arduino Component Constraint

I have only:
- Arduino Uno
- one HC-SR04 ultrasonic sensor
- one SG90 servo motor
- jumper wires

Create an automatic dustbin.

Requirements:
1. Open when an object is 40 cm or nearer.
2. Remain open while the object remains within 40 cm.
3. Close 2 seconds after the object leaves.
4. If the object returns before the 2 seconds finish, keep the lid open.
5. Do not use any component I did not list.
6. Give every pin connection.
7. Give complete Arduino code.
8. Handle the case where the HC-SR04 receives no echo.
9. Do not use an external ultrasonic library.


## TEST 5 — Kiswahili Teaching

Mwanafunzi wa kidato cha kwanza hajawahi kusoma programming.

Mfundishe maana ya:
1. variable
2. if statement
3. loop
4. function

Tumia Kiswahili rahisi lakini majina ya programming kama variable, if statement, loop na function yaendelee kuwa kwa Kiingereza.

Baada ya maelezo, toa mfano mmoja mdogo wa Python unaotumia variable, if statement, loop na function pamoja.

Usitumie istilahi ngumu ambazo hujaeleza.
