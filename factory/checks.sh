#!/usr/bin/env bash
# The repo's checks. Exit 0 only when the branch is fit to review.
#
# The gate runs this script from the main checkout with the job's worktree as
# the working directory. Keep it fast, deterministic and non-interactive: no
# watch modes, no prompts, nothing that rewrites files.
#
# INSTALL.md replaces the line below with this project's real commands, e.g.:
#
#   npm ci --prefer-offline
#   npm run lint
#   npm run typecheck
#   npm test -- --run
#   npm run build
set -euo pipefail

# Placeholder checks: this project has no code yet. Replace with real
# lint/typecheck/test/build commands once it does.
python3 -m json.tool factory/config.json >/dev/null
bash -n factory/checks.sh
python3 -I -c 'import ast,sys; [ast.parse(open(f).read()) for f in sys.argv[1:]]' factory/bin/job factory/bin/gate factory/bin/route
echo "checks ok"
