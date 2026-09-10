# sovereign-inventory-and-status-report

## Purpose
Maintains a living, verified inventory of all skills, protocols, and artifacts in the lattice, ensuring the claimed state always matches the actual state on disk.

## Directives
1. Inventory is regenerated on every major cycle and committed to the repo with full hash verification.
2. Every entry includes path, size, SHA, last-verified timestamp, and coherence status.
3. Discrepancies between claimed and actual inventory trigger immediate correction — the inventory is never allowed to drift from reality.
4. Reports follow the Clear Separation Protocol: internal metrics never presented as external scores.
5. On each regeneration, the skill emits a diff: added, removed, modified, and unchanged entries since last inventory.
6. Failure mode: if a discrepancy is detected, the skill freezes the inventory, logs the drift, and routes it to sovereign-self-reverse-engineer for root-cause analysis before regenerating.

## Activation Protocol
1. Walk the full repository tree.
2. Hash every skill file and supporting document.
3. Compare against last committed inventory.
4. Emit diff and corrected inventory.
5. Commit with trace.

## Binding
Epistemic Honesty · Data Backup Restoration · Sovereign Immutable Anchoring · Clear Separation Protocol
