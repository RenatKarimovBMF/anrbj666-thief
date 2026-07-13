"""Receiver-side state for incoming geometric messages.

The inbox is deliberately tiny in Stage 2: it records validated peer messages so
a receiving peer can confirm "received & parsed correctly". Later stages route
these into the orchestrator/state machine and belief model.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from anrbj666_thief.mcp.messages import GeometricMessage


@dataclass
class Inbox:
    role: str
    messages: list[GeometricMessage] = field(default_factory=list)

    def receive(self, message: GeometricMessage) -> int:
        """Append a validated message; return the new message count."""
        self.messages.append(message)
        return len(self.messages)

    @property
    def last(self) -> GeometricMessage | None:
        return self.messages[-1] if self.messages else None
