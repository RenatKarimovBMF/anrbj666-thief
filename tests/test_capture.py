"""Capture detection tests (Rules 46-48)."""

from __future__ import annotations

from anrbj666_thief.game.board import Board
from anrbj666_thief.game.capture import (
    CaptureReason,
    capture_reason,
    is_captured,
)
from anrbj666_thief.game.geometry import Position


def test_overlap_capture() -> None:
    board = Board(size=7)
    assert capture_reason(board, Position(2, 2), Position(2, 2)) is (
        CaptureReason.OVERLAP
    )
    assert is_captured(board, Position(2, 2), Position(2, 2))


def test_barrier_on_thief_is_capture() -> None:
    board = Board(size=7).with_barrier(Position(4, 4))
    assert capture_reason(board, Position(0, 0), Position(4, 4)) is (
        CaptureReason.BARRIER
    )


def test_thief_trapped_by_barriers_is_capture() -> None:
    thief = Position(3, 3)
    board = Board(size=7)
    for n in (Position(2, 3), Position(4, 3), Position(3, 2), Position(3, 4)):
        board = board.with_barrier(n)
    assert capture_reason(board, Position(0, 0), thief) is CaptureReason.TRAPPED


def test_thief_trapped_in_corner_by_walls_and_police() -> None:
    # Corner (0,0): only exits are (1,0) and (0,1). Wall one, police blocks other.
    board = Board(size=7).with_barrier(Position(0, 1))
    assert capture_reason(board, Position(1, 0), Position(0, 0)) is (
        CaptureReason.TRAPPED
    )


def test_free_thief_not_captured() -> None:
    board = Board(size=7)
    assert capture_reason(board, Position(0, 0), Position(3, 3)) is None
    assert not is_captured(board, Position(0, 0), Position(3, 3))
