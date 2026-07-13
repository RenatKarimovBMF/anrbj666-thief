"""Movement and barrier-placement rule tests."""

from __future__ import annotations

import pytest

from anrbj666_thief.game.board import Board
from anrbj666_thief.game.geometry import Position
from anrbj666_thief.game.rules import (
    MoveError,
    apply_move,
    can_place_barrier,
    is_legal_move,
    legal_moves,
)


def test_legal_moves_include_stay_and_four_steps() -> None:
    board = Board(size=7)
    moves = legal_moves(board, Position(3, 3))
    assert Position(3, 3) in moves  # stay
    assert len(moves) == 5


def test_legal_moves_respect_boundary() -> None:
    board = Board(size=7)
    moves = legal_moves(board, Position(0, 0))
    assert Position(-1, 0) not in moves
    assert Position(0, -1) not in moves
    assert len(moves) == 3  # stay + down + right


def test_legal_moves_blocked_by_barrier_and_occupancy() -> None:
    board = Board(size=7).with_barrier(Position(2, 3))
    moves = legal_moves(board, Position(3, 3), blocked=(Position(4, 3),))
    assert Position(2, 3) not in moves  # barrier
    assert Position(4, 3) not in moves  # occupied
    assert Position(3, 2) in moves


def test_diagonal_move_is_illegal() -> None:
    board = Board(size=7)
    assert not is_legal_move(board, Position(3, 3), Position(4, 4))


def test_two_step_move_is_illegal() -> None:
    board = Board(size=7)
    assert not is_legal_move(board, Position(3, 3), Position(3, 5))


def test_stay_can_be_disallowed() -> None:
    board = Board(size=7)
    assert not is_legal_move(board, Position(3, 3), Position(3, 3),
                             allow_stay=False)


def test_apply_move_rejects_illegal() -> None:
    board = Board(size=7)
    with pytest.raises(MoveError):
        apply_move(board, Position(3, 3), Position(5, 5))


def test_apply_move_returns_destination() -> None:
    board = Board(size=7)
    assert apply_move(board, Position(3, 3), Position(3, 4)) == Position(3, 4)


def test_barrier_within_quota_allowed() -> None:
    board = Board(size=7)
    assert can_place_barrier(board, Position(2, 2), placed_count=0, quota=14)


def test_barrier_over_quota_rejected() -> None:
    board = Board(size=7)
    assert not can_place_barrier(board, Position(2, 2), placed_count=14, quota=14)


def test_barrier_on_existing_barrier_rejected() -> None:
    board = Board(size=7).with_barrier(Position(2, 2))
    assert not can_place_barrier(board, Position(2, 2), placed_count=1, quota=14)


def test_barrier_off_board_rejected() -> None:
    board = Board(size=7)
    assert not can_place_barrier(board, Position(7, 7), placed_count=0, quota=14)


def test_barrier_on_occupied_cell_rejected() -> None:
    board = Board(size=7)
    assert not can_place_barrier(
        board, Position(0, 0), placed_count=0, quota=14,
        occupied=(Position(0, 0),),
    )
