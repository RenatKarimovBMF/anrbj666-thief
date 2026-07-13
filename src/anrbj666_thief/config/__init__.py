"""Configuration loading and validation for the thief peer.

Public shared contract (``shared_config``) values and their
CONSTANT / MINIMUM / NEGOTIABLE status derive solely from Appendix F of
``police_thief_p2p.pdf`` v3.0.0. Nothing here decides moves or talks to peers.
"""

from anrbj666_thief.config.loader import ConfigError, build_config, load_config
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

__all__ = [
    "BoardConfig",
    "ConfigError",
    "GameConfig",
    "LeagueConfig",
    "MovementConfig",
    "NetworkConfig",
    "ScentConfig",
    "ScoringConfig",
    "VerbalConfig",
    "build_config",
    "load_config",
]
