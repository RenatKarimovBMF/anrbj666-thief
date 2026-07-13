"""Client helpers for talking to an opponent's FastMCP server (Stage 2).

*target* is anything FastMCP's :class:`~fastmcp.Client` accepts: a ``FastMCP``
instance (in-memory, used in tests), or an ``http(s)://`` URL for a localhost peer
(Stage 2) or a tunnelled public peer (Stage 5). The helpers open a short-lived
connection per call; batching/persistent sessions arrive with the Gatekeeper
(Stage 4/7).
"""

from __future__ import annotations

from typing import Any

from fastmcp import Client

from anrbj666_thief.mcp.messages import GeometricMessage


async def ping(target: Any) -> dict[str, Any]:
    """Ping a peer; return its ``{"ok", "role"}`` identity payload."""
    async with Client(target) as client:
        result = await client.call_tool("ping", {})
        return result.data


async def send_geometric(target: Any, message: GeometricMessage) -> dict[str, Any]:
    """Send one geometric message to a peer; return the server's ack payload."""
    async with Client(target) as client:
        result = await client.call_tool(
            "submit_geometric", {"message": message.to_wire()}
        )
        return result.data
