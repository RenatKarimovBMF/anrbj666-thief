"""Movement and barrier-placement rules (Appendix E).

A move is legal iff its target is reachable under ``orthogonal4_plus_stay`` and
lands on a free cell (inside the board, no barrier, not blocked by the extra
occupancy the caller supplies). Diagonal and multi-step moves are rejected.
Barrier placement legality (Appendix E Rule 45/46) is a police responsibility;
the thief models it only to reason about the shared rules.
"""

from __future__ import annotations

from collections.abc import Iterable

from anrbj666_thief.game.board import Board
from anrbj666_thief.game.geometry import (
    STAY_DELTA,
    STEP_DELTAS,
    Position,
    translate,
)


class MoveError(ValueError):
    """Raised when an illegal move is applied."""


def legal_moves(
    board: Board,
    src: Position,
    blocked: Iterable[Position] = (),
    *,
    allow_stay: bool = True,
) -> list[Position]:
    """Return every legal destination from *src*.

    *blocked* is extra occupancy (e.g. the opponent's cell) that cannot be
    entered. Staying in place is included when *allow_stay* is true.
    """
    blocked_set = set(blocked)
    moves: list[Position] = []
    if allow_stay:
        moves.append(src)
    for delta in STEP_DELTAS:
        target = translate(src, delta)
        if board.is_free(target) and target not in blocked_set:
            moves.append(target)
    return moves


def is_legal_move(
    board: Board,
    src: Position,
    dst: Position,
    blocked: Iterable[Position] = (),
    *,
    allow_stay: bool = True,
) -> bool:
    """True if moving from *src* to *dst* is legal this turn."""
    delta = (dst.row - src.row, dst.col - src.col)
    if delta == STAY_DELTA:
        return allow_stay
    if delta not in STEP_DELTAS:
        return False
    return board.is_free(dst) and dst not in set(blocked)


def apply_move(
    board: Board,
    src: Position,
    dst: Position,
    blocked: Iterable[Position] = (),
    *,
    allow_stay: bool = True,
) -> Position:
    """Return *dst* if the move is legal, else raise :class:`MoveError`."""
    if not is_legal_move(board, src, dst, blocked, allow_stay=allow_stay):
        raise MoveError(f"illegal move {src} -> {dst}")
    return dst


def can_place_barrier(
    board: Board,
    pos: Position,
    placed_count: int,
    quota: int,
    occupied: Iterable[Position] = (),
) -> bool:
    """True if a barrier may be placed on *pos* this turn.

    Rejected when the quota is exhausted (``placed_count >= quota``), the cell is
    off-board, already a barrier, or occupied by an agent whose cell may not be
    walled. Placing on the thief's cell is a *capture* and is handled by the
    engine, not forbidden here; pass only cells that must stay clear as
    *occupied* (e.g. the police's own cell).
    """
    if placed_count >= quota:
        return False
    if not board.is_inside(pos) or board.is_barrier(pos):
        return False
    return pos not in set(occupied)
