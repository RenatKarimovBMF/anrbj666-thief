"""Stage 1 base game logic: geometry, board, movement rules, capture, scoring.

Single-process, deterministic, no networking / AI / cryptography. These modules
implement the public rules (Appendix E) so the thief peer can validate every move
locally and recognise capture / survival; the strategy that *chooses* moves
arrives in Stage 3. The thief itself never places barriers, but it models them to
detect capture-by-barrier and being trapped.
"""

from anrbj666_thief.game.board import Board
from anrbj666_thief.game.capture import CaptureReason, capture_reason, is_captured
from anrbj666_thief.game.engine import GameState, new_game, play_round
from anrbj666_thief.game.geometry import (
    STEP_DELTAS,
    Position,
    in_bounds,
    neighbors,
)
from anrbj666_thief.game.rules import (
    MoveError,
    can_place_barrier,
    is_legal_move,
    legal_moves,
)
from anrbj666_thief.game.scoring import Outcome, check_termination, score_game

__all__ = [
    "STEP_DELTAS",
    "Board",
    "CaptureReason",
    "GameState",
    "MoveError",
    "Outcome",
    "Position",
    "can_place_barrier",
    "capture_reason",
    "check_termination",
    "in_bounds",
    "is_captured",
    "is_legal_move",
    "legal_moves",
    "neighbors",
    "new_game",
    "play_round",
    "score_game",
]
