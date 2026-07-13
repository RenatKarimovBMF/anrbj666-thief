"""Stage 2 milestone tests: geometric message A -> B over a FastMCP round-trip.

Uses FastMCP's in-memory ``Client(server)`` transport: a real MCP client/server
round-trip with no sockets, which is the deterministic test path recommended by
FastMCP. The runnable localhost server lives in ``mcp/__main__.py`` and is
exercised manually (see docs/OPERATIONS.md).
"""

from __future__ import annotations

import pytest
from fastmcp import Client
from fastmcp.exceptions import ToolError

from anrbj666_thief.mcp.client import ping, send_geometric
from anrbj666_thief.mcp.inbox import Inbox
from anrbj666_thief.mcp.messages import GeometricMessage, MessageKind
from anrbj666_thief.mcp.server import build_server


def _peer_b(board_size: int | None = None) -> tuple[object, Inbox]:
    # In the thief repo, "peer B" (the opponent receiver) is police-role.
    inbox = Inbox(role="police")
    server = build_server(role="police", inbox=inbox, board_size=board_size)
    return server, inbox


async def test_ping_returns_role() -> None:
    server, _ = _peer_b()
    assert (await ping(server))["role"] == "police"


async def test_tools_are_registered() -> None:
    server, _ = _peer_b()
    async with Client(server) as client:
        names = {t.name for t in await client.list_tools()}
    assert {"ping", "submit_geometric"} <= names


async def test_geometric_message_received_and_parsed_by_peer_b() -> None:
    # Milestone: peer A (thief) sends a geometric message; peer B parses it.
    server, inbox = _peer_b(board_size=7)
    outgoing = GeometricMessage("G1", "thief", 4, MessageKind.MOVE, 3, 6)
    ack = await send_geometric(server, outgoing)

    assert ack["received"] is True
    assert ack["count"] == 1
    assert inbox.last is not None
    assert inbox.last == outgoing
    assert inbox.last.coordinate == (3, 6)
    assert inbox.last.kind is MessageKind.MOVE
    assert inbox.last.sender_role == "thief"


async def test_multiple_messages_accumulate() -> None:
    server, inbox = _peer_b()
    first = GeometricMessage("G1", "thief", 0, MessageKind.POSITION, 0, 0)
    second = GeometricMessage("G1", "thief", 1, MessageKind.POSITION, 1, 0)
    await send_geometric(server, first)
    ack = await send_geometric(server, second)
    assert ack["count"] == 2
    assert len(inbox.messages) == 2


async def test_invalid_message_rejected_by_server() -> None:
    server, inbox = _peer_b()
    async with Client(server) as client:
        with pytest.raises(ToolError):
            await client.call_tool("submit_geometric", {"message": {"bad": "data"}})
    assert inbox.messages == []


async def test_out_of_bounds_rejected_by_server() -> None:
    server, inbox = _peer_b(board_size=7)
    bad = GeometricMessage("G1", "thief", 0, MessageKind.MOVE, 9, 9)
    async with Client(server) as client:
        with pytest.raises(ToolError):
            await client.call_tool("submit_geometric", {"message": bad.to_wire()})
    assert inbox.messages == []
