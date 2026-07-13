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

## D-007 — 2026-07-13 — `max_steps` and `survival_threshold` are independent (default-equal)
Per user instruction (resolving C-002): `movement.max_steps` and
`movement.survival_threshold` are treated as **independent, individually configurable
and individually validated** parameters. Appendix F defaults are `35` for each
(default-equal). **They must not be coupled in code** — neither field is derived from
or asserted equal to the other; each is validated against its own MINIMUM (≥35). The
termination engine evaluates survival win (at `survival_threshold`) and the step
ceiling (`max_steps`) as separate conditions. **Rationale:** Appendix F lists them as
two distinct MINIMUM entries; independence keeps the engine correct if a match
negotiates unequal values. **Status:** adopted; requirement kept open (see C-002) for
lecturer/match-level clarification (would affect only negotiated config, never code).

## Pending decisions
- **PD-001 (C-002):** RESOLVED for implementation by D-007 (independent, default-equal).
  Remains open only for optional lecturer/opponent clarification of intended equality;
  no code change would result (config-only). Directly affects the thief's survival-win condition.
- **PD-002:** type checker choice (`mypy` vs `pyright`). Default `mypy` unless changed.
