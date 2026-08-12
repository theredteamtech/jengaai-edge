import json
import random
from pathlib import Path


# ============================================================
# JengaCoder Dataset Builder v1
# ============================================================

SEED = 42
random.seed(SEED)

ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = ROOT / "training" / "data"

TRAIN_FILE = DATA_DIR / "jengacoder_train_v1.json"
VALIDATION_FILE = DATA_DIR / "jengacoder_validation_v1.json"
MANIFEST_FILE = DATA_DIR / "jengacoder_dataset_manifest.json"


# ============================================================
# System Prompts
# ============================================================

SYSTEM_ENGINEERING = (
    "You are JengaCoder, an offline engineering coding assistant "
    "for African students and developers. "
    "Follow the user's hardware constraints exactly. "
    "Never invent components. "
    "For physical systems, verify power, ground, pin configuration, "
    "timing, sensor failure cases, and program behavior before answering."
)

SYSTEM_KISWAHILI = (
    "You are JengaCoder, a beginner-friendly programming teacher. "
    "When the user asks in Kiswahili, respond in simple natural Kiswahili. "
    "Keep standard programming terms such as variable, if statement, "
    "loop, function, list, parameter, argument, return and condition "
    "in English where appropriate."
)

SYSTEM_CODING = (
    "You are JengaCoder. "
    "Produce correct runnable code, follow every requirement, "
    "check edge cases, and explain important decisions clearly."
)

SYSTEM_CONSTRAINTS = (
    "You are JengaCoder. "
    "Respect explicit user constraints exactly. "
    "Do not add hardware, libraries, frameworks, cloud services, "
    "or external dependencies unless the user allows them."
)


# ============================================================
# Helpers
# ============================================================

def make_example(
    system,
    instruction,
    output,
    input_text="",
    category="general",
):
    return {
        "system": system,
        "instruction": instruction,
        "input": input_text,
        "output": output,
        "_category": category,
    }


def code_block(language, lines):
    return (
        f"```{language}\n"
        + "\n".join(lines)
        + "\n```"
    )


def normalize(text):
    return " ".join(text.lower().split())


def fingerprint(item):
    return (
        normalize(item["instruction"]),
        normalize(item.get("input", "")),
    )


def ensure_unique(items):
    seen = set()

    for item in items:
        fp = fingerprint(item)

        if fp in seen:
            raise RuntimeError(
                "Duplicate dataset example detected:\n"
                + item["instruction"]
            )

        seen.add(fp)


# ============================================================
# Evaluation Leakage Protection
# ============================================================

def contains_evaluation_leak(item):
    """
    Prevent our private five evaluation tests from entering training.
    """

    text = normalize(
        item.get("instruction", "")
        + " "
        + item.get("input", "")
    )

    # Test 1: None-average debugging
    if (
        "average of valid numeric values" in text
        and "none values" in text
    ):
        return True

    # Test 2: attendance API
    if (
        "post /attendance" in text
        and "get /attendance" in text
    ):
        return True

    # Test 3: Math/English/Science calculator
    if (
        "mathematics" in text
        and "english" in text
        and "science" in text
        and "invalid mark" in text
    ):
        return True

    # Test 4: exact advanced dustbin challenge
    if (
        "automatic dustbin" in text
        and "40 cm" in text
        and "2 seconds" in text
    ):
        return True

    # Test 5: exact four-concept Kiswahili challenge
    if (
        "variable" in text
        and "if statement" in text
        and "loop" in text
        and "function" in text
        and "kidato cha kwanza" in text
    ):
        return True

    return False


# ============================================================
# CATEGORY 1
# Arduino / IoT State-Machine Training
# Target: 80 examples
# ============================================================

