# Cost Analysis — Thief

The game is designed to run **with no paid API at all** (Appendix F Table 21, course
text). Default LLM mode is `template` = **zero tokens, offline, free**. Paid modes are
opt-in and gated.

## LLM modes and cost (Appendix F Table 21)
| Mode | Where it runs | Token cost | Money | Notes |
|---|---|---|---|---|
| `template` (default) | in-process | 0 | free | prewritten sentence bank |
| `ollama` | `localhost:11434` | 0 API tokens | free | local model, needs Ollama install |
| `claude_api` | Anthropic API | real, billed | paid | small model (Haiku); needs API key |
| `claude_cli` | Claude Code CLI | subscription | paid | highest cost |

`[trash_talk].every_n_steps` reduces calls by invoking the model only every N turns.
In `template`/`ollama` the whole 6-sub-game series runs at zero token cost.

## Budget guidance
- `league.token_estimate_per_series` ≈ **200000** (Appendix F T18#4, NEGOTIABLE) — a
  reporting estimate, not a hard cap. Actual consumption is measured and reported in
  `result_<game_id>.json` (Rule 54) and in the Gmail summary.
- The **Gatekeeper** (Stage 4) enforces per-request and per-session token ceilings,
  rate limits (Appendix F T19), and cost estimation; it logs usage without secrets.

## Cost controls (policy)
- No paid API calls during development without explicit human approval.
- No Gmail sends in automated tests.
- Before any real external call: state what is called, expected cost, data sent, and
  request approval.

## AI-assisted development cost
Recorded per session in PROMPT_BOOK.md (model, purpose, measured/estimated cost when
available). Kept separate from in-game LLM token accounting above.
