"""End-to-end Stage 1 milestone tests for the single-process engine.

Milestone (DEVELOPMENT_STAGES.md Stage 1): two agents move legally on the grid;
an over-quota barrier is rejected; coordinate overlap triggers capture.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

import pytest

from anrbj666_thief.config import build_config
from anrbj666_thief.game.capture import CaptureReason
from anrbj666_thief.game.engine import new_game, play_round
from anrbj666_thief.game.geometry import Position
from anrbj666_thief.game.rules import MoveError
from anrbj666_thief.game.scoring import Outcome

Factory = Callable[[], dict[str, Any]]


def _game(config_dict: Factory, **overrides: Any):
    data = config_dict()
    for section, values in overrides.items():
        data[section].update(values)
    return new_game(build_config(data))


def test_new_game_uses_start_positions(config_dict: Factory) -> None:
    state = _game(config_dict)
    assert state.police == Position(0, 0)
    assert state.thief == Position(3, 3)
    assert state.outcome is Outcome.ONGOING


def test_agents_move_legally_and_step_advances(config_dict: Factory) -> None:
    state = _game(config_dict)
    play_round(state, police_to=Position(0, 1), thief_to=Position(3, 4))
    assert state.police == Position(0, 1)
    assert state.thief == Position(3, 4)
    assert state.steps_completed == 1
    assert state.outcome is Outcome.ONGOING


def test_illegal_police_move_raises(config_dict: Factory) -> None:
    state = _game(config_dict)
    with pytest.raises(MoveError):
        play_round(state, police_to=Position(2, 2), thief_to=Position(3, 4))


def test_over_quota_barrier_rejected(config_dict: Factory) -> None:
    state = _game(config_dict, movement={"barrier_quota": 14})
    state.barriers_placed = 14
    with pytest.raises(MoveError, match="barrier"):
        play_round(state, police_to=Position(0, 1), thief_to=Position(3, 4),
                   barrier_at=Position(5, 5))


def test_overlap_triggers_capture(config_dict: Factory) -> None:
    # Police adjacent to thief steps onto the thief's cell.
    state = _game(config_dict, board={"police_start": [3, 2]})
    play_round(state, police_to=Position(3, 3), thief_to=Position(3, 3))
    assert state.outcome is Outcome.POLICE_CAPTURE
    assert state.capture_reason is CaptureReason.OVERLAP
    assert state.finished


def test_barrier_on_thief_cell_captures(config_dict: Factory) -> None:
    state = _game(config_dict, board={"police_start": [2, 3]})
    # Police stays adjacent, drops a barrier on the thief's cell (Rule 46).
    play_round(state, police_to=Position(2, 3), thief_to=Position(3, 3),
               barrier_at=Position(3, 3))
    assert state.outcome is Outcome.POLICE_CAPTURE
    assert state.capture_reason is CaptureReason.BARRIER
    assert state.barriers_placed == 1


def test_barrier_on_thief_rejected_when_quota_exhausted(
    config_dict: Factory,
) -> None:
    state = _game(config_dict, board={"police_start": [2, 3]})
    state.barriers_placed = 14
    with pytest.raises(MoveError, match="quota exhausted"):
        play_round(state, police_to=Position(2, 3), thief_to=Position(3, 3),
                   barrier_at=Position(3, 3))


def test_thief_move_into_police_is_capture(config_dict: Factory) -> None:
    # Thief voluntarily steps onto the police cell -> overlap capture on the
    # thief's own move (exercises post-thief-move capture settling).
    state = _game(config_dict, board={"police_start": [3, 4]})
    play_round(state, police_to=Position(3, 4), thief_to=Position(3, 4))
    assert state.outcome is Outcome.POLICE_CAPTURE
    assert state.capture_reason is CaptureReason.OVERLAP


def test_legal_barrier_is_recorded(config_dict: Factory) -> None:
    state = _game(config_dict)
    play_round(state, police_to=Position(0, 1), thief_to=Position(3, 4),
               barrier_at=Position(5, 5))
    assert state.barriers_placed == 1
    assert state.board.is_barrier(Position(5, 5))
    assert state.steps_completed == 1


def test_cannot_play_finished_game(config_dict: Factory) -> None:
    state = _game(config_dict, board={"police_start": [3, 2]})
    play_round(state, police_to=Position(3, 3), thief_to=Position(3, 3))
    with pytest.raises(MoveError, match="finished"):
        play_round(state, police_to=Position(3, 3), thief_to=Position(3, 3))


def test_thief_survives_to_threshold(config_dict: Factory) -> None:
    state = _game(config_dict, movement={"max_steps": 35, "survival_threshold": 35})
    positions = [Position(3, 4), Position(3, 3)]
    for i in range(35):
        thief_to = positions[i % 2]
        play_round(state, police_to=Position(0, 0), thief_to=thief_to)
    assert state.steps_completed == 35
    assert state.outcome is Outcome.THIEF_SURVIVAL
