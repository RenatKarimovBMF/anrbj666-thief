"""Breadth-first shortest legal path over the grid.

Movement is ``orthogonal4_plus_stay`` (no diagonals), so an unweighted BFS yields
a shortest path. Cells occupied by barriers or listed in *blocked* (e.g. the
opponent, when we must not path through it) are impassable. Neighbours are
expanded in a fixed order (:data:`STEP_DELTAS`) so paths are deterministic.
"""

from __future__ import annotations

from collections import deque
from collections.abc import Iterable

from anrbj666_thief.game.board import Board
from anrbj666_thief.game.geometry import STEP_DELTAS, Position, translate


def bfs_path(
    board: Board,
    start: Position,
    goal: Position,
    blocked: Iterable[Position] = (),
) -> list[Position] | None:
    """Return a shortest path ``[start, ..., goal]`` or ``None`` if unreachable."""
    if start == goal:
        return [start]
    blocked_set = set(blocked)
    if not board.is_free(goal) or goal in blocked_set:
        return None
    prev: dict[Position, Position | None] = {start: None}
    queue: deque[Position] = deque([start])
    while queue:
        current = queue.popleft()
        for delta in STEP_DELTAS:
            nxt = translate(current, delta)
            if nxt in prev or not board.is_free(nxt) or nxt in blocked_set:
                continue
            prev[nxt] = current
            if nxt == goal:
                return _reconstruct(prev, goal)
            queue.append(nxt)
    return None


def next_step_toward(
    board: Board,
    start: Position,
    goal: Position,
    blocked: Iterable[Position] = (),
) -> Position:
    """Return the first step of the shortest path, or *start* if none exists."""
    path = bfs_path(board, start, goal, blocked)
    if path is None or len(path) < 2:
        return start
    return path[1]


def shortest_path_length(
    board: Board,
    start: Position,
    goal: Position,
    blocked: Iterable[Position] = (),
) -> int | None:
    """Return the number of steps in the shortest path, or ``None``."""
    path = bfs_path(board, start, goal, blocked)
    return None if path is None else len(path) - 1


def _reconstruct(
    prev: dict[Position, Position | None], goal: Position
) -> list[Position]:
    path = [goal]
    node = prev[goal]
    while node is not None:
        path.append(node)
        node = prev[node]
    path.reverse()
    return path
