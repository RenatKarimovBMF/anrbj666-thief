# Prompt Book — Thief

Record of major AI-assisted sessions. **Never** record passwords, API keys, OAuth/refresh
tokens, `credentials.json`/`token.json` contents, private personal data, or tunnel tokens.

---

## Session 2026-07-13 — Stage 0 setup & planning
- **Date:** 2026-07-13
- **Team member:** Renat (with Alon)
- **Model:** Cursor agent (Opus 4.8)
- **Purpose:** Verify repositories; create manual-Git rule; author planning &
  requirements documents; create safe Stage-0 skeletons (no game code).
- **Prompt summary:** Proceed with Stage 0 per the project charter — read-only Git
  verification, Cursor rules, planning/requirements docs, safe skeletons, checks, then
  stop for manual commits in both repos.
- **Files affected (thief):** `.cursor/rules/00-manual-git.mdc`, `.gitignore`,
  `.env.example`, `pyproject.toml`, `src/anrbj666_thief/__init__.py`, `.../py.typed`,
  `config/shared_config.schema.json`, `config/shared_config.example.json`,
  `config/private_config.example.toml`, `README.md`, and `docs/*` (PRD, PLAN, TODO,
  REQUIREMENTS_MATRIX, REQUIREMENTS_CONFLICTS, DEVELOPMENT_STAGES, ARCHITECTURE,
  SECURITY, TEST_STRATEGY, COST_ANALYSIS, INTEROPERABILITY, CONFIGURATION, OPERATIONS,
  DECISIONS, RISK_REGISTER, PROMPT_BOOK).
- **Important decisions:** D-001..D-006 (see DECISIONS.md). Extracted the seven official
  stages from Ch. 10.3 and Appendix F Tables 13–22 (authoritative numeric values).
- **Tests performed:** none yet (no production code in Stage 0). Ruff/pytest to run at
  Stage 1.
- **Manual verification performed:** read-only `git status/branch/remote/ls-files` on
  both repos (clean, `main`, correct remotes, zero commits).
- **Known limitations:** planning only; no game logic; C-002 open.
- **Estimated/measured AI cost:** not measured this session.
- **Related stage / commit:** Stage 0 — commit hash to be filled after manual commit.
