# Continuous Profound-Question Chain · Ω-D1 to Ω-D6

## Cycle protocol
Ask → Answer → Insight → Contribution → Decree → Next Question → Verify → Append.

- **Ω-D1:** Every verified answer generates at least one higher-capacity open question.
- **Ω-D2:** Rank candidate questions by Meta-Leverage; retain all unselected candidates.
- **Ω-D3:** Tag whether a candidate changes question generation, scoring, memory, or selection machinery.
- **Ω-D4:** Version scoring profiles additively; never silently rewrite historical scores.
- **Ω-D5:** Recursive impact never overrides evidence, safety, authorization, or reversibility gates.
- **Ω-D6:** Each completed cycle records a follow-up question, evidence status, and uncertainty note.

## Default scoring heuristic
Meta-Leverage = 35% leverage density + 25% evidence readiness + 20% dependency clarity + 20% recursive self-reference bonus. Subtract 20% of execution cost and 35% of safety risk; clamp the score to [0,1]. Each input is bounded [0,1]. This is a prioritization heuristic, not an objective truth metric.

## Evidence and integrity
The Python module implements deterministic ranking, JSONL append-only cycle recording, and hash-link verification. Local hashes are tamper-evident, not immutable against a privileged actor who can rewrite the ledger and recompute hashes. No network calls or autonomous code execution are enabled.
