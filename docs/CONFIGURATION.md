# Configuration

All mandatory numerical parameters come from **Appendix F** (`police_thief_p2p.pdf`
v3.0.0, Tables 13–19, pp. 135–139) and are validated at load time. **No mandatory
value is hard-coded in implementation modules** — they live in configuration and
are read through a single central config loader (built in Stage 1+).

## Configuration classes

| Class | Where it lives | Shared? | Secret? |
|---|---|---|---|
| Public shared match config | `config/shared_config.*.json` | Yes — byte-identical both peers, crypto-locked | No |
| Private per-peer config | `config/private_config.toml` (local) | No | No |
| Environment-specific | `.env` (local, git-ignored) | No | Partially |
| Secrets | `.env`, `credentials.json`, `token.json` | No | **Yes** |
| Test config | `tests/fixtures/` | No | No |

## Status semantics (Appendix F §1, p. 139)
- **CONSTANT** — may never change; deviation disqualifies the group.
- **MINIMUM** — may be negotiated **upward** only; never below the example; default = example value.
- **NEGOTIABLE** — any value both sides agree; default = example value.

## Public shared parameters (from Appendix F)

| # | Field (`shared_config`) | Meaning | Example | Status | Source |
|---|---|---|---|---|---|
| 1 | `board.size` | square grid side | 7 | MINIMUM | T13#1 |
| 2 | `board.num_agents` | players in the race | 2 | CONSTANT | T13#2 |
| 3 | `board.axis_origin` | origin corner of (0,0) | top-left | NEGOTIABLE | T13#3 |
| 4 | `board.axis_start_index` | first index of each axis | 0 | NEGOTIABLE | T13#4 |
| 5 | `board.thief_start` | thief start cell | [3,3] (center) | NEGOTIABLE | T13#5 |
| 6 | `board.police_start` | police start cell | [0,0] (corner) | NEGOTIABLE | T13#6 |
| 7 | `verbal.arena` | place-name seed for hints | "New York" | NEGOTIABLE | T14#1 |
| 8 | `verbal.hint_word_limit` | max words per verbal hint | 15 | NEGOTIABLE | T14#2 |
| 9 | `movement.set` | legal moves | orthogonal 4 + stay, no diagonals | CONSTANT | T15#1 |
| 10 | `movement.barrier_quota` | max barriers police may place | 14 | MINIMUM | T15#2 |
| 11 | `movement.max_steps` | max steps per sub-game | 35 | MINIMUM | T15#3 |
| 12 | `movement.survival_threshold` | steps thief must survive to win | 35 | MINIMUM | T15#4 |
| 13 | `scent.source_strength` | pheromone at emitting cell | 0.9 | CONSTANT | T16#1 |
| 14 | `scent.decay_rate` | decay per turn | 0.10 | CONSTANT | T16#2 |
| 15 | `scent.field_size` | emission window side | 5 | CONSTANT | T16#3 |
| 16 | `scoring.capture_police` | police score on capture | 20 | CONSTANT | T17#1 |
| 17 | `scoring.capture_thief` | thief score on being captured | 5 | CONSTANT | T17#2 |
| 18 | `scoring.survival_police` | police score if thief survives | 5 | CONSTANT | T17#3 |
| 19 | `scoring.survival_thief` | thief score on survival | 10 | CONSTANT | T17#4 |
| 20 | `scoring.tie` | score each on aggregate tie | 2 | CONSTANT | T17#5 |
| 21 | `league.sub_games` | sub-games per series | 6 | CONSTANT | T18#1 |
| 22 | `league.variety_reward` | bonus for beating a new opponent | 10 | CONSTANT | T18#2 |
| 23 | `league.min_games_to_pass` | min games vs distinct groups | 2 | CONSTANT | T18#3 |
| 24 | `league.max_games_per_group` | max games per group | 10 | CONSTANT | T18#5 |
| 25 | `network.requests_per_minute` | outgoing API rate | 30 | MINIMUM | T19#1 |
| 26 | `network.parallel_requests` | max concurrent requests | 2 | MINIMUM | T19#2 |
| 27 | `network.retry_delay_s` | wait before retry | 5 | MINIMUM | T19#3 |
| 28 | `network.retry_attempts` | retries before failure | 3 | MINIMUM | T19#4 |
| 29 | `network.queue_depth` | request queue under load | 100 | MINIMUM | T19#5 |
| 30 | `network.response_timeout_s` | per-request timeout | 30 | NEGOTIABLE | T19#6 |
| 31 | `network.watchdog_timeout_s` | freeze time before Watchdog acts | 60 | NEGOTIABLE | T19#7 |

`league.token_estimate_per_series` (~200000, NEGOTIABLE, T18#4) is tracked as a
cost/reporting figure (see COST_ANALYSIS.md), not a hard gameplay parameter.

## Private per-peer parameters (Appendix F Tables 21–22 — never shared, no negotiation)

| Key | Meaning | Values / Example |
|---|---|---|
| `[strategy].thief_class` | strategy class overriding `ThiefBrain` (`_pick_move` chooses evasion step) | `pkg.mod:Class` |
| `[trash_talk].provider` | verbal-deception LLM mode (never decides moves) | `template` (default) / `ollama` / `claude_api` / `claude_cli` |
| `[trash_talk].every_n_steps` | invoke LLM only every N turns | integer ≥ 1 |
| `[gatekeeper].session_token_budget` | local token ceiling | ~200000 |

> The thief never places barriers; there is no barrier key in the thief's private config.

## Config mandatory rules (Appendix F §2, p. 140)
1. Both groups define **all** shared values; values must be **identical** and **crypto-locked**.
2. A new game may change definitions **only if the opponent agrees**.
3. Each game's config gets a distinct name (`config_<game_id>_g<NN>.json`) for replay.
4. Each game's config file **must be committed** to the GitHub repo.
5. Code may change between games; each game, email the lecturer the **commit hash** used.

## Validation behaviour (to implement Stage 1+)
On load: schema-validate against `shared_config.schema.json`; enforce CONSTANT equality,
MINIMUM lower bounds, and NEGOTIABLE presence; reject unknown fields; log the resolved
config safely (no secrets). Invalid config ⇒ refuse to start (fail safely).
