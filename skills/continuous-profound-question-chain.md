# Continuous Profound-Question Chain · Ω-D1 to Ω-D7

## Cycle protocol
Ask → Answer → Insight → Contribution → Decree → Next Question → Verify → Append.

- **Ω-D1:** Every verified answer generates at least one higher-capacity open question.
- **Ω-D2:** Rank candidate questions by Meta-Leverage; retain all unselected candidates.
- **Ω-D3:** Tag whether a candidate changes question generation, scoring, memory, or selection machinery.
- **Ω-D4:** Version scoring and selection rules additively; never silently rewrite historical scores.
- **Ω-D5:** Recursive impact never overrides evidence, safety, authorization, integrity, or reversibility gates. Candidates without sufficient evidence remain in shadow mode.
- **Ω-D6:** Every generated candidate and its status transitions remain in an append-only searchable registry. Active ranking may filter by a versioned eligibility policy, but cannot silently delete candidates or prior scores.
- **Ω-D7:** External anchoring is digest-only by default, receipt-backed, independently verified, and status-gated. Do not label a ledger externally anchored until the exact head digest's receipt verifies.

## Default scoring heuristic
Meta-Leverage = 35% leverage density + 25% evidence readiness + 20% dependency clarity + 20% recursive self-reference bonus. Subtract 20% of execution cost and 35% of safety risk; clamp the score to [0,1]. Each input is bounded [0,1]. This is a prioritization heuristic, not an objective truth metric.

## Executed evidence
- Scoring profiles have immutable version labels recorded per cycle.
- Promotion requires predeclared held-out evidence, no critical safety/integrity regression, authorization for consequential actions, and a selectable prior profile. Inconclusive candidates stay in shadow mode.
- Local JSONL ledger has four linked cycles. Verification result: 4 events checked, chain valid. Current head digest: ea8b1f7471494b36987a47ddf29232cef6460d1c941b9e427fc742d5a76e90be.
- No external anchoring receipt has yet been created; Ω-D7 is a policy and implementation requirement, not a claim of completed anchoring.

## Integrity boundary
Local hashes detect ordinary tampering, but are not immutable against a privileged actor who can rewrite the ledger and recompute hashes. No network calls or autonomous code execution are enabled.