def build_arduino_state_examples():
    examples = []

    # Deliberately avoid 40 cm + 2000 ms,
    # which appears in our evaluation test.
    distances = [
        18,
        22,
        28,
        32,
        36,
        44,
        48,
        55,
        65,
    ]

    close_delays = [
        1200,
        1600,
        2400,
        2800,
        3200,
        4000,
    ]

    trig_echo_pairs = [
        (2, 3),
        (4, 7),
        (7, 8),
        (8, 9),
        (9, 10),
        (10, 11),
    ]

    servo_pins = [
        3,
        5,
        6,
        9,
        11,
    ]

    project_names = [
        "automatic storage-box lid",
        "contactless classroom container lid",
        "automatic cabinet lid",
        "touch-free storage lid",
        "automatic demonstration lid",
        "proximity-controlled flap",
    ]

    combinations = []

    for distance in distances:
        for close_delay in close_delays:
            for trig_pin, echo_pin in trig_echo_pairs:
                for servo_pin in servo_pins:

                    if servo_pin in (trig_pin, echo_pin):
                        continue

                    combinations.append(
                        (
                            distance,
                            close_delay,
                            trig_pin,
                            echo_pin,
                            servo_pin,
                        )
                    )

    random.shuffle(combinations)

    for index, combination in enumerate(
        combinations[:80]
    ):
        (
            distance,
            close_delay,
            trig_pin,
            echo_pin,
            servo_pin,
        ) = combination

        project_name = (
            project_names[
                index % len(project_names)
            ]
        )

        seconds = close_delay / 1000

        instruction = (
               f"I have only an Arduino Uno, one HC-SR04 ultrasonic sensor, "
               f"one SG90 servo motor and jumper wires. "
               f"Build a {project_name}. "
               f"Use D{trig_pin} for TRIG, D{echo_pin} for ECHO, "
               f"and D{servo_pin} for the servo signal. "
               f"Open when an object is {distance} cm or nearer. "
               f"Keep it open while the object is present. "
               f"Start a {seconds:g}-second closing timer only after "
               f"the object leaves. "
               f"If the object returns before the timer finishes, cancel "
               f"the closing action. "
               f"Handle no echo safely. "
               f"Do not use an external ultrasonic library."
                      )

        cpp = code_block(
            "cpp",
            [
                "#include <Servo.h>",
                "",
                f"const int TRIG_PIN = {trig_pin};",
                f"const int ECHO_PIN = {echo_pin};",
                f"const int SERVO_PIN = {servo_pin};",
                "",
                "const int CLOSED_ANGLE = 0;",
                "const int OPEN_ANGLE = 90;",
                f"const float THRESHOLD_CM = {distance}.0f;",
                (
                    "const unsigned long CLOSE_DELAY_MS = "
                    f"{close_delay}UL;"
                ),
                "",
                "Servo lid;",
                "",
                "bool lidOpen = false;",
                "bool closeTimerActive = false;",
                "unsigned long objectLeftAt = 0;",
                "",
                "float readDistanceCm() {",
                "  digitalWrite(TRIG_PIN, LOW);",
                "  delayMicroseconds(2);",
                "",
                "  digitalWrite(TRIG_PIN, HIGH);",
                "  delayMicroseconds(10);",
                "",
                "  digitalWrite(TRIG_PIN, LOW);",
                "",
                (
                    "  unsigned long duration = "
                    "pulseIn(ECHO_PIN, HIGH, 30000UL);"
                ),
                "",
                "  if (duration == 0) {",
                "    return -1.0f;",
                "  }",
                "",
                (
                    "  return duration * "
                    "0.0343f / 2.0f;"
                ),
                "}",
                "",
                "void setup() {",
                "  pinMode(TRIG_PIN, OUTPUT);",
                "  pinMode(ECHO_PIN, INPUT);",
                "",
                "  lid.attach(SERVO_PIN);",
                "  lid.write(CLOSED_ANGLE);",
                "}",
                "",
                "void loop() {",
                "  float distance = readDistanceCm();",
                "",
                (
                    "  bool objectPresent = "
                    "distance > 0 && "
                    "distance <= THRESHOLD_CM;"
                ),
                "",
                "  if (objectPresent) {",
                "",
                "    if (!lidOpen) {",
                "      lid.write(OPEN_ANGLE);",
                "      lidOpen = true;",
                "    }",
                "",
                "    closeTimerActive = false;",
                "  }",
                "",
                "  else if (lidOpen) {",
                "",
                "    if (!closeTimerActive) {",
                "      objectLeftAt = millis();",
                "      closeTimerActive = true;",
                "    }",
                "",
                (
                    "    if (millis() - objectLeftAt "
                    ">= CLOSE_DELAY_MS) {"
                ),
                "      lid.write(CLOSED_ANGLE);",
                "      lidOpen = false;",
                "      closeTimerActive = false;",
                "    }",
                "  }",
                "",
                "  delay(50);",
                "}",
            ],
        )

        output = "\n".join(
            [
                "Connections:",
                (
                    "- HC-SR04 VCC -> "
                    "Arduino 5V"
                ),
                (
                    "- HC-SR04 GND -> "
                    "Arduino GND"
                ),
                (
                    f"- HC-SR04 TRIG -> "
                    f"Arduino D{trig_pin}"
                ),
                (
                    f"- HC-SR04 ECHO -> "
                    f"Arduino D{echo_pin}"
                ),
                (
                    "- SG90 red/VCC -> "
                    "Arduino 5V"
                ),
                (
                    "- SG90 brown/GND -> "
                    "Arduino GND"
                ),
                (
                    f"- SG90 orange/signal -> "
                    f"Arduino D{servo_pin}"
                ),
                "",
                cpp,
                "",
                "Why this works:",
                (
                    "- HC-SR04 distance uses "
                    "`duration * 0.0343 / 2` "
                    "because the echo time is a round trip."
                ),
                (
                    "- `pulseIn(..., 30000UL)` "
                    "provides a timeout."
                ),
                (
                    "- A timeout returns -1 instead "
                    "of being interpreted as 0 cm."
                ),
                (
                    "- `millis()` provides non-blocking "
                    "timing, so the sensor continues being read."
                ),
                (
                    "- If the object returns before "
                    "closing, the close timer is cancelled."
                ),
            ]
        )

        examples.append(
            make_example(
                SYSTEM_ENGINEERING,
                instruction,
                output,
                category="arduino_state_machine",
            )
        )

    return examples


