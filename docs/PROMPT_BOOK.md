# Prompt Book — Thief

Record of major AI-assisted sessions. **Never** record passwords, API keys, OAuth/refresh
tokens, `credentials.json`/`token.json` contents, private personal data, or tunnel tokens.

---

## Session 2026-07-13 — Stage 0 setup & planning
- **Date:** 2026-07-13
- **Team member:** Renat (with Alon)
- **Model:** Cursor agent (Opus 4.8)
- **Purpose:** Verify repositories; create manual-Git rule; author planning &
  requirements documents; create safe Stage-0 skeletons (no game code).
- **Prompt summary:** Proceed with Stage 0 per the project charter — read-only Git
  verification, Cursor rules, planning/requirements docs, safe skeletons, checks, then
  stop for manual commits in both repos.
- **Files affected (thief):** `.cursor/rules/00-manual-git.mdc`, `.gitignore`,
  `.env.example`, `pyproject.toml`, `src/anrbj666_thief/__init__.py`, `.../py.typed`,
  `config/shared_config.schema.json`, `config/shared_config.example.json`,
  `config/private_config.example.toml`, `README.md`, and `docs/*` (PRD, PLAN, TODO,
  REQUIREMENTS_MATRIX, REQUIREMENTS_CONFLICTS, DEVELOPMENT_STAGES, ARCHITECTURE,
  SECURITY, TEST_STRATEGY, COST_ANALYSIS, INTEROPERABILITY, CONFIGURATION, OPERATIONS,
  DECISIONS, RISK_REGISTER, PROMPT_BOOK).
- **Important decisions:** D-001..D-006 (see DECISIONS.md). Extracted the seven official
  stages from Ch. 10.3 and Appendix F Tables 13–22 (authoritative numeric values).
- **Tests performed:** none yet (no production code in Stage 0). Ruff/pytest to run at
  Stage 1.
- **Manual verification performed:** read-only `git status/branch/remote/ls-files` on
  both repos (clean, `main`, correct remotes, zero commits).
- **Known limitations:** planning only; no game logic; C-002 open.
- **Estimated/measured AI cost:** not measured this session.
- **Related stage / commit:** Stage 0 — commit hash to be filled after manual commit.

---

## Session 2026-07-13 — Stage 1 base logic
- **Date:** 2026-07-13
- **Team member:** Renat (with Alon)
- **Model:** Cursor agent (Opus 4.8)
- **Purpose:** Implement Stage 1 base logic (config validation + single-process
  game: geometry, board, movement rules, capture, scoring, engine) via TDD.
- **Prompt summary:** Resolve C-002 (treat `max_steps`/`survival_threshold` as
  independent, default-equal 35, uncoupled in code; document in
  REQUIREMENTS_CONFLICTS.md + DECISIONS.md). Proceed with Stage 1 following
  planning → tests → smallest implementation → complete checks → manual commit;
  no Git writes by Cursor.
- **Files affected (thief):** `src/anrbj666_thief/__init__.py`,
  `config/{__init__,model,loader}.py`, `game/{__init__,geometry,board,rules,capture,scoring,engine}.py`,
  `tests/{conftest,test_config,test_geometry,test_board,test_rules,test_capture,test_scoring,test_engine}.py`,
  `.gitignore` (re-saved UTF-8/ASCII), `docs/{REQUIREMENTS_CONFLICTS,DECISIONS,TODO,PROMPT_BOOK,REQUIREMENTS_MATRIX}.md`.
- **Important decisions:** D-007 (independent max_steps/survival_threshold);
  C-005 (Rule 47 "trapped" = no adjacent step available). Base game logic is kept
  byte-consistent with the police repo per INTEROPERABILITY.md (shared public rules).
- **Tests performed:** `uv run pytest --cov` → 71 passed, 100% coverage;
  `uv run ruff check .` → all checks passed (Python 3.14.3, uv 0.11.28).
