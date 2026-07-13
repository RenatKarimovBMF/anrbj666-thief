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
Each peer runs a FastMCP server; the opponent connects over localhost. In the
default suite the A->B round-trip is covered deterministically by FastMCP's
in-memory client; the live localhost path is verified manually:

```powershell
# Terminal 1 - thief server (this repo)
$env:AGENT_ROLE = "thief"; $env:SELF_HOST = "127.0.0.1"; $env:SELF_PORT = "8902"
uv run python -m anrbj666_thief.mcp      # serves streamable HTTP at /mcp

# Terminal 2 - quick client check against a running peer (police or thief URL)
uv run python -c "import asyncio; from anrbj666_thief.mcp.client import ping; print(asyncio.run(ping('http://127.0.0.1:8902/mcp')))"
```

The police server runs identically from the companion repo (default port 8901).
Real-network checks are **manual** (marked `network`) and excluded from the
default `uv run pytest`.

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
