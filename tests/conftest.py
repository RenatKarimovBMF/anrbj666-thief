"""Shared pytest fixtures for the thief Stage 1 test suite."""

from __future__ import annotations

import copy
from collections.abc import Callable
from pathlib import Path
from typing import Any

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
EXAMPLE_CONFIG = REPO_ROOT / "config" / "shared_config.example.json"

_BASE_CONFIG: dict[str, Any] = {
    "config_version": "1.0.0",
    "game_id": "TEST-GAME",
    "board": {
        "size": 7,
        "num_agents": 2,
        "axis_origin": "top-left",
        "axis_start_index": 0,
        "thief_start": [3, 3],
        "police_start": [0, 0],
    },
    "movement": {
        "set": "orthogonal4_plus_stay",
        "barrier_quota": 14,
        "max_steps": 35,
        "survival_threshold": 35,
    },
    "scent": {"source_strength": 0.9, "decay_rate": 0.10, "field_size": 5},
    "scoring": {
        "capture_police": 20,
        "capture_thief": 5,
        "survival_police": 5,
        "survival_thief": 10,
        "tie": 2,
    },
    "league": {
        "sub_games": 6,
        "variety_reward": 10,
        "min_games_to_pass": 2,
        "max_games_per_group": 10,
    },
    "verbal": {"arena": "New York", "hint_word_limit": 15},
    "network": {
        "requests_per_minute": 30,
        "parallel_requests": 2,
        "retry_delay_s": 5,
        "retry_attempts": 3,
        "queue_depth": 100,
        "response_timeout_s": 30,
        "watchdog_timeout_s": 60,
    },
}


@pytest.fixture
def config_dict() -> Callable[[], dict[str, Any]]:
    """Return a factory yielding a fresh, valid shared-config dict each call."""
    return lambda: copy.deepcopy(_BASE_CONFIG)