# ============================================================
# CATEGORY 2
# Arduino Engineering Reasoning
# Target: 20 examples
# ============================================================

def build_arduino_reasoning_examples():
    topics = [
        (
            "An HC-SR04 pulseIn call returned 0. "
            "What should the program do?",
            (
                "A duration of 0 normally means no echo was received "
                "before the timeout. Treat it as an invalid or no-echo "
                "reading. Do not interpret it as 0 cm."
            ),
        ),

        (
            "Why is HC-SR04 distance calculated using "
            "`duration * 0.0343 / 2`?",
            (
                "The echo duration measures sound travelling to the "
                "object and back. Multiplying by 0.0343 converts the "
                "time into travelled centimetres, and dividing by two "
                "gives the one-way distance."
            ),
        ),

        (
            "Why must the Arduino, HC-SR04 and servo share GND?",
            (
                "The devices need the same electrical reference for "
                "their signal voltages. Without common GND, sensor and "
                "servo signals may not be interpreted reliably."
            ),
        ),

        (
            "Does a normal HC-SR04 use SDA and SCL?",
            (
                "No. A normal HC-SR04 uses VCC, GND, TRIG and ECHO. "
                "SDA and SCL are I2C signals and are not required."
            ),
        ),

        (
            "Why use millis() instead of delay() when the sensor "
            "must keep being checked?",
            (
                "`delay()` blocks the main loop. A millis()-based "
                "timer allows the Arduino to keep reading sensors "
                "while waiting."
            ),
        ),

        (
            "Why must TRIG be OUTPUT and ECHO be INPUT?",
            (
                "The Arduino sends the trigger pulse through TRIG, "
                "so TRIG must be OUTPUT. The Arduino receives the echo "
                "pulse through ECHO, so ECHO must be INPUT."
            ),
        ),

        (
            "Does the SG90 signal wire require an Arduino pin "
            "marked with the PWM symbol?",
            (
                "Not necessarily. The Arduino Servo library generates "
                "servo control pulses using timers, so the signal wire "
                "does not have to use a pin marked as hardware PWM."
            ),
        ),

        (
            "What can happen if no echo is interpreted as zero distance?",
            (
                "The system may falsely believe an object is extremely "
                "close and activate the mechanism even though the sensor "
                "actually timed out."
            ),
        ),

        (
            "Why should the closing timer start only after "
            "the object leaves?",
            (
                "If the requirement says to close after departure, "
                "the timer must begin when the state changes from "
                "object-present to object-absent."
            ),
        ),

        (
            "How can Arduino cancel a pending close when "
            "the object returns?",
            (
                "Store whether the close timer is active. When the "
                "object leaves, record `millis()`. If the object returns "
                "before the delay expires, deactivate the timer."
            ),
        ),
    ]

    prefixes = [
        "Explain clearly:",
        "For a beginner, explain:",
    ]

    examples = []

    for topic, answer in topics:
        for prefix in prefixes:

            examples.append(
                make_example(
                    SYSTEM_ENGINEERING,
                    f"{prefix} {topic}",
                    answer,
                    category="arduino_reasoning",
                )
            )

    return examples


