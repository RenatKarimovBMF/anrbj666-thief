"""Runnable localhost entrypoint for the thief FastMCP server (Stage 2).

Run with ``uv run python -m anrbj666_thief.mcp`` (see docs/OPERATIONS.md). Reads
``SELF_HOST``/``SELF_PORT``/``AGENT_ROLE`` from the environment (.env). Started
manually per the manual-Git / operations policy; not exercised by the unit suite.
"""

from __future__ import annotations

import os

from anrbj666_thief.mcp.inbox import Inbox
from anrbj666_thief.mcp.server import build_server


def main() -> None:  # pragma: no cover - starts a blocking network server
    role = os.environ.get("AGENT_ROLE", "thief")
    host = os.environ.get("SELF_HOST", "127.0.0.1")
    port = int(os.environ.get("SELF_PORT", "8902"))
    server = build_server(role=role, inbox=Inbox(role=role))
    server.run(transport="http", host=host, port=port)


if __name__ == "__main__":  # pragma: no cover
    main()
