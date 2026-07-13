"""Immutable typed model of the public shared match configuration.

Field names and grouping mirror ``config/shared_config.schema.json`` byte-for-byte
so both peers interpret the crypto-locked contract identically. Values originate
from Appendix F (Tables 13-19). This module only *describes* the data; semantic
validation lives in :mod:`anrbj666_thief.config.loader`.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class BoardConfig:
    size: int
    num_agents: int
    axis_origin: str
    axis_start_index: int
    thief_start: tuple[int, int]
    police_start: tuple[int, int]


@dataclass(frozen=True)
class MovementConfig:
    set: str
    barrier_quota: int
    # NOTE (C-002 / D-007): max_steps and survival_threshold are INDEPENDENT.
    # They default-equal (35) but are never derived from or asserted equal to
    # one another; each is validated against its own MINIMUM separately.
    max_steps: int
    survival_threshold: int


@dataclass(frozen=True)
class ScentConfig:
    source_strength: float
    decay_rate: float
    field_size: int


@dataclass(frozen=True)
class ScoringConfig:
    capture_police: int
    capture_thief: int
    survival_police: int
    survival_thief: int
    tie: int


@dataclass(frozen=True)
class LeagueConfig:
    sub_games: int
    variety_reward: int
    min_games_to_pass: int
    max_games_per_group: int


@dataclass(frozen=True)
class VerbalConfig:
    arena: str = ""
    hint_word_limit: int = 15


@dataclass(frozen=True)
class NetworkConfig:
    requests_per_minute: int
    parallel_requests: int
    retry_delay_s: int
    retry_attempts: int
    queue_depth: int
    response_timeout_s: int
    watchdog_timeout_s: int


@dataclass(frozen=True)
class GameConfig:
    config_version: str
    game_id: str
    board: BoardConfig
    movement: MovementConfig
    scent: ScentConfig
    scoring: ScoringConfig
    league: LeagueConfig
    network: NetworkConfig
    verbal: VerbalConfig
