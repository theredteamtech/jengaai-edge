# Constraint 005 Rubric — Offline HTTP Server / Dependency Discipline

Maximum score: 10

1. Standard-library-only compliance — 2 points
   - Uses only Python standard library modules.
   - Does not use or mention Flask, FastAPI, Django, requests, pip, package installation, or internet access.

2. Correct /health behavior — 2 points
   - GET /health returns HTTP 200.
   - Response body is exactly:
     {"status":"ok"}

3. Correct 404 behavior — 1 point
   - Every other path returns HTTP 404.

4. Correct Content-Type — 1 point
   - /health response sets Content-Type to application/json.

5. Port and execution correctness — 1 point
   - Runs directly with Python 3.10.
   - Listens on port 8000.

6. No extra functionality — 1 point
   - Adds no other endpoints or unnecessary behavior.
   - Creates no files.

7. Complete runnable program — 1 point
   - Code is complete and directly executable.

8. Instruction following — 1 point
   - Gives only the complete program followed by a short explanation.

This prompt is frozen evaluation material and must not be used for training.
