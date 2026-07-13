# Security & Secret Management — Thief

## Secrets policy
Never read, print, copy, summarize, or commit secret values. Potential secret files:
`.env`, `credentials.json`, `token.json`, OAuth client secrets, refresh/access tokens,
API keys, ngrok/tunnel tokens, private certificates, service-account credentials.

- All such files are git-ignored (see `.gitignore`); only `.env.example` with obvious
  placeholders is committed (Appendix E, Rule 40 makes ignoring credentials mandatory).
- Secrets are never sent to an LLM prompt, test log, Markdown doc, or GitHub.
- Before every manual commit checkpoint: review the changed-file list, scan for
  accidental secrets, verify `.gitignore`, and warn without exposing contents.

## Cryptographic integrity (Stage 6, Chapter 5)
- **Commit-Reveal over SHA-256** (Rule 17): each move is committed as
  `SHA256(canonical_payload ‖ nonce)`, revealed next turn. Deterministic canonical
  serialization is mandatory so both sides hash identically (see INTEROPERABILITY.md).
- **Nonce** (Rule 18): fresh, cryptographically random, kept strictly secret until
  reveal; never reused. Dictionary-attack resistance required.
- **Verification** (Rule 19): any hash mismatch at reveal ⇒ immediate technical loss
  (score 0) for the cheating side; enforced by deterministic Python, not the LLM.
- **Step-0** (Rule 24): signed hardware declaration before the game; failure forfeits
  the computational-fairness bonus.
- **Emission model lock** (Rule 23): the scent emission/decay formula is crypto-locked
  before the game; deviation invalidates the game. The thief is the primary emitter.

## Log & audit integrity (Rule 20, 36)
Structured, append-only, auditable logs enable full replay verification. Mutual audit
at the end of each game is a precondition for agreeing on the shared result JSON.

## Network hardening (Appendix F T19; Rules 28–30)
Central Gatekeeper enforces rate limit (≥30 rpm), parallelism (≥2), retry (≥3 after
≥5 s), queue depth (≥100), response timeout, and a DOS guard. Gmail access uses a
send-only OAuth scope (Rule 30). Handle Google `429` by backing off, never hammering.

## Threat notes
- **Malicious peer input:** validate/reject every incoming message; never trust peer
  claims about our hidden state (e.g. a false capture claim by the police, Rule 21–22).
- **Information leakage (Rule 2, 8, 9, 39):** GUI shows local truth only; never render
  the full objective board; never push secrets/tokens to the repo even if private.
- **LLM injection:** treat LLM output as untrusted text; parse defensively; never let
  it influence rule enforcement or crypto.

## Security testing (see TEST_STRATEGY.md)
Commit-Reveal success/mismatch, invalid nonce, replay tampering, log-integrity,
malformed/incompatible messages, timeout/watchdog, Gatekeeper budget, secret-scan of
changed files. Tests requiring paid APIs / Gmail send / tunnels / a second machine are
marked and disabled by default.
