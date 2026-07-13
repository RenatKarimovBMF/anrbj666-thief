# Interoperability

The project MUST play against other groups' implementations. The protocol is therefore
the **mandatory public contract**, not a private scheme that only works between our two
repos. This document is duplicated (identical intent) in both repos and is versioned
together with the shared config.

## Ground rules
- Use the mandatory protocol/message shapes from the book (Chapters 2, 5; Appendix F).
- One repo must **never** import runtime code from the other; only public contracts,
  JSON schemas, and message models may be duplicated.
- Validate unknown/additional fields safely (ignore unknown, never crash) while
  rejecting malformed or type-invalid required fields.
- Any change to a public contract requires updating **both repos**, the requirements
  matrix, this doc, and tests, and stopping for manual commits in both repos.

## To be specified precisely before Stage 2/4/6 (tracked as PRDs)
- FastMCP tool names, request/response schemas, and error responses.
- Version negotiation (`config_version`) and rejection of incompatible versions.
- Identifiers: `game_id`, `game_uid`, sub-game index `<NN>`, turn id, message id.
- Timeouts (`network.response_timeout_s`), retries (`retry_attempts`,`retry_delay_s`).
- Commit-Reveal ordering: commit(t) precedes reveal(t) exactly one turn later; define
  what is hashed and in what order.
- **Deterministic serialization for hashing:** UTF-8, sorted keys, no insignificant
  whitespace, fixed number formatting — so independent implementations produce the
  same SHA-256. (Exact canonical form finalized in the Commit-Reveal PRD, Stage 6.)
- Character encoding: UTF-8 everywhere. Timestamps: ISO-8601 UTC.
- Free-language dialogue channel (Stage 4): hints are natural-language, ≤
  `verbal.hint_word_limit` words; **no** direct numeric-coordinate protocol (Rule 27).

## Signed submission artifacts (Appendix F Table 20)
Four JSON files carry a shared `game_uid`; each file name derives from `game_id`:
- `declaration_<game_id>.json` — pre-game declaration (teams, repos, MCP addresses,
  hardware, model, token ceiling, start/end times; cryptographically signed constants).
- `config_<game_id>_g<NN>.json` — the agreed, crypto-locked per-sub-game config.
- `log_<game_id>_g<NN>.json` — per-sub-game step log enabling full crypto verification in replay.
- `result_<game_id>.json` — final aggregate results for league scoring; emailed to the lecturer.

Both groups must **agree on the result and each send its own** result report; a missing
or contradictory report ⇒ game disqualified, 0 to both (Rule 35).

## Test fixtures (to build)
`tests/fixtures/` will hold example **valid** and **invalid** messages and a golden
canonical-hash vector, so cross-group compatibility can be tested offline and
deterministically.

## Lecturer / league addresses (reference only — Appendix F Table 20)
- Example reference simulator: `https://github.com/rmisegal/GameP2PCopChase`
- Lecturer / repo sharing: `rmisegal@gmail.com`
- Automated JSON report target: `rmisegal+uoh26finalgame@gmail.com`
