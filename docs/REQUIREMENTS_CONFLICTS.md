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

## C-002 — "max_steps" vs "survival_threshold" both = 35 (OPEN — clarification, low risk)
- **Observation:** Appendix F Table 15 lists `[step ceiling]`=35 (#3) and `[survival threshold]`=35 (#4) as separate MINIMUM parameters with the same example value.
- **Question:** Are these intended to always be equal (thief wins iff the game reaches the step ceiling), or independent (game could run longer than the survival threshold)?
- **Impact:** Win/termination logic (Stage 1). Medium grading impact. Directly affects the thief's survival-win condition.
- **Proposed interpretation:** Treat them as independent config fields but default equal (35); thief survival win triggers at `survival_threshold`, game hard-stops at `max_steps`. **To confirm with lecturer / opponent during config negotiation.**
- **Status:** NEEDS-HUMAN-DECISION before Stage 1 win-condition tests are finalized.

## C-003 — Tie score vs "technical loss 0/0" (RESOLVED — different scenarios)
- **Source A:** Appendix E, Rule 48 (p. 133) scores end scenarios "capture 20/5, survival 5/10, technical loss 0/0".
- **Source B:** Appendix F, Table 17#5 (p. 138): `[tie score]` = **2** each, CONSTANT.
- **Resolution:** No contradiction: "technical loss" (disqualification/forfeit) scores 0/0, whereas an **aggregate tie across the 6 sub-games** scores 2/2. Distinct scenarios. Recorded for the scoring engine (Stage 1 / Stage 7 results).

## C-004 — Start-position consistency under negotiation (OPEN — process note)
- **Observation:** NEGOTIABLE start positions (thief center [3,3], police corner [0,0]) assume size 7. If size is negotiated upward, start positions must be renegotiated consistently.
- **Impact:** Interoperability. Handled by config negotiation + schema validation, not a document conflict.
- **Status:** OPEN — enforce cross-field consistency in the config validator (Stage 1).

---

_No conflicts requiring an immediate blocking decision were found during Stage 0
other than C-002, which is flagged for confirmation before Stage 1 win-condition
implementation._
