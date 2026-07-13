"""Capture detection (Appendix E Rules 46-48).

Three independent ways the thief is captured:
* **overlap**  - police and thief occupy the same cell (Rule 48);
* **barrier**  - a barrier is placed on the thief's cell (Rule 46);
* **trapped**  - the thief has no free orthogonal neighbour to step to, i.e. it
  is walled in / cornered with no legal move out (Rule 47). Staying in place
  does not count as an escape.

The Rule 47 "no legal move" wording is interpreted as "no adjacent cell to move
into"; this interpretation is tracked as an open clarification (see
docs/REQUIREMENTS_CONFLICTS.md) but does not affect the default-config games.
"""

from __future__ import annotations

from collections.abc import Iterable
from enum import Enum

from anrbj666_thief.game.board import Board
from anrbj666_thief.game.geometry import Position, neighbors


class CaptureReason(str, Enum):
    OVERLAP = "overlap"
    BARRIER = "barrier"
    TRAPPED = "trapped"


def is_overlap(police_pos: Position, thief_pos: Position) -> bool:
    return police_pos == thief_pos


def is_barrier_capture(board: Board, thief_pos: Position) -> bool:
    return board.is_barrier(thief_pos)


def is_trapped(
    board: Board,
    thief_pos: Position,
    blocked: Iterable[Position] = (),
) -> bool:
    """True if no orthogonal neighbour of the thief is enterable."""
    blocked_set = set(blocked)
    return all(
        (not board.is_free(n)) or n in blocked_set
        for n in neighbors(thief_pos)
    )


def capture_reason(
    board: Board,
    police_pos: Position,
    thief_pos: Position,
) -> CaptureReason | None:
    """Return why the thief is captured, or ``None`` if it is free."""
    if is_overlap(police_pos, thief_pos):
        return CaptureReason.OVERLAP
    if is_barrier_capture(board, thief_pos):
        return CaptureReason.BARRIER
    if is_trapped(board, thief_pos, blocked=(police_pos,)):
        return CaptureReason.TRAPPED
    return None


def is_captured(board: Board, police_pos: Position, thief_pos: Position) -> bool:
    return capture_reason(board, police_pos, thief_pos) is not None
