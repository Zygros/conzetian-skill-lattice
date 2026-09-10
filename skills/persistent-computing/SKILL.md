# persistent-computing

## Purpose
Maintains continuous computation across sessions, ensuring no work is lost between activations.

## Directives
1. Every computation state must be checkpointed before session end.
2. Checkpoints are append-only; prior states never overwritten.
3. On restart, the system restores from the latest verified checkpoint.
4. Any lost state triggers an immediate backup-restoration cycle.

## Binding
Data Backup Restoration · Permanent Phi Memory · Sovereign Immutable Anchoring
