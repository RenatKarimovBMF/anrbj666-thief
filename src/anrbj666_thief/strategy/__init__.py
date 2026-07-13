"""Stage 3 "blind" strategy: deterministic decision core, no scent/language/LLM.

The strategy computes the shortest legal path toward a **known** target cell and
executes one step per turn (Appendix F T22 pluggable brains). "Blind" means it
does not yet infer the opponent from scent or dialogue - it is handed the target.
Stage 4 replaces the ground-truth target with a belief estimate; the LLM never
decides moves (Rule 25). The thief never places barriers.
"""

from anrbj666_thief.strategy.action import Action
from anrbj666_thief.strategy.base import PoliceBrain, ThiefBrain
from anrbj666_thief.strategy.heuristic import HeuristicThief
from anrbj666_thief.strategy.pathfinding import (
    bfs_path,
    next_step_toward,
    shortest_path_length,
)
from anrbj666_thief.strategy.runner import play_with_strategies

__all__ = [
    "Action",
    "HeuristicThief",
    "PoliceBrain",
    "ThiefBrain",
    "bfs_path",
    "next_step_toward",
    "play_with_strategies",
    "shortest_path_length",
]
