"""Geometry primitive tests."""

from __future__ import annotations

from anrbj666_thief.game.geometry import (
    STEP_DELTAS,
    Position,
    in_bounds,
    manhattan,
    neighbors,
    translate,
)


def test_in_bounds() -> None:
    assert in_bounds(Position(0, 0), 7)
    assert in_bounds(Position(6, 6), 7)
    assert not in_bounds(Position(7, 0), 7)
    assert not in_bounds(Position(-1, 0), 7)


def test_no_diagonal_deltas() -> None:
    assert (1, 1) not in STEP_DELTAS
    assert len(STEP_DELTAS) == 4
    for dr, dc in STEP_DELTAS:
        assert abs(dr) + abs(dc) == 1


def test_neighbors_are_orthogonal() -> None:
    ns = neighbors(Position(3, 3))
    assert set(ns) == {
        Position(2, 3),
        Position(4, 3),
        Position(3, 2),
        Position(3, 4),
    }


def test_translate_and_manhattan() -> None:
    assert translate(Position(1, 1), (0, 1)) == Position(1, 2)
    assert manhattan(Position(0, 0), Position(3, 4)) == 7
