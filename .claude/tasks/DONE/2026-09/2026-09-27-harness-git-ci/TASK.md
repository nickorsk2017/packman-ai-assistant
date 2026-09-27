# TASK — 2026-09-27-harness-git-ci
owner: Engineer
immutable: true

## Context
Follow-up to 2026-09-27-fix-harness-docs. The harness is not tracked by git, the pre-commit
gate is not installed, and no server-side gate exists. Remote: GitHub
(nickorsk2017/packman-ai-assistant).

## Requirements
- R1: Harness files (`.claude/` and root `CLAUDE.md`) are tracked by git (staged, not committed).
  Per-developer runtime state is excluded from tracking.
- R2: Local pre-commit gate is installed (`core.hooksPath = .claude/githooks`).
- R3: A GitHub Actions workflow `.github/workflows/harness-gate.yml` runs on push and pull_request:
  harness invariants via `.claude/scripts/ci_check.py`, plus the existing project checks
  (frontend lint + build, device-service build).
- R4: `CLAUDE.md` and `.claude/CLAUDE.md` describe the new state (workflow exists, hook
  installation, what is tracked), replacing the "not configured" statements.

## Acceptance
- A1: `git status` lists harness files as staged; runtime state files are not staged.
- A2: `git config core.hooksPath` prints `.claude/githooks`; the hook is executable.
- A3: Workflow YAML is valid and references only paths, lockfiles and scripts that exist.
- A4: Docs mention no check that does not exist; English only.

## Constraints
- No commit, no push (Engineer commits after review).
- No changes to application code, runner.py, hooks, ci_check.py, SETTINGS.md, skills.
