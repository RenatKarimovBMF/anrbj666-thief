# Requirements Matrix — Thief

Maps every mandatory requirement to responsibility, module, config, tests, evidence,
and status. A requirement is **complete only when implementation + tests + evidence
exist** — not when a file merely exists.

Sources: `police_thief_p2p.pdf` v3.0.0 (chapters + Appendix E Rules 1–55 + Appendix F
Tables 13–22), course-site text, software guidelines V3.
Priority column: F=Appendix F, R=book rule, C=course-site, G=guidelines.

Status legend: NOT-STARTED · IN-PROGRESS · IMPLEMENTED · TESTED · EVIDENCED · DONE.
Stage column = the official stage where the item is delivered.

## Legend for responsibility
- **P** = police repo owns runtime; **T** = thief repo owns runtime; **P/T** = both (duplicated public contract).

| ID | Requirement (summary) | Mand? | Src | Pri | Stage | Police resp | Thief resp | Module (planned) | Config field | Unit | Integ | Manual | Evidence | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| RQ-ARCH-01 | Police & thief run as fully separate processes; Zero-Trust | Yes | E-R1 | R | 2 | P | T | `mcp/server` | — | ✓ | ✓ | ✓ | two PIDs, logs | NOT-STARTED |
| RQ-ARCH-02 | No shared memory/state between sides | Yes | E-R2 | R | all | P | T | — | — | ✓ | ✓ | – | audit | NOT-STARTED |
| RQ-ARCH-03 | Single orchestrator entry point per sub-system | Yes | E-R3 | R | 8→2 | P | T | `orchestrator` | — | ✓ | – | – | design | NOT-STARTED |
| RQ-ARCH-04 | Game state via a proper state machine | Yes | E-R4 | R | 2 | P | T | `orchestrator/fsm` | — | ✓ | ✓ | – | tests | NOT-STARTED |
| RQ-ARCH-05 | Report illegal state-machine transitions | Yes | E-R5 | R | 2 | P | T | `orchestrator/fsm` | — | ✓ | – | – | tests | NOT-STARTED |
| RQ-ARCH-06 | Deadline tracker prevents opponent-wait freeze | Yes | E-R6 | R | 2/6 | P | T | `reliability/deadline` | `network.response_timeout_s` | ✓ | ✓ | – | tests | NOT-STARTED |
| RQ-ARCH-07 | Watchdog monitors crashes; controlled data extraction | Yes | E-R7 | R | 2/6 | P | T | `reliability/watchdog` | `network.watchdog_timeout_s` | ✓ | ✓ | – | tests | NOT-STARTED |
| RQ-ARCH-08 | GUI shows LOCAL truth only | Yes | E-R8 | R | 7 | P | T | `gui` | — | – | – | ✓ | screenshot | NOT-STARTED |
| RQ-ARCH-09 | GUI never shows full board / objective full state | Yes | E-R9 | R | 7 | P | T | `gui` | — | – | – | ✓ | screenshot | NOT-STARTED |
| RQ-NET-10 | Public exposure via tunnel (ngrok/localtonet) | Yes | E-R10 | R | 5 | P | T | `net/tunnel` | `.env` | – | – | ✓ | two-machine log | NOT-STARTED |
| RQ-BOARD-01 | Grid side = `board.size` (min 7) | Yes | F-T13#1 | F | 1 | P | T | `game/board`,`config/loader` | `board.size` | ✓ | – | – | tests | TESTED |
| RQ-BOARD-02 | Exactly 2 agents | Yes | F-T13#2 | F | 1 | P | T | `config/loader` | `board.num_agents` | ✓ | – | – | tests | TESTED |
| RQ-BOARD-03 | Config identical byte-for-byte both sides | Yes | E-R11 | R | 6 | P | T | `config/loader` | all shared | ✓ | ✓ | – | hash match | IN-PROGRESS |
| RQ-MOVE-01 | Orthogonal move + stay; no diagonals | Yes | F-T15#1 / E-R13,14 | F | 1 | P | T | `game/rules`,`game/geometry` | `movement.set` | ✓ | – | – | tests | TESTED |
| RQ-MOVE-02 | Barrier quota ≤ `barrier_quota` (police-only action) | Yes | F-T15#2 | F | 1 | **P** | – (validate only) | `game/rules`,`game/engine` | `movement.barrier_quota` | ✓ | – | – | tests | TESTED |
| RQ-MOVE-03 | Barrier placement declared openly; thief validates & reacts | Yes | E-R15,16 | R | 1/6 | **P** | T (verify) | `game/engine` | — | ✓ | ✓ | – | tests | IN-PROGRESS |
| RQ-CAP-01 | Capture on coordinate overlap (police wins) | Yes | E-R48 | R | 1 | P | T | `game/capture` | — | ✓ | – | – | tests | TESTED |
| RQ-CAP-02 | Barrier on thief's cell = capture (thief detects) | Yes | E-R46 | R | 1 | P | **T** | `game/capture` | — | ✓ | – | – | tests | TESTED |
| RQ-CAP-03 | Thief with no legal move = captured | Yes | E-R47 | R | 1 | P | **T** | `game/capture` | — | ✓ | – | – | tests (C-005) | TESTED |
| RQ-WIN-01 | Max steps / survival threshold (min 35) — thief survival win | Yes | F-T15#3,4 | F | 1 | P | **T** | `game/scoring` | `movement.max_steps`,`survival_threshold` | ✓ | – | – | tests (C-002/D-007) | TESTED |
| RQ-SCORE-01 | Scoring 20/5/5/10, tie 2 | Yes | F-T17, E-R48 | F | 1/7 | P | T | `game/scoring` | `scoring.*` | ✓ | – | – | tests | TESTED |
| RQ-SCENT-01 | Pheromone emit 0.9, decay 0.10, 5×5, crypto-locked (thief emits) | Yes | F-T16, E-R23 | F | 4/6 | P | **T** | `scent` | `scent.*` | ✓ | ✓ | – | tests | NOT-STARTED |
| RQ-BELIEF-01 | Local belief state / Bayesian heatmap of pursuer | Yes | Ch.6 | R | 3/4 | P | **T** | `strategy/belief` | — | ✓ | – | – | tests | NOT-STARTED |
| RQ-STRAT-01 | Pluggable strategy module (`ThiefBrain._pick_move`) | Yes | F-T22 | F | 3 | – | **T** | `strategy` | `[strategy].thief_class` | ✓ | – | – | tests | NOT-STARTED |
| RQ-LANG-01 | Free-language dialogue between agents | Yes | E-R26, C | R/C | 4 | P | T | `protocol/lang` | `verbal.hint_word_limit` | ✓ | ✓ | – | transcript | NOT-STARTED |
| RQ-LANG-02 | No direct numeric-position protocol | Yes | E-R27 | R | 4 | P | T | `protocol` | — | ✓ | ✓ | – | tests | NOT-STARTED |
| RQ-LLM-01 | LLM never decides moves (text/deception only) | Yes | E-R25, F-T21 | R/F | 4 | P | T | `llm/gatekeeper` | `[trash_talk].provider` | ✓ | – | – | tests | NOT-STARTED |
| RQ-LLM-02 | Template mode = zero tokens, default, offline | Yes | F-T21, C | F/C | 3/4 | P | T | `llm/template` | `provider=template` | ✓ | – | – | tests | NOT-STARTED |
| RQ-CRYPT-01 | Commit-Reveal over SHA-256 | Yes | E-R17, Ch.5 | R | 6 | P | T | `crypto/commit_reveal` | — | ✓ | ✓ | – | tests | NOT-STARTED |
| RQ-CRYPT-02 | Fresh secret nonce kept private until reveal | Yes | E-R18 | R | 6 | P | T | `crypto/nonce` | — | ✓ | – | – | tests | NOT-STARTED |
| RQ-CRYPT-03 | Technical loss on any hash mismatch | Yes | E-R19 | R | 6 | P | T | `crypto/verify` | — | ✓ | ✓ | – | tests | NOT-STARTED |
| RQ-CRYPT-04 | Step-0 hardware declaration before game | Yes | E-R24, Ch.5 | R | 6 | P | T | `crypto/step0` | — | ✓ | – | – | tests | NOT-STARTED |
| RQ-AUDIT-01 | Mutual audit + log integrity each game | Yes | E-R36, Ch.5 | R | 6 | P | T | `audit` | — | ✓ | ✓ | – | signed log | NOT-STARTED |
| RQ-REPLAY-01 | Replay viewer verifies recorded log → Verified OK | Yes | E-R20, Ch.7 | R | 7 | P | T | `replay` | — | ✓ | ✓ | ✓ | screenshot | NOT-STARTED |
| RQ-CLAIM-01 | Never falsely deny/claim capture; false claim = 0 | Yes | E-R21,22 | R | 1/6 | P | T | `board/rules` | — | ✓ | – | – | tests | NOT-STARTED |
| RQ-GATE-01 | Central API Gatekeeper: rate/parallel/retry/queue | Yes | F-T19, E-R28,29 | F/R | 4/7 | P | T | `llm/gatekeeper` | `network.*` | ✓ | ✓ | – | tests | NOT-STARTED |
| RQ-GMAIL-01 | Signed JSON results emailed via Gmail API | Yes | E-R32,33,34, Ch.9 | R | 7 | P | T | `report/gmail` | `.env` | ✓ | – | ✓ | sent evidence | NOT-STARTED |
| RQ-GMAIL-02 | OAuth 2.0 send-only scope; secrets git-ignored | Yes | E-R30,40, App.A | R | 7 | P | T | `report/oauth` | `.env` | – | – | ✓ | docs | NOT-STARTED |
| RQ-ART-01 | 4 signed JSON artifacts (declaration/config/log/result) | Yes | F-T20, C | F/C | 7 | P | T | `report/artifacts` | — | ✓ | ✓ | – | files | NOT-STARTED |
| RQ-LEAGUE-01 | ≥2 games vs distinct groups; ≤10; count declared truthfully | Yes | F-T18, E-R31,37,38,52 | F/R | 7 | P | T | `report` | `league.*` | – | – | ✓ | result JSON | NOT-STARTED |
| RQ-SUB-01 | Two repos, README cross-links, 2 submission links, 4 JSON links | Yes | E-R49,50, Ch.9 | R | 0/final | P | T | repo | — | – | – | ✓ | README | IN-PROGRESS |
| RQ-SUB-02 | Repo has README, config/, PRD, PLAN, TODO | Yes | E-R50 | R | 0 | P | T | repo | — | – | – | ✓ | files | IN-PROGRESS |
| RQ-SUB-03 | Unique 8-char group code (anrbj666) | Yes | E-R45, C | R/C | 0 | P | T | repo | — | – | – | ✓ | naming | DONE |
| RQ-SUB-04 | Annotated Git tag for submission version (manual) | Yes | E-R41 | R | final | P | T | repo | — | – | – | ✓ | tag | NOT-STARTED |
| RQ-QUAL-01 | uv + pyproject + uv.lock; Python ≥3.10 | Yes | G | G | 0+ | P | T | repo | — | – | – | ✓ | files | IN-PROGRESS |
| RQ-QUAL-02 | Ruff zero violations | Yes | G | G | all | P | T | repo | — | – | – | ✓ | ruff log | IN-PROGRESS |
| RQ-QUAL-03 | ≥85% meaningful coverage | Yes | G | G | all | P | T | repo | — | ✓ | ✓ | – | cov report (S1: 100%) | IN-PROGRESS |
| RQ-QUAL-04 | ~≤150 lines/source file unless justified | Yes | G | G | all | P | T | repo | — | – | – | ✓ | review | IN-PROGRESS |
| RQ-QUAL-05 | No secrets in source; .gitignore covers them | Yes | E-R39,40, G | R/G | 0+ | P | T | repo | — | – | – | ✓ | scan | IN-PROGRESS |
| RQ-DOC-01 | Academic README (model, dilemmas, strategy, screenshots) | Yes | E-R42, Ch.9 | R | final | P | T | repo | — | – | – | ✓ | README | NOT-STARTED |
| RQ-DOC-02 | Per-student Moodle PDF (unmodified template) | Yes | E-R43,44, C | R/C | final | P | T | — | — | – | – | ✓ | PDF | NOT-STARTED |
| RQ-COST-01 | Token & cost tracking; report per series | Yes | F-T18#4, E-R54 | F/R | 4/7 | P | T | `llm/gatekeeper` | — | ✓ | – | – | result JSON | NOT-STARTED |

> This matrix is updated at the start and end of every stage. No row moves to
> DONE without linked tests and evidence.
