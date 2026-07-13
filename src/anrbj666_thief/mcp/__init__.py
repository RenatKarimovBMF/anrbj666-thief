"""Stage 2 FastMCP transport: geometric (numeric-coordinate) P2P messaging.

Each peer runs a FastMCP server exposing geometric tools and can act as a client
to its opponent (Appendix E Rule 1: each peer is both server and client). Stage 2
exchanges **numeric coordinates** purely as the first transport milestone; Stage 4
replaces/wraps this with free-language dialogue so the *final* system never relies
on a direct numeric-position protocol (Rule 27). No strategy, scent, or crypto here.
"""

from anrbj666_thief.mcp.client import ping, send_geometric
from anrbj666_thief.mcp.inbox import Inbox
from anrbj666_thief.mcp.messages import (
    GeometricMessage,
    MessageKind,
    ProtocolError,
    parse_geometric,
)
from anrbj666_thief.mcp.server import build_server

__all__ = [
    "GeometricMessage",
    "Inbox",
    "MessageKind",
    "ProtocolError",
    "build_server",
    "parse_geometric",
    "ping",
    "send_geometric",
]
