"""Geometric message contract for the Stage 2 numeric transport.

A :class:`GeometricMessage` is a small, immutable, JSON-serialisable record with
numeric coordinates. :func:`parse_geometric` validates untrusted wire data (from a
peer) strictly - unknown keys, wrong types, bad roles/kinds, and (optionally)
out-of-bounds coordinates are rejected - so a malformed or hostile peer message
can never be silently accepted. ``canonical_json`` gives a deterministic encoding
suitable for later Commit-Reveal hashing (Stage 6).
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from enum import Enum
from typing import Any

_ROLES = {"police", "thief"}
_WIRE_KEYS = {"game_id", "sender_role", "step", "kind", "row", "col"}


class ProtocolError(ValueError):
    """Raised when a wire message violates the geometric-message contract."""


class MessageKind(str, Enum):
    POSITION = "position"
    MOVE = "move"


@dataclass(frozen=True)
class GeometricMessage:
    game_id: str
    sender_role: str
    step: int
    kind: MessageKind
    row: int
    col: int

    @property
    def coordinate(self) -> tuple[int, int]:
        return (self.row, self.col)

    def to_wire(self) -> dict[str, Any]:
        """Return the plain-dict wire representation of this message."""
        return {
            "game_id": self.game_id,
            "sender_role": self.sender_role,
            "step": self.step,
            "kind": self.kind.value,
            "row": self.row,
            "col": self.col,
        }

    def canonical_json(self) -> str:
        """Deterministic, key-sorted JSON encoding (stable for hashing)."""
        return json.dumps(self.to_wire(), sort_keys=True, separators=(",", ":"))


def parse_geometric(
    data: Any,
    *,
    board_size: int | None = None,
) -> GeometricMessage:
    """Validate untrusted *data* and build a :class:`GeometricMessage`.

    If *board_size* is given, coordinates must lie inside the ``board_size`` grid.
    """
    if not isinstance(data, dict):
        raise ProtocolError("geometric message must be a JSON object")
    missing = _WIRE_KEYS - data.keys()
    if missing:
        raise ProtocolError(f"missing keys {sorted(missing)}")
    unknown = data.keys() - _WIRE_KEYS
    if unknown:
        raise ProtocolError(f"unknown keys {sorted(unknown)}")

    role = data["sender_role"]
    if role not in _ROLES:
        raise ProtocolError(f"sender_role: must be one of {sorted(_ROLES)}")
    kind_raw = data["kind"]
    try:
        kind = MessageKind(kind_raw)
    except ValueError:
        raise ProtocolError(f"kind: unknown value {kind_raw!r}") from None

    step = _int(data["step"], "step")
    if step < 0:
        raise ProtocolError("step: must be >= 0")
    row = _int(data["row"], "row")
    col = _int(data["col"], "col")
    if board_size is not None and not (
        0 <= row < board_size and 0 <= col < board_size
    ):
        raise ProtocolError(
            f"coordinate ({row},{col}) outside the {board_size}x{board_size} board"
        )
    return GeometricMessage(
        game_id=str(data["game_id"]), sender_role=role, step=step,
        kind=kind, row=row, col=col,
    )


def _int(value: Any, ctx: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise ProtocolError(f"{ctx}: expected an integer, got {value!r}")
    return value
