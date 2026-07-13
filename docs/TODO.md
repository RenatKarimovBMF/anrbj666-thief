# TODO — Thief

Living task list. `[ ]` open · `[~]` in progress · `[x]` done. Grouped by stage.

## Stage 0 — setup & planning
- [x] Read-only verify repo (branch `main`, remote, clean tree)
- [x] `.cursor/rules/00-manual-git.mdc`
- [x] `.gitignore`, `.env.example`
- [x] `pyproject.toml`, `src/anrbj666_thief` package skeleton
- [x] `config/` shared schema + example + private example
- [x] All planning & requirements docs
- [x] Human: manual first commit + push (thief)
- [x] Human: confirm `COMMIT DONE: STAGE 0 ...`

## Stage 1 — base logic
- [x] Central config loader + schema validation + CONSTANT/MIN/NEGOTIABLE checks (`config/loader.py`)
- [x] Board model (size ≥7) + coordinate system (`game/board.py`, `game/geometry.py`)
- [x] Movement rules (orthogonal + stay, no diagonals) + boundary (`game/rules.py`)
- [x] Capture detection (overlap / barrier-on-thief / trapped) (`game/capture.py`)
- [x] Thief survival win at `survival_threshold`, independent of `max_steps` (C-002/D-007) (`game/scoring.py`)
- [x] Scoring table (`game/scoring.py`)
- [x] Single-process end-to-end driver (`game/engine.py`)
- [x] Tests (71) + coverage (100%) + ruff clean
- [ ] Human: manual commit + push (thief, Stage 1)
- [ ] Human: confirm `COMMIT DONE: STAGE 1 ...`

## Later stages
- [ ] Stage 2 FastMCP infra · [ ] Stage 3 strategy · [ ] Stage 4 language+scent
- [ ] Stage 5 tunnel · [ ] Stage 6 crypto · [ ] Stage 7 reporting · [ ] Final hardening

## Open questions
- [~] C-002: RESOLVED for implementation (independent, default-equal; D-007). Open only for optional lecturer clarification.
- [~] C-005: Rule 47 "trapped" interpretation (no adjacent move = captured). Documented; confirm if desired.
