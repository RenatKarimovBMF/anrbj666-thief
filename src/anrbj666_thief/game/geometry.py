"""Grid geometry primitives.

Coordinates follow Appendix F T13#3: origin ``top-left`` at ``(0, 0)`` with axes
growing down (row) and right (col). The movement set is ``orthogonal4_plus_stay``
(Appendix F T15#1): four cardinal steps plus staying in place, never diagonal.
"""

from __future__ import annotations

from typing import NamedTuple


class Position(NamedTuple):
    row: int
    col: int


# Cardinal step deltas only (no diagonals). "Stay" is the zero delta, handled
# separately so callers can distinguish a real step from remaining in place.
STEP_DELTAS: tuple[tuple[int, int], ...] = ((-1, 0), (1, 0), (0, -1), (0, 1))
STAY_DELTA: tuple[int, int] = (0, 0)


def in_bounds(pos: Position, size: int) -> bool:
    """Return True if *pos* lies inside a ``size`` x ``size`` grid."""
    return 0 <= pos.row < size and 0 <= pos.col < size


def translate(pos: Position, delta: tuple[int, int]) -> Position:
    """Return *pos* shifted by *delta* (row, col)."""
    return Position(pos.row + delta[0], pos.col + delta[1])


def neighbors(pos: Position) -> list[Position]:
    """Return the four orthogonal neighbours of *pos* (unbounded, unfiltered)."""
    return [translate(pos, d) for d in STEP_DELTAS]


def manhattan(a: Position, b: Position) -> int:
    """Return the Manhattan (L1) distance between two positions."""
    return abs(a.row - b.row) + abs(a.col - b.col)
