# Test Strategy — Thief

Testing is designed **before** implementation each stage (TDD where practical). Tests
validate behaviour and correctness — never weakened to pass, never mocking away the
central behaviour under test. Target: **≥85% meaningful coverage**, `ruff` zero
violations, plus a type checker.

## Tooling
`pytest`, `pytest-cov`, `ruff`, (type checker TBD: `mypy`/`pyright`). Runner: `uv run`.
Deterministic local mode + template LLM mode ensure the full unit suite is offline and
free.

## Test categories mapped to requirements
| Category | Stage | Requirements |
|---|---|---|
| Legal / illegal move | 1 | RQ-MOVE-01, RQ-CAP-* |
| Board boundary | 1 | RQ-BOARD-01 |
| Barrier reaction & capture-by-barrier detection | 1 | RQ-CAP-02, RQ-MOVE-03 |
| Win/termination & scoring (thief survival) | 1 | RQ-WIN-01, RQ-SCORE-01 |
| Config schema & CONSTANT/MIN/NEGOTIABLE validation | 1 | RQ-BOARD-03 |
| Malformed / incompatible-version message | 2/4 | RQ-LANG-02, interoperability |
| Timeout / retry / Watchdog | 2/6 | RQ-ARCH-06/07 |
| FSM legal/illegal transitions | 2 | RQ-ARCH-04/05 |
| Belief update (pursuer estimate) | 3/4 | RQ-BELIEF-01 |
| Deterministic strategy (evasion) | 3 | RQ-STRAT-01 |
| Scent emission & decay | 4 | RQ-SCENT-01 |
| Free-language dialogue round-trip | 4 | RQ-LANG-01 |
| LLM fallback / invalid LLM output | 4 | RQ-LLM-01/02 |
| Gatekeeper budget / rate limit | 4/7 | RQ-GATE-01, RQ-COST-01 |
| Commit-Reveal success / mismatch | 6 | RQ-CRYPT-01/03 |
| Invalid nonce | 6 | RQ-CRYPT-02 |
| Replay tampering / log integrity | 6/7 | RQ-AUDIT-01, RQ-REPLAY-01 |
| Step-0 hardware declaration | 6 | RQ-CRYPT-04 |
| Gmail payload build (no real send) | 7 | RQ-GMAIL-01 |
| Artifact schema (4 JSON) | 7 | RQ-ART-01 |
| Two-repo interoperability fixtures | 4/6 | interoperability |

## Marked, NOT auto-run tests
Tests needing paid APIs, external LLMs, real Gmail sending, public tunnels, or a second
computer are marked (`network`, `llm`, `gmail`, `integration`) and **off by default**.
Manual instructions accompany each; see OPERATIONS.md.

## Honesty
A command is only reported as run if it actually ran. Coverage numbers require the
generated report as evidence. Unverifiable items are labelled **NOT VERIFIED**.
