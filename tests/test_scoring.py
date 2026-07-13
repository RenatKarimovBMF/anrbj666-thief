"""Termination and scoring tests (independent max_steps / survival_threshold)."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

import pytest

from anrbj666_thief.config import build_config
from anrbj666_thief.game.scoring import Outcome, check_termination, score_game

Factory = Callable[[], dict[str, Any]]


def test_capture_outcome_takes_precedence() -> None:
    assert check_termination(10, captured=True, max_steps=35,
                             survival_threshold=35) is Outcome.POLICE_CAPTURE


def test_survival_win_at_threshold() -> None:
    assert check_termination(35, captured=False, max_steps=35,
                             survival_threshold=35) is Outcome.THIEF_SURVIVAL


def test_ongoing_before_thresholds() -> None:
    assert check_termination(34, captured=False, max_steps=35,
                             survival_threshold=35) is Outcome.ONGOING


def test_independent_survival_before_ceiling() -> None:
    # survival_threshold reached before the (larger) step ceiling.
    assert check_termination(35, captured=False, max_steps=50,
                             survival_threshold=35) is Outcome.THIEF_SURVIVAL
    assert check_termination(34, captured=False, max_steps=50,
                             survival_threshold=35) is Outcome.ONGOING


def test_independent_ceiling_before_survival() -> None:
    # Unusual negotiated case: ceiling lower than survival threshold.
    assert check_termination(40, captured=False, max_steps=40,
                             survival_threshold=45) is Outcome.THIEF_SURVIVAL


def test_score_capture(config_dict: Factory) -> None:
    cfg = build_config(config_dict())
    assert score_game(Outcome.POLICE_CAPTURE, cfg.scoring) == (20, 5)


def test_score_survival(config_dict: Factory) -> None:
    cfg = build_config(config_dict())
    assert score_game(Outcome.THIEF_SURVIVAL, cfg.scoring) == (5, 10)


def test_cannot_score_ongoing(config_dict: Factory) -> None:
    cfg = build_config(config_dict())
    with pytest.raises(ValueError, match="ongoing"):
        score_game(Outcome.ONGOING, cfg.scoring)
