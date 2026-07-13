# anrbj666-thief

Thief peer for **"Distributed Cops-and-Robbers over a Peer-to-Peer Network"** —
University of Haifa, Orchestration of AI Agents, final project 2026.
Group code: **anrbj666**. Authors: **Alon** and **Renat**.

> This is the **thief** agent. It is an autonomous, independent peer. It never
> shares live memory or private state with the police peer. The two agents
> communicate only over the mandatory public FastMCP P2P protocol.

## Companion repository (mandatory cross-link)

- Police agent: https://github.com/RenatKarimovBMF/anrbj666-police

## Status

**Stage 0 — planning & scaffolding.** No game logic is implemented yet.
Development follows the seven official priorities from Chapter 10.3 of the
project book; see [`docs/DEVELOPMENT_STAGES.md`](docs/DEVELOPMENT_STAGES.md).

## Authoritative sources & priority

1. **Appendix F** (mandatory parameter tables) of `police_thief_p2p.pdf` v3.0.0 — the ONLY source of numerical values.
2. Mandatory rules in `police_thief_p2p.pdf` v3.0.0 (esp. Appendix E, Rules 1–55).
3. Course-site instructions.
4. Professional software submission guidelines (V3).
5. Example simulator code (illustrative only).
6. Earlier assignment feedback (quality guidance only).

Conflicts are logged in [`docs/REQUIREMENTS_CONFLICTS.md`](docs/REQUIREMENTS_CONFLICTS.md)
and never silently resolved.

## Planned tooling

- Python ≥ 3.10, [`uv`](https://docs.astral.sh/uv/) for env & locking, `pyproject.toml` + `uv.lock`.
- `ruff` (zero violations), `pytest` + `pytest-cov` (≥ 85% meaningful coverage).
- FastMCP for the P2P protocol; ngrok/localtonet for public exposure.
- Deterministic **template** LLM mode by default (game runs with zero external API calls).

## Quick start (will be fleshed out per stage)

```powershell
# Windows PowerShell
uv sync
uv run pytest
uv run ruff check .
```

## Documentation index

Planning: [PRD](docs/PRD.md) · [PLAN](docs/PLAN.md) · [TODO](docs/TODO.md) ·
[DEVELOPMENT_STAGES](docs/DEVELOPMENT_STAGES.md)
Requirements: [REQUIREMENTS_MATRIX](docs/REQUIREMENTS_MATRIX.md) ·
[REQUIREMENTS_CONFLICTS](docs/REQUIREMENTS_CONFLICTS.md)
Design: [ARCHITECTURE](docs/ARCHITECTURE.md) · [CONFIGURATION](docs/CONFIGURATION.md) ·
[INTEROPERABILITY](docs/INTEROPERABILITY.md) · [SECURITY](docs/SECURITY.md)
Ops & quality: [TEST_STRATEGY](docs/TEST_STRATEGY.md) · [OPERATIONS](docs/OPERATIONS.md) ·
[COST_ANALYSIS](docs/COST_ANALYSIS.md) · [RISK_REGISTER](docs/RISK_REGISTER.md)
Governance: [DECISIONS](docs/DECISIONS.md) · [PROMPT_BOOK](docs/PROMPT_BOOK.md)

## Git policy

Cursor performs **read-only** Git only. All commits/pushes/tags are done manually
by Alon or Renat. See [`.cursor/rules/00-manual-git.mdc`](.cursor/rules/00-manual-git.mdc).

## Submission

Deadline **12/08/2026 23:59** (no late submissions). Repository is public and
accessible to the lecturer (`rmisegal@gmail.com`).
