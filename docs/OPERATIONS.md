# Operations — Thief (Windows PowerShell)

> Stage 0: commands below are the intended workflow; game entry points appear from
> Stage 1 onward. All Git writes are **manual/human-only**.

## Environment
```powershell
uv sync                      # create venv + install locked deps
uv run pytest                # unit suite (offline, template mode)
uv run pytest --cov=src --cov-report=term-missing
uv run ruff check .          # must be zero violations
```

## Local two-terminal play (from Stage 2)
Open two PowerShell terminals (thief here, police in the companion repo). Exact
`uv run ...` server/client commands are documented when Stage 2 lands.

## Public two-machine play (from Stage 5)
1. Copy `.env.example` → `.env`; set `NGROK_AUTHTOKEN` and ports (thief default 8902).
2. Start the tunnel; publish `SELF_PUBLIC_URL`; exchange endpoints with the opponent.
3. Run a full 6-sub-game series; capture screenshots of the Live GUI and Replay.
- These are **manual** tests (marked `network`), not part of the automatic suite.

## Gmail reporting (from Stage 7)
- One-time OAuth per Appendix A (Google API guide). Store `credentials.json` /
  `token.json` locally (git-ignored). Send-only scope.
- Automated tests build the payload but **never send**. A real send is a manual,
  approved step; target `rmisegal+uoh26finalgame@gmail.com`.

## Artifacts
Signed JSON artifacts are written to `artifacts/` and committed deliberately (not under
`logs/`). Four per series: `declaration_*`, `config_*`, `log_*`, `result_*`.

## Read-only Git for humans (verification)
```powershell
git status ; git log --oneline ; git remote -v ; git branch --show-current
```
