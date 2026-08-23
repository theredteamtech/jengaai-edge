# Technical Report — JengaAI Edge / JengaCoder v1.2

**Team ID:** jengaai-edge  
**Domain:** coding_assistants  
**Model:** JengaCoder-v1.2-Q4_K_M  
**Runtime:** llama.cpp  
**Quantization:** GGUF Q4_K_M  
**Parameters:** 1.54B  

---

## 1. Problem

JengaAI Edge is an offline AI engineering and coding assistant designed for students, developers and technology learners who may not always have reliable or affordable Internet access.

Many modern AI coding assistants depend on continuous cloud connectivity and relatively powerful hardware. This can make them difficult to use in schools, laboratories, rural communities and other environments where Internet bandwidth, data cost and computing resources are limited.

JengaCoder addresses this problem by running completely locally on a budget laptop after the model has been downloaded. During inference it requires no external API, cloud model or Internet connection.

The model focuses on practical programming and engineering assistance, including Python programming, debugging, Arduino and embedded-system projects, basic web development and technical explanations.

A major target use case is education in African schools and technology communities where learners can use an AI assistant even when Internet connectivity is unavailable.

---

## 2. Design Decisions

JengaCoder v1.2 is based on Qwen2.5-Coder-1.5B-Instruct and was adapted toward practical coding and engineering assistance.

The 1.5B parameter size was selected because it provides a useful balance between code-generation capability and the memory and CPU limitations of an approximately 8 GB laptop.

The model was adapted using LoRA-based fine-tuning with examples focused on coding, debugging, embedded systems and practical engineering instructions.

Several later corrective experiments were evaluated during development. JengaCoder v1.3 and v1.4 attempted to improve hardware-constraint following and Kiswahili responses. Private evaluation revealed regressions such as unnecessary hardware generation and weaker instruction following in some embedded-system tasks. Those experimental versions were rejected.

JengaCoder v1.2 was therefore retained as the final model because it provided the best overall balance of coding quality, instruction following and generalization observed during development.

### Quantization

The final merged model was converted to GGUF and quantized to Q4_K_M.

Q4_K_M was selected because it provides a strong compromise between:

- model quality,
- storage size,
- inference memory,
- and CPU inference speed.

The final GGUF is approximately 941 MB while retaining all 1.54 billion model parameters.

The model runs through llama.cpp without GPU acceleration.

---

## 3. Constraints

JengaAI Edge was developed around the ADTC budget-laptop target.

The final profiling environment was:

- Intel Core i7-1065G7 CPU @ 1.30 GHz
- 4 CPU threads/vCPUs used by the profiler
- 7.6 GB available system RAM
- no discrete GPU
- Ubuntu 22.04.5 LTS under the development environment
- llama.cpp CPU inference

The project was designed to remain comfortably below the competition memory limit.

The final model reached approximately 1.69 GB peak resident memory during profiling, leaving substantial memory available for the operating system and other applications.

Connectivity was another important constraint. JengaCoder performs inference entirely offline. Network access is required only to obtain the model weights before evaluation. After loading the GGUF, generation does not depend on cloud APIs or external services.

The final model is distributed through a public Hugging Face repository and the provided `download_model.sh` retrieves and verifies the model before use.

SHA-256:

`e253182086f2bfd9e48ee3e4b683f151276fa1dfc6510faea8be0824dbe433bc`

---

## 4. Example Capabilities

One evaluation prompt asked JengaCoder to create a Python function that calculates an average while correctly handling an empty list. The generated solution correctly returned zero for an empty list and provided the requested example calls.

Another evaluation asked JengaCoder to design an automatic dustbin using only an Arduino Uno, HC-SR04 ultrasonic sensor, SG90 servo and jumper wires.

The model produced:

- HC-SR04 pin connections,
- SG90 servo connections,
- a complete Arduino sketch,
- ultrasonic distance measurement,
- servo control,
- and a testing procedure,

without introducing additional hardware components.

These tasks demonstrate the intended combination of general coding assistance and practical engineering support.

---

## 5. Benchmarks

The final full participant-mode ADTC profiler run produced the following results:

| Metric | Result |
| --- | ---: |
| Model parameters | 1,543,714,304 |
| GGUF quantization | Q4_K_M |
| Context length | 32,768 |
| Generation throughput | 18.1 tokens/s |
| Prompt benchmark length | 512 tokens |
| Generated benchmark length | 128 tokens |
| First-token latency | 7802.23 ms |
| Peak RSS memory | 1692.50 MB |
| Steady-state RSS | 1616.07 MB |
| Peak virtual memory | 2175.98 MB |
| ARC Easy accuracy | 0.70 |
| ARC Easy samples | 50 |
| Thermal throttling | None detected |
| CPU p99 utilization | 51.1% |

The accuracy measurement was generated by the official ADTC profiler using the `arc_easy` benchmark with `acc_norm`.

A separate llama.cpp controlled benchmark also demonstrated CPU-only operation of the Q4_K_M model.

No GPU acceleration was used for the reported ADTC profiler measurements.

---

## 6. Limitations

JengaCoder is a compact 1.54B parameter model and does not provide the same reasoning depth as much larger cloud-hosted language models.

Private testing showed that constrained embedded-system generation can occasionally produce small instruction-following or implementation errors. Generated hardware code should therefore be reviewed and tested before deployment.

Kiswahili capability is experimental and English remains the primary declared language scope for this submission.

The project's priority is not to replace large cloud models. Its goal is to provide useful coding and engineering assistance under hardware and connectivity conditions where those services may not be practical.

---

## 7. Conclusion

JengaAI Edge demonstrates that a useful coding and engineering assistant can operate completely offline on a budget-class laptop.

JengaCoder v1.2 combines a compact 1.54B model, Q4_K_M quantization and llama.cpp CPU inference to achieve 18.1 tokens per second while using approximately 1.69 GB peak resident memory during the official participant profiler run.

The project is intended to make practical AI-assisted learning and engineering more accessible in environments where connectivity, computing power and data cost are meaningful constraints.
