# PLAN — 2026-09-27-fix-harness-docs

## v1
impact: [CLAUDE.md, .claude/CLAUDE.md]
risk: losing harness rules while rewriting (A3) -> edit only the listed sections, keep all others byte-identical.

- P1 (R1, A1, A2) Root `CLAUDE.md` header + intro: replace agent-chat description with packman
  layout (frontend/main-app Next.js; backend/ai-service FastAPI/uv/Qdrant; backend/device-service
  Node/pnpm/TypeORM; Qdrant via docker compose; root Makefile targets as entry point).
- P2 (R2, A1) Root `CLAUDE.md` "Subsystem rules": drop the three missing files; state that no
  subsystem `CLAUDE.md` exists yet and service rules live in this file. Keep precedence line,
  adjusted to `.claude/` harness > root file.
- P3 (R3, A1) Root `CLAUDE.md` "No exceptions": reword the bullet that names `harness-gate.yml`
  so it refers only to existing gates (pre-commit, ci_check.py).
- P4 (R3, A1, A2) `.claude/CLAUDE.md` "Commit Gate & Task Closure": remove claims about
  harness-gate.yml, pytest/jest, dev-install targets; state server-side gate is not configured,
  local pre-commit + ci_check.py are the gates, project checks are `make lint` / `make build`.
- P5 (R4, A2) `.claude/CLAUDE.md` Boot Sequence, Runner, Task Layout, Crash Recovery: prefix task
  paths with `.claude/`; runner invoked as `.claude/runner.py`; skills path `.claude/skills/`.
- P6 (R5) `.claude/CLAUDE.md` Read/Write Matrix note: add scope of enforce_matrix.py (local
  Claude Code only) and self-enforcement duty elsewhere.
- P7 (A1-A4) Self-check: grep both files for forbidden terms and non-ASCII-Cyrillic; verify every
  named path/target exists.
