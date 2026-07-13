"""Shortest-path (BFS) tests for the blind strategy core."""

from __future__ import annotations

from anrbj666_thief.game.board import Board
from anrbj666_thief.game.geometry import Position
from anrbj666_thief.strategy.pathfinding import (
    bfs_path,
    next_step_toward,
    shortest_path_length,
)


def test_straight_path_length_is_manhattan_on_empty_board() -> None:
    board = Board(size=7)
    assert shortest_path_length(board, Position(0, 0), Position(3, 3)) == 6


def test_path_endpoints_and_contiguity() -> None:
    board = Board(size=7)
    path = bfs_path(board, Position(0, 0), Position(0, 3))
    assert path is not None
    assert path[0] == Position(0, 0)
    assert path[-1] == Position(0, 3)
    for a, b in zip(path, path[1:], strict=False):
        assert abs(a.row - b.row) + abs(a.col - b.col) == 1


def test_same_start_and_goal() -> None:
    board = Board(size=7)
    assert bfs_path(board, Position(2, 2), Position(2, 2)) == [Position(2, 2)]
    assert shortest_path_length(board, Position(2, 2), Position(2, 2)) == 0
    assert next_step_toward(board, Position(2, 2), Position(2, 2)) == Position(2, 2)


def test_barrier_forces_detour() -> None:
    board = Board(size=7)
    for r in range(6):
        board = board.with_barrier(Position(r, 1))
    length = shortest_path_length(board, Position(0, 0), Position(0, 2))
    assert length is not None and length > 2


def test_no_path_returns_none() -> None:
    board = Board(size=7)
    for r in range(7):
        board = board.with_barrier(Position(r, 1))
    assert bfs_path(board, Position(0, 0), Position(0, 2)) is None
    assert shortest_path_length(board, Position(0, 0), Position(0, 2)) is None
    assert next_step_toward(board, Position(0, 0), Position(0, 2)) == Position(0, 0)


def test_goal_on_barrier_is_unreachable() -> None:
    board = Board(size=7).with_barrier(Position(2, 2))
    assert bfs_path(board, Position(0, 0), Position(2, 2)) is None


def test_next_step_is_on_shortest_path() -> None:
    board = Board(size=7)
    step = next_step_toward(board, Position(0, 0), Position(0, 3))
    assert step == Position(0, 1)


def test_blocked_cell_is_avoided() -> None:
    board = Board(size=7)
    step = next_step_toward(
        board, Position(0, 0), Position(0, 2), blocked=(Position(0, 1),)
    )
    assert step == Position(1, 0)
