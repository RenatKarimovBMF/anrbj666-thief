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

## D-008 — 2026-07-13 — Stage 2 transport: FastMCP; in-memory tests; numeric channel is a scaffold
Adopt the mandatory `fastmcp` library (v3.x) for the P2P Model Context Protocol.
Each peer exposes a FastMCP server (`mcp/server.py`) with geometric tools
(`ping`, `submit_geometric`) and acts as a client (`mcp/client.py`); a runnable
localhost entrypoint lives in `mcp/__main__.py`. **Testing:** use FastMCP's
in-memory `Client(server)` transport — a real MCP round-trip without sockets — as
the deterministic default; real-network tests are marked `network` and excluded
from the default suite (`addopts = -m 'not network and not llm and not gmail'`).
**Numeric coordinates are a Stage-2 transport scaffold only**; Stage 4 replaces/
wraps them with free-language dialogue so the final system never uses a direct
numeric-position protocol (Rule 27). **Rationale:** book Ch. 2 mandates FastMCP;
in-memory testing keeps the suite offline/fast; staged plan (§10.3.2) explicitly
starts with numeric messages. **Status:** adopted.

## D-009 — 2026-07-13 — Stage 3 blind strategy: BFS shortest path to a *known* target
Add a pluggable, deterministic decision core (`strategy/`, Appendix F T22): `PoliceBrain`/
`ThiefBrain` bases with `decide()`; `HeuristicPolice._decide_move` / `HeuristicThief._pick_move`.
Movement is `orthogonal4_plus_stay`, so an unweighted BFS over free cells (`strategy/pathfinding.py`)
yields a **shortest legal path**; `next_step_toward` executes one step per turn. Barriers and
`blocked` cells are impassable; neighbour expansion order is fixed so paths are deterministic.
**"Blind" = the target cell is handed to the brain**: Stage 3 reads the opponent's actual cell as
the target; **Stage 4 replaces it with a belief estimate from scent/dialogue**, so the final
system uses no ground-truth opponent position. **Barrier placement is not exercised by the blind
police core** (`Action.barrier_at=None`); it is added with the belief model. The thief navigates to
a known escape cell and falls back to the legal step maximising Manhattan distance from the police
when the target is unreachable. **The LLM never decides moves (Rule 25).** A single-process
`play_with_strategies` runner drives both brains through the Stage 1 engine (no networking yet).
**Rationale:** book §10.3.3 "first decision core"; BFS is exact/cheap on a small grid; separating
"known target" (Stage 3) from "belief" (Stage 4) keeps the incremental plan clean. **Status:** adopted.

## Pending decisions
- **PD-001 (C-002):** RESOLVED for implementation by D-007 (independent, default-equal).
  Remains open only for optional lecturer/opponent clarification of intended equality;
  no code change would result (config-only). Directly affects the thief's survival-win condition.
- **PD-002:** type checker choice (`mypy` vs `pyright`). Default `mypy` unless changed.
