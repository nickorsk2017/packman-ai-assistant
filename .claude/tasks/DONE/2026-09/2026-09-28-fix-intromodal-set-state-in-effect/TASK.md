# TASK — 2026-09-28-fix-intromodal-set-state-in-effect
owner: Engineer
immutable: true

## Requirements
- R1: Fix CI lint error `react-hooks/set-state-in-effect` in `frontend/main-app/src/features/home/IntroModal.tsx:14` (setOpen called synchronously inside useEffect).

## Acceptance
- A1: `make lint` passes with 0 errors.
- A2: Behavior unchanged: modal shows on first visit when `packman_intro_seen` is absent in localStorage; "Got it" persists the flag and closes; "Close" closes without persisting.
- A3: No SSR hydration mismatch (server and first client render both output nothing).

## Constraints
- Single file change, no new dependencies, no eslint rule suppression.
