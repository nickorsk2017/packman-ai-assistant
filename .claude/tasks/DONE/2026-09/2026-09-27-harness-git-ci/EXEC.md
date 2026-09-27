# EXEC — 2026-09-27-harness-git-ci

## v1
changed: [.gitignore, .github/workflows/harness-gate.yml (new), CLAUDE.md, .claude/CLAUDE.md, .git/config]
- P1 `.gitignore`: added `.claude/tasks/ACTIVE`; fixed missing trailing newline that merged it into `.DS_Store` line.
- P2 `runner.py install-hooks` -> core.hooksPath=.claude/githooks; pre-commit staged as 100755.
- P3 workflow: jobs harness (python 3.13, ci_check.py), frontend (pnpm 10, node 22, frozen install,
  make lint, make build-frontend), device-service (same toolchain, make build-device). 3 jobs per D2.
- P4 `.claude/CLAUDE.md` Commit Gate: install-hooks after clone, workflow jobs, required = harness,
  branch protection manual, tracking rules. Root: setup step + workflow in No-exceptions bullet.
- P5 `git add .gitignore .github .claude CLAUDE.md`; no commit. Re-add of `.claude` required after
  `runner.py done` moves this task dir to DONE.
- P6 YAML parses (jobs: harness, frontend, device-service; on: push, pull_request); make targets
  lint/build-frontend/build-device exist; no "not configured" leftovers; 0 Cyrillic.
  Project lint/build not run locally (macOS node_modules not executable in agent sandbox, K1).
