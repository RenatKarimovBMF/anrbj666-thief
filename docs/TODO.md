# TODO — Thief

Living task list. `[ ]` open · `[~]` in progress · `[x]` done. Grouped by stage.

## Stage 0 — setup & planning
- [x] Read-only verify repo (branch `main`, remote, clean tree)
- [x] `.cursor/rules/00-manual-git.mdc`
- [x] `.gitignore`, `.env.example`
- [x] `pyproject.toml`, `src/anrbj666_thief` package skeleton
- [x] `config/` shared schema + example + private example
- [x] All planning & requirements docs
- [ ] Human: manual first commit + push (thief)
- [ ] Human: confirm `COMMIT DONE: STAGE 0 ...`

## Stage 1 — base logic (blocked until Stage 0 committed)
- [ ] Central config loader + schema validation + CONSTANT/MIN/NEGOTIABLE checks
- [ ] Board model (size ≥7) + coordinate system
- [ ] Movement rules (orthogonal + stay, no diagonals) + boundary
- [ ] Capture detection (overlap / trapped-by-barrier / no-legal-move)
- [ ] Thief survival win at `survival_threshold` (+ resolve C-002)
- [ ] Scoring table
- [ ] Tests + coverage + ruff + docs + evidence

## Later stages
- [ ] Stage 2 FastMCP infra · [ ] Stage 3 strategy · [ ] Stage 4 language+scent
- [ ] Stage 5 tunnel · [ ] Stage 6 crypto · [ ] Stage 7 reporting · [ ] Final hardening

## Open questions
- [ ] C-002: are `max_steps` and `survival_threshold` independent? (confirm before S1 win logic)
