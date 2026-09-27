# EXEC — 2026-09-27-fix-harness-docs

## v1
changed: [CLAUDE.md, .claude/CLAUDE.md]
- P1 root header/intro -> packman layout (3 services, Qdrant, Makefile targets).
- P2 root "Subsystem rules" -> no subsystem files exist; precedence line kept. Dropped the
  "pinned to latest stable" line (inside rewritten section; false for ai-service pins).
- P3 root "No exceptions" bullet -> references only `ci_check.py`; root Boot step 2 path fixed.
- P4 `.claude/CLAUDE.md` Commit Gate -> no CI workflow, no test suites; gates = pre-commit
  (after install-hooks) + manual ci_check.py; code checks = `make lint`, `make build`.
- P5 all task/runner/skills paths prefixed `.claude/`; "hot set CI scans" -> `ci_check.py`.
- P6 matrix note -> hook scope (local Claude Code only) + self-enforcement duty.
- P7 checks: forbidden-term grep = 0 hits; Cyrillic grep = 0 hits; 14 named paths exist;
  7 named make targets exist. `make lint/build` not run (docs-only change).
