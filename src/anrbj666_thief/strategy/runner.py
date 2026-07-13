"""Drive two strategy brains through the Stage 1 engine to termination.

Single-process helper (no networking): each round both brains decide from the
current state, then the engine applies police-then-thief and evaluates capture /
termination. Real matches run this loop across the FastMCP link (later stages);
here it validates that the blind strategy executes a shortest path end-to-end.
"""

from __future__ import annotations

from anrbj666_thief.game.engine import GameState, play_round
from anrbj666_thief.strategy.base import PoliceBrain, ThiefBrain


def play_with_strategies(
    state: GameState,
    police_brain: PoliceBrain,
    thief_brain: ThiefBrain,
    max_rounds: int | None = None,
) -> GameState:
    """Play until the game finishes or *max_rounds* rounds have elapsed."""
    limit = max_rounds if max_rounds is not None else state.config.movement.max_steps
    rounds = 0
    while not state.finished and rounds < limit:
        police_action = police_brain.decide(state)
        thief_action = thief_brain.decide(state)
        play_round(
            state,
            police_to=police_action.move_to,
            thief_to=thief_action.move_to,
            barrier_at=police_action.barrier_at,
        )
        rounds += 1
    return state
