"""Geometric message contract tests (Stage 2 numeric scaffold).

The numeric-coordinate channel here is the Stage-2 transport scaffold; Stage 4
replaces/wraps it with free-language dialogue (Rule 27). These tests pin the
wire format and validation so both peers parse each other deterministically.
"""

from __future__ import annotations

import pytest

from anrbj666_thief.mcp.messages import (
    GeometricMessage,
    MessageKind,
    ProtocolError,
    parse_geometric,
)


def _msg() -> GeometricMessage:
    return GeometricMessage(
        game_id="G1", sender_role="police", step=3,
        kind=MessageKind.POSITION, row=2, col=5,
    )


def test_wire_round_trip() -> None:
    msg = _msg()
    parsed = parse_geometric(msg.to_wire())
    assert parsed == msg
    assert parsed.coordinate == (2, 5)


def test_canonical_json_is_sorted_and_deterministic() -> None:
    msg = _msg()
    assert msg.canonical_json() == msg.canonical_json()
    assert msg.canonical_json() == (
        '{"col":5,"game_id":"G1","kind":"position","row":2,'
        '"sender_role":"police","step":3}'
    )


def test_kind_move_round_trip() -> None:
    msg = GeometricMessage("G1", "thief", 0, MessageKind.MOVE, 0, 0)
    assert parse_geometric(msg.to_wire()).kind is MessageKind.MOVE


def test_missing_key_rejected() -> None:
    data = _msg().to_wire()
    del data["row"]
    with pytest.raises(ProtocolError, match="missing"):
        parse_geometric(data)


def test_unknown_key_rejected() -> None:
    data = _msg().to_wire()
    data["extra"] = 1
    with pytest.raises(ProtocolError, match="unknown"):
        parse_geometric(data)


def test_bad_role_rejected() -> None:
    data = _msg().to_wire()
    data["sender_role"] = "referee"
    with pytest.raises(ProtocolError, match="sender_role"):
        parse_geometric(data)


def test_bad_kind_rejected() -> None:
    data = _msg().to_wire()
    data["kind"] = "teleport"
    with pytest.raises(ProtocolError, match="kind"):
        parse_geometric(data)


def test_negative_step_rejected() -> None:
    data = _msg().to_wire()
    data["step"] = -1
    with pytest.raises(ProtocolError, match="step"):
        parse_geometric(data)


def test_non_int_coordinate_rejected() -> None:
    data = _msg().to_wire()
    data["row"] = "2"
    with pytest.raises(ProtocolError, match="row"):
        parse_geometric(data)


def test_bool_not_accepted_as_coordinate() -> None:
    data = _msg().to_wire()
    data["col"] = True
    with pytest.raises(ProtocolError, match="col"):
        parse_geometric(data)


def test_out_of_bounds_rejected_when_board_size_given() -> None:
    data = _msg().to_wire()
    data["row"] = 7
    with pytest.raises(ProtocolError, match="board"):
        parse_geometric(data, board_size=7)


def test_in_bounds_ok_when_board_size_given() -> None:
    parsed = parse_geometric(_msg().to_wire(), board_size=7)
    assert parsed.coordinate == (2, 5)


def test_non_object_rejected() -> None:
    with pytest.raises(ProtocolError, match="object"):
        parse_geometric([1, 2])  # type: ignore[arg-type]
