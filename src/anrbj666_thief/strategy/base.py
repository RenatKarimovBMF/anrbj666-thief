"""Pluggable strategy base classes (Appendix F T22).

A concrete police brain implements ``_decide_move`` (step + optional barrier); a
thief brain implements ``_pick_move`` (step only - the thief never places
barriers). The public ``decide`` returns a uniform :class:`Action`. Brains are
deterministic in Stage 3 and never call an LLM (Rule 25).
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from anrbj666_thief.strategy.action import Action

if TYPE_CHECKING:
    from anrbj666_thief.game.engine import GameState
    from anrbj666_thief.game.geometry import Position


class PoliceBrain(ABC):
    @abstractmethod
    def _decide_move(self, state: GameState) -> Action:
        """Return the police action (step + optional barrier) for this turn."""

    def decide(self, state: GameState) -> Action:
        return self._decide_move(state)


class ThiefBrain(ABC):
    @abstractmethod
    def _pick_move(self, state: GameState) -> Position:
        """Return the thief's step for this turn (no barriers)."""

    def decide(self, state: GameState) -> Action:
        return Action(move_to=self._pick_move(state), barrier_at=None)
