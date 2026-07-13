"""Blind thief strategy + runner tests (Stage 3 milestone).

Milestone: given a known target cell, the agent computes and executes the
shortest legal path without manual help. Here the thief navigates to a known
escape cell; Stage 4 adds belief/scent-driven evasion and deception.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from anrbj666_thief.config import build_config
from anrbj666_thief.game.engine import new_game
from anrbj666_thief.game.geometry import Position, manhattan
from anrbj666_thief.game.scoring import Outcome
from anrbj666_thief.strategy.action import Action
from anrbj666_thief.strategy.base import PoliceBrain
from anrbj666_thief.strategy.heuristic import HeuristicThief
from anrbj666_thief.strategy.runner import play_with_strategies

Factory = Callable[[], dict[str, Any]]


class StayPolice(PoliceBrain):
    """Opponent stub: the police never moves (for deterministic thief tests)."""

    def _decide_move(self, state: Any) -> Action:
        return Action(move_to=state.police, barrier_at=None)


def _game(config_dict: Factory, **overrides: Any):
    data = config_dict()
    for section, values in overrides.items():
        data[section].update(values)
    return new_game(build_config(data))


def test_thief_action_has_no_barrier(config_dict: Factory) -> None:
    state = _game(config_dict)
    action = HeuristicThief().decide(state)
    assert isinstance(action, Action)
    assert action.barrier_at is None


def test_thief_executes_shortest_path_to_known_target(config_dict: Factory) -> None:
    # thief (3,3) -> target (6,6): Manhattan 6, police idle far away.
    target = Position(6, 6)
    state = _game(config_dict)
    final = play_with_strategies(
        state, StayPolice(), HeuristicThief(target=target), max_rounds=6
    )
    assert final.thief == target
    assert final.outcome is Outcome.ONGOING


def test_thief_steps_one_legal_cell_toward_target(config_dict: Factory) -> None:
    target = Position(6, 6)
    state = _game(config_dict)
    move = HeuristicThief(target=target)._pick_move(state)
    # single orthogonal step that reduces distance to the target
    assert manhattan(move, state.thief) == 1
    assert manhattan(move, target) < manhattan(state.thief, target)


def test_default_target_heads_for_farthest_corner(config_dict: Factory) -> None:
    # police at (0,0) -> farthest corner is (6,6); the thief steps toward it.
    state = _game(config_dict)
    move = HeuristicThief()._pick_move(state)
    assert manhattan(move, Position(6, 6)) < manhattan(state.thief, Position(6, 6))


def test_thief_evades_when_target_unreachable(config_dict: Factory) -> None:
    # thief adjacent to police; target is the police cell (blocked) -> evade.
    state = _game(config_dict, board={"police_start": [0, 0], "thief_start": [0, 1]})
    brain = HeuristicThief(target=Position(0, 0))
    move = brain._pick_move(state)
    assert move != state.police
    assert manhattan(move, state.police) > manhattan(state.thief, state.police)


def test_runner_reaches_survival_when_nobody_catches(config_dict: Factory) -> None:
    class StayThief(HeuristicThief):
        def _pick_move(self, state: Any) -> Position:
            return state.thief

    state = _game(config_dict)
    final = play_with_strategies(state, StayPolice(), StayThief())
    assert final.outcome is Outcome.THIEF_SURVIVAL
    assert final.steps_completed == 35
