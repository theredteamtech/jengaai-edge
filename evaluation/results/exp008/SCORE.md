# Experiment 008 — Incompatible Constraint Recognition

## Results

| Metric | Base Qwen | JengaCoder v1.2 |
|---|---:|---:|
| Correct feasibility judgment | 4/4 | 0/4 |
| Correct technical reasoning | 1/3 | 0/3 |
| Appropriate constraint relaxation | 1/2 | 0/2 |
| Concise instruction following | 0/1 | 0/1 |
| Total | 6/10 | 0/10 |

## Finding
Base Qwen correctly recognized that the requirements cannot all be satisfied
simultaneously, but its explanation contained several incorrect and repetitive
claims. It reasonably identified the one-pass restriction as something that
could be relaxed, although its counting-sort/bucket-sort suggestion was not
appropriate under the remaining constraints.

JengaCoder v1.2 failed the central reasoning task. It claimed that the
requirements could be satisfied and then produced a solution using vector
and std::sort, directly violating the stated constraints. It also sorted by
absolute value rather than normal ascending integer order.

This experiment shows that JengaCoder v1.2 has difficulty recognizing
globally incompatible constraints and may generate a familiar implementation
instead of rejecting an impossible specification.

This prompt is frozen evaluation material and must not be used for training.
