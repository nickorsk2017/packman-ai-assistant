# TASK — 2026-09-27-fix-harness-docs
owner: Engineer
immutable: true

## Context
Root `CLAUDE.md` and `.claude/CLAUDE.md` were copied from another project ("agent-chat")
and describe structure, CI and tests that do not exist in this repository (packman).

## Requirements
- R1: Root `CLAUDE.md` describes the actual packman repository: `frontend/main-app`,
  `backend/ai-service`, `backend/device-service`, Qdrant, and the root `Makefile` as the
  entry point. No references to agent-chat, gateway, MCP orchestrator or sub-agents.
- R2: Remove references to subsystem `CLAUDE.md` files and directories that do not exist
  (`backend/CLAUDE.md`, `frontend/CLAUDE.md`, `mcp/CLAUDE.md`, `mcp/`).
- R3: `.claude/CLAUDE.md` CI/test statements match reality: no `.github/workflows/harness-gate.yml`,
  no pytest/jest suites, no `make dev-install-*` targets. State the checks that exist
  (`.claude/scripts/ci_check.py`, local pre-commit hook, `make lint`, `make build`) and that a
  server-side gate is not configured.
- R4: Task paths in `.claude/CLAUDE.md` match the code: tasks live under `.claude/tasks/`.
- R5: `.claude/CLAUDE.md` states that `.claude/hooks/enforce_matrix.py` runs only in local
  Claude Code sessions; actors running elsewhere must self-enforce the Read/Write Matrix.

## Acceptance
- A1: No mention of agent-chat, gateway, MCP orchestrator, `mcp/`, pytest, jest,
  `dev-install`, or `harness-gate.yml` as an existing file in either `CLAUDE.md`.
- A2: Every path and `make` target named in both files exists in the repository.
- A3: Harness rules (Prime Directive, Boot Sequence, Routing, Matrix, Loop Control,
  Language rule, No-exceptions rule) are preserved in meaning.
- A4: Both files are English only.

## Constraints
- Documentation only: edit `CLAUDE.md` and `.claude/CLAUDE.md`. No changes to runner.py,
  hooks, scripts, SETTINGS.md, skills, Makefile, or git config.
- Creating a CI workflow or subsystem `CLAUDE.md` files is out of scope (separate task).
