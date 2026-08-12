import json
import re
import sys
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parents[2]

TRAIN_FILE = ROOT / "training/data/jengacoder_train_v1.json"
VAL_FILE = ROOT / "training/data/jengacoder_validation_v1.json"

errors = []
warnings = []


def load_json(path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def normalize(text):
    return " ".join(text.lower().split())


def report_error(index, dataset_name, message):
    errors.append(
        f"[ERROR] {dataset_name} example {index}: {message}"
    )


def report_warning(index, dataset_name, message):
    warnings.append(
        f"[WARNING] {dataset_name} example {index}: {message}"
    )


def check_required_fields(item, index, dataset_name):
    required = [
        "system",
        "instruction",
        "input",
        "output",
    ]

    for field in required:
        if field not in item:
            report_error(
                index,
                dataset_name,
                f"missing field '{field}'",
            )

        elif not isinstance(item[field], str):
            report_error(
                index,
                dataset_name,
                f"field '{field}' is not a string",
            )


def check_empty_fields(item, index, dataset_name):
    for field in ["system", "instruction", "output"]:
        if not item.get(field, "").strip():
            report_error(
                index,
                dataset_name,
                f"'{field}' is empty",
            )


def check_evaluation_leakage(item, index, dataset_name):
    text = normalize(
        item.get("instruction", "")
        + " "
        + item.get("input", "")
    )

    # TEST 1
    if (
        "average of valid numeric values" in text
        and "none values" in text
    ):
        report_error(
            index,
            dataset_name,
            "possible leakage from Python evaluation test",
        )

    # TEST 2
    if (
        "post /attendance" in text
        and "get /attendance" in text
    ):
        report_error(
            index,
            dataset_name,
            "possible leakage from FastAPI evaluation test",
        )

    # TEST 3
    if (
        "mathematics" in text
        and "english" in text
        and "science" in text
        and "invalid mark" in text
    ):
        report_error(
            index,
            dataset_name,
            "possible leakage from HTML evaluation test",
        )

    # TEST 4
    if (
        "automatic dustbin" in text
        and "40 cm" in text
        and "2 seconds" in text
    ):
        report_error(
            index,
            dataset_name,
            "possible leakage from Arduino evaluation test",
        )

    # TEST 5
    if (
        "kidato cha kwanza" in text
        and "variable" in text
        and "if statement" in text
        and "loop" in text
        and "function" in text
    ):
        report_error(
            index,
            dataset_name,
            "possible leakage from Kiswahili evaluation test",
        )


def looks_like_hcsr04(item):
    text = normalize(
        item.get("instruction", "")
        + " "
        + item.get("output", "")
    )

    return (
        "hc-sr04" in text
        or "ultrasonic" in text
    )


def check_hcsr04(item, index, dataset_name):
    if not looks_like_hcsr04(item):
        return

    output = item.get("output", "")
    lower = output.lower()

    # Detect the known bad formula.
    bad_formulas = [
        "duration / 29.1",
        "duration/29.1",
        "duration /29.1",
        "duration/ 29.1",
    ]

    for formula in bad_formulas:
        if formula in lower:
            report_error(
                index,
                dataset_name,
                "incorrect HC-SR04 /29.1 formula detected",
            )

    # A correct engineering answer should normally
    # explain the round trip.
    if (
        "pulsein" in lower
        and "/ 2" not in lower
        and "/2" not in lower
        and "/ 58" not in lower
        and "/58" not in lower
    ):
        report_warning(
            index,
            dataset_name,
            "HC-SR04 answer may not account for round-trip distance",
        )

    # Check no-echo handling where pulseIn is used.
    if "pulsein" in lower:
        no_echo_patterns = [
            "duration == 0",
            "duration==0",
            "return -1",
            "no echo",
            "no-echo",
            "timeout",
        ]

        if not any(
            pattern in lower
            for pattern in no_echo_patterns
        ):
            report_error(
                index,
                dataset_name,
                "pulseIn used without clear no-echo handling",
            )


def looks_like_full_arduino_project(item):
    output = item.get("output", "").lower()

    return (
        "```cpp" in output
        and "hc-sr04" in output
        and "servo" in output
    )


def check_arduino_wiring(item, index, dataset_name):
    if not looks_like_full_arduino_project(item):
        return

    output = item.get("output", "").lower()

    required_terms = [
        "vcc",
        "gnd",
        "trig",
        "echo",
        "signal",
    ]

    for term in required_terms:
        if term not in output:
            report_error(
                index,
                dataset_name,
                f"Arduino hardware answer missing '{term}'",
            )

    if "pinmode(trig_pin, output)" not in output.replace(" ", ""):
        compact = output.replace(" ", "")

        if "pinmode(trig_pin,output)" not in compact:
            report_error(
                index,
                dataset_name,
                "TRIG pinMode OUTPUT not found",
            )

    compact = output.replace(" ", "")

    if "pinmode(echo_pin,input)" not in compact:
        report_error(
            index,
            dataset_name,
            "ECHO pinMode INPUT not found",
        )


def check_blocking_delay(item, index, dataset_name):
    instruction = normalize(
        item.get("instruction", "")
    )

    output = item.get("output", "").lower()

    needs_continuous_sensing = any(
        phrase in instruction
        for phrase in [
            "if the object returns",
            "cancel closing",
            "keep it open while",
            "continue checking",
        ]
    )

    if not needs_continuous_sensing:
        return

    suspicious_delays = re.findall(
        r"delay\s*\(\s*(1[0-9]{3}|[2-9][0-9]{3,})\s*\)",
        output,
    )

    if suspicious_delays:
        report_error(
            index,
            dataset_name,
            "blocking long delay found in continuous-sensing example",
        )

    if "millis()" not in output and "millis (" not in output:
        report_error(
            index,
            dataset_name,
            "continuous-sensing timer does not use millis()",
        )


def check_for_invented_i2c(item, index, dataset_name):
    text = normalize(item.get("instruction", ""))
    output = normalize(item.get("output", ""))

    if "hc-sr04" in text:
        if (
            "sda ->" in output
            or "scl ->" in output
            or "sda:" in output
            or "scl:" in output
        ):
            report_error(
                index,
                dataset_name,
                "invented SDA/SCL wiring for HC-SR04",
            )


def check_code_fences(item, index, dataset_name):
    output = item.get("output", "")

    fence_count = output.count("```")

    if fence_count % 2 != 0:
        report_error(
            index,
            dataset_name,
            "unbalanced Markdown code fences",
        )


def check_kiswahili(item, index, dataset_name):
    system = normalize(item.get("system", ""))

    if "kiswahili" not in system:
        return

    output = normalize(item.get("output", ""))

    bad_phrases = [
        '"variable" ni "maana"',
        '"function" ni "maana"',
        "variable ni maana",
        "function ni maana",
    ]

    for phrase in bad_phrases:
        if phrase in output:
            report_error(
                index,
                dataset_name,
                f"poor Kiswahili phrase detected: {phrase}",
            )

    # Very crude check for answers accidentally written mostly in English.
    swahili_markers = [
     "ni ",
     "hutumika",
     "programu",
     "mwanafunzi",
     "mfano",
     "ikiwa",
     "huhifadhi",
     "kufanya",
     "kurudia",
     "thamani",
     "jina",
     "taarifa",
     "ndani",
     "kwenye",
     "inayoweza",
     "tunapo",
     "tunapoiita",
     "kurudisha",
     "maandishi",
     "hupokea",
    ]

    count = sum(
        marker in output
        for marker in swahili_markers
    )

    if count < 2:
        report_warning(
            index,
            dataset_name,
            "Kiswahili answer may contain too little natural Kiswahili",
        )


def check_duplicates(train, validation):
    all_items = (
        [("train", i, x) for i, x in enumerate(train)]
        +
        [
            ("validation", i, x)
            for i, x in enumerate(validation)
        ]
    )

    fingerprints = {}

    for dataset_name, index, item in all_items:
        fp = (
            normalize(item.get("instruction", "")),
            normalize(item.get("input", "")),
        )

        if fp in fingerprints:
            original = fingerprints[fp]

            errors.append(
                "[ERROR] duplicate instruction/input found: "
                f"{original} and "
                f"{dataset_name} example {index}"
            )
        else:
            fingerprints[fp] = (
                f"{dataset_name} example {index}"
            )


def audit_dataset(data, dataset_name):
    for index, item in enumerate(data):
        check_required_fields(
            item,
            index,
            dataset_name,
        )

        check_empty_fields(
            item,
            index,
            dataset_name,
        )

        check_evaluation_leakage(
            item,
            index,
            dataset_name,
        )

        check_hcsr04(
            item,
            index,
            dataset_name,
        )

        check_arduino_wiring(
            item,
            index,
            dataset_name,
        )

        check_blocking_delay(
            item,
            index,
            dataset_name,
        )

        check_for_invented_i2c(
            item,
            index,
            dataset_name,
        )

        check_code_fences(
            item,
            index,
            dataset_name,
        )

        check_kiswahili(
            item,
            index,
            dataset_name,
        )


def main():
    train = load_json(TRAIN_FILE)
    validation = load_json(VAL_FILE)

    print("JengaCoder Dataset Audit")
    print("=" * 50)

    print(
        f"Training examples:   {len(train)}"
    )

    print(
        f"Validation examples: {len(validation)}"
    )

    print(
        f"Total examples:      {len(train) + len(validation)}"
    )

    audit_dataset(
        train,
        "training",
    )

    audit_dataset(
        validation,
        "validation",
    )

    check_duplicates(
        train,
        validation,
    )

    print()
    print(
        f"Errors:   {len(errors)}"
    )

    print(
        f"Warnings: {len(warnings)}"
    )

    if warnings:
        print()
        print("WARNINGS")
        print("-" * 50)

        for warning in warnings:
            print(warning)

    if errors:
        print()
        print("ERRORS")
        print("-" * 50)

        for error in errors:
            print(error)

        print()
        print(
            "DATASET AUDIT FAILED"
        )

        sys.exit(1)

    print()
    print(
        "DATASET AUDIT PASSED"
    )

    print(
        "No critical dataset problems detected."
    )


if __name__ == "__main__":
    main()
