"""Single-process Stage 1 game driver.

Ties board + rules + capture + scoring into a deterministic round loop with no
networking, strategy, or AI (those arrive in later stages). Turn order is
police-first: the police may move and optionally place one barrier, then the
thief moves; capture is checked after each action. This driver only *validates
and applies* externally supplied actions - it never decides them. The thief peer
uses it to reason about the shared rules locally.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from anrbj666_thief.config.model import GameConfig
from anrbj666_thief.game.board import Board
from anrbj666_thief.game.capture import CaptureReason, capture_reason
from anrbj666_thief.game.geometry import Position
from anrbj666_thief.game.rules import MoveError, apply_move, can_place_barrier
from anrbj666_thief.game.scoring import Outcome, check_termination


@dataclass
class GameState:
    config: GameConfig
    board: Board
    police: Position
    thief: Position
    steps_completed: int = 0
    barriers_placed: int = 0
    outcome: Outcome = Outcome.ONGOING
    capture_reason: CaptureReason | None = None
    history: list[str] = field(default_factory=list)

    @property
    def finished(self) -> bool:
        return self.outcome is not Outcome.ONGOING


def new_game(config: GameConfig) -> GameState:
    """Create the initial state from the shared config's start positions."""
    return GameState(
        config=config,
        board=Board(size=config.board.size),
        police=Position(*config.board.police_start),
        thief=Position(*config.board.thief_start),
    )


def _settle_capture(state: GameState) -> bool:
    reason = capture_reason(state.board, state.police, state.thief)
    if reason is not None:
        state.outcome = Outcome.POLICE_CAPTURE
        state.capture_reason = reason
        state.history.append(f"capture:{reason.value}")
    return state.finished


def play_round(
    state: GameState,
    police_to: Position,
    thief_to: Position,
    barrier_at: Position | None = None,
) -> GameState:
    """Apply one full police-then-thief round in place and return *state*.

    Raises :class:`MoveError` on an illegal move or an illegal / over-quota
    barrier placement. The round only advances the step counter and evaluates
    termination once both agents have acted and no capture occurred earlier.
    """
    if state.finished:
        raise MoveError("game already finished")

    # --- Police move. Stepping onto the thief's cell IS the overlap capture
    # (Rule 48), so the thief cell is intentionally not blocked here. ---
    state.police = apply_move(state.board, state.police, police_to)

    # --- Optional barrier placement. ---
    if barrier_at is not None:
        capture_on_thief = barrier_at == state.thief
        if not capture_on_thief and not can_place_barrier(
            state.board, barrier_at, state.barriers_placed,
            state.config.movement.barrier_quota, occupied=(state.police,),
        ):
            raise MoveError(f"illegal barrier at {barrier_at}")
        if capture_on_thief and state.barriers_placed >= (
            state.config.movement.barrier_quota
        ):
            raise MoveError("barrier quota exhausted")
        state.board = state.board.with_barrier(barrier_at)
        state.barriers_placed += 1

    if _settle_capture(state):
        return state

    # --- Thief move. Moving onto the police cell is also an overlap capture;
    # the engine applies the supplied action and lets capture detection decide. ---
    state.thief = apply_move(state.board, state.thief, thief_to)
    if _settle_capture(state):
        return state

    state.steps_completed += 1
    state.outcome = check_termination(
        state.steps_completed,
        captured=False,
        max_steps=state.config.movement.max_steps,
        survival_threshold=state.config.movement.survival_threshold,
    )
    return state
