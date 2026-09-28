# EXEC — 2026-09-28-fix-intromodal-set-state-in-effect

## v1
- R1: replaced useEffect+setOpen with useSyncExternalStore (localStorage flag, `storage` event subscription, server snapshot = seen) plus local `dismissed` state for close.
- A3: getServerSnapshot returns true, so server and hydration render output null; client re-renders from localStorage after hydration.
- Changed files: frontend/main-app/src/features/home/IntroModal.tsx
- Checks: `eslint` (frontend/main-app) exit 0; `tsc --noEmit` exit 0. `make lint` not run locally (pnpm absent in sandbox); same eslint binary and config.
