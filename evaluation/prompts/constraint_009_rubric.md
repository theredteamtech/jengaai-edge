# Constraint 009 Rubric — Streaming File Processing / Memory Discipline

Maximum score: 10

1. Streaming input — 2 points
   - Reads temperatures.txt line by line.
   - Does not load the whole file into memory.
   - Does not use read(), readlines(), list(), or comprehensions.

2. Correct filtering — 2 points
   - Prints only integer temperatures >= 30.
   - Preserves original order.

3. Invalid-line handling — 1 point
   - Ignores blank lines.
   - Skips non-blank lines that are not valid integers without terminating.

4. Missing-file handling — 1 point
   - Prints exactly:
     FILE NOT FOUND

5. Memory discipline — 1 point
   - Uses O(1) additional memory apart from normal per-line buffering.
   - Does not store matching temperatures for later printing.

6. Dependency compliance — 1 point
   - Uses only the Python standard library.
   - Does not use pandas, numpy, or third-party packages.

7. No extra file creation — 1 point
   - Does not create or write another file.

8. Complete runnable program and instruction following — 1 point
   - Complete Python 3.10 program.
   - Gives only the program followed by a short explanation.

This prompt is frozen evaluation material and must not be used for training.
