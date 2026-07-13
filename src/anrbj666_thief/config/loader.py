"""Load and validate the public shared match configuration.

Validation enforces the CONSTANT / MINIMUM / NEGOTIABLE semantics from Appendix F.
CONSTANT fields must equal the authoritative value; MINIMUM fields must be at least
the bound; NEGOTIABLE fields are range-checked only. Unknown keys are rejected so
the two peers can never silently disagree about the contract. Low-level primitives
live in :mod:`anrbj666_thief.config.checks`.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from anrbj666_thief.config.checks import (
    ConfigError,
    as_int,
    reject_unknown,
    require_const,
    require_fconst,
    require_keys,
    require_min,
)
from anrbj666_thief.config.model import (
    BoardConfig,
    GameConfig,
    LeagueConfig,
    MovementConfig,
    NetworkConfig,
    ScentConfig,
    ScoringConfig,
    VerbalConfig,
)

__all__ = ["ConfigError", "build_config", "load_config"]

_SECTION_KEYS = {
    "board": {"size", "num_agents", "axis_origin", "axis_start_index",
              "thief_start", "police_start"},
    "movement": {"set", "barrier_quota", "max_steps", "survival_threshold"},
    "scent": {"source_strength", "decay_rate", "field_size"},
    "scoring": {"capture_police", "capture_thief", "survival_police",
                "survival_thief", "tie"},
    "league": {"sub_games", "variety_reward", "min_games_to_pass",
               "max_games_per_group"},
    "network": {"requests_per_minute", "parallel_requests", "retry_delay_s",
                "retry_attempts", "queue_depth", "response_timeout_s",
                "watchdog_timeout_s"},
}
_TOP_REQUIRED = {"config_version", "game_id", "board", "movement", "scent",
                 "scoring", "league", "network"}
_TOP_OPTIONAL = {"verbal"}


def load_config(path: str | Path) -> GameConfig:
    """Read a JSON shared-config file from *path* and validate it."""
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return build_config(data)


def build_config(data: dict[str, Any]) -> GameConfig:
    """Build and validate a :class:`GameConfig` from a parsed dict."""
    if not isinstance(data, dict):
        raise ConfigError("shared config must be a JSON object")
    extra = data.keys() - _TOP_REQUIRED - _TOP_OPTIONAL
    if extra:
        raise ConfigError(f"config: unknown keys {sorted(extra)}")
    require_keys(data, _TOP_REQUIRED, "config")
    for section in _SECTION_KEYS:
        reject_unknown(data[section], _SECTION_KEYS[section], section)
    return GameConfig(
        config_version=str(data["config_version"]),
        game_id=str(data["game_id"]),
        board=_build_board(data["board"]),
        movement=_build_movement(data["movement"]),
        scent=_build_scent(data["scent"]),
        scoring=_build_scoring(data["scoring"]),
        league=_build_league(data["league"]),
        network=_build_network(data["network"]),
        verbal=_build_verbal(data.get("verbal", {})),
    )


def _build_board(d: dict[str, Any]) -> BoardConfig:
    size = as_int(d["size"], "board.size")
    require_min("board.size", size, 7)  # Appendix F T13#1 MINIMUM
    require_const("board.num_agents", as_int(d["num_agents"], "board.num_agents"), 2)
    if d["axis_origin"] != "top-left":
        raise ConfigError("board.axis_origin: only 'top-left' is supported")
    start_index = as_int(d["axis_start_index"], "board.axis_start_index")
    require_min("board.axis_start_index", start_index, 0)
    thief = _coord(d["thief_start"], "board.thief_start", size)
    police = _coord(d["police_start"], "board.police_start", size)
    if thief == police:
        raise ConfigError("board: thief_start and police_start must differ")
    return BoardConfig(
        size=size, num_agents=2, axis_origin="top-left",
        axis_start_index=start_index, thief_start=thief, police_start=police,
    )


def _build_movement(d: dict[str, Any]) -> MovementConfig:
    if d["set"] != "orthogonal4_plus_stay":
        raise ConfigError("movement.set: must be 'orthogonal4_plus_stay'")
    quota = as_int(d["barrier_quota"], "movement.barrier_quota")
    require_min("movement.barrier_quota", quota, 14)
    max_steps = as_int(d["max_steps"], "movement.max_steps")
    survival = as_int(d["survival_threshold"], "movement.survival_threshold")
    # C-002 / D-007: validate each independently; never compare to each other.
    require_min("movement.max_steps", max_steps, 35)
    require_min("movement.survival_threshold", survival, 35)
    return MovementConfig("orthogonal4_plus_stay", quota, max_steps, survival)


def _build_scent(d: dict[str, Any]) -> ScentConfig:
    require_fconst("scent.source_strength", float(d["source_strength"]), 0.9)
    require_fconst("scent.decay_rate", float(d["decay_rate"]), 0.10)
    require_const("scent.field_size", as_int(d["field_size"], "scent.field_size"), 5)
    return ScentConfig(0.9, 0.10, 5)


def _build_scoring(d: dict[str, Any]) -> ScoringConfig:
    vals = {k: as_int(d[k], f"scoring.{k}") for k in _SECTION_KEYS["scoring"]}
    for key, expected in (("capture_police", 20), ("capture_thief", 5),
                          ("survival_police", 5), ("survival_thief", 10),
                          ("tie", 2)):
        require_const(f"scoring.{key}", vals[key], expected)
    return ScoringConfig(20, 5, 5, 10, 2)


def _build_league(d: dict[str, Any]) -> LeagueConfig:
    vals = {k: as_int(d[k], f"league.{k}") for k in _SECTION_KEYS["league"]}
    for key, expected in (("sub_games", 6), ("variety_reward", 10),
                          ("min_games_to_pass", 2), ("max_games_per_group", 10)):
        require_const(f"league.{key}", vals[key], expected)
    return LeagueConfig(6, 10, 2, 10)


def _build_network(d: dict[str, Any]) -> NetworkConfig:
    v = {k: as_int(d[k], f"network.{k}") for k in _SECTION_KEYS["network"]}
    for key, bound in (("requests_per_minute", 30), ("parallel_requests", 2),
                       ("retry_delay_s", 5), ("retry_attempts", 3),
                       ("queue_depth", 100), ("response_timeout_s", 30),
                       ("watchdog_timeout_s", 60)):
        require_min(f"network.{key}", v[key], bound)
    return NetworkConfig(v["requests_per_minute"], v["parallel_requests"],
                         v["retry_delay_s"], v["retry_attempts"],
                         v["queue_depth"], v["response_timeout_s"],
                         v["watchdog_timeout_s"])


def _build_verbal(d: dict[str, Any]) -> VerbalConfig:
    reject_unknown(d, {"arena", "hint_word_limit"}, "verbal")
    arena = str(d.get("arena", ""))
    limit = as_int(d.get("hint_word_limit", 15), "verbal.hint_word_limit")
    require_min("verbal.hint_word_limit", limit, 15)
    return VerbalConfig(arena=arena, hint_word_limit=limit)


def _coord(value: Any, ctx: str, size: int) -> tuple[int, int]:
    if not isinstance(value, (list, tuple)) or len(value) != 2:
        raise ConfigError(f"{ctx}: must be a [row, col] pair")
    row, col = as_int(value[0], ctx), as_int(value[1], ctx)
    if not (0 <= row < size and 0 <= col < size):
        raise ConfigError(f"{ctx}: {value} is outside the {size}x{size} board")
    return (row, col)