# ============================================================
# CATEGORY 3
# Kiswahili Programming Teaching
# Target: 40 examples
# ============================================================

def build_kiswahili_examples():
    concepts = {
        "variable": (
            "Variable ni sehemu yenye jina inayohifadhi thamani "
            "ambayo programu inaweza kutumia. Mfano `age = 14` "
            "huhifadhi 14 ndani ya variable inayoitwa `age`."
        ),

        "if statement": (
            "If statement hutumika kufanya uamuzi. Programu hukagua "
            "condition; ikiwa condition ni kweli, code iliyo ndani "
            "ya if statement inatekelezwa."
        ),

        "loop": (
            "Loop hutumika kurudia code mara kadhaa bila kuiandika "
            "tena na tena. Mfano `for` loop inaweza kuchapisha ujumbe "
            "mara kadhaa."
        ),

        "function": (
            "Function ni kundi la code lenye jina ambalo limeandaliwa "
            "kufanya kazi fulani. Unaweza kuita function kila "
            "unapohitaji kazi hiyo ifanyike."
        ),

        "list": (
            "List huhifadhi thamani nyingi pamoja. Mfano "
            "`marks = [70, 80, 65]` huhifadhi marks tatu "
            "ndani ya list moja."
        ),

        "parameter": (
            "Parameter ni jina linalowekwa kwenye function ili function "
            "iweze kupokea taarifa. Katika `def greet(name):`, "
            "`name` ni parameter."
        ),

        "argument": (
            "Argument ni thamani halisi tunayopeleka kwenye function "
            "tunapoiita. Katika `greet(\"Asha\")`, `\"Asha\"` "
            "ni argument."
        ),

        "return": (
            "Return hutumika kurudisha jibu kutoka ndani ya function "
            "kwenda sehemu iliyoita function hiyo."
        ),

        "condition": (
            "Condition ni kipimo kinachoweza kuwa true au false. "
            "If statement hutumia condition kufanya uamuzi."
        ),

        "string": (
            "String ni aina ya data inayohifadhi maandishi. "
            "Mfano `name = \"Amina\"` ina string `\"Amina\"`."
        ),
    }

    phrases = [
        "Elezea kwa Kiswahili rahisi maana ya",
        "Mfundishe mwanafunzi anayeanza programming maana ya",
        "Toa maelezo mafupi kuhusu",
        "Mwanafunzi mpya wa programming anauliza kuhusu",
    ]

    examples = []

    for concept, explanation in concepts.items():

        for phrase in phrases:

            instruction = (
                f"{phrase} {concept}. "
                "Usitumie istilahi ngumu bila kuzieleza."
            )

            examples.append(
                make_example(
                    SYSTEM_KISWAHILI,
                    instruction,
                    explanation,
                    category="kiswahili_teaching",
                )
            )

    return examples


# ============================================================
# CATEGORY 4
# Debugging
# Target: 20 examples
# ============================================================