- **Manual verification performed:** none required (Cursor performed no Git ops).
- **Known limitations:** single process only; no networking, strategy, scent,
  language, or cryptography yet. The thief models barriers to detect capture but
  never places them.
- **Estimated/measured AI cost:** not separately metered.
- **Related stage / commit:** Stage 1 — commit `9569ba2`.

---

## Session 2026-07-13 — Stage 2 basic FastMCP infrastructure
- **Date:** 2026-07-13
- **Team member:** Renat (with Alon)
- **Model:** Cursor agent (Opus 4.8)
- **Purpose:** Stand up the mandatory FastMCP P2P transport: geometric message
  contract, server tools, client helpers, runnable localhost entrypoint (TDD).
- **Prompt summary:** After `COMMIT DONE: STAGE 1 BOTH`, proceed with Stage 2
  following planning -> tests -> smallest implementation -> checks -> manual
  commit; no Git writes by Cursor.
- **Files affected (thief):** `pyproject.toml` (fastmcp + pytest-asyncio, async
  mode, marker deselection, coverage omit), `src/anrbj666_thief/mcp/{__init__,messages,inbox,server,client,__main__}.py`,
  `tests/{test_messages,test_mcp}.py`, `docs/{DECISIONS,OPERATIONS,TODO,PROMPT_BOOK,REQUIREMENTS_MATRIX}.md`, `uv.lock`.
- **Important decisions:** D-008 (FastMCP v3.x; in-memory `Client(server)` tests;
  numeric channel is a Stage-2 scaffold to be wrapped by free language in Stage 4).
  MCP transport code kept byte-consistent with the police repo (symmetric peer).
- **Tests performed:** `uv run pytest --cov` -> 90 passed, 100% coverage;
  `uv run ruff check .` -> clean (fastmcp 3.4.4, Python 3.14.3).
- **Manual verification performed:** none by Cursor; live localhost two-terminal
  run documented in OPERATIONS.md for the team (marked `network`).
- **Known limitations:** no orchestrator/state-machine turn loop yet; no deadline/
  watchdog; numeric messages only; single tool set. Strategy is Stage 3.
- **Estimated/measured AI cost:** not separately metered.
- **Related stage / commit:** Stage 2 — commit `6dabf22`.

---

## Session 2026-07-13 — Stage 3 "blind" strategy module
- **Date:** 2026-07-13
- **Team member:** Renat (with Alon)
- **Model:** Cursor agent (Opus 4.8)
- **Purpose:** First decision core (book §10.3.3): deterministic BFS shortest legal
  path to a **known** target cell, executed one step per turn. No scent, language,
  deception, or LLM yet.
- **Prompt summary:** After `COMMIT DONE: STAGE 2 BOTH`, proceed with Stage 3
  following planning -> tests -> smallest implementation -> checks -> manual
  commit + push; no Git writes by Cursor.
- **Files affected (thief):** `src/anrbj666_thief/strategy/{__init__,action,base,pathfinding,heuristic,runner}.py`,
  `tests/{test_pathfinding,test_strategy}.py`, `docs/{DECISIONS,TODO,PROMPT_BOOK,REQUIREMENTS_MATRIX}.md`.
- **Important decisions:** D-009 (pluggable brains Appendix F T22; BFS shortest path;
  "known target" now, belief in Stage 4; thief evasion fallback; LLM never decides
  moves, Rule 25).
- **Tests performed:** `uv run pytest --cov` -> 104 passed, 100% coverage;
  `uv run ruff check .` -> clean. Milestone verified: thief computes & executes the
  shortest legal path to a known escape cell (Manhattan = number of steps).
- **Manual verification performed:** none by Cursor.
- **Known limitations:** target/police cell is ground truth (Stage 4 replaces with
  belief); no networking in the runner (single-process engine).
- **Estimated/measured AI cost:** not separately metered.
- **Related stage / commit:** Stage 3 — commit hash to be filled after manual commit.
