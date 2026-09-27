# VALIDATION — 2026-09-27-fix-harness-docs

## v1
result: PASS
- A1 PASS: grep for agent-chat/gateway/mcp/sub-agent/pytest/jest/dev-install/harness-gate/.github = 0 hits in both files.
- A2 PASS: all named paths (14) and make targets (7) exist.
- A3 PASS: `.claude/CLAUDE.md` Prime Directive, Roles, Complexity, Routing, Failure Routing,
  Loop Control, Write Discipline, Crash Recovery byte-identical; root Reasoning + Language
  identical; root Prime Directive / No exceptions changed only per P3 (path, CI reference).
- A4 PASS: 0 Cyrillic characters in both files.
- Constraints PASS: only CLAUDE.md and .claude/CLAUDE.md changed; ci_check.py clean.
issues: []
