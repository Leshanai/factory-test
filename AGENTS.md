# factory-test

A small Python project. `palindrome.py` defines `is_palindrome(value)` for strings and ints; tests are in `test_palindrome.py`.

## Setup

No dependencies. Python 3.10+ is needed for `factory/bin/*` and the code.

## Dev server

None yet.

## Validation

`bash factory/checks.sh` (currently placeholder checks: config JSON validity).
Tests: `python3 -m unittest -v` (not run by `checks.sh`, which is protected).

## Software factory

`/factory run` builds every open GitHub issue labeled `factory` through
intake → spec → build → gate → review → approve, one PR per issue. State is in
`factory/jobs/` (gitignored); `factory/bin/job` is its only writer. Checks:
`factory/checks.sh`. Dashboard: `cd factory && python3 -m http.server`, then
open http://localhost:8000/dashboard.html.

Each job works in its own git worktree, a full checkout of the repo at
`.worktrees/<job-id>` (gitignored). A tool run from the repo root that doesn't
read `.gitignore` sees those copies too; exclude `.worktrees/` in its config.