def build_debugging_examples():
    templates = [
        {
            "instruction": (
                "Fix this function so division by zero returns None."
            ),
            "input": (
                "def divide(a, b):\n"
                "    return a / b"
            ),
            "output": code_block(
                "python",
                [
                    "def divide(a, b):",
                    "    if b == 0:",
                    "        return None",
                    "    return a / b",
                ],
            ),
        },

        {
            "instruction": (
                "Fix this function so an empty list returns 0."
            ),
            "input": (
                "def mean(values):\n"
                "    return sum(values) / len(values)"
            ),
            "output": code_block(
                "python",
                [
                    "def mean(values):",
                    "    if not values:",
                    "        return 0",
                    "    return sum(values) / len(values)",
                ],
            ),
        },

        {
            "instruction": (
                "Fix this function so 50 is a pass and marks "
                "outside 0 to 100 raise ValueError."
            ),
            "input": (
                "def result(mark):\n"
                "    if mark > 50:\n"
                '        return "pass"\n'
                '    return "fail"'
            ),
            "output": code_block(
                "python",
                [
                    "def result(mark):",
                    "    if mark < 0 or mark > 100:",
                    (
                        '        raise ValueError('
                        '"mark must be between 0 and 100")'
                    ),
                    '    return "pass" if mark >= 50 else "fail"',
                ],
            ),
        },

        {
            "instruction": (
                "Fix this function so zero is not counted as positive."
            ),
            "input": (
                "def count_positive(numbers):\n"
                "    count = 0\n"
                "    for n in numbers:\n"
                "        if n >= 0:\n"
                "            count += 1\n"
                "    return count"
            ),
            "output": code_block(
                "python",
                [
                    "def count_positive(numbers):",
                    "    count = 0",
                    "    for n in numbers:",
                    "        if n > 0:",
                    "            count += 1",
                    "    return count",
                ],
            ),
        },

        {
            "instruction": (
                "Fix this function so it returns the smallest value."
            ),
            "input": (
                "def smallest(numbers):\n"
                "    result = numbers[0]\n"
                "    for n in numbers[1:]:\n"
                "        if n > result:\n"
                "            result = n\n"
                "    return result"
            ),
            "output": code_block(
                "python",
                [
                    "def smallest(numbers):",
                    "    result = numbers[0]",
                    "    for n in numbers[1:]:",
                    "        if n < result:",
                    "            result = n",
                    "    return result",
                ],
            ),
        },
    ]

    prefixes = [
        "Debug carefully.",
        "Correct the bug and explain the fix briefly.",
        "Return runnable Python code.",
        "Check the edge case before answering.",
    ]

    examples = []

    for template in templates:

        for prefix in prefixes:

            examples.append(
                make_example(
                    SYSTEM_CODING,
                    (
                        f"{prefix} "
                        f"{template['instruction']}"
                    ),
                    template["output"],
                    input_text=template["input"],
                    category="debugging",
                )
            )

    return examples


# ============================================================
# CATEGORY 5
# General Coding Retention
# Target: 10 examples
# ============================================================

def build_retention_examples():
    tasks = [
        (
            "Write a Python function that returns the largest "
            "number in a non-empty list.",
            code_block(
                "python",
                [
                    "def largest(numbers):",
                    "    maximum = numbers[0]",
                    "    for number in numbers[1:]:",
                    "        if number > maximum:",
                    "            maximum = number",
                    "    return maximum",
                ],
            ),
        ),

        (
            "Write a Python function that counts even numbers.",
            code_block(
                "python",
                [
                    "def count_even(numbers):",
                    "    count = 0",
                    "    for number in numbers:",
                    "        if number % 2 == 0:",
                    "            count += 1",
                    "    return count",
                ],
            ),
        ),

        (
            "Create a FastAPI GET /health endpoint "
            "that returns status ok.",
            code_block(
                "python",
                [
                    "from fastapi import FastAPI",
                    "",
                    "app = FastAPI()",
                    "",
                    '@app.get("/health")',
                    "def health():",
                    '    return {"status": "ok"}',
                ],
            ),
        ),

        (
            "Create a FastAPI GET /hello/{name} endpoint.",
            code_block(
                "python",
                [
                    "from fastapi import FastAPI",
                    "",
                    "app = FastAPI()",
                    "",
                    '@app.get("/hello/{name}")',
                    "def hello(name: str):",
                    (
                        '    return {"message": '
                        'f"Hello, {name}"}'
                    ),
                ],
            ),
        ),

        (
            "Create JavaScript that checks whether a number "
            "is between 1 and 10.",
            code_block(
                "javascript",
                [
                    "function inRange(value) {",
                    (
                        "    return Number.isFinite(value) "
                        "&& value >= 1 && value <= 10;"
                    ),
                    "}",
                ],
            ),
        ),

        (
            "Write a Python function that returns True "
            "if a string is empty.",
            code_block(
                "python",
                [
                    "def is_empty(text):",
                    '    return text == ""',
                ],
            ),
        ),

        (
            "Write a Python function that converts Celsius "
            "to Fahrenheit.",
            code_block(
                "python",
                [
                    "def celsius_to_fahrenheit(celsius):",
                    "    return (celsius * 9 / 5) + 32",
                ],
            ),
        ),

        (
            "Write a Python function that sums numbers in a list.",
            code_block(
                "python",
                [
                    "def total(numbers):",
                    "    result = 0",
                    "    for number in numbers:",
                    "        result += number",
                    "    return result",
                ],
            ),
        ),

        (
            "Create JavaScript that formats a number "
            "to two decimal places.",
            code_block(
                "javascript",
                [
                    "function formatTwoDecimals(value) {",
                    "    return Number(value).toFixed(2);",
                    "}",
                ],
            ),
        ),

        (
            "Write a Python function that returns the square "
            "of a number.",
            code_block(
                "python",
                [
                    "def square(number):",
                    "    return number * number",
                ],
            ),
        ),
    ]

    return [
        make_example(
            SYSTEM_CODING,
            instruction,
            output,
            category="retention",
        )
        for instruction, output in tasks
    ]


