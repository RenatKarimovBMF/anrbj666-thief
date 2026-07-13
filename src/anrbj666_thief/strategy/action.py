"""A single turn's decision produced by a strategy brain."""

from __future__ import annotations

from dataclasses import dataclass

from anrbj666_thief.game.geometry import Position


@dataclass(frozen=True)
class Action:
    """One agent's chosen move, plus an optional barrier (police only).

    ``barrier_at`` is always ``None`` for the thief; it exists so the symmetric
    strategy interface can represent the police's barrier action too.
    """

    move_to: Position
    barrier_at: Position | None = None
