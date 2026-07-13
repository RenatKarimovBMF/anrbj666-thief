# Risk Register — Thief

Likelihood (L) / Impact (I): Low / Med / High. Ordered by severity.

| ID | Risk | L | I | Mitigation | Owner |
|---|---|---|---|---|---|
| RK-01 | Accidental secret committed (token/credentials) | Med | High | `.gitignore` + pre-commit human secret scan + Rule 40; only `.env.example` | Alon/Renat |
| RK-02 | Non-deterministic hashing breaks cross-group Commit-Reveal | Med | High | canonical UTF-8 sorted-key serialization + golden hash fixtures (Stage 6) | team |
| RK-03 | Hidden centralization (shared state/judge) creeps in | Low | High | architecture review each stage; Zero-Trust tests (Rules 1,2) | team |
| RK-04 | LLM used to decide moves / enforce rules | Low | High | deterministic Python for all rules; LLM = text only (Rule 25) | team |
| RK-05 | Interop failure vs other groups (schema drift) | Med | High | mandatory public contract + valid/invalid fixtures + version negotiation | team |
| RK-06 | <2 valid league games ⇒ no passing grade | Med | High | schedule games early; keep template mode reliable (Rule 31, 52) | Alon/Renat |
| RK-07 | Coverage < 85% or ruff violations at submission | Med | Med | TDD, CI-style local checks each stage | team |
| RK-08 | Skipping stages ⇒ unbounded debugging | Low | High | enforce end-to-end milestone per stage (§10.4) | team |
| RK-09 | Paid API cost overrun | Low | Med | template default; Gatekeeper caps; approval gate | team |
| RK-10 | Deadline miss (12/08/2026) | Low | High | milestone tracking; hardening stage buffer | Alon/Renat |
| RK-11 | Config mismatch between peers (not byte-identical) | Med | High | crypto-lock + hash-compare shared config (Rule 11) | team |
| RK-12 | GUI leaks full/objective board (Rule 8,9) | Low | High | render local belief only; review screenshots | team |
| RK-13 | Cursor performs a Git write | Low | High | persistent rule `00-manual-git.mdc`; human-only commits | all |
| RK-14 | Thief mis-detects capture-by-barrier / no-legal-move (Rules 46,47) | Med | Med | dedicated Stage 1 tests for trapped and blocked states | team |
