"""Thief peer package for the P2P Cops-and-Robbers final project.

Stage 1 (Base Logic) implemented: config loading/validation and single-process
game logic (geometry, board, movement rules, capture, scoring) under
:mod:`anrbj666_thief.config` and :mod:`anrbj666_thief.game`. The thief never
places barriers, but it models the full public rules locally so it can detect
capture (overlap, barrier-on-cell, trapped) and its own survival win. Networking,
strategy, scent, language, and cryptography arrive in later stages
(see docs/DEVELOPMENT_STAGES.md).
"""

__version__ = "0.1.0"
__role__ = "thief"
