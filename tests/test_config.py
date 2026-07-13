"""Config loading and Appendix F validation tests."""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path
from typing import Any

import pytest

from anrbj666_thief.config import ConfigError, build_config, load_config

Factory = Callable[[], dict[str, Any]]

EXAMPLE_CONFIG = (
    Path(__file__).resolve().parents[1] / "config" / "shared_config.example.json"
)


def test_valid_config_builds(config_dict: Factory) -> None:
    cfg = build_config(config_dict())
    assert cfg.board.size == 7
    assert cfg.movement.set == "orthogonal4_plus_stay"
    assert cfg.scoring.capture_police == 20
    assert cfg.board.thief_start == (3, 3)


def test_shipped_example_is_valid() -> None:
    cfg = load_config(EXAMPLE_CONFIG)
    assert cfg.board.num_agents == 2
    assert cfg.movement.max_steps == 35


def test_max_steps_and_survival_are_independent(config_dict: Factory) -> None:
    # C-002 / D-007: unequal but individually valid values must be accepted.
    data = config_dict()
    data["movement"]["max_steps"] = 50
    data["movement"]["survival_threshold"] = 35
    cfg = build_config(data)
    assert cfg.movement.max_steps == 50
    assert cfg.movement.survival_threshold == 35


def test_survival_threshold_validated_independently(config_dict: Factory) -> None:
    data = config_dict()
    data["movement"]["max_steps"] = 40  # valid
    data["movement"]["survival_threshold"] = 34  # below its own minimum
    with pytest.raises(ConfigError, match="survival_threshold"):
        build_config(data)


@pytest.mark.parametrize(
    ("section", "key", "value"),
    [
        ("board", "size", 6),
        ("movement", "barrier_quota", 13),
        ("movement", "max_steps", 34),
        ("network", "requests_per_minute", 29),
        ("verbal", "hint_word_limit", 14),
    ],
)
def test_minimum_violations_rejected(
    config_dict: Factory, section: str, key: str, value: int
) -> None:
    data = config_dict()
    data[section][key] = value
    with pytest.raises(ConfigError, match="minimum"):
        build_config(data)


@pytest.mark.parametrize(
    ("section", "key", "value"),
    [
        ("board", "num_agents", 3),
        ("scoring", "capture_police", 19),
        ("scoring", "tie", 3),
        ("league", "sub_games", 5),
        ("scent", "field_size", 4),
    ],
)
def test_constant_violations_rejected(
    config_dict: Factory, section: str, key: str, value: int
) -> None:
    data = config_dict()
    data[section][key] = value
    with pytest.raises(ConfigError, match="CONSTANT"):
        build_config(data)


def test_float_constant_violation(config_dict: Factory) -> None:
    data = config_dict()
    data["scent"]["decay_rate"] = 0.2
    with pytest.raises(ConfigError, match="CONSTANT"):
        build_config(data)


def test_unknown_top_level_key_rejected(config_dict: Factory) -> None:
    data = config_dict()
    data["surprise"] = True
    with pytest.raises(ConfigError, match="unknown keys"):
        build_config(data)


def test_unknown_section_key_rejected(config_dict: Factory) -> None:
    data = config_dict()
    data["board"]["extra"] = 1
    with pytest.raises(ConfigError, match="unknown keys"):
        build_config(data)


def test_missing_required_section_rejected(config_dict: Factory) -> None:
    data = config_dict()
    del data["scoring"]
    with pytest.raises(ConfigError, match="missing required keys"):
        build_config(data)


def test_start_position_out_of_bounds(config_dict: Factory) -> None:
    data = config_dict()
    data["board"]["thief_start"] = [7, 0]
    with pytest.raises(ConfigError, match="outside"):
        build_config(data)


def test_start_positions_must_differ(config_dict: Factory) -> None:
    data = config_dict()
    data["board"]["police_start"] = [3, 3]
    with pytest.raises(ConfigError, match="must differ"):
        build_config(data)


def test_bad_movement_set(config_dict: Factory) -> None:
    data = config_dict()
    data["movement"]["set"] = "kings_move"
    with pytest.raises(ConfigError, match="orthogonal4_plus_stay"):
        build_config(data)


def test_section_must_be_object(config_dict: Factory) -> None:
    data = config_dict()
    data["board"] = [1, 2, 3]
    with pytest.raises(ConfigError, match="expected an object"):
        build_config(data)


def test_bad_axis_origin(config_dict: Factory) -> None:
    data = config_dict()
    data["board"]["axis_origin"] = "bottom-right"
    with pytest.raises(ConfigError, match="axis_origin"):
        build_config(data)


def test_bad_coordinate_shape(config_dict: Factory) -> None:
    data = config_dict()
    data["board"]["thief_start"] = [3, 3, 3]
    with pytest.raises(ConfigError, match="row, col"):
        build_config(data)


def test_boolean_not_accepted_as_int(config_dict: Factory) -> None:
    data = config_dict()
    data["board"]["size"] = True
    with pytest.raises(ConfigError, match="integer"):
        build_config(data)


def test_non_object_rejected() -> None:
    with pytest.raises(ConfigError, match="JSON object"):
        build_config([])  # type: ignore[arg-type]


def test_verbal_defaults_when_absent(config_dict: Factory) -> None:
    data = config_dict()
    del data["verbal"]
    cfg = build_config(data)
    assert cfg.verbal.arena == ""
    assert cfg.verbal.hint_word_limit == 15
