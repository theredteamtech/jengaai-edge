# Qwen2.5-Coder-1.5B-Instruct Q4_K_M Baseline


## Hardware
- Backend: CPU
- Threads: 4
- WSL RAM: approximately 7.6 GiB

## Model
- Parameters: 1.78B
- GGUF size: 1.04 GiB
- Quantization: Q4_K_M

## llama-bench
- pp512: 68.33 ± 9.62 tokens/s
- tg128: 22.24 ± 5.29 tokens/s

## Interactive Test
- Observed generation: 13.5 tokens/s

## Arduino Constraint Test
Prompt:
"I have an Arduino Uno, one HC-SR04 ultrasonic sensor, one SG90 servo motor, and jumper wires..."

### Problems identified
1. Invented SDA/SCL wiring.
2. Introduced unnecessary NewPing library.
3. Incorrect HC-SR04 distance formula.
4. Contradictory servo wiring instructions.
5. Unnecessary servo pinMode.
6. Poor handling of invalid/no-echo distance readings.

## Current Decision
Fast and lightweight, but engineering accuracy is insufficient.
