"""Single-game termination and scoring (Appendix E Rule 48, Appendix F T17).

Termination checks capture, the thief survival threshold, and the step ceiling as
three INDEPENDENT conditions (see C-002 / D-007): ``survival_threshold`` and
``max_steps`` are never coupled. With the default-equal values (35/35) the
survival win and the ceiling coincide, but each is evaluated on its own.
"""

from __future__ import annotations

from enum import Enum

from anrbj666_thief.config.model import ScoringConfig


class Outcome(str, Enum):
    ONGOING = "ongoing"
    POLICE_CAPTURE = "police_capture"
    THIEF_SURVIVAL = "thief_survival"


def check_termination(
    steps_completed: int,
    captured: bool,
    max_steps: int,
    survival_threshold: int,
) -> Outcome:
    """Return the outcome after *steps_completed* full rounds.

    ``max_steps`` and ``survival_threshold`` are consulted independently. If the
    thief is not captured and either the survival threshold or the step ceiling
    has been reached, the thief wins by survival.
    """
    if captured:
        return Outcome.POLICE_CAPTURE
    if steps_completed >= survival_threshold:
        return Outcome.THIEF_SURVIVAL
    if steps_completed >= max_steps:
        return Outcome.THIEF_SURVIVAL
    return Outcome.ONGOING


def score_game(outcome: Outcome, scoring: ScoringConfig) -> tuple[int, int]:
    """Return ``(police_points, thief_points)`` for a finished single game."""
    if outcome is Outcome.POLICE_CAPTURE:
        return (scoring.capture_police, scoring.capture_thief)
    if outcome is Outcome.THIEF_SURVIVAL:
        return (scoring.survival_police, scoring.survival_thief)
    raise ValueError("cannot score an ongoing game")
