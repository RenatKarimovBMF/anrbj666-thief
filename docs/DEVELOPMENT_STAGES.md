# Development Stages

**Authoritative source for the official sequence:** `police_thief_p2p.pdf` v3.0.0,
**Chapter 10.3 "The Seven Development Priorities"**, book pages **85–88**
(PDF sheets 100–103); milestone checklist **§10.4, pp. 88–89**; summary
**Table 3, p. 87**. The order below is preserved exactly as written and must not
be reordered. Stage 0 (setup) and a Final hardening stage wrap the official seven.

Each stage runs **end-to-end** before the next is added (§10.4, "do not skip
ahead", p. 89). Every stage ends at a **manual commit checkpoint**; Cursor never
commits.

## Stage 0 — Requirements, repository setup & planning (wrapper, not from the book)
- Audit workspace; verify the two independent repos; create Cursor manual-Git rules.
- Create planning docs, requirements matrix, conflict log, architecture/security/test plans.
- Create safe `.gitignore`, `.env.example`, `pyproject.toml`, config skeletons, package skeleton.
- **No production game implementation.**
- Acceptance: docs present; skeletons import-clean; ruff clean on skeleton; no secrets staged.

## Stage 1 — Base Logic (§10.3.1, p. 85; builds on Ch. 3)
Grid of `board.size` (Appendix F T13#1, min 7×7), movement rules (orthogonal + stay),
`movement.barrier_quota` (min 14), capture detection by coordinate overlap. Single process, no networking, no AI.
- **Thief-specific:** legal evasion moves; recognizing capture states (overlap = caught,
  Rule 48; trapped-by-barrier = caught, Rule 46; no-legal-move = caught, Rule 47); the
  thief never places barriers.
- Milestone (§10.4): two agents move legally on the grid; over-quota barrier rejected; overlap triggers capture.

## Stage 2 — Basic FastMCP Infrastructure (§10.3.2, p. 86; builds on Ch. 2)
Split into separate processes; FastMCP servers + geometric Tools; numeric-coordinate messages over localhost.
- Milestone: a geometric message from peer A over localhost is received & parsed correctly by peer B.

## Stage 3 — "Blind" Strategy Module (§10.3.3, p. 86; builds on Ch. 6)
First decision core (heuristic / LLM-mapped policy / optional Bellman-Q). No scent, language, or deception yet.
- **Thief-specific:** `ThiefBrain._pick_move` chooses an evasion/survival step given belief.
- Milestone: given a known threat cell, the agent computes and executes a maximizing-escape legal move without manual help.

## Stage 4 — Language and Scent (§10.3.4, p. 86; builds on Ch. 4 + Ch. 6)
Replace numeric reports with **free-language** dialogue; pheromone vectors + decay
(Appendix F T16: source 0.9, decay 0.10, 5×5 field); LLM for inference & bluffing.
- **Thief-specific:** the thief emits scent as it moves and may bluff verbally to mislead the police.
- Milestone: free-language hint translated to inference; scent map updates & decays each step; LLM emits a hint (true or false).

## Stage 5 — Cloud Exposure and Tunneling (§10.3.5, p. 86; builds on Ch. 2)
Move localhost → public addresses via ngrok/localtonet; connect remote machines.
- Milestone: an agent on a remote machine connects via tunnel and plays a full round vs the local agent.

## Stage 6 — Security and Cryptography (§10.3.6, p. 87; builds on Ch. 5)
Wrap the working link in **Commit-Reveal** over SHA-256, add the **Nonce** generator, integrate **Step-0** hardware declarations.
- Milestone: a move is Committed then Revealed with a valid nonce; Step-0 verifies hardware.

## Stage 7 — Reporting and Visualization Shell (§10.3.7, p. 87; builds on Ch. 9, Ch. 7, App. A)
**Gmail API over OAuth 2.0**, finish **Live GUI** (belief heatmap + turn banner), polish **Replay App** with verification.
- Milestone: end-of-game summary emailed via Gmail; GUI shows state; Replay reconstructs a recorded round → "Verified OK".

## Final Stage — Submission hardening (wrapper, not from the book)
Complete both READMEs; verify clean-env `uv sync` + locked deps; tests; ≥85% coverage;
ruff zero; two-machine/public-network operation; live GUIs; replay integrity;
Commit-Reveal validation; audit logs; Gmail reporting; OAuth docs; 4 required JSON
artifacts; screenshots; cost analysis; prompt history; no secrets; complete requirements
matrix. Prepare exact **manual** annotated Git tag commands (never create tags via Cursor).

## Per-stage workflow (applied every implementation stage)
Re-read sources → update requirements matrix → update relevant PRD → PLAN → TODO →
acceptance criteria → write/update tests → implement smallest slice → targeted tests →
full suite → coverage → ruff → type check → security/config checks → docs → evidence →
PROMPT_BOOK → self-review → **manual commit checkpoint** → STOP.
