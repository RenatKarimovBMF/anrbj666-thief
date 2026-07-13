"""Low-level validation primitives for the Appendix F shared-config contract.

Small, reusable checks used by :mod:`anrbj666_thief.config.loader`. Each raises
:class:`ConfigError` with a human-readable, field-qualified message so a peer can
report exactly which contract rule a configuration violated.
"""

from __future__ import annotations

import math
from typing import Any


class ConfigError(ValueError):
    """Raised when a shared configuration violates the Appendix F contract."""


def as_int(value: Any, ctx: str) -> int:
    """Return *value* as an int, rejecting bools and non-integers."""
    if isinstance(value, bool) or not isinstance(value, int):
        raise ConfigError(f"{ctx}: expected an integer, got {value!r}")
    return value


def require_min(ctx: str, value: int, bound: int) -> None:
    if value < bound:
        raise ConfigError(f"{ctx}: {value} is below the minimum {bound}")


def require_const(ctx: str, value: int, expected: int) -> None:
    if value != expected:
        raise ConfigError(f"{ctx}: must equal {expected} (CONSTANT), got {value}")


def require_fconst(ctx: str, value: float, expected: float) -> None:
    if not math.isclose(value, expected, abs_tol=1e-9):
        raise ConfigError(f"{ctx}: must equal {expected} (CONSTANT), got {value}")


def require_keys(data: dict[str, Any], keys: set[str], ctx: str) -> None:
    missing = keys - data.keys()
    if missing:
        raise ConfigError(f"{ctx}: missing required keys {sorted(missing)}")


def reject_unknown(data: dict[str, Any], allowed: set[str], ctx: str) -> None:
    if not isinstance(data, dict):
        raise ConfigError(f"{ctx}: expected an object")
    extra = data.keys() - allowed
    if extra:
        raise ConfigError(f"{ctx}: unknown keys {sorted(extra)}")