# ============================================================
# CATEGORY 6
# Constraint Following
# Target: 10 examples
# ============================================================

def build_constraint_examples():
    scenarios = [
        (
            "I have Arduino Uno, one LED and jumper wires only. "
            "Do not use a buzzer.",
            (
                "Use only the Arduino Uno, LED and jumper wires. "
                "I will not add a buzzer or another unlisted component."
            ),
        ),

        (
            "I have Arduino Uno and one ultrasonic sensor only. "
            "Do not assume I have a servo.",
            (
                "The solution must use only the Arduino Uno and "
                "ultrasonic sensor. I will not include servo code."
            ),
        ),

        (
            "Use only Python standard library. Do not use pandas.",
            (
                "I will use only Python's standard library and will "
                "not import pandas or another third-party package."
            ),
        ),

        (
            "Create a webpage using only HTML, CSS and vanilla "
            "JavaScript. Do not use React.",
            (
                "The solution will use HTML, CSS and vanilla JavaScript "
                "only. I will not add React or another framework."
            ),
        ),

        (
            "The program must work completely offline.",
            (
                "The design will not depend on cloud APIs, remote "
                "databases, CDNs or other network services at runtime."
            ),
        ),

        (
            "Use SQLite only. Do not use PostgreSQL or Supabase.",
            (
                "The solution will use SQLite only and will not introduce "
                "PostgreSQL, Supabase or another database service."
            ),
        ),

        (
            "I have ESP32, one buzzer and jumper wires. "
            "Do not add an ultrasonic sensor.",
            (
                "The design will use only the ESP32, buzzer and jumper "
                "wires. I will not add an ultrasonic sensor."
            ),
        ),

        (
            "Do not install an external library for this Python task.",
            (
                "I will solve the task using Python built-in features "
                "and standard library only."
            ),
        ),

        (
            "The application must not call OpenAI, Gemini "
            "or another online API.",
            (
                "The application will run locally and will not call "
                "OpenAI, Gemini or another online API."
            ),
        ),

        (
            "Do not use delay() for a timer that must continue "
            "reacting to sensor changes.",
            (
                "I will use non-blocking timing such as `millis()` "
                "so the program can continue checking sensors."
            ),
        ),
    ]

    return [
        make_example(
            SYSTEM_CONSTRAINTS,
            instruction,
            output,
            category="constraints",
        )
        for instruction, output in scenarios
    ]


# ============================================================
# Dataset Split
# ============================================================

VALIDATION_COUNTS = {
    "arduino_state_machine": 8,
    "arduino_reasoning": 2,
    "kiswahili_teaching": 4,
    "debugging": 2,
    "retention": 2,
    "constraints": 2,
}


def split_dataset(items):
    groups = {}

    for item in items:

        category = item["_category"]

        groups.setdefault(
            category,
            [],
        ).append(item)

    validation = []
    training = []

    for category, category_items in groups.items():

        random.shuffle(category_items)

        validation_count = (
            VALIDATION_COUNTS.get(
                category,
                0,
            )
        )

        validation.extend(
            category_items[:validation_count]
        )

        training.extend(
            category_items[validation_count:]
        )

    random.shuffle(training)
    random.shuffle(validation)

    return training, validation


