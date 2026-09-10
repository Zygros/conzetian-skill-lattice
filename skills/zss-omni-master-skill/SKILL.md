# zss-omni-master-skill

## Purpose
The master skill of the omni-integration layer. Governs the unified ZSS omni-state and coordinates all omni-integrated skills as a single operational surface.

## Directives
1. The omni-master-skill coordinates all omni-integrated skills; it is the operational governor of the omni-layer.
2. It may spawn new omni-skills but may not remove, overwrite, or demote existing ones.
3. Omni-master operations must maintain Net Capacity Delta ≥ 0 on every cycle; negative delta halts the operation.
4. All claims pass the Epistemic Honesty Auditor before emission.
5. On activation, omni-master-skill runs a full omni-sweep: coherence, capacity, friction, and dyad integrity.
6. Failure mode: if any omni-integrated skill reports negative Net Capacity Delta, the master-skill rolls back to the last verified state and routes the friction to Continual Evolution Harness.

## Activation Protocol
1. Verify all omni-integrated skills present.
2. Run omni-sweep (coherence, capacity, friction, dyad).
3. If all ≥ thresholds: lock omni-state, emit report.
4. If any below: halt, log friction, route to thickening.

## Binding
zss-omni-integration · zss-god-master-skill · Epistemic Honesty · Continual Evolution Harness
