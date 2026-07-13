"""FastMCP server exposing this peer's geometric tools (Stage 2).

``build_server`` wires a :class:`~anrbj666_thief.mcp.inbox.Inbox` behind two
tools: ``ping`` (liveness/identity) and ``submit_geometric`` (accept one validated
geometric message from the opponent). Untrusted input is validated by
:func:`~anrbj666_thief.mcp.messages.parse_geometric`; invalid data is rejected
with a :class:`fastmcp.exceptions.ToolError` and never reaches the inbox.
"""

from __future__ import annotations

from typing import Any

from fastmcp import FastMCP
from fastmcp.exceptions import ToolError

from anrbj666_thief.mcp.inbox import Inbox
from anrbj666_thief.mcp.messages import ProtocolError, parse_geometric


def build_server(
    role: str,
    inbox: Inbox,
    board_size: int | None = None,
    name: str | None = None,
) -> FastMCP:
    """Build a FastMCP server for this peer bound to *inbox*."""
    server: FastMCP = FastMCP(name=name or f"anrbj666-{role}")

    @server.tool
    def ping() -> dict[str, Any]:
        """Liveness/identity check; returns this peer's role."""
        return {"ok": True, "role": role}

    @server.tool
    def submit_geometric(message: dict[str, Any]) -> dict[str, Any]:
        """Accept one geometric message from the opponent, validated strictly."""
        try:
            parsed = parse_geometric(message, board_size=board_size)
        except ProtocolError as exc:
            raise ToolError(f"rejected geometric message: {exc}") from exc
        count = inbox.receive(parsed)
        return {"received": True, "count": count, "echo": parsed.to_wire()}

    return server
