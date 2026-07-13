"""Board state tests."""

from __future__ import annotations

from anrbj666_thief.game.board import Board
from anrbj666_thief.game.geometry import Position


def test_free_inside_and_barrier() -> None:
    board = Board(size=7)
    assert board.is_inside(Position(6, 6))
    assert not board.is_inside(Position(7, 0))
    assert board.is_free(Position(3, 3))


def test_with_barrier_is_immutable() -> None:
    board = Board(size=7)
    updated = board.with_barrier(Position(2, 2))
    assert Position(2, 2) not in board.barriers  # original unchanged
    assert updated.is_barrier(Position(2, 2))
    assert not updated.is_free(Position(2, 2))


def test_barrier_off_board_is_not_free() -> None:
    board = Board(size=7)
    assert not board.is_free(Position(-1, 0))
