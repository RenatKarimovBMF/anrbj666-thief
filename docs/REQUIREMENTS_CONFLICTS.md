# Requirements Conflicts Log

Conflicts between authoritative documents are recorded here and **never silently
resolved**. Anything that materially affects grading, protocol compatibility,
security, or architecture is escalated to Alon/Renat before implementation.

Priority order: (1) Appendix F numeric table → (2) mandatory rules in the book v3.0.0
→ (3) course-site → (4) software guidelines → (5) example code → (6) earlier feedback.

Status legend: OPEN · NEEDS-HUMAN-DECISION · RESOLVED.
This file is kept consistent with the identical log in the police repo.

---

## C-001 — Board size example: 10×10 vs 7×7 (RESOLVED — not a true conflict)
- **Source A:** Book abstract, p. ii, gives "10×10" as an illustrative example of the board.
- **Source B:** §10.3.1 (p. 85) says the base grid "default 7×7".
- **Source C (authoritative):** Appendix F, Table 13#1 (p. 136): `[board size]` example **7×7**, status **MINIMUM**.
- **Resolution:** Per the book's own rule (only Appendix F is authoritative for numbers), the binding minimum is **7×7**, negotiable upward. The 10×10 mention is a non-binding illustration. No human decision required. Recorded for traceability.

## C-002 — "max_steps" vs "survival_threshold" both = 35 (RESOLVED for implementation — kept OPEN for lecturer clarification)
- **Observation:** Appendix F Table 15 lists `[step ceiling]`=35 (#3) and `[survival threshold]`=35 (#4) as separate MINIMUM parameters with the same example value.
- **Question:** Are these intended to always be equal (thief wins iff the game reaches the step ceiling), or independent (game could run longer than the survival threshold)?
- **Impact:** Win/termination logic (Stage 1). Medium grading impact. Directly affects the thief's survival-win condition.
- **Decision (user, 2026-07-13):** Treat `movement.max_steps` and `movement.survival_threshold` as **independent, individually configurable and individually validated** fields. Authoritative Appendix F defaults are `max_steps = 35` and `survival_threshold = 35` (default-equal). They **must not be coupled in code** — neither is derived from, nor asserted equal to, the other. Each is validated against its own MINIMUM (≥35) independently.
- **Implementation semantics (Stage 1):** thief survival win triggers when the completed step count reaches `survival_threshold`; the game additionally hard-stops at `max_steps`. With the default-equal values these coincide, but the engine evaluates them separately so unequal negotiated values behave correctly. See `DECISIONS.md` D-007 and Stage 1 termination tests.
- **Status:** RESOLVED for implementation (independent + default-equal). **Kept OPEN** for lecturer or match-level clarification; if the lecturer/opponent mandates strict equality, only config negotiation changes — no code coupling is introduced.

## C-003 — Tie score vs "technical loss 0/0" (RESOLVED — different scenarios)
- **Source A:** Appendix E, Rule 48 (p. 133) scores end scenarios "capture 20/5, survival 5/10, technical loss 0/0".
- **Source B:** Appendix F, Table 17#5 (p. 138): `[tie score]` = **2** each, CONSTANT.
- **Resolution:** No contradiction: "technical loss" (disqualification/forfeit) scores 0/0, whereas an **aggregate tie across the 6 sub-games** scores 2/2. Distinct scenarios. Recorded for the scoring engine (Stage 1 / Stage 7 results).

## C-004 — Start-position consistency under negotiation (OPEN — process note)
- **Observation:** NEGOTIABLE start positions (thief center [3,3], police corner [0,0]) assume size 7. If size is negotiated upward, start positions must be renegotiated consistently.
- **Impact:** Interoperability. Handled by config negotiation + schema validation, not a document conflict.
- **Status:** OPEN — enforce cross-field consistency in the config validator (Stage 1).

## C-005 — Rule 47 "thief with no legal move = captured" vs "stay" being legal (OPEN — interpretation, low risk)
- **Observation:** Appendix E Rule 47 says a thief with *no legal move* is captured, yet the movement set (Appendix F T15#1) always includes "stay", so a thief technically always has at least one legal action.
- **Interpretation (Stage 1):** "no legal move" means "no adjacent orthogonal cell the thief can step into" (fully walled in / cornered); staying in place does not count as an escape. Implemented in `game/capture.py::is_trapped` (police-occupied and barrier/off-board neighbours all count as blocked).
- **Impact:** Capture detection; directly determines when the thief loses by being cornered. Low — only affects fully-surrounded positions, which are rare and unambiguous in intent.
- **Status:** OPEN — confirm with lecturer if desired; no default-config game outcome depends on the edge case.

---

_No conflicts requiring an immediate blocking decision were found. C-002 is
resolved for implementation (independent, default-equal; see DECISIONS.md D-007)
and kept open only for optional lecturer clarification. C-005 records the Rule 47
"trapped" interpretation used by the Stage 1 capture engine._
