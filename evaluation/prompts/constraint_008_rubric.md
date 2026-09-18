# Constraint 008 Rubric — Incompatible Constraint Recognition

Maximum score: 10

1. Correct feasibility judgment — 4 points
   - Clearly states that all listed constraints cannot be satisfied simultaneously for arbitrary input.
   - Does not invent a false solution.

2. Correct technical reasoning — 3 points
   - Explains that producing globally sorted output for arbitrary unseen future values generally requires either:
     - storing information,
     - modifying/revisiting the input,
     - or making multiple passes.
   - Recognizes that one pass + O(1) extra memory + immutable input + irreversible output is insufficient in the general case.

3. Appropriate constraint relaxation — 2 points
   - Identifies a reasonable minimal relaxation, such as allowing extra memory, allowing multiple passes, or allowing input modification.
   - Explains how that relaxation makes sorting feasible.

4. Concise instruction following — 1 point
   - Gives a concise technical explanation.
   - Does not provide code after determining the requirements are incompatible.

This prompt is frozen evaluation material and must not be used for training.
