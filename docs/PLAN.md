# PLAN — Thief

High-level delivery plan aligned to the seven official stages (see
DEVELOPMENT_STAGES.md). Each stage: re-read sources → update matrix/PRD → tests →
smallest implementation → full suite + coverage + ruff + type + security → docs →
evidence → PROMPT_BOOK → self-review → **manual commit checkpoint** → stop.

| Stage | Goal | Key acceptance | Repos touched |
|---|---|---|---|
| 0 | Setup & planning | docs + skeletons, no game code | both |
| 1 | Base logic | legal moves, capture detection, survival win, scoring, config validation | both |
| 2 | FastMCP infra | localhost geometric message round-trip; FSM; deadline/watchdog | both |
| 3 | Blind strategy | maximizing-escape legal move to a known threat; ThiefBrain plug-in | both |
| 4 | Language + scent | free-language hints/bluff; 5×5 scent emit/decay; LLM; Gatekeeper | both |
| 5 | Cloud + tunnel | remote machine plays a full round via tunnel | both |
| 6 | Security & crypto | Commit-Reveal + nonce + Step-0; audit logs; mismatch = loss | both |
| 7 | Reporting shell | Gmail send; Live GUI; Replay "Verified OK"; 4 JSON artifacts | both |
| Final | Hardening | clean-env uv sync; ≥85% cov; ruff 0; 2-machine; screenshots; manual tag | both |

## Milestones (book §10.4 checklist)
- S1: two agents move legally; over-quota barrier rejected; overlap ⇒ capture.
- S2: geometric msg A→B over localhost parsed correctly by B.
- S3: given known threat, compute+execute a maximizing-escape move unaided.
- S4: hint→inference; scent updates+decays each step; LLM emits true/false hint.
- S5: remote agent connects via ngrok and plays a full round.
- S6: move Committed then Revealed with valid nonce; Step-0 verifies hardware.
- S7: summary emailed via Gmail; GUI shows state; Replay reconstructs a recorded round.

## Constraints
No paid API calls without explicit approval; no Gmail sends in automated tests; template
mode must always work; never skip ahead (book §10.4).

## Timeline anchor
Hard deadline **12/08/2026 23:59**. No late submissions accepted.
