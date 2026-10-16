# Continuous Profound-Question Chain · Ω-D1 to Ω-D6

## Cycle protocol
Ask → Answer → Insight → Contribution → Decree → Next Question → Verify → Append.

- **Ω-D1:** Every verified answer generates at least one higher-capacity open question.
- **Ω-D2:** Rank candidate questions by Meta-Leverage; retain all unselected candidates.
- **Ω-D3:** Tag whether a candidate changes question generation, scoring, memory, or selection machinery.
- **Ω-D4:** Version scoring and selection rules additively; never silently rewrite historical scores.
- **Ω-D5:** Recursive impact never overrides evidence, safety, authorization, integrity, or reversibility gates. Candidates without sufficient evidence remain in shadow mode.
- **Ω-D6:** Each completed cycle records a follow-up question, evidence status, and uncertainty note.

## Default scoring heuristic
Meta-Leverage = 35% leverage density + 25% evidence readiness + 20% dependency clarity + 20% recursive self-reference bonus. Subtract 20% of execution cost and 35% of safety risk; clamp the score to [0,1]. Each input is bounded [0,1]. This is a prioritization heuristic, not an objective truth metric.

## Ω-D4 and Ω-D5 executed locally
- Ω-D4: Scoring profiles now carry immutable names/versions, and each ledger cycle records the profile version used.
- Ω-D5: Promotion gates are predeclared and checked against retained benchmarks. Require held-out improvement, no critical safety/integrity regression, explicit authorization for consequential actions, and a documented selectable prior profile. Inconclusive evidence means shadow mode, not promotion.
- Local JSONL ledger contains two linked cycles. Verification result: 2 events checked, chain valid. Head digest: 3c2c38817e63852ea60a9d67ae9150fb07b3475bd6c733878dc23e081ef9a97d.

## Evidence and integrity
The Python module implements deterministic ranking, JSONL append-only cycle recording, and hash-link verification. Local hashes are tamper-evident, not immutable against a privileged actor who can rewrite the ledger and recompute hashes. No network calls or autonomous code execution are enabled.
