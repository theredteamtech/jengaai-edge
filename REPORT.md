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

The model was adapted using QLoRA fine-tuning with examples focused on coding, debugging, embedded systems and practical engineering instructions.

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


### Model Provenance (Gate 2)

JengaCoder v1.2 was produced by QLoRA fine-tuning of `Qwen/Qwen2.5-Coder-1.5B-Instruct`.

- Base-model source: `huggingface:Qwen/Qwen2.5-Coder-1.5B-Instruct`
- Recorded base-model revision: `2e1fd397ee46e1388853d2af2c993145b0f1098a`
- Base weight SHA256: `c1b9b30e907950516ba3c646bdf570d8084c25a6410a0cdca80cf04b11bc13a8`
- Fine-tuning method: QLoRA supervised fine-tuning, 2 epochs and 40 optimizer steps
- Training dataset: 160 records, SHA256 `b40facb331160fab145a0b0b88f1a953ec21ffd2d629059f6bfd15bec56f194f`
- Validation dataset: 20 records, SHA256 `a81ec8ae4c4fdc90ced02c6ad3ad0ed5aecd4c774cb5194707ad68345ad610df`
- Dataset license: GNU GPL v3.0, as provided by the repository `LICENSE`
- Training script SHA256: `5843a0bed5a18687f6e5a93ba07a81bd60e5a0e9528772cdec1a9baf261c9dc1`
- Recovered adapter SHA256: `34455431fea5a115d30d943f901153f86311a86bd60f2881e89d69d7772f9278`
- Recovered trainer-state SHA256: `5a44023a3bc3220ee6c62f1b2a4129724d91dc1c7d7797439d5b6ee287505432`
- Published-model revision: `acd5bc24661d3258176068478be483cd587839e3`
- Final GGUF SHA256: `e253182086f2bfd9e48ee3e4b683f151276fa1dfc6510faea8be0824dbe433bc`

The original adapter checkpoint, adapter configuration and final trainer state were recovered from the archived v1.2 training output. The trainer state records completion at epoch 2.0 and global step 40, with final evaluation loss `0.9508873224258423` and mean token accuracy `0.8057295680046082`.

The historical training script used the base repository's `main` revision without an explicit pin. Therefore, the revision above is the independently recorded upstream revision rather than a runtime-captured hash. The original interactive shell transcript and exact llama.cpp conversion commit were not retained. These limitations are disclosed rather than reconstructed.

#### Base-versus-fine-tuned diagnostic

A frozen 10-prompt ConstraintBench diagnostic produced:

| Evaluation | Qwen base | JengaCoder v1.2 |
| --- | ---: | ---: |
| Overall ConstraintBench score | 77/100 | 59/100 |
| Physical/electrical subset | 24/40 | 15/40 |

Two complete, unmodified before-and-after comparisons are preserved in `provenance/before_after_examples.md`:

- Experiment 001 documents a regression on an Arduino hardware-constraint prompt: the base model scored 4/10 and JengaCoder v1.2 scored 1/10 because the fine-tuned response invented prohibited hardware and used an incorrect distance formula.
- Experiment 009 documents an improvement on memory-disciplined streaming: the base model scored 8/10 and JengaCoder v1.2 scored 10/10 because the fine-tuned response processed the file incrementally without retaining all matching records.

This diagnostic does not support a claim of universal improvement from fine-tuning. It identified regressions in physical/electrical grounding and constraint consistency, while JengaCoder v1.2 was retained for its overall practical coding behavior and measured edge-inference performance. The repository contains the frozen prompts, rubrics, results and an in-progress v2 dataset redesign intended to address those weaknesses. The v2 data was not used to train the submitted v1.2 model.

Supporting evidence is under `provenance/`, `training/`, and `evaluation/`.


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
| Generation throughput | 18.34 tokens/s |
| Prompt benchmark length | 512 tokens |
| Generated benchmark length | 128 tokens |
| First-token latency | 7959.63 ms |
| Peak RSS memory | 1692.39 MB |
| Steady-state RSS | 1617.93 MB |
| Peak virtual memory | 2175.97 MB |
| ARC Easy accuracy | 0.70 |
| ARC Easy samples | 50 |
| Thermal throttling | None detected |
| CPU p99 utilization | 51.0% |

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

JengaCoder v1.2 combines a compact 1.54B model, Q4_K_M quantization and llama.cpp CPU inference to achieve 18.34 tokens per second while using approximately 1.69 GB peak resident memory during the official participant profiler run.

The project is intended to make practical AI-assisted learning and engineering more accessible in environments where connectivity, computing power and data cost are meaningful constraints.
