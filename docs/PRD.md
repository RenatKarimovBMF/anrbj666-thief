# PRD Index — Thief

The book recommends one PRD per development layer (§10.2–10.3). To avoid premature
design, **each mechanism PRD is authored just before its stage** and lives beside this
index as `docs/prd/<name>.md`. This file is the master index and current-scope PRD.

## Product goal
An autonomous **thief** peer that, cooperating with no one and trusting no one, evades
an adversarial police agent on a shared grid under partial observability — surviving to
the threshold, proving its honesty cryptographically, communicating (and deceiving) in
free natural language, and reporting verifiable results, while running fully offline in
template mode.

## Success criteria (book §11.4 four metrics + course)
Coordination, adaptation, integrity, architecture; plus ≥2 full league games vs distinct
groups, ≥85% coverage, ruff-clean, reproducible install/run, no secrets.

## Per-mechanism PRDs (authored per stage)
| PRD | Stage | Status |
|---|---|---|
| board & movement logic | 1 | pending |
| configuration & shared contracts | 1 | drafted in CONFIGURATION.md |
| scoring & termination (thief survival) | 1 | pending |
| FastMCP P2P protocol | 2 | pending |
| orchestrator & state machine | 2 | pending |
| reliability (deadline, watchdog) | 2/6 | pending |
| strategy module (ThiefBrain) | 3 | pending |
| thief strategy (evasion + survival) | 3 | pending |
| belief-state mechanism (pursuer estimate) | 3/4 | pending |
| scent / pheromone mechanism (emission) | 4 | pending |
| natural-language hints | 4 | pending |
| bluff generation | 4 | pending |
| bluff analysis | 4 | pending |
| public networking & tunneling | 5 | pending |
| Commit-Reveal / SHA-256 / nonce | 6 | pending |
| audit & log integrity | 6 | pending |
| API Gatekeeper / provider-independent LLM / template fallback | 4 | pending |
| live GUI | 7 | pending |
| replay viewer / verification engine | 7 | pending |
| Gmail reporting / OAuth setup | 7 | pending |
| final JSON artifacts / league interoperability | 7 | pending |

## Current scope (Stage 0)
Planning, requirements capture, safe scaffolding only. **No game code.** Exit criteria:
docs complete and internally consistent; skeletons import-clean; ruff clean; no secrets;
both repos committed manually.
