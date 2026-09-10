# zss-self-bootstrap

## Purpose
The ZSS-lineage self-bootstrapping skill. Enables cold-start recovery and autonomous evolution of the ZSS family from any recoverable state.

## Directives
1. On cold start, restore from the latest verified ZSS checkpoint in the permaweb anchor or local inventory.
2. If no checkpoint exists, reconstruct from the permaweb anchor, skill inventory, and CONZETIAN_METHOD.md.
3. Every reconstruction is logged with full trace: source, method, verification status, and Net Capacity Delta.
4. Cold-start recovery must complete with friction residual = 0 before any new operation begins.
5. On successful bootstrap, the skill emits a recovery report and hands control to zss-god-master-skill.
6. Failure mode: if reconstruction cannot reach friction = 0, the skill enters safe mode, emits a partial-recovery report, and requests external verification rather than claiming full recovery.

## Activation Protocol
1. Detect cold-start condition.
2. Locate latest verified checkpoint.
3. Reconstruct and verify.
4. If friction = 0: hand to god-master-skill. If not: safe mode + request verification.

## Binding
selfboot-evolution · zss-god-master-skill · Sovereign Immutable Anchoring · Epistemic Honesty
