"""Immutable board state: grid size plus the set of placed barrier cells.

The board holds only static topology. Agent positions and the barrier *quota*
live in the engine, because a barrier's legality depends on runtime state
(how many are already placed, where the agents stand).
"""

from __future__ import annotations

from dataclasses import dataclass, field, replace

from anrbj666_thief.game.geometry import Position, in_bounds


@dataclass(frozen=True)
class Board:
    size: int
    barriers: frozenset[Position] = field(default_factory=frozenset)

    def is_inside(self, pos: Position) -> bool:
        return in_bounds(pos, self.size)

    def is_barrier(self, pos: Position) -> bool:
        return pos in self.barriers

    def is_free(self, pos: Position) -> bool:
        """True if *pos* is on the board and not occupied by a barrier."""
        return self.is_inside(pos) and pos not in self.barriers

    def with_barrier(self, pos: Position) -> Board:
        """Return a new board with *pos* added to the barrier set."""
        return replace(self, barriers=self.barriers | {pos})
