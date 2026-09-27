# PLAN — 2026-09-27-harness-git-ci

## v1
impact: [.gitignore, .github/workflows/harness-gate.yml (new), CLAUDE.md, .claude/CLAUDE.md, .git/config, git index]
decisions:
- D1 `.claude/tasks/ACTIVE` is per-developer runtime state -> add to `.gitignore`; keep
  `CURRENT/.gitkeep` and task dirs tracked (audit trail). `.DS_Store` already ignored.
- D2 Workflow = 4 independent jobs so one red job does not hide others:
  `harness` (python3 ci_check.py, no deps), `frontend` (pnpm install --frozen-lockfile, lint, build),
  `device-service` (pnpm install --frozen-lockfile, build), no ai-service job (no lint/test
  target exists in Makefile; out of R3 scope).
- D3 Toolchain: pnpm 10 (lockfileVersion 9.0 + `allowBuilds` in pnpm-workspace.yaml), Node 22,
  per-job `working-directory` matching Makefile dirs; call `make lint` / `make build-*` targets
  so CI and local stay identical.
- D4 Only `harness` is documented as the required gate; project jobs are reported but their
  current pass/fail is unknown (local lint/tsc could not run in the agent sandbox).
risks:
- K1 frontend/device jobs may be red on first push due to existing code -> visible, not blocking
  harness; Engineer decides whether to mark them required in branch protection.
- K2 Branch protection (making the gate unbypassable) is a GitHub setting, not a repo file ->
  documented as a manual Engineer step.

- P1 (R1, D1) `.gitignore`: add `.claude/tasks/ACTIVE`.
- P2 (R2) Run `.claude/runner.py install-hooks`; verify hooksPath and exec bit.
- P3 (R3, D2, D3) Create `.github/workflows/harness-gate.yml`.
- P4 (R4, D4, K2) Update `.claude/CLAUDE.md` Commit Gate section and root `CLAUDE.md` No-exceptions
  bullet: workflow exists, required gate = `harness` job, branch protection is a manual step.
- P5 (R1) `git add` .gitignore, .github/, .claude/, CLAUDE.md; no commit.
- P6 (A1-A4) Verify: YAML parses, referenced paths exist, staged list excludes ACTIVE, grep docs.