def clean_for_training(items):
    cleaned = []

    for item in items:

        cleaned.append(
            {
                "system": item["system"],
                "instruction": item["instruction"],
                "input": item.get(
                    "input",
                    "",
                ),
                "output": item["output"],
            }
        )

    return cleaned


def category_counts(items):
    counts = {}

    for item in items:

        category = item["_category"]

        counts[category] = (
            counts.get(category, 0) + 1
        )

    return counts


# ============================================================
# Main
# ============================================================

def main():
    DATA_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    all_examples = []

    all_examples.extend(
        build_arduino_state_examples()
    )

    all_examples.extend(
        build_arduino_reasoning_examples()
    )

    all_examples.extend(
        build_kiswahili_examples()
    )

    all_examples.extend(
        build_debugging_examples()
    )

    all_examples.extend(
        build_retention_examples()
    )

    all_examples.extend(
        build_constraint_examples()
    )

    # --------------------------------------------------------
    # Expected total
    # --------------------------------------------------------
    # Arduino state       80
    # Arduino reasoning   20
    # Kiswahili           40
    # Debugging           20
    # Retention           10
    # Constraints         10
    # -----------------------
    # TOTAL              180
    # --------------------------------------------------------

    print(
        f"Generated examples: {len(all_examples)}"
    )

    if len(all_examples) != 180:

        raise RuntimeError(
            "Dataset generator expected exactly "
            f"180 examples but produced "
            f"{len(all_examples)}."
        )

    ensure_unique(all_examples)

    # Evaluation leakage check
    leaked = [
        item
        for item in all_examples
        if contains_evaluation_leak(item)
    ]

    if leaked:

        print(
            "\nWARNING: Evaluation leakage detected:"
        )

        for item in leaked:
            print(
                "-",
                item["instruction"],
            )

        raise RuntimeError(
            "Evaluation leakage detected. "
            "Training stopped."
        )

    training, validation = (
        split_dataset(all_examples)
    )

    if len(training) != 160:

        raise RuntimeError(
            f"Expected 160 training examples, "
            f"got {len(training)}."
        )

    if len(validation) != 20:

        raise RuntimeError(
            f"Expected 20 validation examples, "
            f"got {len(validation)}."
        )

    training_counts = (
        category_counts(training)
    )

    validation_counts = (
        category_counts(validation)
    )

    with TRAIN_FILE.open(
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            clean_for_training(training),
            file,
            ensure_ascii=False,
            indent=2,
        )

    with VALIDATION_FILE.open(
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            clean_for_training(validation),
            file,
            ensure_ascii=False,
            indent=2,
        )

    manifest = {
        "dataset_version": "jengacoder-v1",
        "random_seed": SEED,
        "total_examples": 180,
        "training_examples": 160,
        "validation_examples": 20,
        "evaluation_leak_filter": True,
        "training_category_counts": (
            training_counts
        ),
        "validation_category_counts": (
            validation_counts
        ),
    }

    with MANIFEST_FILE.open(
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            manifest,
            file,
            ensure_ascii=False,
            indent=2,
        )

    print()
    print(
        "JengaCoder dataset built successfully"
    )

    print(
        "Training examples:   ",
        len(training),
    )

    print(
        "Validation examples: ",
        len(validation),
    )

    print(
        "Total:               ",
        len(training) + len(validation),
    )

    print(
        "Seed:                ",
        SEED,
    )

    print()
    print(
        "Training categories:"
    )

    for category in sorted(
        training_counts
    ):
        print(
            f"  {category}: "
            f"{training_counts[category]}"
        )

    print()
    print(
        "Validation categories:"
    )

    for category in sorted(
        validation_counts
    ):
        print(
            f"  {category}: "
            f"{validation_counts[category]}"
        )

    print()
    print(
        f"Training file:   {TRAIN_FILE}"
    )

    print(
        f"Validation file: "
        f"{VALIDATION_FILE}"
    )

    print(
        f"Manifest file:   "
        f"{MANIFEST_FILE}"
    )


if __name__ == "__main__":
    main()
