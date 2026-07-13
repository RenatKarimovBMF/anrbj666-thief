# Architecture — Thief peer

## Principles (Appendix E, Rules 1–9)
- **Autonomous, symmetric, independent peer.** The thief process owns **only** its
  permitted local knowledge. It never accesses the police's private state, private
  log, secret nonce, or true position except via legal revealed protocol messages.
- **Zero-Trust, no judge.** No central server, no shared truth, no shared DB, no
  common `GameManager`. Correctness is proven bottom-up via Commit-Reveal + audit.
- **Deterministic validation for all mandatory rules.** The LLM never enforces rules,
  validates moves, validates commitments, or decides protocol validity.

## Forbidden (must never appear)
Shared mutable state; a shared local state file with both sides' private info; one
process knowing both true positions; importing the other repo's runtime code; LLM
bypassing move validation; localhost-only final architecture; unsigned logs presented
as verified; hardcoded opponent-specific cheating; a common DB as source of truth.

## Layered module map (built stage by stage)
```
src/anrbj666_thief/
├── config/         # central loader + schema validation (Stage 1)      RQ-BOARD-03
├── board/          # grid, movement rules, capture detection (Stage 1) RQ-MOVE/CAP
├── scoring/        # win/termination + scoring table (Stage 1)         RQ-SCORE/WIN
├── mcp/            # FastMCP server + client tools (Stage 2)           RQ-ARCH-01
├── orchestrator/   # state machine + turn loop (Stage 2)              RQ-ARCH-03/04
├── reliability/    # deadline tracker + watchdog (Stage 2/6)          RQ-ARCH-06/07
├── strategy/       # ThiefBrain + belief heatmap + evasion (Stage 3)  RQ-STRAT
├── scent/          # emission + decay 5x5 as the thief moves (Stage 4) RQ-SCENT-01
├── protocol/       # free-language dialogue + schemas (Stage 4)        RQ-LANG
├── llm/            # provider-independent interface + Gatekeeper (Stage 4) RQ-LLM/GATE
├── net/            # tunnel exposure config (Stage 5)                  RQ-NET-10
├── crypto/         # commit-reveal, nonce, step0, verify (Stage 6)     RQ-CRYPT
├── audit/          # signed structured logs (Stage 6)                  RQ-AUDIT-01
├── report/         # artifacts + gmail/oauth (Stage 7)                 RQ-GMAIL/ART
├── gui/            # live belief heatmap + turn banner (Stage 7)       RQ-ARCH-08/09
└── replay/         # replay viewer + verification engine (Stage 7)     RQ-REPLAY-01
```
Each source file targets ≈≤150 lines; larger files require a documented exception.

## Thief-specific responsibilities
- **No barriers.** The thief never places barriers; it must *validate* the police's
  openly-declared barrier placements and *react* to them. A barrier dropped on the
  thief's current cell counts as a capture (Rule 46) that the thief must recognize.
- **Survival & evasion:** the thief wins by surviving `survival_threshold` steps
  (Appendix F T15#4) or is captured on overlap (Rule 48), by being trapped (Rule 46),
  or by having no legal move (Rule 47).
- **Scent emission:** the thief emits pheromone as it moves (source 0.9, decay 0.10,
  5×5 window; Appendix F T16), which the police may exploit — creating the deception
  trade-off between moving effectively and leaving a faint trail.
- **`_pick_move`** for the thief selects the evasion/survival step (Appendix F T22).

## Peer contract (symmetric, must interoperate with other groups)
Each peer exposes required FastMCP tools, consumes the peer protocol, validates every
incoming and outgoing message, rejects illegal moves / malformed data / invalid
commitments / invalid reveals, enforces deadlines, uses Watchdog behaviour, produces
deterministic hashing evidence, keeps auditable logs, fails safely when the peer is
unavailable, supports public-network + local-deterministic modes. Details in
INTEROPERABILITY.md.

## LLM boundary
`llm/` exposes a provider-independent interface with modes `template` (default, zero
tokens, offline), `ollama`, `claude_api`, `claude_cli` (Appendix F T21). All external
calls pass through the **Gatekeeper** (rate/parallel/retry/queue/timeout/cost, Appendix
F T19). Strict validation is applied to all LLM text and any structured output; invalid
output falls back to template behaviour.
