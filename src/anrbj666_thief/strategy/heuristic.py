"""Default heuristic thief brain (Stage 3 blind navigation).

``HeuristicThief`` steps along the shortest legal path toward a **known** target
cell - the milestone behaviour: "given a known target cell, compute and execute
the shortest legal path". With no explicit target it heads for the corner
farthest from the police. When the target is unreachable (or already reached) it
falls back to the legal step that maximises distance from the police. In Stage 3
the police cell is read directly; Stage 4 replaces it with a belief estimate and
adds scent-driven deception. The LLM never decides moves (Rule 25).
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from anrbj666_thief.game.geometry import Position, manhattan
from anrbj666_thief.game.rules import legal_moves
from anrbj666_thief.strategy.base import ThiefBrain
from anrbj666_thief.strategy.pathfinding import next_step_toward

if TYPE_CHECKING:
    from anrbj666_thief.game.engine import GameState


class HeuristicThief(ThiefBrain):
    def __init__(self, target: Position | None = None) -> None:
        self._target = target

    def _pick_move(self, state: GameState) -> Position:
        target = self._target if self._target is not None else _farthest_corner(state)
        step = next_step_toward(
            state.board, state.thief, target, blocked=(state.police,)
        )
        if step != state.thief:
            return step
        return _evade(state)


def _farthest_corner(state: GameState) -> Position:
    last = state.board.size - 1
    corners = [Position(0, 0), Position(0, last), Position(last, 0), Position(last, last)]
    return max(corners, key=lambda c: manhattan(c, state.police))


def _evade(state: GameState) -> Position:
    """Legal step maximising Manhattan distance from the police (never onto it)."""
    options = legal_moves(state.board, state.thief, blocked=(state.police,))
    return max(options, key=lambda m: manhattan(m, state.police))
