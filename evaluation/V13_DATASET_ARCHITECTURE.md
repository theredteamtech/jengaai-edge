# JengaCoder v1.3 — Corrective Dataset Architecture

## Objective

Improve JengaCoder v1.2's identified weaknesses without destroying its existing
strengths in basic coding, offline operation, streaming, and resource-constrained
software tasks.

The frozen ConstraintBench v1 evaluation prompts MUST NOT be used, paraphrased,
or transformed into training examples.

---

## Skill Families

### 1. Physical / Electrical Grounding — 30%

Teach the model to map software requirements to electrically valid physical
connections.

Coverage should include:
- resistor placement
- LED polarity
- sensor power and ground
- analog input topology
- PWM output topology
- digital input/output behavior
- voltage compatibility
- shared ground requirements
- active-high vs active-low signals
- safe interface recognition

Training tasks must use scenarios different from the frozen benchmark.

---

### 2. Global Constraint Consistency — 20%

Teach the model to track all constraints simultaneously.

Coverage should include:
- exact component inventories
- exact pins
- forbidden libraries
- memory limits
- one-pass restrictions
- no-allocation restrictions
- exact output formats
- impossible specifications
- mutually incompatible constraints

The model should explicitly state when a specification cannot be satisfied rather
than silently violating constraints.

---

### 3. Contrastive Embedded Scenarios — 15%

Use closely related but deliberately different scenarios so the model learns
when a component or behavior is allowed.

Examples of contrast structure:

Scenario A:
- sensor only
- no servo available
- model must not invent servo

Scenario B:
- same class of sensor
- servo explicitly provided
- servo use is permitted

Other contrast families:
- normal LED vs RGB LED
- Arduino Uno vs ESP32
- external pull-down vs INPUT_PULLUP
- 3.3V GPIO vs 5V-tolerant interface
- PWM-capable vs non-PWM pins

Do not reuse frozen evaluation scenarios.

---

### 4. Control-Flow / Postcondition Reasoning — 15%

Teach the model to reason about program state after exceptional or failed
operations.

Coverage should include:
- FileNotFoundError
- malformed input
- failed sensor reads
- timeouts
- empty input
- initialization
- early return
- fallback state
- invalid data
- boundary conditions

The response must remain correct after the error path, not merely contain an
exception handler.

---

### 5. Board and API Correctness — 10%

Teach platform-specific behavior.

Coverage should distinguish:
- Arduino Uno
- ESP32
- generic C++ host environment

Examples:
- ADC ranges
- PWM APIs
- pin capabilities
- supported functions
- voltage logic
- board-specific libraries
- functions that exist on one platform but not another

Avoid mixing APIs across platforms.

---

### 6. Preservation / General Coding — 10%

Preserve abilities that v1.2 already performs well.

Coverage should include:
- streaming file processing
- standard-library-only Python
- simple C++ algorithms
- exact-output problems
- O(1) memory problems
- offline operation
- straightforward debugging

These examples should prevent corrective fine-tuning from degrading general
coding ability.

---

## Dataset Composition

Initial corrective target:

- 300 training examples
- 60 validation examples
- 40 internal holdout examples

Total new examples: 400

Suggested training distribution:

- Physical/electrical grounding: 90
- Constraint consistency: 60
- Contrastive embedded scenarios: 45
- Control-flow/postconditions: 45
- Board/API correctness: 30
- Preservation/general coding: 30

Validation and holdout sets should follow the same competency categories but use
different scenario families.

---

## Split Policy

DO NOT randomly split near-duplicate examples.

Use scenario-family separation.

Example:

Training:
- temperature sensor + indicator

Validation:
- soil moisture sensor + actuator

Holdout:
- light sensor + warning output

The underlying skill may be shared, but component combinations, wording, and
solution structure must differ.

---

## Training Example Requirements

Every example must:

1. Have one clearly defined competency target.
2. Contain a technically verified answer.
3. Obey every stated component and software constraint.
4. Avoid unnecessary components.
5. Avoid unsupported APIs.
6. Include correct failure behavior where relevant.
7. Avoid benchmark prompt paraphrases.
8. Be understandable without external internet access.

---

## Hardware Verification Metadata

Each hardware example should internally track:

- board
- allowed_components
- forbidden_components
- required_pins
- voltage_constraints
- required_behavior
- expected_api
- safety_status
- expected_wiring_properties

This metadata does not necessarily need to appear in the final user-visible
training answer, but should be available for dataset auditing.

---

## Contrastive Design Principle

Do not repeatedly teach:

"HC-SR04 means no servo."

Instead teach the broader rule:

"Only use components explicitly available or logically built into the stated
platform."

Likewise, do not teach one specific voltage case.

Teach:

"Before connecting two devices, verify signal-level compatibility. If the
available hardware cannot make the interface safe, say so rather than inventing
a software solution."

---

## Evaluation Isolation

The following are frozen and excluded from training:

- ConstraintBench experiments 001 through 010
- exact benchmark answers
- paraphrased benchmark prompts
- lightly modified versions of benchmark circuits
- judge prompts from Gate 1

These remain evaluation-only material.

---

## Promotion Rule

A new candidate must NOT replace JengaCoder v1.2 merely because training loss is
lower.

Promotion requires:

1. Higher ConstraintBench score.
2. No regression on preservation/general coding tests.
3. Improved hardware subset.
4. Improved impossible-constraint recognition.
5. Similar runtime speed.
6. Similar memory footprint.
7. Successful held-out validation.
8. No new component-invention pattern.

Training loss is supporting evidence only, not the promotion criterion.
