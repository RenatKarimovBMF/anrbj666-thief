# Decision Log (ADRs) — Thief

Chronological, append-only. Format: ID · date · decision · rationale · status.
Kept consistent with the police repo's decision log.

## D-001 — 2026-07-13 — Two independent repos, no central runtime
Keep `anrbj666-police` and `anrbj666-thief` as fully separate repos with no shared
runtime code (only duplicated public contracts). **Rationale:** mandatory (Appendix E
Rules 1–2; Ch. 9.4). **Status:** adopted.

## D-002 — 2026-07-13 — Numeric values sourced only from Appendix F
All mandatory numbers come from Appendix F via central config; none hard-coded.
**Rationale:** book states Appendix F is the sole authoritative source. **Status:** adopted.

## D-003 — 2026-07-13 — Default LLM mode = template (offline, zero cost)
Ship with `provider=template`; paid modes opt-in and gated by the Gatekeeper.
**Rationale:** Appendix F T21 + course text require playable-without-LLM. **Status:** adopted.

## D-004 — 2026-07-13 — uv + hatchling + ruff + pytest, Python ≥3.10
**Rationale:** software submission guidelines V3. **Status:** adopted.

## D-005 — 2026-07-13 — Repository visibility: Public
Per user instruction; lecturer access satisfied by public repos. **Rationale:** user
decision (competitive-secrecy trade-off accepted). **Status:** adopted.

## D-006 — 2026-07-13 — `src/` layout + ≈≤150 lines/file
**Rationale:** guidelines (modularity, testability). **Status:** adopted.

## Pending decisions
- **PD-001 (C-002):** relationship between `max_steps` and `survival_threshold`
  (independent vs equal). Needs human/opponent confirmation before Stage 1 win logic.
  Directly affects the thief's survival-win condition.
- **PD-002:** type checker choice (`mypy` vs `pyright`). Default `mypy` unless changed.
